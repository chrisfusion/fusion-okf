---
type: Custom Resource
title: CIBuild
description: forge's build request (build.fusion-platform.io/v1alpha1) that the forge operator turns into a ConfigMap plus builder Job.
resource: repo://fusion-forge/api/v1alpha1/cibuild_types.go
tags: [forge, crd, build]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: types, resource: repo://fusion-forge/api/v1alpha1/cibuild_types.go, title: cibuild_types.go }
---

# Identity

- Group/version: `build.fusion-platform.io/v1alpha1`, kind `CIBuild`, namespaced (`fusion`).
- Names: `forge-venv-<id>` (requirements), `forge-git-<id>` (git), `forge-app-<id>` (app), `<id>` = forge DB row id. Prefixes must stay distinct.[^forge]

# Schema

| Field | Meaning |
|---|---|
| `spec.builderImage` | builder image resolved from the builder-images ConfigMap |
| `spec.indexBackendURL` | fusion-index base URL for the upload |
| `spec.artifactName`, `spec.artifactVersion` | display name and semver |
| `spec.configData` | files mounted at `/workspace/<filename>` (e.g. `requirements.txt`); empty for git/app builds |
| `spec.env` | e.g. `ARTIFACT_ID` (numeric index id), `ARTIFACT_VERSION`, `VENV_NAME` |
| `spec.buildType` | `git` or `app` (empty for requirements builds); passed to the builder as `BUILD_TYPE` |
| `spec.gitSource` | `url`, `ref`, `projectDir`, `entrypointFile`, `tokenSecretRef` |
| `spec.appSource` | as gitSource plus the metadata.yaml-derived `files`, `fileUploadMode`, `baseDependencies`, `rootAssets` |
| `status.phase` | `Pending` → `Building` → `Succeeded` / `Failed` |
| `status.jobName`, `status.configMapName` | owned objects (ConfigMap name cleared after a terminal phase) |
| `status.message`, `startedAt`, `completedAt` | diagnostics |

[^types]

# Lifecycle

1. Created by forge's `buildtrigger` package (REST handlers and the watcher share it).
2. Operator: new CR → ConfigMap + Job, phase `Building`; Job done → delete ConfigMap, phase `Succeeded` or `Failed`.
3. Job and ConfigMap are owned by the CR and garbage-collected with it. The operator never touches the DB.[^forge]

# Readers

- forge server (lazy sync of the `venv_build` row on `GET`),
- [GitWatcher](/contracts/crds/gitwatcher.md) reconciler (in-flight build check via `status.lastBuildName`).

A CIBuild deleted outside the API leaves the DB row stuck in PENDING/BUILDING - see forge's `zombie-cleanup` endpoint.[^forge]

[^forge]: fusion-forge CLAUDE.md
[^types]: cibuild_types.go
