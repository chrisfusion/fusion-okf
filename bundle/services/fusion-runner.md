---
type: Service
title: fusion-runner
description: Dependency-free Go entrypoint of all runner container images; dispatches on WEAVE_RUNNER_TYPE, unpacks the venvpack and execs the app.
resource: repo://fusion-runner
tags: [runner, weave, images]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

# Purpose

The consumer end of the [artifact lifecycle](/platform/artifact-lifecycle.md): forge builds venvpacks → index stores them → weave injects [`WEAVE_*`](/contracts/weave-env-vars.md) env vars and optionally pre-downloads files → the runner starts the app.[^runner]

# Runner types (`internal/runner/`)

| Type | Behaviour |
|---|---|
| `PythonRunner` | extracts the venvpack, fixes absolute `bin/python3.X` symlinks, `syscall.Exec`s the entrypoint (`ENTRYPOINT` from `runner.args`) |
| `StreamlitRunner` | embeds PythonRunner; sets Streamlit env, incl. `STREAMLIT_SERVER_BASE_URL_PATH` from `WEAVE_INGRESS_PATH` |
| `IndexPythonRunner` | embeds PythonRunner; resolves `WEAVE_ARTIFACT`/`WEAVE_TAG` via index REST (`INDEX_URL`) and downloads the files itself |

New type: add `<type>.go` implementing `Runner` and a case in `New()`.[^runner]

# Images

`dockerfiles/<type>/Dockerfile` (e.g. `fusion-runner-python312:local`). The module has no dependencies - the Dockerfile builds with `GOPROXY=off`. `prepare_Dockerfile.sh` injects a corporate-CA "certify" stage.[^runner]

# Venvpack quirks

- forge archives have a top-level `venv/` prefix - detected from the first tar entry, not from `TypeDir`.
- Under `readOnlyRootFilesystem` the runner runs as UID 1000, `HOME=/home/runner`, and unpacks to `/tmp/venv`, so Python/Streamlit only need `/tmp` writable.[^flux]

# Helpers

`helpers/python/` (`fusion_runner_helpers`) - libraries for code *inside* step pods, e.g. `KeycloakAuth` for OAuth2 client credentials from a Secret injected via weave's `authSecretRef`. Opt-in per artifact via `requirements.txt`.[^runner]

[^runner]: fusion-runner CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
