---
type: REST API
title: fusion-content REST API
description: Read-only content API - changelog entries, help articles and video metadata from polled git repos under /api/v1, TokenReview auth; no spec file.
resource: repo://fusion-content/internal/api/router.go
tags: [content, api, docs]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:40:00Z }
sources:
  - { id: router, resource: repo://fusion-content/internal/api/router.go, title: content router.go }
  - { id: auth, resource: repo://fusion-content/internal/api/middleware/auth.go, title: content auth middleware }
  - { id: content, resource: repo://fusion-content/CLAUDE.md, title: fusion-content CLAUDE.md }
---

**Reference:** `internal/api/router.go`, plus the content-format sections of fusion-content's CLAUDE.md and `docs/help-tutorial.md`.[^router][^content]

# Basics

- **Port:** 8080. Through the BFF: `/api/content/*`, which needs permission `content:changelog:read`.
- **Auth:** TokenReview service-account bearer token on `/api/v1`, switched by `AuthEnabled`.[^auth]
- **Health:** `/q/health/live`, `/q/health/ready`.
- **State:** in memory only; content is re-read from git on a poll interval.

# Routes (`/api/v1`, all GET)

| Route | Content |
|---|---|
| `/changelog` | Keep-a-Changelog entries parsed from each configured repo (paginated). See [changelog convention](/conventions/changelog-and-releases.md). |
| `/help`, `/help/:service/:type/:slug` | Diátaxis Markdown articles |
| `/videos`, `/videos/:service/:slug` | video metadata |

Sources: [^router][^content]

[^router]: content router.go
[^auth]: content auth middleware
[^content]: fusion-content CLAUDE.md
