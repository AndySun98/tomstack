# Readiness and the final handoff

Report what was measured. Do not collapse these independent outcomes into one
green “clean machine” badge:

| Check | Evidence for a pass | What does not prove it |
|---|---|---|
| Approved local cleanup | Each approved artifact/field is absent or selectively cleared, with a fresh observation after normal shutdown | A deletion command returned success |
| Browser website data | Every in-scope profile/store checked; target cookies absent and relevant live storage independently verified | Zero cookies, an empty DevTools view in another partition, or a LevelDB string scan |
| Preserved material | Explicit list of settings, history, extensions, backups and credentials kept | “No trace” or “fully anonymous” claims |
| Network access | User-authorized connection to the real official service succeeds through their normal approved network | IP lookup, ping or a tool's green environment page |
| Account access | User completes official login and confirms the intended workspace/account and an ordinary request succeeds | Local reset, account metadata or a cached session |

The sign-in check is optional and separate from cleanup. Tell the user that
opening/signing in will recreate normal state; preserved authentication can
reuse an existing login. Do not ask for the password, OTP, recovery codes,
tokens or a screenshot containing secrets. If the user wants their credential
store untouched, do not silently log out or replace its entries to force a
fresh login. Unperformed login remains **not tested**.

For network troubleshooting, inspect local clock/timezone and the user's
intended network without changing them automatically. Use current official
availability/network documentation. External IP checks disclose the public IP
to another service: ask before that optional check and do not treat IP
geolocation as precise location. Do not rotate device fingerprints, fabricate a
region, purchase proxies or change system locale to obtain eligibility.
An account restriction requires official support; cleanup is not an unblock.

Use this final shape, in the user's language:

```text
Result: approved local cleanup verified / partial / unknown
Before → after: one row per app and browser profile, with timestamp
Retained: Keychain/credentials, settings/history/backups as agreed
Unknown/not tested: inaccessible stores, unparsed storage, network, login
Next action: one concrete action under two minutes
```

Keep reports local. Redact home usernames, profile labels, account identifiers
and private paths before sharing outside the device. Never commit real audit
outputs to the public skill repository.

- [Official account/session management](https://support.claude.com/en/articles/13124001-managing-your-active-sessions)
- [Claude supported countries](https://www.anthropic.com/supported-countries)
- [Claude Code network configuration](https://code.claude.com/docs/en/network-config)
- [CCBaga's measurement and account-acceptance limits](https://github.com/liseami/CCBaga#browser-verification)
