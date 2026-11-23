---
type: Custom Resource
title: WeaveChain
description: DAG of Job and Deploy steps (weave.fusion-platform.io/v1alpha1, short name fc) with failure, concurrency, shared-storage and auth settings.
resource: repo://fusion-flux/api/v1alpha1/weavechain_types.go
tags: [weave, crd, dag]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: types, resource: repo://fusion-flux/api/v1alpha1/weavechain_types.go, title: weavechain_types.go }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.steps[]` | `name`, `stepKind` (`Job` / `Deploy`), `jobTemplateRef` or `serviceTemplateRef`, `dependsOn`, `runOnSuccess`, `runOnFailure`, `envOverrides`, `producesOutput`, `consumesOutputFrom` |
| `spec.failurePolicy` | `StopAll`, `ContinueOthers`, `RetryFailed` |
| `spec.concurrencyPolicy` | `Wait`, `Forbid` |
| `spec.sharedStorage` | per-run RWX PVC (`size`, `storageClassName`) mounted at `/weave-shared` |
| `spec.authSecretRef` | Secret injected into job pods (e.g. OAuth client credentials for runner helpers) |
| `spec.externalAuthRef` | `mode` `serviceAccount` / `oidc` + `name`: short-lived token per job launch |
| `spec.unsafeEnvironmentInjector` | toggle for the environment injector |
| `status.valid`, `validationMessage` | admission-time DAG validation |
| `status.activeDeployments` | per deploy step: health (`Healthy`, `Unhealthy`, `RollingBack`, `RolledBack`, `Unknown`), revisions, codeSource artifact/tag/deployed version |

[^types]

# Semantics

- Output passing: a step with `producesOutput` writes JSON to stdout; consumers get `/weave-input/input.json`, namespaced by producer. Consumers must reference an ancestor producer.
- The chain controller watches deploy-step health, auto-rolls back after `unhealthyDuration` and polls index tags for codeSource steps.
- One-shot annotation `fusion-platform.io/reload-deploy-step: <step>@<version>` forces a code reload.
- Executed through a [WeaveTrigger](/contracts/crds/weavetrigger.md) or a directly created [WeaveRun](/contracts/crds/weaverun.md). Shown as a "Run Blueprint" in spectra.[^flux]

[^types]: weavechain_types.go
[^flux]: fusion-weave CLAUDE.md
