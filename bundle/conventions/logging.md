---
type: Convention
title: Logging
description: Go services log through log/slog with LOG_LEVEL/LOG_FORMAT (JSON by default) and a per-request logger from LoggerFromCtx; controller-runtime binaries keep logr/zap.
resource: repo://fusion-shared/docs/logging_principles.md
tags: [forge, index, weave, bff, ext-bff, wizard, content, shared, logging]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: lp, resource: repo://fusion-shared/docs/logging_principles.md, title: logging_principles.md }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: content, resource: repo://fusion-content/CLAUDE.md, title: fusion-content CLAUDE.md }
---

The canonical text is `docs/logging_principles.md` in [fusion-shared](/services/fusion-shared.md). Read it before changing logging; this page only summarizes it.[^lp]

# Rules

- Use `log/slog` only: no `import "log"`, no direct logrus, zerolog or zap.
- `LOG_LEVEL` (`debug|info|warn|error`, default `info`) and `LOG_FORMAT` (`json|text`, default `json`) are fields in the `Config` struct, wired through Helm values → ConfigMap → env.[^lp]
- Request handlers log via `middleware.LoggerFromCtx(ctx)`, which carries `request_id`, never bare `slog.*`. Background and startup code uses `slog.Default()`.[^bff][^flux]
- Add structured context fields (ids, names, versions) on mutation error paths.

# Operators

Binaries built on [controller-runtime](/conventions/controller-runtime.md) keep its `logr`/`zap` setup. In weave, the HTTP layer (slog) and the operator controllers (zap) coexist in one binary.[^lp][^flux]

# Exception

[fusion-content](/services/fusion-content.md) uses the standard `log` package, and its CLAUDE.md says not to migrate. See [the known issue](/issues/content-logging-exception.md).[^content]

[^lp]: logging_principles.md
[^bff]: fusion-bff CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^content]: fusion-content CLAUDE.md
