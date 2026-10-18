---
name: product-demo-studio
description: Build product demo batches, review alternative demos, and iteratively polish a selected demo through an interactive requirements interview.
---

# Product Demo Studio

Help the user go from an interview to a batch of demos, review them, and refine a chosen demo. Start with the user's product and preferences. Do not infer creative specifications from the skill, templates, a previous project, or the available tools.

## 1. Interview first

Read [interview.md](references/interview.md). Ask one focused question at a time in the user's language. Reuse supplied answers. Establish product/audience/outcome, the journey to show, source access and footage, style/brand, languages, placements/aspect ratios, duration, sound, batch size, what should differ between demos, and delivery/review access.

Unanswered specifications remain undecided. Offer options when useful; recommendations become specifications only when the user accepts them or explicitly delegates that decision. Do not default to particular languages, lengths, ratios, colors, CTA, number of demos, or seven engines.

Present a compact brief and proposed batch differences. Wait for agreement/corrections before production. If the user explicitly skips the interview, document delegated decisions and resolve only blocking gaps. Resume existing briefs without repeating settled questions.

## 2. Plan the batch

Read [batch-and-polish.md](references/batch-and-polish.md). Assign stable demo IDs, record the agreed common specs and the deliberate difference for each variant, and keep a batch manifest. A batch means multiple creative demos; it does not automatically mean benchmarking seven tools.

Choose tools after the brief is agreed. Read [dependencies.md](references/dependencies.md) and the selected entries in [workflows.md](references/workflows.md). Fetch pinned upstream sources on demand with the included fetch_workflows.py. Read their actual skill entrypoints. Use the smallest suitable toolchain; respect any user tool preference.

## 3. Build the agreed demos

Read [production.md](references/production.md). Reuse approved source assets where appropriate; produce the agreed variations rather than copies with different filenames. Preserve actual product behavior, locale alignment, output specs and truthful capture boundaries. Each demo records its real renderer and adaptations.

The optional C03 starter handles one demo project at a time; create separate projects for batch variants. Its project.json deliberately contains no creative specs. Populate it from the confirmed brief before rendering. Other workflows use their own real upstream pipelines. A shared edit is not a fresh native-engine benchmark.

## 4. Review, then polish

Present all completed variants together in a gallery with stable IDs and playable/downloadable files. The included viewer supports sequential selection, vertical scrolling and language/format switching. Read [batch-and-polish.md](references/batch-and-polish.md) for the manifest and review loop.

Ask which demo the user wants to develop and what to change. Keep the batch and selected original intact. Create a new revision of the selected demo, apply the requested changes, show before/after, and continue the loop. Do not rerender the entire batch for a change to one demo. User feedback updates only the affected decisions.

For authorized hosted review, load the installed Sites skill and [hosting.md](references/hosting.md). Otherwise provide the local gallery/files. Static viewer code is not authentication.

## 5. Handoff

Deliver the batch, selected polished revisions, editable source/config, provenance and actual review location. Keep checks proportional to the request; [verification.md](references/verification.md) is available when needed. State unverified items instead of claiming a pass.

Official skills/plugins are integrated on demand, not embedded account permissions. Do not purchase credits, mutate production, post to social accounts, send invitations, or widen access without the relevant user instruction.
