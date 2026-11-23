---
type: Glossary Term
title: Blueprint
description: spectra's UI name for weave templates - Step Blueprints are job/service templates, Run Blueprints are chains; Deploy steps are shown as Service.
tags: [glossary, spectra, weave]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: spectra-pipelines, resource: repo://fusion-spectra/src/pages/pipelines/CLAUDE.md, title: spectra pipelines pages }
---

| UI term (spectra) | API term (weave) |
|---|---|
| Step Blueprint | [WeaveJobTemplate](/contracts/crds/weavejobtemplate.md), [WeaveServiceTemplate](/contracts/crds/weaveservicetemplate.md) |
| Run Blueprint | [WeaveChain](/contracts/crds/weavechain.md) |
| Service (step) | `stepKind: Deploy` |
| Weave context | route `/pipelines` |

All "templates" were renamed to "blueprints" in UI labels only; APIs keep the weave names.[^spectra][^spectra-pipelines]

[^spectra]: fusion-spectra CLAUDE.md
[^spectra-pipelines]: spectra pipelines pages CLAUDE.md
