---
type: Known Issue
title: Local port-forward ports used twice
description: The CLAUDE.md files forward forge and index both to local port 18080, and content and ext-bff both to 18082, so these pairs cannot be port-forwarded at the same time.
tags: [content, ext-bff, operations]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: content, resource: repo://fusion-content/CLAUDE.md, title: fusion-content CLAUDE.md }
  - { id: ext-bff, resource: repo://fusion-ext-system-bff/CLAUDE.md, title: fusion-ext-system-bff CLAUDE.md }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
---

# Symptom

`kubectl port-forward` fails with "address already in use" when a second service is forwarded to 18080 or 18082.

# Cause

Documented local ports:

| Port | Service |
|---|---|
| 18080 | [fusion-forge](/services/fusion-forge.md)[^forge] **and** [fusion-index](/services/fusion-index.md)[^index] |
| 18081 | [fusion-bff](/services/fusion-bff.md)[^bff] |
| 18082 | [fusion-content](/services/fusion-content.md)[^content] **and** [fusion-ext-system-bff](/services/fusion-ext-system-bff.md)[^ext-bff] |

# Workaround

Forward the second service of a pair to a free port, e.g. `18083:8080`.

# Fix

Give each service its own local port. The [minikube](/operations/minikube.md) page is the place for a port table.

[^forge]: fusion-forge CLAUDE.md
[^index]: fusion-index CLAUDE.md
[^bff]: fusion-bff CLAUDE.md
[^content]: fusion-content CLAUDE.md
[^ext-bff]: fusion-ext-system-bff CLAUDE.md
