# App Canvas

Use this skill to connect an application's actual pages and named states to one interactive canvas, with source updates, synthetic data and checked user flows.

The canvas engine lives in [tombelieber/app-canvas](https://github.com/tombelieber/app-canvas). This repository owns the canonical [skill](../../skills/engineering/app-canvas/SKILL.md); the standalone tool carries a compatibility snapshot for its installer.

```sh
npm install -g github:tombelieber/app-canvas#v0.1.1
app-canvas install --target both
app-canvas browsers
app-canvas --config canvas.config.mjs
```

The integration keeps real components and CSS. Projects maintain catalogs, fixtures and preview adapters rather than a separate design implementation. New states need registration; route and interaction checks make missing coverage visible. Preview mutations stay synthetic and do not authorize application deployment or real provider operations.
