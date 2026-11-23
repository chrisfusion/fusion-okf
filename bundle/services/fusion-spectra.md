---
type: Service
title: fusion-spectra
description: Vue 3 + Quasar web GUI (Module Federation host) with Simple and Expert mode; talks only to fusion-bff.
resource: repo://fusion-spectra
tags: [spectra, gui, frontend]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: spectra-pipelines, resource: repo://fusion-spectra/src/pages/pipelines/CLAUDE.md, title: spectra pipelines pages }
  - { id: spectra-wizards, resource: repo://fusion-spectra/src/pages/wizards/CLAUDE.md, title: spectra wizards pages }
---

# Purpose

The platform's web UI. Stack: Vue 3, Quasar 2, Pinia, Vue Router 4, Vite 5; served by nginx (non-root, port 8080).[^spectra]

# Contexts (activity rail)

| Context | Route | Backend |
|---|---|---|
| Data | `/data` | - |
| Weave | `/pipelines` | [fusion-weave](/services/fusion-weave.md) - runs, chains, "blueprints" |
| Monitoring | `/monitoring` | weave monitoring API |
| Forge | `/forge` | [fusion-forge](/services/fusion-forge.md) |
| Fusion Index | `/fusion-index` | [fusion-index](/services/fusion-index.md) |
| Admin | `/admin` (admin only) | BFF admin endpoints, index/forge cleanup |

Plus wizards (backed by [fusion-wizard](/services/fusion-wizard.md)) and help (backed by [fusion-content](/services/fusion-content.md)).[^spectra]

# Integration rules

- All calls go to [fusion-bff](/services/fusion-bff.md) with `credentials: 'include'`; a 401 redirects to `/bff/login`. BFF URL from the runtime `config.js` (`window.FUSION_CONFIG`).
- UI is gated by **permissions**, not roles: `can('index:artifacts:delete', id)` mirrors the BFF `rbac.yaml`.
- [Simple / Expert mode](/glossary/simple-expert-mode.md) depends on the UI-only permission `ui:expert`.
- Naming differences from the backend: weave templates are shown as "blueprints", `stepKind: Deploy` as "Service" ([blueprint](/glossary/blueprint.md)).[^spectra-pipelines]
- Building a `codeSource.artifactName` from a forge build needs the `app.` / `venv.` prefix ([artifact naming](/contracts/artifact-naming.md)).
- Cron input is weave's 6-field, seconds-first format.

# Deployment

Semver image tags only; bump `package.json`, `deployment/Chart.yaml` and `values-dev.yaml` together. `index.html` must be served with no-cache, otherwise redeploys show blank pages. Local dev at `http://dev.fusion.local:5174`; E2E against `http://spectra.fusion.local` (manual `fusion` namespace) - Flux instances are `spectra-a/b.fusion.local`.[^spectra]

[^spectra]: fusion-spectra CLAUDE.md
[^spectra-pipelines]: spectra pipelines pages CLAUDE.md
