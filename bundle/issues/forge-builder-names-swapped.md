---
type: Known Issue
title: forge builder functions buildFromGit and buildFromApp are named backwards
description: In fusion-forge's builder, buildFromGit handles pyproject.toml wheels and buildFromApp handles metadata.yaml apps - the opposite of what the names suggest.
resource: repo://fusion-forge/CLAUDE.md
tags: [forge, build, naming]
resolution: unresolved
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
---

# Detail

In `builder/main.go` of [fusion-forge](/services/fusion-forge.md):[^forge]

| Function | What it really does | Planned name |
|---|---|---|
| `buildFromGit` | pyproject.toml → pip wheel (Python libraries) | `buildFromToml` |
| `buildFromApp` | [metadata.yaml](/contracts/metadata-yaml.md) → pip install requirements (Streamlit apps) | `buildFromMetadata` |

# Constraint

Hold off on the rename until the REST layer and the BFF clients have been audited. The `BUILD_TYPE` values `"git"` and `"app"` ([build type](/glossary/build-type.md)) are part of the contract and must stay unchanged.[^forge]

[^forge]: fusion-forge CLAUDE.md
