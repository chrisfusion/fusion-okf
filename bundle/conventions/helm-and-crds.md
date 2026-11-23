---
type: Convention
title: Helm charts and CRDs
description: Every service ships its own chart in deployment/; CRDs are generated into config/crd/bases and copied into the chart's crds/, which plain Helm installs but never upgrades.
tags: [forge, weave, wizard, bff, ext-bff, index, fleet, helm, crd]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# Charts

- Each repo's chart lives in `deployment/` (weave: `deployment/fusion-weave/`, wizard: `deployment/fusion-wizard/`). Charts are not published to a registry: [fusion-fleet](/services/fusion-fleet.md) pulls them from git.[^fleet]
- Secrets belong in Secret templates, never in the ConfigMap (bff removed `config.dbDsn` for this reason).[^bff]
- Pod templates carry `checksum/config` and `checksum/secrets` annotations so that config changes restart the pods. Env vars are read only at startup.[^index]
- Database bootstrapping uses `pre-install,pre-upgrade` hook Jobs, ordered by weight (bff: create-database, then RBAC seed). `helm template` does not test the embedded scripts, so render them and run them yourself.[^bff]
- Files the chart reads via `.Files.Get` must live inside the chart. bff and ext-bff keep **two** `rbac.yaml` copies (repo root and `deployment/`) that must stay in sync.[^bff]
- wizard: guard every map level in templates, e.g. `((.Values.definitions | default dict).x | default dict).enabled`, so that `--reuse-values` against an older release does not fail.[^wizard]

# CRDs

| Step | forge | wizard | weave |
|---|---|---|---|
| Generate | `make generate` → `config/crd/bases/` | same | same |
| Copy into chart | `make sync-crds` | `make sync-crds` | manual `cp config/crd/bases/*.yaml deployment/fusion-weave/crds/` |
| Check copy | `make check-crds` | `make check-crds` | none |

Sources: [^forge][^wizard][^flux]

- Plain `helm upgrade` never touches `crds/`. Apply CRD changes first with `kubectl apply --server-side -f config/crd/bases/`.[^forge]
- The fleet HelmReleases set `crds: CreateReplace`, so Flux does update CRDs.[^forge]
- Why this matters: a CRD missing from forge's chart left a Flux cluster on an old GitWatcher schema, and the API server silently pruned `spec.autoTag`.[^forge]
- CRDs are cluster-wide. When several namespaces run different versions, `kubectl diff` before applying.[^wizard]

All eleven CRDs are listed under [custom resources](/contracts/crds/index.md).

[^forge]: fusion-forge CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^bff]: fusion-bff CLAUDE.md
[^index]: fusion-index CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
