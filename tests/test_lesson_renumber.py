#!/usr/bin/env python3
"""Test suite for `lesson.py renumber`.

Run it with:  python3 tests/test_lesson_renumber.py

Renumber is the operation the design calls out as able to silently corrupt a
23-lesson course, and section 9 of the design is normative about the one
thing the validator cannot catch:

    Lesson files reference other lessons BY ID, IN PROSE. Renumbering
    rewrites filenames, slugs, ids and the manifest, and leaves those prose
    references pointing at ids that no longer exist. The validator would NOT
    catch it: design_refs and validators are checked, a prerequisite named in
    prose is not.

So the central case here is not "renumber ran". It is that a real prose
`Prerequisites:` line in a copy of the REAL AutomatonDB bundle is rewritten,
with the exact new bytes asserted - and, just as importantly, that the four
things it must NOT touch are byte-identical afterwards:

  * a substring of an id it is renaming            02-typed-keys
  * a longer token containing an id                lessons/03-x.md.bak
  * an id it does not own                          a lesson not being moved
  * a token that looks like a reference and is not 99-does-not-exist

A rewriter that can only be shown rewriting is a false oracle: it would pass
identically if it rewrote everything it saw. Every negative here has the
positive beside it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import harness as h
from harness import case, check, check_in, check_not_in, run

sys.path.insert(0, str(h.SCRIPTS))
import bundlelib as bl  # noqa: E402


def frontmatter_of(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    raw, _ = bl.split_frontmatter(text)
    assert raw is not None, f"{path} has no frontmatter"
    parsed = bl.load_yaml(raw, str(path))
    assert isinstance(parsed, dict)
    return parsed


def manifest_lessons(bundle: Path) -> list[str]:
    manifest, _ = bl.load_manifest(bundle)
    return [x for x in manifest["lessons"] if isinstance(x, str)]


def real_validator_passes(bundle: Path) -> bool:
    validator, _ = bl.find_validator()
    done = run(validator, bundle)
    return done.returncode == 0


# --------------------------------------------------------------------------


def test_nothing_to_do() -> None:
    """An already-consistent bundle is reported as such, not churned.

    The positive control for every other case in this file: if renumber
    rewrote a consistent bundle, "it rewrote things" would prove nothing.
    """
    with h.Workspace() as ws, case("a consistent bundle has nothing to renumber"):
        bundle = ws.copy("rust-automaton-db")
        before = h.tree_digest(bundle)
        done = run(h.LESSON, "renumber", bundle)
        check(done.returncode == 1, "exits 1 when there is nothing to do")
        check_in("Nothing to do", done.output, "says so in words")
        check(
            h.tree_digest(bundle) == before,
            "a no-op renumber leaves the bundle byte-identical",
        )


def test_prose_prerequisite_is_rewritten() -> None:
    """The design's section 9 hazard, on the real bundle it was found in.

    AutomatonDB's lessons/04-richer-typed-schemas.md carries, in prose:

        ## Prerequisites

        - `03-first-refactor`

    Inserting a lesson at position 3 pushes 03-first-refactor to 04. Nothing
    in the bundle format or the validator would notice that this line is now
    dangling. renumber must rewrite it.
    """
    with h.Workspace() as ws, case("a real prose Prerequisites reference is rewritten"):
        bundle = ws.copy("rust-automaton-db")

        # Establish the starting fact rather than trusting the fixture.
        source = bundle / "lessons" / "04-richer-typed-schemas.md"
        original = source.read_text(encoding="utf-8")
        check(
            "- `03-first-refactor`" in original,
            "the fixture really does name 03-first-refactor in prose",
        )

        added = run(
            h.LESSON,
            "add",
            bundle,
            "--id",
            "ownership-interlude",
            "--title",
            "An ownership interlude",
            "--position",
            "3",
        )
        check(added.returncode == 0, "the insert that causes the renumber succeeds")

        done = run(h.LESSON, "renumber", bundle)
        check(done.returncode == 0, "renumber succeeds")

        moved = bundle / "lessons" / "05-richer-typed-schemas.md"
        check(
            h.has_exactly(bundle / "lessons", "05-richer-typed-schemas.md"),
            "the lesson file moved from 04- to 05-",
        )
        text = moved.read_text(encoding="utf-8")
        # The VALUE, not the shape: the exact new line, and the old one gone.
        check(
            "- `04-first-refactor`" in text,
            "the prose prerequisite now names 04-first-refactor",
        )
        check(
            "03-first-refactor" not in text,
            "no trace of the old id is left in that lesson",
        )
        check(
            frontmatter_of(moved)["id"] == "05-richer-typed-schemas",
            "the frontmatter id equals the new slug",
        )
        check_in(
            "03-first-refactor -> 04-first-refactor",
            done.output,
            "every rewrite is reported, so git diff is reviewable",
        )
        check_in(
            "bare lesson ids in prose",
            done.output,
            "prose id rewrites are reported under their own label",
        )
        check(real_validator_passes(bundle), "the renumbered bundle validates")

        # The manifest agrees with the disk, in order.
        listed = manifest_lessons(bundle)
        check(
            listed[3] == "lessons/03-ownership-interlude.md"
            and listed[4] == "lessons/04-first-refactor.md"
            and listed[5] == "lessons/05-richer-typed-schemas.md",
            "the lessons list is in the renumbered order",
        )
        for entry in listed:
            resolved, why = bl.resolve_exact(bundle, entry)
            check(resolved is not None, f"lessons entry {entry} resolves exactly ({why})")


def test_does_not_touch_what_it_does_not_own() -> None:
    """Section 9: never a substring, never an id it does not own.

    Four tokens are planted in one lesson body. Exactly one of them is a
    reference to a lesson being renamed, and only that one may change. The
    one that DOES change is the positive control: without it, "nothing
    changed" would also be the result of a rewriter that did nothing at all.
    """
    with h.Workspace() as ws, case("substrings, longer tokens and foreign ids are left alone"):
        bundle = ws.copy("rust-automaton-db")
        planted = bundle / "lessons" / "22-hardening-performance.md"
        text = planted.read_text(encoding="utf-8")
        text += (
            "\n## Planted references\n"
            "\n"
            "- exact, and being renamed: `03-first-refactor`\n"
            "- a substring of an id being renamed: `03-first`\n"
            "- a longer token containing one: `lessons/03-first-refactor.md.bak`\n"
            "- hyphen-joined to more: `03-first-refactor-notes`\n"
            "- an id NOT being renamed: `00-foundations`\n"
            "- shaped like a reference, names nothing: `99-does-not-exist`\n"
        )
        planted.write_text(text, encoding="utf-8")

        added = run(
            h.LESSON, "add", bundle, "--id", "interlude", "--title", "I", "--position", "3"
        )
        check(added.returncode == 0, "the insert succeeds")
        done = run(h.LESSON, "renumber", bundle)
        check(done.returncode == 0, "renumber succeeds")

        after = (bundle / "lessons" / "23-hardening-performance.md").read_text(
            encoding="utf-8"
        )

        # POSITIVE CONTROL. The exact token did change; so the four negatives
        # below are about what the rewriter chose, not about it doing nothing.
        check(
            "exact, and being renamed: `04-first-refactor`" in after,
            "the exact whole-token id it owns IS rewritten (positive control)",
        )
        check(
            "a substring of an id being renamed: `03-first`" in after,
            "a substring of a renamed id is NOT rewritten",
        )
        check(
            "a longer token containing one: `lessons/03-first-refactor.md.bak`" in after,
            "a longer token containing a renamed path is NOT rewritten",
        )
        check(
            "hyphen-joined to more: `03-first-refactor-notes`" in after,
            "an id hyphen-joined into a longer token is NOT rewritten",
        )
        check(
            "an id NOT being renamed: `00-foundations`" in after,
            "an id this run does not own is NOT rewritten",
        )
        check(
            "shaped like a reference, names nothing: `99-does-not-exist`" in after,
            "a look-alike naming no lesson is NOT rewritten",
        )

        # ... and the ones left alone are REPORTED, which section 9 requires.
        check_in("left alone:", done.output, "a left-alone section is printed")
        check_in(
            "99-does-not-exist",
            done.output,
            "a look-alike that names no lesson is reported individually",
        )
        check_in(
            "00-foundations",
            done.output,
            "references to lessons this run did not renumber are reported",
        )
        # 03-first is shaped like a lesson id but names nothing, so it is
        # reported too. Asserting it proves the look-alike scan is not merely
        # echoing the rename map back.
        check_in(
            "03-first\n", done.output + "\n", "the substring look-alike is reported too"
        )


def test_check_changes_nothing() -> None:
    """--check must do the whole thing on a copy and write nothing."""
    with h.Workspace() as ws, case("--check prints the plan and changes nothing"):
        bundle = ws.copy("rust-automaton-db")
        run(h.LESSON, "add", bundle, "--id", "interlude", "--title", "I", "--position", "3")
        before = h.tree_digest(bundle)
        done = run(h.LESSON, "renumber", bundle, "--check")
        check(done.returncode == 0, "--check exits 0 when the plan would validate")
        check_in("nothing was written", done.output, "says nothing was written")
        check_in("03-first-refactor  ->  04-first-refactor", done.output, "prints the plan")
        check(
            h.tree_digest(bundle) == before,
            "--check leaves the bundle byte-identical",
        )
        # POSITIVE CONTROL: the same command without --check does change it.
        applied = run(h.LESSON, "renumber", bundle)
        check(applied.returncode == 0, "the same run without --check succeeds")
        check(
            h.tree_digest(bundle) != before,
            "without --check the bundle really does change (positive control)",
        )


def test_folder_lesson_and_binary_material() -> None:
    """A foldered lesson is renamed as a folder, and binary material is untouched.

    The exact-case assertion matters: this filesystem is case-insensitive, so
    a rename that lost the case of LESSON.md would resolve locally and fail
    on Linux. has_miscased is the only way to see it.
    """
    with h.Workspace() as ws, case("a foldered lesson renumbers without touching its material"):
        bundle = ws.copy("foldered-bundle")
        binary = bundle / "lessons" / "01-shapes" / "assets" / "shape.bin"
        binary_before = binary.read_bytes()
        check(
            len(binary_before) > 0 and b"\xff" in binary_before,
            "the fixture's material really is non-UTF-8 bytes",
        )

        added = run(
            h.LESSON, "add", bundle, "--id", "vocabulary", "--title", "V", "--position", "0"
        )
        check(added.returncode == 0, "inserting at position 0 succeeds")
        done = run(h.LESSON, "renumber", bundle)
        check(done.returncode == 0, "renumber succeeds")

        lessons = bundle / "lessons"
        check(
            h.has_exactly(lessons, "02-shapes"),
            "the lesson FOLDER was renamed 01-shapes -> 02-shapes",
        )
        folder = lessons / "02-shapes"
        check(
            h.has_exactly(folder, "LESSON.md"),
            "the folder still holds an entry named exactly LESSON.md",
        )
        check(
            h.has_miscased(folder, "LESSON.md") is None,
            "and no differently-cased near-miss beside it",
        )
        check(
            frontmatter_of(folder / "LESSON.md")["id"] == "02-shapes",
            "the foldered lesson's frontmatter id follows the folder name",
        )
        check(
            manifest_lessons(bundle)[2] == "lessons/02-shapes/LESSON.md",
            "the manifest names the LESSON.md inside the renamed folder",
        )
        check(
            (folder / "assets" / "shape.bin").read_bytes() == binary_before,
            "the non-UTF-8 material file is byte-identical",
        )
        # 01-shapes names `00-start` as its prerequisite. Inserting a lesson
        # at position 0 pushes 00-start to 01-start, so the prose reference
        # must follow it. This is the same section 9 hazard as the AutomatonDB
        # case above, reached through a FOLDERED lesson's body.
        check(
            "- `01-start`" in (folder / "LESSON.md").read_text(encoding="utf-8"),
            "the foldered lesson's prose prerequisite was rewritten too",
        )
        check(real_validator_passes(bundle), "the renumbered foldered bundle validates")


def test_state_template_follows_lesson_zero() -> None:
    """bundle-format section 5: active_lesson MUST equal lessons[0].

    Both directions, because a maintenance step that always writes is as
    wrong as one that never does.
    """
    with h.Workspace() as ws, case("STATE.template.md follows lessons[0] when it changes"):
        bundle = ws.copy("rust-automaton-db")
        state = bundle / "STATE.template.md"
        check(
            "active_lesson: lessons/00-foundations.md" in state.read_text(encoding="utf-8"),
            "the fixture starts pointing at 00-foundations",
        )
        run(h.LESSON, "add", bundle, "--id", "welcome", "--title", "W", "--position", "0")
        done = run(h.LESSON, "renumber", bundle)
        check(done.returncode == 0, "renumber succeeds")
        text = state.read_text(encoding="utf-8")
        check(
            "active_lesson: lessons/00-welcome.md" in text,
            "active_lesson now names the new lessons[0]",
        )
        check(
            manifest_lessons(bundle)[0] == "lessons/00-welcome.md",
            "and that really is lessons[0]",
        )
        check(real_validator_passes(bundle), "which is what the validator's check 12 wants")

    with h.Workspace() as ws, case("STATE.template.md is left alone when lessons[0] does not move"):
        bundle = ws.copy("rust-automaton-db")
        state_before = (bundle / "STATE.template.md").read_bytes()
        run(h.LESSON, "add", bundle, "--id", "interlude", "--title", "I", "--position", "5")
        done = run(h.LESSON, "renumber", bundle)
        check(done.returncode == 0, "renumber succeeds")
        check(
            (bundle / "STATE.template.md").read_bytes() == state_before,
            "STATE.template.md is byte-identical when lessons[0] did not change",
        )
        check_in(
            "already agreed",
            done.output,
            "and the tool says it left it alone rather than silently writing",
        )


def test_dirty_tree_refusal() -> None:
    """Section 8: refuse a dirty working tree unless forced."""
    with h.Workspace() as ws, case("a dirty working tree refuses the renumber"):
        bundle = ws.copy("rust-automaton-db")
        h.git_init(bundle)

        # POSITIVE CONTROL first: clean, it runs.
        clean = run(h.LESSON, "add", bundle, "--id", "interlude", "--title", "I", "--position", "3")
        check(clean.returncode == 0, "on a clean tree the insert succeeds (positive control)")

        # `add` just wrote, so the tree is now dirty for real.
        before = h.tree_digest(bundle)
        refused = run(h.LESSON, "renumber", bundle)
        check(refused.returncode != 0, "a dirty tree refuses")
        check_in("uncommitted change", refused.output, "and names what is dirty")
        check_in("--force", refused.output, "and says how to override")
        check(
            h.tree_digest(bundle) == before,
            "the refused run left the bundle byte-identical",
        )

        forced = run(h.LESSON, "renumber", bundle, "--force")
        check(forced.returncode == 0, "--force overrides the refusal")
        check_in("--force was given", forced.output, "and says it is doing so")
        check(h.tree_digest(bundle) != before, "and the forced run really did change it")

    with h.Workspace() as ws, case("an untracked file counts as dirty"):
        bundle = ws.copy("rust-automaton-db")
        run(h.LESSON, "add", bundle, "--id", "interlude", "--title", "I", "--position", "3")
        h.git_init(bundle)
        # Committed and clean; renumber should now be allowed.
        allowed = run(h.LESSON, "renumber", bundle, "--check")
        check(allowed.returncode == 0, "a clean tree is allowed (positive control)")
        (bundle / "lessons" / "stray-notes.txt").write_text("scratch\n", encoding="utf-8")
        refused = run(h.LESSON, "renumber", bundle)
        check(refused.returncode != 0, "an untracked file inside the bundle refuses")
        check_in("stray-notes.txt", refused.output, "and the stray file is named")


def test_unlisted_lesson_is_not_renumbered() -> None:
    """A lesson the manifest does not name has no position to compute.

    Inventing one would be this tool deciding where an unlisted lesson
    belongs. It is left alone; the validator already reports it as invisible.
    """
    with h.Workspace() as ws, case("an unlisted lesson blocks the renumber rather than being renamed"):
        bundle = ws.copy("rust-automaton-db")
        # Set up a renumber that WOULD have work to do, first, so that a
        # "nothing to do" result cannot be mistaken for the refusal under
        # test. This ordering is the point: the add must succeed while the
        # bundle is still valid.
        added = run(
            h.LESSON, "add", bundle, "--id", "interlude", "--title", "I", "--position", "3"
        )
        check(added.returncode == 0, "the insert succeeds while the bundle is valid")

        orphan = bundle / "lessons" / "90-orphan.md"
        orphan.write_text(
            "---\nid: 90-orphan\ntitle: Orphan\n---\n\n## Purpose\n\nUnlisted.\n",
            encoding="utf-8",
        )
        before = h.tree_digest(bundle)
        done = run(h.LESSON, "renumber", bundle)
        # The post-validation MUST fail: an unlisted lesson is a check-4
        # finding, so the bundle would not be valid afterwards. Refusing is
        # the safety property working, not a defect.
        check(done.returncode != 0, "renumber refuses while an unlisted lesson exists")
        check_in("unchanged", done.output, "and says the bundle is unchanged")
        check_in("90-orphan", done.output, "and the validator's finding names it")
        check(
            h.tree_digest(bundle) == before,
            "the refused renumber left the bundle byte-identical",
        )
        check(
            h.has_exactly(bundle / "lessons", "90-orphan.md"),
            "the unlisted lesson was neither renamed nor removed",
        )


def main() -> int:
    print("lesson.py renumber test suite")
    print(f"  script:  {h.LESSON}")
    print(f"  python:  {sys.version.split()[0]}")
    try:
        validator, how = bl.find_validator()
        print(f"  runner:  {validator}  ({how})")
    except bl.ToolError:
        print("  runner:  NOT FOUND - this suite needs the tutorAIl runner installed")
        return 2
    print()

    test_nothing_to_do()
    test_prose_prerequisite_is_rewritten()
    test_does_not_touch_what_it_does_not_own()
    test_check_changes_nothing()
    test_folder_lesson_and_binary_material()
    test_state_template_follows_lesson_zero()
    test_dirty_tree_refusal()
    test_unlisted_lesson_is_not_renumbered()
    return h.report("lesson.py renumber")


if __name__ == "__main__":
    sys.exit(main())
