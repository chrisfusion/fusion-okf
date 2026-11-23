---
type: Contract
title: metadata.yaml
description: App manifest at the root of an app repo - parsed by forge at build time, stored in index, read by weave at deploy time and consumed by the runner via WEAVE_* env vars.
resource: repo://fusion-testcases/simple_streamlit_template/metadata.yaml
tags: [forge, index, weave, runner, wizard, contract]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: forge-meta, resource: repo://fusion-forge/internal/gitutil/metadata.go, title: forge metadata.go parser }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
  - { id: sample, resource: repo://fusion-testcases/simple_streamlit_template/metadata.yaml, title: canonical sample }
---

# Example

```yaml
name: test-template            # -> index artifact app.test-template
version: 0.1.0                 # semver; a change triggers a build
maintainer: some.maintainer@example.local
builderImage: python3.12       # key in forge's builder-images ConfigMap
runner:
  type: streamlit              # -> WEAVE_RUNNER_TYPE
  port: 8501                   # -> WEAVE_PORT and container port
  args:
    ENTRYPOINT: "main.py"      # map style, each key becomes an env var
ingress:
  path: testproject            # URL path segment, not a hostname
resources:
  requests: { cpu: "200m", memory: "500Mi" }
  limits:   { cpu: "500m", memory: "1Gi" }
```

[^sample]

# Schema

| Field | Type | Required | Consumed by |
|---|---|---|---|
| `name` | string | yes (422 if missing) | forge → artifact `app.<name>`[^forge] |
| `version` | semver string | yes | forge (build trigger, index version), GitWatcher change detection |
| `builderImage` | string | yes | forge; must match a builder-images key exactly (`3.12`, `python3.12`, ...)[^forge] |
| `basedependencies` | URL string | no | forge builder[^forge-meta] |
| `files` | list | no | forge builder - extra files to upload (path-validated) |
| `rootAssets` | bool | no | forge builder - bundle root-level non-`.py` files into `site-packages/_root_assets/` |
| `runner.type` | string | - | forge stores it in the DB; weave → `WEAVE_RUNNER_TYPE`; runner dispatch |
| `runner.port` | int | - | weave → `WEAVE_PORT` and, for override/app deployments, container port[^flux] |
| `runner.args` | map | - | weave → one env var per key (e.g. `ENTRYPOINT`) |
| `runner.builderImage` | string | - | weave → `WEAVE_BUILDER_IMAGE` |
| `ingress.path` | string | - | weave → Ingress path and `WEAVE_INGRESS_PATH`; empty or `/` = root |
| `resources.requests/limits` | k8s quantities | - | weave (override/app deployments) |
| `maintainer` | string | - | weave → `WEAVE_MAINTAINER` |

forge parses `runner` as an opaque value and passes everything beyond the typed fields through to index as raw YAML - don't add typed fields there.[^forge]

# Who reads it when

1. **Build time** - forge watcher / app build handler reads it from the repo (in-memory clone) for name, version, builder image; the builder uploads it as one of the three app files.
2. **Deploy time** - weave's `indexclient.FetchAppMetadataAndVersion` downloads it from index (cached 30 s) and maps it to [`WEAVE_*` env vars](/contracts/weave-env-vars.md), ports and resources.[^flux]
3. **Run time** - [fusion-runner](/services/fusion-runner.md) reads only the env vars, never the file.[^runner]

# Rules

- Per-run overrides cannot change metadata-sourced values; point a run at a different tag/version instead.
- `ingress.path` alone does not make an app serve under that prefix: each runner type must apply `WEAVE_INGRESS_PATH` (Streamlit does).
- `runner.args` keys colliding with template env vars produce duplicates; runner.args effectively wins.
- Renamed keys have no back-compat aliases (`pathPrefix` → `path`); republish artifacts.

# Change checklist

Renaming or removing a field touches independent copies - grep all of them:

- forge `internal/gitutil/metadata.go` (parse/validate) and the app-build layers,
- weave `internal/indexclient` and the deploybuilder,
- `fusion-runner` (consumer of the resulting env vars),
- `fusion-testcases` (sample metadata.yaml files and docs).[^flux]

[^forge]: fusion-forge CLAUDE.md
[^forge-meta]: forge metadata.go parser
[^flux]: fusion-weave CLAUDE.md
[^runner]: fusion-runner CLAUDE.md
[^sample]: canonical sample
