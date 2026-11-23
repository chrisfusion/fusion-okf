---
type: Glossary Term
title: venvpack
description: A packed Python virtual environment (.tar.gz with top-level venv/) produced by forge, stored in index and unpacked by the runner.
tags: [glossary, forge, runner]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
  - { id: forge, resource: repo://fusion-forge/CLAUDE.md, title: fusion-forge CLAUDE.md }
---

The build output of [fusion-forge](/services/fusion-forge.md): a `venv-pack` archive of a virtualenv with all dependencies installed (for app builds also the project's subpackages, copied into `site-packages`). Entries start with `venv/`. The `bin/python3.X` symlinks point to the build host's interpreter and are rewritten by [fusion-runner](/services/fusion-runner.md) at start.[^runner][^forge]

App subdirectories need an `__init__.py`, and `main.py` must locate them via package imports, not file paths.[^forge]

[^runner]: fusion-runner CLAUDE.md
[^forge]: fusion-forge CLAUDE.md
