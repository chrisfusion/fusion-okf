---
type: REST API
title: fusion-wizard REST API
description: Wizard API on port 8083 - list definitions, create/retry/rollback/delete WizardRuns and inspect ledger resources under /api/v1, TokenReview auth with audience fusion-bff; no spec file.
resource: repo://fusion-wizard/internal/apiserver/router.go
tags: [wizard, api, provisioning]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T13:40:00Z }
sources:
  - { id: router, resource: repo://fusion-wizard/internal/apiserver/router.go, title: wizard router.go }
  - { id: server, resource: repo://fusion-wizard/internal/apiserver/server.go, title: wizard server.go }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
  - { id: bff-config, resource: repo://fusion-bff/internal/config/config.go, title: fusion-bff config.go }
---

**Reference:** `internal/apiserver/router.go`; no spec file exists.[^router] The BFF's `openapi.yaml` transcribes these routes for its own documentation.

# Basics

- **Port:** **8083**, service `fusion-wizard-api`. Through the BFF: `/api/wizard/*`.[^bff-config]
- **Auth:** Kubernetes TokenReview. If `AuthAudience` is set (`api.auth.audience`), the token must be valid for that audience. Behind the BFF it must be `fusion-bff`, otherwise every call returns 401.[^server][^wizard]
- **Health:** `/healthz`, `/readyz`.

# Routes (`/api/v1`)

| Group | Routes |
|---|---|
| [Definitions](/contracts/crds/wizarddefinition.md) | `GET /definitions`, `GET /definitions/{name}` |
| [Runs](/contracts/crds/wizardrun.md) | `GET/POST /runs`, `GET/DELETE /runs/{name}`, `POST /runs/{name}/retry`, `POST /runs/{name}/rollback`, `POST /runs/bulk-rollback` |
| [Resources](/contracts/crds/wizardresource.md) ([ledger](/glossary/ledger.md)) | `GET /resources` |

Sources: [^router]

# Gotchas

- **Input precedence:** run input, then definition default, then instance config.[^wizard]
- **Rollback:** ledger-driven, and deletes only objects the wizard created (`managed: true`).

[^router]: wizard router.go
[^server]: wizard server.go
[^wizard]: fusion-wizard CLAUDE.md
[^bff-config]: fusion-bff config.go
