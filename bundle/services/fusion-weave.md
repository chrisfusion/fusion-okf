---
type: Service
title: fusion-weave
description: Kubernetes operator that runs job DAGs, triggered runs, deploy steps and WeaveApps, plus a REST and monitoring API; repo directory is fusion-flux.
resource: repo://fusion-flux
tags: [weave, operator, scheduler]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# Purpose

Executes workloads. Two models exist side by side:[^flux]

- **DAG model** - [WeaveJobTemplate](/contracts/crds/weavejobtemplate.md) / [WeaveServiceTemplate](/contracts/crds/weaveservicetemplate.md) (step blueprints) → [WeaveChain](/contracts/crds/weavechain.md) (DAG of steps) → [WeaveTrigger](/contracts/crds/weavetrigger.md) (OnDemand, Cron, Webhook, BatchCron, Kafka) → [WeaveRun](/contracts/crds/weaverun.md) (one execution).
- **Fast lane** - [WeaveApp](/contracts/crds/weaveapp.md): one resource that owns a service (Deployment/Service/Ingress) or a set of job entrypoints, no DAG.

The name: the directory is `fusion-flux`, the service, chart, git origin and Flux names are `fusion-weave`. See [weave vs flux](/glossary/weave-vs-flux.md).[^fleet]

# Binaries (one image)

| Binary | Role |
|---|---|
| `/manager` | Operator: reconcilers per CRD, DAG engine, cron/batch/Kafka/webhook schedulers |
| `/api-server` | REST API (chi), port 8082; monitoring API under `/monitor/v1/`, Prometheus `/metrics` on port 9091 |
| `/loader` | `code-loader` init container: downloads artifact files from index ([code source](/glossary/code-source.md)) |
| `/backup` | Daily CronJob dumping template/chain/trigger specs to S3; restore is manual |

# Interfaces

- **Provides:** CRUD for all CRDs under `/api/v1/` (`runs/{name}/image`, `apps/{name}/fire`, `batchtriggers`, `kafkatriggers`, `external-auth/options`, ...); `PATCH` is a raw JSON merge patch that silently drops unknown fields. Hand-written reference: `apidescription.md`.[^flux]
- **Consumes:** [fusion-index](/services/fusion-index.md) (tag resolve + metadata.yaml + downloads), Kafka (Redpanda in dev), S3 (backup), Keycloak (external-auth OIDC tokens).
- **Auth (API):** API key Secrets, OIDC JWT, or SA TokenReview; roles from the label `fusion-platform.io/role`: `viewer` (GET), `editor` (+POST/PUT/PATCH), `admin` (+DELETE).
- **Callers:** [fusion-bff](/services/fusion-bff.md) (`/api/weave/*`, `/api/weave/monitor/*`), [fusion-wizard](/services/fusion-wizard.md), Flux (user GitOps repos via the `fusion-weave-gitops` SA, WeaveApps only).

# Policies enforced by the operator

The operator, not the API, is the real gate (Flux, kubectl and PATCH bypass API validation):[^flux]

- `ALLOWED_IMAGE_PREFIXES` - image allowlist for run/trigger overrides; for WeaveApps an empty list means unrestricted.
- Workload policy on every built PodSpec: allowed service accounts, Secrets must carry `fusion-platform.io/mountable=true`, security floor, image allowlist.
- `FUSION_INDEX_URL` + `FUSION_INDEX_ALLOWED_URLS` - user-set `indexURL` must be allowed.
- Ingress hosts are DNS labels plus the cluster-wide `INGRESS_HOST_SUFFIX`; never free text.

# Deployment

Helm chart `deployment/fusion-weave/`, CRDs in `crds/` (never upgraded by Helm). The live `fusion` namespace is a raw-YAML install (`config/manager`, `config/rbac`), not a Helm release; `fusion-dev-a/b` are Flux-managed Helm releases.[^flux]

# Where to look

`repo://fusion-flux/CLAUDE.md` (very detailed gotchas), `apidescription.md`, `config/samples/`, showroom templates in `deployment/fusion-weave/templates/showroom/` ([showroom](/glossary/showroom.md)).

[^flux]: fusion-weave CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
