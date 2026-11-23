---
type: Playbook
title: Local minikube cluster
description: The dev cluster is one minikube with ingress-nginx, Keycloak, Gitea and Flux; images are built into minikube's Docker daemon with fresh semver tags.
tags: [operations, minikube, forge, index, weave, bff, spectra, wizard, content]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

# What runs where

| Namespace | Content | Managed by |
|---|---|---|
| `fusion` | the user's own dev/test instance (`spectra.fusion.local`) | by hand, see the [deploy matrix](/operations/deploy-matrix.md)[^wizard] |
| `fusion-dev-a`, `fusion-dev-b` | GitOps instances (`spectra-a`/`spectra-b.fusion.local`) | Flux, see [Gitea and Flux](/operations/gitea-and-flux.md)[^fleet] |
| `monitoring` | kube-prometheus-stack plus fusion-grafana dashboards (`grafana.fusion.local`) | Flux[^fleet] |
| `gitea` | Gitea mirror (`gitea.fusion.local`) | Helm[^fleet] |
| `default` | Keycloak StatefulSet (`keycloak.default.svc:8080`, realm `fusion`) | by hand[^flux] |
| `flux-system` | Flux controllers, fleet root `GitRepository`/`Kustomization` | flux bootstrap[^fleet] |

Never `helm upgrade` `fusion-dev-a`/`-b`: they are Flux-managed. Test chart structure changes in a disposable namespace, because `fusion` holds real data.[^wizard][^index]

# Building images

1. `eval $(minikube docker-env)` before `docker build`. Without it, pods fail with `ErrImageNeverPull`.[^spectra] The Makefiles of content and weave do this for you.
2. Use a **fresh semver tag** per build. Kubernetes ignores a rebuilt image under the same tag: use `kubectl rollout restart` while iterating, a new tag for real deploys.[^spectra][^wizard]
3. When building outside minikube's daemon: `minikube image load <name>:<tag>` can keep a stale image and still report success. Use `docker save -o x.tar` + `minikube image load x.tar` instead.[^flux]

# Cluster details

- Storage: `standard` (hostPath) survives restarts and `minikube stop/start` but not `minikube delete`. For RWX (weave shared storage) run `minikube addons enable csi-hostpath-driver` → `csi-hostpath-sc`.[^index][^flux]
- Ingress without DNS: `curl -sk --resolve <name>.fusion.local:443:$(minikube ip) https://<name>.fusion.local/`.[^flux] Normally [local DNS](/operations/local-dns.md) handles this.
- OIDC: tokens fetched through a `localhost` port-forward carry the wrong `iss`. Fetch them from inside the cluster.[^bff]
- Local port-forward ports clash, see [known issue](/issues/port-forward-clash.md).

[^spectra]: fusion-spectra CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
[^index]: fusion-index CLAUDE.md
[^bff]: fusion-bff CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
