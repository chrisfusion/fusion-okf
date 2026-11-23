---
type: Custom Resource
title: WizardResource
description: Ledger entry (wizard.fusion-platform.io/v1alpha1, short name wres) for one upstream object in forge, index or weave, ref-counted across wizard runs.
resource: repo://fusion-wizard/api/v1alpha1/wizardresource_types.go
tags: [wizard, crd, ledger]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: types, resource: repo://fusion-wizard/api/v1alpha1/wizardresource_types.go, title: wizardresource_types.go }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.service` | `forge`, `index` or `weave` |
| `spec.kind`, `name`, `externalID` | the upstream object |
| `spec.specHash` | hash of the identity-defining settings; same name + different hash = conflict |
| `spec.managed` | `true` only when the wizard created it; unmanaged entries are never deleted |
| `spec.terminating` | set (resourceVersion-guarded) before an upstream delete; adopters skip such entries |
| `spec.refs[]` | `run`, `step` - every run that uses the object |

[^types]

# Semantics

See [ledger](/glossary/ledger.md). The upstream object is deleted only when the last ref is gone **and** `managed: true`. `SweepTerminating` finishes deletions interrupted by a crash. Writes use a 30-step conflict backoff because entries are shared by design.[^wizard]

[^types]: wizardresource_types.go
[^wizard]: fusion-wizard CLAUDE.md
