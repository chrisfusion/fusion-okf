---
type: Custom Resource
title: WeaveTrigger
description: Activation source for a WeaveChain (weave.fusion-platform.io/v1alpha1, short name ft) - OnDemand, Cron, Webhook, BatchCron or Kafka - that creates WeaveRuns.
resource: repo://fusion-flux/api/v1alpha1/weavetrigger_types.go
tags: [weave, crd, trigger, scheduling]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: types, resource: repo://fusion-flux/api/v1alpha1/weavetrigger_types.go, title: weavetrigger_types.go }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.chainRef` | chain to run |
| `spec.type` | `OnDemand`, `Cron`, `Webhook`, `BatchCron`, `Kafka` |
| `spec.schedule` | Cron: **6 fields, seconds first** (`0 0 9 * * *`) |
| `spec.webhook` | `path`, `secretRef` (Bearer token, required) |
| `spec.batchCron` | `jobsConfigMapRef` - list of jobs with their own standard 5-field schedules |
| `spec.kafka` | `brokers`, `topic`, `consumerGroup`, `secretRef`, `tls`, `eventFilter`, `bucketFilter` (S3 events), `maxConcurrentRuns` |
| `spec.paused` | user pause |
| `spec.parameterOverrides`, `imageOverrides` | copied into every created run (image overrides only for Job steps) |
| `spec.authSecretRefOverride`, `externalAuthRefOverride`, `unsafeEnvironmentInjectorOverride` | override the chain's settings (run > trigger > chain) |
| `status.active`, `inactiveReason` | activation state (`active` is required in the CRD) |
| `status.quarantined`, `quarantineReason`, `quarantinedAt` | set after a panic in the trigger's goroutine; cleared only by annotation `fusion-platform.io/reset=true` |
| `status.lastScheduleTime`, `lastRunName`, `webhookURL`, `pendingRuns`, `batchJobCount`, `batchJobErrors` | runtime info |

[^types]

# Operations

- Fire on demand: annotation `fusion-platform.io/fire=true` (use `--overwrite`).
- Created runs carry the labels `fusion-platform.io/trigger` and `fusion-platform.io/chain` (BatchCron also `fusion-platform.io/batch-job-id`); custom trigger labels are **not** propagated.
- REST: generic `/api/v1/triggers` plus dedicated `/batchtriggers` (creates the jobs ConfigMap) and `/kafkatriggers`.[^flux]

[^types]: weavetrigger_types.go
[^flux]: fusion-weave CLAUDE.md
