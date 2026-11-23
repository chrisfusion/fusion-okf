---
okf_version: "0.2"
---

# fusion-platform knowledge bundle

## Subdirectories

* [apis](apis/index.md) - One page per service API - base path, auth, route groups and gotchas, linking to the OpenAPI file or router instead of copying it.
* [contracts](contracts/index.md) - Shapes shared between services - manifests, naming, env vars, headers, labels.
* [conventions](conventions/index.md) - Rules every repo follows - offline builds, logging, changelog and releases, Helm and CRDs, operators, health endpoints.
* [decisions](decisions/index.md) - Architecture decisions the sources state explicitly, with status (accepted or proposed), context and consequences.
* [glossary](glossary/index.md) - Platform terms, one page per term.
* [issues](issues/index.md) - Verified bugs, inconsistencies and stale documentation across repos, each with cause, impact and fix.
* [operations](operations/index.md) - Running the platform locally - minikube, per-service deploys, Postgres, DNS, Gitea and Flux.
* [platform](platform/index.md) - What the platform is, how the services fit together and the end-to-end artifact flow.
* [services](services/index.md) - One page per fusion-* repository - purpose, interfaces, dependencies, deployment.
