---
type: Platform Overview
title: Artifact lifecycle
description: End-to-end path of an app from a git push through forge build, index storage and tag move to a running weave workload.
tags: [platform, forge, index, weave, runner, wizard, flow]
status: stable
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
verified: { by: human:chrisfusion, at: 2026-11-23T12:47:41Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

# The path in one picture

```
git repo (metadata.yaml / pyproject.toml)
   │  push (version bump)
   ▼
forge watcher ── polls HEAD (GitWatcher) ──► forge trigger ──► CIBuild CR
                                                                │ forge operator
                                                                ▼
                                                     builder Job (fusion-venv-builder)
                                                                │ upload venvpack + files
                                                                ▼
                                index: artifact app.<name>, version x.y.z, tag "stable"
                                                                │ tag poll (CODE_SOURCE_POLL_INTERVAL)
                                                                ▼
                         weave: WeaveApp / deploy step with codeSource ──► rolling restart
                                                                │ code-loader init container
                                                                ▼
                                       runner image: fusion-runner unpacks venv, starts app
```

# Step by step

1. **Repository.** An app repo carries a [`metadata.yaml`](/contracts/metadata-yaml.md) (app build) or a `pyproject.toml` (git/library build). The declared `version` drives everything: builds are *version-change-driven*, not commit-driven.[^forge]
2. **Detect.** A [GitWatcher](/contracts/crds/gitwatcher.md) polls the remote HEAD cheaply (`ls-refs`, no clone) every `WATCHER_POLL_INTERVAL` (jittered). On a new commit it reads the version; if it differs from `lastBuiltVersion` it triggers a build.[^forge]
3. **Register.** forge finds or creates the index artifact ([naming](/contracts/artifact-naming.md): `app.<name>` / `venv.<name>`), creates the version and writes a `venv_build` DB row, then creates a [CIBuild](/contracts/crds/cibuild.md) named `forge-app-<id>` / `forge-git-<id>` / `forge-venv-<id>`.[^forge]
4. **Build.** The forge operator turns the CIBuild into a ConfigMap + Job. The builder installs dependencies into a venv, packs it (venvpack, top-level `venv/` prefix) and uploads it to index; app builds upload three files: the `.tar.gz`, `main.py` and `metadata.yaml`.[^forge]
5. **Tag.** With `autoTag` set (wizard sets it via `autoPromote`), the watcher moves the index tag (e.g. `stable`) to every newly built version. Tags follow the *declared* version: reverting the version moves the tag back.[^forge]
6. **Store.** index stores files under `{artifactID}/{major}/{minor}/{patch}/{fileID}/{filename}` (filesystem or S3) with a two-phase upload (PENDING → AVAILABLE).[^index]
7. **Roll out.** A [WeaveApp](/contracts/crds/weaveapp.md) or a deploy step with `codeSource` resolves `artifactName@tag` → version. The chain/app controller polls the tag every `CODE_SOURCE_POLL_INTERVAL` (default 60 s); a moved tag updates `WEAVE_VERSION` in the pod template, which itself is the rolling restart.[^flux]
8. **Load.** The `code-loader` init container (`/loader` in the weave image) downloads every file of the resolved version into `/weave-code` and writes `.version`. Files are copied as-is, not extracted.[^flux]
9. **Run.** The runner image's entrypoint ([fusion-runner](/services/fusion-runner.md)) dispatches on `WEAVE_RUNNER_TYPE`, extracts the venvpack, rewrites the absolute `bin/python3.X` symlinks to the container interpreter and `exec`s the app. Configuration arrives as [`WEAVE_*` env vars](/contracts/weave-env-vars.md).[^runner]

# The wizard shortcut

[fusion-wizard](/services/fusion-wizard.md) performs steps 2-7 for a user in one [WizardRun](/contracts/crds/wizardrun.md): `gitWatcher` → `waitBuild` → `tag` → `app` (or template/chain/trigger for batch jobs). Every resource it touches is recorded in the [ledger](/glossary/ledger.md), so a rollback removes exactly what the run created.[^wizard]

# Failure behaviour

- A failed build: the watcher deletes the version from index and the DB row (best-effort), counts `consecutiveFailures` and disables itself after `WATCHER_MAX_FAILURES` (default 2).[^forge]
- Re-triggering the same version needs the old index version gone, otherwise forge answers 409 (treated as "skipped").[^forge]
- A deleted index artifact (e.g. by a wizard rollback) is rebuilt by the watcher on the next HEAD change; dormant repos need `POST /api/v1/builds/index-drift-cleanup`.[^wizard]

[^forge]: fusion-forge CLAUDE.md
[^index]: fusion-index CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^runner]: fusion-runner CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
