# Copyable team handoff

After installing the skill, paste this into your agent:

```text
Use $claude-clean-reborn to guide me through cleaning my own machine before
using legitimate Claude access again.

Start read-only. Discover my OS, Claude Desktop/Claude Code integrations,
browser profiles and custom data roots. Show all affected profiles together
with the exact proposed removals, their impact and anything you cannot check.

Keep my Keychain, credential stores, passwords, unrelated browser data,
projects, conversations, skills, plugins, MCP settings and backups untouched
unless I separately approve an exact change. Do not read or decrypt secrets.
Ask me to confirm the concrete deletion list before removing anything.

Guide me one action at a time in my language. Reuse my answers and approvals.
After normal app shutdown, verify the same scope and show an updated combined
table. Unknown is not zero, an API success is not deletion proof, and zero
cookies does not prove all website storage is empty. If an item returns,
diagnose its profile, partition and writer before retrying.

End with what was removed, retained and still unknown. Check official network
reachability and my user-performed login separately if I want that final test.
Do not change fingerprints, system region, network routes or account controls
to bypass restrictions. Give me one clear next action, not a blanket promise
that the machine cannot be linked or the account cannot be restricted.
```

Without installation, provide this prompt together with `SKILL.md` and the
linked references; do not assume the receiving agent can resolve `$skill-name`
by itself. The optional audit helper needs Python 3.10+ and macOS-shaped paths.
