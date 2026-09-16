#!/usr/bin/env python3
"""check_report.py - re-adding a finished course-quality report against itself.

Run: python3 tests/test_check_report.py

COST
====

`COST = "cheap"`. This suite spends no tokens and touches no bundle. It reads
reports, which is all the script under test does.

WHAT THIS SUITE IS ACTUALLY ABOUT
=================================

Two failure modes, and the second is the one that costs something.

**A check that finds nothing when a defect is there.** The audit of
2026-09-13 published five reports; two carried arithmetic defects that
survived publication and were found only when a second reader added the
columns. Those two reports, as they stood before commit `19c92f5`, are pinned
in `tests/fixtures/reports/` and are the positive control for the whole
script. If those two cases ever stop firing, the script is worthless whatever
else passes: it would be reporting clean on the exact input it exists for.

**A check that reports clean because it could not read the input.** This is
`CLAUDE.md`'s `FAIL - 0 finding(s)` in a new costume - a checker that found no
tables, found therefore no mismatch, and called that a pass. The reports are
hand-written Markdown and their table shapes differ between authors, so a
parser that goes blind on one author's shape is not a hypothetical. Three
fixtures exist for it: a report whose breakdowns are prose and not tables, a
report with no course-total block, and a report with one score cell the
parser cannot read. Each must come back BLIND (exit 2), never clean.

Beside it sits the opposite control, because a blindness signal nobody has
watched NOT fire is not a signal: `excluded-row.md` carries a row the report
itself marks "not an element", and that row must be excluded and reported as
excluded, not counted as a blind spot.

THE LIVE CORPUS, AND WHY A PASS ON IT MEANS SOMETHING
=====================================================

The suite also runs the script over the ten reports in `docs/audits/`. They
are expected to be clean - that is the acceptance criterion of
`skomp/tutorail-authoring#12`, and it is also a standing regression guard: a
report edited into inconsistency turns this suite red.

A clean run over ten files proves nothing on its own, so every one of those
ten is then MUTATED - one element score changed, and separately the course
total changed - and the mutant must be rejected. That is what separates "the
tables add up" from "the parser never found the tables".
"""

from __future__ import annotations

COST = "cheap"

import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    REPO,
    case,
    check,
    check_in,
    check_not_in,
    note,
    report,
    run,
)

CHECK_REPORT = REPO / "skills" / "course-quality" / "scripts" / "check_report.py"
REPORT_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "reports"
AUDIT_DIRS = [
    REPO / "docs" / "audits" / "2026-09-13",
    REPO / "docs" / "audits" / "2026-09-15",
]

CLEAN = 0
MISMATCH = 1
BLIND = 2


def live_reports() -> list[Path]:
    found: list[Path] = []
    for directory in AUDIT_DIRS:
        found.extend(sorted(directory.glob("*.md")))
    return found


def mutate(source: Path, anchor: str, before: str, after: str, target: Path) -> Path:
    """Copy `source` to `target`, changing `before` to `after` on one line.

    The line is found by content and never by number, so a fixture that grows
    a paragraph does not silently start mutating a different line.
    """
    lines = source.read_text(encoding="utf-8").splitlines()
    hits = [i for i, text in enumerate(lines) if anchor in text and before in text]
    assert len(hits) == 1, f"{source}: {anchor!r} + {before!r} matches {len(hits)} line(s)"
    lines[hits[0]] = lines[hits[0]].replace(before, after, 1)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def bump_total(source: Path, target: Path) -> Path:
    """Copy `source` with its stated COURSE TOTAL raised by one."""
    lines = source.read_text(encoding="utf-8").splitlines()
    for index, text in enumerate(lines):
        if "COURSE TOTAL" in text:
            found = list(re.finditer(r"\d+", text))
            assert found, f"{source}: the COURSE TOTAL line carries no figure"
            last = found[-1]
            lines[index] = text[: last.start()] + str(int(last.group()) + 1) + text[last.end():]
            target.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return target
    raise AssertionError(f"{source} has no COURSE TOTAL line")


ELEMENT_FIRST_CELL = re.compile(r"^[\s`*]*(?::?\d|[A-Za-z0-9_./-]+\.md:\d)")
ELEMENT_SCORE_CELL = re.compile(r"^\s*\**\s*\+?2\b")


def bump_one_element(source: Path, target: Path) -> Path | None:
    """Copy `source` with one +2 element row changed to +5.

    The row is found the way a reader finds one - a first cell that names a
    line, a last cell that starts with a score - rather than by importing the
    script under test, so the test cannot inherit the parser's blind spots.
    """
    lines = source.read_text(encoding="utf-8").splitlines()
    for index, text in enumerate(lines):
        if not text.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in text.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[0] or not cells[-1]:
            continue
        if not ELEMENT_FIRST_CELL.match(cells[0]):
            continue
        if not ELEMENT_SCORE_CELL.match(cells[-1]):
            continue
        prefix, sep, last = text.rstrip().rstrip("|").rpartition("|")
        lines[index] = prefix + sep + last.replace("2", "5", 1) + "|"
        target.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return target
    return None


# --------------------------------------------------------------------------
# 1. The positive control: the two defects that reached publication
# --------------------------------------------------------------------------

with case("the bytebeat lesson-01 addition error is reported, with both figures"):
    fixture = REPORT_FIXTURES / "pre-19c92f5-portable-bytebeat-wav.md"
    done = run(CHECK_REPORT, fixture)
    check(done.returncode == MISMATCH, f"exit {MISMATCH} on a mismatch (got {done.returncode})")
    check_in("lesson-sum", done.output, "the finding names the lesson-sum check")
    check_in("01-write-a-tone", done.output, "the finding names the lesson")
    check_in("states 12", done.output, "the finding carries the stated figure")
    check_in("sum to 10", done.output, "the finding carries the computed figure")
    check_in(f"{fixture}:173", done.output, "the finding carries the file and the line")
    note(
        "the report states 12 in four places - the heading, the sum line, the "
        "per-lesson summary table and the course arithmetic - and each is "
        "reported separately, with its own line number"
    )
    for wanted in ("the lesson heading", "the sum line under the table",
                   "the per-lesson summary table", "the course arithmetic"):
        check_in(wanted, done.output, f"the place that states 12 is named: {wanted}")

with case("the rate limiter's miscounted `teaching` elements are reported"):
    fixture = REPORT_FIXTURES / "pre-19c92f5-portable-fixed-window-rate-limiter.md"
    done = run(CHECK_REPORT, fixture)
    check(done.returncode == MISMATCH, f"exit {MISMATCH} on a mismatch (got {done.returncode})")
    check_in("category-count", done.output, "the finding names the category-count check")
    check_in("states 17 `teaching`", done.output, "the finding carries the stated count")
    check_in("tables hold 16", done.output, "the finding carries the counted rows")
    check_in(f"{fixture}:496", done.output, "the first statement is reported at its line")
    check_in(f"{fixture}:668", done.output, "the second statement is reported at its line")
    note("36 is the report's own element total and the check agrees with it, so only "
         "the `teaching` half of '17 of 36' is charged")
    check_not_in("scored element(s) in total", done.output,
                 "the element total of 36 is NOT reported as wrong")

with case("the two reports as they stand today carry neither defect"):
    for name in ("portable-bytebeat-wav.md", "portable-fixed-window-rate-limiter.md"):
        fixed = REPO / "docs" / "audits" / "2026-09-13" / name
        done = run(CHECK_REPORT, fixed)
        check(done.returncode == CLEAN, f"{name} is clean after 19c92f5 (exit {done.returncode})")

# --------------------------------------------------------------------------
# 2. Blind is not clean
# --------------------------------------------------------------------------

with case("a report whose breakdowns are prose comes back BLIND, not clean"):
    fixture = REPORT_FIXTURES / "blind-no-element-table.md"
    done = run(CHECK_REPORT, fixture)
    check(done.returncode == BLIND, f"exit {BLIND} when no element table is found (got {done.returncode})")
    check_in("no-element-tables", done.output, "the blind spot is named")
    check_in("0 element table(s)", done.output, "the readout says how many tables were found")
    check_not_in("OK -", done.output, "the run does not claim to be clean")

with case("a report with no course-total block comes back BLIND"):
    fixture = REPORT_FIXTURES / "blind-no-course-total.md"
    done = run(CHECK_REPORT, fixture)
    check(done.returncode == BLIND, f"exit {BLIND} when no total is found (got {done.returncode})")
    check_in("no-course-total", done.output, "the blind spot is named")
    check_in("course-total block(s): 0", done.output, "the readout says no total block was found")

with case("a score cell the parser cannot read comes back BLIND"):
    fixture = REPORT_FIXTURES / "blind-unreadable-score.md"
    done = run(CHECK_REPORT, fixture)
    check(done.returncode == BLIND, f"exit {BLIND} on an unreadable row (got {done.returncode})")
    check_in("unreadable-row", done.output, "the unreadable row is named")
    check_in("1 unreadable row(s)", done.output, "the readout counts it")
    check_in(f"{fixture}:34", done.output, "the unreadable row is reported at its line")

with case("the positive control for blindness: a row the REPORT excludes is not a blind spot"):
    fixture = REPORT_FIXTURES / "excluded-row.md"
    done = run(CHECK_REPORT, fixture)
    check(done.returncode == CLEAN, f"exit {CLEAN} on a deliberately unscored row (got {done.returncode})")
    check_in("1 row(s) the report itself marks unscored", done.output,
             "the excluded row is counted as excluded")
    check_in("0 unreadable row(s)", done.output, "and not as unreadable")
    check_in("the tables were found and they add up", done.output,
             "the clean message says WHICH clean result this is")

with case("a consistent report says the tables were found, not merely that nothing was wrong"):
    fixture = REPORT_FIXTURES / "consistent.md"
    done = run(CHECK_REPORT, fixture)
    check(done.returncode == CLEAN, f"exit {CLEAN} on a consistent report (got {done.returncode})")
    check_in("2 element table(s)", done.output, "the readout names the tables it read")
    check_in("9 element(s)", done.output, "the readout names the rows it re-added")
    check_in("the tables were found and they add up", done.output, "the clean message is specific")

# --------------------------------------------------------------------------
# 3. Each of the three comparisons bites
# --------------------------------------------------------------------------

SOURCE = REPORT_FIXTURES / "consistent.md"

with tempfile.TemporaryDirectory() as raw:
    workspace = Path(raw)

    with case("a lesson figure that disagrees with its element rows is reported"):
        target = mutate(SOURCE, "### `lessons/00-first.md`", "— 4", "— 5",
                        workspace / "lesson-figure.md")
        done = run(CHECK_REPORT, target)
        check(done.returncode == MISMATCH, f"exit {MISMATCH} (got {done.returncode})")
        check_in("lesson-sum", done.output, "the lesson-sum check fires")
        check_in("states 5", done.output, "the stated figure is quoted")
        check_in("sum to 4", done.output, "the computed figure is quoted")

    with case("a per-lesson summary figure that disagrees with the element rows is reported"):
        target = mutate(SOURCE, "| `lessons/01-second.md`", "**3**", "**2**",
                        workspace / "summary-figure.md")
        done = run(CHECK_REPORT, target)
        check(done.returncode == MISMATCH, f"exit {MISMATCH} (got {done.returncode})")
        check_in("the per-lesson summary table states 2", done.output,
                 "the summary table is named as the place that states it")

    with case("a course total that does not equal the lessons plus the penalties is reported"):
        target = mutate(SOURCE, "COURSE TOTAL", "       4", "       5",
                        workspace / "course-total.md")
        done = run(CHECK_REPORT, target)
        check(done.returncode == MISMATCH, f"exit {MISMATCH} (got {done.returncode})")
        check_in("course-total", done.output, "the course-total check fires")
        check_in("states a total of 5", done.output, "the stated total is quoted")
        check_in("sum to 4", done.output, "the re-added figure is quoted")

    with case("a lesson subtotal that does not equal its own lesson lines is reported"):
        target = mutate(SOURCE, "sum of lessons", "     7", "     8",
                        workspace / "subtotal.md")
        done = run(CHECK_REPORT, target)
        check(done.returncode == MISMATCH, f"exit {MISMATCH} (got {done.returncode})")
        check_in("lesson-subtotal", done.output, "the subtotal check fires")

    with case("a stated category count that disagrees with the rows is reported"):
        target = mutate(SOURCE, "scored elements are", "3 of 9", "4 of 9",
                        workspace / "category.md")
        done = run(CHECK_REPORT, target)
        check(done.returncode == MISMATCH, f"exit {MISMATCH} (got {done.returncode})")
        check_in("category-count", done.output, "the category-count check fires")
        check_in("states 4 `teaching`", done.output, "the stated count is quoted")
        check_in("tables hold 3", done.output, "the counted rows are quoted")

    with case("a stated element total that disagrees with the rows is reported"):
        target = mutate(SOURCE, "scored elements are", "3 of 9", "3 of 11",
                        workspace / "element-total.md")
        done = run(CHECK_REPORT, target)
        check(done.returncode == MISMATCH, f"exit {MISMATCH} (got {done.returncode})")
        check_in("states 11 scored element(s) in total", done.output,
                 "the stated element total is quoted")
        check_in("tables hold 9", done.output, "the counted elements are quoted")

# --------------------------------------------------------------------------
# 4. The live corpus, and the mutation that proves the pass
# --------------------------------------------------------------------------

with case("every published report in docs/audits/ is consistent with itself"):
    found = live_reports()
    check(len(found) == 10, f"ten published reports were found (got {len(found)})")
    done = run(CHECK_REPORT, *found)
    check(done.returncode == CLEAN, f"the published corpus is clean (exit {done.returncode})")
    check_in("0 mismatch(es); 0 blind spot(s)", done.output, "no mismatch and no blind spot")
    check_not_in("0 element table(s)", done.output, "no report was read with zero tables")

with tempfile.TemporaryDirectory() as raw:
    workspace = Path(raw)
    with case("and every one of them rejects a single injected error"):
        for source in live_reports():
            label = f"{source.parent.name}/{source.name}"

            # One element row, anywhere in the file, moved by three points.
            target = bump_one_element(source, workspace / f"element-{source.name}")
            if target is None:
                check(False, f"{label}: no element row was found to mutate")
            else:
                done = run(CHECK_REPORT, target)
                check(
                    done.returncode == MISMATCH and "lesson-sum" in done.output,
                    f"{label}: a changed element score is caught "
                    f"(exit {done.returncode})",
                )

            # The course total itself.
            target = bump_total(source, workspace / f"total-{source.name}")
            done = run(CHECK_REPORT, target)
            check(
                done.returncode == MISMATCH and "course-total" in done.output,
                f"{label}: a changed course total is caught (exit {done.returncode})",
            )

with case("the checker reads reports and nothing else"):
    text = CHECK_REPORT.read_text(encoding="utf-8")
    for forbidden in ("tutorial.yaml", "validate_bundle", "TUTORAIL_VALIDATOR"):
        check_not_in(forbidden, text, f"check_report.py does not reach for {forbidden}")
    note("the script reads the report only. It reads no bundle and computes no score, "
         "which is what keeps it clear of the rule that audit.py computes no score.")

sys.exit(report("check_report.py"))
