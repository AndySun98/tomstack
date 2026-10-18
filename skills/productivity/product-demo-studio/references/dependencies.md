# Dependencies and composition

Included: interview workflow, project/Remotion starter, pinned-source downloader, capture runner, media verification and swipeable gallery. Upstream skills are loaded on demand; naming one does not install it.

## Local tools

Python 3.10+, Git, Node.js/npm, FFmpeg/ffprobe, a browser for capture/render, and authorized product access. The initializer reports executable availability. The starter pins direct npm versions and includes package-lock.json for npm ci. Dependencies may download browser/FFmpeg binaries. Keep each upstream runtime isolated.

fetch_workflows.py downloads immutable commits and verifies required files, repository identity and clean state. It does not run upstream installers. Read selected sources before executing setup. Missing optional tools block only the selected path, not the interview.

## Skills/plugins used in the originating workflow

| Capability | Composition | Recipient setup |
|---|---|---|
| Seven local video workflows | Exact sources in dependencies.lock.json, skill entrypoints and native-export recipes | Fetch only selected IDs, then load actual upstream guidance. |
| Browser / Chrome integration | Product inspection and viewer playback QA | Read/use the host's current supported browser tools; connect its browser integration if needed. |
| app-canvas | Real components with isolated synthetic fixtures when the product already uses it | Use the standalone [App Canvas](https://github.com/tombelieber/app-canvas) CLI/skill. Optional elsewhere; private fixture transport is not included. |
| frontend-design:frontend-design | Optional gallery branding/refinement | Load installed skill if available. Included viewer does not require it. |
| sites:sites / Sites | Optional hosted review and audience management | Prefer native Sites capability; otherwise discover/connect the official integration on the recipient's account. Read its installed identity/access and preview guidance. |
| skill-creator / Superpowers authoring guidance | Used to author this package | Authoring provenance, not runtime requirements for making a film. |

Do not copy publisher-managed plugin caches or proprietary runtime files. Skills cannot automatically install transitive plugins. agents/openai.yaml is UI metadata, not a plugin installer. Discover tool IDs and installed skill paths on the recipient's machine. Do not copy the originating computer's paths.

Hera, Tella and Anthropic-hosted Claude Motion are excluded from the local-seven path. C07 is the distinct open-source whaleyxbt/claude-motion toolkit. Hosted voice/image/music APIs are opt-in and require their own access and budget.

## Distribution and terms

The package contains original workflow instructions/starter code and immutable source coordinates, not full third-party source or one common license. Guizang's pinned source carries AGPL-3.0; HyperFrames and Shotcraft carry Apache-2.0; Testreel, PLM and community claude-motion carry MIT notices. Preserve licenses/notices for copied code. The pinned Remotion skills repo has no root license file; do not relicense it.

Check current [Remotion terms](https://www.remotion.dev/docs/license) for the actual organization/use. Local rendering is not a blanket promise of free commercial use. Original research date/pins: 17 October 2026; runtime integrations should use their current installed instructions.
