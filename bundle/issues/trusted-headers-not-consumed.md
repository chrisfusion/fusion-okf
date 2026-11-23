---
type: Known Issue
title: forge and index ignore the X-User-* trusted headers
description: The BFF forwards X-User-* identity and group headers, but neither fusion-forge nor fusion-index reads them yet, so owner-group isolation is not enforced.
resource: repo://fusion-shared/docs/multi-tenancy.md
tags: [forge, index, bff, auth, multi-tenancy]
resolution: unresolved
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: mt, resource: repo://fusion-shared/docs/multi-tenancy.md, title: multi-tenancy plan }
---

# State

- [fusion-bff](/services/fusion-bff.md) resolves owner groups at login and forwards them as `X-User-Groups`, along with the other [trusted headers](/contracts/trusted-headers.md). It does this forward-only.[^bff]
- [fusion-forge](/services/fusion-forge.md) and [fusion-index](/services/fusion-index.md) contain no code that reads `X-User-*`. Their CLAUDE.md files only point to the cross-project plan.[^forge][^index]

# Impact

Every authenticated user who passes the BFF's route RBAC sees and changes all artifacts and builds, whatever their [owner group](/glossary/owner-group.md).

# Plan

The rollout is described in the multi-tenancy plan in [fusion-shared](/services/fusion-shared.md).[^mt] Read it before touching ownership or these headers.

[^bff]: fusion-bff CLAUDE.md
[^forge]: fusion-forge CLAUDE.md
[^index]: fusion-index CLAUDE.md
[^mt]: multi-tenancy plan
