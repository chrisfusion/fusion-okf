---
type: Known Issue
title: fusion-index /q/metrics is JSON, not Prometheus
description: The Quarkus-style path /q/metrics returns a JSON registry snapshot, so a Prometheus scrape of it fails.
resource: repo://fusion-index/internal/api/handlers/metrics.go
tags: [index, metrics, observability]
resolution: unresolved
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: metrics, resource: repo://fusion-index/internal/api/handlers/metrics.go, title: fusion-index metrics.go }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
---

# Symptom

A ServiceMonitor or scrape config aimed at `/q/metrics` on [fusion-index](/services/fusion-index.md) gets parse errors.

# Cause

`GET /q/metrics` returns `c.JSON(200, snapshot)`: aggregate registry figures (`MetricsSnapshot` in `openapi.yaml`), cached for `METRICS_CACHE_TTL` (default 60s) and always public.[^metrics][^index] The path follows the Quarkus convention, where it serves Prometheus text, but the content does not.

# Fix options

- Leave `/q/metrics` as the JSON endpoint and add a Prometheus endpoint elsewhere, e.g. `/metrics`, or
- rename the JSON endpoint (an API change: spectra and the bff OpenAPI would have to follow).

[^metrics]: fusion-index metrics.go
[^index]: fusion-index CLAUDE.md
