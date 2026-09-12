#!/usr/bin/env python3
"""Emit the evidence a course-quality review starts from.

Usage:
    audit.py <bundle> [--json]

This is the `course-quality` skill's own script, not the authoring toolkit's.
It reads a bundle and reports facts a script can honestly produce: the lesson
skeleton, the coverage list `COURSE.md` declares, the `DESIGN.md` anchors,
declared `supplies:` entries, and candidate sites of authored toil. Default
output is a Markdown skeleton for a human (or the skill that wraps this
script) to fill in with judgement; `--json` is the same data as a JSON
object.

THE DISCIPLINE THAT MATTERS MOST HERE: this script never rules on anything.

  * `candidates` is a list of possible toil sites, found by a regex over
    imperative-looking sentences. It is a CANDIDATE GENERATOR, nothing more.
    An empty list is NOT evidence that a course has no toil - it is evidence
    only that this particular pattern found nothing, and the skill that
    consumes this output must read the lessons itself before concluding
    anything. A scanner nobody has watched fire is not a scanner, and a
    scanner nobody has watched stay silent on a near-miss is worse - see
    the negative control in tests/test_audit.py and in the corpus itself
    (webgl-typescript-scene/lessons/15-render-to-texture.md:41, "Provide a
    direct-copy composition shader before adding effects.", which contains
    the word "copy" and must never appear here).
  * `topic_candidates` is the same kind of guess, from word overlap between
    a coverage-list topic and a lesson's title, slug, design_refs and
    learning objectives. It never claims a topic is covered - an empty
    hit list for a topic says only that no lesson's frontmatter shares a
    meaningful word with it, which is itself worth a human's attention, not
    a verdict that the topic is untaught.

This script computes no score. Scoring is judgement (the rubric in
`references/rubric.md`, applied by the skill this script serves); this
script's job stops at honest evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# audit.py lives in a DIFFERENT skill directory from bundlelib.py, which
# belongs to tutorail-authoring. Reach across to it explicitly rather than
# duplicating lesson discovery, YAML parsing or frontmatter splitting here -
# this script consumes bl.load_bundle, bl.Lesson and bl._ANCHOR_RE (by way
# of bl.Bundle.design_anchors(), which wraps the same regex) exactly as the
# authoring toolkit's own scripts do.
_SCRIPTS_DIR = Path(__file__).resolve().parent
_AUTHORING_SCRIPTS = _SCRIPTS_DIR.parents[1] / "tutorail-authoring" / "scripts"

try:
    import bundlelib as bl
except ImportError:  # pragma: no cover - only when sys.path lacks this dir
    sys.path.insert(0, str(_AUTHORING_SCRIPTS))
    import bundlelib as bl


CANDIDATE_DISCLAIMER = (
    "This scanner is a CANDIDATE GENERATOR, not a verdict. An empty candidate "
    "list is not evidence that this course has no toil - read the lessons "
    "before concluding that."
)

TOPIC_DISCLAIMER = (
    "Topic-to-lesson matches are candidates from shared words, not proof of "
    "coverage. This script never claims a topic is taught."
)


# --------------------------------------------------------------------------
# The toil scanner
#
# A candidate generator (see the module docstring). It requires the verb at
# an imperative "lead" position - the start of a line, of a markdown bullet,
# of a sentence, of an introductory clause set off by a comma or semicolon,
# or right after "must"/"should"/"then" - so that a noun phrase like
# "a direct-copy composition shader" does not fire just because it contains
# the word "copy", and so that "Do not copy X" (an instruction NOT to do
# something) does not fire either, since "copy" there follows "not ", not a
# lead.
#
# The comma alternative is load-bearing. Real toil in the corpus reads
# "Before starting, copy every file under `model/` ..." - an introductory
# clause, so the verb is neither at the start of the line nor after a full
# stop. Without it the scanner misses
# webgl-typescript-scene/lessons/13-load-gltf-model/LESSON.md:40, which is
# one of the two sites this script is required to find.
#
# The semicolon alternative (fix round 2) is load-bearing the same way.
# The regenerated webgl catalogue still carries the five-file copy
# instruction that started this whole change, now at
# lessons/01-canvas-and-context/LESSON.md:42: "... the tutor MUST read
# `starter/README.md`; copy `starter/package.json`, ...". Without
# `(?<=;\s)` the scanner produced ZERO candidates for the exact sentence
# whose presence in lesson 00 is why this tool exists - a scanner that
# misses it in a bundle where it is still present is not doing its job.
# --------------------------------------------------------------------------

TOIL_VERBS = {
    "copy": r"copy|copies",
    "download": r"download",
    "install": r"install",
    "unzip": r"unzip|extract",
    "paste": r"paste",
    "move": r"move",
    "rename": r"rename",
    "clone": r"clone",
    "create-directory": r"(?:create|make)\s+(?:the\s+|a\s+)?(?:directory|folder)",
}

_LEAD = (
    r"(?:^|^[-*]\s+|(?<=[.!?]\s)|(?<=,\s)|(?<=;\s)|"
    r"(?<=\bmust\s)|(?<=\bshould\s)|(?<=\bthen\s))"
)

_TOIL_PATTERNS = {
    name: re.compile(_LEAD + r"\b(?:" + verb + r")\b", re.IGNORECASE)
    for name, verb in TOIL_VERBS.items()
}

# `move` and `unzip`/`extract` are narrowed to require a nearby file-or-path
# token on the SAME LINE. Measured against both real bundles
# (webgl-typescript-scene and durable-event-broker), every `move` and every
# `unzip`/`extract` candidate found was a false positive - both words are
# used constantly in ordinary technical prose with no file anywhere in
# sight ("Move from clip-space drawing to a genuine 3D coordinate
# pipeline.", "Extract one supported mesh primitive into the existing
# `MeshData` representation."). A pattern with zero observed true positives
# does not buy recall, it buys noise, and noise accumulates linearly with
# course size while real toil stays rare.
#
# `copy` is deliberately NOT narrowed. It produced both of this scanner's
# required true positives, and its own false positives are the accepted
# cost of the one pattern that actually works - narrowing it too risks the
# real toil this tool exists to find for a small gain in tidiness.
_REQUIRES_FILE_TOKEN = {"move", "unzip"}

# A "recognisable file extension" - deliberately not exhaustive, but wide
# enough to cover source, markup, data, image, shader and archive files, the
# categories this project's own bundles actually reference.
_PATH_EXTENSIONS = (
    r"md|txt|json|ya?ml|toml|lock|ini|cfg"
    r"|py|rs|go|c|cc|cpp|h|hpp|java|rb|sh"
    r"|js|jsx|ts|tsx|mjs|cjs"
    r"|html?|css|scss"
    r"|glb|gltf|obj|fbx|png|jpe?g|gif|svg|ico|bmp|webp"
    r"|glsl|frag|vert|wgsl|hlsl"
    r"|zip|tar|gz|tgz|rar|7z"
)

# A backticked span containing '.' or '/' - a backticked path, such as
# `starter/package.json` or `model/` - and a recognisable extension anywhere
# on the line, backticked or not. A BARE forward slash on its own is
# deliberately NOT treated as a path signal: the real corpus has at least
# one line where a bare '/' is ordinary English shorthand rather than a
# path ("Introduce emissive/bright scene values, ... extract bright
# regions, ...", durable-event-broker is unaffected but webgl-typescript-
# scene's own 16-bloom.md:43 has this exact shape), and treating every
# slash as a path token would let that line keep firing - exactly the noise
# this narrowing exists to remove.
_FILE_TOKEN_RE = re.compile(
    r"`[^`\n]*[/.][^`\n]*`" r"|\.(?:" + _PATH_EXTENSIONS + r")\b",
    re.IGNORECASE,
)


def _has_file_token(line: str) -> bool:
    return _FILE_TOKEN_RE.search(line) is not None


# --------------------------------------------------------------------------
# The unit of scanning: a PARAGRAPH, not a physical line (fix round 2).
#
# Prose in this corpus is hard-wrapped, so a physical line routinely begins
# mid-sentence. `_LEAD` starting with `^` cannot tell "a fresh sentence
# happens to start at column 0" from "a hard-wrap happens to land here",
# and durable-event-broker/lessons/14-asynchronous-follower.md:30 is a real
# false positive from exactly that confusion: the sentence is "... Therefore
# the\ncopy is neither a quorum ...", so the NOUN "copy" (its article "the"
# sits on the PREVIOUS physical line) lands at a physical line's start and
# reads, to a per-line scan, exactly like an imperative "Copy ...".
#
# The fix is to decide the MATCH against the joined paragraph, while still
# reporting the single physical line a reader would open their editor to -
# `_paragraph_blocks` groups physical line indices into the units scan_toil
# treats as one piece of prose, `_join_block` reassembles a block's lines
# into one string (word-unwrapped) plus a map back to physical lines, and
# `_line_for_offset` uses that map to attribute a match position to its
# real line.
#
# A blank line always ends a block. A heading or a markdown bullet always
# STARTS a fresh block of its own, even with no blank line before it - each
# bullet is a complete, self-contained unit, and joining two consecutive
# bullets into one string would let the FIRST bullet's marker satisfy
# `_LEAD` for a word in a LATER bullet that never had one.
# --------------------------------------------------------------------------


def _paragraph_blocks(lines: list[str]) -> list[list[int]]:
    """Group physical line indices (0-based) into scan_toil's match units."""
    blocks: list[list[int]] = []
    current: list[int] = []
    for i, line in enumerate(lines):
        if not line.strip():
            if current:
                blocks.append(current)
                current = []
            continue
        if _HEADING_RE.match(line) or _BULLET_RE.match(line):
            if current:
                blocks.append(current)
            current = [i]
            continue
        current.append(i)
    if current:
        blocks.append(current)
    return blocks


def _join_block(lines: list[str], indices: list[int]) -> tuple[str, list[tuple[int, int, int]]]:
    """Word-unwrap the given physical lines into one string.

    Returns (joined_text, spans), where spans is a list of
    (start_offset, end_offset, line_index) covering joined_text in order,
    so a regex match position in joined_text can be mapped back to the
    physical line it came from.
    """
    parts: list[str] = []
    spans: list[tuple[int, int, int]] = []
    pos = 0
    for idx in indices:
        segment = lines[idx].strip()
        start = pos
        end = start + len(segment)
        spans.append((start, end, idx))
        parts.append(segment)
        pos = end + 1  # +1 for the single joining space
    return " ".join(parts), spans


def _line_for_offset(spans: list[tuple[int, int, int]], offset: int) -> int:
    """The physical line index whose span contains `offset` in the joined text."""
    line = spans[0][2]
    for start, _end, idx in spans:
        if start > offset:
            break
        line = idx
    return line


def scan_toil(rel: str, text: str) -> list[dict]:
    """Candidate toil sites in `text`.

    The MATCH is decided against each paragraph, joined back into one
    word-unwrapped string (see the block comment above `_paragraph_blocks`).
    Each hit still reports a single physical LINE - `line` and `text` - since
    that is what a reader opens their editor to; only the lead-position
    decision uses the joined text.

    `move` and `unzip`/`extract` additionally require a file-or-path token -
    see `_REQUIRES_FILE_TOKEN` above for why they are narrowed at all. The
    token check is scoped to the SAME PHYSICAL LINE as the match, not the
    whole paragraph: a paragraph can easily mention an unrelated backticked
    identifier or path elsewhere in the same block, several sentences away
    from a `move`/`extract` that has nothing to do with it, and widening the
    check to the whole paragraph would let that launder an unrelated match
    into a hit - the same shape of mistake `_FILE_TOKEN_RE` already avoids
    for a bare `/`.
    """
    lines = text.splitlines()
    candidates: list[dict] = []
    for indices in _paragraph_blocks(lines):
        joined, spans = _join_block(lines, indices)
        for name, pattern in _TOIL_PATTERNS.items():
            for m in pattern.finditer(joined):
                line_idx = _line_for_offset(spans, m.start())
                if name in _REQUIRES_FILE_TOKEN and not _has_file_token(lines[line_idx]):
                    continue
                candidates.append(
                    {
                        "rel": rel,
                        "line": line_idx + 1,
                        "text": lines[line_idx].strip(),
                        "pattern": name,
                    }
                )
    candidates.sort(key=lambda c: (c["line"], c["pattern"]))
    return candidates


# --------------------------------------------------------------------------
# Markdown section parsing - shared by the coverage list and by
# ## Learning objectives.
# --------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", re.MULTILINE)
_BULLET_RE = re.compile(r"^[ \t]*[-*][ \t]+(.+?)[ \t]*$")


def _sections(text: str) -> list[tuple[str, str]]:
    """Split `text` into (heading text, body text) pairs, in document order."""
    headings = list(_HEADING_RE.finditer(text))
    out = []
    for i, m in enumerate(headings):
        start = m.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        out.append((m.group(2).strip(), text[start:end]))
    return out


def _bullets(body: str) -> list[str]:
    return [m.group(1).strip() for m in map(_BULLET_RE.match, body.splitlines()) if m]


def coverage_list(course_text: str | None) -> dict | None:
    """The bundle's coverage list, or None when it declares none at all.

    bundle-format.md section 3: `COURSE.md` SHOULD carry a section naming
    the topics the course must eventually cover, one per line, under a
    heading that says what it is ("Topics this course must cover", "Rust
    coverage requirements", ...). A course MAY have none - that is a finding
    in itself, so this returns None rather than [], and callers must not
    confuse the two: an empty list would be indistinguishable from a parser
    that cannot tell "absent" from "empty".

    The heading is matched on the substring "cover" (case-insensitive),
    which both real examples in bundle-format.md contain and which the
    other headings a COURSE.md carries ("Course map", "Checkpoints",
    "Explicit boundaries", "Prerequisites", ...) do not.

    A heading matching "cover" with a bullet list under it wins outright. If
    several such headings exist, the first one that actually lists topics is
    used; the search keeps going past a heading with nothing under it, in
    case a later heading is the real one. Only if NO matching heading ever
    has topics does this fall back to reporting the first empty one it saw -
    `{"heading": ..., "topics": []}` - which is a THIRD, DISTINCT case from
    "no matching heading at all" (returns None). A course that writes the
    heading and lists nothing under it has done something different from a
    course that never declared a coverage list, and this function must not
    collapse the two into the same result.
    """
    if course_text is None:
        return None
    empty_heading: str | None = None
    for heading, body in _sections(course_text):
        if "cover" not in heading.lower():
            continue
        topics = _bullets(body)
        if topics:
            return {"heading": heading, "topics": topics}
        if empty_heading is None:
            empty_heading = heading
    if empty_heading is not None:
        return {"heading": empty_heading, "topics": []}
    return None


def learning_objectives(lesson_text: str) -> list[str]:
    """The bullets under a lesson's `## Learning objectives` section."""
    _, body = bl.split_frontmatter(lesson_text)
    for heading, section_body in _sections(body):
        if heading.strip().lower() == "learning objectives":
            return _bullets(section_body)
    return []


def _section_text(lesson_text: str, heading_name: str) -> str:
    """The raw body text under a heading matched by exact (lowercased) name.

    Unlike `learning_objectives`, this does not assume the section is a
    bullet list - `## Concepts to teach` is prose in some lessons ("Compilation,
    linking, program status.") and a bullet list in others, and both forms
    need to reach the word-overlap tokenizer, which does not care about
    punctuation either way.
    """
    _, body = bl.split_frontmatter(lesson_text)
    for heading, section_body in _sections(body):
        if heading.strip().lower() == heading_name.lower():
            return section_body
    return ""


# --------------------------------------------------------------------------
# Frontmatter
# --------------------------------------------------------------------------


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


def _frontmatter_supplies(text: str) -> list[dict]:
    fm, _ = bl.split_frontmatter(text)
    if fm is None:
        return []
    try:
        parsed = bl.load_yaml(fm, "frontmatter")
    except bl.YamlError:
        return []
    raw = parsed.get("supplies") if isinstance(parsed, dict) else None
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def gather_supplies(bundle: bl.Bundle) -> list[dict]:
    """Every declared supplies entry, manifest- and lesson-scoped, with its scope."""
    entries: list[dict] = []
    manifest_raw = bundle.manifest.get("supplies")
    if isinstance(manifest_raw, list):
        for item in manifest_raw:
            if isinstance(item, dict):
                entries.append(
                    {
                        "scope": "manifest",
                        "lesson": None,
                        "from": item.get("from"),
                        "to": item.get("to"),
                        "describe": item.get("describe"),
                    }
                )
    for lesson in bundle.ordered:
        text = bl.read_text(lesson.path)
        if text is None:
            continue
        for item in _frontmatter_supplies(text):
            entries.append(
                {
                    "scope": "lesson",
                    "lesson": lesson.slug,
                    "from": item.get("from"),
                    "to": item.get("to"),
                    "describe": item.get("describe"),
                }
            )
    return entries


# --------------------------------------------------------------------------
# Topic candidates - the same "candidate, never a verdict" treatment as the
# toil scanner, applied to matching a coverage-list topic against a lesson.
# --------------------------------------------------------------------------

_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if",
    "in", "into", "is", "it", "its", "of", "on", "or", "over", "own",
    "the", "their", "this", "through", "to", "with", "without",
}


def _tokenize(text: str) -> set[str]:
    return {
        word
        for word in re.findall(r"[a-z0-9]+", text.lower())
        if len(word) >= 3 and word not in _STOPWORDS
    }


def _stem(word: str) -> str:
    """A crude suffix-strip - not a real stemmer, and deliberately not one.

    Exists so a coverage-list topic named in the plural ("checksums") still
    matches a lesson that only ever says the word in the singular
    ("checksum"), and the reverse, without adding a dependency. Round 1
    missed `checksums` in `durable-event-broker` against `02-record-framing`
    for exactly this reason - the topic and the lesson never happened to
    use the identical inflected form.
    """
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith("es"):
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def _stemmed(tokens: set[str]) -> set[str]:
    return {_stem(word) for word in tokens}


def _lesson_tokens(lesson: bl.Lesson, fm: dict) -> set[str]:
    parts = [str(fm.get("title", "")), lesson.slug]
    parts.extend(as_names(fm.get("design_refs")))
    text = bl.read_text(lesson.path)
    if text is not None:
        parts.extend(learning_objectives(text))
        # Round 1 read only title/slug/design_refs/objectives, and missed
        # `## Concepts to teach`, which is often where the coverage-list
        # topic's own vocabulary actually lives (durable-event-broker's
        # `02-record-framing` names "Checksums and their limits" here, not
        # in its objectives).
        parts.append(_section_text(text, "Concepts to teach"))
    return _tokenize(" ".join(parts))


def topic_candidates_for(
    topics: list[str], lesson_tokens: list[tuple[bl.Lesson, set[str]]]
) -> dict:
    """Possible topic-to-lesson matches, from word overlap alone.

    Never claims a topic is covered (see TOPIC_DISCLAIMER). An empty hit
    list for a topic is itself worth a human's attention - it says no
    lesson's title, slug, design_refs, learning objectives or concepts
    share a meaningful (stemmed) word with it - but it is not proof the
    topic goes untaught; a lesson may teach it under different words
    entirely.

    Matching is done on STEMMED tokens (see `_stem`), so a coverage-list
    topic and a lesson's own vocabulary need only share a word up to a
    crude plural/singular difference, not an identical spelling.
    """
    out: dict[str, list[dict]] = {}
    stemmed_lessons = [(lesson, _stemmed(tokens)) for lesson, tokens in lesson_tokens]
    for topic in topics:
        topic_tokens = _stemmed(_tokenize(topic))
        hits = []
        for lesson, tokens in stemmed_lessons:
            overlap = topic_tokens & tokens
            if overlap:
                hits.append({"rel": lesson.rel, "shared": sorted(overlap)})
        hits.sort(key=lambda h: (-len(h["shared"]), h["rel"]))
        out[topic] = hits
    return out


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------


def build(bundle: bl.Bundle) -> dict:
    manifest = bundle.manifest
    ordered = bundle.ordered
    optional = bundle.optional

    course_text = bl.read_text(bundle.root / "COURSE.md")
    cov = coverage_list(course_text)

    lesson_rows = []
    lesson_tokens: list[tuple[bl.Lesson, set[str]]] = []
    candidates: list[dict] = []
    for lesson in ordered:
        fm = frontmatter_of(lesson)
        text = bl.read_text(lesson.path)
        objectives = learning_objectives(text) if text is not None else []
        lesson_rows.append(
            {
                "rel": lesson.rel,
                "id": fm.get("id", lesson.slug),
                "title": fm.get("title"),
                "optional": lesson.rel in optional,
                "form": lesson.form,
                "design_refs": as_names(fm.get("design_refs")),
                "validators": as_names(fm.get("validators")),
                "learning_objectives": objectives,
            }
        )
        lesson_tokens.append((lesson, _lesson_tokens(lesson, fm)))
        if text is not None:
            candidates.extend(scan_toil(lesson.rel, text))

    optional_on_disk = {lesson.rel for lesson in bundle.lessons if lesson.rel in optional}
    course = {
        "id": manifest.get("id"),
        "title": manifest.get("title"),
        "lesson_count": len(bundle.lessons) - len(optional_on_disk),
        "optional_lesson_count": len(optional_on_disk),
    }

    topic_candidates = topic_candidates_for(cov["topics"], lesson_tokens) if cov else {}

    return {
        "course": course,
        "coverage_list": cov,
        "anchors": sorted(bundle.design_anchors()),
        "lessons": lesson_rows,
        "supplies": gather_supplies(bundle),
        "candidates": candidates,
        "topic_candidates": topic_candidates,
        "notes": {
            "toil_scanner": CANDIDATE_DISCLAIMER,
            "topic_matching": TOPIC_DISCLAIMER,
        },
    }


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def render_markdown(data: dict) -> str:
    out: list[str] = []
    course = data["course"]
    out.append(f"# Course quality evidence: {course.get('id')}")
    out.append("")
    out.append(str(course.get("title") or ""))
    out.append(
        f"{course['lesson_count']} lesson(s), {course['optional_lesson_count']} optional"
    )
    out.append("")

    out.append("## Coverage list")
    out.append("")
    cov = data["coverage_list"]
    if cov is None:
        out.append(
            "COURSE.md declares no coverage list at all - no heading naming one. "
            "This is a finding, not an empty result: the course has no declared "
            "boundary for a tutor to check a blocked learner's topic against."
        )
    elif not cov["topics"]:
        out.append(
            f'COURSE.md has a coverage-list heading, "{cov["heading"]}", but it '
            f"names no topics. This is a DIFFERENT finding from declaring none "
            f"at all: the author started this section and never filled it in."
        )
    else:
        out.append(f'Under "{cov["heading"]}":')
        out.extend(f"- {topic}" for topic in cov["topics"])
        out.append("")
        out.append(TOPIC_DISCLAIMER)
        for topic, hits in data["topic_candidates"].items():
            if hits:
                names = ", ".join(h["rel"] for h in hits[:3])
                out.append(f"  - {topic}: word-overlap candidate(s), unconfirmed -> {names}")
            else:
                out.append(
                    f"  - {topic}: this word-overlap search found NO candidate - "
                    f"that is NOT a verdict that the topic is untaught, only that "
                    f"no lesson's words overlapped with it; read the lessons "
                    f"before concluding anything"
                )
    out.append("")

    out.append("## Lessons")
    out.append("")
    for row in data["lessons"]:
        flag = " [optional]" if row["optional"] else ""
        out.append(f"- {row['rel']}{flag}: {row['title'] or '(no title)'}")
    out.append("")

    out.append("## Toil candidates")
    out.append("")
    out.append(CANDIDATE_DISCLAIMER)
    out.append("")
    if not data["candidates"]:
        out.append(
            "(none found - this is NOT evidence the course has no toil; read "
            "the lessons.)"
        )
    else:
        for c in data["candidates"]:
            out.append(f"- {c['rel']}:{c['line']} [{c['pattern']}] {c['text']}")
    out.append("")

    out.append("## Supplies declared")
    out.append("")
    if not data["supplies"]:
        out.append("(none declared)")
    else:
        for entry in data["supplies"]:
            scope = "manifest" if entry["scope"] == "manifest" else f"lesson {entry['lesson']}"
            out.append(f"- [{scope}] {entry.get('from')} -> {entry.get('to')}: {entry.get('describe')}")
    out.append("")

    out.append(f"DESIGN.md anchors ({len(data['anchors'])}): {', '.join(data['anchors']) or '(none)'}")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="audit.py",
        description="Emit the evidence a course-quality review starts from.",
    )
    parser.add_argument("bundle", help="the bundle directory")
    parser.add_argument(
        "--json", action="store_true", help="print the same data as a JSON object"
    )
    args = parser.parse_args(argv)

    bundle = bl.load_bundle(Path(args.bundle))
    data = build(bundle)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(render_markdown(data))
    return 0


if __name__ == "__main__":
    sys.exit(bl.run_main(main))
