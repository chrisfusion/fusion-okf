---
type: Glossary Term
title: Simple and Expert mode
description: spectra's two audiences - common users see wizards and runs, experts with the ui:expert permission see the full Weave, Forge and Index UI.
tags: [glossary, spectra, bff, rbac]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
---

- **Simple mode** - wizard cards, own runs, logs, "Run now" on job apps. Users in group `platform-user` (BFF role `user`) have no forge/index/weave write permissions; wizard provisioning runs under fusion-wizard's service account. `user` has `weave:apps:fire` but deliberately not `weave:apps:write`.
- **Expert mode** - requires the UI-only permission `ui:expert` (no route rule in the BFF); experts toggle via the top bar.
- Navigation entries are marked `audience: 'expert'`; filtering happens in one place (`contextsForMode`).[^spectra]

See [fusion-spectra](/services/fusion-spectra.md), [fusion-bff](/services/fusion-bff.md).

[^spectra]: fusion-spectra CLAUDE.md
