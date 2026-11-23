---
type: Service
title: fusion-forge
description: Async builder of Python venvs and apps via Kubernetes Jobs, with a GitOps watcher that rebuilds when a repo's declared version changes.
resource: repo://fusion-forge
tags: [forge, build, operator]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# Purpose

Builds Python virtual environments (from `requirements.txt`), library wheels (from a git repo with `pyproject.toml`) and apps (from a git repo with [`metadata.yaml`](/contracts/metadata-yaml.md)) asynchronously, and publishes the results to [fusion-index](/services/fusion-index.md).[^forge]

# Binaries (one image)

| Binary | Role |
|---|---|
| `/server` | REST API (Gin), PostgreSQL `venv_build` table, runs migrations at start |
| `/operator` | Reconciles [CIBuild](/contracts/crds/cibuild.md) → ConfigMap + Job; no DB access |
| `/watcher` | Reconciles [GitWatcher](/contracts/crds/gitwatcher.md): polls HEAD, triggers builds, moves `autoTag` |
| builder (`fusion-venv-builder` image) | Runs inside the Job: clone, validate, build, upload to index |

# Build types

| Type | Input | API | CIBuild prefix | Index artifact |
|---|---|---|---|---|
| requirements | `requirements.txt` upload (multipart) | `POST /api/v1/venvs` | `forge-venv-<id>` | `venv.<name>` |
| git | repo + `pyproject.toml` (JSON) | `POST /api/v1/gitbuilds` | `forge-git-<id>` | `venv.<name>` |
| app | repo + `metadata.yaml` | `POST /api/v1/appbuilds` | `forge-app-<id>` | `app.<name>` |

See [build type](/glossary/build-type.md) and [artifact naming](/contracts/artifact-naming.md).[^forge]

# Interfaces

- **Provides:** REST under `/api/v1/` (venvs, gitbuilds, appbuilds, gitwatchers, builds bulk/cleanup endpoints); health at `/q/health/live` and `/q/health/ready`.
- **Consumes:** fusion-index REST (find/create artifact, create/delete version, upload, set tag); git remotes (go-git in-memory clones, `ls-refs`).
- **Callers:** [fusion-bff](/services/fusion-bff.md) (path `/api/forge/*`), [fusion-wizard](/services/fusion-wizard.md) (GitWatcher create with labels).
- **Auth:** optional Kubernetes SA TokenReview (`AUTH_ENABLED`, `AUTH_AUDIENCE`, `AUTH_ALLOWED_SA`).[^forge]

# State

- PostgreSQL `fusion_forge` - bundled StatefulSet in its own chart (`postgresql.enabled`, default true), or external with a create-database hook Job.[^fleet]
- The DB row is lazily synced from the CIBuild phase on `GET`; a CR deleted outside the API leaves rows stuck - remedy `POST /api/v1/builds/zombie-cleanup`.

# Deployment

Helm chart `deployment/` (release `fusion-forge`, namespace `fusion`), Flux in [fleet](/services/fusion-fleet.md). The chart ships both CRDs in `crds/`, which Helm never upgrades - apply CRD changes server-side before `helm upgrade`; Flux uses `crds: CreateReplace`.[^forge]

# Cross-repo notes

- Builder images are selected by key (`3.12` / `python3.12`, `3.10` / `python3.10`) from the `fusion-forge-builder-images` ConfigMap; `metadata.yaml` `builderImage` must match a key exactly.
- `builder/main.go` is built in a throw-away module and cannot import `internal/` - duplicated helpers are intentional.
- The builder functions are misnamed: `buildFromGit` is the pyproject path, `buildFromApp` the metadata.yaml path (rename planned; `BUILD_TYPE` values `git`/`app` must stay).
- Large uploads through Linkerd need `linkerd.opaquePorts: "8080"` on fusion-index; `linkerd.builderInject: disabled` only fixes Job completion.[^forge]
- Canonical app example: `fusion-testcases/simple_streamlit_template/`.

# Where to look

Repo-internal details (commands, layer checklists, logging rules, gotchas): `repo://fusion-forge/CLAUDE.md`; docs `README.md`, `ARCHITECTURE.md`, `EXAMPLES.md`, `FLUX.md`.

[^forge]: fusion-forge CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
