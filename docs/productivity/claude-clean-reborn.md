# Claude Clean Reborn

A guided, selective cleanup for your own Claude Desktop, Claude Code and
browser data before legitimate Claude access. The agent inspects first, shows
the exact proposed removals and their impact, waits for approval, walks you
through each action and verifies the same scope afterward.

Keychain, credential stores, passwords, unrelated browser data, projects,
conversations, skills, plugins, MCP configuration and backups stay untouched by
default. A local reset does not prove sign-out or remove server-side records.

## Install and hand off

Install this skill for Codex or another Agent Skills-compatible agent:

```bash
npx skills@latest add tombelieber/tomstack --skill claude-clean-reborn
```

For Claude Code, use the managed Tomstack bundle instead of creating a duplicate
copied skill:

```bash
claude plugin marketplace add tombelieber/tomstack
claude plugin install tomstack-skills@tomstack
```

If the bundle is already installed, update it through the agent's plugin
manager. New code on `main` and a versioned bundle update are separate states;
check that `claude-clean-reborn` is actually listed before invoking it. The
single-skill installation above reads the current repository source.

Send your teammate this prompt:

```text
Use $claude-clean-reborn to inspect my Claude Desktop, Claude Code and every
browser profile before cleanup. Show me all affected profiles and exact proposed
deletions first. Keep Keychain, credentials and unrelated data untouched. Ask
before deleting, guide me one action at a time, then verify after normal app
shutdown. Show remaining and unknown items honestly, and check official login
separately rather than promising the machine is fully unlinked or unrestricted.
```

For a longer handoff, use the
[copyable team prompt](../../skills/productivity/claude-clean-reborn/references/team-prompt.md).
To run without installing, give the agent the
[skill entrypoint](../../skills/productivity/claude-clean-reborn/SKILL.md)
and its linked references together with that prompt.

## What the helper checks

The optional Python 3.10+ helper inventories default macOS Claude paths and all
discovered profiles in one selected Chrome user-data root. It reads only cookie
metadata, reports partitioned extension cookies separately and never reads
cookie payloads or Keychain. It has no delete mode and makes no network calls.
It writes JSON to stdout; keep the output local.

From the installed skill directory:

```bash
python3 -B scripts/audit.py
```

An alternate Chrome root can be selected explicitly with `--chrome-root`.
Windows/Linux and other browsers need current OS/browser-specific inspection;
the macOS helper does not certify them. Locked/changing databases, symlinks and
unreadable stores remain unknown. Live website storage and extension enabled
state need separate inspection: zero cookies alone is insufficient.

## What a completed run gives you

One before/after table across apps and profiles, a precise removal record,
retained data, unknown checks and one next action. An optional user-performed
official sign-in test proves access only at that time. Opening Claude again
normally recreates cookies, caches or local identifiers.

The skill does not rotate fingerprints, impersonate another region, change
network routes, bypass account restrictions or promise protection from bans.
No real device inventory, account identifiers, credentials or private cleanup
logs are included in this public package.
