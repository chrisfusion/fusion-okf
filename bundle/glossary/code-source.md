---
type: Glossary Term
title: Code source
description: weave's codeSource mechanism - load an index artifact by tag into a pod via the code-loader init container and follow tag moves with rolling restarts.
tags: [glossary, weave, index]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: flux, resource: repo://fusion-flux/CLAUDE.md, title: fusion-weave CLAUDE.md }
---

`spec.codeSource` (`artifactName`, `tag`, `indexURL`, `mountPath`, `loaderImage`) on [WeaveJobTemplate](/contracts/crds/weavejobtemplate.md), [WeaveServiceTemplate](/contracts/crds/weaveservicetemplate.md) and [WeaveApp](/contracts/crds/weaveapp.md) separates *code* from *image*: the image is a generic runner, the code comes from [fusion-index](/services/fusion-index.md).[^flux]

- A `code-loader` init container (`/loader` from the weave image) resolves tag → version, downloads every file as-is into `mountPath` (default `/weave-code`) and writes `.version`.
- Services poll the tag every `CODE_SOURCE_POLL_INTERVAL` (60 s) and roll when it moves.
- The container receives [`WEAVE_*` env vars](/contracts/weave-env-vars.md).
- In minikube set `loaderImage` to the weave operator image; the default `fusion-code-loader:latest` does not exist.[^flux]

[^flux]: fusion-weave CLAUDE.md
