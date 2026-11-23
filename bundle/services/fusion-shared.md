---
type: Service
title: fusion-shared
description: Public repo with cross-project documents (multi-tenancy plan, logging principles) and planned shared Go libraries such as ownership.
resource: repo://fusion-shared
tags: [shared, docs, library]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: shared, resource: repo://fusion-shared/CLAUDE.md, title: fusion-shared CLAUDE.md }
  - { id: mt, resource: repo://fusion-shared/docs/multi-tenancy.md, title: Multi-tenancy / Ownership plan }
---

# Purpose

Single source of truth for documents and libraries that every fusion repo uses. Public repository (GPL-3.0, module `github.com/chrisfusion/fusion-shared`) - it must not contain internal hostnames, credentials or customer data, which is why this knowledge bundle lives in its own repo and links here instead.[^shared]

# Documents

| Document | Content |
|---|---|
| `docs/multi-tenancy.md` | Agreed contract for owner groups: wishes W1-W39, header contract, permissions, rollout. Read before touching ownership or `X-User-*` headers. |
| `docs/logging_principles.md` | `log/slog` everywhere, per-request logger, `LOG_LEVEL` / `LOG_FORMAT`. |
| `docs/ownership-package-plan.md` | Plan for the `ownership` Go package. |

Changes to the multi-tenancy plan add a new `W<n>` entry; answered questions stay listed.[^shared]

# Libraries

Planned first: `ownership` (scope, header parsing, SQL/label builders, service-account scope config). Consumers vendor the module, so tags must build offline; semver tags only for Go changes.[^shared]

# Relation to this bundle

The [trusted headers](/contracts/trusted-headers.md) contract summarizes the header part of the multi-tenancy plan;[^mt] the plan itself stays authoritative.

[^shared]: fusion-shared CLAUDE.md
[^mt]: Multi-tenancy / Ownership plan
