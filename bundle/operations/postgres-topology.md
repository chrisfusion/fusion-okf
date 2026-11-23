---
type: Playbook
title: Postgres topology
description: forge bundles its own Postgres; index and bff share one server per instance (fusion-index-postgresql, databases fusion_index and fusion_bff); content and weave have no database.
tags: [operations, postgres, forge, index, bff, content, weave, fleet]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
  - { id: bff, resource: repo://fusion-bff/CLAUDE.md, title: fusion-bff CLAUDE.md }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
---

| Service | Database | Server |
|---|---|---|
| [forge](/services/fusion-forge.md) | own | bundled raw manifests in its chart (`postgresql.enabled`, default true)[^fleet] |
| [index](/services/fusion-index.md) | `fusion_index` | external since 0.5.0. The Bitnami subchart is gone, and upgrading a 0.4.x release prunes its StatefulSet.[^fleet] |
| [bff](/services/fusion-bff.md) | `fusion_bff` (optional) | the index server, via `db.dsn`[^bff] |
| content, weave, wizard | none (weave and wizard state lives in CRDs) | - |

# Dev server

Every instance (and the manual `fusion` namespace) runs a hand-rolled `postgres:18-trixie` Deployment, Service and Secret named **`fusion-index-postgresql`**: user `fusion` (superuser), dev password, **emptyDir** data. It keeps the old Bitnami name so existing DSNs still resolve. index's `values-dev.yaml` uses the short host name, so it resolves in any namespace.[^fleet]

- Files: `fusion-fleet/dev-cluster/projects/fusion/dev/instance_a/{secrets,postgres-deployment}.yaml`. Apply them with `-n fusion` for the manual namespace.
- emptyDir means a pod restart loses all data. Use index's backup/restore (`pg_dump`, S3) for anything worth keeping.[^index]
- Databases are created by `createDatabaseJob` hook Jobs (index, bff). No manual `CREATE DATABASE` is needed.[^fleet]

# pg_dump compatibility

index's runtime image ships `pg_dump`/`psql` from `PG_MAJOR` (default 18), which must be ≥ the newest server it backs up. Restoring onto a server older than 17 needs the stripped `transaction_timeout` line, which `restore-db` handles.[^index]

[^fleet]: fusion-fleet CLAUDE.md
[^bff]: fusion-bff CLAUDE.md
[^index]: fusion-index CLAUDE.md
