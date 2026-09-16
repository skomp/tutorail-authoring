#!/usr/bin/env python3
"""index.py - the compact bundle index.

Run: python3 tests/test_index.py

index.py exists so an interview about restructuring one chapter of a 23-lesson,
~2,700-line course does not begin by loading the course. Two properties carry
that promise, and both are easy to claim and hard to check:

  * the index is SHORT - the design says roughly 40 lines for 23 lessons, so
    this asserts the real line count rather than "it is not enormous";
  * the index reads FRONTMATTER ONLY, with the single documented exception of
    the first line of each `## Purpose` section.

The second is tested with a sentinel and a POSITIVE CONTROL. Asserting that a
unique string buried under `## Theory` is absent from the output proves nothing
on its own - a probe that looks for the wrong string, or an index that printed
nothing at all, would pass it too. So the same sentinel is also placed on the
first line of `## Purpose` in a second copy, where it MUST appear. Only the two
together say anything.

Every failure flag below is shown firing against a deliberately broken copy of
a fixture, and each one is paired with the unmodified fixture as its control.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    FIXTURES,
    INDEX,
    Workspace,
    case,
    check,
    check_in,
    check_not_in,
    has_exactly,
    listing,
    report,
    run,
)


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

ANCHOR_RE = re.compile(r"\{#([A-Za-z0-9][A-Za-z0-9._-]*)\}")
ROW_RE = re.compile(r"^\s{0,3}(\d+) (\S+) +(file|folder) +d:(\S+) v:(.*?)(?:  ⚑ (.*?))?  ·  (.*)$")


def edit(path: Path, old: str, new: str) -> None:
    """Replace `old` with `new`, and refuse to be a silent no-op.

    A fixture mutation that did not actually change anything is the cheapest
    way to build a test that can only pass, so the substitution is verified
    rather than assumed.
    """
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise AssertionError(f"{path}: fixture text {old!r} not found; the edit would do nothing")
    replaced = text.replace(old, new, 1)
    if replaced == text:
        raise AssertionError(f"{path}: replacing {old!r} changed nothing")
    path.write_text(replaced, encoding="utf-8")


def rows(output: str) -> list[re.Match]:
    return [m for m in (ROW_RE.match(line) for line in output.splitlines()) if m]


def row_for(output: str, lesson_id: str) -> re.Match | None:
    for match in rows(output):
        if match.group(2) == lesson_id:
            return match
    return None


VALID_LESSON = """---
id: {slug}
title: {title}
design_refs: [naming]
validators: [manual]
---

## Purpose

{purpose}

## Completion conditions

The learner can say so.
"""


# --------------------------------------------------------------------------
# Cases
# --------------------------------------------------------------------------


def case_real_course() -> None:
    """The 23-lesson course: short, complete, and a header that names the bundle."""
    bundle = FIXTURES / "rust-automaton-db"
    done = run(INDEX, bundle)
    check(done.returncode == 0, f"rust-automaton-db: exit 0 (got {done.returncode}; stderr={done.stderr.strip()!r})")

    lines = done.stdout.splitlines()
    # The design promises "roughly 40 lines for a 23-lesson course". Assert the
    # real number, not a vague ceiling: a regression that doubled the output
    # would still sit under any generous bound.
    check(
        len(lines) == 29,
        f"rust-automaton-db: the index is exactly 29 lines (got {len(lines)})",
    )
    check(
        len(lines) <= 40,
        f"rust-automaton-db: the index is at most the ~40 lines the design allows (got {len(lines)})",
    )

    check(
        lines[0] == "rust-automaton-db — Learn Rust by Building AutomatonDB",
        f"header line 1 names bundle id and title (got {lines[0]!r})",
    )
    check(
        lines[1]
        == "23 lessons (23 file, 0 folder) · level intermediate-to-advanced"
        " · workspace existing-or-new-repository · bundle_format 1",
        f"header line 2 names count, form split, level, workspace_kind (got {lines[1]!r})",
    )
    check(
        lines[2] == "validators declared: cargo-check cargo-run cargo-test git-diff has-lib manual",
        f"header line 3 names every validator tutorial.yaml declares (got {lines[2]!r})",
    )

    # The anchor count is re-derived here from DESIGN.md rather than copied out
    # of the index, so this asserts the VALUE index.py computed, not its shape.
    anchors = set(ANCHOR_RE.findall((bundle / "DESIGN.md").read_text(encoding="utf-8")))
    check(len(anchors) == 23, f"the fixture's DESIGN.md really carries 23 anchors (got {len(anchors)})")
    check(
        lines[3].startswith(f"DESIGN.md anchors ({len(anchors)}): "),
        f"header line 4 names the DESIGN.md anchor count (got {lines[3]!r})",
    )

    slugs = sorted(name[:-3] for name in listing(bundle / "lessons") if name.endswith(".md"))
    check(len(slugs) == 23, f"the fixture really holds 23 lesson files (got {len(slugs)})")
    missing = [slug for slug in slugs if row_for(done.stdout, slug) is None]
    check(not missing, f"every one of the 23 lesson ids has a row ({len(missing)} missing: {missing[:3]})")


def case_every_field_per_lesson() -> None:
    """Each row carries id, form, design_refs, validators and a purpose line."""
    bundle = FIXTURES / "rust-automaton-db"
    done = run(INDEX, bundle)
    parsed = rows(done.stdout)
    check(len(parsed) == 23, f"23 lesson rows parse with every field present (got {len(parsed)})")

    # Every row must carry a non-empty purpose-or-title. An empty tail would
    # parse fine and say nothing, so the value is asserted, not the shape.
    empty = [m.group(2) for m in parsed if not m.group(7).strip()]
    check(not empty, f"every row ends in a non-empty purpose or title (empty for {empty})")
    bad_form = [m.group(2) for m in parsed if m.group(3) not in ("file", "folder")]
    check(not bad_form, f"every row's form is 'file' or 'folder' (bad: {bad_form})")

    row = row_for(done.stdout, "03-first-refactor")
    check(row is not None, "03-first-refactor has a row")
    if row is None:
        return

    check(row.group(3) == "file", f"03-first-refactor form is 'file' (got {row.group(3)!r})")
    check(
        row.group(4) == "table-model,row-cell-model,partition-key,clustering-key",
        f"03-first-refactor carries its real design_refs in order (got {row.group(4)!r})",
    )
    # Its validators differ from the common set, and the index prints the
    # DELTA. The three it adds on top of cargo-check/cargo-test are these.
    check(
        row.group(5).strip() == "+git-diff +has-lib +manual",
        f"03-first-refactor's validator delta is +git-diff +has-lib +manual (got {row.group(5).strip()!r})",
    )

    # purpose_line joins the wrapped source lines of `## Purpose`, so the text
    # must run past the first hard-wrapped line of the real lesson file. The
    # tail of the sentence is clipped at 110 characters, so only the part that
    # survives the clip is asserted.
    expected = (
        "Use real structural pressure in a growing `main.rs` to teach Rust's "
        "binary/library distinction, modules,"
    )
    check(
        row.group(7).startswith(expected),
        f"03-first-refactor's purpose is the real first sentence of its ## Purpose "
        f"section, wrapped lines joined (got {row.group(7)!r})",
    )


def case_form_discriminates() -> None:
    """`folder` and `file` are told apart, not merely printed."""
    done = run(INDEX, FIXTURES / "foldered-bundle")
    check(done.returncode == 0, f"foldered-bundle: exit 0 (got {done.returncode})")

    foldered = row_for(done.stdout, "01-shapes")
    single = row_for(done.stdout, "00-start")
    check(foldered is not None and single is not None, "both lessons have rows")
    if foldered is None or single is None:
        return
    check(foldered.group(3) == "folder", f"01-shapes is reported as form 'folder' (got {foldered.group(3)!r})")
    # The discriminating half: a script that hardcoded one word would pass the
    # assertion above. This one fails unless the two forms really differ.
    check(foldered.group(3) != "file", "01-shapes is NOT reported as form 'file'")
    check(single.group(3) == "file", f"00-start is reported as form 'file' (got {single.group(3)!r})")
    check(
        "2 lessons (1 file, 1 folder)" in done.stdout,
        "the header counts 1 file and 1 folder",
    )


def case_unlisted_fires() -> None:
    """A lesson on disk that tutorial.yaml does not list."""
    with Workspace() as ws:
        # POSITIVE CONTROL first: the untouched fixture must be silent and green,
        # otherwise the firing case below proves nothing about the new file.
        clean = run(INDEX, ws.copy("foldered-bundle", "clean"))
        check(clean.returncode == 0, f"control: the unmodified fixture exits 0 (got {clean.returncode})")
        check_not_in("UNLISTED", clean.output, "control: the unmodified fixture prints no UNLISTED")

        bundle = ws.copy("foldered-bundle", "broken")
        (bundle / "lessons" / "02-extra.md").write_text(
            VALID_LESSON.format(slug="02-extra", title="An extra lesson", purpose="A lesson nobody listed."),
            encoding="utf-8",
        )
        check(
            has_exactly(bundle / "lessons", "02-extra.md"),
            f"the unlisted lesson file is really on disk under its exact name "
            f"(saw {listing(bundle / 'lessons')})",
        )

        done = run(INDEX, bundle)
        check_in("UNLISTED", done.output, "an unlisted lesson on disk is flagged UNLISTED")
        row = row_for(done.stdout, "02-extra")
        check(row is not None and "UNLISTED" in (row.group(6) or ""), "the UNLISTED flag is on the offending row")
        # A lesson on disk but not in `lessons:` is the mirror image of a lesson
        # in `lessons:` but not on disk, and the runner's own validator fails
        # the bundle for it (its check 4). The index must not report it as a
        # clean bundle.
        check(
            done.returncode == 1,
            f"an unlisted lesson makes index.py exit 1 (got {done.returncode})",
        )


def case_id_not_slug_fires() -> None:
    """Frontmatter `id` that disagrees with the file's slug."""
    with Workspace() as ws:
        clean = run(INDEX, ws.copy("foldered-bundle", "clean"))
        check_not_in("id≠slug", clean.output, "control: the unmodified fixture prints no id≠slug")

        bundle = ws.copy("foldered-bundle", "broken")
        edit(bundle / "lessons" / "00-start.md", "id: 00-start", "id: totally-wrong")
        done = run(INDEX, bundle)
        # Naming the real slug is the point: the flag has to say what the id
        # should have been, or the author cannot act on it.
        check_in("id≠slug(00-start)", done.output, "a mismatched id is flagged, naming the real slug")
        row = row_for(done.stdout, "totally-wrong")
        check(row is not None, "the row is keyed by the frontmatter id that was actually read")


def case_dangling_ref_fires() -> None:
    """A design_refs anchor DESIGN.md does not define."""
    with Workspace() as ws:
        clean = run(INDEX, ws.copy("foldered-bundle", "clean"))
        check_not_in("refs-dangle", clean.output, "control: the unmodified fixture prints no refs-dangle")

        bundle = ws.copy("foldered-bundle", "broken")
        anchors = set(ANCHOR_RE.findall((bundle / "DESIGN.md").read_text(encoding="utf-8")))
        check(
            "ghost-anchor" not in anchors and anchors == {"naming", "shape-model"},
            f"the fixture's DESIGN.md defines exactly naming and shape-model (got {sorted(anchors)})",
        )
        edit(bundle / "lessons" / "00-start.md", "design_refs: [naming]", "design_refs: [naming, ghost-anchor]")
        done = run(INDEX, bundle)
        check_in("refs-dangle:ghost-anchor", done.output, "a dangling design_refs anchor is flagged by name")
        check_not_in(
            "refs-dangle:naming",
            done.output,
            "the anchor DESIGN.md does define is not flagged (the flag discriminates)",
        )


def case_undeclared_validator_fires() -> None:
    """A validator name tutorial.yaml never declared."""
    with Workspace() as ws:
        clean = run(INDEX, ws.copy("foldered-bundle", "clean"))
        check_not_in("val-undeclared", clean.output, "control: the unmodified fixture prints no val-undeclared")

        bundle = ws.copy("foldered-bundle", "broken")
        edit(bundle / "lessons" / "00-start.md", "validators: [manual]", "validators: [manual, cargo-test]")
        done = run(INDEX, bundle)
        check_in("val-undeclared:cargo-test", done.output, "an undeclared validator is flagged by name")
        check_not_in(
            "val-undeclared:manual",
            done.output,
            "the validator that IS declared is not flagged (the flag discriminates)",
        )


def case_listed_but_absent_fires() -> None:
    """A lessons entry in tutorial.yaml with no file behind it."""
    with Workspace() as ws:
        clean = run(INDEX, ws.copy("foldered-bundle", "clean"))
        check(clean.returncode == 0, f"control: the unmodified fixture exits 0 (got {clean.returncode})")
        check_not_in(
            "lessons listed in tutorial.yaml that are not on disk",
            clean.output,
            "control: the unmodified fixture reports no missing lesson",
        )

        bundle = ws.copy("foldered-bundle", "broken")
        (bundle / "lessons" / "00-start.md").unlink()
        check(
            not has_exactly(bundle / "lessons", "00-start.md"),
            f"the lesson file is really gone - checked by listing, not exists() "
            f"(saw {listing(bundle / 'lessons')})",
        )

        done = run(INDEX, bundle)
        check_in(
            "lessons listed in tutorial.yaml that are not on disk:",
            done.output,
            "a listed lesson with no file is reported under its own heading",
        )
        check_in("  lessons/00-start.md", done.output, "the missing entry is named by its manifest path")
        check(done.returncode == 1, f"a listed-but-absent lesson exits 1 (got {done.returncode})")


SENTINEL = "ZQX-SENTINEL-7f3a91"


def case_frontmatter_only() -> None:
    """The contract: frontmatter only, plus the first line of ## Purpose.

    The absence check below is worthless alone - so the SAME sentinel is put on
    the first line of ## Purpose in a second copy and must appear. One copy
    proves index.py can see the sentinel at all; the other proves it does not
    read that far down the file.
    """
    with Workspace() as ws:
        deep = ws.copy("foldered-bundle", "deep")
        edit(
            deep / "lessons" / "01-shapes" / "LESSON.md",
            "## Theory\n\nFor the worked example",
            f"## Theory\n\n{SENTINEL} is buried here, well below the Purpose section.\nFor the worked example",
        )
        deep_run = run(INDEX, deep)
        check(deep_run.returncode == 0, f"the deep-sentinel bundle still indexes cleanly (got {deep_run.returncode})")
        check_not_in(
            SENTINEL,
            deep_run.output,
            "a sentinel under ## Theory never reaches the index (no lesson body is read)",
        )

        # POSITIVE CONTROL. Without this the assertion above would pass against
        # an index.py that printed nothing, or against a typo in SENTINEL.
        shallow = ws.copy("foldered-bundle", "shallow")
        edit(
            shallow / "lessons" / "01-shapes" / "LESSON.md",
            "Introduce the shape model and the material that goes with it.",
            f"{SENTINEL} introduces the shape model.",
        )
        shallow_run = run(INDEX, shallow)
        check_in(
            SENTINEL,
            shallow_run.output,
            "control: the same sentinel on the first ## Purpose line DOES appear",
        )
        row = row_for(shallow_run.stdout, "01-shapes")
        check(
            row is not None and row.group(7).startswith(SENTINEL),
            "control: the sentinel arrives as that lesson's purpose text, not somewhere incidental",
        )


def case_no_purpose_section() -> None:
    """A lesson with no ## Purpose at all falls back to the title.

    This case carries a SECOND, DELIBERATE job, and it must not be tidied away.

    `foldered-bundle/lessons/00-start.md` writes its title as an UNQUOTED
    scalar containing a colon followed by a space. Plain YAML does not permit
    that; the runner's restricted reader accepts it. After
    tutorail-authoring#21 quoted the two titles in the rust-automaton-db
    fixture - where they were wrong, because the live bundle quotes them -
    this is the ONLY place in the suite where that lenient path is exercised,
    and the only place where a lesson title's parsed value is asserted
    verbatim. It lives here rather than in a bundle copy because
    foldered-bundle is synthetic: nothing ever synchronises it against a live
    bundle, so the colon cannot be "corrected" away by a later sync.

    If the reader is changed to reject an unquoted colon scalar - a question
    that belongs to skomp/tutorAIl, which owns it - this case is what fails,
    and it is meant to fail rather than be quietly re-quoted.
    """
    with Workspace() as ws:
        bundle = ws.copy("foldered-bundle", "no-purpose")
        # The construct under test, asserted on disk rather than assumed: the
        # title line must really be unquoted and must really contain ": ".
        # Without this the assertion below could pass against a quoted title
        # and the lenient path would be uncovered with nobody told.
        raw = (bundle / "lessons" / "00-start.md").read_text(encoding="utf-8")
        title_line = next(
            (ln for ln in raw.splitlines() if ln.startswith("title:")), ""
        )
        check(
            title_line == "title: Getting started: the naming rule",
            f"DELIBERATE COVERAGE: the fixture's title is an unquoted scalar "
            f"holding ': ' (got {title_line!r}; see the docstring above and the "
            f"note in the fixture before changing either)",
        )
        check(
            '"' not in title_line and "'" not in title_line,
            f"DELIBERATE COVERAGE: that title carries no quotes, so the reader "
            f"is really taking the lenient path (got {title_line!r})",
        )

        edit(
            bundle / "lessons" / "00-start.md",
            "## Purpose\n\nEstablish the vocabulary the rest of the course uses.\n\n## Prerequisites",
            "## Prerequisites",
        )
        text = (bundle / "lessons" / "00-start.md").read_text(encoding="utf-8")
        check("## Purpose" not in text, "the fixture copy really has no ## Purpose section left")

        done = run(INDEX, bundle)
        check(done.returncode == 0, f"a lesson with no ## Purpose does not crash index.py (exit {done.returncode})")
        row = row_for(done.stdout, "00-start")
        check(row is not None, "the purpose-less lesson still gets a row")
        if row is not None:
            check(
                row.group(7) == "Getting started: the naming rule",
                f"the row falls back to the frontmatter title (got {row.group(7)!r})",
            )
            # The discriminating half. A reader that stopped at the colon would
            # return "Getting started" and still look like a plausible title,
            # so assert the text AFTER the colon survived the parse.
            check(
                row.group(7).endswith(": the naming rule"),
                f"the unquoted colon scalar parsed whole, not truncated at the "
                f"colon (got {row.group(7)!r})",
            )
        # The other lesson still shows its own purpose, so the fallback is
        # per-lesson rather than a whole-bundle collapse to titles.
        other = row_for(done.stdout, "01-shapes")
        check(
            other is not None and other.group(7).startswith("Introduce the shape model"),
            "the untouched lesson still shows its purpose, not its title",
        )


def main() -> int:
    print(f"index.py  ({INDEX})")
    print()
    with case("the real 23-lesson course: short, complete, informative header"):
        case_real_course()
    with case("every lesson row carries id, form, design_refs, validators, purpose"):
        case_every_field_per_lesson()
    with case("file and folder forms are told apart"):
        case_form_discriminates()
    with case("FIRING: a lesson on disk that tutorial.yaml does not list"):
        case_unlisted_fires()
    with case("FIRING: frontmatter id that is not the slug"):
        case_id_not_slug_fires()
    with case("FIRING: a design_refs anchor DESIGN.md does not define"):
        case_dangling_ref_fires()
    with case("FIRING: a validator tutorial.yaml does not declare"):
        case_undeclared_validator_fires()
    with case("FIRING: a lessons entry with no file behind it"):
        case_listed_but_absent_fires()
    with case("frontmatter only: a sentinel deep in a body, and its positive control"):
        case_frontmatter_only()
    with case("a lesson with no ## Purpose section falls back to its title"):
        case_no_purpose_section()
    return report("index.py")


if __name__ == "__main__":
    sys.exit(main())
