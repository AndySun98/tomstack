# Capture and editing

## Source truth

Use supplied footage or an authorized local/test product. For synthetic capture, run actual frontend components/styles behind isolated test IO. Distinguish real frontend operations, test backend results and provider-confirmed production results. Pre-seeded published rows do not prove the recorded click published anything.

Keep a receipt with product revision, boundary, viewport, tested steps, locales, file and SHA-256. Exclude credentials/customer records. Screenshot plates can support a film; a screenshot slideshow is not continuous product footage.

The starter capture.mjs runs native Testreel definitions. Author definitions from the real UI and fetched upstream schema. Use stable locators, meaningful holds and screenshots after critical operations. Never reuse the example product's selectors/ports. A returned MP4 is not capture success: reject failed step results and inspect entered text, selection, modal and actual screen. Preserve rejected-attempt receipts. Repeated failure needs diagnosis or user help, not blind capture retries.

## Timeline and localization

project.json stores the approved brief and canonical scenes. Each scene has a stable ID, time interval, kind and per-locale copy. Keep semantic equivalents and equivalent timing. Supply a recording per locale when visible UI/data differ. Reuse language-neutral media only when explicitly documented with evidence.

Align product UI, synthetic names/posts, entered text, dates/timezones, headline/captions, voiceover, disclosure, CTA and review UI. Technical names may remain unchanged. Translated overlays over wrong-language footage fail. Set ui_reviewed/data_reviewed only after inspecting source frames; these are attestations, not automated semantic proof.

Included render.mjs implements C03. Additional native workflows need their own sources/exporters/receipts and delivery.json rows with actual engine provenance. Never duplicate one MP4 under seven workflow names.

## Formats/audio

Obtain dimensions, aspect ratio, fps, duration, safe margins and audio requirements from the confirmed brief. No creative/output format is preset. Use an appropriate delivery codec after those choices; check current official requirements before claiming platform compliance.

Recompose portrait camera/crops/type/CTA; avoid stretching or cropping away essential UI. Inspect a moving draft at normal speed before finals. Platform overlays vary by device and placement.

Use supplied/licensed audio or original local synthesis. Gather voice/language preference and rights. Do not invent voice identity or purchase API access. Optional music is supported; voiceover needs a timed audio/caption edit. Technical sound measurements are not listening review.

## Commands

Run npm commands from the initialized project:

```text
python3 <skill-dir>/scripts/check_project.py <project>
npm ci
node capture.mjs <definition.json> <new-capture-folder>
npm run render
python3 <skill-dir>/scripts/verify_media.py <project> --decode
python3 <skill-dir>/scripts/build_review.py <project> --output <new-review-folder>
```

An existing renderer browser may be selected with npm run render -- --browser-executable <path>. Do not assume macOS Chrome paths. Adapt the composition to the brief; the starter is a baseline, not compulsory styling.
