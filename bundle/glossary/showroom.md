---
type: Glossary Term
title: Showroom
description: Optional demo tour shipped in the fusion-weave chart - Tier 1 self-contained chains, Tier 2 real code-source apps built from fusion-testcases.
tags: [glossary, weave, demo]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

Enabled with `showroom.enabled=true` on the [fusion-weave](/services/fusion-weave.md) chart; one template per chain under `templates/showroom/`, each with its own flag.[^flux]

- **Tier 1** (`showroom.chains.*`) - busybox/nginx only, no external dependencies (Kafka demo off by default).
- **Tier 2** (`showroom.codeSourceApps.*`) - deploys artifacts built from `fusion-testcases/testcases_v2/` via forge and tagged `stable` in index; the artifacts must exist first.

Formerly called `samples`.

[^flux]: fusion-weave CLAUDE.md
