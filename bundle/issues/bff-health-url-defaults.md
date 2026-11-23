---
type: Known Issue
title: BFF health probe defaults miss forge, index and weave
description: fusion-bff probes `<url>/health` for forge, index and weave, but none of them serves that path, so /bff/system-health reports them down unless the URL is overridden.
resource: repo://fusion-bff/internal/config/config.go
tags: [bff, forge, index, weave, health]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: bff-config, resource: repo://fusion-bff/internal/config/config.go, title: fusion-bff config.go }
  - { id: bff-values, resource: repo://fusion-bff/deployment/values.yaml, title: fusion-bff values.yaml }
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: weave-router, resource: repo://fusion-flux/internal/apiserver/router.go, title: fusion-weave router.go }
---

# Symptom

`/bff/system-health` (and the status view in [fusion-spectra](/services/fusion-spectra.md)) can show forge, index and weave as unhealthy even though they are running.

# Cause

[fusion-bff](/services/fusion-bff.md) builds default probe URLs from the upstream base URL:[^bff-config]

| Upstream | BFF default | Path the service actually serves |
|---|---|---|
| forge | `/health` | `/q/health/live`, `/q/health/ready` (Quarkus)[^forge] |
| index | `/health` | `/q/health/live`, `/q/health/ready`[^index] |
| weave | `/health` | `/healthz`, `/readyz`[^weave-router] |
| wizard | `/healthz` | correct |
| content | `/q/health/ready` | correct |

The chart leaves `forgeHealthUrl`, `indexHealthUrl` and `weaveHealthUrl` empty, so these defaults apply.[^bff-values] fusion-fleet sets no override either.

# Workaround

Set `config.forgeHealthUrl` / `indexHealthUrl` to `<url>/q/health/ready` and `config.weaveHealthUrl` to `<url>/readyz` in the bff values.

# Fix

Change the three defaults in `config.go` and the comments in `values.yaml`. See the [health endpoints convention](/conventions/health-endpoints.md).

[^bff-config]: fusion-bff config.go
[^bff-values]: fusion-bff values.yaml
[^forge]: fusion-forge CLAUDE.md
[^index]: fusion-index CLAUDE.md
[^weave-router]: fusion-weave router.go
