---
type: Playbook
title: Deploy matrix for the fusion namespace
description: How each service is actually deployed into the hand-managed fusion namespace - which ones use Helm, which raw YAML or kubectl set image, and the traps for each.
tags: [operations, minikube, forge, index, weave, bff, ext-bff, spectra, wizard, content]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
  - { id: content, resource: repo://fusion-content/CLAUDE.md, title: fusion-content CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

The `fusion` namespace is not Flux-managed, and direct deploys there are fine.[^wizard] The repos' own CLAUDE.md files sometimes describe the *intended* method. This table shows what the live namespace needs, where the sources say so.

| Service | Method in `fusion` | Image tag | Trap |
|---|---|---|---|
| [forge](/services/fusion-forge.md) | `docker build -t fusion-forge:local` → `docker save` → `minikube image load <tar>` → `rollout restart` server/operator/watcher | `:local` (IfNotPresent) | Helm release `failed` since 2026-09-22 (StatefulSet immutable). forge's own CLAUDE.md still names `helm upgrade` as the primary method.[^wizard][^forge] Apply CRDs by hand. |
| [index](/services/fusion-index.md) | `helm upgrade --install fusion-index deployment/ -n fusion -f deployment/values-dev.yaml --wait` | `fusion-index:latest` in the doc | Structural chart changes: disposable namespace first.[^index] |
| [weave](/services/fusion-weave.md) | **raw YAML** (`make minikube-deploy`, `config/manager/`), image build + `rollout restart` of operator and api | fixed version tag; check the live deployment | The Helm release named `fusion-weave` (in `default`) is orphaned. Live env has drifted from `manager.yaml` in both directions, so change single vars with `kubectl set env`.[^flux] |
| [wizard](/services/fusion-wizard.md) | `helm upgrade fusion-wizard deployment/fusion-wizard -n fusion --reuse-values --set image.tag=X.Y.Z` | fresh semver per build | Enable a definition with `--set definitions.<x>.enabled=true`.[^wizard][^spectra] |
| [bff](/services/fusion-bff.md) | build `fusion-bff:X.Y.Z`, then `kubectl set image` + manual patch of the rbac ConfigMap | semver | `helm upgrade` fails locally: "config.oidcIssuerUrl is required".[^spectra][^bff] |
| [spectra](/services/fusion-spectra.md) | build `fusion-spectra:X.Y.Z`, then `kubectl set image deployment/fusion-spectra frontend=...` | semver | `helm upgrade` hits a field-manager conflict with `kubectl-set`. It still applies the ConfigMap first; the release stays `failed`, which is harmless.[^spectra] |
| [content](/services/fusion-content.md) | `make docker-build && helm upgrade --install fusion-content deployment/ -n fusion -f deployment/values-local.yaml` | semver | `values-local.yaml` is gitignored (holds tokens), so Flux cannot use it.[^content][^fleet] |
| [ext-bff](/services/fusion-ext-system-bff.md) | Helm chart in `deployment/` | semver | Not in the fleet; see [issue](/issues/ext-bff-flux-dir-missing.md). |

# Flux instances (fusion-dev-a/b)

Deploy by pushing to the `gitea` remote. Flux deploys spectra, bff, forge, index, content and weave there. **ext-bff and wizard have no HelmRelease in the fleet.**[^fleet] Chart changes need a `Chart.yaml` `version` bump to be repackaged. See [Gitea and Flux](/operations/gitea-and-flux.md).

[^forge]: fusion-forge CLAUDE.md
[^index]: fusion-index CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^bff]: fusion-bff CLAUDE.md
[^spectra]: fusion-spectra CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
[^content]: fusion-content CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
