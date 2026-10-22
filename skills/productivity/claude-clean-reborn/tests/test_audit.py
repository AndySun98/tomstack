"""Exercise the public audit command against disposable macOS-shaped homes."""
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit.py"
EXTENSION = "chrome-extension://fcoeoabgfenejglbffodgkkbkcdhcgfn"
SECRET = "fixture-secret-must-never-appear"


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name).resolve()
        self.chrome = self.home / "Library/Application Support/Google/Chrome"
        self.chrome.mkdir(parents=True)

    def run_audit(self):
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--home", str(self.home)],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(SECRET, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def database(self, profile, records, relative="Cookies", legacy=False):
        path = self.chrome / profile / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as db:
            suffix = "" if legacy else ", top_frame_site_key TEXT, has_cross_site_ancestor INTEGER"
            db.execute("CREATE TABLE cookies (host_key TEXT, name TEXT, path TEXT, value TEXT, encrypted_value BLOB" + suffix + ")")
            for host, name, partition in records:
                values = [host, name, "/", SECRET, SECRET.encode()]
                if not legacy:
                    values += [partition, 1]
                db.execute("INSERT INTO cookies VALUES (" + ",".join("?" for _ in values) + ")", values)
        return path

    def profiles(self, result):
        return {p["directory"]: p for p in result["chrome"]["profiles"]}

    def test_all_profiles_and_partition_metadata_without_secret_or_source_changes(self):
        (self.chrome / "Local State").write_text(json.dumps({"profile": {"info_cache": {
            "Default": {"name": "Personal"}, "Profile 7": {"name": "Work"},
        }}}))
        db = self.database("Default", [
            (".claude.ai", "cf_clearance", EXTENSION),
            ("claude.ai", "anthropic-consent-preferences", EXTENSION),
            ("claude.ai", "sessionKey", ""),
            ("claude.ai.evil.example", "unrelated", ""),
            ("example.com", "unrelated", ""),
        ])
        self.database("Profile 7", [], relative="Network/Cookies")
        (self.chrome / "Profile 9").mkdir()  # Not registered in Local State.
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.home.rglob("*") if p.is_file()}
        result = self.run_audit()
        profiles = self.profiles(result)
        self.assertEqual(set(profiles), {"Default", "Profile 7", "Profile 9"})
        self.assertEqual(profiles["Default"]["name"], "Personal")
        cookies = profiles["Default"]["cookie_databases"][0]
        self.assertEqual(cookies["status"], "readable")
        self.assertEqual(cookies["target_row_count"], 3)
        self.assertEqual(cookies["extension_partition_row_count"], 2)
        self.assertEqual({c["name"] for c in cookies["rows"]},
                         {"cf_clearance", "anthropic-consent-preferences", "sessionKey"})
        self.assertTrue(cookies["rows"][0]["has_cross_site_ancestor"])
        self.assertEqual(profiles["Profile 7"]["cookie_databases"][0]["target_row_count"], 0)
        self.assertEqual(profiles["Profile 9"]["cookie_databases"][0]["status"], "absent")
        after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in self.home.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertTrue(db.exists())
        self.assertEqual(result["readiness"], "not_assessed")

    def test_corrupt_database_is_unknown_not_zero(self):
        path = self.chrome / "Default/Cookies"
        path.parent.mkdir()
        path.write_bytes(b"not a SQLite database")
        row = self.profiles(self.run_audit())["Default"]["cookie_databases"][0]
        self.assertEqual(row["status"], "unknown")
        self.assertIsNone(row["target_row_count"])

    def test_pending_database_journal_is_unknown_and_left_untouched(self):
        path = self.database("Default", [("claude.ai", "sessionKey", "")])
        journal = path.with_name(path.name + "-journal")
        journal.write_bytes(b"pending transaction")
        row = self.profiles(self.run_audit())["Default"]["cookie_databases"][0]
        self.assertEqual(row["status"], "unknown")
        self.assertIsNone(row["target_row_count"])
        self.assertEqual(journal.read_bytes(), b"pending transaction")

    def test_legacy_schema_is_readable_without_inventing_partition_fields(self):
        self.database("Default", [(".anthropic.com", "sessionKey", "")], legacy=True)
        row = self.profiles(self.run_audit())["Default"]["cookie_databases"][0]
        self.assertEqual(row["target_row_count"], 1)
        self.assertEqual(row["extension_partition_row_count"], 0)
        self.assertIsNone(row["rows"][0]["partition_key"])

    def test_exclusively_locked_database_is_unknown_not_empty(self):
        path = self.database("Default", [("claude.ai", "sessionKey", "")])
        connection = sqlite3.connect(path)
        try:
            connection.execute("BEGIN EXCLUSIVE")
            row = self.profiles(self.run_audit())["Default"]["cookie_databases"][0]
            self.assertEqual(row["status"], "unknown")
            self.assertIsNone(row["target_row_count"])
        finally:
            connection.rollback()
            connection.close()

    def test_target_partition_is_detected_without_domain_substring_false_positives(self):
        self.database("Default", [
            ("third-party.example", "partitioned", "https://claude.ai"),
            ("third-party.example", "unrelated", "https://claude.ai.evil.example"),
            ("notclaude.ai", "unrelated", ""),
        ])
        row = self.profiles(self.run_audit())["Default"]["cookie_databases"][0]
        self.assertEqual(row["target_row_count"], 1)
        self.assertEqual(row["rows"][0]["name"], "partitioned")

    def test_symlinked_profile_is_unknown_without_following_it(self):
        outside = self.home / "unrelated"
        outside.mkdir()
        (outside / "Cookies").write_text(SECRET)
        (self.chrome / "Profile 8").symlink_to(outside, target_is_directory=True)
        row = self.profiles(self.run_audit())["Profile 8"]["cookie_databases"][0]
        self.assertEqual(row["status"], "unknown")
        self.assertIsNone(row["target_row_count"])
        self.assertEqual((outside / "Cookies").read_text(), SECRET)

    def test_local_identity_presence_and_preserved_history_are_separate(self):
        (self.home / ".claude.json").write_text(json.dumps({
            "userID": SECRET, "oauthAccount": {"token": SECRET},
            "projects": {"private-project": {"secret": SECRET}},
        }))
        (self.home / ".claude/projects").mkdir(parents=True)
        desktop = self.home / "Library/Application Support/Claude"
        desktop.mkdir(parents=True)
        (desktop / "ant-did").write_text(SECRET)
        result = self.run_audit()
        self.assertEqual(result["claude_code"]["identity_fields"], {
            "userID": True, "machineID": False, "anonymousId": False, "oauthAccount": True,
        })
        paths = {p["path"]: p for p in result["claude_code"]["artifacts"]}
        self.assertEqual(paths["~/.claude/projects"]["status"], "present")
        desktop_paths = {p["path"]: p for p in result["desktop"]["artifacts"]}
        self.assertEqual(desktop_paths["~/Library/Application Support/Claude/ant-did"]["status"], "present")

    def test_custom_config_and_invalid_profile_names_are_not_silently_certified(self):
        (self.chrome / "Local State").write_text(json.dumps({"profile": {"info_cache": {
            "../unrelated": {"name": "Untrusted"}, "Profile 2": {"name": "Work"},
        }}}))
        result = self.run_audit()
        self.assertNotIn("../unrelated", self.profiles(result))
        self.assertEqual(self.profiles(result)["Profile 2"]["directory_status"], "absent")
        self.assertIn("custom Claude profiles, other browsers and OS stores", result["not_checked"])

    def test_desktop_http_storage_and_external_caches_are_in_the_inventory(self):
        http = self.home / "Library/HTTPStorages/com.anthropic.claudefordesktop"
        http.mkdir(parents=True)
        result = self.run_audit()
        paths = {p["path"]: p["status"] for p in result["desktop"]["artifacts"]}
        self.assertEqual(paths.get("~/Library/HTTPStorages/com.anthropic.claudefordesktop"), "present")
        self.assertEqual(paths.get("~/Library/Caches/com.anthropic.claudefordesktop"), "absent")


if __name__ == "__main__":
    unittest.main()
