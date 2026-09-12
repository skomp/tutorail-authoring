#!/usr/bin/env python3
"""Add a lesson to a bundle, or renumber the ones it already has.

Usage:
    lesson.py add <bundle> --id <slug> --title <text>
                           [--after <lesson-path> | --position <n>] [--folder]
                           [--check] [--force]
    lesson.py add <bundle> --id <slug> --title <text> --optional
                           --offer-at <lesson> --offer-because <text>
                           [--anticipates <failure-mode-id>]
                           [--repair-in <lesson>] [--required-for <lesson>]
                           [--folder] [--check] [--force]
    lesson.py renumber <bundle> [--check] [--force]

`--optional` creates a lesson the tutor OFFERS instead of sequencing. Such a
lesson is listed under `optional_lessons` and never under `lessons`, so it
has no position in the main path and therefore no number prefix and no
renumber. The three writes it makes - the lesson file, its `optional: true`
frontmatter and the `optional_lessons` entry - land together or not at all;
check 20 of the runner's validator requires the frontmatter and the list to
agree, so a half-applied run would leave a bundle the runner rejects.

Both subcommands MUTATE the bundle, so both obey the design's three safety
properties:

  * the runner's validator runs against the edited bundle, and a run that is
    not clean is discarded - the bundle is never left broken and reported as
    done;
  * --check does the whole operation on a staging copy, validates it, prints
    what it would do, and throws the copy away;
  * a dirty git working tree under the bundle refuses the run unless --force,
    so `git diff` afterwards is a record of exactly what this tool did.

A failure at any point leaves the bundle byte-identical. The edit happens on
a copy and is swapped in only after the validator passes.

Exit codes:
    0  done (or, with --check, the plan is printable and would validate)
    1  nothing to do
    2  usage, I/O, a refused run, or a validator failure
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import bundlelib as bl
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import bundlelib as bl


# --------------------------------------------------------------------------
# The lesson template
#
# The section list is bundle-format.md section 6, in order. It is deliberately
# a skeleton: the format says a lesson is objectives, constraints and
# completion conditions, not dialogue, and a generator that wrote plausible
# prose would be writing the course. Nothing here trips the validator's
# progress-marker check - no `Status:` label, no ticked box, no `Next:`
# heading - which is why the placeholder wording is what it is.
# --------------------------------------------------------------------------

TEMPLATE = """---
id: {slug}
title: {title}
design_refs: []
validators: []
---

## Purpose

TODO: why this lesson exists and what pressure motivates it. The first line of
this section is what index.py shows, so make it one sentence.

## Prerequisites

TODO: what must already be true. Reference earlier lesson ids.

## Learning objectives

- TODO

## Theory

TODO: the concepts the learner needs. Teach them; do not assume them.

## Concepts to teach

TODO: named concepts the tutor must actually cover, not skip past.

## Constraints

TODO: what the learner's solution must and must not do.

## Suggested progression

TODO: a rough sequence of tasks. Not a script of conversational turns.

## Completion conditions

TODO: checkable conditions. Be specific enough that "looks plausible" is not
enough.

## On completion, persist

TODO: what to record in the instance's DESIGN.md or STATE.md.

## Optional deeper paths

TODO: material available if the learner asks. Not required.
"""


# --------------------------------------------------------------------------
# The one opinion this tool carries
#
# `required_for` on an optional lesson scores -3 in the course-quality rubric
# AND is raised for review, by the owner's decision of 2026-09-12. The flag
# exists because the skill forbids hand-editing tutorial.yaml, so refusing it
# would leave no legitimate way to declare a gate the format permits.
#
# THE TEXT BELOW IS QUOTED VERBATIM from
# skills/course-quality/references/rubric.md, the section "`required_for`
# scores and is raised, both". It is not paraphrased, and it must not be
# edited here alone: tests/test_lesson_add.py reads the rubric and asserts
# these exact lines are in it, so a drift in either direction fails the
# suite rather than leaving the tool teaching something the rubric does not
# say.
# --------------------------------------------------------------------------

RUBRIC_REL = "skills/course-quality/references/rubric.md"

REQUIRED_FOR_WARNING = (
    "This gate cost the course 3 points and may still be correct. If the lesson genuinely",
    "cannot be completed while its failure stands, the gate is doing its job — say so and",
    "keep it. Do not delete a gate to improve a score. A course that drops a justified gate",
    "lets a learner finish a lesson whose failure is still standing, which is worse than the",
    "toil this rubric hunts.",
)


def print_required_for_warning() -> None:
    print()
    print("     --required-for declares a GATE. The course-quality rubric scores it")
    print(f"     -3 and raises it for review. In the rubric's own words ({RUBRIC_REL}):")
    print()
    for line in REQUIRED_FOR_WARNING:
        print(f"       {line}")


def resolve_main_path(bundle: bl.Bundle, value: str, flag: str) -> str:
    """Resolve `value` to an entry of the manifest's `lessons` list.

    An offer point, a repair site and a gate are all places on the MAIN PATH
    (the runner's check 18 says so in those words), so each one must name a
    lesson the runner actually walks. Both spellings an author has in front
    of them are accepted - the manifest entry `lessons/03-x.md` and the bare
    lesson id `03-x` - and anything else is refused rather than written and
    left for the validator to explain in its own vocabulary.
    """
    value = value.strip()
    if value in bundle.listed:
        return value
    index = bundle.by_rel
    by_slug = {
        index[rel].slug: rel for rel in bundle.listed if rel in index
    }
    if value in by_slug:
        return by_slug[value]
    near = [rel for rel in bundle.listed if rel.lower() == value.lower()]
    near += [rel for slug, rel in by_slug.items() if slug.lower() == value.lower()]
    hint = f" Did you mean {near[0]!r}?" if near else ""
    raise bl.ToolError(
        f"{flag} {value!r} is not a lesson on this course's main path, so it "
        f"names no place in tutorial.yaml's lessons list.{hint}\n"
        f"An offer point, a repair site and a gate are all places on the main "
        f"path. Give a lessons entry (lessons/03-x.md) or its lesson id (03-x).\n"
        f"Run  python3 index.py {bundle.root}  to see the list."
    )


def parse_position(bundle: bl.Bundle, after: str | None, position: int | None) -> int:
    listed = bundle.listed
    if after is not None:
        if after not in listed:
            near = [rel for rel in listed if rel.lower() == after.lower()]
            hint = f" Did you mean {near[0]!r}?" if near else ""
            raise bl.ToolError(
                f"--after {after!r} is not an entry in tutorial.yaml's lessons "
                f"list, so there is no position to insert after.{hint}\n"
                f"Run  python3 index.py {bundle.root}  to see the list."
            )
        return listed.index(after) + 1
    if position is not None:
        if position < 0 or position > len(listed):
            raise bl.ToolError(
                f"--position {position} is outside 0..{len(listed)}; the bundle "
                f"has {len(listed)} lessons."
            )
        return position
    return len(listed)


def add(args: argparse.Namespace) -> int:
    # The runner is a hard prerequisite, so establish it BEFORE anything else
    # - before reading the bundle, before the dirty-tree check, and before any
    # early return. `renumber` used to reach its "Nothing to do" exit without
    # ever looking, so on a machine with no runner installed it reported a
    # clean outcome it had not been able to check. Nothing here mutates, so
    # that was not unsafe; it was misleading, which is how a false oracle
    # starts.
    bl.find_validator()
    root = Path(args.bundle)
    bundle = bl.load_bundle(root)
    bl.require_clean_tree(root, args.force)

    given = args.id.strip()
    prefix, body = bl.split_number_prefix(given)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", body):
        raise bl.ToolError(
            f"--id {args.id!r} is not a usable slug. After any leading number "
            f"prefix it must match [a-z0-9]+(-[a-z0-9]+)* - lowercase letters, "
            f"digits and single hyphens."
        )

    offer_flags = {
        "--offer-at": args.offer_at,
        "--offer-because": args.offer_because,
        "--anticipates": args.anticipates,
        "--repair-in": args.repair_in,
        "--required-for": args.required_for,
    }
    if not args.optional:
        used = [flag for flag, value in offer_flags.items() if value]
        if used:
            raise bl.ToolError(
                f"{', '.join(used)} describes when the tutor OFFERS a lesson, "
                f"which only an optional lesson has. Add --optional, or drop "
                f"{'these flags' if len(used) > 1 else 'the flag'}."
            )
        position = parse_position(bundle, args.after, args.position)
        return add_main_path(args, root, bundle, body, position)
    return add_optional(args, root, bundle, given, prefix, body)


def add_optional(
    args: argparse.Namespace,
    root: Path,
    bundle: bl.Bundle,
    given: str,
    prefix: str | None,
    body: str,
) -> int:
    """`add --optional`: a lesson the tutor offers instead of sequencing.

    Three writes, one transaction. The refusals come first and every one of
    them leaves the bundle byte-identical, because nothing is copied until
    bl.Staged opens.
    """
    if args.after is not None or args.position is not None:
        which = "--after" if args.after is not None else "--position"
        raise bl.ToolError(
            f"{which} cannot be combined with --optional. An optional lesson "
            f"has no position: it is offered at the points --offer-at names, "
            f"and it is never an entry in the lessons list."
        )
    missing = [
        flag
        for flag, value in (("--offer-at", args.offer_at), ("--offer-because", args.offer_because))
        if not value
    ]
    if missing:
        raise bl.ToolError(
            f"--optional needs {' and '.join(missing)}, which "
            f"{'are' if len(missing) > 1 else 'is'} missing.\n"
            f"--offer-at names the lessons entry at which the tutor raises the "
            f"offer, and --offer-because is the sentence it says to the learner. "
            f"The format requires both, and nothing incomplete is written: a "
            f"placeholder is safe for a person and invisible to an agent."
        )
    if prefix is not None:
        raise bl.ToolError(
            f"--id {given!r} carries the number prefix {prefix!r}, and an "
            f"optional lesson has none. A number is a position in the main "
            f"path's order, which an optional lesson does not have. Pass "
            f"--id {body}."
        )

    slug = body
    rel = f"lessons/{slug}/LESSON.md" if args.folder else f"lessons/{slug}.md"
    existing = {lesson.slug for lesson in bundle.lessons}
    if slug in existing:
        raise bl.ToolError(
            f"lessons/{slug} already exists. Choose a different --id."
        )
    twin = sorted(s for s in existing if bl.split_number_prefix(s)[1] == body)
    if twin:
        raise bl.ToolError(
            f"a lesson whose slug ends in {body!r} already exists ({twin[0]}). "
            f"Two lessons with the same name differing only in number is a "
            f"rename waiting to collide."
        )

    entry: dict = {
        "offer_at": [resolve_main_path(bundle, v, "--offer-at") for v in args.offer_at],
        "offer_because": args.offer_because,
    }
    if args.anticipates:
        entry["anticipates"] = list(args.anticipates)
    if args.repair_in:
        entry["repair_in"] = resolve_main_path(bundle, args.repair_in, "--repair-in")
    if args.required_for:
        entry["required_for"] = [
            resolve_main_path(bundle, v, "--required-for") for v in args.required_for
        ]

    print(f"add: {rel}   OPTIONAL - offered, not sequenced")
    print(f"     id      {slug}")
    print(f"     title   {args.title}")
    print(f"     form    {'folder' if args.folder else 'single file'}")
    print(f"     offer_at        {', '.join(entry['offer_at'])}")
    print(f"     offer_because   {entry['offer_because']}")
    if "anticipates" in entry:
        print(f"     anticipates     {', '.join(entry['anticipates'])}")
    if "repair_in" in entry:
        print(f"     repair_in       {entry['repair_in']}")
    if "required_for" in entry:
        print(f"     required_for    {', '.join(entry['required_for'])}")
    print(
        f"     note    an optional lesson has no position. It is NOT added to "
        f"tutorial.yaml's\n"
        f"             lessons list, its filename carries no number prefix, and "
        f"no renumber\n"
        f"             is needed or performed."
    )
    if "required_for" in entry:
        print_required_for_warning()

    with bl.Staged(root, check_only=args.check) as stage:
        target = stage.root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        text = TEMPLATE.format(slug=slug, title=args.title)
        # Write 1 and 2 are one file write. Check 20 requires the frontmatter
        # and the optional_lessons list to agree, so they are never apart.
        text, changed = bl.set_frontmatter_field(text, "optional", "true")
        if not changed:
            raise bl.ToolError(
                "the lesson template's frontmatter did not accept "
                "'optional: true'. Nothing was written."
            )
        target.write_text(text, encoding="utf-8")
        manifest_path = stage.root / "tutorial.yaml"
        manifest_text = bl.read_text(manifest_path)
        assert manifest_text is not None
        manifest_path.write_text(
            bl.add_optional_lesson(manifest_text, rel, entry), encoding="utf-8"
        )
        # The lessons list did not move, so this can only REPAIR a template
        # that was already out of step. It is called anyway, for the same
        # reason every other mutating operation calls it.
        first = bundle.listed[0] if bundle.listed else ""
        report_state_template(bl.reconcile_state_template(stage.root, first))
        run = stage.commit()

    _report_validator(run, args.check)
    return 0


def add_main_path(
    args: argparse.Namespace,
    root: Path,
    bundle: bl.Bundle,
    body: str,
    position: int,
) -> int:
    # The width the bundle will need AFTER this lesson joins it, so a later
    # renumber computes the same width and has nothing to repad.
    width = max(bundle.number_width, len(str(len(bundle.listed))))
    slug = f"{position:0{width}d}-{body}"

    existing = {lesson.slug for lesson in bundle.lessons}
    if slug in existing:
        raise bl.ToolError(
            f"lessons/{slug} already exists. Choose a different --id, or a "
            f"different position."
        )
    if body in {bl.split_number_prefix(s)[1] for s in existing}:
        raise bl.ToolError(
            f"a lesson whose slug ends in {body!r} already exists "
            f"({sorted(s for s in existing if bl.split_number_prefix(s)[1] == body)[0]}). "
            f"Two lessons with the same name differing only in number is a "
            f"rename waiting to collide."
        )

    rel = f"lessons/{slug}/LESSON.md" if args.folder else f"lessons/{slug}.md"
    new_listed = list(bundle.listed)
    new_listed.insert(position, rel)

    # The filename prefix follows the list, not the other way round
    # (bundle-format section 8, step 7). Inserting in the middle therefore
    # leaves the prefixes out of sequence until renumber runs, and saying so
    # is more honest than silently renaming 20 files inside an `add`.
    prefixes_out_of_sequence = position != len(bundle.listed)

    print(f"add: {rel}")
    print(f"     id      {slug}")
    print(f"     title   {args.title}")
    print(f"     form    {'folder' if args.folder else 'single file'}")
    print(f"     position {position} of {len(new_listed)} in tutorial.yaml lessons")
    if prefixes_out_of_sequence:
        print(
            f"     note    inserting at {position} leaves the filename prefixes out "
            f"of sequence.\n"
            f"             The lessons list is the authoritative order, so the bundle "
            f"is valid as it stands.\n"
            f"             Run  python3 lesson.py renumber {root}  to make the "
            f"prefixes match the order."
        )

    with bl.Staged(root, check_only=args.check) as stage:
        target = stage.root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            TEMPLATE.format(slug=slug, title=args.title), encoding="utf-8"
        )
        manifest_path = stage.root / "tutorial.yaml"
        manifest_text = bl.read_text(manifest_path)
        assert manifest_text is not None
        manifest_path.write_text(
            bl.replace_lessons_list(manifest_text, new_listed), encoding="utf-8"
        )
        report_state_template(bl.reconcile_state_template(stage.root, new_listed[0]))
        run = stage.commit()

    _report_validator(run, args.check)
    return 0


def report_state_template(changes: list[str]) -> None:
    print()
    if changes:
        print("STATE.template.md brought back in step with tutorial.yaml:")
        for change in changes:
            print(f"    {change}")
    else:
        print("STATE.template.md already agreed with tutorial.yaml; left alone.")


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


# --------------------------------------------------------------------------
# renumber
# --------------------------------------------------------------------------


def renumber_plan(bundle: bl.Bundle) -> tuple[dict[str, str], dict[str, str]]:
    """Return (slug map, path map) for the manifest order.

    The manifest's lessons list is the authoritative order (format section
    2), so the target number of a lesson is its index in that list. A lesson
    on disk that the list does not name has no position and is left alone -
    the validator already reports it as invisible, and inventing a number for
    it would be this tool deciding where it belongs.
    """
    width = bundle.number_width
    slug_map: dict[str, str] = {}
    path_map: dict[str, str] = {}
    index = bundle.by_rel
    for position, rel in enumerate(bundle.listed):
        lesson = index.get(rel)
        if lesson is None:
            continue
        _, body = bl.split_number_prefix(lesson.slug)
        target = f"{position:0{width}d}-{body}"
        if target == lesson.slug:
            continue
        slug_map[lesson.slug] = target
        if lesson.is_folder:
            path_map[f"lessons/{lesson.slug}/LESSON.md"] = f"lessons/{target}/LESSON.md"
        else:
            path_map[f"lessons/{lesson.slug}.md"] = f"lessons/{target}.md"
    return slug_map, path_map


def apply_renames(root: Path, bundle: bl.Bundle, slug_map: dict[str, str]) -> None:
    """Rename every lesson file or folder, in two phases.

    Two phases because a renumber routinely swaps or shifts names: renaming
    03 -> 04 while 04 still exists would clobber it. Everything moves to a
    unique temporary name first, then to its target. The temporary name also
    sidesteps this filesystem's case-insensitivity, where a rename that only
    changes case is a silent no-op.
    """
    lessons_dir = root / "lessons"
    staged: list[tuple[Path, Path]] = []
    for number, lesson in enumerate(bundle.lessons):
        target_slug = slug_map.get(lesson.slug)
        if target_slug is None:
            continue
        source = lesson.folder if lesson.is_folder else lesson.path
        source = lessons_dir / source.name
        temp = lessons_dir / f".tutorail-renumber-{number}"
        final_name = target_slug if lesson.is_folder else f"{target_slug}.md"
        source.rename(temp)
        staged.append((temp, lessons_dir / final_name))
    for temp, final in staged:
        temp.rename(final)


def renumber(args: argparse.Namespace) -> int:
    # The runner is a hard prerequisite, so establish it BEFORE anything else
    # - before reading the bundle, before the dirty-tree check, and before any
    # early return. `renumber` used to reach its "Nothing to do" exit without
    # ever looking, so on a machine with no runner installed it reported a
    # clean outcome it had not been able to check. Nothing here mutates, so
    # that was not unsafe; it was misleading, which is how a false oracle
    # starts.
    bl.find_validator()
    root = Path(args.bundle)
    bundle = bl.load_bundle(root)
    bl.require_clean_tree(root, args.force)

    slug_map, path_map = renumber_plan(bundle)
    if not slug_map:
        print("renumber: the filename prefixes already match the lessons order.")
        print("          Nothing to do.")
        return 1

    print(f"renumber: {len(slug_map)} lesson(s) change number")
    for old, new in slug_map.items():
        print(f"    {old}  ->  {new}")
    print()

    known_ids = {lesson.slug for lesson in bundle.lessons}
    renamed = set(slug_map)

    with bl.Staged(root, check_only=args.check) as stage:
        assert stage.root is not None
        apply_renames(stage.root, bundle, slug_map)

        rewrites: list[bl.Rewrite] = []
        left_alone: list[bl.LeftAlone] = []
        for path in bl.text_files(stage.root):
            text = bl.read_text(path)
            if text is None:
                continue  # binary material; there is no prose to rewrite
            where = path.relative_to(stage.root).as_posix()
            text, path_hits = bl.rewrite_tokens(text, path_map, "path", where)
            text, id_hits = bl.rewrite_tokens(text, slug_map, "id", where)
            hits = path_hits + id_hits
            if hits:
                path.write_text(text, encoding="utf-8")
                rewrites.extend(hits)
            left_alone.extend(
                bl.find_left_alone(text, where, known_ids | set(slug_map.values()), set(slug_map.values()))
            )

        report_rewrites(rewrites, left_alone, renamed)
        # The rewrite pass above already retargets STATE.template.md's
        # active_lesson, because that field holds a full lesson PATH and the
        # path map covers it. This call is the belt to that braces: it proves
        # the field equals lessons[0] afterwards whatever the rewrite did, and
        # it also repairs a template that was out of step before the run.
        new_first = path_map.get(bundle.listed[0], bundle.listed[0]) if bundle.listed else ""
        report_state_template(bl.reconcile_state_template(stage.root, new_first))
        run = stage.commit()

    _report_validator(run, args.check)
    return 0


def report_rewrites(
    rewrites: list[bl.Rewrite], left_alone: list[bl.LeftAlone], renamed: set[str]
) -> None:
    """Print every rewrite, and everything deliberately left alone.

    Design section 9 requires both halves. The rewrites make the change
    reviewable in `git diff` rather than silent; the left-alone list is the
    honest part - a token shaped like a lesson reference that this tool did
    not own is reported, not guessed at.
    """
    by_kind: dict[str, list[bl.Rewrite]] = {}
    for item in rewrites:
        by_kind.setdefault(item.kind, []).append(item)

    print(f"rewrote {len(rewrites)} reference(s):")
    for kind in ("path", "id"):
        items = by_kind.get(kind, [])
        if not items:
            continue
        label = (
            "lesson paths (tutorial.yaml, STATE.template.md, prose that names a file)"
            if kind == "path"
            else "bare lesson ids in prose (Prerequisites: and friends)"
        )
        print(f"  {len(items)} {label}")
        for item in items:
            print(f"    {item.where}  {item.old} -> {item.new}")
    if not rewrites:
        print("  (none)")

    unknown = [item for item in left_alone if item.reason == "unknown"]
    resolves = [item for item in left_alone if item.reason == "resolves"]
    print()
    print("left alone:")
    if resolves:
        names = sorted({item.token for item in resolves})
        print(
            f"  {len(resolves)} reference(s) to {len(names)} lesson(s) this run did "
            f"not renumber: {', '.join(names[:8])}"
            + (" …" if len(names) > 8 else "")
        )
    if unknown:
        print(
            f"  {len(unknown)} token(s) that look like a lesson reference but name no "
            f"lesson in this bundle. Left exactly as they are - check each one:"
        )
        for item in unknown[:40]:
            print(f"    {item.where}  {item.token}")
            print(f"        {bl.clip(item.line, 100)}")
        if len(unknown) > 40:
            print(f"    ... and {len(unknown) - 40} more")
    if not resolves and not unknown:
        print("  (nothing else in the bundle looks like a lesson reference)")


# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="lesson.py", description="Add or renumber lessons in a tutorAIl bundle."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("bundle", help="the bundle directory")
    common.add_argument(
        "--check",
        action="store_true",
        help="do the whole operation on a copy, validate it, print the plan, "
        "and change nothing",
    )
    common.add_argument(
        "--force",
        action="store_true",
        help="run even though the working tree under the bundle is dirty",
    )

    p_add = sub.add_parser("add", parents=[common], help="create a lesson")
    p_add.add_argument("--id", required=True, help="the lesson slug, with or without a number prefix")
    p_add.add_argument("--title", required=True, help="the human-facing lesson title")
    where = p_add.add_mutually_exclusive_group()
    where.add_argument("--after", help="insert after this lessons-list entry")
    where.add_argument("--position", type=int, help="insert at this 0-based position")
    p_add.add_argument(
        "--folder",
        action="store_true",
        help="create lessons/<slug>/LESSON.md instead of lessons/<slug>.md",
    )
    p_add.add_argument(
        "--optional",
        action="store_true",
        help="create a lesson the tutor OFFERS instead of sequencing: listed "
        "under optional_lessons, never in lessons, with no number prefix",
    )
    p_add.add_argument(
        "--offer-at",
        action="append",
        default=[],
        metavar="LESSON",
        help="a lessons entry (or lesson id) at which the tutor raises the "
        "offer. Required with --optional; repeat it for several points",
    )
    p_add.add_argument(
        "--offer-because",
        metavar="TEXT",
        help="the sentence the tutor says when it offers the lesson. Required "
        "with --optional",
    )
    p_add.add_argument(
        "--anticipates",
        action="append",
        default=[],
        metavar="FAILURE-MODE-ID",
        help="a failure_modes id this lesson anticipates; repeatable",
    )
    p_add.add_argument(
        "--repair-in",
        metavar="LESSON",
        help="the lessons entry whose work an anticipated failure damages",
    )
    p_add.add_argument(
        "--required-for",
        action="append",
        default=[],
        metavar="LESSON",
        help="a lessons entry this lesson gates. The course-quality rubric "
        "scores a gate -3 and raises it for review; using this flag prints "
        "the rubric's warning",
    )

    sub.add_parser(
        "renumber",
        parents=[common],
        help="make the filename prefixes match the lessons order",
    )

    args = parser.parse_args(argv)
    if args.command == "add":
        return add(args)
    return renumber(args)


if __name__ == "__main__":
    sys.exit(bl.run_main(main))
