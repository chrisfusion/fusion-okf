---
type: Known Issue
title: fusion-weave CLAUDE.md says index has no PVC
description: fusion-weave's CLAUDE.md claims fusion-index-backend loses artifact files on restart, but index now has an artifacts PVC enabled in values-dev.yaml.
resource: repo://fusion-flux/CLAUDE.md
tags: [weave, index, docs, storage]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
---

# Symptom

The [fusion-weave](/services/fusion-weave.md) CLAUDE.md (in the `fusion-flux` clone, see [weave vs flux](/glossary/weave-vs-flux.md)) says "fusion-index-backend has no PVC - artifact file bytes are lost on pod restart" and recommends re-uploading files when downloads return 500.[^flux]

# Reality

`backend.persistence.enabled: true` creates PVC `fusion-index-backend-artifacts` mounted at `/data/artifacts`, enabled by default in `values-dev.yaml`. Files are only ephemeral when `storageBackend: FILESYSTEM` runs without the PVC.[^index]

# Impact

An agent following the weave note may delete and re-upload artifact versions that were never broken. Before doing that, check whether the PVC exists.

# Fix

Replace the note in fusion-weave's CLAUDE.md with a pointer to [fusion-index](/services/fusion-index.md) storage. This needs an edit in the other repo, which the bundle does not make itself.

[^flux]: fusion-weave CLAUDE.md
[^index]: fusion-index CLAUDE.md
