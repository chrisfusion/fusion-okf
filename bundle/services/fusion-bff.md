---
type: Service
title: fusion-bff
description: Backend for the web GUI - OIDC login with sessions, allowlist, RBAC per route, and a proxy to forge, index, weave, wizard and content.
resource: repo://fusion-bff
tags: [bff, auth, rbac, proxy]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
  - { id: bff-config, resource: repo://fusion-bff/internal/config/config.go, title: fusion-bff config.go }
---

# Purpose

The only entry point for human users. [fusion-spectra](/services/fusion-spectra.md) knows nothing about Keycloak or tokens - the BFF owns the whole OIDC flow.[^bff]

# Responsibilities

1. **Login** - PKCE against Keycloak (`/bff/login`, `/bff/callback`, `/bff/logout`), HttpOnly `sid` cookie, in-memory session store (single pod; every restart logs everyone out).
2. **Allowlist** - `ALLOWED_USERS` (`sub` or email); empty = any authenticated user.
3. **RBAC** - JWT `groups` (leading `/` stripped) → roles → permissions, resolved at login; per-route check on every `/api/*` call. Group→role mappings from `rbac.yaml` (`group_source: jwt`), the DB (`db`) or both; plus direct user→role grants and resource-scoped permissions.[^bff]
4. **Proxy** - `/api/<svc>/*` → upstream with the prefix stripped, using the BFF's own SA token; identity forwarded as [trusted headers](/contracts/trusted-headers.md).
5. **Owner groups** - resolved at login, forwarded as `X-User-Groups` (forward-only today; enforcement moves into the services - see the multi-tenancy plan in [fusion-shared](/services/fusion-shared.md)).

# Upstreams

| Path prefix | Upstream | Default URL |
|---|---|---|
| `/api/forge/*` | [fusion-forge](/services/fusion-forge.md) | `http://fusion-forge.<ns>.svc:8080` |
| `/api/index/*` | [fusion-index](/services/fusion-index.md) | `http://fusion-index-backend.<ns>.svc:8080` |
| `/api/weave/*` | [fusion-weave](/services/fusion-weave.md) | `http://fusion-weave-api.<ns>.svc:8082` |
| `/api/wizard/*` | [fusion-wizard](/services/fusion-wizard.md) | `http://fusion-wizard-api.<ns>.svc:8083` (health `/healthz`)[^bff-config] |
| `/api/content/*` | [fusion-content](/services/fusion-content.md) | `http://fusion-content.<ns>.svc:8080` |

The default token for forge/index/content/wizard is minted for audience `fusion-bff`; weave gets a separate token without audience. Upstreams that validate audience must set it to `fusion-bff` (wizard: `api.auth.audience`), otherwise every call fails with 401.[^wizard]

# BFF-owned endpoints

`/bff/userinfo` (sub, email, roles, permissions, resource_permissions, owner_groups, preferred_owner_group), `/bff/preferences`, `/bff/system-health`, `/bff/admin/*` (group-roles, user-roles, resource-permissions, owner groups, service-status overrides).

# RBAC files

- `rbac.yaml` has `group_roles`, `role_permissions`, `route_permissions` (ordered, first match wins; `*` = one segment, trailing `*` = one or more), `permission_implies`.
- Two copies: repo root and `deployment/rbac.yaml` (the chart reads the latter) - always keep both in sync. The live file is the `fusion-bff-rbac` ConfigMap.
- Permission strings are mirrored in spectra's `can()` checks; a new role must also be added to spectra's `ROLES` list.[^spectra]
- Every upstream endpoint is itemized in `internal/docs/openapi.yaml` with `x-required-permission`.

# State

PostgreSQL database `fusion_bff` (optional, needed for `group_source: db|both`, owner groups, preferences) - shares the fusion-index Postgres server in dev. Hook Jobs: create-database and RBAC seed (`rbacSeed.adminGroup`, default `platform-admin`).[^bff]

# Where to look

`repo://fusion-bff/CLAUDE.md` (procedure for reflecting upstream API changes), `rbac.yaml`, `internal/docs/openapi.yaml`, `README.md`, `ARCHITECTURE.md`.

[^bff]: fusion-bff CLAUDE.md
[^spectra]: fusion-spectra CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
[^bff-config]: fusion-bff config.go (the wizard upstream is not yet documented in fusion-bff CLAUDE.md)
