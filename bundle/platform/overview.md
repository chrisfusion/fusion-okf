---
type: Platform Overview
title: fusion-platform overview
description: Kubernetes-native platform that builds Python apps and venvs from git, stores them as versioned artifacts and runs them as jobs, DAGs or services.
tags: [platform, architecture]
status: stable
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
verified: { by: human:chrisfusion, at: 2026-11-23T12:47:41Z }
sources:
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# What it does

fusion-platform turns a git repository into a running workload on Kubernetes:

1. **Build** - [fusion-forge](/services/fusion-forge.md) builds a Python venv or app from a requirements file, a `pyproject.toml` or a [`metadata.yaml`](/contracts/metadata-yaml.md) repo, inside a Kubernetes Job.[^forge]
2. **Store** - the result lands in [fusion-index](/services/fusion-index.md), the artifact registry, as a semver version with files and movable tags.
3. **Run** - [fusion-weave](/services/fusion-weave.md) runs it as a one-off job, a scheduled/triggered DAG or a long-running service, pulling the code from the index at pod start.[^flux]
4. **Execute** - inside the pod, [fusion-runner](/services/fusion-runner.md) unpacks the venv and starts the app (plain Python, Streamlit, ...).[^runner]

[fusion-wizard](/services/fusion-wizard.md) orchestrates steps 1-3 as one transactional "wizard run" with rollback.[^wizard] The full chain is described in [Artifact lifecycle](/platform/artifact-lifecycle.md).

# Components

| Layer | Service | Role |
|---|---|---|
| UI | [fusion-spectra](/services/fusion-spectra.md) | Vue 3 / Quasar web GUI (Simple and Expert mode) |
| Edge | [fusion-bff](/services/fusion-bff.md) | OIDC login, sessions, RBAC, proxy for humans[^bff] |
| Edge | [fusion-ext-system-bff](/services/fusion-ext-system-bff.md) | OAuth2 / API-key proxy for machines; public artifact downloads |
| Orchestration | [fusion-wizard](/services/fusion-wizard.md) | Multi-service provisioning with a ref-counted ledger |
| Build | [fusion-forge](/services/fusion-forge.md) | Async venv/app builds, GitOps watcher |
| Storage | [fusion-index](/services/fusion-index.md) | Artifact registry (PostgreSQL + filesystem/S3) |
| Execution | [fusion-weave](/services/fusion-weave.md) | Job-DAG operator, WeaveApp services/jobs, REST + monitoring API |
| Execution | [fusion-runner](/services/fusion-runner.md) | Entrypoint binary of all runner images |
| Content | [fusion-content](/services/fusion-content.md) | Changelogs, help articles and videos from git |
| Delivery | [fusion-fleet](/services/fusion-fleet.md) | Flux GitOps fleet for all clusters |
| Shared | [fusion-shared](/services/fusion-shared.md) | Cross-project docs and Go libraries |

# Request paths

```
Browser ──► spectra ──► fusion-bff ─────────┬──► forge ──► index
                         (OIDC, RBAC)       ├──► index
Machines ─► fusion-ext-system-bff ──────────┤──► weave ──► index, runner pods
                         (oauth2/apikey)    ├──► wizard ──► forge, index, weave
                                            └──► content ──► git repos
Pod ──► Bearer <K8s SA token> ──► forge / index / weave / wizard  (TokenReview, no BFF)
```

Humans never call backend services directly: the BFF validates the OIDC session, checks the route permission, then calls the upstream with its own service-account token and forwards the identity as [trusted headers](/contracts/trusted-headers.md).[^bff]

# Technology baseline

- Backends: Go 1.25 (weave: Go 1.27), Gin (weave/wizard: chi), pgx/v5, controller-runtime v0.19 for operators.
- All Go repos vendor their dependencies: CI builds images without internet access (`docker build --network none`).
- Images are distroless; charts live in each repo's `deployment/` and are deployed by [Flux](/services/fusion-fleet.md).[^fleet]
- License: GPL-3.0 everywhere.

# Kubernetes API groups

| Group | Owner | Kinds |
|---|---|---|
| `build.fusion-platform.io` | forge | [CIBuild](/contracts/crds/cibuild.md), [GitWatcher](/contracts/crds/gitwatcher.md) |
| `weave.fusion-platform.io` | weave | [WeaveJobTemplate](/contracts/crds/weavejobtemplate.md), [WeaveServiceTemplate](/contracts/crds/weaveservicetemplate.md), [WeaveChain](/contracts/crds/weavechain.md), [WeaveTrigger](/contracts/crds/weavetrigger.md), [WeaveRun](/contracts/crds/weaverun.md), [WeaveApp](/contracts/crds/weaveapp.md) |
| `wizard.fusion-platform.io` | wizard | [WizardDefinition](/contracts/crds/wizarddefinition.md), [WizardRun](/contracts/crds/wizardrun.md), [WizardResource](/contracts/crds/wizardresource.md) |

Label and annotation keys use the shared prefix `fusion-platform.io/` - see [Labels and annotations](/contracts/labels-and-annotations.md).

[^bff]: fusion-bff CLAUDE.md
[^forge]: fusion-forge CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
[^runner]: fusion-runner CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
