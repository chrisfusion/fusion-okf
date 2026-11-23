---
type: REST API
title: fusion-index REST API
description: Artifact registry API - artifacts, semver versions, files, tags, types, retention and admin cleanup under /api/v1; the embedded openapi.yaml is served at /api/openapi.json and /swagger/.
resource: repo://fusion-index/internal/api/openapi/openapi.yaml
tags: [index, api, artifacts]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:40:00Z }
sources:
  - { id: spec, resource: repo://fusion-index/internal/api/openapi/openapi.yaml, title: fusion-index openapi.yaml }
  - { id: router, resource: repo://fusion-index/internal/api/router.go, title: index router.go }
  - { id: auth, resource: repo://fusion-index/internal/api/middleware/auth.go, title: index auth middleware }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
---

**Reference:** `internal/api/openapi/openapi.yaml`. It is embedded in the binary and served live at `GET /api/openapi.json` and `/swagger/`, both public.[^spec][^router] Because it is served, it stays in sync. README/EXAMPLES/API_ARCHITECTURE are hand-maintained and drift.[^index]

# Basics

- **Port:** 8080, service `fusion-index-backend`. Through the BFF: `/api/index/*`. Machine clients: via the [ext-bff](/apis/ext-bff-api.md).
- **Auth:** only `/api/v1` requires a TokenReview service-account bearer token (switched by `AuthEnabled`). Health, `/q/metrics`, the spec and swagger are public.[^auth][^index]
- **Health:** `/q/health/live`, `/q/health/ready`. `/q/metrics` is JSON ([issue](/issues/index-metrics-not-prometheus.md)).

# Routes (`/api/v1`)

| Group | Routes |
|---|---|
| Artifacts | `GET/POST /artifacts`, `GET/PUT/DELETE /artifacts/:id` |
| Versions | `GET/POST/DELETE /artifacts/:id/versions` (DELETE = bulk), `GET/DELETE /artifacts/:id/versions/:semver`, `GET /versions` |
| Files | `GET/POST .../versions/:semver/files` (multipart upload), `GET/DELETE .../files/:fileId`, `GET .../files/:fileId/download` |
| Tags | `GET /tags`, `PUT/DELETE /artifacts/:id/tags/:tag` |
| Types | `GET/POST /types`, `GET/PUT/DELETE /types/:typeId`, `GET /artifacts/:id/types`, `PUT/DELETE /artifacts/:id/types/:typeId` |
| Retention | `GET /retention-policies`, `GET/PUT/DELETE /artifacts/:id/retention`, `GET/PUT/DELETE /types/:typeId/retention` |
| Admin | `/admin/artifacts/empty`, `/admin/artifacts/no-files`, `/admin/versions`, `/admin/versions/empty`, `/admin/files/incomplete`, `/admin/types/unused`: GET lists, DELETE bulk-removes |

Sources: [^router]

# Gotchas

- **Inconsistent list shapes:** `GET /artifacts` is paginated (`{"items":[...]}`), while the versions and files lists return bare arrays.[^runner]
- **Combined filters:** `GET /artifacts` filters (`type`, `name`, `tag`) combine with AND since 0.6.0.
- **Duplicates:** a duplicate name, version or filename returns 409.[^index]
- **Filenames:** not validated ([issue](/issues/index-dotdot-filename.md)).
- **Naming:** artifact names follow [artifact naming](/contracts/artifact-naming.md).
- **Adding an endpoint:** update `openapi.yaml` and all three prose docs. `MetricsSnapshot` must mirror `metrics.Snapshot`.[^index]

[^spec]: fusion-index openapi.yaml
[^router]: index router.go
[^auth]: index auth middleware
[^index]: fusion-index CLAUDE.md
[^runner]: fusion-runner CLAUDE.md
