# fusion-okf

Cross-repository knowledge about the fusion platform, packaged as an
[Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format) (OKF v0.2) bundle:
plain markdown with YAML frontmatter, readable by humans and agents alike.

The per-repo `CLAUDE.md` files stay authoritative for repo-internal details (commands, code layout,
code-level gotchas). This bundle holds what spans repositories: how the services fit together, the
contracts between them, the CRDs, shared conventions and the glossary. It does not modify any other repo.

## Layout

```
bundle/            the OKF bundle (only concepts, index.md, log.md and .okf-dirs.yaml)
  platform/        overview and end-to-end artifact flow
  services/        one page per fusion-* repo
  contracts/       metadata.yaml, naming, env vars, headers, labels
    crds/          the eleven CRDs
  glossary/        one page per term
tools/okf_check.py validator, index generator, drift check
```

Start reading at [`bundle/index.md`](bundle/index.md) or [`bundle/platform/overview.md`](bundle/platform/overview.md).

## Profile (rules on top of OKF v0.2)

| Field | Rule |
|---|---|
| `type` | One of `Platform Overview`, `Service`, `Custom Resource`, `REST API`, `Contract`, `Convention`, `Playbook`, `Decision`, `Glossary Term`, `Known Issue` |
| `title`, `description` | Required (OKF only requires `type`); `description` is one sentence and feeds `index.md` |
| `tags` | Service short names (`forge`, `index`, `weave`, `bff`, `ext-bff`, `wizard`, `runner`, `content`, `spectra`, `fleet`, `shared`) plus topic |
| `resource` | The thing described, as `repo://<repo>/<path>` or an absolute URL |
| `sources` | Files the page was derived from, `repo://<repo>/<path>`; claims cite them with footnotes `[^id]` |
| `generated` | `{ by: claude-code/opus-5.5, at: ... }` for generated content, `human:<id>` for hand-written |
| `verified` | Added when a human reviewed the page (`human:chrisfusion`) - makes it *human-reviewed* |
| `status` | Generated pages start as `draft`, become `stable` after review |
| Links | Bundle-absolute (`/services/fusion-forge.md`) |

`repo://<repo>/<path>` resolves against the directory that contains the sibling `fusion-*` clones
(by default the parent of this repo). It keeps paths stable and free of internal hostnames.

## Tooling

All checks run in Docker (Python 3.12); the sibling repos are mounted read-only.

```bash
make check      # validate + index.md up to date + drift (non-zero exit on errors)
make index      # regenerate every index.md from frontmatter
make drift      # pages whose repo:// sources changed after their generated.at
make validate   # conformance only
```

- **validate** - OKF conformance (frontmatter, `type`, reserved files) plus the profile above;
  footnotes must match a `sources[].id`. Broken links and missing local sources are warnings
  (OKF allows not-yet-written knowledge).
- **drift** - compares the last git commit of every `repo://` source with the page's
  `generated.at`. A newer source (or uncommitted changes) means the page may be stale: re-check it,
  update it and bump `generated.at`.
- **index** - `index.md` files are generated; never edit them by hand. Directory headings and
  descriptions come from `bundle/.okf-dirs.yaml`.

## Contributing

1. Edit or add a concept under `bundle/`, keep the profile above.
2. `make index && make check`.
3. Add an entry to `bundle/log.md`.

## License

GPL-3.0 - see [LICENSE](LICENSE).
