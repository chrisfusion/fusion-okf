---
type: Custom Resource
title: GitWatcher
description: forge resource (build.fusion-platform.io/v1alpha1, short name gw) that polls a git repo and builds whenever the declared version changes.
resource: repo://fusion-forge/api/v1alpha1/gitwatcher_types.go
tags: [forge, crd, gitops]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: types, resource: repo://fusion-forge/api/v1alpha1/gitwatcher_types.go, title: gitwatcher_types.go }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# Schema

| Field | Meaning |
|---|---|
| `spec.repoURL`, `spec.repoRef` | repo and branch (default `main`) |
| `spec.buildType` | `git` (pyproject.toml) or `app` ([metadata.yaml](/contracts/metadata-yaml.md)) |
| `spec.enabled` | `false` pauses without deleting |
| `spec.metadataSource` | git builds only: `manual` (name+version from spec), `version` (version from pyproject), `full` (both from pyproject) |
| `spec.name`, `spec.version` | used by `manual` / `version` modes |
| `spec.pythonVersion` | builder image key (git builds) |
| `spec.projectDir`, `spec.entrypointFile`, `spec.description` | optional |
| `spec.autoTag` | index tag (e.g. `stable`) moved to every built version; empty = tags moved by hand |
| `spec.tokenSecretRef` | Secret for private repos, used by the watcher *and* the builder's clone |
| `status.phase` | `Active` / `Disabled` |
| `status.lastSeenCommit`, `lastBuiltVersion`, `lastBuildName`, `lastBuildVersion` | polling and in-flight state |
| `status.consecutiveFailures`, `lastError`, `artifactID`, `lastAutoTag` | failure counting and tag bookkeeping |

[^types]

# Behaviour

- Polls `ls-refs` HEAD every `WATCHER_POLL_INTERVAL` (default 60 s) plus a per-watcher jitter `fnv32a(name) % (interval/4)`.
- Builds are **version-change-driven**: a new commit with the same version only updates `lastSeenCommit`.
- After `WATCHER_MAX_FAILURES` (default 2) consecutive failures the watcher disables itself; re-enable via `spec.enabled`.
- `autoTag` follows the declared version, not the highest one.
- Created via forge REST `POST /api/v1/gitwatchers` (live repo reachability check) - by users or by [fusion-wizard](/services/fusion-wizard.md) (`autoPromote`). Labels `fusion-platform.io/managed-by` default to `manual`.[^forge]

# Pitfall: stale CRD

The CRD must be installed from forge's chart `crds/` (since 0.11.1) and kept current. A cluster that kept an old CRD silently pruned `spec.autoTag`, which broke the wizard's autoPromote.[^fleet]

[^forge]: fusion-forge CLAUDE.md
[^types]: gitwatcher_types.go
[^fleet]: fusion-fleet CLAUDE.md
