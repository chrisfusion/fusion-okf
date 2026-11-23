---
type: Known Issue
title: fusion-content uses the standard log package against the logging rules
description: The shared logging principles forbid import "log", but fusion-content logs with log.Printf and its CLAUDE.md says not to migrate to slog.
resource: repo://fusion-content/CLAUDE.md
tags: [content, shared, logging]
resolution: unresolved
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: content, resource: repo://fusion-content/CLAUDE.md, title: fusion-content CLAUDE.md }
  - { id: lp, resource: repo://fusion-shared/docs/logging_principles.md, title: logging_principles.md }
---

# Conflict

- `logging_principles.md`: use `log/slog`, with `LOG_LEVEL`/`LOG_FORMAT` and JSON by default.[^lp]
- [fusion-content](/services/fusion-content.md) CLAUDE.md: "uses standard `log` package (`log.Printf`, `log.Fatalf`) throughout - do **not** migrate to `slog`".[^content]

# Impact

content's logs are unstructured text with no level and no request id, so log collectors cannot correlate them with the other services.

# Resolution

Two options: record the exception, with its reason, in the logging principles, or migrate content. Until one of them happens, the content CLAUDE.md wins inside that repo. See [logging](/conventions/logging.md).

[^content]: fusion-content CLAUDE.md
[^lp]: logging_principles.md
