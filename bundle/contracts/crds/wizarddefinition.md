---
type: Custom Resource
title: WizardDefinition
description: Instance-agnostic provisioning recipe (wizard.fusion-platform.io/v1alpha1, short name wdef) with typed parameters and an ordered subset of wizard steps.
resource: repo://fusion-wizard/api/v1alpha1/wizarddefinition_types.go
tags: [wizard, crd]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: types, resource: repo://fusion-wizard/api/v1alpha1/wizarddefinition_types.go, title: wizarddefinition_types.go }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.description` | shown in the GUI |
| `spec.parameters[]` | `name`, `type` (`string`, `number`, `boolean`, `stringList`, `objectList`), `description`, `required`, `default`, `pattern` |
| `spec.steps[]` | `name`, `type` (`gitWatcher`, `waitBuild`, `tag`, `app`, `jobTemplate`, `serviceTemplate`, `chain`, `trigger`, `batchTrigger`), `forEach` (a list parameter), `params` (templated strings) |

[^types]

# Semantics

- Steps always run in the fixed catalogue order; a definition chooses a subset.
- `params` use templates like `${params.x}`, `${item}`, `${item.<field>}` and filters (`${item|stem|k8sName}`). For `objectList`, every entry needs a non-empty `key`.
- A parameter `pattern` is also checked against its `default`.
- Definitions ship in the wizard chart (`definitions/*.yaml`, enabled per `definitions.<x>.enabled`) and are what spectra's wizard cards run.[^wizard]

[^types]: wizarddefinition_types.go
[^wizard]: fusion-wizard CLAUDE.md
