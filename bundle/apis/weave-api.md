---
type: REST API
title: fusion-weave REST API
description: CRUD over the weave CRDs (job/service templates, chains, apps, triggers, runs, batch/kafka triggers) under /api/v1 plus a read-only /monitor/v1, on port 8082; reference is apidescription.md.
resource: repo://fusion-flux/apidescription.md
tags: [weave, api, scheduling]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T13:40:00Z }
sources:
  - { id: desc, resource: repo://fusion-flux/apidescription.md, title: fusion-weave apidescription.md }
  - { id: router, resource: repo://fusion-flux/internal/apiserver/router.go, title: weave router.go }
  - { id: mon, resource: repo://fusion-flux/internal/monitoring/routes.go, title: weave monitoring routes.go }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

**Reference:** `apidescription.md` in the `fusion-flux` clone (Markdown, not OpenAPI).[^desc] Its intro still says "all five CRDs", but the router serves more resources, so check `internal/apiserver/router.go` for the full set.[^router]

# Basics

- **Process and port:** a separate `/api-server` process on port **8082**, service `fusion-weave-api`. Through the BFF: `/api/weave/*`. The BFF calls weave with a token that has no audience.
- **Auth:** `Authorization: Bearer` with one of three token kinds:[^desc]
  - **API key:** a Secret labelled `fusion-platform.io/api-key=true`; the role comes from the annotation `fusion-platform.io/role`.
  - **OIDC JWT.**
  - **Service-account token (TokenReview):** the SA must be in the API's namespace or in `AUTH_SA_NAMESPACES`, and must carry the label `fusion-platform.io/role`.

  Roles are `viewer`/`editor`/`admin`. `AllowUnauthenticated` is for development only.
- **Health:** `/healthz`, `/readyz`, registered before the auth middleware.

# Routes (`/api/v1`, auth + RBAC)

Every resource gets the same six routes: `GET/POST /<res>`, `GET/PUT/PATCH/DELETE /<res>/{name}`.[^router]

| Resource | Extra routes |
|---|---|
| `/jobtemplates`, `/servicetemplates`, `/chains` | none |
| `/apps` ([WeaveApp](/contracts/crds/weaveapp.md)) | `POST /apps/{name}/fire`, `GET /apps/{name}/executions`, `GET /apps/{name}/manifest` |
| `/triggers` | none (image overrides checked against `ALLOWED_IMAGE_PREFIXES`) |
| `/runs` | `GET /runs/facets`, `POST /runs/{name}/stop`, `POST /runs/{name}/image` |
| `/batchtriggers` | `POST /batchtriggers/validate`, `POST /batchtriggers/{name}/stop`, `.../resume` |
| `/kafkatriggers` | none |
| options | `GET /image-overrides/options`, `GET /external-auth/options` |

# Monitoring (`/monitor/v1`, only with monitoring enabled)

GET-only, so the `viewer` role can see everything:[^mon]
- **Runs:** `/runs`, `/runs/{name}`, `/runs/{name}/jobs[/{jobName}]`, `/runs/{name}/steps/{step}/logs`, `/runs/{name}/events`
- **Apps and chains:** `/apps/{name}/logs`, `/chains/{name}/deployments`
- **Stats and events:** `/stats/runs`, `/stats/chains/{name}`, `/events`

Not to be confused with the Prometheus `metrics` port that `api.monitoring.enabled` exposes for the ServiceMonitor.[^fleet]

# Gotchas

The API validates image overrides, but PATCH via kubectl or Flux bypasses that check. The operator checks again when a run starts. CRD details: [WeaveRun](/contracts/crds/weaverun.md), [WeaveChain](/contracts/crds/weavechain.md), [WeaveTrigger](/contracts/crds/weavetrigger.md).

[^desc]: fusion-weave apidescription.md
[^router]: weave router.go
[^mon]: weave monitoring routes.go
[^fleet]: fusion-fleet CLAUDE.md
