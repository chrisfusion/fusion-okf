---
type: Contract
title: Trusted identity headers
description: Headers the BFFs set on proxied requests to carry the caller's identity and owner groups, and the rules for trusting them.
tags: [bff, ext-bff, wizard, forge, index, weave, security, contract]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: extbff, resource: repo://fusion-ext-system-bff/CLAUDE.md, title: fusion-ext-system-bff CLAUDE.md }
  - { id: mt, resource: repo://fusion-shared/docs/multi-tenancy.md, title: Multi-tenancy / Ownership plan }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

# Headers

| Header | Set by | Meaning | Status |
|---|---|---|---|
| `X-User-ID` | [fusion-bff](/services/fusion-bff.md) | OIDC subject / user id | live |
| `X-User-Email` | fusion-bff | user email | live |
| `X-User-Groups` | fusion-bff | owner groups the user may see, comma-separated | live (forward-only) |
| `X-User-Writable-Groups` | fusion-bff | subset the user may write to | planned (W24) |
| `X-User-All-Groups` | fusion-bff | `true` if the user holds `admin:all-groups:access` | planned (W13) |
| `X-User-Default-Group` | fusion-bff | group used when a create names none | proposal (W14) |
| `X-System-ID`, `X-System-Name` | [fusion-ext-system-bff](/services/fusion-ext-system-bff.md) | machine client identity | live |
| `X-Request-ID` | BFF logging middleware | request correlation | live |

[^bff][^extbff][^mt]

# Trust rules

- The BFF strips all identity headers from incoming client requests before setting them from the session or token.
- The BFF calls upstreams with its **own** service-account token; the headers only describe the human behind the call.
- Services must honour the headers only from service accounts marked as trusted proxy (BFF; wizard and weave API as forwarding proxies) and ignore them from anyone else.[^mt]
- Today: [fusion-wizard](/services/fusion-wizard.md) stamps `createdBy` from `X-User-ID` only for allowlisted BFF service accounts.[^wizard] forge and index do not consume the headers yet (`creator_id` and per-user list scoping are planned).[^bff]
- Header size: at most 100 groups per header; above that the BFF truncates deterministically (proposal).

The authoritative plan is `fusion-shared/docs/multi-tenancy.md`; see [owner group](/glossary/owner-group.md).

[^bff]: fusion-bff CLAUDE.md
[^extbff]: fusion-ext-system-bff CLAUDE.md
[^mt]: Multi-tenancy / Ownership plan
[^wizard]: fusion-wizard CLAUDE.md
