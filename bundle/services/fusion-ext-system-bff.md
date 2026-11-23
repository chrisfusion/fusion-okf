---
type: Service
title: fusion-ext-system-bff
description: Machine-to-machine gateway for CI/CD and third-party systems - oauth2 or API-key auth, RBAC, proxy to fusion-index and a public download endpoint.
resource: repo://fusion-ext-system-bff
tags: [ext-bff, auth, proxy]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: extbff, resource: repo://fusion-ext-system-bff/CLAUDE.md, title: fusion-ext-system-bff CLAUDE.md }
---

# Purpose

Counterpart of [fusion-bff](/services/fusion-bff.md) for non-human clients: no browser sessions, no cookies. Today it proxies only [fusion-index](/services/fusion-index.md); more upstreams are on the roadmap.[^extbff]

# Auth modes (`AUTH_MODES`, comma-separated)

| Mode | Credential | Identity |
|---|---|---|
| `oauth2` | `Bearer` access token (client credentials), JWKS-validated | `client_id` / `sub` |
| `apikey` | `X-Api-Key` header, SHA-256-hashed keys from env (`APIKEY_HASHED_KEYS`) or DB (`system_api_keys`) | system name bound to the key |
| `open` | none | `anonymous` - never in production |

Identity → roles via `system_roles` in `rbac.yaml`, then the same first-match `route_permissions` semantics as fusion-bff. Forwarded upstream as `X-System-ID` / `X-System-Name` ([trusted headers](/contracts/trusted-headers.md)).[^extbff]

# Public endpoint

`/api/public/index/*` needs no auth. Listings get `?type=<PUBLIC_TYPE>` forced (default `streamlit`); with `PUBLIC_DOWNLOAD_TAG` set, the `TagGate` middleware only allows downloads of versions carrying that tag.[^extbff]

# Deployment

Helm chart `deployment/` with its own `rbac.yaml` copy (keep root and chart copy in sync), Flux config in `flux/`, semver image tags only. Route reference: `ENDPOINT.md`.

[^extbff]: fusion-ext-system-bff CLAUDE.md
