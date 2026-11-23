#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate, index and drift-check the fusion-platform OKF bundle.

Commands:
  validate  OKF v0.2 conformance plus the fusion profile (see README.md)
  index     (re)generate every index.md from concept frontmatter
  drift     list concepts whose repo:// sources changed after generated.at
  check     validate + index --check + drift (CI entry point)
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

OKF_VERSION = "0.2"
RESERVED = {"index.md", "log.md"}
PROFILE_REQUIRED = ("type", "title", "description")
STATUS_VALUES = {"draft", "stable", "deprecated"}
ACTOR_RE = re.compile(r"^(human:[\w.@-]+|process:[\w.@-]+|[\w.-]+/[\w.:-]+)$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
FOOTNOTE_REF_RE = re.compile(r"\[\^([\w-]+)\](?!:)")
REPO_SCHEME = "repo://"
DIRS_FILE = ".okf-dirs.yaml"


# --------------------------------------------------------------------------- model


@dataclass
class Concept:
    path: Path  # absolute
    rel: str  # bundle-relative, posix, with .md
    meta: dict
    body: str


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"ERROR   {where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"WARNING {where}: {msg}")

    def print(self) -> None:
        for line in self.errors + self.warnings:
            print(line)
        print(f"-- {len(self.errors)} error(s), {len(self.warnings)} warning(s)")


# --------------------------------------------------------------------------- parsing


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter_yaml, body); frontmatter is None when absent."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :]


def load_concepts(bundle: Path, report: Report) -> list[Concept]:
    concepts = []
    for path in sorted(bundle.rglob("*.md")):
        if path.name in RESERVED:
            continue
        rel = path.relative_to(bundle).as_posix()
        raw, body = split_frontmatter(path.read_text(encoding="utf-8"))
        if raw is None:
            report.error(rel, "missing YAML frontmatter")
            continue
        try:
            meta = yaml.safe_load(raw) or {}
        except yaml.YAMLError as exc:
            report.error(rel, f"unparseable frontmatter: {exc}")
            continue
        if not isinstance(meta, dict):
            report.error(rel, "frontmatter is not a mapping")
            continue
        concepts.append(Concept(path, rel, meta, body))
    return concepts


def as_list(value) -> list:
    """OKF allows a bare mapping where a list is expected (verified)."""
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def to_datetime(value) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        return value if value.tzinfo else value.replace(tzinfo=dt.timezone.utc)
    if isinstance(value, str):
        try:
            return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def resolve_repo_uri(uri: str, repos_root: Path) -> Path:
    """repo://<repo>/<path>[#anchor] -> <repos_root>/<repo>/<path>"""
    return repos_root / uri[len(REPO_SCHEME) :].split("#", 1)[0]


# --------------------------------------------------------------------------- validate


def validate(bundle: Path, repos_root: Path, report: Report) -> list[Concept]:
    concepts = load_concepts(bundle, report)
    for c in concepts:
        validate_meta(c, report)
        validate_links(c, bundle, report)
        validate_sources(c, repos_root, report)
    validate_reserved(bundle, report)
    return concepts


def validate_meta(c: Concept, report: Report) -> None:
    for key in PROFILE_REQUIRED:
        if not str(c.meta.get(key) or "").strip():
            # type is required by OKF itself, title/description by our profile
            report.error(c.rel, f"missing required field '{key}'")
    status = c.meta.get("status")
    if status is not None and status not in STATUS_VALUES:
        report.error(c.rel, f"invalid status '{status}'")
    generated = c.meta.get("generated")
    if generated is not None:
        if not isinstance(generated, dict) or not generated.get("by"):
            report.error(c.rel, "generated needs at least 'by'")
        else:
            check_actor(c, generated["by"], "generated.by", report)
            if "at" in generated and to_datetime(generated["at"]) is None:
                report.error(c.rel, "generated.at is not an ISO 8601 datetime")
    for entry in as_list(c.meta.get("verified")):
        if not isinstance(entry, dict) or not entry.get("by") or not entry.get("at"):
            report.error(c.rel, "verified entries need 'by' and 'at'")
        else:
            check_actor(c, entry["by"], "verified.by", report)
    if "stale_after" in c.meta and to_datetime(c.meta["stale_after"]) is None:
        report.error(c.rel, "stale_after is not an ISO 8601 datetime")


def check_actor(c: Concept, actor: str, where: str, report: Report) -> None:
    if not ACTOR_RE.match(str(actor)):
        report.error(c.rel, f"{where} '{actor}' does not follow the actor convention")


def validate_links(c: Concept, bundle: Path, report: Report) -> None:
    for target in LINK_RE.findall(c.body):
        if re.match(r"^[a-z]+://|^mailto:|^#", target):
            continue
        clean = target.split("#", 1)[0]
        resolved = (bundle / clean.lstrip("/")) if clean.startswith("/") else (c.path.parent / clean)
        if not resolved.exists():
            # OKF: broken links are allowed (not-yet-written knowledge) -> warning only
            report.warn(c.rel, f"link target not found: {target}")


def validate_sources(c: Concept, repos_root: Path, report: Report) -> None:
    ids = set()
    for src in as_list(c.meta.get("sources")):
        if not isinstance(src, dict) or not src.get("resource"):
            report.error(c.rel, "every sources entry needs 'resource'")
            continue
        if src.get("id"):
            ids.add(src["id"])
        res = str(src["resource"])
        if res.startswith(REPO_SCHEME) and not resolve_repo_uri(res, repos_root).exists():
            report.warn(c.rel, f"source not found locally: {res}")
    for ref in sorted(set(FOOTNOTE_REF_RE.findall(c.body)) - ids):
        report.error(c.rel, f"footnote [^{ref}] has no matching sources[].id")


def validate_reserved(bundle: Path, report: Report) -> None:
    for path in bundle.rglob("index.md"):
        rel = path.relative_to(bundle).as_posix()
        raw, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        if raw is not None and path.parent != bundle:
            report.error(rel, "only the bundle-root index.md may carry frontmatter")
    for path in bundle.rglob("log.md"):
        rel = path.relative_to(bundle).as_posix()
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## ") and not re.match(r"^## \d{4}-\d{2}-\d{2}$", line):
                report.error(rel, f"log heading must be '## YYYY-MM-DD': {line}")


# --------------------------------------------------------------------------- index


def render_indexes(bundle: Path, concepts: list[Concept]) -> dict[Path, str]:
    dirs_meta = yaml.safe_load((bundle / DIRS_FILE).read_text(encoding="utf-8")) or {}
    by_dir: dict[Path, list[Concept]] = {}
    for c in concepts:
        by_dir.setdefault(c.path.parent, []).append(c)
    all_dirs = {bundle} | {p for p in bundle.rglob("*") if p.is_dir()}
    out = {}
    for d in sorted(all_dirs):
        lines = []
        if d == bundle:
            lines += ["---", f'okf_version: "{OKF_VERSION}"', "---", ""]
        rel_dir = "" if d == bundle else d.relative_to(bundle).as_posix()
        heading = dirs_meta.get(rel_dir or ".", {}).get("title", rel_dir or "fusion-platform knowledge bundle")
        lines += [f"# {heading}", ""]
        items = sorted(by_dir.get(d, []), key=lambda c: str(c.meta.get("title", "")).lower())
        if items:
            lines += ["## Concepts", ""]
            for c in items:
                lines.append(f"* [{c.meta.get('title')}]({c.path.name}) - {c.meta.get('description', '')}")
            lines.append("")
        subdirs = sorted(p for p in d.iterdir() if p.is_dir())
        if subdirs:
            lines += ["## Subdirectories", ""]
            for sub in subdirs:
                key = sub.relative_to(bundle).as_posix()
                desc = dirs_meta.get(key, {}).get("description", "")
                lines.append(f"* [{sub.name}]({sub.name}/index.md) - {desc}")
            lines.append("")
        out[d / "index.md"] = "\n".join(lines).rstrip() + "\n"
    return out


def write_indexes(bundle: Path, concepts: list[Concept], check_only: bool, report: Report) -> None:
    for path, content in render_indexes(bundle, concepts).items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        rel = path.relative_to(bundle).as_posix()
        if check_only:
            report.error(rel, "out of date - run 'make index'")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"wrote {rel}")


# --------------------------------------------------------------------------- drift


def git_last_change(file: Path) -> tuple[dt.datetime | None, bool]:
    """Return (last commit datetime, has_uncommitted_changes) for a file."""
    repo = file.parent
    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True).stdout.strip()
    # Commits marked [okf-skip] (e.g. adding the bundle pointer line) do not count as content changes.
    date = git("log", "-1", "--format=%cI", "--invert-grep", "--grep=\\[okf-skip\\]", "--", file.name)
    dirty = bool(git("status", "--porcelain", "--", file.name))
    return (to_datetime(date) if date else None), dirty


def drift(concepts: list[Concept], repos_root: Path, report: Report) -> None:
    cache: dict[Path, tuple[dt.datetime | None, bool]] = {}
    for c in concepts:
        generated_at = to_datetime((c.meta.get("generated") or {}).get("at"))
        for src in as_list(c.meta.get("sources")):
            res = str((src or {}).get("resource", ""))
            if not res.startswith(REPO_SCHEME):
                continue
            file = resolve_repo_uri(res, repos_root)
            if not file.is_file():
                continue
            if file not in cache:
                cache[file] = git_last_change(file)
            changed, dirty = cache[file]
            if dirty:
                report.warn(c.rel, f"source has uncommitted changes: {res}")
            elif generated_at and changed and changed > generated_at:
                report.warn(c.rel, f"source changed {changed.isoformat()} after generated.at: {res}")


# --------------------------------------------------------------------------- verify


def verify(bundle: Path, pages: list[str], by: str, report: Report) -> None:
    """Mark reviewed pages: add verified {by, at} and move status draft -> stable."""
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for rel in pages:
        path = bundle / rel
        if not path.is_file():
            report.error(rel, "no such page")
            continue
        text = path.read_text(encoding="utf-8")
        head, sep, body = text.partition("\n---\n")
        if not head.startswith("---") or not sep:
            report.error(rel, "no frontmatter")
            continue
        if "\nverified:" in head:
            report.error(rel, "already verified - edit it by hand")
            continue
        lines = head.split("\n")
        at = next((i for i, l in enumerate(lines) if l.startswith("generated:")), len(lines) - 1)
        lines.insert(at + 1, f"verified: {{ by: {by}, at: {now} }}")
        head = "\n".join("status: stable" if l == "status: draft" else l for l in lines)
        path.write_text(head + sep + body, encoding="utf-8")
        print(f"verified {rel}")


# --------------------------------------------------------------------------- main


def main() -> int:
    here = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["validate", "index", "drift", "check", "verify"])
    parser.add_argument("pages", nargs="*", help="verify: bundle-relative page paths")
    parser.add_argument("--by", default="", help="verify: reviewer, e.g. human:chrisfusion")
    parser.add_argument("--bundle", type=Path, default=here / "bundle")
    parser.add_argument("--repos-root", type=Path, default=here.parent,
                        help="directory holding the sibling fusion-* repos (repo:// root)")
    args = parser.parse_args()

    report = Report()
    concepts = validate(args.bundle, args.repos_root, report)
    if args.command == "index":
        write_indexes(args.bundle, concepts, check_only=False, report=report)
    elif args.command == "drift":
        report = Report()  # drift output only
        drift(concepts, args.repos_root, report)
    elif args.command == "verify":
        if not args.pages or not args.by:
            parser.error("verify needs page paths and --by")
        report = Report()
        verify(args.bundle, args.pages, args.by, report)
    elif args.command == "check":
        write_indexes(args.bundle, concepts, check_only=True, report=report)
        drift(concepts, args.repos_root, report)
    report.print()
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
