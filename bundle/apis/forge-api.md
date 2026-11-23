---
type: REST API
title: fusion-forge REST API
description: Build API of fusion-forge - requirements, git and app builds, GitWatcher CRUD and bulk build maintenance under /api/v1, TokenReview auth; no OpenAPI file, the router is the reference.
resource: repo://fusion-forge/internal/api/router.go
tags: [forge, api, build]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T13:40:00Z }
sources:
  - { id: router, resource: repo://fusion-forge/internal/api/router.go, title: forge router.go }
  - { id: auth, resource: repo://fusion-forge/internal/api/middleware/auth.go, title: forge auth middleware }
  - { id: examples, resource: repo://fusion-forge/EXAMPLES.md, title: forge EXAMPLES.md }
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
---

**Reference:** there is no OpenAPI file. The routes are in `internal/api/router.go`;[^router] curl examples for every group are in `EXAMPLES.md`;[^examples] and the BFF's `openapi.yaml` transcribes them (see [BFF API](/apis/bff-api.md)).

# Basics

- **Port:** 8080. Through the BFF: `/api/forge/*` (the prefix is stripped).
- **Auth:** `/api/v1` requires a Kubernetes service-account bearer token, checked with TokenReview. With `AuthEnabled=false` the check is a no-op.[^auth]
- **Health:** `/q/health/live`, `/q/health/ready` (public).

# Routes (`/api/v1`)

| Group | Routes | Notes |
|---|---|---|
| Requirements builds | `GET/POST /venvs`, `POST /venvs/validate`, `GET /venvs/:id`, `GET /venvs/:id/logs` | multipart (requirements file) |
| Git builds | same shape under `/gitbuilds` | JSON body, not multipart[^forge] |
| App builds | same shape under `/appbuilds` | from [metadata.yaml](/contracts/metadata-yaml.md) |
| [GitWatchers](/contracts/crds/gitwatcher.md) | `GET/POST /gitwatchers`, `GET/PUT/DELETE /gitwatchers/:name` | stored as CRs only, no DB rows |
| Bulk maintenance | `DELETE /builds`, `POST /builds/zombie-cleanup`, `POST /builds/index-drift-cleanup` | spans all build types |

Sources: [^router]

# Gotchas

- `*/validate` endpoints must stay read-only: they must never create artifacts in [index](/apis/index-api.md).[^forge]
- Build types and their naming trap: [build type](/glossary/build-type.md), [known issue](/issues/forge-builder-names-swapped.md).

[^router]: forge router.go
[^auth]: forge auth middleware
[^examples]: forge EXAMPLES.md
[^forge]: fusion-forge CLAUDE.md
