# REST APIs

## Concepts

* [fusion-bff REST API](bff-api.md) - BFF-owned endpoints under /bff (login, userinfo, preferences, presets, system health, admin RBAC and owner groups) plus the /api/<svc>/* proxy; openapi.yaml documents both with x-required-permission.
* [fusion-content REST API](content-api.md) - Read-only content API - changelog entries, help articles and video metadata from polled git repos under /api/v1, TokenReview auth; no spec file.
* [fusion-ext-system-bff REST API](ext-bff-api.md) - Machine-client gateway to fusion-index only - an authenticated /api/index/* proxy (OAuth2 client credentials, API key or open) and a read-only, type-filtered public /api/public/index/*; reference is ENDPOINT.md.
* [fusion-forge REST API](forge-api.md) - Build API of fusion-forge - requirements, git and app builds, GitWatcher CRUD and bulk build maintenance under /api/v1, TokenReview auth; no OpenAPI file, the router is the reference.
* [fusion-index REST API](index-api.md) - Artifact registry API - artifacts, semver versions, files, tags, types, retention and admin cleanup under /api/v1; the embedded openapi.yaml is served at /api/openapi.json and /swagger/.
* [fusion-weave REST API](weave-api.md) - CRUD over the weave CRDs (job/service templates, chains, apps, triggers, runs, batch/kafka triggers) under /api/v1 plus a read-only /monitor/v1, on port 8082; reference is apidescription.md.
* [fusion-wizard REST API](wizard-api.md) - Wizard API on port 8083 - list definitions, create/retry/rollback/delete WizardRuns and inspect ledger resources under /api/v1, TokenReview auth with audience fusion-bff; no spec file.
