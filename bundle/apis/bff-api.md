---
type: REST API
title: fusion-bff REST API
description: BFF-owned endpoints under /bff (login, userinfo, preferences, presets, system health, admin RBAC and owner groups) plus the /api/<svc>/* proxy; openapi.yaml documents both with x-required-permission.
resource: repo://fusion-bff/internal/docs/openapi.yaml
tags: [bff, api, auth, rbac, proxy]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:40:00Z }
sources:
  - { id: spec, resource: repo://fusion-bff/internal/docs/openapi.yaml, title: fusion-bff openapi.yaml }
  - { id: router, resource: repo://fusion-bff/internal/api/router.go, title: bff router.go }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
---

**Reference:** `internal/docs/openapi.yaml` (~8,400 lines), served at `GET /bff/openapi.yaml` with a UI at `/bff/docs/`.[^router] It covers the BFF's own endpoints and **every proxied upstream endpoint**, with schemas transcribed from the upstream services and `x-required-permission` on each route.[^bff] For the platform as a whole, it is the most complete API reference.

# Basics

- **Clients:** [fusion-spectra](/services/fusion-spectra.md) in the browser, using the HttpOnly `sid` cookie. See [BFF owns OIDC](/decisions/bff-owns-oidc.md).
- **Health:** `/health`, `/livez`, `/readyz`.

# BFF-owned routes (`/bff`)

| Group | Routes |
|---|---|
| Login | `GET /login`, `GET /callback`, `POST /logout`, `GET /userinfo` |
| Per user | `GET/PUT/DELETE /preferences`, `GET /presets` |
| Health | `GET /system-health` (probes the upstreams; see [issue](/issues/bff-health-url-defaults.md)), `GET/PUT/DELETE /admin/service-status[/:service]` |
| RBAC admin | `/admin/group-roles`, `/admin/user-roles`, `/admin/resource-permissions` (GET/POST, DELETE `/:id`), `GET /admin/rbac-config` |
| Owner groups | `/admin/owner-groups`, `/admin/owner-group-mappings`, `/admin/owner-group-members` (GET/POST, DELETE `/:id`) |

Every group except login is registered only when its handler is configured. Preferences and owner groups also need the database.[^router][^bff]

# Proxy (`/api`)

`/api/forge|index|weave|wizard|content/*` forwards any method, with the prefix stripped, to [forge](/apis/forge-api.md), [index](/apis/index-api.md), [weave](/apis/weave-api.md), [wizard](/apis/wizard-api.md) and [content](/apis/content-api.md).[^router] Before forwarding, the BFF checks permissions per route using `route_permissions` in `rbac.yaml` (first match wins), and adds the [trusted headers](/contracts/trusted-headers.md).[^bff]

# Changing an upstream API

When an upstream API changes, update all of these: `openapi.yaml`, both `rbac.yaml` copies, spectra's `can()` permission strings, and the CHANGELOG. New BFF-owned endpoints also need README, ARCHITECTURE and EXAMPLE updates. The full procedure is in fusion-bff's CLAUDE.md.[^bff]

[^spec]: fusion-bff openapi.yaml
[^router]: bff router.go
[^bff]: fusion-bff CLAUDE.md
