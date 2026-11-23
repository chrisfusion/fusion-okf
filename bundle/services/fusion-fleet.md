---
type: Service
title: fusion-fleet
description: Flux GitOps fleet repo with GitRepository, HelmRelease and Kustomization manifests for every fusion service across all clusters.
resource: repo://fusion-fleet
tags: [fleet, flux, gitops, deployment]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# Purpose

Declares which version of which service runs where. Charts are not pulled from a registry - they live in each service repo (`deployment/`) and are sourced via `GitRepository` objects.[^fleet]

# Layout

- `dev-cluster/` - minikube, the Flux bootstrap path. `cluster1/`, `cluster2/` - production skeletons with only the `stable` channel.
- `gitrepositories/<project>-<ref>.yaml` - one source per repo + ref in use, shared by instances on that ref.
- `projects/fusion/base/` - one canonical `HelmRelease` per microservice (spectra, bff, forge, index, content, weave). Umbrella project, not one folder per repo.
- `projects/fusion/<channel>/<instance>/` - one namespaced instance; channel `dev` (branch), `staging` (RC tag), `stable` (release tag), `personal` (developer branch). Patches contain only values that differ from base.
- `projects/monitoring/dev/shared/` - kube-prometheus-stack plus fusion-grafana dashboards, one per cluster.[^fleet]

# Rules that affect service charts

- Charts must use `{{ .Release.Namespace }}` everywhere - a hard-coded namespace once broke the live spectra deployment.
- `helm.sh/chart` labels must not use the raw `.Chart.Version` (Flux appends `+N`, which is invalid in a label).
- Chart namespace-creation toggles must be off; the instance's `namespace.yaml` owns the Namespace.
- CRDs (forge, weave, wizard only) use `install/upgrade.crds: CreateReplace`; instances pinned to an older ref get `crds: Skip`.
- Bump `Chart.yaml` `version` to make Flux repackage a chart.
- `valuesFiles` paths are relative to the GitRepository root and must be committed (not gitignored).[^fleet]

# Instances and sources

- Flux watches the in-cluster Gitea mirrors (`http://gitea.fusion.local/gitea_admin/<project>.git`); pushing to the `gitea` remote deploys.
- Namespaces: `fusion-dev-a` / `fusion-dev-b` (Flux), `fusion` (manual, not Flux-managed).
- Per-instance ingress hosts follow `<service>-<instance>.fusion.local`; spectra needs three matching bff overrides (`oidcBypassBaseUrl`, `corsOrigins`, `postLoginRedirectUrl`).[^fleet]

[^fleet]: fusion-fleet CLAUDE.md
