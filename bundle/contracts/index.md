# Contracts

## Concepts

* [Artifact naming and versioning](artifact-naming.md) - How build outputs are named, versioned and tagged in fusion-index (app.<name>, venv.<name>, semver, movable tags) and which services rely on it.
* [Labels, annotations and finalizers](labels-and-annotations.md) - Kubernetes label, annotation and finalizer keys under fusion-platform.io used across forge, weave and wizard, and what each one means.
* [metadata.yaml](metadata-yaml.md) - App manifest at the root of an app repo - parsed by forge at build time, stored in index, read by weave at deploy time and consumed by the runner via WEAVE_* env vars.
* [Trusted identity headers](trusted-headers.md) - Headers the BFFs set on proxied requests to carry the caller's identity and owner groups, and the rules for trusting them.
* [WEAVE_* environment variables](weave-env-vars.md) - Env vars that fusion-weave injects into codeSource containers from the resolved artifact and its metadata.yaml, and that fusion-runner consumes.

## Subdirectories

* [crds](crds/index.md) - The eleven CRDs of forge, weave and wizard, who writes and who reads them.
