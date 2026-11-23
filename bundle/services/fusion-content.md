---
type: Service
title: fusion-content
description: In-memory content API that polls git repos and serves service changelogs, Diataxis help articles and video metadata.
resource: repo://fusion-content
tags: [content, help, changelog]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: content, resource: repo://fusion-content/CLAUDE.md, title: fusion-content CLAUDE.md }
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
---

# Purpose

Feeds the help drawer, help page and changelog view of [fusion-spectra](/services/fusion-spectra.md). No database - everything is cloned with go-git and indexed in memory.[^content]

# Content sources (repos config, mounted from a Secret)

| Kind | Repo layout | API |
|---|---|---|
| Changelogs | `CHANGELOG.md` (Keep a Changelog) of each listed service repo | `GET /api/v1/changelog` (grouped by date) |
| Help | `help/<service>/<type>/<slug>.md`, type = `tutorial` / `how-to` / `reference` / `explanation` (from the directory) | `GET /api/v1/help` (`service`, `type`, `tag`, `route`, `q`) |
| Videos | `videos/<service>/<slug>.md`, frontmatter only | `GET /api/v1/videos` |

Help frontmatter: `title`, `tags`, `routes` (exact static spectra paths for context help), `summary`.[^content]

# Interfaces

- Reached via [fusion-bff](/services/fusion-bff.md) at `/api/content/*` (permissions `content:help:read`, `content:videos:read`, `content:changelog:read`, all granted to every role).[^spectra]
- Health at `/q/health/live|ready`; SA TokenReview auth pattern copied from forge.
- Service identifiers must match spectra's activity-rail IDs (`data`, `weave`, `monitoring`, `forge`, `fusion-index`/`index`, `admin`).

# Conventions

Follows fusion-forge conventions, explicitly **not** fusion-flux. Exception: uses the standard `log` package, not slog. `readOnlyRootFilesystem` needs an `emptyDir` at `/tmp` for clones.[^content]

[^content]: fusion-content CLAUDE.md
[^spectra]: fusion-spectra CLAUDE.md
