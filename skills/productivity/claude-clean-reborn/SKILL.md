---
name: claude-clean-reborn
description: Use when a user wants guided local Claude Desktop, Claude Code, or browser cleanup before a legitimate fresh sign-in, especially across Chrome profiles or with persistent Claude extension cookies.
---

# Claude Clean Reborn

Guide the device owner through a reviewable local cleanup and a measured access
check. “Reborn” means an agreed local reset, not a new identity certificate or a
promise about account restrictions. Use official sign-in and support routes;
do not turn this into fingerprint spoofing, region impersonation or ban evasion.

## 1. Agree the scope, then inspect

Reuse the user's choices. Establish OS, installed Claude surfaces, browsers,
custom data roots and desired outcome: cache repair, selected website-data
removal, local reset or sign-out. Default to preserving Keychain, credential
stores, passwords, history, projects, skills, plugins, MCP settings and backups.
Read [local-data.md](references/local-data.md) for local paths and
[browser-data.md](references/browser-data.md) when browsers are included.

On macOS, run `python3 -B <skill-dir>/scripts/audit.py` for metadata only. It
writes JSON to stdout, with no network requests or source mutations. Inspect
all discovered Chrome profiles, including profiles missing from `Local State`.
An explicit `--chrome-root` supports another user-data root; it does not discover
every browser/channel. Other OSes require current official path verification.

## 2. Show a preview and wait for approval

Present one combined table: app/profile, exact path or site/extension partition,
observed state, proposed action, loss/sign-out impact, retained data and unknowns.
Separate required cleanup from optional retained material. Ask for approval of
that concrete scope before destructive actions; reuse existing exact approval.
A later instruction to preserve something overrides earlier broad cleanup.

Never read/decrypt cookie values, tokens or passwords to identify cleanup
targets. Keychain stays untouched unless the owner separately authorizes an
exact supported operation; do not request their Keychain password. Sign-out
can itself update credentials, so explain that effect before offering it.

## 3. Guide the approved changes

Ask the user to save work and normally quit affected apps before disk cleanup
or final verification. If this assistant itself runs in Claude using the target
root, hand the final cleanup/check to another agent or the user after exit;
continuing this session can recreate the data. Do not force-kill a working
session. Give one bounded
action at a time, in the user's language, with progress and the expected result.
Use supported app/browser controls. Respect tool restrictions; when automation
is blocked, use a manual walkthrough rather than another API or filesystem
workaround. Never delete an entire Chrome profile or Claude data root as a
shortcut. Do not touch unrelated data or publish local reports.

## 4. Verify the actual state

Repeat the same scoped observations after normal shutdown. Report each profile
and surface together: **verified**, **remaining**, **retained** or **unknown**.
Locked/changing databases are unknown, never zero. A cookie count of zero says
nothing about unread website storage. Raw LevelDB strings can be deleted records;
they are not proof of live identity data. A successful command response is not
proof of deletion. Diagnose the exact partition/store before retrying.

Apps can recreate caches and IDs on launch; compare timestamps and rerun scoped
checks instead of repeatedly deleting. Preserve useful uncertainty. After three
failed attempts, stop mutation and name the doubtful assumption.

## 5. Hand off access readiness

Use [readiness.md](references/readiness.md). Separate local cleanup, retained
authentication, network reachability and a user-observed official sign-in.
Never call the machine “good to go” from a green local checklist alone. Finish
with the before/after table, retained/unknown items and one next action. The
[team prompt](references/team-prompt.md) is the copyable starting handoff.
