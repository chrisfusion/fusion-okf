---
type: Contract
title: Labels, annotations and finalizers
description: Kubernetes label, annotation and finalizer keys under fusion-platform.io used across forge, weave and wizard, and what each one means.
tags: [weave, forge, wizard, contract, kubernetes]
status: stable
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
verified: { by: human:chrisfusion, at: 2026-11-23T12:47:41Z }
sources:
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

# Ownership labels (on CRs created through the REST APIs)

| Key | Values | Set by |
|---|---|---|
| `fusion-platform.io/managed-by` | `manual` (default), `wizard`, open-valued | forge and weave API handlers default it to `manual` unless the caller set one; wizard sends `wizard`[^forge][^flux] |
| `wizard.fusion-platform.io/run` | wizard run name | fusion-wizard, on everything it creates[^wizard] |

`PUT` never touches metadata, so these labels survive updates. They answer "is this wizard-managed?" from a plain `kubectl get` without the ledger.

# Linkage and selector labels (weave)

| Key | Meaning |
|---|---|
| `fusion-platform.io/trigger`, `fusion-platform.io/chain` | on WeaveRuns created by a trigger - query with `-l fusion-platform.io/trigger=<name>` |
| `fusion-platform.io/batch-job-id` | BatchCron runs |
| `fusion-platform.io/chain` + `fusion-platform.io/step` | immutable Deployment selector of deploy steps (never the run name) |
| `fusion-platform.io/run` | weave's own run linkage (different concept from the wizard's run label) |

# Policy labels (weave)

| Key | On | Meaning |
|---|---|---|
| `fusion-platform.io/api-key=true` | Secret | weave API key; role in annotation `fusion-platform.io/role` |
| `fusion-platform.io/role` | ServiceAccount label | API role for SA TokenReview callers (`viewer` / `editor` / `admin`) |

# One-shot annotations (consumed by the reconciler)

| Key | On | Effect |
|---|---|---|
| `fusion-platform.io/fire` | WeaveTrigger (`true`), WeaveApp (`<entrypoint>`) | start a run / execution now |
| `fusion-platform.io/reset=true` | WeaveTrigger | clear quarantine after a panic |
| `fusion-platform.io/restart-step=<step>` | WeaveRun | rolling restart of a deployed step |
| `fusion-platform.io/reload-deploy-step=<step>@<version>` | WeaveChain | code-source rolling restart |

Use `kubectl annotate --overwrite` when re-applying.

# Finalizers

`weave.fusion-platform.io/deploy-cleanup` on WeaveRuns with deploy steps - removes Deployment, Service and Ingress on deletion or Stopped/Failed.[^flux]

# Value rules

Label values must be sanitized (`[A-Za-z0-9][-A-Za-z0-9_.]*`, max 63 chars); Job and Service names are capped at 63 bytes because Kubernetes derives labels from them.[^flux]

[^flux]: fusion-weave CLAUDE.md
[^forge]: fusion-forge CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
