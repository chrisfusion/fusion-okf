---
type: Service
title: fusion-index
description: Artifact registry storing namespaced, semver-versioned artifacts with files, configs, mutable tags, types and retention policies.
resource: repo://fusion-index
tags: [index, registry, storage]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

# Purpose

Central store for everything the platform builds. Artifacts have dotted names (`org.team.name`, in practice `app.<name>` / `venv.<name>`), versions are `major.minor.patch` integers, each version holds files plus a free-form `config`, and tags (`stable`, ...) point at one version and can move.[^index]

# Data model

| Table | Holds |
|---|---|
| `registry_artifact` | name, description, trigger-maintained size/count statistics |
| `registry_artifact_version` | `major/minor/patch` (no `version` column), `config` |
| `registry_artifact_file` | name, size, storage backend/path, `status` PENDING / AVAILABLE / ERROR |
| `registry_artifact_tag` | unique `(artifact, tag)` → version; upsert moves the tag |
| `registry_artifact_type` (+ map) | M:N artifact types (e.g. `streamlit`) |
| `registry_retention_policy` | `keepLast` / `maxAgeDays` per artifact or type - stored, never applied by index itself |

# Interfaces

- **Provides:** REST `/api/v1/` - artifacts, versions, files (multipart upload, streaming download), tags, types, retention, admin cleanup; hand-written OpenAPI 3.1 at `/api/openapi.json`, Swagger UI at `/swagger/`; health `/q/health/*`; `/q/metrics` (JSON, **not** Prometheus format).[^index]
- **Callers:** [forge](/services/fusion-forge.md) (create/upload/tag), [weave](/services/fusion-weave.md) (tag resolve, file download via code-loader), [runner](/services/fusion-runner.md) (`IndexPythonRunner`), [wizard](/services/fusion-wizard.md), both BFFs.
- **Auth:** Kubernetes SA TokenReview on `/api/v1` only (no client-go; own minimal in-cluster client); health, metrics, OpenAPI and Swagger are always public.[^index]

# Response-shape pitfalls for clients

- `GET /artifacts?name=` is a case-insensitive **prefix** filter, paginated (`{"items": [...]}`, 20 per page by default) - match `fullName` exactly on the client side.[^flux]
- `GET .../versions` and `GET .../versions/{semver}/files` return **bare arrays**.[^runner]
- `VersionResponse.version` is already the formatted semver; `FileResponse.downloadUrl` is the ready relative download path.
- Errors are always `{"error": "..."}`; duplicates answer 409.

# Storage and backup

- Backends: `FILESYSTEM` (PVC `fusion-index-backend-artifacts` in dev) or `S3` with `S3_PREFIX` (Helm default `<namespace>/index/data`) so several instances can share a bucket. The DB stores relative paths only.[^index]
- S3 is the source of truth for files; a daily CronJob `backup-db` dumps metadata only. `restore-db` is manual and deliberately not templated in the chart.
- PostgreSQL is external only (since 0.5.0); a hook Job creates the `fusion_index` database. In dev-cluster instances it is a hand-rolled `postgres:18-trixie` named `fusion-index-postgresql`, shared with fusion-bff.[^fleet]

# Cross-repo notes

- Runs as distroless nonroot UID 65532; root-owned files left on an old PVC break uploads.
- Behind Linkerd set `linkerd.opaquePorts: "8080"`; behind nginx ingress `ingress.proxyBodySize` (default `100m`) - otherwise large uploads fail silently.
- index accepts a file named `..` (path traversal on its side) - tracked as a cross-repo item in weave's plan.[^flux]

# Where to look

`repo://fusion-index/CLAUDE.md`, `internal/api/openapi/openapi.yaml`, `API_ARCHITECTURE.md`.

[^index]: fusion-index CLAUDE.md
[^runner]: fusion-runner CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
