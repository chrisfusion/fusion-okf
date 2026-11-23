---
type: Contract
title: WEAVE_* environment variables
description: Env vars that fusion-weave injects into codeSource containers from the resolved artifact and its metadata.yaml, and that fusion-runner consumes.
tags: [weave, runner, contract]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
---

# Variables

| Variable | Source | When |
|---|---|---|
| `WEAVE_ARTIFACT` | `codeSource.artifactName` | always with codeSource |
| `WEAVE_TAG` | `codeSource.tag` | always with codeSource |
| `WEAVE_VERSION` | tag resolved to a version | always with codeSource; updated on every rolling restart |
| `WEAVE_NAMESPACE` | pod namespace | always with codeSource |
| `WEAVE_MOUNT_PATH` | `codeSource.mountPath` (default `/weave-code`) | always with codeSource |
| `WEAVE_PORT` | `runner.port` | metadata available |
| `WEAVE_RUNNER_TYPE` | `runner.type` | metadata available |
| `WEAVE_BUILDER_IMAGE` | `runner.builderImage` | metadata available |
| `WEAVE_MAINTAINER` | `maintainer` | metadata available |
| `WEAVE_INGRESS_PATH` | `ingress.path` (normalized) | metadata available |
| every key of `runner.args` | e.g. `ENTRYPOINT` | metadata available |

[^flux]

Related, not `WEAVE_*`: `INDEX_URL` for the runner's own index access (`IndexPythonRunner`); job pods of BatchCron triggers also get `JOB_*` / `JOB_METADATA`.

# Rules

- Any rolling-restart path must update `WEAVE_VERSION` together with the restart (`deploybuilder.UpdateVersionEnvVar`); the changed env var *is* the restart for code-source services.[^flux]
- A runner `Config` field populated from a `WEAVE_*` var is useless until something reads it - `WEAVE_INGRESS_PATH` sat unused until Streamlit mapped it to `STREAMLIT_SERVER_BASE_URL_PATH`.[^runner]
- Renaming a variable needs a grep across fusion-flux, fusion-runner and fusion-testcases (independent copies). See [metadata.yaml](/contracts/metadata-yaml.md).
- fusion-runner's CLAUDE.md names `tmp_create_docker.md` as the full reference, but that file does not exist in the repo (checked 2026-11-17) - this page is the current reference.[^runner]

[^flux]: fusion-weave CLAUDE.md
[^runner]: fusion-runner CLAUDE.md
