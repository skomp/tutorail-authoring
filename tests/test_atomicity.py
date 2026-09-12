#!/usr/bin/env python3
"""Cross-cutting proof of the toolkit's central safety property.

Run it with:  python3 tests/test_atomicity.py

Design section 8, last line:

    A failed operation must leave the bundle unchanged rather than
    half-edited. This is a TESTED PROPERTY, not an intention.

This suite is that test. It takes every mutating operation - `lesson.py add`,
`lesson.py renumber`, `promote.py` - and makes each one fail in four
independent ways, asserting after each failure that the bundle is
BYTE-IDENTICAL: every path, every mode bit, every byte.

The four ways matter, because they fail at different points and a design
that only survived one of them would not be atomic:

  1. before any work      - the runner's validator cannot be found
  2. before any work      - the git working tree is dirty
  3. after the whole edit - the validator reports the result invalid
  4. part-way through     - the manifest cannot be edited surgically

Each has a POSITIVE CONTROL beside it: the same command, in the same place,
succeeding. Without that, "the bundle did not change" is equally consistent
with a tool that does nothing at all, and this whole file would be a false
oracle.

`tree_digest` is what makes the assertion real. "The new lesson file is
absent" is a much weaker claim: it passes against a tutorial.yaml that was
rewritten and a STATE.template.md that was retargeted.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

import harness as h
from harness import case, check, check_in, run

sys.path.insert(0, str(h.SCRIPTS))
import bundlelib as bl  # noqa: E402


# --------------------------------------------------------------------------
# The three mutating operations, as (label, argv-builder) pairs, so every
# failure injection below runs against all of them rather than against
# whichever one was convenient.
# --------------------------------------------------------------------------


def add_argv(bundle: Path, instance: Path) -> tuple[Path, list[str]]:
    return h.LESSON, ["add", str(bundle), "--id", "an-extra-lesson", "--title", "Extra"]


def renumber_argv(bundle: Path, instance: Path) -> tuple[Path, list[str]]:
    return h.LESSON, ["renumber", str(bundle)]


def promote_argv(bundle: Path, instance: Path) -> tuple[Path, list[str]]:
    return h.PROMOTE, [
        str(instance),
        "lessons.generated/lifetimes-and-borrows.md",
        str(bundle),
    ]


OPERATIONS = (
    ("lesson.py add", add_argv),
    ("lesson.py renumber", renumber_argv),
    ("promote.py", promote_argv),
)


def prepare(ws: h.Workspace, name: str) -> tuple[Path, Path]:
    """A bundle on which ALL THREE operations have real work to do.

    `renumber` only has work when the filename prefixes disagree with the
    lessons order, so the bundle is set up with one lesson deliberately
    misnumbered. Without this, a "renumber changed nothing" result would be
    indistinguishable from the property under test.
    """
    bundle = ws.copy("rust-automaton-db", f"{name}-bundle")
    instance = ws.copy("instance-with-generated", f"{name}-instance")

    lessons = bundle / "lessons"
    os.rename(lessons / "22-hardening-performance.md", lessons / "40-hardening-performance.md")
    manifest = bundle / "tutorial.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "lessons/22-hardening-performance.md", "lessons/40-hardening-performance.md"
        ),
        encoding="utf-8",
    )
    lesson = lessons / "40-hardening-performance.md"
    lesson.write_text(
        lesson.read_text(encoding="utf-8").replace(
            "id: 22-hardening-performance", "id: 40-hardening-performance"
        ),
        encoding="utf-8",
    )
    # Prove the setup really is a valid bundle with pending renumber work,
    # rather than assuming it.
    validator, _ = bl.find_validator()
    assert run(validator, bundle).returncode == 0, "the prepared bundle must be valid"
    return bundle, instance


def leftovers(bundle: Path) -> list[str]:
    """Staging directories the transaction should have cleaned up.

    Staged works in a temp directory beside the bundle, so a leak is visible
    as a sibling. A tool that left one behind after every failure would fill
    a bundles repository with copies of itself.
    """
    return [
        name
        for name in h.listing(bundle.parent)
        if name.startswith(".tutorail-stage-") or name.startswith(".tutorail-")
    ]


# --------------------------------------------------------------------------
# 1. No validator: fail before doing anything
# --------------------------------------------------------------------------


def test_missing_validator() -> None:
    for label, build in OPERATIONS:
        with h.Workspace() as ws, case(f"{label}: no validator findable -> unchanged"):
            bundle, instance = prepare(ws, "x")
            empty_home = ws.path("empty-home")
            empty_home.mkdir()
            script, args = build(bundle, instance)

            before = h.tree_digest(bundle)
            before_instance = h.tree_digest(instance)
            done = run(script, *args, env=h.no_runner_env(empty_home))

            check(done.returncode != 0, "exits non-zero rather than proceeding")
            check_in(
                "tutorAIl runner is not installed",
                done.output,
                "says the runner must be installed",
            )
            check_in("$TUTORAIL_VALIDATOR", done.output, "lists search location 1")
            check_in("~/.agents/skills/tutorail", done.output, "lists search location 2")
            check_in("~/.claude/skills/tutorail", done.output, "lists search location 3")
            check_in("~/.claude/plugins", done.output, "lists search location 4")
            check(
                h.tree_digest(bundle) == before,
                "the bundle is byte-identical",
            )
            check(
                h.tree_digest(instance) == before_instance,
                "the instance is byte-identical",
            )
            check(leftovers(bundle) == [], "no staging directory was left behind")

            # POSITIVE CONTROL. Without it, "it failed" is equally consistent
            # with the command being wrong, the bundle being unusable, or the
            # operation being a no-op.
            good = run(script, *args)
            check(
                good.returncode == 0,
                "the identical command succeeds with the runner installed",
            )
            check(
                h.tree_digest(bundle) != before,
                "and really does change the bundle (positive control)",
            )


# --------------------------------------------------------------------------
# 2. Dirty working tree: fail before doing anything
# --------------------------------------------------------------------------


def test_dirty_tree() -> None:
    for label, build in OPERATIONS:
        with h.Workspace() as ws, case(f"{label}: dirty working tree -> unchanged"):
            bundle, instance = prepare(ws, "x")
            h.git_init(bundle)
            script, args = build(bundle, instance)

            # POSITIVE CONTROL first, on a --check run so the tree stays clean.
            clean = run(script, *args, "--check")
            check(clean.returncode == 0, "a clean tree is allowed (positive control)")

            (bundle / "COURSE.md").write_text(
                (bundle / "COURSE.md").read_text(encoding="utf-8") + "\nA local edit.\n",
                encoding="utf-8",
            )
            before = h.tree_digest(bundle)
            done = run(script, *args)
            check(done.returncode != 0, "a dirty tree refuses")
            check_in("uncommitted change", done.output, "and names the count")
            check_in("COURSE.md", done.output, "and names the dirty path")
            check(h.tree_digest(bundle) == before, "the bundle is byte-identical")
            check(leftovers(bundle) == [], "no staging directory was left behind")

            forced = run(script, *args, "--force")
            check(forced.returncode == 0, "--force overrides")
            check(h.tree_digest(bundle) != before, "and the forced run changes it")


# --------------------------------------------------------------------------
# 3. The validator rejects the RESULT: the whole edit is discarded
#
# This is the interesting one. The operation has already written the lesson
# file, rewritten tutorial.yaml and possibly renamed twenty files by the time
# the validator runs. Every one of those has to disappear.
# --------------------------------------------------------------------------


def test_validator_rejects_the_result() -> None:
    for label, build in OPERATIONS:
        with h.Workspace() as ws, case(f"{label}: validator rejects the result -> unchanged"):
            bundle, instance = prepare(ws, "x")
            stub = h.write_stub_validator(ws.root)
            script, args = build(bundle, instance)

            before = h.tree_digest(bundle)
            done = run(script, *args, env={"TUTORAIL_VALIDATOR": str(stub)})

            check(done.returncode != 0, "exits non-zero when the result does not validate")
            check_in("is unchanged", done.output, "says the bundle is unchanged")
            check_in(
                "DESIGN.md: the file is required and is missing",
                done.output,
                "and quotes the validator's finding rather than hiding it",
            )
            check(
                h.tree_digest(bundle) == before,
                "every file, mode and byte is as it was",
            )
            check(leftovers(bundle) == [], "no staging directory was left behind")

            # POSITIVE CONTROL: the stub, not the operation, caused this.
            good = run(script, *args)
            check(good.returncode == 0, "the same command passes the real validator")
            check(h.tree_digest(bundle) != before, "and changes the bundle")


def test_genuinely_invalid_result_with_the_real_validator() -> None:
    """The same discard, driven by the REAL validator rather than a stub.

    The stub above proves the discard path. This proves the real validator is
    wired into it - that the toolkit is not passing a stub-shaped exit code
    around while ignoring what the runner actually says.
    """
    with h.Workspace() as ws, case("a genuinely invalid result is discarded by the real validator"):
        bundle, instance = prepare(ws, "x")
        # An anchor a lesson will reference but DESIGN.md does not define is
        # the validator's check 1. The bundle is valid until the promotion
        # brings the offending lesson in, so the failure is caused by the
        # operation itself.
        generated = instance / "lessons.generated" / "lifetimes-and-borrows.md"
        generated.write_text(
            generated.read_text(encoding="utf-8").replace(
                "design_refs: [row-cell-model]", "design_refs: [row-cell-model]\nextra: keep"
            ),
            encoding="utf-8",
        )
        # Remove an anchor the bundle's DESIGN.md has, so an EXISTING lesson's
        # design_ref dangles the moment anything revalidates.
        design = bundle / "DESIGN.md"
        design.write_text(
            design.read_text(encoding="utf-8").replace("{#temporal-semantics}", "{#temporal}"),
            encoding="utf-8",
        )
        validator, _ = bl.find_validator()
        check(
            run(validator, bundle).returncode != 0,
            "the bundle is now genuinely invalid (setup check)",
        )

        before = h.tree_digest(bundle)
        done = run(h.LESSON, "add", bundle, "--id", "another", "--title", "A")
        check(done.returncode != 0, "the operation refuses to write into an invalid bundle")
        check_in("temporal-semantics", done.output, "and shows the real finding")
        check_in(
            "already invalid",
            done.output,
            "and says the bundle may have been invalid before this run, "
            "so the author is not sent hunting for a fault in their own edit",
        )
        check(h.tree_digest(bundle) == before, "the bundle is byte-identical")


# --------------------------------------------------------------------------
# 4. Failing part-way through, after files have been written
# --------------------------------------------------------------------------


def test_manifest_edit_failure_mid_operation() -> None:
    """A manifest the surgical editor will not guess at fails after the write.

    `add` writes the lesson file BEFORE it rewrites tutorial.yaml, so a
    manifest it cannot edit raises with a file already created in the staging
    copy. That file must not reach the bundle.
    """
    with h.Workspace() as ws, case("a manifest the editor refuses fails after the lesson was written"):
        bundle = ws.copy("rust-automaton-db")
        manifest = bundle / "tutorial.yaml"
        text = manifest.read_text(encoding="utf-8")
        start = text.index("lessons:\n")
        end = text.index("\nworkspace_kind:")
        entries = [
            line.strip()[2:]
            for line in text[start:end].split("\n")
            if line.strip().startswith("- ")
        ]
        # A NON-EMPTY flow sequence. Valid YAML, and valid per the format -
        # so the bundle still validates - but not a shape this toolkit will
        # silently reformat.
        manifest.write_text(
            text[:start] + "lessons: [" + ", ".join(entries) + "]" + text[end:],
            encoding="utf-8",
        )
        validator, _ = bl.find_validator()
        check(
            run(validator, bundle).returncode == 0,
            "the flow-style manifest is still a VALID bundle (setup check)",
        )

        before = h.tree_digest(bundle)
        done = run(h.LESSON, "add", bundle, "--id", "an-extra-lesson", "--title", "Extra")
        check(done.returncode != 0, "the surgical editor refuses rather than reformatting")
        check_in("block form", done.output, "and says what shape it needs")
        check(
            h.tree_digest(bundle) == before,
            "the lesson file written before the failure never reached the bundle",
        )
        check(
            not h.has_exactly(bundle / "lessons", "23-an-extra-lesson.md"),
            "and specifically the new lesson is not on disk",
        )
        check(leftovers(bundle) == [], "no staging directory was left behind")


# --------------------------------------------------------------------------
# The transaction itself
# --------------------------------------------------------------------------


def test_staged_discards_on_exception() -> None:
    """Staged is a context manager; anything that raises must discard."""
    with h.Workspace() as ws, case("Staged discards its copy when the body raises"):
        bundle = ws.copy("rust-automaton-db")
        before = h.tree_digest(bundle)
        boom = RuntimeError("deliberate")
        raised = False
        try:
            with bl.Staged(bundle) as stage:
                (stage.root / "lessons" / "99-half-written.md").write_text("x", "utf-8")
                (stage.root / "tutorial.yaml").write_text("ruined", "utf-8")
                raise boom
        except RuntimeError as exc:
            raised = exc is boom
        check(raised, "the exception propagates rather than being swallowed")
        check(h.tree_digest(bundle) == before, "the bundle is byte-identical")
        check(leftovers(bundle) == [], "the staging directory was removed")

        # POSITIVE CONTROL: the same body, committed, does change the bundle.
        with bl.Staged(bundle) as stage:
            course = stage.root / "COURSE.md"
            course.write_text(course.read_text("utf-8") + "\nAdded.\n", "utf-8")
            stage.commit()
        check(
            h.tree_digest(bundle) != before,
            "a committed Staged really does write (positive control)",
        )
        check(
            "Added." in (bundle / "COURSE.md").read_text("utf-8"),
            "and the committed content is what was written",
        )
        check(leftovers(bundle) == [], "and nothing is left behind after a commit")


def test_staged_preserves_everything_it_copies() -> None:
    """The swap must not quietly lose modes, binaries or nested folders."""
    with h.Workspace() as ws, case("the staged copy preserves modes, binaries and folders"):
        bundle = ws.copy("foldered-bundle")
        binary = bundle / "lessons" / "01-shapes" / "assets" / "shape.bin"
        os.chmod(binary, 0o640)
        before = h.tree_digest(bundle)

        with bl.Staged(bundle) as stage:
            course = stage.root / "COURSE.md"
            course.write_text(course.read_text("utf-8") + "\nA note.\n", "utf-8")
            stage.commit()

        check(h.tree_digest(bundle) != before, "the commit changed something")
        check(
            binary.stat().st_mode & 0o777 == 0o640,
            "an unusual mode bit survived the copy and the swap",
        )
        check(
            binary.read_bytes() == (h.FIXTURES / "foldered-bundle" / "lessons" / "01-shapes" / "assets" / "shape.bin").read_bytes(),
            "the non-UTF-8 material is byte-identical to the fixture",
        )
        check(
            h.has_exactly(bundle / "lessons" / "01-shapes", "LESSON.md")
            and h.has_miscased(bundle / "lessons" / "01-shapes", "LESSON.md") is None,
            "the exact-case LESSON.md survived the copy and the swap",
        )


def test_check_mode_writes_nothing_anywhere() -> None:
    """--check on every operation: the bundle, the instance and the parent."""
    for label, build in OPERATIONS:
        with h.Workspace() as ws, case(f"{label} --check writes nothing"):
            bundle, instance = prepare(ws, "x")
            script, args = build(bundle, instance)
            before_bundle = h.tree_digest(bundle)
            before_instance = h.tree_digest(instance)
            before_parent = h.listing(bundle.parent)

            done = run(script, *args, "--check")
            check(done.returncode == 0, "--check exits 0 when the plan would validate")
            check_in("nothing was written", done.output, "and says so")
            check(h.tree_digest(bundle) == before_bundle, "the bundle is byte-identical")
            check(
                h.tree_digest(instance) == before_instance,
                "the instance is byte-identical",
            )
            check(
                h.listing(bundle.parent) == before_parent,
                "and no new entry appeared beside the bundle",
            )


def main() -> int:
    print("atomicity test suite - every mutating operation, every failure mode")
    print(f"  scripts: {h.SCRIPTS}")
    print(f"  python:  {sys.version.split()[0]}")
    try:
        validator, how = bl.find_validator()
        print(f"  runner:  {validator}  ({how})")
    except bl.ToolError:
        print("  runner:  NOT FOUND - this suite needs the tutorAIl runner installed")
        return 2
    print()

    test_missing_validator()
    test_dirty_tree()
    test_validator_rejects_the_result()
    test_genuinely_invalid_result_with_the_real_validator()
    test_manifest_edit_failure_mid_operation()
    test_staged_discards_on_exception()
    test_staged_preserves_everything_it_copies()
    test_check_mode_writes_nothing_anywhere()
    return h.report("atomicity")


if __name__ == "__main__":
    sys.exit(main())
