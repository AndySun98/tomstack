# Product Demo Studio

## What it does

Interviews the user for the actual product demo requirements, creates an agreed
batch of different demos, presents them for review, and iterates on a selected
demo while preserving the original batch.

No creative specs are assumed: language, duration, aspect ratio, style, audio,
CTA, batch size and review audience come from the interview or explicit user
delegation. Demo variants and renderer engines are separate choices.

## Use it

Invoke `product-demo-studio` and describe the product or the first requirements
you know. The skill asks focused questions, confirms the brief and batch
differences, then proceeds through production, review and selected revisions.

Codex and other compatible agents can install the skill from this repository:

```bash
npx skills@latest add tombelieber/tomstack --skill product-demo-studio
```

Claude Code users can use the managed `tomstack-skills@tomstack` plugin.

## Included tools and optional integrations

The skill includes a pinned-source downloader for Guizang, HyperFrames,
Remotion skills, Video Shotcraft, Testreel, Product Launch Motion and community
claude-motion, plus a single-demo Remotion starter and a batch review gallery.
Only selected upstream sources are fetched. Each keeps its own license.

Browser tools, standalone App Canvas, frontend design and Sites are optional
integrations. Their plugins, accounts, subscriptions and permissions are not
bundled. Hosting and external actions require the user's actual scope.

## Data boundary

This public skill contains reusable instructions, templates and helpers. It
contains no product source, customer footage, account identifiers, credentials
or hosting identity. New projects keep their own source/data boundary and
review audience; using the skill does not authorize public sharing of their
inputs or outputs.

## It is working if

The user can compare the agreed variants, select one by stable ID, request a
change and review a new revision without losing the batch or silently changing
settled specs. Shared edits and native-engine benchmarks are described accurately.
