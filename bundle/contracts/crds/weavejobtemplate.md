---
type: Custom Resource
title: WeaveJobTemplate
description: Reusable batch-job blueprint (weave.fusion-platform.io/v1alpha1, short name fjt) referenced by Job steps of a WeaveChain.
resource: repo://fusion-flux/api/v1alpha1/weavejobtemplate_types.go
tags: [weave, crd, job]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: types, resource: repo://fusion-flux/api/v1alpha1/weavejobtemplate_types.go, title: weavejobtemplate_types.go }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.image`, `command`, `args`, `env` | container definition |
| `spec.resources`, `volumes` (Secret/ConfigMap mounts) | resources and mounts |
| `spec.retryPolicy` | `maxRetries`, `backoffSeconds` |
| `spec.parallelism`, `completions`, `activeDeadlineSeconds` | batch/v1 Job knobs |
| `spec.serviceAccountName` | must pass the workload policy (`WORKLOAD_SERVICE_ACCOUNTS`) |
| `spec.podSecurityContext`, `containerSecurityContext` | merged with `WORKLOAD_SECURITY_DEFAULTS` (template wins) |
| `spec.codeSource` | load an index artifact at pod start ([code source](/glossary/code-source.md)) |
| `status.valid`, `validationMessage` | validation result; an invalid template gates its chain |

[^types]

# Usage

Referenced from a [WeaveChain](/contracts/crds/weavechain.md) step (`jobTemplateRef`, `stepKind: Job`); the operator's `jobbuilder` turns template + step + run into a batch/v1 Job (container named `job`). Shown as a "Step Blueprint" in spectra ([blueprint](/glossary/blueprint.md)).[^flux]

[^types]: weavejobtemplate_types.go
[^flux]: fusion-weave CLAUDE.md
