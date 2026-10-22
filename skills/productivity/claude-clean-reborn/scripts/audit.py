"""Metadata-only inventory of default macOS Claude and Chrome stores. Never deletes."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
from urllib.parse import urlsplit


DOMAINS = ("claude.ai", "anthropic.com", "claude.com", "claudeusercontent.com", "claude.site")
EXTENSION_ID = "fcoeoabgfenejglbffodgkkbkcdhcgfn"
EXTENSION_ORIGIN = "chrome-extension://" + EXTENSION_ID
PROFILE = re.compile(r"(?:Default|Profile \d+|Guest Profile|System Profile)\Z")
IDENTITY_FIELDS = ("userID", "machineID", "anonymousId", "oauthAccount")
DESKTOP_STATE = (
    "ant-did", "ant-device-registry.json", "Cookies", "Local Storage",
    "Session Storage", "IndexedDB", "WebStorage", "SharedStorage",
    "Shared Dictionary", "DIPS", "Trust Tokens", "Network Persistent State",
    "TransportSecurity", "blob_storage", "Network", "Service Worker",
)
DESKTOP_CACHE = ("Cache", "Code Cache", "GPUCache", "DawnGraphiteCache", "DawnWebGPUCache", "Crashpad", "sentry")


def unsafe(path):
    return any(p.is_symlink() for p in (path, *path.parents))


def metadata(path, home):
    label = "~/" + str(path.relative_to(home)) if path.is_relative_to(home) else str(path)
    try:
        if unsafe(path):
            return {"path": label, "status": "unknown", "reason": "symlink_not_followed"}
        s = path.stat()
        return {"path": label, "status": "present", "kind": "directory" if path.is_dir() else "file",
                "file_bytes": s.st_size if path.is_file() else None}
    except FileNotFoundError:
        return {"path": label, "status": "absent"}
    except OSError as error:
        return {"path": label, "status": "unknown", "reason": type(error).__name__}


def read_json(path):
    if unsafe(path):
        raise ValueError("symlink_not_followed")
    if path.stat().st_size > 10_000_000:
        raise ValueError("oversized_metadata")
    return json.loads(path.read_text(encoding="utf-8"))


def target_host(host):
    host = str(host or "").lower().lstrip(".")
    return any(host == domain or host.endswith("." + domain) for domain in DOMAINS)


def target_partition(value):
    try:
        return value == EXTENSION_ORIGIN or target_host(urlsplit(value or "").hostname)
    except ValueError:
        return False


def pending(path):
    for suffix in ("-wal", "-journal", "-shm"):
        sidecar = path.with_name(path.name + suffix)
        if unsafe(sidecar) or (sidecar.exists() and sidecar.stat().st_size):
            return True
    return False


def cookie_metadata(path, home):
    item = metadata(path, home)
    item.update(target_row_count=None, extension_partition_row_count=None, rows=[])
    if item["status"] == "absent":
        item.update(target_row_count=0, extension_partition_row_count=0)
        return item
    if item["status"] != "present":
        return item
    try:
        if pending(path):
            raise ValueError("database_sidecar_present_close_app_first")
        before = path.stat()
        connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=0.2)
        try:
            connection.execute("PRAGMA query_only=ON")
            # Even a future accidental SELECT * cannot read cookie payload columns.
            def authorize(action, table, column, *_):
                if action == sqlite3.SQLITE_READ and column in ("value", "encrypted_value"):
                    return sqlite3.SQLITE_DENY
                return sqlite3.SQLITE_OK
            connection.set_authorizer(authorize)
            columns = {r[1] for r in connection.execute("PRAGMA table_info(cookies)")}
            partition = "top_frame_site_key" if "top_frame_site_key" in columns else "NULL"
            ancestor = "has_cross_site_ancestor" if "has_cross_site_ancestor" in columns else "NULL"
            rows = []
            for host, name, cookie_path, key, cross in connection.execute(
                f"SELECT host_key, name, path, {partition}, {ancestor} FROM cookies"
            ):
                if target_host(host) or target_partition(key):
                    rows.append({"host": host, "name": name, "path": cookie_path,
                                 "partition_key": key,
                                 "has_cross_site_ancestor": bool(cross) if cross is not None else None})
        finally:
            connection.close()
        after = path.stat()
        if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns) or pending(path):
            raise ValueError("database_changed_during_read")
        item.update(status="readable", rows=rows, target_row_count=len(rows),
                    extension_partition_row_count=sum(r["partition_key"] == EXTENSION_ORIGIN for r in rows))
    except (OSError, sqlite3.Error, ValueError) as error:
        item.update(status="unknown", reason=str(error) if isinstance(error, ValueError) else type(error).__name__)
    return item


def chrome_inventory(root, home):
    result = {"root": metadata(root, home), "profiles": [], "profile_registry": "unknown"}
    if result["root"]["status"] != "present":
        return result
    cache = {}
    try:
        cache = read_json(root / "Local State").get("profile", {}).get("info_cache", {})
        if not isinstance(cache, dict):
            raise ValueError("invalid_profile_registry")
        result["profile_registry"] = "readable"
    except (OSError, ValueError, AttributeError, TypeError):
        cache = {}
    try:
        names = {p.name for p in root.iterdir() if PROFILE.fullmatch(p.name)}
    except OSError:
        result["root"].update(status="unknown", reason="profile_enumeration_failed")
        return result
    names.update(name for name in cache if PROFILE.fullmatch(name))
    for name in sorted(names):
        profile = root / name
        state = metadata(profile, home)
        known = cache.get(name, {})
        row = {"directory": name, "name": known.get("name", name) if isinstance(known, dict) else name,
               "directory_status": state["status"], "cookie_databases": [],
               "storage_artifacts": [], "extension_artifacts": []}
        for relative in ("Cookies", "Network/Cookies", "Extension Cookies"):
            database = cookie_metadata(profile / relative, home)
            if database["status"] != "absent":
                row["cookie_databases"].append(database)
        if not row["cookie_databases"]:
            row["cookie_databases"].append(cookie_metadata(profile / "Cookies", home))
        row["storage_artifacts"] = [metadata(profile / n, home) for n in ("Local Storage", "Session Storage", "IndexedDB", "Service Worker")]
        row["extension_artifacts"] = [metadata(profile / n / EXTENSION_ID, home) for n in
                                      ("Extensions", "Local Extension Settings", "Sync Extension Settings", "Managed Extension Settings")]
        result["profiles"].append(row)
    return result


def audit(home, chrome_root):
    desktop = home / "Library/Application Support/Claude"
    config_status = metadata(home / ".claude.json", home)
    fields = {key: None for key in IDENTITY_FIELDS}
    if config_status["status"] == "absent":
        fields = {key: False for key in IDENTITY_FIELDS}
    elif config_status["status"] == "present":
        try:
            config = read_json(home / ".claude.json")
            if not isinstance(config, dict):
                raise ValueError("invalid_config")
            fields = {key: key in config for key in IDENTITY_FIELDS}
        except (OSError, ValueError):
            config_status.update(status="unknown", reason="config_unreadable")
    code_paths = (".claude/cache", ".claude/telemetry", ".claude/paste-cache", ".claude/stats-cache.json",
                  "Library/Caches/claude-cli-nodejs", ".claude/projects", ".claude/history.jsonl",
                  ".claude/skills", ".claude/plugins", ".claude/backups", ".claude.json.backup")
    desktop_external = ("Library/Caches/com.anthropic.claudefordesktop",
                        "Library/Caches/com.anthropic.claudefordesktop.ShipIt",
                        "Library/Logs/Claude", "Library/HTTPStorages/com.anthropic.claudefordesktop")
    partitions = []
    partition_root = desktop / "Partitions"
    if metadata(partition_root, home)["status"] == "present":
        try:
            for child in sorted(partition_root.iterdir()):
                if metadata(child, home).get("kind") == "directory":
                    partitions.append({"partition": child.name, "cookies": cookie_metadata(child / "Cookies", home)})
        except OSError:
            partitions.append({"status": "unknown", "reason": "partition_enumeration_failed"})
    return {
        "schema_version": 1, "checked_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "default macOS Claude paths and selected Chrome user-data root",
        "readiness": "not_assessed", "keychain_accessed": False, "cookie_values_read": False,
        "claude_code": {"config": config_status, "identity_fields": fields,
                        "artifacts": [metadata(home / p, home) for p in code_paths]},
        "desktop": {"artifacts": [metadata(desktop / n, home) for n in (*DESKTOP_STATE, *DESKTOP_CACHE,
                     "config.json", "claude_desktop_config.json", "Partitions", "local-agent-mode-sessions", "vm_bundles")]
                     + [metadata(home / n, home) for n in desktop_external],
                    "preview_partitions": partitions},
        "chrome": chrome_inventory(chrome_root, home),
        "custom_config_dir_detected": bool(os.environ.get("CLAUDE_CONFIG_DIR")),
        "not_checked": ["Keychain, passwords, tokens and cookie payloads", "custom Claude profiles, other browsers and OS stores",
                        "live processes and in-memory browser state", "live LevelDB records, extension enabled state and saved passwords",
                        "network exit, service eligibility, server sessions and successful sign-in"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, help="macOS-shaped home (also supports disposable fixtures)")
    parser.add_argument("--chrome-root", type=Path, help="explicit Chrome user-data directory")
    args = parser.parse_args()
    if sys.platform != "darwin" and args.home is None:
        parser.error("automatic paths support macOS only; use current official OS guidance")
    home = (args.home or Path.home()).expanduser().absolute()
    root = (args.chrome_root or home / "Library/Application Support/Google/Chrome").expanduser().absolute()
    print(json.dumps(audit(home, root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
