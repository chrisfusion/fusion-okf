---
type: Glossary Term
title: Ledger
description: fusion-wizard's ref-counted record of every upstream object it touches, which makes provisioning idempotent and rollback exact.
tags: [glossary, wizard]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-17T14:30:00Z }
sources:
  - { id: wizard, resource: repo://fusion-wizard/CLAUDE.md, title: fusion-wizard CLAUDE.md }
---

One [WizardResource](/contracts/crds/wizardresource.md) per upstream object (GitWatcher, index artifact/tag, WeaveApp, chain, ...), with a list of referencing runs.[^wizard]

- **Write-ahead:** entry first, upstream create second.
- **Ownership:** `managed: true` only for objects the wizard created. Objects found without an entry are recorded as `FoundUnowned` / `managed: false` and never deleted.
- **Sharing:** a second run needing the same object adds a ref; the object is deleted only when the last ref goes.
- **Conflicts:** same name with a different `specHash` is reported, never silently updated.
- **Rollback:** driven by the ledger (every entry referencing the run), in kind order trigger → chain → template → watcher → tag → artifact.

Known gap: an e2e run once recorded a pre-existing index artifact as `Created` and deleted it on rollback - run e2e tests only against repos nothing else uses.[^wizard]

[^wizard]: fusion-wizard CLAUDE.md
