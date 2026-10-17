# App Canvas has moved to its standalone repository

[App Canvas](https://github.com/tombelieber/app-canvas) owns its canvas, CLI,
canonical [skill](https://github.com/tombelieber/app-canvas/tree/main/skills/app-canvas),
completion/native references, marketplace and releases. Tomstack no longer
bundles or maintains a copy. No Tomstack installation is required to use it.

## Migrate before updating an older Tomstack bundle

For the Claude bundle, install the standalone skill first:

```sh
claude plugin marketplace add tombelieber/app-canvas
claude plugin install app-canvas@app-canvas
```

Then update the Tomstack bundle as usual; it retains the other promoted skills.
The standalone plugin supplies the skill. Install the App Canvas CLI separately
as documented in the [current installation guide](https://github.com/tombelieber/app-canvas#connect-a-project).

For a Codex or other agent skill installed with `skills`, select the same target
agents from the new source:

```sh
npx skills@latest add tombelieber/app-canvas --skill app-canvas
```

For CLI-managed copies, update the CLI and run `app-canvas install --target both`.
Preserve a manually copied or locally linked skill before installing: the CLI
refuses to overwrite unmanaged or locally edited files. Choose one Claude skill
installation route to avoid duplicates.

The legacy `app-canvas@tomstack` marketplace entry still points directly to the
standalone repository for existing installations. New users can use
`app-canvas@app-canvas` independently. Future skill changes and releases happen
only in App Canvas; Tomstack's listing is for discovery and compatibility.
