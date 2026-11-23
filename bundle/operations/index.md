# Operations

## Concepts

* [Deploy matrix for the fusion namespace](deploy-matrix.md) - How each service is actually deployed into the hand-managed fusion namespace - which ones use Helm, which raw YAML or kubectl set image, and the traps for each.
* [Gitea mirror and Flux instances](gitea-and-flux.md) - Flux on minikube watches Gitea mirrors of every repo (not the real origin); git push gitea main deploys to fusion-dev-a/b, with chart-version bumps and CRD ownership as the main traps.
* [Local DNS for *.fusion.local](local-dns.md) - A host-side dnsmasq on 127.0.0.1:5353 resolves the *.fusion.local wildcard to the minikube IP via systemd-resolved, self-healing every 60s; only dev.fusion.local stays in /etc/hosts.
* [Local minikube cluster](minikube.md) - The dev cluster is one minikube with ingress-nginx, Keycloak, Gitea and Flux; images are built into minikube's Docker daemon with fresh semver tags.
* [Postgres topology](postgres-topology.md) - forge bundles its own Postgres; index and bff share one server per instance (fusion-index-postgresql, databases fusion_index and fusion_bff); content and weave have no database.
