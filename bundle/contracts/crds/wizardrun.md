---
type: Custom Resource
title: WizardRun
description: One execution of a WizardDefinition (wizard.fusion-platform.io/v1alpha1, short name wrun) with parameters, definition snapshot, desired state and per-step status.
resource: repo://fusion-wizard/api/v1alpha1/wizardrun_types.go
tags: [wizard, crd]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: types, resource: repo://fusion-wizard/api/v1alpha1/wizardrun_types.go, title: wizardrun_types.go }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.definitionRef`, `definitionSnapshot`, `definitionGeneration` | the recipe, frozen at creation |
| `spec.parameters` | run input (JSON values) |
| `spec.createdBy`, `createdByEmail` | stamped from `X-User-ID` / `X-User-Email` for allowlisted BFF callers |
| `spec.desiredState` | `Applied` or `RolledBack` |
| `status.phase` | `Pending`, `Running`, `Ready`, `Failed`, `RollingBack`, `RolledBack`, `RollbackFailed` |
| `status.steps[]` | `key` (`<step>/<item>` for forEach), `phase` (`Pending`, `Running`, `Succeeded`, `Failed`, `RolledBack`, `RollbackFailed`), `outputs`, `resources[]` with `disposition` (`Created`, `Adopted`, `FoundUnowned`) |
| `status.conditions`, `startedAt`, `completedAt` | standard bookkeeping |

[^types]

# Operations

- Create via `POST /api/wizard/api/v1/runs` through the BFF; one 422 lists every validation problem.
- Roll back: `kubectl patch wizardrun <name> --type=merge -p '{"spec":{"desiredState":"RolledBack"}}'` - never delete the weave objects by hand (leaves the ledger inconsistent). A rolled-back run is terminal.[^spectra]
- Runs are terminal after `Ready`; later builds are followed by forge's `autoTag`, not by the wizard.[^wizard]

[^types]: wizardrun_types.go
[^wizard]: fusion-wizard CLAUDE.md
[^spectra]: fusion-spectra CLAUDE.md
