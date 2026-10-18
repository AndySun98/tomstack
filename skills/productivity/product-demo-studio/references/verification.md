# Verification and acceptance

check_project.py verifies approved required fields, complete locale copy, contiguous timing, format durations/safe margins, and source paths/locale attestations. It cannot establish that an attestation is true.

verify_media.py --decode checks the requested locale × format × variant matrix, unique keys, safe local paths, file existence, H.264/yuv420p, dimensions/fps/duration, AAC when audio is present, full decode and hashes. It writes project verification.json. Native receipts/source review establish that separate engines really ran.

Inspect opening, critical state transitions, CTA and moving playback at normal speed. Check values, locale demo records, subtitles, logo, crop and safe margins. Listen if actually supported; otherwise mark listening unverified. Save checks and limits in qa.md.

At desktop and phone sizes, verify one playing video, off-screen pause, locale/format switching preserves variant, deep links, previous/next, downloads and overflow. Responsive desktop testing is not physical-device touch proof.

Native deployment success proves deployment. Anonymous denial for HTML AND media proves sampled protection. A service-token fetch proves service access, not visitor login. Record actual viewer login separately; never remove authentication to manufacture a pass.

Handoff states requested/delivered matrix, capture boundary, engine/shared adaptations, technical and visual/audio checks, editable sources, reproduction steps and remaining limits. Do not claim social upload or production outcomes that did not occur.
