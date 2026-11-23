# Known issues

## Concepts

* [BFF health probe defaults miss forge, index and weave](bff-health-url-defaults.md) - fusion-bff probes `<url>/health` for forge, index and weave, but none of them serves that path, so /bff/system-health reports them down unless the URL is overridden.
* [Conflicting git push rules between spectra and fleet](push-rule-conflict.md) - fusion-spectra's CLAUDE.md says push to origin only, while fusion-fleet's says push to gitea freely and never to origin without confirmation.
* [forge and index ignore the X-User-* trusted headers](trusted-headers-not-consumed.md) - The BFF forwards X-User-* identity and group headers, but neither fusion-forge nor fusion-index reads them yet, so owner-group isolation is not enforced.
* [forge builder functions buildFromGit and buildFromApp are named backwards](forge-builder-names-swapped.md) - In fusion-forge's builder, buildFromGit handles pyproject.toml wheels and buildFromApp handles metadata.yaml apps - the opposite of what the names suggest.
* [fusion-bff CLAUDE.md does not mention the wizard upstream](bff-claude-md-missing-wizard.md) - The BFF proxies /api/wizard/* to fusion-wizard (health at /healthz), but the BFF's CLAUDE.md never mentions wizard.
* [fusion-content uses the standard log package against the logging rules](content-logging-exception.md) - The shared logging principles forbid import "log", but fusion-content logs with log.Printf and its CLAUDE.md says not to migrate to slog.
* [fusion-ext-system-bff CLAUDE.md describes a flux/ directory that does not exist](ext-bff-flux-dir-missing.md) - ext-bff's CLAUDE.md lists Flux config in flux/ with three environments, but the directory is missing and neither ext-bff nor wizard has a HelmRelease in fusion-fleet.
* [fusion-index /q/metrics is JSON, not Prometheus](index-metrics-not-prometheus.md) - The Quarkus-style path /q/metrics returns a JSON registry snapshot, so a Prometheus scrape of it fails.
* [fusion-index accepts an upload named ".."](index-dotdot-filename.md) - The multipart filename goes unvalidated into the storage path, so a file named ".." resolves to the version's parent directory on the filesystem backend.
* [fusion-runner CLAUDE.md points to a missing tmp_create_docker.md](runner-missing-env-reference.md) - fusion-runner's CLAUDE.md sends readers to tmp_create_docker.md for the full env-var reference, but no such file exists in any repo.
* [fusion-weave CLAUDE.md says index has no PVC](weave-claude-md-index-pvc-stale.md) - fusion-weave's CLAUDE.md claims fusion-index-backend loses artifact files on restart, but index now has an artifacts PVC enabled in values-dev.yaml.
* [Local port-forward ports used twice](port-forward-clash.md) - The CLAUDE.md files forward forge and index both to local port 18080, and content and ext-bff both to 18082, so these pairs cannot be port-forwarded at the same time.
