#!/usr/bin/env python3
"""Compact index of a bundle, for an interview that must not load the course.

Usage:
    index.py <bundle>

AutomatonDB is 23 lessons and roughly 2,700 lines. An interview about
restructuring one chapter must not begin by reading all of it. This prints
what the interview actually needs - id, title, form, design_refs, validators
and a one-line purpose - and nothing else.

Reads frontmatter only, with one deliberate exception: the first line of each
lesson's `## Purpose` section. The file is streamed and the read stops at that
line, so no lesson body is loaded.

Exit codes:
    0  the index was printed and nothing in it was flagged
    1  the index was printed and at least one item is flagged - an unlisted
       lesson, an id that is not its slug, a dangling design_ref, an
       undeclared validator, a listed lesson with no file, or a malformed
       lesson folder
    2  usage or I/O error

Exit 1 is not a validation verdict. This tool reads frontmatter, so it sees
a subset of what the runner's validator sees and makes no judgement at all
about teaching quality. Run `validate_bundle.py <bundle>` for the
authoritative answer.
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


def frontmatter_of(lesson: bl.Lesson) -> dict:
    text = bl.read_text(lesson.path)
    if text is None:
        return {}
    raw, _ = bl.split_frontmatter(text)
    if raw is None:
        return {}
    try:
        parsed = bl.load_yaml(raw, lesson.rel + " frontmatter")
    except bl.YamlError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def as_names(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).lstrip("#") for item in value]
    if value is None:
        return []
    return [str(value).lstrip("#")]


def build(bundle: bl.Bundle) -> tuple[list[str], int]:
    manifest = bundle.manifest
    ordered = bundle.ordered
    listed = set(bundle.listed)
    # See Bundle.optional: an authored lesson off the main path is accounted
    # for, not reported as UNLISTED. This toolkit does not edit one.
    optional = bundle.optional
    anchors = bundle.design_anchors()
    declared = bundle.declared_validators()

    rows = []
    for lesson in ordered:
        fm = frontmatter_of(lesson)
        rows.append(
            {
                "lesson": lesson,
                "title": str(fm.get("title", "")) or "(no title)",
                "id": str(fm.get("id", "")) or "(no id)",
                "refs": as_names(fm.get("design_refs")),
                "validators": as_names(fm.get("validators")),
                "purpose": bl.purpose_line(lesson.path),
            }
        )

    # Most lessons share one validator set. Printing it once and showing only
    # the per-lesson difference is what keeps this to about two lines a
    # lesson instead of three.
    counts: dict[tuple[str, ...], int] = {}
    for row in rows:
        key = tuple(sorted(row["validators"]))
        counts[key] = counts.get(key, 0) + 1
    common: tuple[str, ...] = ()
    if counts:
        best, times = max(counts.items(), key=lambda kv: (kv[1], len(kv[0])))
        if times > 1 and best:
            common = best

    n_folder = sum(1 for row in rows if row["lesson"].is_folder)
    out: list[str] = []
    out.append(
        f"{manifest.get('id', '(no id)')} — {manifest.get('title', '(no title)')}"
    )
    out.append(
        f"{len(rows)} lessons ({len(rows) - n_folder} file, {n_folder} folder)"
        f" · level {manifest.get('level', '?')}"
        f" · workspace {manifest.get('workspace_kind', '?')}"
        f" · bundle_format {manifest.get('bundle_format', '?')}"
    )
    out.append(
        f"validators declared: {' '.join(sorted(declared)) if declared else '(none)'}"
    )
    out.append(
        f"DESIGN.md anchors ({len(anchors)}): "
        f"{bl.clip(' '.join(sorted(anchors)), 200) if anchors else '(none)'}"
    )
    if common:
        out.append(f"validators on most lessons: {' '.join(common)}  (deltas shown as +/-)")
    out.append("")

    width = max((len(row["id"]) for row in rows), default=10)
    width = min(max(width, 10), 40)
    flagged = 0
    for position, row in enumerate(rows):
        lesson = row["lesson"]
        flags = []
        if lesson.rel not in listed and lesson.rel not in optional:
            flags.append("UNLISTED")
        if row["id"] != lesson.slug:
            flags.append(f"id≠slug({lesson.slug})")
        missing_refs = [r for r in row["refs"] if r not in anchors]
        if missing_refs:
            flags.append("refs-dangle:" + ",".join(missing_refs))
        missing_vals = [v for v in row["validators"] if v not in declared]
        if missing_vals:
            flags.append("val-undeclared:" + ",".join(missing_vals))

        if common:
            have = set(row["validators"])
            delta = [f"+{v}" for v in sorted(have - set(common))]
            delta += [f"-{v}" for v in sorted(set(common) - have)]
            vals = " ".join(delta) if delta else "="
        else:
            vals = ",".join(row["validators"]) or "—"

        # One line per lesson. Long lines cost nothing here - the reader is an
        # interview that must not spend its context on the course - and one
        # line per lesson is what keeps a 23-lesson bundle near 30 lines
        # instead of the 2,700 the lessons themselves are.
        form = "opt" if lesson.rel in optional else lesson.form
        out.append(
            f"{position:>3} {row['id']:<{width}} {form:<6} "
            f"d:{','.join(row['refs']) or '—'} v:{vals}"
            + ("  ⚑ " + " ".join(flags) if flags else "")
            + f"  ·  {bl.clip(row['purpose'] or row['title'], 110)}"
        )

        if flags:
            flagged += 1

    if bundle.problems:
        out.append("")
        out.append("problems found while walking lessons/:")
        out.extend(f"  {problem}" for problem in bundle.problems)
    missing = [rel for rel in bundle.listed if rel not in bundle.by_rel]
    if missing:
        out.append("")
        out.append("lessons listed in tutorial.yaml that are not on disk:")
        out.extend(f"  {rel}" for rel in missing)

    total = flagged + len(bundle.problems) + len(missing)
    if total:
        out.append("")
        out.append(
            f"{total} flagged item(s). This is an INDEX, not a verdict: it reports "
            f"what it can see from frontmatter. Run the runner's validator for the "
            f"authoritative answer."
        )
    return out, total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="index.py", description="Print a compact index of a tutorAIl bundle."
    )
    parser.add_argument("bundle", help="the bundle directory")
    args = parser.parse_args(argv)

    bundle = bl.load_bundle(Path(args.bundle))
    lines, flagged = build(bundle)
    print("\n".join(lines))
    # Exit 1 whenever ANY flag was raised, not only for some of them.
    #
    # This was asymmetric and wrong: a lesson listed in tutorial.yaml but
    # absent from disk exited 1, while a lesson present on disk but absent
    # from the list printed its UNLISTED flag and exited 0. The runner's
    # validator reports BOTH (its check 4), so a bundle the runner refuses
    # came back clean from here - the false-oracle shape this project has
    # been bitten by before. Every flag now counts.
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(bl.run_main(main))
