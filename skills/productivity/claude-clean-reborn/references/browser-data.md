# Browser profiles and persistent cookies

## Inventory and selective cleanup

List every discovered profile with its display name and directory. For Chrome,
merge `Local State` profile metadata with actual `Default`, `Profile N`, Guest
and System directories. Include custom user-data roots or other installed
channels only after discovering them. Do not assume the active profile is the
owner's intended profile. Read-only disk counts can lag running Chrome.

Match these exact domains or their subdomains, not arbitrary substring hits:
`claude.ai`, `anthropic.com`, `claude.com`, `claudeusercontent.com`, `claude.site`.
Add another origin only with evidence and an updated preview. Include cookies
partitioned under a target origin or the verified official Claude extension.
The observed extension ID is `fcoeoabgfenejglbffodgkkbkcdhcgfn`; verify the current
installed extension before relying on that identifier.

Use the browser's supported site-data controls to remove only the approved
origins. In DevTools, Application → Storage → Cookies can select and delete a
visible cookie. Navigate to account sites only when needed: opening a site or
an enabled extension can create data again. Do not clear all browsing data,
saved passwords, history, bookmarks or the profile itself.

Treat extension installation, enabled state, extension storage and partitioned
website cookies as four separate observations. Disabling an extension does
not remove its data. Preview whether the user wants to keep it disabled,
remove its storage, or uninstall it; explain the effect. Do not reinstall it
just to inspect a residual cookie.

## When a deleted entry returns

`0 B · 2 cookies` is not zero cookies. Record name, domain, path, partition key,
ancestor flag and profile/store; no values are needed. `cf_clearance` and
`anthropic-consent-preferences` have security/consent roles; their presence alone
does not prove a Claude account is logged in. Do not call them anonymous or
harmless based on their names.

Persistent extension-partitioned cookies can reflect a version-specific All
sites deletion issue. One investigated implementation reconstructed an HTTP(S)
partition from a host, while the stored partition used `chrome-extension://`.
Treat that as a version-specific diagnosis to verify, not a universal vendor
guarantee. Old timestamps can indicate a row was never deleted, rather than
continuously regenerated. Disk writes can also lag; close Chrome normally
before distinguishing these cases.

If UI deletion fails, inspect the actual request and affected profile before
choosing another supported manual route. Do not copy an unverified fix into a
loop. Protocol monitor is optional and advanced, not required because cookies
are encrypted. A `Network.deleteCookies` request needs exact metadata including
`partitionKey.topLevelSite` and `hasCrossSiteAncestor` when partitioned. Its target
must support Network, typically a page/frame; a parent `Tab ()` may not.
An empty `{}` response can mean zero matching cookies. Verify persisted state;
never treat that response as deletion proof. A proposed command sequence remains
unverified until a fresh scoped observation confirms the matching rows are gone.

Respect the active harness's browser restrictions. Do not automate internal
Chrome pages, raw CDP, cookie APIs or database writes to bypass a denied tool
operation. A manual walkthrough is still subject to the owner's approval.

## Verification limits

The helper reads cookie metadata only. A nonempty journal/WAL/SHM, changed DB,
symlink, lock or unreadable schema produces unknown, not zero. It does not copy
raw cookie databases, decrypt values or access Keychain. It lists storage
directories without parsing their live records. A generic `Local Storage`
directory may contain only unrelated data; inspect through supported scoped
controls rather than deleting the directory. Likewise, raw LevelDB text may
be a tombstone or embedded URL, not a live cookie or authenticated session.

- [Chrome cookie viewing and selective deletion](https://developer.chrome.com/docs/devtools/application/cookies)
- [Investigated Chrome 156 All sites implementation](https://chromium.googlesource.com/chromium/src/+/refs/tags/156.0.8078.48/chrome/browser/ui/webui/settings/site_settings_handler.cc)
- [Protocol monitor](https://developer.chrome.com/docs/devtools/protocol-monitor)
- [CDP cookie deletion parameters](https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-deleteCookies)
- [Anthropic cookie classifications](https://privacy.claude.com/en/articles/10023541-what-cookies-does-anthropic-use)
- [Cloudflare clearance](https://developers.cloudflare.com/cloudflare-challenges/concepts/clearance/)
