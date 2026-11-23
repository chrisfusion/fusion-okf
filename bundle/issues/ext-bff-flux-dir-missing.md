---
type: Known Issue
title: fusion-ext-system-bff CLAUDE.md describes a flux/ directory that does not exist
description: ext-bff's CLAUDE.md lists Flux config in flux/ with three environments, but the directory is missing and neither ext-bff nor wizard has a HelmRelease in fusion-fleet.
resource: repo://fusion-ext-system-bff/CLAUDE.md
tags: [ext-bff, wizard, fleet, docs, deployment]
resolution: unresolved
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: ext-bff, resource: repo://fusion-ext-system-bff/CLAUDE.md, title: fusion-ext-system-bff CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# Gap

- [fusion-ext-system-bff](/services/fusion-ext-system-bff.md): "Flux config at `flux/` with three environments: `dev-fusion`, `dev-staging-fusion`, `prod-fusion`".[^ext-bff] No `flux/` directory exists in the repo.
- [fusion-fleet](/services/fusion-fleet.md) is where Flux config actually lives, and its `projects/fusion/base/` has HelmReleases for spectra, bff, forge, index, content and weave only. Neither ext-bff nor wizard is there; the wizard is applied by hand.[^fleet]

# Fix

Add both services to the fleet, or correct the ext-bff CLAUDE.md. See the [deploy matrix](/operations/deploy-matrix.md).

[^ext-bff]: fusion-ext-system-bff CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
