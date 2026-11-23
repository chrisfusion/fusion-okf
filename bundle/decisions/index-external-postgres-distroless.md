---
type: Decision
title: fusion-index uses external Postgres and a Debian distroless image
description: Accepted - index dropped its bundled Bitnami Postgres subchart (0.4.0) for a pre-installed server, and dropped Alpine for distroless Debian (0.6.0) because production can use apt but not apk.
resource: repo://fusion-index/CHANGELOG.md
tags: [index, postgres, build, decision]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:40:00Z }
sources:
  - { id: cl, resource: repo://fusion-index/CHANGELOG.md, title: fusion-index CHANGELOG }
  - { id: index, resource: repo://fusion-index/CLAUDE.md, title: fusion-index CLAUDE.md }
  - { id: fleet, resource: repo://fusion-fleet/CLAUDE.md, title: fusion-fleet CLAUDE.md }
---

**Status:** accepted, shipped.

# 1. External Postgres (0.4.0, 2026-07-07)

- **What changed:** the bundled Bitnami `postgresql` subchart was removed. fusion-index now always connects to a pre-installed server. Values were flattened to `postgresql.host/port/database/username/password/existingSecret`.[^cl]
- **Database creation:** the new `createDatabaseJob` hook creates the database, using separate admin credentials.[^cl]
- **Upgrade trap:** upgrading an old release prunes the subchart's StatefulSet, so reset or uninstall first.[^fleet]
- **Version mismatch:** fusion-fleet's CLAUDE.md dates this change to 0.5.0. The changelog lists it under 0.4.0.
- **Reason:** not recorded. In practice, the bff database shares the same server; see [Postgres topology](/operations/postgres-topology.md).

# 2. No Alpine, distroless Debian (0.6.0, 2026-10-27)

- **Reason:** "no Alpine (production can `apt`, not `apk`)".[^index]
- **New images:** build stage `golang:1.25-trixie`, runtime `gcr.io/distroless/base-debian13:nonroot`, hook Jobs on `postgres:18-trixie`.[^cl]
- **Why `base` and not `static`:** the runtime ships `pg_dump`/`psql` for backups, copied with their shared libraries from the postgres image, and they need glibc. The two images must stay on the same Debian release.[^index]
- **New user:** the container runs as UID/GID 65532. A PVC written by the old root image needs a chown or a reset.[^cl]

[^cl]: fusion-index CHANGELOG
[^index]: fusion-index CLAUDE.md
[^fleet]: fusion-fleet CLAUDE.md
