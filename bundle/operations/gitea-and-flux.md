---
type: Playbook
title: Gitea mirror and Flux instances
description: Flux on minikube watches Gitea mirrors of every repo (not the real origin); git push gitea main deploys to fusion-dev-a/b, with chart-version bumps and CRD ownership as the main traps.
tags: [operations, fleet, flux, gitea, deployment]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

# Gitea

- Namespace `gitea`, `http://gitea.fusion.local/gitea_admin/<project>.git` (public mirrors, no credentials Secret needed).[^fleet]
- Ingress annotation `proxy-body-size: 512m` (in the Helm values). Without it, larger pushes fail.
- Create repos and tokens via the REST API. Never put credentials in a remote URL; use a credential helper.

# Remotes

Each repo has `origin` (GitHub/work: confirm every push) and `gitea` (the Flux source).[^fleet] They drift apart. Before pushing to gitea, run `git fetch gitea && git rev-list --count gitea/main..HEAD`: a push deploys the whole backlog.[^flux] The rules in the CLAUDE.md files contradict each other: see [known issue](/issues/push-rule-conflict.md).

# Fleet layout (dev-cluster)

- `gitrepositories/<project>-<ref>.yaml`, shared by instances on the same ref.
- `projects/fusion/base/`: one HelmRelease per service (spectra, bff, forge, index, content, weave). Instances under `projects/fusion/<channel>/<instance>/` with channels `dev` (branch), `staging` (rc tag), `stable` (release tag), `personal` (dev branch).[^fleet]
- The root `kustomization.yaml` lists **only** each instance's `flux-kustomization.yaml`, never directories. Anything else causes field-manager conflicts.
- Resource order inside an instance: namespace → secrets → serviceaccounts → ingress → services → postgres → `../../base` → jobs.
- `cluster1/`, `cluster2/` (production) are skeletons with a single `stable` channel.

# Traps

- `reconcileStrategy: ChartVersion`: a content-only chart push does **not** redeploy. Bump `Chart.yaml` `version`. As a last resort, delete and recreate the `HelmChart` object.[^fleet]
- Charts must use `{{ .Release.Namespace }}` and a sanitized `helm.sh/chart` label (Flux appends `+N` to versions), and must not create the namespace themselves. A hard-coded namespace once broke the live `fusion` deploy twice.[^fleet]
- `valuesFiles` paths are relative to the GitRepository root (`deployment/values.yaml`). Gitignored files (content's `values-local.yaml`) never reach Flux.
- CRDs use `crds: CreateReplace`. An instance pinned to an older ref needs `crds: Skip`, or it rolls the CRDs back. `scripts/apply-crds.sh` applies them all from the sibling clones. See [Helm and CRDs](/conventions/helm-and-crds.md).
- Monitoring: per-instance `ServiceMonitor`s live in `instance_*/monitoring/` with their own Kustomization, which `dependsOn` the shared stack. Index's `/q/metrics` cannot be scraped ([issue](/issues/index-metrics-not-prometheus.md)).

[^fleet]: fusion-fleet CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
