---
type: Glossary Term
title: Deploy step
description: A WeaveChain step with stepKind Deploy that creates or rolling-updates a long-lived Deployment, Service and Ingress owned by the chain.
tags: [glossary, weave]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

- Uses a [WeaveServiceTemplate](/contracts/crds/weaveservicetemplate.md); resource name `<chain>-<step>`, stable across runs.
- **Chain-owned** (normal) deployments survive the run; **run-owned** ones come from `stepOverrides` and are torn down with Stopped/Failed runs.
- Phase `Deployed` is non-terminal: dependents may start, the run stays `Running`.
- Health is monitored by the chain controller, with automatic rollback after `unhealthyDuration`.[^flux]

For a single service without a DAG, prefer a [WeaveApp](/contracts/crds/weaveapp.md). Shown as "Service" in spectra ([blueprint](/glossary/blueprint.md)).

[^flux]: fusion-weave CLAUDE.md
