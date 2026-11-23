---
type: Known Issue
title: fusion-index accepts an upload named ".."
description: The multipart filename goes unvalidated into the storage path, so a file named ".." resolves to the version's parent directory on the filesystem backend.
resource: repo://fusion-index/internal/api/handlers/files.go
tags: [index, storage, security]
status: draft
generated: { by: claude-code/opus-5.5, at: 2026-11-23T12:30:00Z }
sources:
  - { id: files, resource: repo://fusion-index/internal/api/handlers/files.go, title: fusion-index files.go }
  - { id: helpers, resource: repo://fusion-index/internal/api/handlers/helpers.go, title: fusion-index helpers.go }
  - { id: fs, resource: repo://fusion-index/internal/storage/filesystem.go, title: fusion-index filesystem.go }
---

# Cause

The upload handler uses `header.Filename` as-is.[^files] Go's multipart parser applies `filepath.Base`, which strips directories but returns `..` and `.` unchanged. The name becomes the last segment of `{artifactID}/{major}/{minor}/{patch}/{fileID}/{name}`,[^helpers] and the filesystem backend resolves it with `filepath.Join(root, path)`.[^fs]

# Impact

`filepath.Join` cleans the path, so `..` points one level up at the `{patch}` directory instead of a file under `{fileID}`. The path stays inside the storage root, but the upload either fails or writes a file where a directory is expected, which can block later uploads to that version. On S3 the key just contains a literal `..` segment.

# Fix

Reject `.`, `..`, empty names and names with path separators in the upload handler, with a 400 response.

[^files]: fusion-index files.go
[^helpers]: fusion-index helpers.go
[^fs]: fusion-index filesystem.go
