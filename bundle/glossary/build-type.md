---
type: Glossary Term
title: Build type
description: forge's three build flavours - requirements build, git build and app build - which differ in input, API and artifact prefix.
tags: [glossary, forge]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
---

| Term | Input | Result |
|---|---|---|
| **requirements build** ("venv build") | uploaded `requirements.txt` (multipart) | `venv.<name>` |
| **git build** | repo with `pyproject.toml`, wheel built with pip (library) | `venv.<name>` |
| **app build** | repo with [`metadata.yaml`](/contracts/metadata-yaml.md) + `requirements.txt` + `main.py` (e.g. Streamlit app) | `app.<name>` |

The builder's internal function names are swapped: `buildFromGit` handles the pyproject path, `buildFromApp` the metadata.yaml path.[^forge] Details: [fusion-forge](/services/fusion-forge.md), [artifact naming](/contracts/artifact-naming.md).

[^forge]: fusion-forge CLAUDE.md
