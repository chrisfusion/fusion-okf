---
type: Known Issue
title: fusion-runner CLAUDE.md points to a missing tmp_create_docker.md
description: fusion-runner's CLAUDE.md sends readers to tmp_create_docker.md for the full env-var reference, but no such file exists in any repo.
resource: repo://fusion-runner/CLAUDE.md
tags: [runner, weave, docs, env]
resolution: unresolved
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: runner, resource: repo://fusion-runner/CLAUDE.md, title: fusion-runner CLAUDE.md }
---

# Gap

The env-var section of [fusion-runner](/services/fusion-runner.md) ends with "see `tmp_create_docker.md` for the full reference".[^runner] The file does not exist in fusion-runner or in any sibling repo.

# Where to look instead

[Weave env vars](/contracts/weave-env-vars.md) collects the variables fusion-weave injects from [metadata.yaml](/contracts/metadata-yaml.md).

# Fix

Point the CLAUDE.md line at the contract page, or at the injecting code in fusion-weave.

[^runner]: fusion-runner CLAUDE.md
