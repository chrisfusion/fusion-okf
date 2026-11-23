# Bundle history

## 2026-11-17

* **Initialization**: Phase 1 generated from the CLAUDE.md files of 11 fusion-* repositories plus the CRD Go types - [platform](/platform/index.md), [services](/services/index.md), [CRDs](/contracts/crds/index.md), core [contracts](/contracts/index.md) and [glossary](/glossary/index.md). All concepts are `status: draft` until reviewed. fusion-weave-testbed and fusion-grafana are out of scope for now.

## 2026-11-23

* **Phase 2**: Added [conventions](/conventions/index.md) (offline vendoring, logging, changelog and releases, Helm and CRDs, controller-runtime, health endpoints), [operations](/operations/index.md) (minikube, deploy matrix for `fusion`, Postgres topology, local DNS, Gitea and Flux) and [known issues](/issues/index.md) (12, each re-checked against the source on this date). Removed from the issue list: the `../logging_principles.md` links in index and weave, which were already fixed upstream. Corrected: content's bff health default is right; forge, index and weave are wrong. All new pages are `status: draft`.
* **Decisions**: Added [decisions](/decisions/index.md) - BFF owns OIDC, vendored Go dependencies, index external Postgres + distroless, multi-tenancy via trusted headers (proposed, mirrors the draft plan). Only decisions written down in the sources; a missing rationale is stated as such. Fixed the index Bitnami-removal version in Postgres topology (0.4.0 per changelog).
* **Phase 3**: Added [REST APIs](/apis/index.md), one page per service (forge, index, weave, wizard, content, bff, ext-bff). Routes come from each router. The pages link to the OpenAPI/Markdown references (bff, index, weave) and don't copy them; forge, wizard and content have no spec file.
* **Review**: platform/ and contracts/ (7 pages) verified by human:chrisfusion and set to stable. Known Issue pages gained the required `resolution` field; all 12 are `unresolved`. The two convention proposals (`/healthz`+`/readyz` for new Go services; upgrading controller-runtime in forge, weave and wizard together) were accepted as rules. All other pages stay unreviewed drafts.
