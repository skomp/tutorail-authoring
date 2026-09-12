#!/usr/bin/env python3
"""Build a catalog.yaml for a repository of bundles.

Usage:
    catalog.py <bundles-repo> [-o <path>]

Scans `<bundles-repo>` for bundles, reads each manifest, and writes a
catalogue naming them by RELATIVE path, so the repository can ship its own
catalogue and every bundle travels with it. The default output is
`<bundles-repo>/catalog.yaml`, and `-o -` writes to stdout instead.

`scope` is the one field a catalogue carries that a bundle's tutorial.yaml
does not. It is DERIVED from the length of the manifest's lessons list rather
than invented, and the derivation is printed, because a scope that
under-states the work is a disservice to the learner choosing on it.

The written file is checked with the runner's own catalogue validator
(`validate_bundle.py --catalog --portable`) before this exits. A catalogue
this tool wrote and did not check would be exactly the drift it exists to
prevent.

Exit codes:
    0  written (or printed) and the validator passed
    1  no bundle was found under the given directory
    2  usage, I/O error, or the written catalogue did not validate
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import bundlelib as bl
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import bundlelib as bl


CATALOG_VERSION = 1
MAX_DEPTH = 3

# Derived, not invented. The wording matches the two examples the runner
# already ships - "3 lessons; a few hours" in catalog/builtin.yaml and
# "23 lessons; months of work" in catalogue-format.md - so a generated
# catalogue reads like a hand-written one.
SCOPE_BANDS: tuple[tuple[int, str], ...] = (
    (3, "a few hours"),
    (8, "a few days"),
    (15, "a few weeks"),
    (10**9, "months of work"),
)


def scope_for(lesson_count: int) -> str:
    for ceiling, phrase in SCOPE_BANDS:
        if lesson_count <= ceiling:
            return f"{lesson_count} lesson{'' if lesson_count == 1 else 's'}; {phrase}"
    raise AssertionError  # pragma: no cover - the last band is unbounded


def find_bundles(repo: Path) -> list[Path]:
    """Directories holding both tutorial.yaml and STATE.template.md.

    Both files, because that pair is what the runner's catalogue validator
    checks for (its check 6) and it is what distinguishes a bundle from an
    instance: an instance has STATE.md instead. A repository of bundles that
    accidentally contained a learner's copy must not have it catalogued.
    """
    found: list[Path] = []

    def walk(directory: Path, depth: int) -> None:
        entries = bl.list_dir(directory)
        if "tutorial.yaml" in entries and "STATE.template.md" in entries:
            found.append(directory)
            return  # a bundle holds no bundles
        if depth >= MAX_DEPTH:
            return
        for name in entries:
            if name.startswith("."):
                continue
            child = directory / name
            if child.is_dir() and not child.is_symlink():
                walk(child, depth + 1)

    walk(repo, 0)
    return sorted(found)


def yaml_scalar(value: str) -> str:
    """Quote a scalar when plain style would change its meaning."""
    text = str(value)
    if text == "":
        return '""'
    risky = text[0] in "-?:,[]{}#&*!|>'\"%@`" or text[-1] in " \t"
    risky = risky or any(token in text for token in (": ", " #", "\n"))
    risky = risky or text.lower() in ("true", "false", "null", "yes", "no", "on", "off", "~")
    if risky:
        return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return text


def yaml_list(values: list) -> str:
    return "[" + ", ".join(yaml_scalar(str(v)) for v in values) + "]"


def wrap_description(text: str, indent: str) -> list[str]:
    """A folded block scalar, so a long description stays readable."""
    words = " ".join(str(text).split()).split(" ")
    lines: list[str] = []
    current = indent
    for word in words:
        if current != indent and len(current) + 1 + len(word) > 88:
            lines.append(current)
            current = indent + word
        else:
            current = current + (" " if current != indent else "") + word
    if current != indent:
        lines.append(current)
    return lines


def entry_lines(manifest: dict, relative: str, lesson_count: int) -> list[str]:
    out = [f"  - id: {yaml_scalar(manifest['id'])}"]
    out.append(f"    title: {yaml_scalar(manifest.get('title', ''))}")
    out.append("    description: >")
    out.extend(wrap_description(manifest.get("description", ""), "      "))
    # Field order follows catalogue-format.md section 5, so a generated entry
    # diffs cleanly against a hand-written one.
    for field in ("subjects", "aliases"):
        value = manifest.get(field)
        if isinstance(value, list) and value:
            out.append(f"    {field}: {yaml_list(value)}")
    out.append(f"    level: {yaml_scalar(manifest.get('level', ''))}")
    value = manifest.get("style")
    if isinstance(value, list) and value:
        out.append(f"    style: {yaml_list(value)}")
    # scope is always quoted: it is a phrase with a semicolon in it, and the
    # two examples the runner ships quote it.
    out.append('    scope: "{}"'.format(scope_for(lesson_count).replace('"', '\\"')))
    out.append(f"    workspace_kind: {yaml_scalar(manifest.get('workspace_kind', ''))}")
    out.append("    source:")
    out.append("      type: local")
    out.append(f"      path: {yaml_scalar(relative)}")
    return out


HEADER = """# Catalogue of the bundles in this repository.
#
# GENERATED by tutorail-authoring's catalog.py. Edit the bundles' tutorial.yaml
# files and run it again rather than editing this file, which is overwritten.
#
# Every source.path is RELATIVE to this file's own directory, which is the rule
# for every catalogue: a catalogue's bundles are resolved from the directory
# that holds it. That is what lets this repository be added as a catalogue and
# serve its own bundles.
#
# `scope` has no field in a bundle's tutorial.yaml. It is derived from the
# length of that bundle's lessons list.
"""


def build(repo: Path, catalog_path: Path) -> tuple[str, list[str]]:
    bundles = find_bundles(repo)
    notes: list[str] = []
    blocks: list[list[str]] = []
    seen: dict[str, str] = {}
    for directory in bundles:
        try:
            manifest, _ = bl.load_manifest(directory)
        except bl.ToolError as exc:
            notes.append(f"skipped {directory}: {exc}")
            continue
        identifier = manifest.get("id")
        if not isinstance(identifier, str) or not identifier:
            notes.append(f"skipped {directory}: tutorial.yaml has no usable 'id'")
            continue
        if identifier in seen:
            notes.append(
                f"skipped {directory}: id {identifier!r} is already used by "
                f"{seen[identifier]}; two entries answering to one id make "
                f"precedence undecidable"
            )
            continue
        raw = manifest.get("lessons")
        lessons = [x for x in raw if isinstance(x, str)] if isinstance(raw, list) else []
        if not lessons:
            notes.append(
                f"skipped {directory}: its lessons list is empty, so scope cannot "
                f"be derived and there is nothing to offer a learner"
            )
            continue
        relative = _relative(directory, catalog_path.parent)
        if relative is None:
            notes.append(
                f"skipped {directory}: it is not inside {catalog_path.parent}, so a "
                f"catalogue served from that directory could not reach it"
            )
            continue
        seen[identifier] = str(directory)
        blocks.append(entry_lines(manifest, relative, len(lessons)))
        notes.append(
            f"{identifier}: {len(lessons)} lessons -> scope "
            f"{scope_for(len(lessons))!r}, path {relative!r}"
        )

    body = [HEADER, f"catalog_version: {CATALOG_VERSION}", "tutorials:"]
    for block in blocks:
        body.extend(block)
    return "\n".join(body) + "\n", notes


def _relative(directory: Path, base: Path) -> str | None:
    try:
        return directory.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="catalog.py",
        description="Generate catalog.yaml for a repository of tutorAIl bundles.",
    )
    parser.add_argument("repo", help="the bundles repository")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="where to write it; default <repo>/catalog.yaml, '-' for stdout",
    )
    args = parser.parse_args(argv)

    repo = Path(args.repo)
    if not repo.is_dir():
        raise bl.ToolError(f"{repo}: not a directory.")
    to_stdout = args.output == "-"
    catalog_path = (
        repo / "catalog.yaml" if args.output in (None, "-") else Path(args.output)
    )

    text, notes = build(repo, catalog_path)
    count = text.count("\n  - id:")
    for note in notes:
        print(f"  {note}", file=sys.stderr)
    if count == 0:
        print(
            f"error: no bundle was found under {repo}. A bundle is a directory "
            f"holding both tutorial.yaml and STATE.template.md.",
            file=sys.stderr,
        )
        return 1

    if to_stdout:
        sys.stdout.write(text)
        print(f"  {count} bundle(s); not written (-o -)", file=sys.stderr)
        return 0

    bl.atomic_write_text(catalog_path, text)
    run = bl.run_validator(catalog_path, mode="catalog")
    print(f"  wrote {catalog_path} ({count} bundle(s))", file=sys.stderr)
    print(f"  validator: {run.validator} --catalog --portable", file=sys.stderr)
    print(f"             {run.summary()}", file=sys.stderr)
    if not run.clean:
        for line in run.findings[:25]:
            print(f"    {line}", file=sys.stderr)
        print(
            "error: the catalogue this tool just wrote does not validate. It is on "
            "disk so the findings can be read against it; do not ship it.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(bl.run_main(main))
