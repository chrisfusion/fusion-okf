---
type: Glossary Term
title: Owner group
description: Team that owns platform resources; resolved by the BFF at login and forwarded as X-User-Groups, with service-side enforcement planned.
tags: [glossary, bff, shared, multi-tenancy]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: mt, resource: repo://fusion-shared/docs/multi-tenancy.md, title: Multi-tenancy / Ownership plan }
---

Separate from role-based RBAC. Membership = mapped OIDC group ∪ direct match on email or user id. Stored in the BFF tables `owner_groups`, `owner_group_oidc_mappings`, `owner_group_members`; resolved at login and forwarded upstream as `X-User-Groups`.[^bff]

**Today:** forward-only, nothing is enforced by owner group; a shared default group (`DEFAULT_OWNER_GROUP`) is always added.

**Planned:** personal groups per user, wildcard mapping `*` → `shared`, writable vs readable groups and enforcement inside each service through the shared `ownership` library. Do not extend the default-group code.[^mt]

See [trusted headers](/contracts/trusted-headers.md), [fusion-shared](/services/fusion-shared.md).

[^bff]: fusion-bff CLAUDE.md
[^mt]: Multi-tenancy / Ownership plan
