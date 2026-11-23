# Conventions

## Concepts

* [Changelog, versions and image tags](changelog-and-releases.md) - Each repo keeps a Keep-a-Changelog CHANGELOG.md updated before every commit; a release promotes [Unreleased] and bumps chart, app and image tag to the same semver.
* [Health endpoints](health-endpoints.md) - Two health-path families exist - Quarkus-style /q/health/live|ready for the REST services ported from Quarkus, and /healthz|/readyz for operators and newer APIs.
* [Helm charts and CRDs](helm-and-crds.md) - Every service ships its own chart in deployment/; CRDs are generated into config/crd/bases and copied into the chart's crds/, which plain Helm installs but never upgrades.
* [Kubernetes operators with controller-runtime](controller-runtime.md) - forge, weave and wizard operators are built on controller-runtime v0.19.3 and client-go v0.31.0, with probes on /healthz and /readyz and logr/zap logging.
* [Logging](logging.md) - Go services log through log/slog with LOG_LEVEL/LOG_FORMAT (JSON by default) and a per-request logger from LoggerFromCtx; controller-runtime binaries keep logr/zap.
* [Offline builds and Go vendoring](offline-vendoring.md) - Every Go repo commits vendor/ and builds with -mod=vendor because the image-building CI has no internet; docker build --network none is the test.
