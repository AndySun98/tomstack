# Batch → review → selected polish

## Shared brief and batch manifest

Use one confirmed brief for common constraints. Store each demo's deliberate creative difference separately. Ask for batch size and variation axes; do not assume a number or tool count.

Create batch.json from assets/batch.json. Keep stable creative IDs (for example V01) independent of renderer IDs (for example C03). Record source/config, actual toolchain, output rows and status per demo. Record locales and formats from the brief; an absent value is undecided, not a preset.

Each locale/format film belongs to its creative demo. Reuse the same verified product recording when appropriate, while giving variants the agreed different hook, narrative, motion treatment, pacing or other axis. Differences must be visible, not just filenames.

## Produce and present a batch

1. State the agreed common constraints and each variant's difference.
2. Build each requested demo using its selected upstream workflow. Keep separate owned output folders.
3. Collect playable files and provenance into the manifest. Keep failures explicit.
4. Present a review gallery and ask the user to choose a demo ID or request another batch round.

For the included gallery helper, create project.json with the exact batch variants/locales/formats and delivery.json rows with id, name, locale, format, engine, src and poster. Paths are relative to the batch folder. The helper copies only listed final media/posters into a new review folder. Do not confuse its static UI with access control.

The optional starter renders one C03 project per demo. Rename/collect its output under the creative ID in the outer manifest while retaining actual engine/source metadata. For other engines, use their native project/export instead.

## Polish one selected demo

Ask which ID and which changes the user wants. Record the selection and feedback. Preserve the original and batch siblings. Create an explicit next revision in a new folder; revise only the selected demo and affected locale/format cuts.

Offer before/after playback with a concise description of what changed. Let the user continue polishing, return to a sibling, or create a new batch. Do not silently choose a winner, replace all originals, or rebuild unrelated demos.

## No spec inheritance

The original product's languages, duration, ratio, colors, CTA, audience and number of variants are not defaults. This skill carries the workflow and tool integrations. Every new project's creative specifications come from its own interview or explicit delegated decisions.
