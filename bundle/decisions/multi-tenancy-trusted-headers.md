---
type: Decision
title: Multi-tenancy via owner groups and BFF trusted headers
description: Proposed (draft design) - the BFF resolves owner groups and sends read/write scope as X-User-* headers; services enforce ownership through the fusion-shared ownership package.
resource: repo://fusion-shared/docs/multi-tenancy.md
tags: [bff, forge, index, weave, wizard, shared, multi-tenancy, auth, decision]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:40:00Z }
sources:
  - { id: mt, resource: repo://fusion-shared/docs/multi-tenancy.md, title: multi-tenancy plan }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
---

**Status:** proposed. Section 4 of the plan is a "DRAFT for review", and some of its items are still marked *(proposal)*.[^mt] The canonical text is `docs/multi-tenancy.md` in [fusion-shared](/services/fusion-shared.md); this page only summarizes the direction.

# Today

- The BFF resolves [owner groups](/glossary/owner-group.md) at login and forwards `X-User-Groups`, but nothing enforces them.[^mt]
- index has no owner column. forge stores only audit fields (`creator_id`/`creator_email`).
- See [known issue](/issues/trusted-headers-not-consumed.md).

# Proposed design

- **Header contract:** `X-User-ID`, `X-User-Email`, `X-User-Groups` (read), plus new headers:
  - `X-User-Writable-Groups`
  - `X-User-All-Groups`
  - `X-User-Default-Group` (itself still a proposal)

  The BFF strips these headers from client requests, and services honour them only from service accounts marked `trustedProxy`. At most 100 groups per header.[^mt]
- **Shared package:** `ownership` in fusion-shared. It provides:
  - `Scope` with `CanRead`/`CanWrite`/`CanCreate`/`CanMove`
  - SQL and label-selector builders
  - Gin middleware and a config file
  - fail-closed behaviour when nothing else applies
- **Services:**
  - an `owner_group` column (Postgres) or the label `fusion-platform.io/owner-group` (CRDs)
  - the scope is applied before pagination
  - a move endpoint `PUT /<resource>/{id}/owner`
  - an `ownership.enforce` switch for migration
- **Out-of-scope reads:** answer 404 instead of 403. Still a proposal.

# Consequences

Every service with owned resources (index, forge, weave, wizard) needs a migration and has to adopt the shared package. The GUI gets a group picker on every create form.

[^mt]: multi-tenancy plan
[^bff]: fusion-bff CLAUDE.md
