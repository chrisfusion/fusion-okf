---
type: REST API
title: fusion-ext-system-bff REST API
description: Machine-client gateway to fusion-index only - an authenticated /api/index/* proxy (OAuth2 client credentials, API key or open) and a read-only, type-filtered public /api/public/index/*; reference is ENDPOINT.md.
resource: repo://fusion-ext-system-bff/ENDPOINT.md
tags: [ext-bff, index, api, auth]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:40:00Z }
sources:
  - { id: endpoint, resource: repo://fusion-ext-system-bff/ENDPOINT.md, title: ext-bff ENDPOINT.md }
  - { id: router, resource: repo://fusion-ext-system-bff/internal/api/router.go, title: ext-bff router.go }
  - { id: mt, resource: repo://fusion-shared/docs/multi-tenancy.md, title: multi-tenancy plan }
---

**Reference:** `ENDPOINT.md`. The README and SETTINGS.md cover configuration.[^endpoint]

# Basics

- **Clients:** external systems, not humans. The only upstream is [fusion-index](/apis/index-api.md).[^mt]
- **Health:** `/health`, `/livez`, `/readyz`.

# Routes

| Route | Auth | Behaviour |
|---|---|---|
| `ANY /api/index/*path` | `SystemAuth` chain: OAuth2 client credentials, API key or open, then RBAC from `rbac.yaml` | Proxies to index. Identity is forwarded as `X-System-ID`/`X-System-Name`, without groups.[^router][^mt] |
| `GET /api/public/index/*path` | none | Read-only. `?type=<PUBLIC_TYPE>` (default `streamlit`) is forced on every request. With `PUBLIC_DOWNLOAD_TAG` set, version-specific paths return 403 unless the version carries that tag. Identity headers are stripped.[^endpoint] |

# Notes

- **Logging:** the router uses `gin.Logger()`, not the slog request middleware the [logging convention](/conventions/logging.md) asks for.[^router]
- **Deployment:** not deployed by the fleet ([issue](/issues/ext-bff-flux-dir-missing.md)).

[^endpoint]: ext-bff ENDPOINT.md
[^router]: ext-bff router.go
[^mt]: multi-tenancy plan
