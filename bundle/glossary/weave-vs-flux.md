---
type: Glossary Term
title: weave vs flux
description: fusion-weave is the job scheduler, developed in the local directory fusion-flux; "Flux" alone means the FluxCD GitOps tool used by fusion-fleet.
tags: [glossary, weave, fleet]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
---

| Name | Means |
|---|---|
| **fusion-weave** | the service: operator, API, chart, git origin, image `fusion-weave-operator`, Helm release, BFF path `/api/weave` |
| **fusion-flux** | only the local clone directory of fusion-weave |
| **Flux** / FluxCD | the GitOps controller that deploys everything from [fusion-fleet](/services/fusion-fleet.md) |

Use `fusion-weave` in GitRepository, mirror and HelmRelease names.[^fleet][^bff] In this bundle, `repo://fusion-flux/...` points into the weave repo.

[^fleet]: fusion-fleet CLAUDE.md
[^bff]: fusion-bff CLAUDE.md
