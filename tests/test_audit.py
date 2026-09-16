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
proves it is read verbatim, a second fixture - the same bundle with the
section deleted - proves absence comes back as `None`, not `[]`, and a THIRD
case (a copy of the second with just the heading re-added, no topics under
it) proves a declared-but-empty list is neither of the other two. Without
each control, its neighbour is indistinguishable from a parser that cannot
tell the cases apart.

Fix round 1 narrowed `move` and `unzip`/`extract` to require a file-or-path
token on the same line, after both patterns turned out to have zero observed
true positives across the two real bundles while firing constantly on
ordinary technical prose. `copy` was deliberately left alone - it produced
both of this scanner's required true positives. The narrowing is tested with
both halves, using the real corpus sentences for the negative half wherever
one already existed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    AUDIT,
    FIXTURES,
    Workspace,
    case,
    check,
    check_in,
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


def case_semicolon_lead_fires() -> None:
    """FIRING (fix round 2, DEFECT 1): a verb after a semicolon-space.

    The regenerated webgl-typescript-scene catalogue still carries, at
    lessons/01-canvas-and-context/LESSON.md:42, the exact five-file copy
    instruction whose presence in lesson 00 is what started this whole
    change: "... the tutor MUST read `starter/README.md`; copy
    `starter/package.json`, ...". Round 1's `_LEAD` had no semicolon
    alternative, so this produced ZERO candidates - a scanner that misses
    the sentence that started the work, in a bundle where it is still
    present, is not doing its job. Reproduced verbatim in its own fixture,
    `toil-course-semicolon`, per the review's explicit instruction.
    """
    data = audit_json(FIXTURES / "toil-course-semicolon")
    hits = [c for c in data["candidates"] if "starter/README.md" in c["text"]]
    check(len(hits) >= 1, f"the semicolon-led 'copy' fires (got {data['candidates']})")
    if hits:
        check(hits[0]["pattern"] == "copy", f"pattern is 'copy' (got {hits[0]['pattern']!r})")

    lesson_text = (FIXTURES / "toil-course-semicolon" / "lessons" / "00-bootstrap.md").read_text(
        encoding="utf-8"
    )
    check(
        "starter/README.md`; copy" in lesson_text,
        "control: the real semicolon-led sentence is actually in the fixture",
    )


def case_wrapped_noun_stays_silent() -> None:
    """NEGATIVE CONTROL (fix round 2, DEFECT 2): a hard-wrapped NOUN is not
    an imperative just because it lands at a physical line's start.

    Reproduces, verbatim and with the real line wrap, the false positive at
    durable-event-broker/lessons/14-asynchronous-follower.md:30: "... the
    leader acknowledges without waiting for it. Therefore the\ncopy is
    neither a quorum ...". The article "the" that makes "copy" a NOUN sits
    on the PREVIOUS physical line; a per-line scan cannot see that, which is
    why the unit of scanning had to become the paragraph, not the line.
    """
    data = audit_json(FIXTURES / "toil-course-semicolon")
    hits = [c for c in data["candidates"] if "neither a quorum" in c["text"]]
    check(not hits, f"the wrapped noun 'copy' does not fire (got {hits})")
    hits2 = [c for c in data["candidates"] if "create another copy" in c["text"]]
    check(not hits2, f"the other 'copy' in the same paragraph does not fire either (got {hits2})")

    lesson_text = (FIXTURES / "toil-course-semicolon" / "lessons" / "00-bootstrap.md").read_text(
        encoding="utf-8"
    )
    check(
        "copy is neither a quorum nor a failover protocol." in lesson_text,
        "control: the real noun-copy sentence, with its real line wrap, is actually in the fixture",
    )


def case_move_and_extract_require_a_path_token() -> None:
    """`move` and `unzip`/`extract` are narrowed: they need a file-or-path
    token (a backticked path, or a recognisable file extension) on the same
    line.

    Both verbs were dropped to zero observed true positives across the two
    real bundles during this tool's own verification, while firing on
    ordinary technical prose that has no file anywhere in sight. `copy` is
    deliberately NOT narrowed - see case_copy_is_not_narrowed.

    Both negative halves here are the REAL sentences from the corpus, not
    invented ones:

      * "Move from clip-space drawing to a genuine 3D coordinate pipeline."
        - webgl-typescript-scene/lessons/05-transforms-and-perspective.md:10
      * "Extract one supported mesh primitive into the existing `MeshData`
        representation" - webgl-typescript-scene/lessons/13-load-gltf-model/
        LESSON.md:21 (a Learning objectives bullet there too)

    No real `move`/`unzip` true positive exists in either corpus (that is
    the whole reason for this change), so the positive halves are
    necessarily invented, in the same prose style as the rest of the fixture.
    """
    data = audit_json(FIXTURES / "toil-course")

    move_fires = [c for c in data["candidates"] if "checker.png" in c["text"]]
    check(len(move_fires) == 1, f"a 'move' with a real path token fires (got {move_fires})")
    if move_fires:
        check(move_fires[0]["pattern"] == "move", f"pattern is 'move' (got {move_fires[0]['pattern']!r})")

    move_silent = [c for c in data["candidates"] if "clip-space drawing" in c["text"]]
    check(
        not move_silent,
        f"the real corpus sentence about clip-space drawing still does not fire - "
        f"no path token, ordinary prose (got {move_silent})",
    )

    unzip_fires = [c for c in data["candidates"] if "textures.zip" in c["text"]]
    check(len(unzip_fires) == 1, f"an 'unzip' with a real path token fires (got {unzip_fires})")
    if unzip_fires:
        check(unzip_fires[0]["pattern"] == "unzip", f"pattern is 'unzip' (got {unzip_fires[0]['pattern']!r})")

    unzip_silent = [c for c in data["candidates"] if "MeshData" in c["text"]]
    check(
        not unzip_silent,
        f"the real corpus sentence about extracting a mesh primitive still does not "
        f"fire - the backticked `MeshData` token has no '.' or '/' inside it, so it "
        f"is not a path (got {unzip_silent})",
    )

    # Positive control on the fixture itself: the real negative sentences
    # really are present verbatim, or the absence checks above prove nothing.
    lesson_text = (FIXTURES / "toil-course" / "lessons" / "01-texture-work.md").read_text(encoding="utf-8")
    check(
        "Move from clip-space drawing to a genuine 3D coordinate pipeline." in lesson_text,
        "control: the real 'move' negative sentence is actually in the fixture",
    )
    check(
        "Extract one supported mesh primitive into the existing `MeshData` representation" in lesson_text,
        "control: the real 'extract' negative sentence is actually in the fixture",
    )


def case_copy_is_not_narrowed() -> None:
    """`copy` keeps firing with no path token at all - it was deliberately
    left as it was, because it is the one pattern that produced both of
    this scanner's required true positives.
    """
    data = audit_json(FIXTURES / "toil-course")
    hits = [c for c in data["candidates"] if "without rounding" in c["text"]]
    check(
        len(hits) == 1,
        f"'Copy the reference values exactly as given, without rounding.' has no "
        f"backtick, no '/', no file extension anywhere on the line, and still "
        f"fires (got {hits})",
    )
    if hits:
        check(hits[0]["pattern"] == "copy", f"pattern is 'copy' (got {hits[0]['pattern']!r})")


def case_coverage_heading_with_no_topics() -> None:
    """A heading that says 'cover' but lists nothing is a THIRD, distinct case
    from both "no coverage list at all" and "a coverage list with topics".

    Built from `toil-course-no-coverage` (which has neither the heading nor
    any topics) by inserting the real heading text with no bullets under it,
    so the only variable between this case and case_no_coverage_reports_null
    is whether the heading is there at all.
    """
    with Workspace() as ws:
        bundle = ws.copy("toil-course-no-coverage", "empty-heading")
        path = bundle / "COURSE.md"
        text = path.read_text(encoding="utf-8")
        check("## Optional lessons" in text, "fixture sanity: the anchor point for the edit is present")
        edited = text.replace(
            "## Optional lessons",
            "## Topics this course must cover\n\n## Optional lessons",
            1,
        )
        check(edited != text, "the edit actually changed the fixture copy")
        path.write_text(edited, encoding="utf-8")

        data = audit_json(bundle)
        cov = data["coverage_list"]
        check(cov is not None, f"a declared-but-empty coverage list is NOT null (got {cov!r})")
        if cov is not None:
            check(
                cov["heading"] == "Topics this course must cover",
                f"the heading is still reported (got {cov.get('heading')!r})",
            )
            check(
                cov["topics"] == [],
                f"topics is an explicit empty list, distinct from the null case (got {cov.get('topics')!r})",
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


def case_topic_candidates_stem_and_read_concepts() -> None:
    """FIRING (fix round 2, DEFECT 3): a plural topic matches a lesson that
    only ever uses the singular, and only in `## Concepts to teach`.

    The real miss was durable-event-broker's coverage-list topic
    "checksums" against `02-record-framing`, which teaches it by name four
    times but never as the exact plural, and mostly under `## Concepts to
    teach`, which round 1 never read. Reproduced here: the coverage list's
    only topic is "checksums" (plural); the fixture's only lesson never
    uses that word anywhere except "frame checksum verification" (singular)
    in `## Concepts to teach` - not in its title, slug, design_refs or
    learning objectives. Both the stemming fix and the concepts-to-teach fix
    are needed together for this to match; either alone is not enough.
    """
    data = audit_json(FIXTURES / "toil-course-semicolon")
    cov = data["coverage_list"]
    check(cov is not None and cov["topics"] == ["checksums"], f"fixture sanity: the topic is 'checksums' (got {cov!r})")

    hits = data["topic_candidates"].get("checksums", [])
    check(
        any(h["rel"] == "lessons/00-bootstrap.md" for h in hits),
        f"'checksums' (plural, coverage list) matches the lesson that only ever says "
        f"'checksum' (singular), and only in Concepts to teach (got {hits})",
    )

    lesson_text = (FIXTURES / "toil-course-semicolon" / "lessons" / "00-bootstrap.md").read_text(
        encoding="utf-8"
    )
    check(
        "checksum" in lesson_text.lower() and "checksums" not in lesson_text.lower(),
        "control: the fixture really uses only the singular form, nowhere the plural",
    )
    check(
        "frame checksum verification" in lesson_text
        and lesson_text.index("## Concepts to teach") < lesson_text.index("frame checksum verification")
        < lesson_text.index("## Constraints"),
        "control: the singular form really lives only in Concepts to teach",
    )


# --------------------------------------------------------------------------
# Short symbols a lesson uses and nothing introduces (tutorail-authoring#14).
#
# Every case below reads `symbol-course`, a fixture built to carry ONE symbol
# of each binding kind, so that each bucket has a control and no bucket can
# be mistaken for a constant:
#
#   `N` - introduced by a '## Concepts to teach' bullet AND by a defining
#         sentence beside its first use. This is the shape of
#         portable-fixed-window-rate-limiter after its own fix, and it is
#         here as a FIXTURE rather than as a read of the sibling bundles
#         repository, which is being edited and would change under this file.
#   `K` - mentioned ONLY by a DESIGN.md anchor. The runner loads an anchor
#         for the TUTOR, so this introduces nothing to a learner, and the
#         issue requires it be reported apart from "introduced nowhere".
#   `Q` - introduced nowhere at all.
#
# plus `N + 1` and `2N` (the multi-character spans that must never be lost -
# `2N` is the adversarial one, a two-character span built from a
# one-character symbol, which the issue's own suggested "single uppercase
# letter only" rule would drop silently) and the negatives `bool`, `New` and
# `starter/package.json`.
# --------------------------------------------------------------------------


def symbol_evidence(bundle: Path) -> dict:
    return audit_json(bundle)["symbol_evidence"]


def bucket(ev: dict, name: str, channel: str | None = None) -> list[dict]:
    """The candidates in one binding bucket, optionally of ONE channel.

    tutorail-authoring#18 added two more candidate channels to the same list
    (`concept-phrase` and `acronym`). Every case below that was written for
    the short-token channel of #14 now names that channel explicitly, so a
    #14 assertion cannot be silently satisfied - or silently broken - by a
    row the #18 channels produced.
    """
    rows = [c for c in ev["candidates"] if c["binding"] == name]
    if channel is not None:
        rows = [c for c in rows if c["channel"] == channel]
    return rows


def case_symbol_nothing_introduces_is_reported() -> None:
    """FIRING: a symbol a lesson uses and nothing anywhere introduces."""
    ev = symbol_evidence(FIXTURES / "symbol-course")
    unbound = bucket(ev, "none", "short-token")
    check(len(unbound) == 1, f"exactly one short-token symbol is bound nowhere (got {unbound})")
    if not unbound:
        return
    row = unbound[0]
    check(row["symbol"] == "Q", f"it is `Q` (got {row['symbol']!r})")
    check(
        row["first_use"]["rel"] == "lessons/01-counting.md",
        f"the lesson of the first use is reported (got {row['first_use']['rel']!r})",
    )
    check(
        isinstance(row["first_use"]["line"], int) and row["first_use"]["line"] > 0,
        f"with a 1-indexed line (got {row['first_use']['line']!r})",
    )
    check(row["named_in_concepts"] == [], f"no '## Concepts to teach' names it (got {row['named_in_concepts']})")
    check(row["defined_in_window"] is None, "no defining sentence near the first use")
    check(row["defined_elsewhere_in_lesson"] == [], "none elsewhere in the same lesson either")
    check(row["defined_in_other_lessons"] == [], "and none in any other lesson")
    check(row["design_md"] is None, f"and DESIGN.md does not mention it (got {row['design_md']})")

    # Controls: the line really says what the report says, and `Q` really is
    # absent from every other place the scanner looks. Without these the
    # report above is equally consistent with a scanner that cannot read.
    lesson = FIXTURES / "symbol-course" / "lessons" / "01-counting.md"
    text = lesson.read_text(encoding="utf-8").splitlines()
    check(
        "`Q`" in text[row["first_use"]["line"] - 1],
        f"control: line {row['first_use']['line']} of the fixture really uses `Q` "
        f"(it says {text[row['first_use']['line'] - 1]!r})",
    )
    design = (FIXTURES / "symbol-course" / "DESIGN.md").read_text(encoding="utf-8")
    check("`Q`" not in design, "control: the fixture's DESIGN.md really never mentions `Q`")


def case_design_md_only_is_a_distinct_bucket() -> None:
    """FIRING: a symbol only a DESIGN.md anchor binds is its OWN category.

    The issue's acceptance criteria require "defined only in DESIGN.md" to be
    separated from "defined nowhere", because the runner loads an anchor for
    the TUTOR and not for the learner - a DESIGN.md binding does not
    introduce a symbol to a learner. Reported together, the two would be
    indistinguishable and the author could not tell which fix each needs.
    """
    ev = symbol_evidence(FIXTURES / "symbol-course")
    design_only = bucket(ev, "design-md-only", "short-token")
    check(len(design_only) == 1, f"exactly one symbol is bound only in DESIGN.md (got {design_only})")
    if not design_only:
        return
    row = design_only[0]
    check(row["symbol"] == "K", f"it is `K` (got {row['symbol']!r})")
    check(row["design_md"] is not None, "its DESIGN.md binding is reported")
    if row["design_md"]:
        check(
            row["design_md"]["anchors"] == ["sharding"],
            f"with the anchor it sits under (got {row['design_md']['anchors']!r})",
        )
    check(row["named_in_concepts"] == [], "no '## Concepts to teach' names it")
    check(row["defined_in_window"] is None, "no defining sentence near the first use")
    check(row["defined_in_other_lessons"] == [], "and no lesson defines it anywhere")

    # THE DISTINCTION ITSELF: `K` and `Q` must not land in the same bucket.
    check(
        {c["symbol"] for c in design_only} != {c["symbol"] for c in bucket(ev, "none")},
        "'bound only in DESIGN.md' and 'bound nowhere' are different buckets",
    )
    check(
        row["binding"] != "none",
        f"`K` is NOT reported as bound nowhere (got {row['binding']!r})",
    )

    design = (FIXTURES / "symbol-course" / "DESIGN.md").read_text(encoding="utf-8")
    check("`K`" in design, "control: the fixture's DESIGN.md really does mention `K`")
    for rel in ("lessons/00-contract.md", "lessons/01-counting.md"):
        body = (FIXTURES / "symbol-course" / rel).read_text(encoding="utf-8")
        check(
            "Concepts to teach" in body and "`K`" not in body.split("## Concepts to teach")[1],
            f"control: {rel} really does not name `K` in its concepts section",
        )


def case_design_md_binding_is_not_a_constant() -> None:
    """NEGATIVE CONTROL for the case above: take the DESIGN.md line away and
    `K` must fall through to "bound nowhere".

    Without this, `K` landing in `design-md-only` is equally consistent with
    a scanner that puts everything it does not understand there.
    """
    with Workspace() as ws:
        bundle = ws.copy("symbol-course", "no-design-binding")
        path = bundle / "DESIGN.md"
        text = path.read_text(encoding="utf-8")
        check("The shard count `K` fixes" in text, "fixture sanity: the DESIGN.md binding is there to remove")
        edited = text.replace("The shard count `K` fixes", "The shard count fixes")
        check(edited != text, "the edit actually changed the fixture copy")
        path.write_text(edited, encoding="utf-8")

        ev = symbol_evidence(bundle)
        left = bucket(ev, "design-md-only", "short-token")
        check(left == [], f"no short token is DESIGN.md-only any more (got {left})")
        unbound = sorted(c["symbol"] for c in bucket(ev, "none", "short-token"))
        check(unbound == ["K", "Q"], f"`K` has fallen through to 'bound nowhere', beside `Q` (got {unbound})")


def case_introduced_symbol_is_not_reported_as_unbound() -> None:
    """NEGATIVE CONTROL: a symbol a lesson really does introduce comes back
    CLEAN, and the report says which channel introduced it.

    This is the shape of `portable-fixed-window-rate-limiter` after its own
    fix - `N` defined in prose beside its first use AND listed under '##
    Concepts to teach' - reproduced as a fixture rather than read from the
    sibling bundles repository, which is being edited concurrently and would
    change under this file. A scanner that reported `N` here would be wrong
    about the real bundle too.

    tutorail-authoring#18 changed WHICH channel is reported as introducing
    it. `concepts` used to outrank every prose bucket, so the report showed
    the weakest evidence and hid the strongest; the issue states that a
    symbol named in '## Concepts to teach' is NOT thereby introduced, and the
    row passes on a defining sentence. So the binding is now the defining
    sentence, and the Concepts bullet is still printed beside it.
    """
    ev = symbol_evidence(FIXTURES / "symbol-course")
    n_rows = [c for c in ev["candidates"] if c["symbol"] == "N"]
    check(len(n_rows) == 3, f"`N` is used in all three lessons and every use is tabulated (got {len(n_rows)})")
    check(
        all(c["binding"].endswith("prose") or c["binding"] == "lesson-prose-in-window" for c in n_rows),
        f"every use of `N` is reported as introduced by a DEFINING SENTENCE, "
        f"not by the weaker concepts bullet (got {[c['binding'] for c in n_rows]})",
    )
    check(
        n_rows[0]["binding"] == "lesson-prose-in-window",
        f"the first use is bound by the sentence beside it (got {n_rows[0]['binding']!r})",
    )
    check(
        all(c["named_in_concepts"] for c in n_rows),
        "and the concepts bullet is still reported on every row, never dropped",
    )
    check(
        not any(c["symbol"] == "N" for c in bucket(ev, "none")),
        "`N` is NOT in the 'bound nowhere' bucket",
    )
    first = n_rows[0]
    check(
        first["defined_in_window"] is not None,
        f"and the defining sentence beside its first use is reported too (got {first['defined_in_window']})",
    )
    if first["defined_in_window"]:
        check(
            "is the" in first["defined_in_window"]["sentence"],
            f"quoted, so a reader can overrule it (got {first['defined_in_window']['sentence']!r})",
        )
    check(
        any(h["form"] == "backticked" for h in first["named_in_concepts"]),
        f"and the concepts bullet that names it (got {first['named_in_concepts']})",
    )


def case_multi_character_span_is_not_lost() -> None:
    """FIRING: `N + 1` yields the symbol `N`, with the span AS WRITTEN.

    The issue names `N + 1` as a symbol that must survive collection. A rule
    that measured the LENGTH OF THE WHOLE BACKTICKED SPAN would throw it away
    at five characters; the length bound is a property of the TOKEN, and the
    span is kept beside it so nothing a reader needs is flattened away.
    """
    ev = symbol_evidence(FIXTURES / "symbol-course")
    row = next(
        (c for c in ev["candidates"] if c["lesson"] == "lessons/01-counting.md" and c["symbol"] == "N"),
        None,
    )
    check(row is not None, "the `N` in lessons/01-counting.md is a candidate at all")
    if row is None:
        return
    check(
        row["first_use"]["span"] == "N + 1",
        f"its first use is the multi-character span, kept verbatim (got {row['first_use']['span']!r})",
    )
    lesson = (FIXTURES / "symbol-course" / "lessons" / "01-counting.md").read_text(encoding="utf-8")
    check("`N + 1`" in lesson, "control: the fixture really writes `N + 1`")
    check(
        lesson.index("`N + 1`") < lesson.index("The first `N` requests"),
        "control: and writes it BEFORE any bare `N`, so the span really is the first use",
    )


def case_derived_symbol_2n_is_not_lost() -> None:
    """FIRING: `2N` - a two-character span built from a one-character symbol.

    The adversarial case for the issue's own suggested rule. "Report a single
    uppercase letter only" loses `2N` SILENTLY, and the loss is exactly the
    kind the author's ruling warns about: `N` and `2N` are the same concept,
    while `bool` and `go` are a different kind of thing entirely, so the sort
    is categorical and not lexical. A lexical rule gets it backwards in both
    directions at once.

    This scanner keeps it because the length bound is a property of the
    IDENTIFIER TOKEN, not of the span: `2N` tokenizes to the literal `2` and
    the identifier `N`, so it resolves to the same symbol lesson 00 defines,
    and the span is reported verbatim beside it so the reader can see it was
    written `2N`. Whether "same concept as `N`, already introduced" is the
    right call is the READER's, and this test asserts only that the reader is
    shown the row.
    """
    ev = symbol_evidence(FIXTURES / "symbol-course")
    row = next((c for c in ev["candidates"] if c["lesson"] == "lessons/02-headroom.md"), None)
    check(row is not None, "the `2N` use is a candidate at all - it is NOT dropped")
    if row is None:
        return
    check(row["symbol"] == "N", f"it resolves to the one-character symbol `N` (got {row['symbol']!r})")
    check(
        row["first_use"]["span"] == "2N",
        f"and the span is reported as written, so the reader sees `2N` (got {row['first_use']['span']!r})",
    )
    check(
        row["first_use"]["rel"] == "lessons/02-headroom.md" and row["first_use"]["line"] > 0,
        f"with a file:line for the first use (got {row['first_use']['rel']}:{row['first_use']['line']})",
    )
    check(
        [h["rel"] for h in row["named_in_concepts"]] == ["lessons/00-contract.md"],
        f"and it resolves to the `N` lesson 00 introduces, not to nothing "
        f"(got {row['named_in_concepts']})",
    )
    check(
        row["binding"] == "other-lesson-prose",
        f"so its binding is the defining sentence lesson 00 carries, not the "
        f"weaker concepts bullet beside it (got {row['binding']!r})",
    )
    check(
        row["named_in_concepts"] != [],
        "with the concepts bullet still printed on the row",
    )

    lesson = (FIXTURES / "symbol-course" / "lessons" / "02-headroom.md").read_text(encoding="utf-8")
    check("`2N`" in lesson, "control: the fixture really writes `2N`")
    check("`N`" not in lesson, "control: and never writes a bare `N`, so the hit really came from `2N`")


def case_length_and_path_negatives_stay_silent() -> None:
    """NEGATIVE CONTROL: `bool`, `New` and a backticked path produce nothing.

    They are excluded by the SHAPE of the span and the LENGTH of the token -
    never by a denylist of words, which the author ruled out: this script
    must not try to tell a conceptual parameter from a language identifier.
    A two-character language identifier is still emitted, on purpose.
    """
    ev = symbol_evidence(FIXTURES / "symbol-course")
    symbols = {c["symbol"] for c in ev["candidates"] if c["channel"] == "short-token"}
    check(symbols == {"N", "K", "Q"}, f"only the three real short tokens are collected (got {sorted(symbols)})")
    for noise in ("bool", "New", "package", "json", "starter"):
        check(noise not in symbols, f"`{noise}` is not a candidate")

    lesson = (FIXTURES / "symbol-course" / "lessons" / "00-contract.md").read_text(encoding="utf-8")
    for needle in ("`bool`", "`New`", "`starter/package.json`"):
        check(needle in lesson, f"control: {needle} really is in the fixture, and still produced nothing")


def case_nothing_to_check_is_not_checked_and_clean() -> None:
    """The distinction this section exists to make visible.

    `FAIL - 0 finding(s)` is this repo's canonical example of a check that
    failed while reporting nothing. The analogue here is a bundle that yields
    an empty 'bound nowhere' list because nothing was ever looked at. Both
    bundles below have an EMPTY 'none' bucket and they mean opposite things,
    so the difference has to be legible in the JSON without reading the
    candidate list: `status` plus `warnings`.
    """
    clean = symbol_evidence(FIXTURES / "symbol-course")

    # `toil-course` is no longer candidate-free: tutorail-authoring#18 reads
    # its '## Concepts to teach' sections, and "Texture units, samplers,
    # wrapping, filtering." holds a multi-word term the lessons use. So the
    # empty half of this pair is BUILT, by replacing each Concepts section
    # with a single one-word term - which is also the control for the #18
    # candidate rule: take the multi-word concepts away and the candidates go
    # away with them.
    with Workspace() as ws:
        bundle = ws.copy("toil-course", "no-candidates")
        replacements = {
            "lessons/00-shader-basics.md": ("Compilation, linking, program status.", "Compilation."),
            "lessons/01-texture-work.md": ("Texture units, samplers, wrapping, filtering.", "Samplers."),
            "lessons/debug-overlay.md": ("Overlay rendering, bitmap glyphs, frame timing.", "Glyphs."),
        }
        for rel, (before, after) in replacements.items():
            path = bundle / rel
            text = path.read_text(encoding="utf-8")
            check(before in text, f"fixture sanity: {rel} really writes {before!r}")
            path.write_text(text.replace(before, after), encoding="utf-8")

        populated = symbol_evidence(FIXTURES / "toil-course")
        check(
            populated["scan"]["candidate_rows"] > 0,
            f"control: the unedited toil-course DOES yield concept candidates "
            f"(got {populated['scan']['candidate_rows']})",
        )

        empty = symbol_evidence(bundle)
        check(
            empty["scan"]["candidate_rows"] == 0,
            f"with one-word concepts it yields no candidate at all "
            f"(got {[c['symbol'] for c in empty['candidates']]})",
        )
        check(
            empty["status"] == "nothing-to-check",
            f"and says so: status is 'nothing-to-check' (got {empty['status']!r})",
        )
        check(empty["warnings"] != [], "with a warning saying why, never silence")
        check(
            any("NOT" in w for w in empty["warnings"]),
            f"that spells out that no candidate found is not no undefined symbol (got {empty['warnings']})",
        )
        check(
            clean["status"] == "checked",
            f"symbol-course, where every channel was alive, says 'checked' (got {clean['status']!r})",
        )
        check(clean["warnings"] == [], f"with no warnings (got {clean['warnings']})")
        check(
            empty["status"] != clean["status"],
            "so 'nothing to check' and 'checked' are never the same value",
        )

        # And the Markdown a reader actually reads must carry it too.
        done = run(AUDIT, bundle)
        check(done.returncode == 0, f"markdown mode exits 0 (got {done.returncode}; {done.output!r})")
        check_in("This section checked NOTHING", done.stdout, "the Markdown report says it checked nothing")


def case_blind_concepts_channel_is_announced() -> None:
    """A bundle with no '## Concepts to teach' anywhere has lost a channel.

    Its candidates are then reported as un-introduced by that channel because
    the channel does not exist, NOT because a reader checked it. Built from
    `symbol-course` by renaming the heading, so the only variable between
    this case and case_introduced_symbol_is_not_reported_as_unbound is
    whether the section is there at all.
    """
    with Workspace() as ws:
        bundle = ws.copy("symbol-course", "blind-concepts")
        for rel in (
            "lessons/00-contract.md",
            "lessons/01-counting.md",
            "lessons/02-headroom.md",
        ):
            path = bundle / rel
            text = path.read_text(encoding="utf-8")
            check("## Concepts to teach" in text, f"fixture sanity: {rel} has the section to rename")
            path.write_text(text.replace("## Concepts to teach", "## Ideas"), encoding="utf-8")

        ev = symbol_evidence(bundle)
        check(
            ev["scan"]["lessons_with_concepts_section"] == [],
            f"no lesson declares the section now (got {ev['scan']['lessons_with_concepts_section']})",
        )
        check(
            ev["status"] == "checked-with-blind-channels",
            f"status says a channel was blind (got {ev['status']!r})",
        )
        check(
            any("Concepts to teach" in w for w in ev["warnings"]),
            f"and a warning names it (got {ev['warnings']})",
        )
        check(
            not any(c["binding"] == "concepts" for c in ev["candidates"]),
            "with the channel gone, nothing is reported as introduced by it",
        )
        # `N` must not silently become "bound nowhere": its prose definition
        # is still there, and the scanner must still see it.
        n_first = next(c for c in ev["candidates"] if c["symbol"] == "N")
        check(
            n_first["binding"] == "lesson-prose-in-window",
            f"`N` falls back to its prose definition, not to 'nowhere' (got {n_first['binding']!r})",
        )


def case_symbol_section_renders_in_markdown() -> None:
    """The Markdown report carries the section, its rule, its window and its
    caveat - a reader who never opens the JSON must still see all four."""
    done = run(AUDIT, FIXTURES / "symbol-course")
    check(done.returncode == 0, f"markdown mode exits 0 (got {done.returncode}; {done.output!r})")
    check_in("## Short symbols a lesson uses", done.stdout, "the section is rendered")
    check_in("Candidate rule [short-token]:", done.stdout, "the short-token candidate rule is stated in the report itself")
    check_in("Candidate rule [concept-phrase]:", done.stdout, "so is the concept-phrase rule")
    check_in("Candidate rule [acronym]:", done.stdout, "so is the acronym rule")
    check_in("Window:", done.stdout, "so is the near-the-first-use window")
    check_in("TABULATION, not a verdict", done.stdout, "and the caveat that this is not a verdict")
    check_in("does NOT introduce the symbol to a learner", done.stdout, "the DESIGN.md caveat is spelled out")
    check_in("`Q` first used at lessons/01-counting.md:", done.stdout, "the unbound symbol is reported with a file:line")


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


# --------------------------------------------------------------------------
# A coverage list written inside a fenced block (tutorail-authoring#10).
#
# The measured defect: `audit.py` read the coverage list as Markdown list
# items ONLY. `rust-automaton-db/COURSE.md:225` opens a ```text fence holding
# 45 topics, so the script returned `topics: []` AND the Markdown report said
# the author "never filled it in" - a false statement that, believed, would
# have suppressed five real coverage gaps.
#
# The fixture is `tests/fixtures/rust-automaton-db`, which is IN THIS REPO
# and whose COURSE.md is the real one byte for byte. The sibling
# tutorail-bundles checkout is deliberately not read from here: it moves.
#
# Four cases, and each is a control on its neighbour:
#
#   * the fence IS read, and the count is exact (45, not 0 and not 46 - two
#     earlier write-ups said 46 and both were wrong);
#   * deleting the fence from a COPY drops the count to zero, so the 45
#     above cannot be a constant;
#   * list items still win where a course uses them, and an unread fence
#     beside them is announced as a blind channel rather than dropped;
#   * "could not read it" and "the author left it empty" are different
#     results, and both are different from "there is no coverage list".
# --------------------------------------------------------------------------

FENCED_TOPIC_COUNT = 45

# The status vocabulary `symbol_evidence` established. The coverage list is
# required to reuse it rather than invent a second one for the same idea, so
# this set is asserted against BOTH sections below.
_SYMBOL_STATUSES = {"checked", "checked-with-blind-channels", "nothing-to-check"}


def case_fenced_coverage_list_is_read() -> None:
    """FIRING (#10): the 45 topics inside a ```text fence are read."""
    data = audit_json(FIXTURES / "rust-automaton-db")
    cov = data["coverage_list"]
    check(cov is not None, "the fenced coverage list is not reported as absent")
    if cov is None:
        return
    check(
        cov["heading"] == "Rust coverage requirements",
        f"the heading is reported (got {cov['heading']!r})",
    )
    check(
        len(cov["topics"]) == FENCED_TOPIC_COUNT,
        f"exactly {FENCED_TOPIC_COUNT} topics are read (got {len(cov['topics'])})",
    )
    check(
        cov["topics"][:2] == ["Cargo and crates", "variables and mutability"],
        f"in document order, verbatim, from the first line of the fence "
        f"(got {cov['topics'][:2]!r})",
    )
    check(
        cov["topics"][-1] == "platform/FFI APIs if naturally required",
        f"through to the last line of the fence (got {cov['topics'][-1]!r})",
    )
    check(
        "```text" not in cov["topics"] and "```" not in cov["topics"],
        "and the fence markers themselves are not topics",
    )
    check(
        cov["scan"]["topic_source"] == "fenced-block",
        f"the report says which channel they came from (got {cov['scan']['topic_source']!r})",
    )
    check(cov["status"] == "checked", f"status is 'checked' (got {cov['status']!r})")
    check(cov["warnings"] == [], f"with no blind channel to warn about (got {cov['warnings']})")

    # The five topics the 2026-09-15 audit found unserved are the reason this
    # defect cost anything. If the parser loses any of them the -15 vanishes
    # again, so name them here rather than trusting the count alone.
    for topic in (
        "interior mutability",
        "atomics",
        "associated types",
        "Cargo workspaces",
        "refactoring across crate boundaries",
    ):
        check(topic in cov["topics"], f"the unserved topic {topic!r} is among them")

    # Controls on the fixture: the topics really are in a fence and really
    # are not list items, or this case proves nothing about fences.
    course = (FIXTURES / "rust-automaton-db" / "COURSE.md").read_text(encoding="utf-8")
    lines = course.splitlines()
    heading_at = lines.index("## Rust coverage requirements")
    section = lines[heading_at + 1 :]
    section = section[: next(i for i, l in enumerate(section) if l.startswith("## "))]
    check(
        any(l.startswith("```") for l in section),
        "control: the fixture's coverage section really does open a fence",
    )
    check(
        not any(l.lstrip().startswith(("- ", "* ")) for l in section),
        "control: and it carries NO Markdown list item, so list-item parsing "
        "cannot be what produced the topics above",
    )
    check(
        len([l for l in section if l.strip()]) > FENCED_TOPIC_COUNT,
        "control: the section holds more non-empty lines than topics (the prose "
        "line and the two fence markers), so a naive line count would not give 45",
    )


def case_fenced_topics_are_not_a_constant() -> None:
    """NEGATIVE CONTROL (#10): delete the fence and the 45 topics go away.

    Without this, `len(topics) == 45` above is equally consistent with a
    parser that reads the fence and with one that hard-codes the corpus.
    """
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db", "no-fence")
        path = bundle / "COURSE.md"
        lines = path.read_text(encoding="utf-8").splitlines()
        heading_at = lines.index("## Rust coverage requirements")
        opens = next(i for i in range(heading_at, len(lines)) if lines[i].startswith("```"))
        closes = next(i for i in range(opens + 1, len(lines)) if lines[i].startswith("```"))
        kept = lines[:opens] + lines[closes + 1 :]
        check(closes - opens - 1 == FENCED_TOPIC_COUNT, f"control: the fence really holds {FENCED_TOPIC_COUNT} lines (got {closes - opens - 1})")
        path.write_text("\n".join(kept) + "\n", encoding="utf-8")

        cov = audit_json(bundle)["coverage_list"]
        check(cov is not None, f"the heading alone still reports a section (got {cov!r})")
        if cov is None:
            return
        check(cov["topics"] == [], f"and with the fence gone there are no topics (got {len(cov['topics'])})")
        check(
            cov["scan"]["fenced_blocks"] == 0,
            f"the scan says no fenced block was found (got {cov['scan']['fenced_blocks']})",
        )


def case_list_items_win_and_an_unread_fence_is_announced() -> None:
    """NO REGRESSION (#10): list items still win, and a fence beside them is
    reported as a BLIND CHANNEL rather than silently dropped.

    The four bundles that use list items must not change, so list items take
    precedence. That precedence can lose topics, and the rule in this file is
    that a channel nobody read is named, never passed over in silence.
    """
    with Workspace() as ws:
        bundle = ws.copy("toil-course", "both-forms")
        path = bundle / "COURSE.md"
        text = path.read_text(encoding="utf-8")
        check("- texture sampling" in text, "fixture sanity: the last list item is where expected")
        edited = text.replace(
            "- texture sampling",
            "- texture sampling\n\n```text\nframebuffer objects\nmipmapping\n```",
            1,
        )
        check(edited != text, "the edit actually changed the fixture copy")
        path.write_text(edited, encoding="utf-8")

        cov = audit_json(bundle)["coverage_list"]
        check(cov is not None, "the section is still found")
        if cov is None:
            return
        check(
            cov["topics"] == ["shader compilation", "depth testing", "texture sampling"],
            f"the list items still win, unchanged (got {cov['topics']!r})",
        )
        check(
            cov["scan"]["topic_source"] == "list-items",
            f"and the report says so (got {cov['scan']['topic_source']!r})",
        )
        check(
            cov["status"] == "checked-with-blind-channels",
            f"but the status is NOT a clean 'checked' (got {cov['status']!r})",
        )
        joined = " ".join(cov["warnings"])
        check(
            "BLIND" in joined,
            f"a warning names the channel that went unread (got {cov['warnings']!r})",
        )
        check(
            "fenced" in joined.lower(),
            f"and says it was the fenced block (got {cov['warnings']!r})",
        )


def _coverage_of(ws: "Workspace", name: str, replacement: str) -> dict | None:
    """Build a bundle whose coverage section is `replacement`, and audit it."""
    bundle = ws.copy("toil-course-no-coverage", name)
    path = bundle / "COURSE.md"
    text = path.read_text(encoding="utf-8")
    assert "## Optional lessons" in text
    path.write_text(
        text.replace("## Optional lessons", replacement + "\n## Optional lessons", 1),
        encoding="utf-8",
    )
    return audit_json(bundle)["coverage_list"]


def case_unreadable_is_not_absent_and_not_empty() -> None:
    """#10, the requirement added on 2026-09-15: "no coverage list" and "a
    coverage list I could not read" must be different results.

    All THREE states are built from ONE fixture in ONE case, so the only
    variable between them is what sits under the heading:

      absent     -> null, no dict at all
      empty      -> nothing-to-check, scan.body_lines == 0
      unreadable -> nothing-to-check, scan.body_lines  > 0

    The vocabulary is `symbol_evidence`'s (`status` + `warnings`), not a
    second one invented for this field.
    """
    with Workspace() as ws:
        absent = audit_json(FIXTURES / "toil-course-no-coverage")["coverage_list"]
        empty = _coverage_of(ws, "empty-section", "## Topics this course must cover\n\n")
        unreadable = _coverage_of(
            ws,
            "unreadable-section",
            "## Topics this course must cover\n\n"
            "Shader compilation, depth testing and texture sampling, in a paragraph\n"
            "this parser does not know how to split into topics.\n\n",
        )

        check(absent is None, f"ABSENT is null (got {absent!r})")
        for name, cov in (("EMPTY", empty), ("UNREADABLE", unreadable)):
            check(cov is not None, f"{name} is a dict, not null - it is NOT the absent case")
        if empty is None or unreadable is None:
            return

        check(empty["topics"] == [] and unreadable["topics"] == [], "neither reports a topic")
        check(
            empty["status"] == "nothing-to-check",
            f"EMPTY status is 'nothing-to-check' (got {empty['status']!r})",
        )
        check(
            unreadable["status"] == "nothing-to-check",
            f"UNREADABLE status is 'nothing-to-check' too - nothing WAS read "
            f"(got {unreadable['status']!r})",
        )
        check(
            empty["status"] in _SYMBOL_STATUSES and unreadable["status"] in _SYMBOL_STATUSES,
            f"and both use symbol_evidence's vocabulary, not a second one "
            f"(got {empty['status']!r}, {unreadable['status']!r})",
        )
        # Control on that claim: `_SYMBOL_STATUSES` must really be the symbol
        # section's own words, not a list this test made up to agree with
        # itself. Take one from a live symbol_evidence run.
        live = audit_json(FIXTURES / "toil-course")["symbol_evidence"]["status"]
        check(
            live in _SYMBOL_STATUSES,
            f"control: symbol_evidence really does use these words (got {live!r})",
        )

        # The discriminator, machine-readable.
        check(
            empty["scan"]["body_lines"] == 0,
            f"EMPTY has nothing under the heading (got {empty['scan']['body_lines']})",
        )
        check(
            unreadable["scan"]["body_lines"] > 0,
            f"UNREADABLE has content under the heading (got {unreadable['scan']['body_lines']})",
        )
        check(
            empty["scan"] != unreadable["scan"],
            "so the two scans are not the same object with the same numbers",
        )

        # And in prose, because a human reads the warning, not the scan.
        empty_says = " ".join(empty["warnings"])
        unreadable_says = " ".join(unreadable["warnings"])
        check(
            "never filled it in" in empty_says,
            f"EMPTY warns that the author never filled the section in (got {empty_says!r})",
        )
        check(
            "never filled it in" not in unreadable_says,
            f"UNREADABLE must NOT say that - it is the false statement #10 is about "
            f"(got {unreadable_says!r})",
        )
        check(
            "NOTHING WAS READ" in unreadable_says,
            f"UNREADABLE says nothing was read (got {unreadable_says!r})",
        )
        check(
            "by hand" in unreadable_says,
            f"and sends the reader to COURSE.md (got {unreadable_says!r})",
        )


def case_markdown_never_claims_an_unread_section_is_empty() -> None:
    """#10 in the Markdown report, which is what the auditor of 2026-09-15
    actually read. The false sentence must be gone for a fenced list and must
    not reappear for an unreadable one."""
    done = run(AUDIT, FIXTURES / "rust-automaton-db")
    check(done.returncode == 0, f"the Markdown report exits 0 (got {done.returncode}; {done.output!r})")
    check(
        "never filled it in" not in done.stdout,
        "the report NO LONGER says the author never filled the section in",
    )
    check_in("Rust coverage requirements", done.stdout, "it names the heading")
    check_in("interior mutability", done.stdout, "and prints a topic that was invisible before")
    check_in("status: checked", done.stdout, "with the coverage-list status alongside it")

    with Workspace() as ws:
        bundle = ws.copy("toil-course-no-coverage", "unreadable-md")
        path = bundle / "COURSE.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace(
                "## Optional lessons",
                "## Topics this course must cover\n\nA paragraph, not a list.\n\n## Optional lessons",
                1,
            ),
            encoding="utf-8",
        )
        done = run(AUDIT, bundle)
        check(done.returncode == 0, f"and on an unreadable section it still exits 0 (got {done.returncode})")
        check_in("COULD NOT READ A TOPIC", done.stdout, "the report says it could not read the section")
        check(
            "never filled it in" not in done.stdout,
            "and does NOT tell the reader the author left it empty",
        )
        check(
            "declares no coverage list at all" not in done.stdout,
            "nor that the course declares no coverage list at all",
        )



# --------------------------------------------------------------------------
# tutorail-authoring#18 - the concept-phrase and acronym channels.
#
# The audit of 2026-09-15 answered the undefined-symbol row by hand across
# five bundles and found six symbols, and the short-token channel of #14
# found NONE of them: every one is a word or an acronym, and three are not in
# backticks. The `concept-course` fixture reproduces the SHAPE of each real
# finding rather than reading the sibling bundles repository, which moves.
#
#   * `Base offsets`  - durable-event-broker/lessons/07-segments.md:32,
#                       declared, used at :41, defined nowhere.
#   * `thickness bias` - webgl-typescript-scene/lessons/
#                       17-depth-reconstruction-and-ssr.md:37, declared as a
#                       compound and written in prose at :45 as the bare
#                       word `thickness`.
#   * `WAL`           - rust-automaton-db/lessons/10-storage-durability.md,
#                       used at :18, mentioned in a Theory paragraph at :28,
#                       and expanded nowhere.
#
# Every firing case below has its negative control beside it, and the
# controls matter more than the firings: the issue that created this row
# warned that a false report costs the author trust.
# --------------------------------------------------------------------------


def case_concept_declared_used_and_undefined_is_reported() -> None:
    """FIRING (#18): a declared concept the course uses and never defines.

    The `Base offsets` shape. This is the finding the short-token channel
    cannot reach, because the candidate is two ordinary words.
    """
    ev = symbol_evidence(FIXTURES / "concept-course")
    unbound = bucket(ev, "none", "concept-phrase")
    symbols = sorted(c["symbol"] for c in unbound)
    check("base offsets" in symbols, f"`base offsets` is reported as bound nowhere (got {symbols})")
    row = next((c for c in unbound if c["symbol"] == "base offsets"), None)
    if row is None:
        return
    check(
        row["first_use"]["rel"] == "lessons/00-segments.md" and row["first_use"]["line"] > 0,
        f"with the file:line of a USE, not of the bullet (got "
        f"{row['first_use']['rel']}:{row['first_use']['line']})",
    )
    check(row["mention"] == "phrase", f"matched as the whole phrase (got {row['mention']!r})")
    check(row["defined_in_window"] is None, "no defining sentence near the first use")
    check(row["defined_in_other_lessons"] == [], "and none in any other lesson")
    check(
        row["mentioned_in_theory"] is None,
        f"and the '## Theory' section never mentions it (got {row['mentioned_in_theory']})",
    )

    # Controls: the fixture really writes both halves, and the singular /
    # plural difference between them is real - the bullet says "Base
    # offsets" and the constraint says "base offset".
    lesson = (FIXTURES / "concept-course" / "lessons" / "00-segments.md").read_text(encoding="utf-8")
    check("- Base offsets" in lesson, "control: the fixture really declares the concept `Base offsets`")
    check(
        "deterministically by base offset." in lesson,
        "control: and really uses the SINGULAR `base offset` outside the Concepts section",
    )


def case_concepts_bullet_is_the_source_and_never_the_binding() -> None:
    """#18: naming a concept is not introducing it.

    The issue is explicit: "A symbol named in `## Concepts to teach` is not
    thereby introduced. The row passes on a defining sentence." For a
    concept-phrase candidate the bullet is what PRODUCED the candidate, so it
    can never also be what binds it - otherwise every row in this channel
    would report itself as clean.
    """
    ev = symbol_evidence(FIXTURES / "concept-course")
    row = next(
        (c for c in ev["candidates"] if c["channel"] == "concept-phrase" and c["symbol"] == "base offsets"),
        None,
    )
    check(row is not None, "the `base offsets` row is there at all")
    if row is None:
        return
    check(
        row["named_in_concepts"] != [],
        f"the bullet that declared it IS reported, so a reader can read it "
        f"(got {row['named_in_concepts']})",
    )
    check(
        row["binding"] == "none",
        f"and the row is STILL 'bound nowhere' - the bullet is the source, "
        f"not the binding (got {row['binding']!r})",
    )
    check(
        not any(c["binding"] == "concepts" for c in ev["candidates"] if c["channel"] == "concept-phrase"),
        "no concept-phrase row anywhere is bound by 'concepts'",
    )


def case_theory_mention_is_a_bucket_of_its_own() -> None:
    """#18: 'the Theory section mentions it' is neither defined nor nowhere.

    FIRING and NEGATIVE CONTROL in one fixture. `Page cache` is declared,
    used, and only MENTIONED in '## Theory'; `Group commit` is declared and
    carries a real defining sentence in the same section. A scanner that put
    them in one bucket would be useless in both directions.
    """
    ev = symbol_evidence(FIXTURES / "concept-course")
    page = next((c for c in ev["candidates"] if c["symbol"] == "page cache"), None)
    commit = next((c for c in ev["candidates"] if c["symbol"] == "group commit"), None)
    check(page is not None and commit is not None, "both concepts are candidates")
    if page is None or commit is None:
        return
    check(
        page["binding"] == "theory-mention",
        f"a bare Theory mention is its own bucket (got {page['binding']!r})",
    )
    check(
        page["mentioned_in_theory"] is not None and page["defined_in_window"] is None,
        f"the mention is reported and no definition is claimed (got {page['mentioned_in_theory']})",
    )
    check(
        commit["binding"] == "lesson-prose-in-window",
        f"a real defining sentence outranks it (got {commit['binding']!r})",
    )
    if commit["defined_in_window"]:
        check(
            "is one flush" in commit["defined_in_window"]["sentence"],
            f"quoted, so a reader can overrule it (got {commit['defined_in_window']['sentence']!r})",
        )

    lesson = (FIXTURES / "concept-course" / "lessons" / "00-segments.md").read_text(encoding="utf-8")
    check("The page cache sits between" in lesson, "control: the Theory section really only MENTIONS the page cache")
    check("A group commit is one flush" in lesson, "control: and really DEFINES the group commit")


def case_declared_and_never_mentioned_is_not_a_candidate() -> None:
    """NEGATIVE CONTROL (#18): reading every bullet as a candidate floods.

    Measured against the real corpus, every `## Concepts to teach` term is
    111, 176 and 172 candidates for durable-event-broker, rust-automaton-db
    and webgl-typescript-scene. The candidate rule therefore requires the
    term to be MENTIONED outside the Concepts section - the moment a learner
    meets the word. `edge fade` is declared and never written again, and must
    produce nothing.

    The one-word blind spot is asserted here too, and it is deliberate: the
    sort between `metrics` (a name in the chosen language) and vocabulary of
    the subject is the categorical one the author ruled a script must not
    attempt.
    """
    ev = symbol_evidence(FIXTURES / "concept-course")
    symbols = {c["symbol"] for c in ev["candidates"]}
    check("edge fade" not in symbols, f"a declared-and-never-mentioned concept is not reported (got {sorted(symbols)})")
    check("metrics" not in symbols, "a ONE-WORD concept is not reported - the stated blind spot")

    lesson = (FIXTURES / "concept-course" / "lessons" / "00-segments.md").read_text(encoding="utf-8")
    reflections = (FIXTURES / "concept-course" / "lessons" / "01-reflections.md").read_text(encoding="utf-8")
    check("- metrics" in lesson, "control: `metrics` really is declared as a concept")
    check("reports its metrics once a second" in lesson, "control: and really IS mentioned outside the section")
    check("edge fade" in reflections, "control: `edge fade` really is declared")
    check(
        reflections.count("edge fade") == 1,
        f"control: and really is written exactly once, in the bullet "
        f"(got {reflections.count('edge fade')})",
    )


def case_two_word_concept_falls_back_to_the_word_the_prose_uses() -> None:
    """FIRING (#18): `thickness bias` declared, `thickness` written.

    webgl-typescript-scene declares the compound and then writes, at
    17-depth-reconstruction-and-ssr.md:45, "Expose step count, thickness and
    maximum distance as controlled parameters." The compound never appears
    again. The human reader reported `thickness`, and so must this.
    """
    ev = symbol_evidence(FIXTURES / "concept-course")
    row = next((c for c in ev["candidates"] if c["symbol"] == "thickness"), None)
    check(row is not None, "`thickness` is a candidate")
    if row is None:
        return
    check(row["mention"] == "partial", f"reported as a PARTIAL mention (got {row['mention']!r})")
    check(
        row["declared_as"] == "thickness bias",
        f"with the compound the course actually declared (got {row['declared_as']!r})",
    )
    check(
        row["first_use"]["rel"] == "lessons/01-reflections.md",
        f"and the file:line of the prose that uses the bare word "
        f"(got {row['first_use']['rel']}:{row['first_use']['line']})",
    )

    lesson = (FIXTURES / "concept-course" / "lessons" / "01-reflections.md").read_text(encoding="utf-8")
    line = lesson.splitlines()[row["first_use"]["line"] - 1]
    check("thickness" in line, f"control: line {row['first_use']['line']} really says it (it says {line!r})")
    check("thickness bias" not in line, "control: and says the BARE word, not the compound")


def case_a_bare_word_binding_in_design_md_is_not_a_constant() -> None:
    """NEGATIVE CONTROL (#18): `thickness` is bound by DESIGN.md only because
    DESIGN.md really mentions it. Take the line away and it falls through.

    The #14 index only reads BACKTICKED spans, so without a bare-word
    DESIGN.md lookup this channel would report every concept as bound
    nowhere, and 'bound only in DESIGN.md' would stop meaning anything.
    """
    with Workspace() as ws:
        bundle = ws.copy("concept-course", "no-design-thickness")
        path = bundle / "DESIGN.md"
        text = path.read_text(encoding="utf-8")
        check("policy for thickness, step size" in text, "fixture sanity: the DESIGN.md mention is there to remove")

        before = symbol_evidence(bundle)
        row = next((c for c in before["candidates"] if c["symbol"] == "thickness"), None)
        check(row is not None and row["binding"] == "design-md-only",
              f"control: DESIGN.md binds it to start with (got {row and row['binding']})")

        path.write_text(text.replace("policy for thickness, step size", "policy for step size"), encoding="utf-8")
        after = symbol_evidence(bundle)
        row = next((c for c in after["candidates"] if c["symbol"] == "thickness"), None)
        check(row is not None, "it is still a candidate")
        if row is None:
            return
        check(
            row["binding"] == "none",
            f"and falls through to 'bound nowhere' once DESIGN.md stops mentioning it "
            f"(got {row['binding']!r})",
        )


def case_acronym_without_an_expansion_is_reported() -> None:
    """FIRING (#18): `WAL` used, mentioned in Theory, expanded nowhere.

    The `rust-automaton-db` shape, and the reason a Theory mention does NOT
    bind an acronym: lesson 10 writes "A WAL converts in-memory mutation into
    an ordered durable record stream." in its Theory section and never says
    what the three letters stand for.
    """
    ev = symbol_evidence(FIXTURES / "concept-course")
    row = next((c for c in ev["candidates"] if c["symbol"] == "WAL"), None)
    check(row is not None, "`WAL` is a candidate at all")
    if row is None:
        return
    check(row["channel"] == "acronym", f"from the acronym channel (got {row['channel']!r})")
    check(row["binding"] == "none", f"and bound nowhere (got {row['binding']!r})")
    check(
        row["mentioned_in_theory"] is not None,
        f"even though the Theory section mentions it - a mention is reported, "
        f"never treated as an introduction (got {row['mentioned_in_theory']})",
    )
    check(row["first_use"]["line"] > 0, "with a 1-indexed line for the first use")


def case_acronym_expansion_binds_it() -> None:
    """NEGATIVE CONTROL (#18): an acronym the course expands comes back bound.

    "a record is encoded as JavaScript Object Notation (JSON)" is the form
    that introduces an acronym, and it matches none of the shared cues -
    the thing being defined is the expansion and the acronym is the
    parenthetical. Without this control, `WAL` landing in 'none' is equally
    consistent with a channel that binds nothing at all.
    """
    ev = symbol_evidence(FIXTURES / "concept-course")
    row = next((c for c in ev["candidates"] if c["symbol"] == "JSON"), None)
    check(row is not None, "`JSON` is a candidate at all - it is not dropped")
    if row is None:
        return
    check(row["binding"] != "none", f"and it is NOT reported as bound nowhere (got {row['binding']!r})")
    cues = [
        d["cue"]
        for d in ([row["defined_in_window"]] if row["defined_in_window"] else [])
        + row["defined_elsewhere_in_lesson"]
        + row["defined_in_other_lessons"]
    ]
    check("expansion" in cues, f"the cue that bound it is named 'expansion' (got {cues})")

    lesson = (FIXTURES / "concept-course" / "lessons" / "00-segments.md").read_text(encoding="utf-8")
    check("Notation (JSON)" in lesson, "control: the fixture really writes the expansion form")


def case_acronym_negatives_stay_silent() -> None:
    """NEGATIVE CONTROL (#18): a filename and a six-letter word are not acronyms.

    `STATE.md` is a filename - that is a fact about the DOT after the run,
    not about its letters - and `SHOULD` is six letters, one past the bound.
    Neither may be reported, and both really are in the fixture.
    """
    ev = symbol_evidence(FIXTURES / "concept-course")
    seen = set(ev["scan"]["acronyms_seen"])
    check("STATE" not in seen, f"`STATE.md` produces no acronym candidate (got {sorted(seen)})")
    check("SHOULD" not in seen, f"`SHOULD` is past the 5-letter bound (got {sorted(seen)})")
    check(seen == {"JSON", "WAL"}, f"only the two real acronyms are collected (got {sorted(seen)})")

    lesson = (FIXTURES / "concept-course" / "lessons" / "00-segments.md").read_text(encoding="utf-8")
    check("`STATE.md`" in lesson, "control: `STATE.md` really is in the fixture and still produced nothing")
    check("A reader SHOULD be" in lesson, "control: so is SHOULD")


def case_a_noun_is_not_a_defining_verb_for_a_bare_word() -> None:
    """FIRING + CONTROL (#18): the `let-be` cue mis-read a NOUN as its verb.

    Measured defect, from the corpus:
    rust-automaton-db/lessons/10-storage-durability.md:22 says "make one
    logical row write atomic in the WAL". The noun "write", read as the verb,
    bound `WAL` in a lesson that introduces it nowhere - it hid exactly the
    finding this change exists to surface. For a span that need not be
    backticked the cue now requires the verb to open a sentence or a clause,
    and "write" is not one of its verbs.
    """
    with Workspace() as ws:
        bundle = ws.copy("concept-course", "let-be-control")
        path = bundle / "lessons" / "00-segments.md"
        text = path.read_text(encoding="utf-8")
        needle = "- Make one logical row write atomic in the WAL."
        check(needle in text, "fixture sanity: the corpus sentence is there")

        ev = symbol_evidence(bundle)
        row = next(c for c in ev["candidates"] if c["symbol"] == "WAL")
        check(
            row["binding"] == "none",
            f"the noun 'write' does not bind `WAL` (got {row['binding']!r})",
        )

        # The positive control: the same cue, with a real defining clause.
        path.write_text(
            text.replace(needle, "- Let the WAL be the ordered durable record stream."),
            encoding="utf-8",
        )
        ev = symbol_evidence(bundle)
        row = next(c for c in ev["candidates"] if c["symbol"] == "WAL")
        check(
            row["binding"] != "none",
            f"while a real 'Let the WAL be ...' clause DOES bind it - the cue "
            f"still fires (got {row['binding']!r})",
        )


def case_channels_are_named_on_every_row_and_in_the_markdown() -> None:
    """#18: a reader must be able to tell which rule produced a row.

    Three channels feed one list. Without the label a reader cannot tell a
    short-token candidate, whose rule is tight, from a partial-mention
    concept candidate, whose rule is deliberately loose.
    """
    ev = symbol_evidence(FIXTURES / "concept-course")
    channels = {c["channel"] for c in ev["candidates"]}
    check(channels <= {"short-token", "concept-phrase", "acronym"}, f"every row names a known channel (got {channels})")
    check({"concept-phrase", "acronym"} <= channels, f"and this fixture exercises both new ones (got {channels})")
    by_channel = ev["scan"]["candidate_rows_by_channel"]
    check(
        sum(by_channel.values()) == ev["scan"]["candidate_rows"],
        f"the per-channel counts add up to the row count (got {by_channel} vs {ev['scan']['candidate_rows']})",
    )
    check(
        ev["scan"]["concept_terms_declared"] > ev["scan"]["concept_terms_probed"],
        f"and the report says how many declared concepts the rule DROPPED "
        f"(got {ev['scan']['concept_terms_declared']} declared, "
        f"{ev['scan']['concept_terms_probed']} probed)",
    )

    done = run(AUDIT, FIXTURES / "concept-course")
    check(done.returncode == 0, f"markdown mode exits 0 (got {done.returncode}; {done.output!r})")
    check_in("[concept-phrase] `base offsets`", done.stdout, "the Markdown report labels a concept-phrase row")
    check_in("[acronym] `WAL`", done.stdout, "and an acronym row")
    check_in("declared as the concept `thickness bias`", done.stdout, "and says which compound a partial mention came from")
    check_in("Rows by channel:", done.stdout, "and states the per-channel counts a reader is spending attention on")


def main() -> int:
    print(f"audit.py  ({AUDIT})")
    print()
    with case("FIRING: the scanner fires on a real copy-the-starter constraint"):
        case_positive_control_fires()
    with case("NEGATIVE CONTROL: it does not fire on 'a direct-copy composition shader'"):
        case_negative_control_silent()
    with case("FIRING (round 2, DEFECT 1): a verb after a semicolon-space"):
        case_semicolon_lead_fires()
    with case("NEGATIVE CONTROL (round 2, DEFECT 2): a hard-wrapped noun is not an imperative"):
        case_wrapped_noun_stays_silent()
    with case("NARROWED: 'move'/'unzip' need a path token; both real negatives stay silent"):
        case_move_and_extract_require_a_path_token()
    with case("'copy' is deliberately NOT narrowed: it still fires with no path token"):
        case_copy_is_not_narrowed()
    with case("the coverage list comes back verbatim, under its own heading"):
        case_coverage_list_verbatim()
    with case("NEGATIVE CONTROL: a course with no coverage list reports null, not empty"):
        case_no_coverage_reports_null()
    with case("a coverage heading with no topics is a third case, distinct from null"):
        case_coverage_heading_with_no_topics()
    with case("FIRING (#10): a coverage list inside a ```text fence is read - 45 topics"):
        case_fenced_coverage_list_is_read()
    with case("NEGATIVE CONTROL (#10): delete the fence and the 45 topics go away"):
        case_fenced_topics_are_not_a_constant()
    with case("NO REGRESSION (#10): list items still win; an unread fence is announced"):
        case_list_items_win_and_an_unread_fence_is_announced()
    with case("#10: 'could not read it', 'left it empty' and 'there is none' are three results"):
        case_unreadable_is_not_absent_and_not_empty()
    with case("#10: the Markdown report never calls an unread section an empty one"):
        case_markdown_never_claims_an_unread_section_is_empty()
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
    with case("FIRING (round 2, DEFECT 3): stemming + Concepts to teach match 'checksums'"):
        case_topic_candidates_stem_and_read_concepts()
    with case("--json is well-formed and the default Markdown mode states its own caveat"):
        case_json_and_markdown_agree_on_shape()
    with case("FIRING (#14): a symbol nothing introduces is reported with a file:line"):
        case_symbol_nothing_introduces_is_reported()
    with case("FIRING (#14): 'bound only in DESIGN.md' is its own bucket, not 'bound nowhere'"):
        case_design_md_only_is_a_distinct_bucket()
    with case("NEGATIVE CONTROL (#14): remove the DESIGN.md line and `K` falls through to nowhere"):
        case_design_md_binding_is_not_a_constant()
    with case("NEGATIVE CONTROL (#14): a symbol a lesson really introduces comes back clean"):
        case_introduced_symbol_is_not_reported_as_unbound()
    with case("#14: `N + 1` is not lost - the length bound is on the TOKEN, not the span"):
        case_multi_character_span_is_not_lost()
    with case("#14: `2N` is not lost - a two-char span built from a one-char symbol"):
        case_derived_symbol_2n_is_not_lost()
    with case("NEGATIVE CONTROL (#14): `bool`, `New` and a backticked path produce nothing"):
        case_length_and_path_negatives_stay_silent()
    with case("#14: 'nothing to check' and 'checked and clean' are different results"):
        case_nothing_to_check_is_not_checked_and_clean()
    with case("#14: a bundle with no '## Concepts to teach' anywhere is told it lost a channel"):
        case_blind_concepts_channel_is_announced()
    with case("#14: the Markdown report carries the section, its rule, its window and its caveat"):
        case_symbol_section_renders_in_markdown()
    with case("FIRING (#18): a declared concept the course uses and defines nowhere"):
        case_concept_declared_used_and_undefined_is_reported()
    with case("#18: a '## Concepts to teach' bullet is the SOURCE of a row, never its binding"):
        case_concepts_bullet_is_the_source_and_never_the_binding()
    with case("#18: 'mentioned in Theory' is a bucket of its own; a real definition outranks it"):
        case_theory_mention_is_a_bucket_of_its_own()
    with case("NEGATIVE CONTROL (#18): a concept never mentioned again, and a one-word concept"):
        case_declared_and_never_mentioned_is_not_a_candidate()
    with case("FIRING (#18): `thickness bias` declared, bare `thickness` written in prose"):
        case_two_word_concept_falls_back_to_the_word_the_prose_uses()
    with case("NEGATIVE CONTROL (#18): remove the DESIGN.md line and `thickness` falls through"):
        case_a_bare_word_binding_in_design_md_is_not_a_constant()
    with case("FIRING (#18): `WAL` is used, mentioned in Theory, and expanded nowhere"):
        case_acronym_without_an_expansion_is_reported()
    with case("NEGATIVE CONTROL (#18): an expanded acronym comes back bound"):
        case_acronym_expansion_binds_it()
    with case("NEGATIVE CONTROL (#18): `STATE.md` and `SHOULD` are not acronyms"):
        case_acronym_negatives_stay_silent()
    with case("#18 DEFECT: the noun 'write' must not bind `WAL`; a real 'Let ... be' still does"):
        case_a_noun_is_not_a_defining_verb_for_a_bare_word()
    with case("#18: every row names its channel, and the report states the per-channel counts"):
        case_channels_are_named_on_every_row_and_in_the_markdown()
    return report("audit.py")


if __name__ == "__main__":
    sys.exit(main())
