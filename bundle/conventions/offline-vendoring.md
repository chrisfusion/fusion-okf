---
type: Convention
title: Offline builds and Go vendoring
description: Every Go repo commits vendor/ and builds with -mod=vendor because the image-building CI has no internet; docker build --network none is the test.
tags: [forge, index, weave, bff, ext-bff, wizard, content, runner, shared, build]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
  - { id: shared, resource: repo://fusion-shared/CLAUDE.md, title: fusion-shared CLAUDE.md }
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

# Rule

The CI environment that builds images has no internet access, so builds must not download anything.[^bff]

- `vendor/` is committed. Makefile targets and Dockerfiles use `-mod=vendor`, and no Dockerfile runs `go mod download`.
- After any `go.mod` change: `make vendor`, then commit `vendor/` together with `go.mod`/`go.sum`. `make check-vendor` fails on drift.[^forge]
- `vendor/**` is marked `-diff linguist-vendored` in `.gitattributes`.
- To verify: `docker build --network none .`
- Blueprint: `docs/go-vendoring-blueprint.md` in each repo.

# Remaining external inputs

- **Docker base images**: `golang:<ver>-alpine` and `gcr.io/distroless/static:nonroot` (index: `distroless/base-debian13`). Mirror them in an internal registry or `docker save`/`docker load` them.
- forge's `builder/Dockerfile` also needs `python:3.12-slim-bookworm` and its `apt-get`.[^forge]
- **Build tools** such as `controller-gen` (`make generate`) are not vendored. Keep them out of the CI build path.[^flux]

# Go versions

All modules are on Go 1.25 except [fusion-weave](/services/fusion-weave.md), which moved to 1.27.3 (go.mod `toolchain` line, `golang:1.27.3-alpine`). Outside Docker the pinned toolchain must be installed (`GOTOOLCHAIN=local`). For weave on a box whose system Go is older, leave `GOTOOLCHAIN` unset so the cached toolchain is used, and use the toolchain's own `gofmt`.[^flux]

# Special cases

- [fusion-runner](/services/fusion-runner.md) has no dependencies (empty `go.sum`) and builds with `GOPROXY=off GOFLAGS=-mod=readonly`, so adding a dependency fails loudly.[^runner]
- [fusion-shared](/services/fusion-shared.md) is vendored by its consumers. A published tag must build without network access, and committed `go.mod` files contain no `replace` directives. For local co-development, use a gitignored `go.work`.[^shared]
- fusion-wizard: `vendor/` is ~57 MB on disk, ~7 MB in git.[^wizard]

[^bff]: fusion-bff CLAUDE.md
[^forge]: fusion-forge CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^runner]: fusion-runner CLAUDE.md
[^shared]: fusion-shared CLAUDE.md
[^wizard]: fusion-wizard CLAUDE.md
