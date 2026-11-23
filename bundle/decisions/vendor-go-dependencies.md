---
type: Decision
title: Vendor Go dependencies for offline CI
description: Accepted - every Go repo commits vendor/ and builds with -mod=vendor, because the CI environment that builds images has no internet access.
resource: repo://fusion-bff/docs/go-vendoring-blueprint.md
tags: [forge, index, weave, bff, ext-bff, wizard, content, shared, build, decision]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:40:00Z }
sources:
  - { id: blueprint, resource: repo://fusion-bff/docs/go-vendoring-blueprint.md, title: go-vendoring-blueprint.md }
  - { id: index-cl, resource: repo://fusion-index/CHANGELOG.md, title: fusion-index CHANGELOG }
  - { id: shared, resource: repo://fusion-shared/CLAUDE.md, title: fusion-shared CLAUDE.md }
---

**Status:** accepted, rolled out to all Go repos (index: 0.6.0, 2026-10-27).[^index-cl]

# Context

"The CI environment that builds our images has no internet access, so a build must not download anything."[^blueprint]

# Decision

- Commit `vendor/` and build with `-mod=vendor`.
- Keep vendor/ in sync with `make vendor`; `make check-vendor` catches drift.
- Prove it with `docker build --network none`.

The steps are in the blueprint (`docs/go-vendoring-blueprint.md`, one copy per repo). How it works day to day: [offline vendoring](/conventions/offline-vendoring.md).

# Consequences

- **Bigger repos:** 35-79 MB of `vendor/` per repo. It is hidden from diffs and language stats via `.gitattributes`.
- **Not covered by vendoring:** Docker base images, which must be mirrored or loaded with `docker save`/`docker load`, and build tools such as `controller-gen`.
- **Rules for fusion-shared:** every published tag must build offline, and no `replace` directives may be committed.[^shared]

[^blueprint]: go-vendoring-blueprint.md
[^index-cl]: fusion-index CHANGELOG
[^shared]: fusion-shared CLAUDE.md
