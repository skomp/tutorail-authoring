#!/usr/bin/env python3
"""`lesson.py add` - the operation that creates a lesson.

Stdlib only, no pytest: `python3 tests/test_lesson_add.py`.

Three habits run through this file, and each is a rule this project has
already paid for once:

  * every failure is shown FIRING, and every refusal has a POSITIVE CONTROL
    beside it - the same probe, on an input that differs only in the thing
    under test, reporting the opposite. A refusal that fires for the wrong
    reason looks identical to one that fires for the right reason;
  * no filename is asserted with `.exists()`. THIS FILESYSTEM IS
    CASE-INSENSITIVE, so `(folder / "LESSON.md").exists()` is True for a
    folder holding `lesson.md`. Every filename assertion goes through
    `listing()` / `has_exactly()`, and the folder case also asserts
    `has_miscased(...) is None`;
  * every refusal is followed by a `tree_digest` comparison, not by "the new
    file is absent". A half-written tutorial.yaml would pass the weaker
    check. The digest oracle itself is shown FIRING in case 5, where a real
    add changes it - otherwise "the digest matched" would be unfalsifiable.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    FIXTURES,
    LESSON,
    Run,
    Workspace,
    case,
    check,
    check_in,
    check_not_in,
    has_exactly,
    has_miscased,
    git_init,
    listing,
    note,
    report,
    run,
    tree_digest,
    write_stub_validator,
)

import bundlelib as bl  # noqa: E402  (harness put SCRIPTS on sys.path)


# --------------------------------------------------------------------------
# Reading the bundle back the way a consumer would
# --------------------------------------------------------------------------


def frontmatter(path: Path) -> dict:
    """The lesson's frontmatter as a mapping. Parsed, never regexed.

    The brief is explicit that `id` must equal the slug EXACTLY. A loose
    regex over the whole file would also match the slug where it appears in
    prose, so this splits the frontmatter and parses it - the same two steps
    the runner's validator takes.
    """
    text = path.read_text(encoding="utf-8")
    raw, _body = bl.split_frontmatter(text)
    if raw is None:
        return {}
    parsed = bl.load_yaml(raw, str(path))
    return parsed if isinstance(parsed, dict) else {}


def manifest_lessons(bundle: Path) -> list[str]:
    """tutorial.yaml's `lessons` list, as the YAML reader sees it."""
    manifest, _text = bl.load_manifest(bundle)
    raw = manifest.get("lessons")
    return [x for x in raw if isinstance(x, str)] if isinstance(raw, list) else []


def manifest_id(bundle: Path) -> str:
    manifest, _text = bl.load_manifest(bundle)
    return str(manifest.get("id"))


def manifest_optional(bundle: Path) -> dict:
    """tutorial.yaml's `optional_lessons` map, as the YAML reader sees it."""
    manifest, _text = bl.load_manifest(bundle)
    raw = manifest.get("optional_lessons")
    return raw if isinstance(raw, dict) else {}


def numbered_twins(directory: Path, body: str) -> list[str]:
    """Listing entries that are `<digits>-<body>` - the prefix that must not
    appear on an optional lesson. By listing, never by exists()."""
    return [
        name
        for name in listing(directory)
        if re.fullmatch(rf"\d+-{re.escape(body)}(?:\.md)?", name)
    ]


def validate(bundle: Path) -> Run:
    """Run the runner's own validator against `bundle`.

    The path is discovered through bundlelib.find_validator(), never
    hardcoded: a test that pinned a path would pass on this machine and say
    nothing about the search the tool actually performs.
    """
    validator, _how = bl.find_validator()
    return run(validator, bundle)


def add(bundle: Path, *args: str, env: dict | None = None) -> Run:
    return run(LESSON, "add", bundle, *args, env=env)


# The fixture's own lessons list, read from the fixture rather than retyped,
# so "the other 23 entries survived in order" is checked against the truth.
ORIGINAL = manifest_lessons(FIXTURES / "rust-automaton-db")


# --------------------------------------------------------------------------
# The bootstrap scaffold: a brand-new course with no lessons yet
#
# Such a bundle is INVALID per bundle-format section 9 (`lessons` must be
# non-empty), and `add` is the only way to give it its first lesson - so the
# tool must accept it. The manifest carries every field check 8 requires.
# --------------------------------------------------------------------------

SCAFFOLD_MANIFEST = """bundle_format: 1
id: brand-new-course
title: A Brand New Course
description: >
  A scaffold with no lessons yet, used to prove that `lesson.py add` can
  create the very first lesson of a course.
subjects: [testing]
aliases: [scaffold]
level: beginner
style: [exercise-based]

{lessons_line}

workspace_kind: none
tutor_owned: [tutorial/STATE.md, tutorial/DESIGN.md]
learner_owned: []
ownership_policy: tutor-must-not-edit-learner-owned

validators:
  manual: { kind: manual }

one_task_at_a_time: true
solution_code: on-request-only
advance_on: validated-evidence-only
"""

SCAFFOLD_COURSE = """# A Brand New Course

A scaffold used to prove that `lesson.py add` can create the first lesson.

## What you will build

Nothing yet. The course has no lessons.
"""

SCAFFOLD_DESIGN = """# Design

## Scope {#scope}

The course has no lessons yet.
"""

SCAFFOLD_STATE = """---
tutorial_id: brand-new-course
active_lesson: lessons/00-placeholder.md
status: not-started
updated: null
---

## Last completed task

None. The course has not started.

## Concepts demonstrated

None yet.

## Decisions made in discussion

None yet.

## Known intentional or incomplete state

None yet.

## Accepted warnings

None.

## Next task

Begin the first lesson.

## Deferred items

None.
"""


def scaffold(root: Path, lessons_line: str) -> Path:
    """Write a brand-new-course bundle whose lessons list is `lessons_line`.

    `.format()` is not used on SCAFFOLD_MANIFEST as a whole because the
    validators block contains literal braces; the one substitution is done by
    replace instead.
    """
    root.mkdir(parents=True, exist_ok=True)
    (root / "lessons").mkdir(exist_ok=True)
    (root / "tutorial.yaml").write_text(
        SCAFFOLD_MANIFEST.replace("{lessons_line}", lessons_line), encoding="utf-8"
    )
    (root / "COURSE.md").write_text(SCAFFOLD_COURSE, encoding="utf-8")
    (root / "DESIGN.md").write_text(SCAFFOLD_DESIGN, encoding="utf-8")
    (root / "STATE.template.md").write_text(SCAFFOLD_STATE, encoding="utf-8")
    return root


def bootstrap_case(label: str, lessons_line: str, invalid_because: str) -> None:
    """Cases 8 and 9: the first lesson of a course, two scaffold shapes.

    `invalid_because` differs between the two shapes and that is not
    incidental: `lessons: []` parses to an empty list and trips check 9,
    while a bare `lessons:` parses to None and trips check 8's required-field
    test. Asserting the exact finding is what stops this positive control
    from passing on a bundle that is invalid for some unrelated reason.
    """
    with Workspace() as ws:
        bundle = scaffold(ws.path("new-course"), lessons_line)

        # POSITIVE CONTROL for the validator probe used below. If this
        # scaffold already validated, "valid afterwards" would prove nothing
        # about the add - the probe has to be shown reporting the opposite on
        # the input that differs only by the missing lesson.
        before = validate(bundle)
        check(before.returncode != 0, f"{label}: the empty scaffold is invalid before the add")
        check_in(
            invalid_because,
            before.output,
            f"{label}: and it is invalid for the reason we think it is",
        )

        result = add(bundle, "--id", "first-steps", "--title", "First steps")
        check(result.returncode == 0, f"{label}: add creates the first lesson (exit 0)")

        after = validate(bundle)
        check(after.returncode == 0, f"{label}: the bundle validates after the add")

        entries = manifest_lessons(bundle)
        check(
            entries == ["lessons/00-first-steps.md"],
            f"{label}: the manifest holds exactly the new entry, not {entries!r}",
        )
        text = (bundle / "tutorial.yaml").read_text(encoding="utf-8")
        check(
            "\nlessons:\n  - lessons/00-first-steps.md\n" in text,
            f"{label}: the list is written in BLOCK form, not reformatted to flow",
        )
        check(
            has_exactly(bundle / "lessons", "00-first-steps.md"),
            f"{label}: lessons/ holds 00-first-steps.md by directory listing",
        )
        state = frontmatter(bundle / "STATE.template.md")
        check(
            state.get("active_lesson") == "lessons/00-first-steps.md",
            f"{label}: active_lesson points at the new lessons[0], not "
            f"{state.get('active_lesson')!r}",
        )


def refusal(
    label: str,
    bundle: Path,
    args: tuple[str, ...],
    needle: str,
    env: dict | None = None,
) -> Run:
    """Run `add` expecting a refusal, and prove the bundle did not move.

    The digest is taken immediately before the run, so any setup the caller
    did (dirtying a file, rewriting the manifest) is part of the baseline.
    """
    before = tree_digest(bundle)
    result = add(bundle, *args, env=env)
    check(result.returncode != 0, f"{label}: exits non-zero")
    check_in(needle, result.output, f"{label}: says what the author can act on")
    check(
        tree_digest(bundle) == before,
        f"{label}: the bundle is byte-identical afterwards",
    )
    return result


# --------------------------------------------------------------------------
# A. Happy paths
# --------------------------------------------------------------------------


def case_append() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        result = add(
            bundle, "--id", "deployment-story", "--title", "Deployment and operations"
        )
        check(result.returncode == 0, "append: exit 0")

        check(
            has_exactly(bundle / "lessons", "23-deployment-story.md"),
            "append: lessons/ holds 23-deployment-story.md by directory listing",
        )
        fm = frontmatter(bundle / "lessons" / "23-deployment-story.md")
        check(
            fm.get("id") == "23-deployment-story",
            f"append: frontmatter id is the numbered slug, not {fm.get('id')!r}",
        )
        check(
            fm.get("title") == "Deployment and operations",
            f"append: frontmatter title is what was passed, not {fm.get('title')!r}",
        )
        check(
            fm.get("design_refs") == [] and fm.get("validators") == [],
            "append: the template's design_refs and validators are empty lists",
        )

        entries = manifest_lessons(bundle)
        check(len(entries) == 24, f"append: the manifest has 24 entries, not {len(entries)}")
        check(
            entries[-1] == "lessons/23-deployment-story.md",
            f"append: the new path is LAST in the lessons list, not {entries[-1]!r}",
        )
        check(
            entries[:23] == ORIGINAL,
            "append: the original 23 entries survive unchanged and in order",
        )

        check_in("PASS", result.output, "append: the output reports the validator PASSED")
        # The out-of-sequence warning must be conditional. Case 3 shows it
        # firing; this is the same probe reporting the opposite on the input
        # that differs only by the insert position.
        check_not_in(
            "out of sequence",
            result.output,
            "append: no renumber warning, because appending keeps the prefixes in step",
        )


def case_folder() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        result = add(
            bundle, "--id", "materials-demo", "--title", "A lesson with material",
            "--folder",
        )
        check(result.returncode == 0, "--folder: exit 0")

        folder = bundle / "lessons" / "23-materials-demo"
        check(
            has_exactly(bundle / "lessons", "23-materials-demo"),
            "--folder: lessons/ holds the 23-materials-demo entry by listing",
        )
        check(folder.is_dir(), "--folder: the new entry is a directory")
        check(
            has_exactly(folder, "LESSON.md"),
            f"--folder: the folder holds an entry named exactly LESSON.md, "
            f"listing is {listing(folder)!r}",
        )
        # On this case-insensitive filesystem a mis-cased body resolves
        # through exists() and through open(), so it would be invisible to
        # every check except a listing comparison. bundle-format section 6
        # requires the exact name; assert no other-cased twin is what proves
        # the exact name was actually written.
        check(
            has_miscased(folder, "LESSON.md") is None,
            f"--folder: no differently-cased LESSON.md twin "
            f"({has_miscased(folder, 'LESSON.md')!r})",
        )
        # POSITIVE CONTROL for that probe. `has_miscased(...) is None` is the
        # one assertion in this file that is guaranteed to pass if the probe
        # is broken, so build the thing it must detect - a folder whose body
        # is named `lesson.md` - and show it reported. Both names cannot
        # coexist here, which is precisely why exists() cannot see this.
        decoy = ws.path("decoy-lesson-folder")
        decoy.mkdir()
        (decoy / "lesson.md").write_text("# mis-cased body\n", encoding="utf-8")
        check(
            has_miscased(decoy, "LESSON.md") == "lesson.md",
            f"--folder control: has_miscased DOES report a mis-cased body "
            f"({has_miscased(decoy, 'LESSON.md')!r})",
        )
        check(
            not has_exactly(decoy, "LESSON.md"),
            "--folder control: and has_exactly refuses it, where exists() would not",
        )
        check(
            (decoy / "LESSON.md").exists(),
            "--folder control: exists() really is fooled here - the reason for listing()",
        )
        check(
            listing(folder) == ["LESSON.md"],
            "--folder: the folder holds the body and nothing else",
        )

        entries = manifest_lessons(bundle)
        check(
            entries[-1] == "lessons/23-materials-demo/LESSON.md",
            f"--folder: the manifest entry is the LESSON.md path, not {entries[-1]!r}",
        )
        fm = frontmatter(folder / "LESSON.md")
        check(
            fm.get("id") == "23-materials-demo",
            f"--folder: the id is the FOLDER name, not {fm.get('id')!r}",
        )
        check_in("PASS", result.output, "--folder: the output reports the validator PASSED")


def case_position() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        result = add(bundle, "--id", "interlude", "--title", "An interlude", "--position", "3")
        check(result.returncode == 0, "--position 3: exit 0")

        entries = manifest_lessons(bundle)
        check(len(entries) == 24, f"--position 3: 24 entries, not {len(entries)}")
        check(
            entries[3] == "lessons/03-interlude.md",
            f"--position 3: the new entry sits at index 3, not {entries[3]!r}",
        )
        check(
            entries[2] == "lessons/02-typed-keys-table-hierarchy.md",
            f"--position 3: the entry before it is unchanged, not {entries[2]!r}",
        )
        check(
            entries[4] == "lessons/03-first-refactor.md",
            f"--position 3: the displaced entry follows it, not {entries[4]!r}",
        )
        check(
            has_exactly(bundle / "lessons", "03-interlude.md"),
            "--position 3: the file is named 03-interlude.md by directory listing",
        )
        # An insert in the middle deliberately leaves the filename prefixes
        # out of step with the list. Saying so, and naming the fix, is the
        # documented behaviour - silence here would be the tool hiding a
        # 20-file rename it decided not to do.
        check_in(
            "out of sequence",
            result.output,
            "--position 3: the output warns the prefixes are out of sequence",
        )
        check_in(
            "renumber",
            result.output,
            "--position 3: the output names renumber as the fix",
        )


def case_after() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        result = add(
            bundle,
            "--id",
            "keyed-interlude",
            "--title",
            "A keyed interlude",
            "--after",
            "lessons/02-typed-keys-table-hierarchy.md",
        )
        check(result.returncode == 0, "--after: exit 0")
        entries = manifest_lessons(bundle)
        check(
            entries[3] == "lessons/03-keyed-interlude.md",
            f"--after: inserted at index 3, not {entries[3]!r}",
        )
        check(
            entries[2] == "lessons/02-typed-keys-table-hierarchy.md",
            "--after: the named entry is still at index 2",
        )
        check(len(entries) == 24, "--after: 24 entries")
        check_in("PASS", result.output, "--after: the output reports the validator PASSED")


def case_check() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        before = tree_digest(bundle)
        result = add(bundle, "--id", "dry-run", "--title", "A dry run", "--check")
        after = tree_digest(bundle)

        check(result.returncode == 0, "--check: exit 0")
        check(after == before, "--check: the bundle is byte-identical afterwards")
        check_in("add: lessons/23-dry-run.md", result.output, "--check: the plan is printed")
        check_in("PASS", result.output, "--check: the output reports the validator PASSED")
        check_in(
            "nothing was written",
            result.output,
            "--check: the output says nothing was written",
        )
        check(
            not has_exactly(bundle / "lessons", "23-dry-run.md"),
            "--check: lessons/ does not hold the planned file",
        )

        # POSITIVE CONTROL for the digest oracle itself. "the digest matched"
        # is worthless unless the same probe can be shown reporting a
        # difference; the identical command WITHOUT --check must move it.
        real = add(bundle, "--id", "dry-run", "--title", "A dry run")
        check(real.returncode == 0, "--check control: the same add without --check succeeds")
        check(
            tree_digest(bundle) != before,
            "--check control: the digest DOES change for a real add, so it can fire",
        )
        check(
            has_exactly(bundle / "lessons", "23-dry-run.md"),
            "--check control: and the file the plan described IS written this time",
        )


# --------------------------------------------------------------------------
# B. STATE.template.md maintenance (bundle-format section 5)
# --------------------------------------------------------------------------


def case_state_changed() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        before = (bundle / "STATE.template.md").read_bytes()
        result = add(bundle, "--id", "prelude", "--title", "A prelude", "--position", "0")
        check(result.returncode == 0, "--position 0: exit 0")

        entries = manifest_lessons(bundle)
        check(
            entries[0] == "lessons/00-prelude.md",
            f"--position 0: the new lesson is lessons[0], not {entries[0]!r}",
        )
        state = frontmatter(bundle / "STATE.template.md")
        check(
            state.get("active_lesson") == entries[0],
            f"--position 0: active_lesson equals the new lessons[0], not "
            f"{state.get('active_lesson')!r}",
        )
        check(
            state.get("tutorial_id") == manifest_id(bundle),
            "--position 0: tutorial_id still equals the manifest id",
        )
        check(
            state.get("status") == "not-started",
            "--position 0: status is left at not-started",
        )
        # The reported change is the point: a silent edit to a file the author
        # never touched is exactly what the design forbids.
        check_in(
            "STATE.template.md brought back in step",
            result.output,
            "--position 0: the tool REPORTS that it changed STATE.template.md",
        )
        check_in(
            "'lessons/00-foundations.md' -> 'lessons/00-prelude.md'",
            result.output,
            "--position 0: the report names the old and the new active_lesson",
        )
        # The runner's check 12 enforces active_lesson == lessons[0]. A PASS
        # here is what separates "the tool fixed it" from "the tool broke it
        # and the failure surfaced somewhere unrelated".
        check_in("PASS", result.output, "--position 0: the validator PASSED afterwards")
        # POSITIVE CONTROL for the byte comparison used in the next case: the
        # same probe must be able to report a difference.
        check(
            (bundle / "STATE.template.md").read_bytes() != before,
            "--position 0 control: the STATE bytes DID change, so the byte probe can fire",
        )


def case_state_unchanged() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        before = (bundle / "STATE.template.md").read_bytes()
        result = add(bundle, "--id", "epilogue", "--title", "An epilogue")
        check(result.returncode == 0, "append: exit 0 (STATE case)")

        after = (bundle / "STATE.template.md").read_bytes()
        check(
            after == before,
            "append: STATE.template.md is byte-identical - an append never moves lessons[0]",
        )
        state = frontmatter(bundle / "STATE.template.md")
        check(
            state.get("active_lesson") == manifest_lessons(bundle)[0]
            == "lessons/00-foundations.md",
            "append: active_lesson still equals lessons[0]",
        )
        check_in(
            "left alone",
            result.output,
            "append: the tool says it left STATE.template.md alone",
        )
        check_not_in(
            "brought back in step",
            result.output,
            "append: and does not claim a change it did not make",
        )


# --------------------------------------------------------------------------
# D. Failures, each shown firing
# --------------------------------------------------------------------------


def case_slug_exists() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        # --position 0 makes the generated slug 00-foundations, which is the
        # slug of an existing lesson. This is the exact-slug branch; the
        # same-body branch is case 11.
        refusal(
            "duplicate slug",
            bundle,
            ("--id", "foundations", "--title", "Again", "--position", "0"),
            "lessons/00-foundations already exists",
        )
        # POSITIVE CONTROL: the same command at the same position, differing
        # only in the slug body, is accepted. So the refusal is about the
        # duplicate, not about --position 0.
        ok = add(bundle, "--id", "groundwork", "--title", "Again", "--position", "0")
        check(ok.returncode == 0, "duplicate slug control: a free slug at position 0 is accepted")


def case_same_body_other_number() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        result = refusal(
            "same body, different number",
            bundle,
            ("--id", "99-foundations", "--title", "Foundations again"),
            "rename waiting to collide",
        )
        check_in(
            "(00-foundations)",
            result.output,
            "same body, different number: the message names the lesson it collides with",
        )
        # POSITIVE CONTROL: the same shape of --id - a number prefix the tool
        # discards, plus a body - is accepted when the body is free. The
        # refusal is therefore about the body, not about the prefix.
        ok = add(bundle, "--id", "99-fresh-body", "--title", "Fresh")
        check(ok.returncode == 0, "same body control: 99-fresh-body is accepted")
        check(
            manifest_lessons(bundle)[-1] == "lessons/23-fresh-body.md",
            "same body control: the given 99- prefix is replaced by the position",
        )


def case_bad_slug() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        refusal(
            "slug with spaces",
            bundle,
            ("--id", "Not A Slug", "--title", "Nope"),
            "is not a usable slug",
        )
        refusal(
            "slug with underscores",
            bundle,
            ("--id", "has_underscores", "--title", "Nope"),
            "is not a usable slug",
        )
        refusal(
            "slug with a trailing hyphen",
            bundle,
            ("--id", "trailing-", "--title", "Nope"),
            "is not a usable slug",
        )
        # POSITIVE CONTROL: the SAME three words, separated by hyphens
        # instead of spaces. Only the separator differs, so this proves the
        # refusal is the slug rule firing and not the words.
        ok = add(bundle, "--id", "not-a-slug", "--title", "Nope")
        check(ok.returncode == 0, "bad slug control: not-a-slug is accepted")
        check(
            has_exactly(bundle / "lessons", "23-not-a-slug.md"),
            "bad slug control: and the file is written",
        )


def case_after_unknown() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        refusal(
            "--after an unlisted path",
            bundle,
            ("--id", "orphan", "--title", "Orphan", "--after", "lessons/99-nowhere.md"),
            "is not an entry in tutorial.yaml's lessons list",
        )
        # A mis-cased --after must ALSO be refused. On this filesystem the
        # path resolves, so a tool that checked the disk instead of the list
        # would silently accept it and write a manifest entry that fails on
        # Linux. The "Did you mean" hint is the proof it compared against the
        # list, exact-case.
        miscased = refusal(
            "--after a mis-cased path",
            bundle,
            (
                "--id",
                "orphan",
                "--title",
                "Orphan",
                "--after",
                "lessons/02-Typed-Keys-Table-Hierarchy.md",
            ),
            "is not an entry in tutorial.yaml's lessons list",
        )
        check_in(
            "Did you mean 'lessons/02-typed-keys-table-hierarchy.md'?",
            miscased.output,
            "--after a mis-cased path: the message offers the exact-case entry",
        )
        # POSITIVE CONTROL: the correctly-cased path is accepted, so the
        # refusal above is the case comparison, not a blanket rejection.
        ok = add(
            bundle,
            "--id",
            "orphan",
            "--title",
            "Orphan",
            "--after",
            "lessons/02-typed-keys-table-hierarchy.md",
        )
        check(ok.returncode == 0, "--after control: the exact-case path is accepted")


def case_position_out_of_range() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        refusal(
            "--position -1",
            bundle,
            ("--id", "nowhere", "--title", "Nowhere", "--position", "-1"),
            "is outside 0..23",
        )
        refusal(
            "--position 24 (one past the end)",
            bundle,
            ("--id", "nowhere", "--title", "Nowhere", "--position", "24"),
            "is outside 0..23",
        )
        refusal(
            "--position 99",
            bundle,
            ("--id", "nowhere", "--title", "Nowhere", "--position", "99"),
            "is outside 0..23",
        )
        # POSITIVE CONTROL on the boundary itself. 23 == the lesson count is
        # the append position and MUST be accepted; without this the range
        # check could be off by one in the accepting direction and every
        # assertion above would still pass.
        ok = add(bundle, "--id", "nowhere", "--title", "Nowhere", "--position", "23")
        check(ok.returncode == 0, "--position control: 23, the lesson count, is accepted")
        check(
            manifest_lessons(bundle)[23] == "lessons/23-nowhere.md",
            "--position control: and it appends at index 23",
        )


def case_dirty_tree() -> None:
    with Workspace() as ws:
        # git_init goes on the PARENT, so the bundle directory itself holds
        # no .git and tree_digest measures only bundle content.
        clean_repo = ws.path("clean-repo")
        clean_repo.mkdir()
        clean_bundle = ws.copy("rust-automaton-db", "clean-repo/b")
        git_init(clean_repo)

        # POSITIVE CONTROL FIRST: the same command, on a bundle inside a git
        # repository whose tree is clean, succeeds. Without it "add refused"
        # is equally consistent with "add refuses inside any git repo".
        ok = add(clean_bundle, "--id", "clean-run", "--title", "Clean run")
        check(ok.returncode == 0, "dirty tree control: a clean repo is accepted")
        check_not_in(
            "uncommitted change",
            ok.output,
            "dirty tree control: and nothing is reported as uncommitted",
        )
        check_not_in(
            "not inside a git repository",
            ok.output,
            "dirty tree control: the bundle really was inside a git repo",
        )

        # Tracked file modified.
        tracked_repo = ws.path("tracked-repo")
        tracked_repo.mkdir()
        tracked_bundle = ws.copy("rust-automaton-db", "tracked-repo/b")
        git_init(tracked_repo)
        lesson_file = tracked_bundle / "lessons" / "00-foundations.md"
        lesson_file.write_text(
            lesson_file.read_text(encoding="utf-8") + "\nAn uncommitted edit.\n",
            encoding="utf-8",
        )
        tracked = refusal(
            "dirty tree (tracked file modified)",
            tracked_bundle,
            ("--id", "dirty-run", "--title", "Dirty run"),
            "uncommitted change(s)",
        )
        check_in(
            "lessons/00-foundations.md",
            tracked.output,
            "dirty tree (tracked): the message NAMES the dirty path",
        )
        check_in(
            "--force",
            tracked.output,
            "dirty tree (tracked): the message names --force as the override",
        )

        # --force overrides, on the same still-dirty bundle.
        forced = add(tracked_bundle, "--id", "dirty-run", "--title", "Dirty run", "--force")
        check(forced.returncode == 0, "dirty tree: --force runs anyway (exit 0)")
        check_in(
            "--force was given",
            forced.output,
            "dirty tree: --force says out loud that it is overriding the refusal",
        )
        check(
            has_exactly(tracked_bundle / "lessons", "23-dirty-run.md"),
            "dirty tree: --force actually wrote the lesson",
        )
        check(
            "An uncommitted edit." in lesson_file.read_text(encoding="utf-8"),
            "dirty tree: --force left the author's uncommitted edit alone",
        )

        # Untracked file present. A stray file is exactly what stops `git
        # diff` being a record of what the tool did, so it must refuse too -
        # and `git status --porcelain` reports it differently from a
        # modification, which is why it gets its own case.
        untracked_repo = ws.path("untracked-repo")
        untracked_repo.mkdir()
        untracked_bundle = ws.copy("rust-automaton-db", "untracked-repo/b")
        git_init(untracked_repo)
        (untracked_bundle / "lessons" / "scratch-notes.md").write_text(
            "# scratch\n", encoding="utf-8"
        )
        untracked = refusal(
            "dirty tree (untracked file)",
            untracked_bundle,
            ("--id", "dirty-run", "--title", "Dirty run"),
            "uncommitted change(s)",
        )
        check_in(
            "lessons/scratch-notes.md",
            untracked.output,
            "dirty tree (untracked): the message NAMES the untracked path",
        )


def case_flow_sequence() -> None:
    with Workspace() as ws:
        # POSITIVE CONTROL FIRST: the fixture as it ships, with a block
        # sequence, is accepted. The two bundles differ only in the shape of
        # the lessons list.
        block_bundle = ws.copy("foldered-bundle", "block")
        ok = add(block_bundle, "--id", "in-block-form", "--title", "Block form")
        check(ok.returncode == 0, "flow sequence control: the block form is accepted")
        check(
            manifest_lessons(block_bundle)[-1] == "lessons/02-in-block-form.md",
            "flow sequence control: and the entry is appended",
        )

        flow_bundle = ws.copy("foldered-bundle", "flow")
        manifest = flow_bundle / "tutorial.yaml"
        text = manifest.read_text(encoding="utf-8")
        rewritten = text.replace(
            "lessons:\n  - lessons/00-start.md\n  - lessons/01-shapes/LESSON.md\n",
            "lessons: [lessons/00-start.md, lessons/01-shapes/LESSON.md]\n",
        )
        check(
            rewritten != text,
            "flow sequence: the fixture rewrite actually fired (guard against a no-op setup)",
        )
        manifest.write_text(rewritten, encoding="utf-8")

        result = refusal(
            "non-empty flow sequence",
            flow_bundle,
            ("--id", "in-flow-form", "--title", "Flow form"),
            "the lessons list is written inline",
        )
        check_in(
            "block form",
            result.output,
            "non-empty flow sequence: the message tells the author to use block form",
        )
        check_in(
            "- lessons/00-first.md",
            result.output,
            "non-empty flow sequence: and shows the shape it wants",
        )


def case_validator_failure_discards() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        stub = write_stub_validator(ws.root)

        before = tree_digest(bundle)
        result = add(
            bundle,
            "--id",
            "discarded",
            "--title",
            "Discarded",
            env={"TUTORAIL_VALIDATOR": str(stub)},
        )
        check(result.returncode != 0, "validator failure: exits non-zero")
        check_in(
            "is unchanged",
            result.output,
            "validator failure: the message says the bundle is unchanged",
        )
        check_in(
            "Nothing was written",
            result.output,
            "validator failure: and that nothing was written",
        )
        check_in(
            "[check  9] DESIGN.md: the file is required and is missing",
            result.output,
            "validator failure: the stub's finding is reported verbatim",
        )
        # Every happy path in this file asserts check_in("PASS", ...). That
        # probe is only worth something if it can report the opposite, so
        # assert here that a failing run carries no PASS anywhere.
        check_not_in(
            "PASS",
            result.output,
            "validator failure: the output does NOT say PASS - the PASS probe discriminates",
        )
        check(
            tree_digest(bundle) == before,
            "validator failure: the bundle is byte-identical - the edit was discarded",
        )
        check(
            not has_exactly(bundle / "lessons", "23-discarded.md"),
            "validator failure: the staged lesson is not left behind",
        )
        check(
            len(manifest_lessons(bundle)) == 23,
            "validator failure: the manifest still has 23 entries",
        )

        # POSITIVE CONTROL: the IDENTICAL command with the real validator
        # succeeds. This is what proves the stub caused the failure, and not
        # the bundle, the slug or the operation itself.
        ok = add(bundle, "--id", "discarded", "--title", "Discarded")
        check(ok.returncode == 0, "validator failure control: the real validator accepts it")
        check_in("PASS", ok.output, "validator failure control: and reports PASS")
        check(
            has_exactly(bundle / "lessons", "23-discarded.md"),
            "validator failure control: the same lesson IS written this time",
        )


# --------------------------------------------------------------------------
# E. --optional: a lesson the tutor offers instead of sequencing
#
# Three writes have to land together - the lesson file, its `optional: true`
# frontmatter and the optional_lessons entry - because the runner's check 20
# requires the frontmatter and the list to agree. Every refusal below is
# therefore followed by tree_digest, not by "the new file is absent": a run
# that wrote the file and then failed on the manifest would pass the weaker
# check and leave a bundle the runner rejects.
# --------------------------------------------------------------------------

OFFER_AT = "lessons/03-first-refactor.md"
BECAUSE = "The borrow checker usually stops a learner right here."


def optional_add(bundle: Path, *args: str, env: dict | None = None) -> Run:
    return add(
        bundle,
        "--id",
        "borrow-detour",
        "--title",
        "A borrow detour",
        "--optional",
        *args,
        env=env,
    )


def case_optional_creates_the_block() -> None:
    """A bundle with no optional_lessons key at all gets one."""
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        # POSITIVE CONTROL for the manifest probe: before the run there is no
        # optional_lessons map, so "it holds the entry" below records a change
        # rather than reading a fixture that already had one.
        check(
            manifest_optional(bundle) == {},
            "optional: the fixture declares no optional_lessons before the run",
        )
        result = optional_add(
            bundle, "--offer-at", OFFER_AT, "--offer-because", BECAUSE
        )
        check(result.returncode == 0, f"optional: exit 0 ({result.output[-400:]})")

        check(
            has_exactly(bundle / "lessons", "borrow-detour.md"),
            "optional: lessons/ holds borrow-detour.md by directory listing",
        )
        # The format says an optional lesson has no position, so it carries no
        # number prefix. Asserting the absence of a numbered twin is the check
        # that fails if the tool reused the main-path naming.
        check(
            numbered_twins(bundle / "lessons", "borrow-detour") == [],
            f"optional: no numbered twin was written "
            f"({numbered_twins(bundle / 'lessons', 'borrow-detour')!r})",
        )
        fm = frontmatter(bundle / "lessons" / "borrow-detour.md")
        check(
            fm.get("id") == "borrow-detour",
            f"optional: the frontmatter id is the un-numbered slug, not {fm.get('id')!r}",
        )
        check(
            fm.get("optional") is True,
            f"optional: the frontmatter declares optional: true as a BOOLEAN, "
            f"not {fm.get('optional')!r} - check 20 compares against True",
        )

        # It is never in the lessons list. This is the assertion the whole
        # mode exists for.
        check(
            manifest_lessons(bundle) == ORIGINAL,
            "optional: the lessons list is byte-for-byte the original 23 entries",
        )
        entries = manifest_optional(bundle)
        check(
            list(entries) == ["lessons/borrow-detour.md"],
            f"optional: optional_lessons holds exactly the new path, not {list(entries)!r}",
        )
        entry = entries.get("lessons/borrow-detour.md", {})
        check(
            entry.get("offer_at") == [OFFER_AT],
            f"optional: offer_at is a LIST holding the resolved path, not "
            f"{entry.get('offer_at')!r}",
        )
        check(
            entry.get("offer_because") == BECAUSE,
            f"optional: offer_because is the sentence that was passed, not "
            f"{entry.get('offer_because')!r}",
        )
        check(
            sorted(entry) == ["offer_at", "offer_because"],
            f"optional: no empty optional field was written alongside them "
            f"(keys: {sorted(entry)})",
        )
        check_in("PASS", result.output, "optional: the validator PASSED")
        check_in("OPTIONAL", result.output, "optional: the plan says so out loud")
        # An optional lesson has no position, so no renumber can ever be owed.
        # Case A3 shows this probe firing on a main-path insert.
        check_not_in(
            "out of sequence",
            result.output,
            "optional: no renumber is advised, because there are no prefixes to fix",
        )


def case_optional_appends_to_an_existing_block() -> None:
    """A bundle that already offers a lesson keeps the entry it had."""
    with Workspace() as ws:
        bundle = ws.copy("optional-course", "b")
        before = manifest_optional(bundle)
        check(
            list(before) == ["lessons/vertex-winding-detour.md"],
            f"optional append: the fixture starts with one optional lesson, not {list(before)!r}",
        )
        result = add(
            bundle,
            "--id",
            "second-detour",
            "--title",
            "A second detour",
            "--optional",
            "--offer-at",
            "02-finish",
            "--offer-because",
            "A learner who asks twice deserves an answer.",
            "--anticipates",
            "inverted-winding",
            "--repair-in",
            "01-shapes",
        )
        check(result.returncode == 0, f"optional append: exit 0 ({result.output[-400:]})")
        after = manifest_optional(bundle)
        check(
            list(after) == ["lessons/vertex-winding-detour.md", "lessons/second-detour.md"],
            f"optional append: both entries are present, the old one first, got {list(after)!r}",
        )
        check(
            after["lessons/vertex-winding-detour.md"] == before["lessons/vertex-winding-detour.md"],
            "optional append: the entry that was already there reads back unchanged",
        )
        entry = after["lessons/second-detour.md"]
        check(
            entry.get("offer_at") == ["lessons/02-finish.md"],
            f"optional append: the lesson ID form of --offer-at resolved to the "
            f"manifest path, got {entry.get('offer_at')!r}",
        )
        check(
            entry.get("anticipates") == ["inverted-winding"],
            f"optional append: anticipates is a list, got {entry.get('anticipates')!r}",
        )
        check(
            entry.get("repair_in") == "lessons/01-shapes.md",
            f"optional append: repair_in is a SCALAR path, not a list, got "
            f"{entry.get('repair_in')!r}",
        )
        check(
            manifest_lessons(bundle) == [
                "lessons/00-start.md",
                "lessons/01-shapes.md",
                "lessons/02-finish.md",
            ],
            "optional append: the main path is untouched",
        )
        check_in("PASS", result.output, "optional append: the validator PASSED")


def case_optional_folder() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        result = optional_add(
            bundle, "--offer-at", OFFER_AT, "--offer-because", BECAUSE, "--folder"
        )
        check(result.returncode == 0, f"optional --folder: exit 0 ({result.output[-300:]})")
        folder = bundle / "lessons" / "borrow-detour"
        check(
            has_exactly(bundle / "lessons", "borrow-detour"),
            "optional --folder: lessons/ holds the un-numbered folder by listing",
        )
        check(
            has_exactly(folder, "LESSON.md")
            and has_miscased(folder, "LESSON.md") is None,
            f"optional --folder: the folder holds an exact-case LESSON.md "
            f"({listing(folder)!r})",
        )
        check(
            list(manifest_optional(bundle)) == ["lessons/borrow-detour/LESSON.md"],
            f"optional --folder: the optional_lessons key names the LESSON.md path, "
            f"got {list(manifest_optional(bundle))!r}",
        )
        check(
            frontmatter(folder / "LESSON.md").get("optional") is True,
            "optional --folder: the foldered body declares optional: true",
        )
        check_in("PASS", result.output, "optional --folder: the validator PASSED")


def case_required_for_quotes_the_rubric() -> None:
    """The one opinion the toolkit carries must be the rubric's own words.

    Two halves, and both are needed. The tool must PRINT the warning, and the
    printed text must be IN the rubric - otherwise the tool drifts into
    teaching something the rubric does not say, silently, and no test notices.
    """
    rubric = (
        Path(__file__).resolve().parent.parent
        / "skills"
        / "course-quality"
        / "references"
        / "rubric.md"
    )
    rubric_text = rubric.read_text(encoding="utf-8")
    check(
        "`required_for` scores and is raised, both" in rubric_text,
        "required_for: the rubric still carries the section this warning comes from",
    )

    with Workspace() as ws:
        bundle = ws.copy("optional-course", "b")
        result = add(
            bundle,
            "--id",
            "gated-detour",
            "--title",
            "A gated detour",
            "--optional",
            "--offer-at",
            "01-shapes",
            "--offer-because",
            "The winding rule is worth a detour.",
            "--anticipates",
            "inverted-winding",
            "--required-for",
            "02-finish",
        )
        check(result.returncode == 0, f"required_for: exit 0 ({result.output[-400:]})")

        # The warning is quoted, line for line, from the rubric's block quote.
        # Asserting both sides is what makes a drift in EITHER file fail here.
        for line in (
            "This gate cost the course 3 points and may still be correct. If the lesson genuinely",
            "cannot be completed while its failure stands, the gate is doing its job — say so and",
            "keep it. Do not delete a gate to improve a score. A course that drops a justified gate",
            "lets a learner finish a lesson whose failure is still standing, which is worse than the",
            "toil this rubric hunts.",
        ):
            check_in(line, result.output, f"required_for: the tool prints {line[:38]!r}...")
            check(
                f"> {line}" in rubric_text,
                f"required_for: and the rubric carries that line VERBATIM as a "
                f"quoted line ({line[:38]!r}...)",
            )
        check_in(
            "skills/course-quality/references/rubric.md",
            result.output,
            "required_for: the warning names the file it is quoting",
        )
        check_in(
            "-3", result.output, "required_for: the warning names the score it costs"
        )
        check(
            manifest_optional(bundle)["lessons/gated-detour.md"].get("required_for")
            == ["lessons/02-finish.md"],
            "required_for: the gate really was written, resolved to the manifest path",
        )
        check_in("PASS", result.output, "required_for: the validator PASSED")

        # POSITIVE CONTROL for the check_in probes above: the same command
        # WITHOUT --required-for must not print the warning. Otherwise "the
        # warning is there" is equally consistent with a tool that prints it
        # on every run, which would train an author to ignore it.
        quiet = add(
            bundle,
            "--id",
            "ungated-detour",
            "--title",
            "An ungated detour",
            "--optional",
            "--offer-at",
            "01-shapes",
            "--offer-because",
            "The winding rule is worth a second detour.",
        )
        check(quiet.returncode == 0, "required_for control: the ungated add succeeds")
        check_not_in(
            "This gate cost the course 3 points",
            quiet.output,
            "required_for control: an add with no gate prints NO warning",
        )


def case_optional_refusals() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")

        refusal(
            "--optional with no --offer-at",
            bundle,
            ("--id", "d1", "--title", "D", "--optional", "--offer-because", BECAUSE),
            "--optional needs --offer-at",
        )
        refusal(
            "--optional with no --offer-because",
            bundle,
            ("--id", "d1", "--title", "D", "--optional", "--offer-at", OFFER_AT),
            "--optional needs --offer-because",
        )
        refusal(
            "--optional with --position",
            bundle,
            (
                "--id", "d1", "--title", "D", "--optional", "--position", "3",
                "--offer-at", OFFER_AT, "--offer-because", BECAUSE,
            ),
            "--position cannot be combined with --optional",
        )
        refusal(
            "--optional with --after",
            bundle,
            (
                "--id", "d1", "--title", "D", "--optional", "--after", OFFER_AT,
                "--offer-at", OFFER_AT, "--offer-because", BECAUSE,
            ),
            "--after cannot be combined with --optional",
        )
        refusal(
            "--optional with a numbered --id",
            bundle,
            (
                "--id", "05-d1", "--title", "D", "--optional",
                "--offer-at", OFFER_AT, "--offer-because", BECAUSE,
            ),
            "carries the number prefix",
        )
        refusal(
            "--offer-at names no lesson",
            bundle,
            (
                "--id", "d1", "--title", "D", "--optional",
                "--offer-at", "lessons/99-nowhere.md", "--offer-because", BECAUSE,
            ),
            "is not a lesson on this course's main path",
        )
        miscased = refusal(
            "--offer-at is mis-cased",
            bundle,
            (
                "--id", "d1", "--title", "D", "--optional",
                "--offer-at", "lessons/03-First-Refactor.md",
                "--offer-because", BECAUSE,
            ),
            "is not a lesson on this course's main path",
        )
        check_in(
            "Did you mean 'lessons/03-first-refactor.md'?",
            miscased.output,
            "--offer-at mis-cased: the message offers the exact-case entry",
        )
        refusal(
            "--repair-in names no lesson",
            bundle,
            (
                "--id", "d1", "--title", "D", "--optional",
                "--offer-at", OFFER_AT, "--offer-because", BECAUSE,
                "--repair-in", "lessons/99-nowhere.md",
            ),
            "--repair-in 'lessons/99-nowhere.md' is not a lesson",
        )
        refusal(
            "an offer flag without --optional",
            bundle,
            ("--id", "d1", "--title", "D", "--offer-at", OFFER_AT),
            "Add --optional",
        )

        # POSITIVE CONTROL for all nine. The same command, with exactly the
        # two required flags and nothing wrong, is accepted - so each refusal
        # above is about the thing it names and not about --optional itself,
        # the bundle, or the slug.
        ok = add(
            bundle, "--id", "d1", "--title", "D", "--optional",
            "--offer-at", OFFER_AT, "--offer-because", BECAUSE,
        )
        check(ok.returncode == 0, f"optional refusal control: the good run is accepted ({ok.output[-300:]})")
        check(
            list(manifest_optional(bundle)) == ["lessons/d1.md"],
            "optional refusal control: and it writes the entry the nine refused runs did not",
        )

    with Workspace() as ws:
        # An --offer-at naming a lesson the bundle HAS, but which is not on
        # the main path. The path resolves on disk, so a tool that checked the
        # filesystem instead of the lessons list would accept it and write an
        # offer point no learner ever reaches.
        bundle = ws.copy("optional-course", "b")
        refusal(
            "--offer-at names an OPTIONAL lesson",
            bundle,
            (
                "--id", "d2", "--title", "D", "--optional",
                "--offer-at", "lessons/vertex-winding-detour.md",
                "--offer-because", BECAUSE,
            ),
            "is not a lesson on this course's main path",
        )
        check(
            has_exactly(bundle / "lessons", "vertex-winding-detour.md"),
            "--offer-at an optional lesson: the file really does exist, which is "
            "why a disk check would have passed it",
        )
        ok = add(
            bundle, "--id", "d2", "--title", "D", "--optional",
            "--offer-at", "lessons/01-shapes.md", "--offer-because", BECAUSE,
        )
        check(
            ok.returncode == 0,
            "--offer-at control: a MAIN-PATH path at the same spelling is accepted",
        )


def case_optional_duplicate_and_inline() -> None:
    with Workspace() as ws:
        bundle = ws.copy("optional-course", "b")
        refusal(
            "an optional lesson that already exists",
            bundle,
            (
                "--id", "vertex-winding-detour", "--title", "Again", "--optional",
                "--offer-at", "01-shapes", "--offer-because", BECAUSE,
            ),
            "lessons/vertex-winding-detour already exists",
        )

    with Workspace() as ws:
        # POSITIVE CONTROL FIRST: `optional_lessons: {}` is the one inline
        # shape the editor rewrites rather than refuses, mirroring what
        # add_supplies does for `supplies: []`.
        empty = ws.copy("rust-automaton-db", "empty")
        manifest = empty / "tutorial.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8") + "\noptional_lessons: {}\n",
            encoding="utf-8",
        )
        ok = optional_add(empty, "--offer-at", OFFER_AT, "--offer-because", BECAUSE)
        check(ok.returncode == 0, f"empty inline map: accepted ({ok.output[-300:]})")
        check(
            list(manifest_optional(empty)) == ["lessons/borrow-detour.md"],
            "empty inline map: rewritten in block form with the entry in it",
        )
        check(
            "optional_lessons: {}" not in manifest.read_text(encoding="utf-8"),
            "empty inline map: the inline spelling is gone",
        )

        # And the non-empty inline value is refused. This is also the
        # three-writes-or-none case: the refusal is raised by the MANIFEST
        # edit, after the lesson file has already been written to the staging
        # copy, so a digest that matches proves the staged file went with it.
        inline = ws.copy("rust-automaton-db", "inline")
        inline_manifest = inline / "tutorial.yaml"
        inline_manifest.write_text(
            inline_manifest.read_text(encoding="utf-8")
            + "\noptional_lessons: {lessons/other.md: x}\n",
            encoding="utf-8",
        )
        refused = refusal(
            "a non-empty inline optional_lessons",
            inline,
            (
                "--id", "borrow-detour", "--title", "D", "--optional",
                "--offer-at", OFFER_AT, "--offer-because", BECAUSE,
            ),
            "already carries an inline value",
        )
        check_in(
            "block form",
            refused.output,
            "non-empty inline map: the message tells the author to use block form",
        )
        check(
            not has_exactly(inline / "lessons", "borrow-detour.md"),
            "non-empty inline map: the lesson file written to the staging copy "
            "is not left behind",
        )


def case_optional_validator_failure_discards() -> None:
    """All three writes are discarded together when the validator objects."""
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        stub = write_stub_validator(ws.root)
        before = tree_digest(bundle)
        result = optional_add(
            bundle,
            "--offer-at",
            OFFER_AT,
            "--offer-because",
            BECAUSE,
            env={"TUTORAIL_VALIDATOR": str(stub)},
        )
        check(result.returncode != 0, "optional discard: exits non-zero")
        check(
            tree_digest(bundle) == before,
            "optional discard: the bundle is byte-identical afterwards",
        )
        check(
            not has_exactly(bundle / "lessons", "borrow-detour.md"),
            "optional discard: the lesson file is not left behind",
        )
        check(
            manifest_optional(bundle) == {},
            "optional discard: and no optional_lessons entry is left behind either",
        )
        # POSITIVE CONTROL: the identical command with the real validator
        # writes both halves.
        ok = optional_add(bundle, "--offer-at", OFFER_AT, "--offer-because", BECAUSE)
        check(ok.returncode == 0, "optional discard control: the real validator accepts it")
        check(
            has_exactly(bundle / "lessons", "borrow-detour.md")
            and list(manifest_optional(bundle)) == ["lessons/borrow-detour.md"],
            "optional discard control: this time BOTH the file and the entry are there",
        )


def case_optional_check() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "b")
        before = tree_digest(bundle)
        result = optional_add(
            bundle, "--offer-at", OFFER_AT, "--offer-because", BECAUSE, "--check"
        )
        check(result.returncode == 0, "optional --check: exit 0")
        check(
            tree_digest(bundle) == before,
            "optional --check: the bundle is byte-identical afterwards",
        )
        check_in("nothing was written", result.output, "optional --check: says so")
        check_in(
            "offer_because   " + BECAUSE,
            result.output,
            "optional --check: the plan prints the offer metadata it would write",
        )
        # POSITIVE CONTROL for the digest oracle on this path.
        real = optional_add(bundle, "--offer-at", OFFER_AT, "--offer-because", BECAUSE)
        check(real.returncode == 0, "optional --check control: the same run without --check succeeds")
        check(
            tree_digest(bundle) != before,
            "optional --check control: the digest DOES move for a real optional add",
        )


# --------------------------------------------------------------------------


def main() -> int:
    print("lesson.py add")
    print(f"  fixtures: {FIXTURES}")
    try:
        validator, how = bl.find_validator()
        note(f"validator under test: {validator} ({how})")
    except bl.ToolError as exc:  # pragma: no cover - a machine without the runner
        print(f"  cannot run: {exc}")
        return 2
    print()

    with case("A1 append at the end of rust-automaton-db"):
        case_append()
    with case("A2 --folder creates lessons/<slug>/LESSON.md"):
        case_folder()
    with case("A3 --position 3 inserts in the middle and warns"):
        case_position()
    with case("A4 --after inserts behind the named entry"):
        case_after()
    with case("A5 --check prints the plan and changes nothing"):
        case_check()

    with case("B6 --position 0 retargets STATE.template.md active_lesson"):
        case_state_changed()
    with case("B7 an append leaves STATE.template.md byte-identical"):
        case_state_unchanged()

    with case("C8 bootstrap: lessons: [] gets its first lesson"):
        bootstrap_case(
            "bootstrap []", "lessons: []", "the lessons list is empty"
        )
    with case("C9 bootstrap: a bare lessons: key gets its first lesson"):
        bootstrap_case(
            "bootstrap bare", "lessons:", "the required field 'lessons' is empty"
        )

    with case("D10 a slug that already exists is refused"):
        case_slug_exists()
    with case("D11 the same body under another number is refused"):
        case_same_body_other_number()
    with case("D12 an --id that is not a slug is refused"):
        case_bad_slug()
    with case("D13 --after a path that is not listed is refused"):
        case_after_unknown()
    with case("D14 --position outside 0..count is refused"):
        case_position_out_of_range()
    with case("D15 a dirty git working tree is refused, and --force overrides"):
        case_dirty_tree()
    with case("D16 a non-empty flow lessons list is refused"):
        case_flow_sequence()
    with case("D17 a validator failure discards the edit"):
        case_validator_failure_discards()

    with case("E18 --optional creates the optional_lessons block"):
        case_optional_creates_the_block()
    with case("E19 --optional appends to a block that already exists"):
        case_optional_appends_to_an_existing_block()
    with case("E20 --optional --folder writes an un-numbered lesson folder"):
        case_optional_folder()
    with case("E21 --required-for prints the rubric's warning verbatim"):
        case_required_for_quotes_the_rubric()
    with case("E22 every --optional refusal fires, with one positive control"):
        case_optional_refusals()
    with case("E23 a duplicate lesson and an inline optional_lessons are refused"):
        case_optional_duplicate_and_inline()
    with case("E24 a validator failure discards all three optional writes"):
        case_optional_validator_failure_discards()
    with case("E25 --optional --check prints the plan and changes nothing"):
        case_optional_check()

    return report("lesson.py add")


if __name__ == "__main__":
    sys.exit(main())
