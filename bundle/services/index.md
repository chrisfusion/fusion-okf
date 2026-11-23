# Services

## Concepts

* [fusion-bff](fusion-bff.md) - Backend for the web GUI - OIDC login with sessions, allowlist, RBAC per route, and a proxy to forge, index, weave, wizard and content.
* [fusion-content](fusion-content.md) - In-memory content API that polls git repos and serves service changelogs, Diataxis help articles and video metadata.
* [fusion-ext-system-bff](fusion-ext-system-bff.md) - Machine-to-machine gateway for CI/CD and third-party systems - oauth2 or API-key auth, RBAC, proxy to fusion-index and a public download endpoint.
* [fusion-fleet](fusion-fleet.md) - Flux GitOps fleet repo with GitRepository, HelmRelease and Kustomization manifests for every fusion service across all clusters.
* [fusion-forge](fusion-forge.md) - Async builder of Python venvs and apps via Kubernetes Jobs, with a GitOps watcher that rebuilds when a repo's declared version changes.
* [fusion-index](fusion-index.md) - Artifact registry storing namespaced, semver-versioned artifacts with files, configs, mutable tags, types and retention policies.
* [fusion-runner](fusion-runner.md) - Dependency-free Go entrypoint of all runner container images; dispatches on WEAVE_RUNNER_TYPE, unpacks the venvpack and execs the app.
* [fusion-shared](fusion-shared.md) - Public repo with cross-project documents (multi-tenancy plan, logging principles) and planned shared Go libraries such as ownership.
* [fusion-spectra](fusion-spectra.md) - Vue 3 + Quasar web GUI (Module Federation host) with Simple and Expert mode; talks only to fusion-bff.
* [fusion-weave](fusion-weave.md) - Kubernetes operator that runs job DAGs, triggered runs, deploy steps and WeaveApps, plus a REST and monitoring API; repo directory is fusion-flux.
* [fusion-wizard](fusion-wizard.md) - Operator plus REST API that provisions resources across forge, index and weave from declarative wizard definitions, with a ref-counted ledger and rollback.
