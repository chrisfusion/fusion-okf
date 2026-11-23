---
type: Convention
title: Changelog, versions and image tags
description: Each repo keeps a Keep-a-Changelog CHANGELOG.md updated before every commit; a release promotes [Unreleased] and bumps chart, app and image tag to the same semver.
tags: [forge, index, weave, bff, ext-bff, wizard, content, spectra, shared, release]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: content, resource: repo://fusion-content/CLAUDE.md, title: fusion-content CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
  - { id: shared, resource: repo://fusion-shared/CLAUDE.md, title: fusion-shared CLAUDE.md }
  - { id: ext-bff, resource: repo://fusion-ext-system-bff/CLAUDE.md, title: fusion-ext-system-bff CLAUDE.md }
---

# Changelog

- Format: [Keep a Changelog](https://keepachangelog.com/). Entries go under `## [Unreleased]`, in `### Added` / `### Changed` / `### Fixed` sections, one line per item.[^spectra]
- Every feature and bugfix gets an entry **before the commit**.[^content][^wizard]
- On release, `[Unreleased]` becomes `## [x.y.z] — YYYY-MM-DD`. Get the date from `date +%Y-%m-%d`.[^spectra]
- Changelogs are not only for humans: [fusion-content](/services/fusion-content.md) parses them from git and serves them to the GUI, so the format must stay parseable.[^content]

# Versions

- Semver everywhere. Changes made in one session go into one version bump.[^bff]
- fusion-bff: RBAC-only additions (a new permission plus a route rule, no Go code) bump the **patch** version.[^bff]
- fusion-weave: version headings are not in order (a `[0.3.0]` heading predates `[0.2.1]`), so check for collisions before choosing a number.[^flux]
- fusion-shared: git tags only for Go code changes, never for `docs/`. `v0.x` (breaking = minor) until every service has adopted it.[^shared]

# Image tags and charts

- Always use semver image tags, never `latest` or `local`.[^spectra][^ext-bff]
- A release bumps everything to the same semver together: `package.json` (spectra), `deployment/Chart.yaml` `version`/`appVersion`, and `image.tag` in the values file. The tag change makes Helm replace the pods.[^spectra]
- Known deviation: forge in the `fusion` namespace runs `fusion-forge:local`, see the [deploy matrix](/operations/deploy-matrix.md).[^wizard]

[^spectra]: fusion-spectra CLAUDE.md
[^content]: fusion-content CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^bff]: fusion-bff CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
[^shared]: fusion-shared CLAUDE.md
[^ext-bff]: fusion-ext-system-bff CLAUDE.md
