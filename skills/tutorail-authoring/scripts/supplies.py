#!/usr/bin/env python3
"""Declare the files a bundle hands the learner's workspace.

Usage:
    supplies.py list <bundle>
    supplies.py add  <bundle> --from <path> --to <path> --describe <text>
                              [--lesson <lesson-id>] [--check] [--force]

`supplies:` is the channel a course uses to hand the learner's workspace
files it supplies rather than files the learner is asked to produce. The
runner places them; a lesson must never assign a file copy as a task. This
tool is the only supported way to declare an entry - hand-editing
tutorial.yaml or a lesson's frontmatter is already forbidden in this skill.

Two scopes, and where an entry is declared decides its timing, nothing else:

    manifest scope   tutorial.yaml, top level     placed after materialization,
                                                   before the first lesson opens
    lesson scope     a lesson's frontmatter        placed when that lesson opens,
                                                   before its first task

`add` obeys the three safety properties every mutating script in this
toolkit obeys:

  * the runner's validator runs against the edited bundle, and a run that is
    not clean is discarded - the bundle is never left broken and reported as
    done;
  * --check does the whole operation on a staging copy, validates it, prints
    what it would do, and throws the copy away;
  * a dirty git working tree under the bundle refuses the run unless --force,
    so `git diff` afterwards is a record of exactly what this tool did.

`--lesson` takes a lesson **id** (what `index.py` prints, and the bare
filename slug an author has in front of them), not a path.

Exit codes:
    0  done (list: the index was printed; add: written, or --check validated it)
    2  usage, I/O, a refused run, or a validator failure
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    import bundlelib as bl
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import bundlelib as bl


MANIFEST_TIMING = "placed after materialization, before the first lesson opens"
LESSON_TIMING = "placed when that lesson opens, before its first task"


# --------------------------------------------------------------------------
# add
# --------------------------------------------------------------------------


def _resolve_from(root: Path, from_path: str) -> Path:
    """Resolve `--from` against the bundle root. Raises ToolError if it fails.

    A trailing '/' means "the contents of this directory, recursively" (the
    format's own rule, section 4.1), so it is required to resolve to a
    directory; its absence requires a file.
    """
    if not from_path:
        raise bl.ToolError("--from must not be empty.")
    is_dir_form = from_path.endswith("/")
    stripped = from_path[:-1] if is_dir_form else from_path
    if not stripped:
        raise bl.ToolError(f"--from {from_path!r} does not name a path.")
    resolved, reason = bl.resolve_exact(root, stripped)
    if resolved is None:
        raise bl.ToolError(
            f"--from {from_path!r} does not exist in the bundle ({reason})."
        )
    if is_dir_form and not resolved.is_dir():
        raise bl.ToolError(
            f"--from {from_path!r} ends with '/', which means a directory, but "
            f"{stripped} is a file, not a directory."
        )
    if not is_dir_form and resolved.is_dir():
        raise bl.ToolError(
            f"--from {from_path!r} names a directory. Add a trailing '/' to "
            f"supply its contents recursively."
        )
    return resolved


def _validate_to(to: str) -> None:
    """Refuse a `--to` that would escape the workspace or reach `tutorial/`."""
    if to == ".":
        return
    if not to:
        raise bl.ToolError("--to must not be empty; use '.' for the workspace root.")
    if os.path.isabs(to):
        raise bl.ToolError(
            f"--to {to!r} is absolute; it must be relative to the workspace root."
        )
    if "\\" in to:
        raise bl.ToolError(f"--to {to!r} uses a backslash; use '/' in bundle paths.")
    stripped = to[:-1] if to.endswith("/") else to
    parts = stripped.split("/")
    for part in parts:
        if part in ("", ".", ".."):
            raise bl.ToolError(
                f"--to {to!r} is not a safe workspace path: the component "
                f"{part!r} is not allowed. It must not escape the workspace root."
            )
    if parts[0] == "tutorial":
        raise bl.ToolError(
            f"--to {to!r} begins with 'tutorial/'. Placement never reaches "
            f"inside tutorial/ - the instance is not the workspace."
        )


def _resolve_lesson(bundle: bl.Bundle, lesson_id: str) -> bl.Lesson:
    """Resolve `--lesson` against the bundle's lesson slugs.

    `--lesson` is an id, not a path - the same thing an author has in front
    of them and what index.py prints. A lesson on disk that the manifest
    lists in neither `lessons` nor `optional_lessons` is refused too: a
    lesson in either list is a real lesson (section 2, 6, 12, 13 of
    bundle-format.md), "listed exactly once in `lessons`" has not been true
    since optional lessons landed, and this tool must not reject one just
    because it lives off the main path.
    """
    by_slug = {lesson.slug: lesson for lesson in bundle.lessons}
    lesson = by_slug.get(lesson_id)
    if lesson is None:
        near = [slug for slug in by_slug if slug.lower() == lesson_id.lower()]
        hint = f" Did you mean {near[0]!r}?" if near else ""
        raise bl.ToolError(
            f"--lesson {lesson_id!r} does not name a lesson in this bundle.{hint}\n"
            f"Run  python3 index.py {bundle.root}  to see the lesson ids."
        )
    known = set(bundle.listed) | bundle.optional
    if lesson.rel not in known:
        raise bl.ToolError(
            f"--lesson {lesson_id!r} exists on disk ({lesson.rel}) but is not "
            f"listed in tutorial.yaml's lessons: or optional_lessons:, so it is "
            f"not part of this bundle."
        )
    return lesson


def _existing_frontmatter_supplies(text: str, where: str) -> list:
    fm, _ = bl.split_frontmatter(text)
    if fm is None:
        return []
    try:
        parsed = bl.load_yaml(fm, where + " frontmatter")
    except bl.YamlError:
        return []
    existing = parsed.get("supplies") if isinstance(parsed, dict) else None
    return existing if isinstance(existing, list) else []


def _print_plan(entry: dict, lesson: bl.Lesson | None) -> None:
    if lesson is None:
        scope = f"manifest scope, {MANIFEST_TIMING}"
    else:
        scope = f"lesson scope: {lesson.slug}, {LESSON_TIMING}"
    print(f"add: supplies entry ({scope})")
    print(f"     from     {entry['from']}")
    print(f"     to       {entry['to']}")
    print(f"     describe {entry['describe']}")


def _report_validator(run: bl.ValidatorRun, check_only: bool) -> None:
    print()
    print(f"validator: {run.validator}  ({run.how})")
    print(f"           {run.summary()}")
    if check_only:
        print()
        print("--check: nothing was written. The plan above validates.")
    else:
        print()
        print("written. `git diff` now shows exactly this change.")


def add(args: argparse.Namespace) -> int:
    # The runner is a hard prerequisite, so establish it BEFORE anything else
    # - before reading the bundle, before the dirty-tree check, and before
    # any early return, exactly as lesson.py add does. A machine with no
    # runner installed must not reach a clean-looking exit.
    bl.find_validator()
    root = Path(args.bundle)
    bundle = bl.load_bundle(root)
    bl.require_clean_tree(root, args.force)

    describe = args.describe.strip()
    if not describe:
        raise bl.ToolError(
            "--describe must not be empty; it is the sentence the runner says "
            "to the learner."
        )

    lesson: bl.Lesson | None = None
    if args.lesson:
        lesson = _resolve_lesson(bundle, args.lesson)

    _resolve_from(root, args.from_)
    _validate_to(args.to)

    entry = {"from": args.from_, "to": args.to, "describe": describe}

    if lesson is not None:
        text = bl.read_text(lesson.path)
        assert text is not None
        existing = _existing_frontmatter_supplies(text, lesson.rel)
        where = f"lesson {lesson.slug}'s frontmatter"
    else:
        existing_raw = bundle.manifest.get("supplies")
        existing = existing_raw if isinstance(existing_raw, list) else []
        where = "tutorial.yaml"

    if entry in existing:
        raise bl.ToolError(
            f"this exact supplies entry is already declared in {where}:\n"
            f"    from     {entry['from']}\n"
            f"    to       {entry['to']}\n"
            f"    describe {entry['describe']}\n"
            f"Nothing to add."
        )

    _print_plan(entry, lesson)

    with bl.Staged(root, check_only=args.check) as stage:
        if lesson is not None:
            target_path = stage.root / lesson.rel
            target_text = bl.read_text(target_path)
            assert target_text is not None
            new_text = bl.add_supplies(target_text, entry, frontmatter=True)
            target_path.write_text(new_text, encoding="utf-8")
        else:
            manifest_path = stage.root / "tutorial.yaml"
            manifest_text = bl.read_text(manifest_path)
            assert manifest_text is not None
            new_text = bl.add_supplies(manifest_text, entry, frontmatter=False)
            manifest_path.write_text(new_text, encoding="utf-8")
        run = stage.commit()

    _report_validator(run, args.check)
    return 0


# --------------------------------------------------------------------------
# list
# --------------------------------------------------------------------------


def list_cmd(args: argparse.Namespace) -> int:
    root = Path(args.bundle)
    bundle = bl.load_bundle(root)

    manifest_raw = bundle.manifest.get("supplies")
    manifest_supplies = manifest_raw if isinstance(manifest_raw, list) else []

    entries: list[tuple[str, bl.Lesson | None, dict]] = []
    for item in manifest_supplies:
        if isinstance(item, dict):
            entries.append(("manifest", None, item))

    for lesson in bundle.ordered:
        text = bl.read_text(lesson.path)
        if text is None:
            continue
        lesson_supplies = _existing_frontmatter_supplies(text, lesson.rel)
        for item in lesson_supplies:
            if isinstance(item, dict):
                entries.append(("lesson", lesson, item))

    if not entries:
        print(f"{root}: no supplies declared, in the manifest or in any lesson.")
        return 0

    plural = "y" if len(entries) == 1 else "ies"
    print(f"{root}: {len(entries)} supplies entr{plural} declared")
    print()
    for scope, lesson, item in entries:
        if scope == "manifest":
            print(f"[manifest]  {MANIFEST_TIMING}")
        else:
            assert lesson is not None
            print(f"[lesson {lesson.slug}]  {LESSON_TIMING}")
        print(f"    from     {item.get('from', '')}")
        print(f"    to       {item.get('to', '')}")
        print(f"    describe {item.get('describe', '')}")
        print()
    return 0


# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="supplies.py",
        description="Declare the files a bundle hands the learner's workspace.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="print every declared supplies entry")
    p_list.add_argument("bundle", help="the bundle directory")

    p_add = sub.add_parser("add", help="declare a new supplies entry")
    p_add.add_argument("bundle", help="the bundle directory")
    p_add.add_argument(
        "--from",
        dest="from_",
        required=True,
        help="path relative to the bundle root; a trailing '/' means the "
        "directory's contents, recursively",
    )
    p_add.add_argument(
        "--to",
        required=True,
        help="path relative to the workspace root; '.' is the workspace root itself",
    )
    p_add.add_argument(
        "--describe",
        required=True,
        help="one line, in the author's words, naming what these files are",
    )
    p_add.add_argument(
        "--lesson",
        help="a lesson id: declare in that lesson's frontmatter instead of "
        "the manifest",
    )
    p_add.add_argument(
        "--check",
        action="store_true",
        help="do the whole operation on a copy, validate it, print the plan, "
        "and change nothing",
    )
    p_add.add_argument(
        "--force",
        action="store_true",
        help="run even though the working tree under the bundle is dirty",
    )

    args = parser.parse_args(argv)
    if args.command == "add":
        return add(args)
    return list_cmd(args)


if __name__ == "__main__":
    sys.exit(bl.run_main(main))
