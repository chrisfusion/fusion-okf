---
type: Custom Resource
title: WeaveApp
description: Single-resource fast lane (weave.fusion-platform.io/v1alpha1, short name fa) that owns either a service or a set of job entrypoints, without templates, chains or runs.
resource: repo://fusion-flux/api/v1alpha1/weaveapp_types.go
tags: [weave, crd, app]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: types, resource: repo://fusion-flux/api/v1alpha1/weaveapp_types.go, title: weaveapp_types.go }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.type` | `service` or `job` |
| `spec.image` | always required; the runner image when `codeSource` is set |
| `spec.codeSource` | index artifact + tag loaded at pod start ([code source](/glossary/code-source.md)) |
| `spec.command`, `args`, `env`, `resources`, `volumes` | container definition |
| `spec.writablePaths[]` | `mountPath`, `sizeLimit`, `medium` - emptyDirs for read-only root filesystems |
| `spec.serviceAccountName`, security contexts | pod service account; security contexts override `WORKLOAD_SECURITY_DEFAULTS` |
| `spec.service` | type=service: `ports`, `replicas`, `serviceType`, `ingressName` / `ingress`, `ingressAnnotations`, probes |
| `spec.entrypoints[]` | type=job: `name`, `command`, `args`, `env`, `schedule` (6-field, seconds first) |
| `spec.externalAuthRef` | jobs only |
| `spec.activeDeadlineSeconds`, `executionTTLSeconds` | job limits; finished job logs expire after the TTL (24 h) |
| `status.phase` | `Pending`, `Ready`, `Running`, `Invalid` |
| `status.deploymentName`, `codeSourceDeployedVersion` | service state |
| `status.executions[]` | last 20 job executions (`entrypoint`, `jobName`, `phase`) |

[^types]

# Semantics

- Everything is owner-referenced to the app: deleting it is the full teardown.
- Jobs are created by the operator per launch (never CronJobs, because the external-auth token is minted per launch).
- Fire an entrypoint: annotation `fusion-platform.io/fire=<entrypoint>` or `POST /api/v1/apps/{name}/fire` (BFF permission `weave:apps:fire`, granted to common users).
- Not supported: Kafka/BatchCron triggers, step outputs, shared storage, backup.
- Logs: `GET /monitor/v1/apps/{name}/logs`.[^flux]
- Created by [fusion-wizard](/services/fusion-wizard.md)'s `app` step for all wizards except the batch ones; can also come from user GitOps repos via the `fusion-weave-gitops` service account.[^wizard]

[^types]: weaveapp_types.go
[^flux]: fusion-weave CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
