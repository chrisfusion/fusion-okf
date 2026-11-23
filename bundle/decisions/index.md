# Decisions

## Concepts

* [fusion-index uses external Postgres and a Debian distroless image](index-external-postgres-distroless.md) - Accepted - index dropped its bundled Bitnami Postgres subchart (0.4.0) for a pre-installed server, and dropped Alpine for distroless Debian (0.6.0) because production can use apt but not apk.
* [Multi-tenancy via owner groups and BFF trusted headers](multi-tenancy-trusted-headers.md) - Proposed (draft design) - the BFF resolves owner groups and sends read/write scope as X-User-* headers; services enforce ownership through the fusion-shared ownership package.
* [The BFF owns the whole OIDC flow](bff-owns-oidc.md) - Accepted - fusion-bff runs the OIDC login and keeps tokens server-side behind an HttpOnly session cookie; fusion-spectra never sees Keycloak or a token.
* [Vendor Go dependencies for offline CI](vendor-go-dependencies.md) - Accepted - every Go repo commits vendor/ and builds with -mod=vendor, because the CI environment that builds images has no internet access.
