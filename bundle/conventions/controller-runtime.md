---
type: Convention
title: Kubernetes operators with controller-runtime
description: forge, weave and wizard operators are built on controller-runtime v0.19.3 and client-go v0.31.0, with probes on /healthz and /readyz and logr/zap logging.
tags: [forge, weave, wizard, operator, crd]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: forge-mod, resource: repo://fusion-forge/go.mod, title: fusion-forge go.mod }
  - { id: flux-mod, resource: repo://fusion-flux/go.mod, title: fusion-weave go.mod }
  - { id: wizard-mod, resource: repo://fusion-wizard/go.mod, title: fusion-wizard go.mod }
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

# Stack

| Repo | Binaries | controller-runtime | client-go |
|---|---|---|---|
| [fusion-forge](/services/fusion-forge.md) | operator (CIBuild), watcher (GitWatcher) | v0.19.3[^forge-mod] | v0.31.0 |
| [fusion-weave](/services/fusion-weave.md) | operator plus API server in one binary | v0.19.3[^flux-mod] | v0.31.0 |
| [fusion-wizard](/services/fusion-wizard.md) | operator plus API | v0.19.3[^wizard-mod] | v0.31.0 |

All three are on the same versions today. *Proposal:* upgrade them together, since they share CRD tooling (`controller-gen`) and run on the same clusters.

# Practice

- CRD types live in `api/v1alpha1/`. `make generate` writes deepcopy code and CRDs, then the CRDs are copied into the chart: see [Helm and CRDs](/conventions/helm-and-crds.md).
- Manager probes: `/healthz` (liveness) and `/readyz` (readiness) on the health port. See [health endpoints](/conventions/health-endpoints.md).
- Logging: keep controller-runtime's `logr`/`zap`. HTTP code in the same binary uses slog. See [logging](/conventions/logging.md).
- Tests: controller-runtime's fake client for pure logic (e.g. weave `internal/backup`).[^flux] wizard runs `make test` with `-race`, which is required because the ledger and the reconciler are concurrent.[^wizard]
- weave: never `gofmt -w` `api/v1alpha1/weaverun_types.go`. gofmt rewrites a CEL rule in a doc comment into a broken CRD rule.[^flux]

[^forge-mod]: fusion-forge go.mod
[^flux-mod]: fusion-weave go.mod
[^wizard-mod]: fusion-wizard go.mod
[^forge]: fusion-forge CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
