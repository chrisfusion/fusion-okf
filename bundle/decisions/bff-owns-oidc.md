---
type: Decision
title: The BFF owns the whole OIDC flow
description: Accepted - fusion-bff runs the OIDC login and keeps tokens server-side behind an HttpOnly session cookie; fusion-spectra never sees Keycloak or a token.
tags: [bff, spectra, auth, decision]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T13:10:00Z }
sources:
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
---

**Status:** accepted, implemented.

# Decision

[fusion-bff](/services/fusion-bff.md) is the only component that talks to Keycloak. It runs the PKCE login, stores the session in memory, and gives the browser only an HttpOnly `sid` cookie. [fusion-spectra](/services/fusion-spectra.md) "knows nothing about Keycloak or tokens":[^spectra] it calls `GET /bff/userinfo` with credentials and redirects to `/bff/login` on 401.

# Consequences

- **Upstream calls carry the BFF's identity.** Upstreams receive the BFF's own service-account token plus [trusted headers](/contracts/trusted-headers.md) with the user's identity, never the user's token.[^bff]
- **RBAC is resolved once, at login.** The BFF maps groups to roles and permissions, then checks every `/api/*` route against them. spectra only mirrors the permission strings in `can()` to hide UI elements; that is not enforcement.[^spectra]
- **Sessions do not survive restarts.** The session store is in memory and single-pod, so a BFF restart logs everyone out.[^bff]
- **Each spectra host needs matching BFF settings.** Redirect URL, CORS origins and the bypass base URL must match, otherwise login loops. See [local DNS](/operations/local-dns.md).

# Reason recorded in the sources

Only the rule itself is recorded; the sources give no rationale. The effect is that tokens never reach the browser.

[^spectra]: fusion-spectra CLAUDE.md
[^bff]: fusion-bff CLAUDE.md
