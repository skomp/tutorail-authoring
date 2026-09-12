#!/usr/bin/env python3
"""audit.py - the evidence a course-quality review starts from.

Run: python3 tests/test_audit.py

`audit.py` lives in a different skill (`skills/course-quality/`) from every
other script this suite exercises, so it is run as a SUBPROCESS, exactly the
way every other suite here runs its script - never imported. `harness.py`
already inserts `skills/tutorail-authoring/scripts` onto `sys.path` for the
authoring scripts; a second insert for `skills/course-quality/scripts` would
put two script directories on one path, and any module name they share (this
script imports `bundlelib`, which is not its own) would then resolve by
insert order rather than by which directory actually owns it.

The toil scanner is a CANDIDATE GENERATOR, not a verdict, and this suite
tests that discipline directly with a real positive and a real negative
control, both drawn from the actual tutorail-bundles corpus:

  * POSITIVE - the copy-the-starter constraint from
    webgl-typescript-scene/lessons/00-project-setup/LESSON.md:34, reproduced
    in the `toil-course` fixture, must produce a candidate;
  * NEGATIVE - "Provide a direct-copy composition shader before adding
    effects.", from webgl-typescript-scene/lessons/15-render-to-texture.md:41
    and reproduced in the same fixture, contains the word "copy" and must
    NOT produce one. A scanner that fires on the bare word would pass the
    positive case and still be useless.

The coverage-list parser gets the same treatment: a fixture that HAS a list
proves it is read verbatim, and a second fixture - the same bundle with the
section deleted - proves absence comes back as `None`, not `[]`. Without the
second fixture, `None` is indistinguishable from a parser that returns an
empty result for every input, which is the one thing the field exists to
rule out.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    AUDIT,
    FIXTURES,
    case,
    check,
    report,
    run,
)


def audit_json(bundle: Path) -> dict:
    done = run(AUDIT, bundle, "--json")
    if done.returncode != 0:
        raise AssertionError(
            f"audit.py {bundle} --json exited {done.returncode}:\n{done.output}"
        )
    try:
        return json.loads(done.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"audit.py {bundle} --json did not print JSON: {exc}\n---\n{done.stdout}"
        ) from exc


# --------------------------------------------------------------------------
# Cases
# --------------------------------------------------------------------------


def case_positive_control_fires() -> None:
    """FIRING: the real copy-the-starter constraint is a candidate."""
    data = audit_json(FIXTURES / "toil-course")
    hits = [c for c in data["candidates"] if "starter/package.json" in c["text"]]
    check(len(hits) == 1, f"the copy-the-starter sentence is a candidate (got {len(hits)})")
    if hits:
        check(hits[0]["pattern"] == "copy", f"and it says which pattern matched (got {hits[0]['pattern']!r})")
        check(hits[0]["rel"] == "lessons/00-shader-basics.md", f"and which lesson it is in (got {hits[0]['rel']!r})")
        check(isinstance(hits[0]["line"], int) and hits[0]["line"] > 0, "and a 1-indexed line number")


def case_negative_control_silent() -> None:
    """NEGATIVE CONTROL: 'a direct-copy composition shader' never fires.

    This is not optional decoration - without it, a scanner that matches the
    bare word "copy" anywhere in a line would pass the positive case above
    and still be wrong. Both sentences contain "copy"; only one is an
    instruction to the learner.
    """
    data = audit_json(FIXTURES / "toil-course")
    hits = [c for c in data["candidates"] if "composition shader" in c["text"]]
    check(not hits, f"prose that merely contains 'copy' is not a candidate (got {hits})")
    # And the control itself must be real: the sentence has to actually be
    # present in the fixture, or the absence of a hit proves nothing.
    lesson_text = (FIXTURES / "toil-course" / "lessons" / "01-texture-work.md").read_text(encoding="utf-8")
    check(
        "Provide a direct-copy composition shader before adding effects." in lesson_text,
        "control: the real negative-control sentence is actually in the fixture",
    )


def case_coverage_list_verbatim() -> None:
    """The coverage list comes back verbatim, in order, under its own heading."""
    data = audit_json(FIXTURES / "toil-course")
    cov = data["coverage_list"]
    check(cov is not None, "toil-course declares a coverage list")
    if cov is None:
        return
    check(
        cov["heading"] == "Topics this course must cover",
        f"the heading the topics were found under is reported (got {cov['heading']!r})",
    )
    check(
        cov["topics"] == ["shader compilation", "depth testing", "texture sampling"],
        f"every topic is reported verbatim, in order (got {cov['topics']!r})",
    )


def case_no_coverage_reports_null() -> None:
    """NEGATIVE CONTROL: a course with no coverage list reports null, not empty.

    `toil-course-no-coverage` is the same fixture with the section deleted.
    Without this case, `coverage_list == {...}` above is equally consistent
    with a parser that cannot tell an absent section from an empty one,
    which is the exact distinction this field exists to make.
    """
    data = audit_json(FIXTURES / "toil-course-no-coverage")
    check(data["coverage_list"] is None, f"absent is null (got {data['coverage_list']!r})")
    check(data["coverage_list"] != [], "absent is not an empty list")

    # Positive control on the fixture pairing itself: the two bundles must
    # actually differ only in the coverage section, or this proves nothing
    # about the parser.
    with_cov = (FIXTURES / "toil-course" / "COURSE.md").read_text(encoding="utf-8")
    without_cov = (FIXTURES / "toil-course-no-coverage" / "COURSE.md").read_text(encoding="utf-8")
    check(
        "Topics this course must cover" in with_cov and "Topics this course must cover" not in without_cov,
        "control: the no-coverage fixture really has the section removed",
    )


def case_optional_lesson_inventoried() -> None:
    """An optional lesson is inventoried, not reported as unreachable.

    A lesson in `lessons/` is listed in `lessons` OR in `optional_lessons` -
    code that cross-references only the ordered `lessons:` list would find
    this one nowhere and report it as unreachable.
    """
    data = audit_json(FIXTURES / "toil-course")
    optional = [l for l in data["lessons"] if l["optional"]]
    check(len(optional) == 1, f"the optional lesson is listed (got {len(optional)})")
    if optional:
        check(
            optional[0]["rel"] == "lessons/debug-overlay.md",
            f"it is the one declared in optional_lessons (got {optional[0]['rel']!r})",
        )
    main = [l for l in data["lessons"] if not l["optional"]]
    check(len(main) == 2, f"the two main-path lessons are also listed, not optional (got {len(main)})")
    check(
        data["course"]["lesson_count"] == 2 and data["course"]["optional_lesson_count"] == 1,
        f"course carries the split too (got {data['course']})",
    )


def case_learning_objectives_and_frontmatter() -> None:
    """Each lesson row carries id, title, form, design_refs, validators, objectives."""
    data = audit_json(FIXTURES / "toil-course")
    by_rel = {l["rel"]: l for l in data["lessons"]}
    row = by_rel.get("lessons/00-shader-basics.md")
    check(row is not None, "00-shader-basics has a row")
    if row is None:
        return
    check(row["id"] == "00-shader-basics", f"id (got {row['id']!r})")
    check(row["title"] == "Shader compilation basics", f"title (got {row['title']!r})")
    check(row["form"] == "file", f"form (got {row['form']!r})")
    check(row["design_refs"] == ["pipeline"], f"design_refs (got {row['design_refs']!r})")
    check(row["validators"] == ["manual"], f"validators (got {row['validators']!r})")
    check(
        row["learning_objectives"]
        == ["Compile a vertex and fragment shader", "Link a shader program and check its status"],
        f"the ## Learning objectives bullets, verbatim (got {row['learning_objectives']!r})",
    )


def case_anchors_from_design() -> None:
    """DESIGN.md anchors are read via the real anchor regex, not guessed at."""
    import re

    data = audit_json(FIXTURES / "toil-course")
    real = set(
        re.findall(
            r"\{#([A-Za-z0-9][A-Za-z0-9._-]*)\}",
            (FIXTURES / "toil-course" / "DESIGN.md").read_text(encoding="utf-8"),
        )
    )
    check(real == {"pipeline", "sampling"}, f"control: the fixture really defines these two anchors (got {real})")
    check(sorted(data["anchors"]) == sorted(real), f"audit.py reports the same anchors (got {data['anchors']!r})")


def case_supplies_reported() -> None:
    """A declared supplies entry is reported with its scope."""
    data = audit_json(FIXTURES / "toil-course")
    check(len(data["supplies"]) == 1, f"exactly one supplies entry is declared (got {data['supplies']})")
    if data["supplies"]:
        entry = data["supplies"][0]
        check(entry["scope"] == "manifest", f"its scope is manifest (got {entry['scope']!r})")
        check(entry["from"] == "starter/vertex.glsl", f"from (got {entry['from']!r})")
        check(entry["to"] == "src/vertex.glsl", f"to (got {entry['to']!r})")


def case_topic_candidates_show_the_gap() -> None:
    """topic_candidates finds two topics and is honestly empty for the gap.

    Not part of the brief's required test list, but Step 4 requires
    `topic_candidates` to exist and to never claim coverage - this checks
    both: two topics get a real candidate lesson, and the deliberately
    uncovered third topic ("depth testing" - no lesson in the fixture
    mentions depth) comes back with an empty list rather than a guess.
    """
    data = audit_json(FIXTURES / "toil-course")
    topics = data["topic_candidates"]
    check(set(topics) == {"shader compilation", "depth testing", "texture sampling"}, f"got {sorted(topics)}")
    shader_hits = topics.get("shader compilation", [])
    texture_hits = topics.get("texture sampling", [])
    gap_hits = topics.get("depth testing", [])
    check(
        any(h["rel"] == "lessons/00-shader-basics.md" for h in shader_hits),
        f"'shader compilation' candidates include the lesson that teaches it (got {shader_hits})",
    )
    check(
        any(h["rel"] == "lessons/01-texture-work.md" for h in texture_hits),
        f"'texture sampling' candidates include the lesson that teaches it (got {texture_hits})",
    )
    check(gap_hits == [], f"'depth testing' - taught by no lesson - has no candidate (got {gap_hits})")


def case_json_and_markdown_agree_on_shape() -> None:
    """--json is well-formed and the default Markdown mode does not crash."""
    done = run(AUDIT, FIXTURES / "toil-course")
    check(done.returncode == 0, f"default (Markdown) mode exits 0 (got {done.returncode}; {done.output!r})")
    check(
        "candidate" in done.stdout.lower(),
        "the Markdown report names candidates, not a verdict",
    )
    check(
        "not evidence" in done.stdout.lower() or "never" in done.stdout.lower(),
        "the report states the candidate-generator disclaimer, not just the list",
    )


def main() -> int:
    print(f"audit.py  ({AUDIT})")
    print()
    with case("FIRING: the scanner fires on a real copy-the-starter constraint"):
        case_positive_control_fires()
    with case("NEGATIVE CONTROL: it does not fire on 'a direct-copy composition shader'"):
        case_negative_control_silent()
    with case("the coverage list comes back verbatim, under its own heading"):
        case_coverage_list_verbatim()
    with case("NEGATIVE CONTROL: a course with no coverage list reports null, not empty"):
        case_no_coverage_reports_null()
    with case("an optional lesson is inventoried, not reported as unreachable"):
        case_optional_lesson_inventoried()
    with case("each lesson row carries id, title, form, design_refs, validators, objectives"):
        case_learning_objectives_and_frontmatter()
    with case("DESIGN.md anchors are read via the real anchor regex"):
        case_anchors_from_design()
    with case("a declared supplies entry is reported with its scope"):
        case_supplies_reported()
    with case("topic_candidates finds two topics and stays honestly empty for the gap"):
        case_topic_candidates_show_the_gap()
    with case("--json is well-formed and the default Markdown mode states its own caveat"):
        case_json_and_markdown_agree_on_shape()
    return report("audit.py")


if __name__ == "__main__":
    sys.exit(main())
