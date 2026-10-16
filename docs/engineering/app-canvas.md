# App Canvas

Use this skill to connect an application's actual pages and named states to one interactive canvas, with source updates, synthetic data and checked user flows.

The canvas engine lives in [tombelieber/app-canvas](https://github.com/tombelieber/app-canvas). This repository owns the canonical [skill](../../skills/engineering/app-canvas/SKILL.md); the standalone tool carries a compatibility snapshot for its installer.

Try the [hosted StoolSense canvas](https://tombelieber.github.io/app-canvas/) without
installing anything. To connect another app, give its coding agent the
[integration guide](https://github.com/tombelieber/app-canvas/blob/main/AGENT_GUIDE.md).
The guide is agent-neutral; the optional skill installer supports Codex and Claude.

```sh
npm install -g github:tombelieber/app-canvas#v0.3.0
app-canvas install --target both
app-canvas browsers
app-canvas --config canvas.config.mjs
```

The integration keeps real components and CSS. Projects maintain catalogs, fixtures and preview adapters rather than a separate design implementation. New states need registration; route and interaction checks make missing coverage visible. Preview mutations stay synthetic and do not authorize application deployment or real provider operations.

Every named screen renders real HTML/CSS/JS simultaneously, with in-canvas
interaction and isolated preview storage. Flow links select and zoom to the
destination. Checked journeys play happy, failure and recovery paths in one
continuing session; pause, single-step and replay make the flow inspectable.
Measure the target application's frame cost; the demo verifies 77 cases.
