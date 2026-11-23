---
type: Service
title: fusion-wizard
description: Operator plus REST API that provisions resources across forge, index and weave from declarative wizard definitions, with a ref-counted ledger and rollback.
resource: repo://fusion-wizard
tags: [wizard, operator, orchestration]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
  - { id: spectra-wizards, resource: repo://fusion-spectra/src/pages/wizards/CLAUDE.md, title: spectra wizards pages }
---

# Purpose

Replaces the browser-side orchestration of spectra's shortcut wizards ("Git → Python Service", "Image → Cron Job", ...) with a server-side, transactional process. All seven spectra wizards run against wizard definitions.[^wizard][^spectra-wizards]

# Model

- [WizardDefinition](/contracts/crds/wizarddefinition.md) - instance-agnostic recipe: parameters + an ordered subset of steps.
- [WizardRun](/contracts/crds/wizardrun.md) - one execution with parameters, a snapshot of the definition and per-step status.
- [WizardResource](/contracts/crds/wizardresource.md) - [ledger](/glossary/ledger.md) entry per upstream object, ref-counted across runs.

Fixed step order: `gitWatcher, waitBuild, tag, app, jobTemplate, serviceTemplate, chain, trigger, batchTrigger`.[^wizard]

| Step | Upstream call |
|---|---|
| `gitWatcher` | forge `POST /api/v1/gitwatchers` (with labels, optional `autoTag` via `autoPromote`) |
| `waitBuild` | polls forge builds (matched by repoUrl + projectDir) |
| `tag` | index tag on the built version |
| `app` | weave `POST /api/v1/apps` - one [WeaveApp](/contracts/crds/weaveapp.md) per service/job |
| `jobTemplate`, `serviceTemplate`, `chain`, `trigger` | weave DAG objects (still used by batch wizards) |
| `batchTrigger` | weave `POST /api/v1/batchtriggers` (BatchCron) |

# Design invariants (agreed, not to be re-litigated)

- Write-ahead: ledger entry first, upstream create second.
- Same name + different `specHash` = visible conflict, never a silent update; resources found without a ledger entry are `managed: false` and never deleted.
- Rollback is driven by the ledger, not by run status; undo order by kind: trigger, chain, template, **watcher**, tag, artifact (watcher before artifact, or forge rebuilds it).
- Runs use `spec.definitionSnapshot`, never the live definition.
- Precedence of values: run input > definition default > instance config (Helm-rendered ConfigMap).[^wizard]

# Interfaces

- **Provides:** REST (api-server) that only reads/writes CRs; validates everything on create and answers one 422 with `details`. Refuses to start without `AUTH_ALLOWED_SA`; stamps `createdBy` from `X-User-ID` only for allowlisted BFF service accounts.
- **Consumes:** forge, index, weave REST from the operator (SA token re-read per request). `AUTH_AUDIENCE` must match the caller's token audience (`fusion-bff`).
- **Labels:** stamps `fusion-platform.io/managed-by: wizard` and `wizard.fusion-platform.io/run: <run>` on everything it creates ([labels](/contracts/labels-and-annotations.md)).

# Where to look

`repo://fusion-wizard/CLAUDE.md`, chart definitions in `deployment/fusion-wizard/definitions/`.

[^wizard]: fusion-wizard CLAUDE.md
[^spectra-wizards]: spectra wizards pages CLAUDE.md
