---
type: Known Issue
title: fusion-bff CLAUDE.md does not mention the wizard upstream
description: The BFF proxies /api/wizard/* to fusion-wizard (health at /healthz), but the BFF's CLAUDE.md never mentions wizard.
resource: repo://fusion-bff/CLAUDE.md
tags: [bff, wizard, docs]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: bff-config, resource: repo://fusion-bff/internal/config/config.go, title: fusion-bff config.go }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

# Gap

`config.go` defines the wizard upstream and its `/healthz` probe,[^bff-config] but the word "wizard" does not appear in fusion-bff's CLAUDE.md.[^bff] An agent working only in the BFF repo misses two facts:

- [fusion-wizard](/services/fusion-wizard.md) validates the token audience, which must be `fusion-bff`. Otherwise every call fails with 401.[^wizard]
- Its health path is `/healthz`, not `/health`.

The upstream table on the [fusion-bff](/services/fusion-bff.md) page already lists the wizard upstream.

# Fix

Add the wizard to the upstream list in fusion-bff's CLAUDE.md (an edit in that repo).

[^bff]: fusion-bff CLAUDE.md
[^bff-config]: fusion-bff config.go
[^wizard]: fusion-wizard CLAUDE.md
