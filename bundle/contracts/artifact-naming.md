---
type: Contract
title: Artifact naming and versioning
description: How build outputs are named, versioned and tagged in fusion-index (app.<name>, venv.<name>, semver, movable tags) and which services rely on it.
tags: [index, forge, weave, spectra, wizard, contract]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: spectra, resource: repo://fusion-spectra/CLAUDE.md, title: fusion-spectra CLAUDE.md }
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: extbff, resource: repo://fusion-ext-system-bff/CLAUDE.md, title: fusion-ext-system-bff CLAUDE.md }
---

# Names

| Build type | Index artifact | Created by |
|---|---|---|
| requirements, git (pyproject) | `venv.<name>` | forge, on first build |
| app (metadata.yaml) | `app.<name>` | forge, on first build |

`<name>` is forge's build name. A forge build object's `name` is **not** the index artifact name - clients (spectra, wizard) building a `codeSource.artifactName` must add the prefix.[^forge][^spectra]

index itself accepts any dotted, Python-style name (`org.team.name`, max 500 chars).[^index]

# Versions

- Strict semver `major.minor.patch`, stored as three integers (no pre-release or build metadata).
- A version is created *before* the build runs; a failed build deletes it again (best-effort).
- Uniqueness per artifact: re-building an existing version answers 409.[^forge]

# Tags

- A tag (`stable`, ...) points to exactly one version of an artifact; assigning it again moves it atomically (`PUT /api/v1/artifacts/{id}/tags/{tag}` with `{"version": "1.2.3"}`).
- Tagged versions are protected from bulk deletes and retention; an `ADMIN_PROTECTED_TAG` protects whole artifacts from admin cleanup.[^index]
- weave deploys by `artifactName@tag` and polls the tag; moving the tag is how a new version is rolled out.[^flux]
- forge's GitWatcher `autoTag` moves a tag to every new build; [fusion-ext-system-bff](/services/fusion-ext-system-bff.md) only serves downloads of versions carrying `PUBLIC_DOWNLOAD_TAG`.[^extbff]

# Files of a version

| Build type | Files |
|---|---|
| requirements / git | venvpack `.tar.gz` (+ optional entrypoint for git builds) |
| app | venvpack `.tar.gz`, `main.py`, [`metadata.yaml`](/contracts/metadata-yaml.md) |

The venvpack has a top-level `venv/` prefix ([venvpack](/glossary/venvpack.md)).

[^forge]: fusion-forge CLAUDE.md
[^index]: fusion-index CLAUDE.md
[^spectra]: fusion-spectra CLAUDE.md
[^flux]: fusion-weave CLAUDE.md
[^extbff]: fusion-ext-system-bff CLAUDE.md
