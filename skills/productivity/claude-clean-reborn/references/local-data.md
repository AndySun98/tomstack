# Local Claude data

Check installed versions, running processes and custom roots without printing
process arguments or environment secrets. Inventory first; these are discovery
candidates, not an authorized deletion list. Cache removal, sign-out and
identity-field removal have different effects.

## macOS candidates

| Surface | Candidates | Impact and default |
|---|---|---|
| Code cache | `~/.claude/cache`, `telemetry`, `paste-cache`, `stats-cache.json`; `~/Library/Caches/claude-cli-nodejs` | Rebuildable cache/log data; preview the actual existing paths |
| Code local account fields | `~/.claude.json`: `userID`, `machineID`, `anonymousId`, `oauthAccount` | Removing fields does not revoke authentication; edit only approved fields and verify all other values unchanged |
| Desktop device state | `~/Library/Application Support/Claude/ant-did`, `ant-device-registry.json` | Version-dependent local identifiers; recreated on launch; not server deletion |
| Desktop website state | Under the same Desktop root: `Cookies`, `Local Storage`, `Session Storage`, `IndexedDB`, `WebStorage`, related browser storage and `Network`; `~/Library/HTTPStorages/com.anthropic.claudefordesktop` | Can remove sign-in state, local drafts and website preferences; scope exact existing paths |
| Desktop cache | `Cache`, `Code Cache`, `GPUCache`, graphics caches, `Crashpad`, `sentry`; `~/Library/Caches/com.anthropic.claudefordesktop`; `~/Library/Logs/Claude` | Selective cache/diagnostics cleanup; not an account reset |

The helper reports presence, not a delete recommendation. Folder presence is
not proof it contains credentials. It does not parse live LevelDB records or
fully inventory Desktop's retained preview partitions.

Preserve `~/.claude/projects`, history, file history, settings, skills, plugins,
MCP config, backups, `.encryption_key`, Desktop config, preview `Partitions`,
Cowork sessions and VM bundles unless separately reviewed and authorized.
Old backups may retain account fields; disclose retention without deleting them.
Do not use `rm -rf ~/.claude` as a targeted reset.

## Credentials and shutdown

On macOS, Claude Code normally uses encrypted Keychain credentials; current
versions can fall back to `.credentials.json`. Custom `CLAUDE_CONFIG_DIR` changes
the scope. Do not inspect credential contents or call `claude auth status`
blindly: credential access is outside this metadata audit.

Keep `Claude Safe Storage` and `Claude Code-credentials` untouched by default.
Deleting an encryption key can strand retained data. Leaving credentials means
file cleanup cannot prove sign-out. If the user requests complete sign-out,
explain that the official logout operation may update the credential store and
resolve any conflicting “Keychain untouched” constraint first.

Before an approved filesystem change, verify the exact targets, reject symlink
redirection, close affected apps normally and stop if files changed since the
preview. Do not create an extra identity backup without consent: it retains
the data the user may be trying to remove. User-level settings need a scoped
edit; write safely and compare unselected values. Never print account values.

CLI, IDE integrations, Desktop or background sessions can recreate shared
state. A newly present field is not proof its value is new or old. If data
returns, inspect which process/store is writing it before another deletion.
When the guiding assistant is itself Claude Code/Desktop using that root, it
is one of those writers. Inspect and prepare the preview there, then hand off
the approved cleanup and shutdown verification to another agent, or the user
after exiting. Do not keep using the same session while claiming its state
will remain cleared.

## Sources and portability

- [Claude Code credential management](https://code.claude.com/docs/en/authentication#credential-management)
- [Official uninstall/configuration consequences](https://code.claude.com/docs/en/setup#remove-configuration-files)
- [CCBaga local identity scope and permissions](https://github.com/liseami/CCBaga#data--permissions)

These path candidates were reviewed on 2026-10-23. Recheck current primary
documentation for the installed version. On Windows/Linux, discover the
actual app/config roots first; this helper's macOS layout is not an OS-neutral
cleanup recipe. If a path or operation cannot be verified, mark it unknown.
