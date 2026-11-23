---
type: Custom Resource
title: WeaveServiceTemplate
description: Long-running service blueprint (weave.fusion-platform.io/v1alpha1, short name wst) used by Deploy steps; becomes a Deployment, Service and optional Ingress.
resource: repo://fusion-flux/api/v1alpha1/weaveservicetemplate_types.go
tags: [weave, crd, service, deploy]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: types, resource: repo://fusion-flux/api/v1alpha1/weaveservicetemplate_types.go, title: weaveservicetemplate_types.go }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.image`, `command`, `args`, `env`, `resources`, `volumes` | container definition |
| `spec.replicas`, `ports` (required), `serviceType` | Deployment / Service shape |
| `spec.livenessProbe`, `readinessProbe`, `startupProbe` | probes |
| `spec.ingress` | `rules[]` with `name` (DNS label, host = name + `INGRESS_HOST_SUFFIX`), `path`, `pathType`, `servicePort`; `ingressClassName`, `tlsSecretName` |
| `spec.unhealthyDuration`, `revisionHistoryLimit` | auto-rollback after sustained unhealthiness |
| `spec.codeSource` | `artifactName`, `tag`, `indexURL`, `mountPath` (default `/weave-code`), `loaderImage` |
| `spec.serviceAccountName`, security contexts | as for [WeaveJobTemplate](/contracts/crds/weavejobtemplate.md) |
| `status.valid`, `validationMessage` | invalid when `spec.ingress` is set but no host suffix is configured |

[^types]

# Usage

Referenced by a [WeaveChain](/contracts/crds/weavechain.md) step with `stepKind: Deploy` ([deploy step](/glossary/deploy-step.md)). Resources are named `<chain>-<step>`, owned by the chain (they survive runs), and rolling-updated by later runs. With `codeSource`, a moved index tag triggers a rolling restart.[^flux]

[^types]: weaveservicetemplate_types.go
[^flux]: fusion-weave CLAUDE.md
