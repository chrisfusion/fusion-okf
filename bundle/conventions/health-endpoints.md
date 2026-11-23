---
type: Convention
title: Health endpoints
description: Two health-path families exist - Quarkus-style /q/health/live|ready for the REST services ported from Quarkus, and /healthz|/readyz for operators and newer APIs.
tags: [forge, index, content, weave, wizard, bff, ext-bff, health]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: forge-chart, resource: repo://fusion-forge/deployment/templates/server-deployment.yaml, title: forge server-deployment.yaml }
  - { id: index-chart, resource: repo://fusion-index/deployment/templates/backend-deployment.yaml, title: index backend-deployment.yaml }
  - { id: content-chart, resource: repo://fusion-content/deployment/templates/deployment.yaml, title: content deployment.yaml }
  - { id: weave-chart, resource: repo://fusion-flux/deployment/fusion-weave/templates/api-deployment.yaml, title: weave api-deployment.yaml }
  - { id: wizard-chart, resource: repo://fusion-wizard/deployment/fusion-wizard/templates/api-deployment.yaml, title: wizard api-deployment.yaml }
  - { id: bff-values, resource: repo://fusion-bff/deployment/values.yaml, title: fusion-bff values.yaml }
  - { id: ext-values, resource: repo://fusion-ext-system-bff/deployment/values.yaml, title: fusion-ext-system-bff values.yaml }
---

# Current paths

| Component | Liveness | Readiness | Other |
|---|---|---|---|
| forge server | `/q/health/live` | `/q/health/ready`[^forge-chart] | |
| forge operator, watcher | `/healthz` | `/readyz` | |
| index backend | `/q/health/live` | `/q/health/ready`[^index-chart] | `/q/metrics` is JSON, see [issue](/issues/index-metrics-not-prometheus.md) |
| content | `/q/health/live` | `/q/health/ready`[^content-chart] | |
| weave operator and API | `/healthz` | `/readyz`[^weave-chart] | |
| wizard operator and API | `/healthz` | `/readyz`[^wizard-chart] | |
| bff, ext-bff | `/livez` | `/readyz`[^bff-values][^ext-values] | `/health` |

# Rules

- Health routes are public and sit outside auth. In chi (weave), register them on the root router *before* the Auth/RBAC middleware.
- New Go services use `/healthz` + `/readyz` (the controller-runtime family; agreed by `human:chrisfusion` on 2026-11-23). Keep `/q/health/*` where it exists, because probes, the bff and smoke tests depend on it.
- Anything that probes another service (e.g. the bff's `/bff/system-health`) must use the target's real path. The bff defaults are currently wrong for three services: [known issue](/issues/bff-health-url-defaults.md).

[^forge-chart]: forge server-deployment.yaml
[^index-chart]: index backend-deployment.yaml
[^content-chart]: content deployment.yaml
[^weave-chart]: weave api-deployment.yaml
[^wizard-chart]: wizard api-deployment.yaml
[^bff-values]: fusion-bff values.yaml
[^ext-values]: fusion-ext-system-bff values.yaml
