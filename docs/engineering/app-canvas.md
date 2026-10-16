# App Canvas

Use this skill to have a coding agent discover and populate an application's
complete UI landscape: screens, components, variants, states and navigation.
The agent prepares missing fixtures, previews and render harnesses itself;
the user does not need to supply a screen list or ask repeatedly for the rest.

The canvas engine lives in [tombelieber/app-canvas](https://github.com/tombelieber/app-canvas). This repository owns the canonical [skill](../../skills/engineering/app-canvas/SKILL.md); the standalone tool carries a compatibility snapshot for its installer.

Try the [hosted StoolSense canvas](https://tombelieber.github.io/app-canvas/) without
installing anything. To connect another app, give its coding agent the
[integration guide](https://github.com/tombelieber/app-canvas/blob/main/AGENT_GUIDE.md).
The guide is agent-neutral; the optional skill installer supports Codex and Claude.

```sh
npm install -g github:tombelieber/app-canvas#v0.6.1
app-canvas install --target both
app-canvas browsers
app-canvas --config canvas.config.mjs
```

The integration uses original UI code. Projects maintain an independent source
inventory, catalog, fixtures and adapters. A new source-inventory gate checks
file freshness and item/case mappings alongside route and playable-case checks.
Semantic discovery and scope cross-checking remain the agent's responsibility.
A representative subset or a passing self-selected catalog is not completion;
blocked items remain counted and incomplete. Read the
[completion contract](../../skills/engineering/app-canvas/references/completion.md).
Use a verified tool revision exporting `@tombelieber/app-canvas/inventory` for
that gate; the older install example above only establishes CLI/skill setup.
Preview mutations stay synthetic and do not authorize deployment or real
provider operations.

Web screens show full source-rendered HTML/CSS without summary cards.
Render-only DOM previews avoid starting every app; selection and playback use
the original HTML/CSS/JS with isolated preview storage. A compact toolbar and
collapsible left/right sidebars preserve iPad landscape space. Unsupported drawing/embedded content retains live rendering and needs
its own resource checks. Flow links select and zoom to the
destination. Checked journeys play happy, failure and recovery paths in one
continuing session; pause, single-step and replay make the flow inspectable.
Measure the target application's frame cost; the demo verifies 77 cases.

The state graph combines all declared branches and checked transitions with
success/failure/waiting labels. Every graph node shows its full real UI.
The demo has 44 interaction flows and independent playback for every one of
its 77 cases, with whole-set queue playback. Set complete-case and connected
graph guards so a newly registered state cannot silently miss its playback.
Declare fixture conditions explicitly; a login boundary or read-only variant
does not need an invented button-driven transition.

Native UIKit/storyboard, SwiftUI, Android Views/Compose and React Native
repositories use agent-authored native harnesses and captures or a verified
device adapter, following the [native workflow](../../skills/engineering/app-canvas/references/native.md).
Full original captures are valid visual surfaces with recorded source/build,
fixture and device provenance. Native assertions and recapture checks run in
the original runtime and connect to the canvas verification hook; viewer clicks
are not native E2E. Existing previews or a React rewrite are not prerequisites.
