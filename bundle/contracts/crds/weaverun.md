---
type: Custom Resource
title: WeaveRun
description: One execution of a WeaveChain (weave.fusion-platform.io/v1alpha1, short name fr) with per-step status, overrides and deploy bookkeeping.
resource: repo://fusion-flux/api/v1alpha1/weaverun_types.go
tags: [weave, crd, run]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: types, resource: repo://fusion-flux/api/v1alpha1/weaverun_types.go, title: weaverun_types.go }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.chainRef`, `triggerRef` | what runs and who started it |
| `spec.parameterOverrides` | env overrides for all steps |
| `spec.stepOverrides[]` | per deploy step: `stepName`, `artifactName`, `tag`, `ingressName`, `indexURL` - identity/location only; everything else comes from the artifact's [metadata.yaml](/contracts/metadata-yaml.md) |
| `spec.imageOverrides[]` | `stepName`, `image`, `imagePullPolicy` - checked against `ALLOWED_IMAGE_PREFIXES` at run start |
| `spec.authSecretRefOverride`, `externalAuthRefOverride`, `unsafeEnvironmentInjectorOverride` | highest-precedence auth settings |
| `status.phase` | `Pending`, `Running`, `Succeeded`, `Failed`, `Stopped` |
| `status.steps[]` | `phase` (`Pending`, `Running`, `Succeeded`, `Failed`, `Skipped`, `Retrying`, `Deployed`), job/deployment refs, retries, `outputCaptured` |
| `status.sharedPVCName`, `activeDeployments` | per-run PVC and run-owned deployments |

[^types]

# Semantics

- A deploy step becomes `Deployed` (non-terminal) when its Deployment is available; downstream steps may start, but the run stays `Running` while any step is `Deployed`.
- Runs with deploy steps get the finalizer `weave.fusion-platform.io/deploy-cleanup`; Stopped/Failed runs tear their deployments down, Succeeded runs keep them for later rolling updates.
- Change one step image on a live run: `POST /api/v1/runs/{name}/image` (BFF permission `weave:runs:image`); stop: `POST /runs/{name}/stop`.
- Rolling restart a deployed step: annotation `fusion-platform.io/restart-step=<step>`.[^flux]

[^types]: weaverun_types.go
[^flux]: fusion-weave CLAUDE.md
