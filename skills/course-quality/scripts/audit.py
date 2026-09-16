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
  * `symbol_evidence` TABULATES candidates from THREE rules - a short
    backticked token (`short-token`), a multi-word `## Concepts to teach`
    term the course also uses (`concept-phrase`), and a 2-to-5 letter
    all-capitals run (`acronym`) - and fills in the same evidence columns for
    each: does any lesson's `## Concepts to teach` name it, is there a
    defining sentence near the first use, is there one elsewhere in the same
    lesson or in another lesson, does its own `## Theory` section merely
    mention it, and does only `DESIGN.md` bind it. Every row names the
    channel that produced it. It does NOT decide whether a candidate is a
    parameter of the subject (`N`, `W`, `base offset`) or an identifier of
    the chosen language (`go`, `fn`, `traits`) - that distinction is
    categorical and a reader makes it, so there is no keyword denylist and no
    uppercase-only rule here. Its `status` separates "nothing to check" from
    "checked and clean", and its `warnings` name any evidence channel that
    was blind.
  * `coverage_list` reads the topics `COURSE.md` declares, from Markdown
    list items OR from a fenced block (one topic per non-empty line) - the
    corpus uses both, and reading only the first form made this script state
    that rust-automaton-db's author "never filled it in" over a fence
    holding 45 topics (tutorail-authoring#10). It carries the SAME `status`
    and `warnings` pair as `symbol_evidence`, for the same reason: an empty
    `topics` must never be mistaken for a course that declared none. THREE
    results are distinct - `null` (no heading at all), a `nothing-to-check`
    dict with `scan.body_lines == 0` (heading, nothing under it), and a
    `nothing-to-check` dict with `scan.body_lines > 0` (a coverage list this
    parser COULD NOT READ, which is a fact about this script and not about
    the course).

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

# One definition, used by BOTH readers of fenced blocks in this file: the
# coverage-list parser below, which reads what is INSIDE a fence, and
# `strip_fenced_blocks`, which blanks the same thing for the symbol scanner.
_FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")


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


def _fenced_blocks(body: str) -> tuple[list[list[str]], bool]:
    """(the content of every fenced code block in `body`, was one left open).

    Each block comes back as its list of non-empty, whitespace-stripped
    lines - nothing else is interpreted, because a course that writes its
    coverage list in a fence writes one topic per line and no markers.

    The open-fence flag is not decoration. `_sections` ends a section at the
    next ATX heading, and a `#`-commented line INSIDE a fence looks exactly
    like one, so a fence can be cut in half by the section splitter. When
    that happens the lines gathered so far are still returned - losing them
    would reproduce the very failure this parser exists to fix - and the
    caller warns that the block was not closed.
    """
    blocks: list[list[str]] = []
    fence: str | None = None
    current: list[str] = []
    for line in body.splitlines():
        marker = _FENCE_RE.match(line)
        if fence is None:
            if marker:
                fence = marker.group(1)[0]
                current = []
            continue
        if marker and marker.group(1)[0] == fence:
            blocks.append(current)
            fence = None
            current = []
            continue
        if line.strip():
            current.append(line.strip())
    if fence is not None:
        blocks.append(current)
        return blocks, True
    return blocks, False


def _coverage_section(heading: str, body: str) -> dict:
    """One "cover" heading, read as a coverage list, with its own status.

    The status vocabulary is `symbol_evidence`\'s, deliberately - `checked`,
    `checked-with-blind-channels`, `nothing-to-check`, plus a `warnings`
    list naming any channel that was blind. There is no second vocabulary in
    this file for the same idea.

      * `checked` - topics were read and no other topic-bearing channel
        under this heading went unread.
      * `checked-with-blind-channels` - topics were read, but something else
        under the same heading that could ALSO hold topics was not read.
        `warnings` say what, so a short list can never pass for a whole one.
      * `nothing-to-check` - no topic could be read. `warnings` then say
        WHICH of the two very different reasons applies, and
        `scan["body_lines"]` is the machine-readable form of the same split:

          - `body_lines == 0`: the section is empty. The author started it
            and never filled it in. That is a finding about the COURSE.
          - `body_lines > 0`: there IS content under the heading and this
            parser could not read a topic out of it. That is a finding about
            THIS PARSER, and a reader must not report it as "no topics
            declared" - which is exactly the false statement
            tutorail-authoring#10 caught this script making about
            rust-automaton-db, where 45 topics sat in a ```text fence.

    Both of those are different again from "no matching heading at all",
    which `coverage_list` reports as None and never as a dict.
    """
    bullets = _bullets(body)
    blocks, unclosed = _fenced_blocks(body)
    filled = [block for block in blocks if block]
    body_lines = len([line for line in body.splitlines() if line.strip()])
    warnings: list[str] = []

    if bullets:
        topics = bullets
        source: str | None = "list-items"
        if filled:
            warnings.append(
                f"The {len(bullets)} topic(s) were read from Markdown list items, and "
                f"{len(filled)} fenced code block(s) under the same heading, holding "
                f"{sum(len(b) for b in filled)} non-empty line(s), were NOT read. That "
                f"channel is BLIND here: if the real list is in the fence, this one is "
                f"short. Read the section by hand."
            )
    elif filled:
        topics = list(filled[0])
        source = "fenced-block"
        if len(filled) > 1:
            warnings.append(
                f"{len(filled)} fenced code blocks sit under this heading and only the "
                f"FIRST was read as the coverage list. The other "
                f"{sum(len(b) for b in filled[1:])} non-empty line(s) are unread."
            )
        if unclosed:
            warnings.append(
                "A fenced code block under this heading was never closed inside the "
                "section. A `#`-commented line in a fence reads as a Markdown heading "
                "and cuts the section short, so this list may be truncated. Read the "
                "section by hand."
            )
    else:
        topics = []
        source = None

    if topics:
        status = "checked-with-blind-channels" if warnings else "checked"
    elif body_lines:
        status = "nothing-to-check"
        warnings.append(
            f"The heading is present and {body_lines} non-empty line(s) sit under it, "
            f"but NO topic could be read from them - no Markdown list item, and no "
            f"fenced code block with content. NOTHING WAS READ; this is not a clean "
            f"result and it is NOT evidence that the author declared no topics. The "
            f"list may well be there in a form this parser does not know. Read "
            f"COURSE.md by hand before reporting anything about this course\'s "
            f"coverage."
        )
    else:
        status = "nothing-to-check"
        warnings.append(
            "The heading is present and NOTHING at all sits under it. The author "
            "started this section and never filled it in. This one is a finding about "
            "the course, not a blind spot in this parser."
        )

    return {
        "heading": heading,
        "topics": topics,
        "status": status,
        "warnings": warnings,
        "scan": {
            "topic_source": source,
            "list_items": len(bullets),
            "fenced_blocks": len(blocks),
            "fenced_lines": sum(len(b) for b in blocks),
            "body_lines": body_lines,
        },
    }


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

    TWO forms of list are read under that heading, because the corpus uses
    both: Markdown list items (durable-event-broker, portable-bytebeat-wav,
    portable-fixed-window-rate-limiter, webgl-typescript-scene) and a FENCED
    BLOCK, one topic per non-empty line (rust-automaton-db, `COURSE.md:225`,
    45 topics inside a ```text fence). Reading only the first form is
    tutorail-authoring#10: the script reported an empty list and the
    Markdown report said the author "never filled it in", which was false,
    and which would have suppressed five real coverage gaps had the auditor
    believed it.

    List items WIN when both are present, so the four bundles that use them
    are unaffected; the unread fence is then reported as a blind channel in
    `warnings`, never dropped in silence. See `_coverage_section` for the
    status vocabulary, which is `symbol_evidence`\'s.

    A heading matching "cover" with topics under it wins outright. If
    several such headings exist, the first one that actually lists topics is
    used; the search keeps going past a heading with nothing under it, in
    case a later heading is the real one. Only if NO matching heading ever
    has topics does this fall back to reporting the first topic-less one it
    saw, which is a THIRD, DISTINCT case from "no matching heading at all"
    (returns None). A course that writes the heading and lists nothing under
    it has done something different from a course that never declared a
    coverage list, and this function must not collapse the two.
    """
    if course_text is None:
        return None
    fallback: dict | None = None
    for heading, body in _sections(course_text):
        if "cover" not in heading.lower():
            continue
        section = _coverage_section(heading, body)
        if section["topics"]:
            return section
        if fallback is None:
            fallback = section
    return fallback


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
# Symbols a lesson uses and nothing introduces (tutorail-authoring#14).
#
# THE SAME DISCIPLINE AS EVERY OTHER SCANNER HERE, AND MORE STRICTLY: this
# TABULATES candidates, it does not classify them. The author ruled that the
# distinction between a conceptual parameter of the thing being taught (`N`,
# `W`) and an identifier of the chosen language (`bool`, `go`, `fn`) is
# CATEGORICAL and that no script can make it today - a reader makes it. So
# there is deliberately:
#
#   * no keyword denylist. `go`, `fn`, `id`, `ok` and `db` are emitted like
#     any other candidate, with the evidence a reader needs to dismiss them.
#   * no uppercase-only rule. The issue's own open question floats "report a
#     single uppercase letter only"; that rule silently drops `n`, `w`, `qs`
#     and anything a course writes in lower case, and this scanner's job is
#     to make sure a reader cannot MISS a candidate.
#   * no pruning of a candidate because some evidence channel bound it. EVERY
#     candidate is emitted with all four evidence columns filled in and a
#     `binding` field that is a PURE FUNCTION of those columns. A reader who
#     disagrees with a "definition" this scanner found can see the sentence
#     it matched, quoted, and overrule it.
#
# THE CANDIDATE RULE, and why it is this one.
#
# A candidate is an IDENTIFIER TOKEN OF ONE OR TWO CHARACTERS that appears
# inside an EXPRESSION-SHAPED backticked span.
#
#   * "one or two characters" is the issue's own bound. Two is the first
#     bound that keeps `qs`, `dt`, `id` and `go` while dropping `New`, `bool`
#     and `null` by length alone rather than by a denylist - which is exactly
#     the line the author drew. It is a property of the TOKEN, never of the
#     whole span.
#   * "expression-shaped" is what keeps `N + 1` from being lost. The issue
#     names `N + 1` as a symbol that must survive, and a rule that measured
#     the whole backticked span would throw it away at five characters. So
#     the span is TOKENIZED, and a span qualifies when it holds nothing but
#     identifiers, integer literals, whitespace and arithmetic/comparison
#     operators. `N + 1` yields the candidate `N`; `starter/package.json`
#     and `db.Exec()` are excluded outright by the `.` they contain, before
#     length is even considered.
#
# A pure digit run (`1`, `256`) is a literal, not an identifier, and is never
# a candidate.
# --------------------------------------------------------------------------

SYMBOL_DISCLAIMER = (
    "Short-symbol candidates are a TABULATION, not a verdict. This scanner "
    "cannot tell a conceptual parameter of the subject (`N`, `W`) from an "
    "identifier of the chosen language (`go`, `fn`, `id`) - that distinction "
    "is categorical and a reader makes it. Every candidate is listed with "
    "its evidence, including the ones some channel appears to bind, so a "
    "reader can overrule this scanner in both directions."
)

SYMBOL_RULE = (
    "candidate = an identifier token of 1-2 characters inside a backticked "
    "span made only of identifiers, integer literals, whitespace and "
    "arithmetic/comparison operators, with a binary '-' requiring whitespace "
    "so a slug is not mistaken for a subtraction. `N + 1` yields `N`; "
    "`starter/package.json` is excluded by its '.'; `automaton-db` by its "
    "wedged hyphen; `bool` and `New` are excluded by token length, not by a "
    "denylist."
)

# --------------------------------------------------------------------------
# tutorail-authoring#18 - two more candidate channels, for the same row.
#
# The audit of 2026-09-15 answered the undefined-symbol row by hand across
# five bundles and found six symbols. The short-token channel above found
# NONE of them, and the reason is structural rather than a bug: every one of
# the six is a WORD or an ACRONYM, and three of them are not in backticks at
# all. A 1-2 character token rule cannot reach any of them.
#
# The fix the issue forbids is widening the token rule. A rule reporting
# every 3-to-5 character backticked token reports `bool`, `New`, `go`, `Vec`,
# `impl` and every type name in every Rust lesson, and the author has ruled
# that the sort between a parameter of the subject and an identifier of the
# chosen language is CATEGORICAL - no rule of shape performs it. So instead
# of one wider rule there are two more NARROW ones, each with its own source:
#
#   * `concept-phrase` - the course's own `## Concepts to teach` list is the
#     candidate source. A course states its vocabulary there, so nothing is
#     guessed. The direction is inverted from the short-token channel: that
#     one finds uses and asks whether they are defined; this one takes a
#     declared concept and asks whether any lesson ever defines it.
#   * `acronym` - an all-capitals run of 2 to 5 letters. `CAS`, `WAL` and
#     `FST` share exactly one shape. `AST`, `GC` and `NFA` share it too and
#     the human reader PASSED them, which is the expected outcome: these are
#     candidates, and a reader sorts them.
#
# Neither channel classifies, neither computes a score, and both fill in the
# same evidence columns as the short-token channel.
#
# WHY A CONCEPT PHRASE MUST ALSO BE MENTIONED SOMEWHERE ELSE. Reading every
# Concepts bullet as a candidate produces 111, 176 and 172 rows against
# durable-event-broker, rust-automaton-db and webgl-typescript-scene, and a
# report nobody reads is worth less than a smaller one somebody does. The
# candidate rule therefore requires the declared term to appear OUTSIDE every
# `## Concepts to teach` section - that is the moment a learner meets the
# word and needs it to have been introduced. Measured on the same three
# bundles the rule yields 13, 52 and 62 terms.
#
# THE TWO-WORD PARTIAL MENTION. `webgl-typescript-scene` declares the concept
# `thickness bias` and then writes, in prose, "Expose step count, thickness
# and maximum distance as controlled parameters."
# (17-depth-reconstruction-and-ssr.md:45). The compound never appears again;
# the bare word does, and the bare word is what the human reader reported. So
# a TWO-word term whose full phrase is never mentioned falls back to its
# constituent words, under three restrictions that keep the fallback from
# becoming a word-soup scanner: the word is at least 5 characters, it appears
# in no OTHER declared concept of the same bundle (a word shared by several
# concepts - "error", "context", "index" - is a generic modifier, not a
# term), and it is mentioned in the lesson that DECLARED the concept. Terms
# of three words and more do not fall back at all; that is a stated blind
# spot, not an oversight.
#
# ONE-WORD CONCEPTS ARE A STATED BLIND SPOT. `metrics`, `traits`, `mmap`,
# `arc`, `indices` and `precision` are one-word Concepts bullets, and the
# sort between "vocabulary of the subject" and "name in the chosen language"
# is exactly the categorical sort the author ruled a script cannot make.
# Emitting them would put 26 Rust API names into rust-automaton-db's report.
# They are not reported, and this comment is the record of that choice.
CONCEPT_RULE = (
    "candidate = a term of TWO OR MORE words from a lesson's '## Concepts to "
    "teach' section that is also mentioned OUTSIDE every such section, "
    "somewhere a learner reads it. A two-word term whose full phrase is "
    "never mentioned falls back to a constituent word of 5+ characters that "
    "no other declared concept contains and that the declaring lesson "
    "mentions - that is how `thickness bias` is reported as `thickness`. "
    "One-word concepts are NOT reported: telling `metrics` and `traits` "
    "(names in the chosen language) from vocabulary of the subject is the "
    "categorical sort this script must not attempt. Terms of three words or "
    "more do not fall back to single words."
)

ACRONYM_RULE = (
    "candidate = a run of 2 to 5 capital letters, in backticks or bare, used "
    "in a lesson outside a fenced block. `CAS`, `WAL` and `FST` share this "
    "one shape. `AST`, `GC`, `HTTP` and `JSON` share it too and a reader is "
    "expected to pass them; this is a candidate list, not a verdict. A run "
    "followed by a dot and an alphanumeric (`STATE.md`) is a filename, not "
    "an acronym, and is skipped."
)

CONCEPT_DISCLAIMER = (
    "A term named in '## Concepts to teach' is NOT thereby introduced. The "
    "row passes on a DEFINING SENTENCE, and a Concepts bullet is a "
    "declaration of vocabulary, not a definition of it - two of the six "
    "symbols the 2026-09-15 audit found by hand are named in a Concepts "
    "bullet and defined nowhere. So for a concept-phrase candidate the "
    "Concepts bullet is the SOURCE of the candidate and can never also be "
    "its binding; it is printed on the row so a reader can read the bullet "
    "and judge it. THREE BLIND SPOTS, stated so an empty list is never read "
    "as a clean one: a ONE-WORD concept is not reported, a concept of THREE "
    "WORDS OR MORE does not fall back to a constituent word, and a noun "
    "phrase that NO SECTION DECLARES is invisible to every channel here - "
    "`metadata seam` (durable-event-broker/lessons/09-retention.md:44) is "
    "one, and a reader still has to find that kind by reading."
)

SYMBOL_WINDOW = (
    "near the first use = the PARAGRAPH BLOCK holding the first use, plus "
    "the block immediately before it and the block immediately after it "
    "(the same blocks the toil scanner treats as one piece of prose; a "
    "heading or a bullet always starts a fresh one). Prose in this corpus is "
    "hard-wrapped, so a line-count window would cut sentences in half; a "
    "paragraph is the smallest unit an author actually writes a definition "
    "in. The block AFTER the first use is included deliberately - whether a "
    "definition arrives early enough is a reader's question, not this "
    "script's, so a late definition is reported as found-and-late rather "
    "than suppressed. A definition anywhere else in the same lesson is "
    "reported too, in its own `lesson-prose-elsewhere` bucket."
)

_MAX_SYMBOL_LEN = 2

# The characters an expression-shaped span may contain, beyond identifier
# and digit characters: whitespace and the arithmetic/comparison operators a
# course writes inline. `.`, `/`, `:`, quotes, brackets and braces are all
# ABSENT on purpose - they are what a path, a method call, a type parameter
# or a dict literal is made of, and none of those is the shape this scanner
# is looking for.
_EXPRESSION_SPAN_RE = re.compile(r"^[A-Za-z0-9_\s+\-*%^<>=(),×·]+$")

# A hyphen wedged BETWEEN two word characters is not a minus sign, it is a
# slug: `automaton-db`, `01-write-a-tone`,
# `frame-decoder-breaks-on-arbitrary-input`. Measured against the five real
# bundles, every one of those three spans reached the `none` bucket and every
# one was noise - a lesson id or a validator name, not a symbol anybody has
# to introduce. Requiring whitespace around a binary `-` (a leading unary `-`
# is still fine, as in `-1`) removes all three while keeping `N - 1`.
#
# This is a refinement of the EXPRESSION SHAPE, not a denylist of
# identifiers: no token is judged by what it spells, only by the punctuation
# of the span it sits in.
_SLUG_HYPHEN_RE = re.compile(r"[A-Za-z0-9_]-[A-Za-z0-9_]")

_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")

# An all-capitals run of 2 to 5 letters, in backticks or bare. The lookbehind
# excludes only WORD characters, so a backticked `WAL` is still found; the
# `-` and `/` of "regex/automata/FST" are not word characters either, which
# is the shape FST is actually written in.
_ACRONYM_RE = re.compile(r"(?<![A-Za-z0-9_])([A-Z]{2,5})(?![A-Za-z0-9_])")

# `STATE.md`, `README.md`: a capital run followed by a dot and an
# alphanumeric is a filename. This is a property of the PUNCTUATION that
# follows the run, never of the letters in it - there is no denylist here.
_ACRONYM_FILE_TAIL_RE = re.compile(r"^\.[A-Za-z0-9]")

# A concept term is split on whitespace, '/' and '-' for matching, so
# "latency/availability trade-offs" and "per-partition ordering" match the
# prose that writes them the same way.
_TERM_SPLIT_RE = re.compile(r"[\s/-]+")

# The shortest constituent word a two-word concept may fall back to. Below
# this the fallback starts matching ordinary prose ("cost", "close", "user").
_CONCEPT_MIN_WORD = 5

# A prose-form Concepts section is one sentence of comma-separated terms:
# "Depth linearisation, inverse projection, NDC reconstruction, ... and
# temporal instability." A bulleted one is one term per bullet and is NOT
# split further, because "hash maps and sets" is one concept.
_CONCEPT_SEPARATOR_RE = re.compile(r",|\s+and\s+|\s+or\s+")

def strip_fenced_blocks(text: str) -> tuple[str, int]:
    """Blank the CONTENT of every fenced code block, keeping the line count.

    Returns (text, number of fences opened). Line numbers survive, so every
    `file:line` this section reports still points at the real line.

    Fenced blocks are skipped DELIBERATELY and the count is reported, so that
    "this bundle has no inline symbols" can never be confused with "this
    bundle writes everything inside fences and the scanner never looked" -
    the failure shape tutorail-authoring#10 describes for the coverage-list
    parser. A bundle whose fence count is high and whose candidate count is
    zero is a bundle to read by hand.
    """
    out: list[str] = []
    fence: str | None = None
    opened = 0
    for line in text.splitlines():
        marker = _FENCE_RE.match(line)
        if fence is None:
            if marker:
                fence = marker.group(1)[0]
                opened += 1
                out.append("")
                continue
            out.append(line)
        else:
            out.append("")
            if marker and marker.group(1)[0] == fence:
                fence = None
    return "\n".join(out), opened


def symbols_in_span(span: str) -> list[str]:
    """The 1-2 character identifier tokens an expression-shaped span holds."""
    if not _EXPRESSION_SPAN_RE.match(span) or _SLUG_HYPHEN_RE.search(span):
        return []
    return [tok for tok in _IDENT_RE.findall(span) if len(tok) <= _MAX_SYMBOL_LEN]


def symbol_uses(text: str) -> list[dict]:
    """Every candidate-symbol use in `text`, in document order.

    `text` must already have its fenced blocks blanked. Each use records the
    symbol, the backticked span AS WRITTEN (so `N + 1` is never flattened
    into a bare `N` and lost), the 1-indexed line and that line's text.
    """
    uses: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in _INLINE_CODE_RE.finditer(line):
            span = m.group(1)
            for symbol in symbols_in_span(span):
                uses.append(
                    {
                        "symbol": symbol,
                        "span": span.strip(),
                        "line": lineno,
                        "text": line.strip(),
                    }
                )
    return uses


# --------------------------------------------------------------------------
# What counts as a defining sentence.
#
# Five cues, each reported BY NAME with the sentence it matched, so a reader
# can reject any one of them. The copula cue is the one that most easily
# over-claims - "`N + 1` is rejected." is a sentence about `N`, and it is not
# a definition - so `is`/`are` additionally require a determiner, a numeral
# or a defining participle after them. That kills "is rejected", "is
# allowed", "is enough" while keeping "`N` is the request limit" and "`W` is
# a positive duration".
#
# The appositive cue ("a positive request limit `N`") requires the span to be
# at the END of its noun phrase - followed by punctuation, "and", "or", or
# the end of the sentence. Without that lookahead, "the first `N` requests"
# reads as an apposition when `N` is really a determiner for "requests".
# --------------------------------------------------------------------------

_DETERMINER = r"(?:the|a|an|its|our|one|any|each|every|either|both|two|\d+|written|called|defined|known|shorthand)"
_COPULA = r"(?:is|are|was|were|will\s+be|shall\s+be)"
_NAMES = r"(?:means|denotes|represents|refers\s+to|stands\s+for|names)"


def _symbol_span(symbol: str) -> str:
    """The regex source for "a backticked span containing this symbol"."""
    sym = re.escape(symbol)
    return r"`[^`\n]*(?<![A-Za-z0-9_])" + sym + r"(?![A-Za-z0-9_])[^`\n]*`"


def _plural_tail(word: str) -> str:
    """`word`, matching its own simple plural as well.

    A Concepts bullet writes "Base offsets" and the prose that uses it writes
    "base offset". Neither form is more correct and a scanner that matched
    only the declared one would miss the use it exists to find. Three endings
    cover this corpus: -ies/-y, -es, -s.
    """
    if len(word) > 3 and word.endswith("ies"):
        return re.escape(word[:-3]) + r"(?:y|ies)"
    if len(word) > 3 and word.endswith("es"):
        return re.escape(word[:-2]) + r"(?:es)?"
    if len(word) > 2 and word.endswith("s") and not word.endswith("ss"):
        return re.escape(word[:-1]) + r"s?"
    return re.escape(word) + r"s?"


def _term_core(term: str) -> str | None:
    """The word-sequence regex source for a concept term, or None if empty."""
    words = [w for w in _TERM_SPLIT_RE.split(term) if w]
    if not words:
        return None
    parts = [re.escape(w) for w in words[:-1]] + [_plural_tail(words[-1])]
    return r"[\s/-]+".join(parts)


def _term_use_re(term: str) -> re.Pattern[str] | None:
    """Where a concept term is MENTIONED - backticked or bare, either number."""
    core = _term_core(term)
    if core is None:
        return None
    return re.compile(r"(?<![A-Za-z0-9_])" + core + r"(?![A-Za-z0-9_])", re.IGNORECASE)


def _term_span(term: str) -> str | None:
    """The regex source a definition cue wraps around a concept term.

    Unlike `_symbol_span` this does NOT require backticks: three of the six
    symbols the 2026-09-15 audit found by hand are written as plain words.
    """
    core = _term_core(term)
    if core is None:
        return None
    return r"`?(?<![A-Za-z0-9_])" + core + r"(?![A-Za-z0-9_])`?"


def _acronym_word_re(acronym: str) -> re.Pattern[str]:
    """Where an acronym is MENTIONED - backticked or bare, singular or plural."""
    return re.compile(r"(?<![A-Za-z0-9_])" + re.escape(acronym) + r"s?(?![A-Za-z0-9_])")


def _acronym_span(acronym: str) -> str:
    return r"`?(?<![A-Za-z0-9_])" + re.escape(acronym) + r"s?(?![A-Za-z0-9_])`?"


def _acronym_cues(acronym: str) -> list[tuple[str, re.Pattern[str]]]:
    """The shared cues, plus the one cue only an acronym has.

    "a write-ahead log (WAL)" introduces `WAL` and matches none of the shared
    cues, because the thing being defined is the EXPANSION and the acronym is
    the parenthetical. The reverse form, "`WAL` (write-ahead log)", is
    already the `gloss` cue.
    """
    expansion = re.compile(
        r"(?:[A-Za-z][A-Za-z-]*[\s/-]+){1,5}\(\s*" + re.escape(acronym) + r"s?\s*\)"
    )
    return _definition_cues(_acronym_span(acronym), bare_word=True) + [("expansion", expansion)]


def _definition_cues(span: str, *, bare_word: bool = False) -> list[tuple[str, re.Pattern[str]]]:
    """The defining-sentence cues, wrapped around any span regex source.

    `span` is a regex SOURCE for the thing being defined - a backticked short
    symbol (`_symbol_span`), a concept phrase (`_term_span`) or an acronym
    (`_acronym_span`). The cues themselves are unchanged and each is still
    reported by name with the sentence it matched.

    `bare_word` tightens the `let-be` cue for the two channels whose span is
    NOT required to be backticked. Backticks are punctuation a reader can
    see, and they make a false match unlikely; a bare word sits in ordinary
    prose, where "write" and "call" are nouns as often as verbs. The
    measured failure is
    rust-automaton-db/lessons/10-storage-durability.md:22, "make one logical
    row write atomic in the WAL" - the noun "write", read as the verb, bound
    `WAL` in a lesson that never introduces it, and that is precisely the
    finding tutorail-authoring#18 exists to surface. In bare-word mode the
    verb must open the sentence or a clause, and "write" is not one of the
    verbs.
    """
    return [
        ("copula", re.compile(span + r"\s+" + _COPULA + r"\s+" + _DETERMINER + r"\b", re.IGNORECASE)),
        ("names", re.compile(span + r"\s+" + _NAMES + r"\b", re.IGNORECASE)),
        (
            "appositive",
            re.compile(
                r"\b(?:the|a|an|each|one|our|its|this|that|some|any|positive|configured)\s+"
                r"(?:[A-Za-z][A-Za-z-]*\s+){0,2}"
                # The head noun must be a NOUN, not a preposition. "the role
                # of `w`" and "a section index from `t`" both have the shape
                # of an apposition and neither defines anything - the span is
                # the preposition's OBJECT, not the noun phrase's name. Real
                # corpus lines, both from bundles this scanner is measured
                # against (webgl-typescript-scene/lessons/
                # 05-transforms-and-perspective.md:20 and
                # portable-bytebeat-wav/lessons/03-compose-and-export.md:28).
                r"(?!(?:of|for|in|to|by|with|on|from|between|against|as|at|into|"
                r"over|under|within|without|per|about|than|via)\s)"
                r"[A-Za-z][A-Za-z-]*\s+" + span + r"(?=\s*(?:[,.;:)]|\band\b|\bor\b|$))",
                re.IGNORECASE,
            ),
        ),
        (
            "gloss",
            re.compile(span + r"\s*(?:\([^)]{2,}\)|[:—]\s+\w|\s-\s+\w)", re.IGNORECASE),
        ),
        (
            "let-be",
            re.compile(
                # Not "use". "- Use `Vec<T>`, slices, iterators, and
                # closures." (rust-automaton-db/lessons/00-foundations.md:29)
                # is an instruction, not a definition, and "use" is the one
                # verb in this family that reads as neither.
                (
                    r"(?:^[-*+]?\s*|[.;:]\s+)(?:let|call|denote|define)\b[^.]{0,48}?"
                    if bare_word
                    else r"\b(?:let|call|write|denote|define)\b[^.]{0,48}?"
                )
                + span,
                re.IGNORECASE,
            ),
        ),
        ("where-is", re.compile(r"\bwhere\s+" + span + r"\s+" + _COPULA + r"\b", re.IGNORECASE)),
    ]


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _sentences(joined: str) -> list[tuple[int, str]]:
    """(start offset, sentence) pairs covering `joined`, in order."""
    out: list[tuple[int, str]] = []
    pos = 0
    for piece in _SENTENCE_SPLIT_RE.split(joined):
        idx = joined.find(piece, pos)
        if idx < 0:  # pragma: no cover - split output is always found
            idx = pos
        out.append((idx, piece))
        pos = idx + len(piece)
    return out


def sentence_index(text: str) -> list[tuple[int, int, str, list[tuple[int, int, int]]]]:
    """Every sentence of `text`, with what is needed to place a match on a line.

    `text` must already have its fenced blocks blanked. A sentence is taken
    inside a word-unwrapped PARAGRAPH BLOCK, because this corpus hard-wraps
    its prose and a definition routinely straddles two physical lines.

    Built ONCE per lesson and reused by every candidate. There are three
    candidate channels now and rust-automaton-db declares 176 concepts across
    23 lessons, so re-splitting each lesson per candidate would be four
    thousand re-parses of the same text.
    """
    lines = text.splitlines()
    out: list[tuple[int, int, str, list[tuple[int, int, int]]]] = []
    for block_index, indices in enumerate(_paragraph_blocks(lines)):
        joined, spans = _join_block(lines, indices)
        for offset, sentence in _sentences(joined):
            out.append((block_index, offset, sentence, spans))
    return out


def find_definitions_in(
    index: list[tuple[int, int, str, list[tuple[int, int, int]]]],
    cues: list[tuple[str, re.Pattern[str]]],
) -> list[dict]:
    """Every defining sentence in a prepared `sentence_index`, with line and cue.

    The reported line is the physical one a reader opens their editor to, and
    `block` is the index of the paragraph block the sentence came from, which
    is what the near-the-first-use window is measured in.
    """
    found: list[dict] = []
    for block_index, offset, sentence, spans in index:
        for name, pattern in cues:
            m = pattern.search(sentence)
            if m is None:
                continue
            line_idx = _line_for_offset(spans, offset + m.start())
            found.append(
                {
                    "line": line_idx + 1,
                    "cue": name,
                    "sentence": sentence.strip(),
                    "block": block_index,
                }
            )
            break
    found.sort(key=lambda d: d["line"])
    return found


def find_definitions(symbol: str, text: str) -> list[dict]:
    """Every defining sentence for a short backticked `symbol` in `text`."""
    return find_definitions_in(sentence_index(text), _definition_cues(_symbol_span(symbol)))


def _block_of_line(blocks: list[list[int]], line_index: int) -> int | None:
    for i, indices in enumerate(blocks):
        if line_index in indices:
            return i
    return None


# --------------------------------------------------------------------------
# The `## Concepts to teach` index and the DESIGN.md index.
# --------------------------------------------------------------------------


def _section_bounds(lesson_text: str, heading_name: str) -> tuple[str | None, int]:
    """(a named section's body, the 1-indexed line it starts on IN THE BODY)."""
    _, body = bl.split_frontmatter(lesson_text)
    for heading, section_body in _sections(body):
        if heading.strip().lower() == heading_name.lower():
            offset = body.index(section_body)
            return section_body, body.count("\n", 0, offset) + 1
    return None, 0


def _concepts_section(lesson_text: str) -> tuple[str | None, int, int]:
    """(the `## Concepts to teach` body, its first line IN THE FILE, its first
    line IN THE BODY), or (None, 0, 0) when the lesson declares no section.

    Two line bases, because two callers need different ones. Everything a
    reader is shown is a line in the FILE, frontmatter included. The
    "mentioned outside the Concepts section" probe works on the body with
    fences blanked, which starts after the frontmatter, so it needs the same
    line in BODY coordinates to blank the right rows.
    """
    _, body = bl.split_frontmatter(lesson_text)
    section: str | None = None
    for heading, section_body in _sections(body):
        if heading.strip().lower() == "concepts to teach":
            section = section_body
            break
    if section is None:
        return None, 0, 0
    offset = body.index(section)
    body_line = body.count("\n", 0, offset) + 1
    frontmatter_lines = lesson_text.count("\n", 0, lesson_text.index(body)) if body else 0
    return section, body_line + frontmatter_lines, body_line


def concept_terms(lesson_text: str) -> tuple[bool, list[dict]]:
    """(does the lesson declare the section, the terms it names).

    The boolean is load-bearing for the same reason it is in
    `concepts_symbols`: a lesson with no section and a lesson whose section
    names nothing both return an empty list, and only the first means "this
    candidate source does not exist here".

    Two forms occur in the corpus and both are read:

      * BULLETS - one term per bullet, kept WHOLE. "hash maps and sets" is
        one concept, and splitting it on "and" would invent two that the
        author never wrote.
      * PROSE - one sentence of comma-separated terms, which is how
        `webgl-typescript-scene` writes every one of its Concepts sections.
        That form IS split, on commas and on "and"/"or", because the commas
        are the author's own separators.

    Each term carries the line IN THE FILE that it was written on, so every
    candidate this channel produces points at a line a reader can open.
    """
    section, base, _body_line = _concepts_section(lesson_text)
    if section is None:
        return False, []

    lines = section.splitlines()
    terms: list[dict] = []
    bullets = [(i, _BULLET_RE.match(line)) for i, line in enumerate(lines)]
    bullets = [(i, m) for i, m in bullets if m]
    if bullets:
        for i, m in bullets:
            terms.append(
                {"term": m.group(1), "line": base + i, "text": lines[i].strip(), "form": "bullet"}
            )
    else:
        joined_parts: list[str] = []
        starts: list[tuple[int, int]] = []
        pos = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            starts.append((pos, i))
            joined_parts.append(stripped)
            pos += len(stripped) + 1
        joined = " ".join(joined_parts)
        pieces: list[tuple[str, int]] = []
        last = 0
        for m in _CONCEPT_SEPARATOR_RE.finditer(joined):
            pieces.append((joined[last : m.start()], last))
            last = m.end()
        pieces.append((joined[last:], last))
        for piece, offset in pieces:
            lead = len(piece) - len(piece.lstrip())
            row = starts[0][1] if starts else 0
            for start, i in starts:
                if start <= offset + lead:
                    row = i
            terms.append(
                {
                    "term": piece,
                    "line": base + row,
                    "text": lines[row].strip() if row < len(lines) else piece.strip(),
                    "form": "prose",
                }
            )

    out: list[dict] = []
    for row in terms:
        cleaned = row["term"].strip().rstrip(".").strip()
        if cleaned:
            out.append({**row, "term": cleaned})
    return True, out


def acronym_uses(text: str) -> list[dict]:
    """Every all-capitals 2-to-5-letter run in `text`, in document order.

    `text` must already have its fenced blocks blanked. A run followed by a
    dot and an alphanumeric is a filename (`STATE.md`) and is skipped - that
    is a fact about the punctuation after the run, not about its letters.
    """
    uses: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in _ACRONYM_RE.finditer(line):
            if _ACRONYM_FILE_TAIL_RE.match(line[m.end() :]):
                continue
            uses.append(
                {
                    "symbol": m.group(1),
                    "span": m.group(1),
                    "line": lineno,
                    "text": line.strip(),
                }
            )
    return uses


def concepts_symbols(lesson_text: str) -> tuple[bool, dict[str, dict]]:
    """(does the lesson declare the section, symbols it names).

    The boolean is load-bearing and is NOT derivable from the dict. A lesson
    with no `## Concepts to teach` section and a lesson whose section names
    no symbol both yield an empty dict, and only the first means "this
    evidence channel does not exist here". Collapsing the two is the shape of
    bug tutorail-authoring#10 describes and the shape `coverage_list` already
    guards against by returning None rather than [].

    A concept bullet names a symbol either in backticks ("the symbols `N`
    (request limit) and `W`") or bare ("the window duration W"); both count,
    and the form is reported so a reader can see which it was.
    """
    section, base, _body_line = _concepts_section(lesson_text)
    if section is None:
        return False, {}

    named: dict[str, dict] = {}
    backticked: set[str] = set()
    for lineno, line in enumerate(section.splitlines(), start=base):
        real_line = lineno
        for m in _INLINE_CODE_RE.finditer(line):
            for symbol in symbols_in_span(m.group(1)):
                backticked.add(symbol)
                named.setdefault(
                    symbol,
                    {"line": real_line, "text": line.strip(), "form": "backticked"},
                )
    # A bare mention only counts for a symbol some lesson actually USES; the
    # caller supplies that set, so record every bare word of candidate length
    # here and let `build_symbol_evidence` intersect.
    bare: dict[str, dict] = {}
    for lineno, line in enumerate(section.splitlines(), start=base):
        real_line = lineno
        stripped = _INLINE_CODE_RE.sub(" ", line)
        for word in re.findall(r"(?<![A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_]*)(?![A-Za-z0-9_])", stripped):
            if len(word) <= _MAX_SYMBOL_LEN and word not in backticked:
                bare.setdefault(word, {"line": real_line, "text": line.strip(), "form": "bare"})
    for symbol, hit in bare.items():
        named.setdefault(symbol, hit)
    return True, named


def design_anchor_map(design_text: str) -> tuple[list[str], list[str | None]]:
    """(DESIGN.md's lines with fences blanked, the anchor in force on each)."""
    stripped, _ = strip_fenced_blocks(design_text)
    lines = stripped.splitlines()
    anchor_at: list[str | None] = []
    current: str | None = None
    for line in lines:
        heading = _HEADING_RE.match(line)
        if heading:
            found = bl._ANCHOR_RE.search(heading.group(2))
            current = found.group(1) if found else None
        anchor_at.append(current)
    return lines, anchor_at


def design_mention(
    lines: list[str], anchor_at: list[str | None], pattern: re.Pattern[str] | None
) -> dict | None:
    """The first DESIGN.md line matching `pattern`, with its anchor, or None.

    The companion of `design_symbol_index` for the two channels whose
    candidates are NOT backticked short tokens. `FST` is written
    "regex/automata/FST libraries" at rust-automaton-db/DESIGN.md:173, with
    no backticks anywhere, and the backticked-span index cannot see it.

    A DESIGN.md mention still never introduces anything to a learner - the
    runner loads an anchor for the TUTOR - so this exists only to keep
    "bound solely in DESIGN.md" distinct from "bound nowhere at all".
    """
    if pattern is None:
        return None
    for lineno, line in enumerate(lines, start=1):
        if pattern.search(line):
            anchor = anchor_at[lineno - 1]
            return {
                "line": lineno,
                "text": line.strip(),
                "anchors": [anchor] if anchor else [],
            }
    return None


def design_symbol_index(design_text: str) -> dict[str, dict]:
    """Where DESIGN.md mentions each candidate symbol, and under which anchor.

    A DESIGN.md mention NEVER introduces a symbol to a learner - the runner
    loads an anchor for the TUTOR - so this index exists only to separate
    "bound solely in DESIGN.md" from "bound nowhere at all", which the issue
    requires be reported distinctly.
    """
    lines, anchor_at = design_anchor_map(design_text)

    index: dict[str, dict] = {}
    for lineno, line in enumerate(lines, start=1):
        for m in _INLINE_CODE_RE.finditer(line):
            for symbol in symbols_in_span(m.group(1)):
                entry = index.setdefault(
                    symbol, {"line": lineno, "text": line.strip(), "anchors": []}
                )
                anchor = anchor_at[lineno - 1]
                if anchor and anchor not in entry["anchors"]:
                    entry["anchors"].append(anchor)
    return index


# --------------------------------------------------------------------------
# Assembly of the symbol evidence
# --------------------------------------------------------------------------

# The buckets, strongest evidence first. `binding` is a PURE FUNCTION of the
# evidence columns and ranks them in this order; it is a label for a row of
# facts, not a judgement about the symbol.
#
# `other-lesson-prose` exists so that `design-md-only` means what the issue
# needs it to mean. `portable-bytebeat-wav` uses `t` in four lessons; only
# `DESIGN.md:24` and lesson 00's own objectives bind it. Without a column for
# a definition in a DIFFERENT lesson, lessons 01, 02 and `stereo-bytebeat`
# would all land in `design-md-only` while lesson 00 in fact defines `t` in
# prose - and "only DESIGN.md binds this" would be a false statement. The
# bucket is still a finding worth a reader's eye (a learner who starts at
# lesson 01 has met no definition), which is why it sits below the
# same-lesson buckets rather than beside `concepts`.
#
# `concepts` MOVED DOWN in tutorail-authoring#18, from the top of this list
# to just below every prose bucket. It used to outrank a real defining
# sentence, which meant that for `N` in portable-fixed-window-rate-limiter
# the report showed the weakest evidence and hid the strongest. The issue
# states the principle plainly: a symbol named in `## Concepts to teach` is
# NOT thereby introduced, and the row passes on a defining sentence. The
# bucket is kept rather than deleted, because deleting it would drop `E`,
# `Eq` and `T` - Rust type parameters named in a Concepts bullet and nowhere
# else - into `none` and invent four findings.
#
# `theory-mention` is new and applies ONLY to a `concept-phrase` candidate.
# A concept the course declares it will teach and then discusses in its own
# `## Theory` section has been addressed by the bundle's explaining section,
# which is weaker than a definition and much stronger than silence; against
# the five real bundles it takes 46 rows out of `none`. It does NOT apply to
# a short token or an acronym: `WAL` appears in a Theory paragraph of
# rust-automaton-db/lessons/10-storage-durability.md and is still introduced
# nowhere, and burying it under a "mentioned in Theory" heading would hide
# exactly the finding this change exists to surface.
_CHANNELS = ["short-token", "concept-phrase", "acronym"]

_BINDING_ORDER = [
    "lesson-prose-in-window",
    "lesson-prose-elsewhere",
    "other-lesson-prose",
    "concepts",
    "theory-mention",
    "design-md-only",
    "none",
]


def _lesson_scan(lesson: bl.Lesson, raw: str) -> dict:
    """Everything the three channels need from one lesson, read ONCE."""
    _, body = bl.split_frontmatter(raw)
    prefix = raw.count("\n", 0, raw.index(body)) if body else 0
    stripped, opened = strip_fenced_blocks(body)

    section, _base, body_line = _concepts_section(raw)
    outside_lines = stripped.splitlines()
    if section is not None:
        count = len(section.splitlines())
        for i in range(body_line - 1, min(body_line - 1 + count, len(outside_lines))):
            outside_lines[i] = ""
    outside = "\n".join(outside_lines)

    # `theory` keeps the body's own line numbering and blanks everything
    # OUTSIDE the `## Theory` section, so a hit in it reports the line a
    # reader opens - the same trick `strip_fenced_blocks` uses.
    theory_lines = [""] * len(stripped.splitlines())
    theory_body, theory_line = _section_bounds(raw, "Theory")
    if theory_body is not None:
        for i in range(theory_line - 1, min(theory_line - 1 + len(theory_body.splitlines()), len(theory_lines))):
            theory_lines[i] = stripped.splitlines()[i]
    theory_stripped = "\n".join(theory_lines)

    return {
        "lesson": lesson,
        "rel": lesson.rel,
        "prefix": prefix,
        "stripped": stripped,
        "outside": outside,
        "theory": theory_stripped,
        "blocks": _paragraph_blocks(stripped.splitlines()),
        "index": sentence_index(stripped),
        "fenced": opened,
    }


def _first_match(scans: list[dict], field: str, pattern: re.Pattern[str] | None) -> dict | None:
    """The first line of `field` in bundle order that `pattern` matches."""
    if pattern is None:
        return None
    for scan in scans:
        for lineno, line in enumerate(scan[field].splitlines(), start=1):
            m = pattern.search(line)
            if m is None:
                continue
            return {
                "rel": scan["rel"],
                "line": lineno + scan["prefix"],
                "span": m.group(0).strip(),
                "text": line.strip(),
            }
    return None


def _bind(
    *,
    channel: str,
    concepts_hits: list[dict],
    in_window: dict | None,
    elsewhere: list[dict],
    other_lessons: list[dict],
    in_theory: dict | None,
    design_hit: dict | None,
) -> str:
    """The `binding` label: a PURE FUNCTION of the evidence columns.

    Two channel-dependent rules, both from tutorail-authoring#18 and both
    documented at `_BINDING_ORDER`: a `concept-phrase` candidate cannot be
    bound by the Concepts bullet that PRODUCED it, and only a
    `concept-phrase` candidate can be bound by a `## Theory` mention.
    """
    if in_window is not None:
        return "lesson-prose-in-window"
    if elsewhere:
        return "lesson-prose-elsewhere"
    if other_lessons:
        return "other-lesson-prose"
    if concepts_hits and channel != "concept-phrase":
        return "concepts"
    if in_theory is not None and channel == "concept-phrase":
        return "theory-mention"
    if design_hit is not None:
        return "design-md-only"
    return "none"


def _candidate_row(
    *,
    channel: str,
    symbol: str,
    declared_as: str | None,
    mention: str | None,
    scan: dict,
    use: dict,
    definitions: list[dict],
    definitions_by_lesson: dict[str, list[dict]],
    concepts_hits: list[dict],
    in_theory: dict | None,
    design_hit: dict | None,
) -> dict:
    """One candidate, with every evidence column filled in and never pruned."""
    use_block = _block_of_line(scan["blocks"], use["line"] - scan["prefix"] - 1)
    in_window: dict | None = None
    elsewhere: list[dict] = []
    for d in definitions:
        row = {"rel": scan["rel"], "line": d["line"], "cue": d["cue"], "sentence": d["sentence"]}
        near = use_block is not None and abs(d["block"] - use_block) <= 1
        if near and in_window is None:
            row["offset_lines"] = row["line"] - use["line"]
            in_window = row
        elif not near:
            elsewhere.append(row)

    other_lessons: list[dict] = []
    for rel, found in definitions_by_lesson.items():
        if rel == scan["rel"]:
            continue
        for d in found:
            other_lessons.append(
                {"rel": rel, "line": d["line"], "cue": d["cue"], "sentence": d["sentence"]}
            )

    return {
        "channel": channel,
        "symbol": symbol,
        "declared_as": declared_as,
        "mention": mention,
        "lesson": scan["rel"],
        "first_use": {
            "rel": use.get("rel", scan["rel"]),
            "line": use["line"],
            "span": use["span"],
            "text": use["text"],
        },
        "named_in_concepts": concepts_hits,
        "defined_in_window": in_window,
        "defined_elsewhere_in_lesson": elsewhere,
        "defined_in_other_lessons": other_lessons,
        "mentioned_in_theory": in_theory,
        "design_md": design_hit,
        "binding": _bind(
            channel=channel,
            concepts_hits=concepts_hits,
            in_window=in_window,
            elsewhere=elsewhere,
            other_lessons=other_lessons,
            in_theory=in_theory,
            design_hit=design_hit,
        ),
    }


def build_symbol_evidence(bundle: bl.Bundle) -> dict:
    """Per lesson, per candidate: the evidence, never a verdict.

    THREE candidate channels feed one list, and every row carries the
    `channel` that produced it:

      * `short-token` - a 1-2 character identifier in an expression-shaped
        backticked span (tutorail-authoring#14).
      * `concept-phrase` - a multi-word `## Concepts to teach` term that the
        course also uses outside that section (tutorail-authoring#18).
      * `acronym` - a 2-to-5 letter all-capitals run (tutorail-authoring#18).

    `status` separates NOTHING TO CHECK from CHECKED AND CLEAN. A bundle
    whose lessons declare no `## Concepts to teach` section anywhere, or
    whose `DESIGN.md` could not be read, has lost an evidence channel - and,
    for the Concepts section, an entire CANDIDATE SOURCE as well - and an
    empty `unbound` list from such a bundle means something entirely
    different from an empty list produced with every channel alive. The same
    goes for a bundle in which no candidate was found at all. Both are
    reported as `status` plus a populated `warnings` list, never as silence.
    """
    warnings: list[str] = []

    design_text = bl.read_text(bundle.root / "DESIGN.md")
    design_present = (bundle.root / "DESIGN.md").exists()
    if design_text is None:
        design_index: dict[str, dict] = {}
        design_lines: list[str] = []
        design_anchor_at: list[str | None] = []
        warnings.append(
            "DESIGN.md could not be read"
            + (" (the file is present but unreadable)" if design_present else " (no such file)")
            + " - the 'defined only in DESIGN.md' column is BLIND for this bundle, "
            "so every symbol it would have bound is reported as bound nowhere."
        )
    else:
        design_index = design_symbol_index(design_text)
        design_lines, design_anchor_at = design_anchor_map(design_text)

    lessons_scanned = 0
    unreadable: list[str] = []
    fenced_blocks = 0
    concepts_lessons: list[str] = []
    without_concepts: list[str] = []
    concepts_named: dict[str, list[dict]] = {}
    declared: dict[str, list[dict]] = {}
    scans: list[dict] = []

    for lesson in bundle.ordered:
        raw = bl.read_text(lesson.path)
        if raw is None:
            unreadable.append(lesson.rel)
            continue
        lessons_scanned += 1

        has_section, named = concepts_symbols(raw)
        if has_section:
            concepts_lessons.append(lesson.rel)
            for symbol, hit in named.items():
                concepts_named.setdefault(symbol, []).append({"rel": lesson.rel, **hit})
        else:
            without_concepts.append(lesson.rel)

        _has_terms, terms = concept_terms(raw)
        for row in terms:
            declared.setdefault(row["term"].lower(), []).append({"rel": lesson.rel, **row})

        scan = _lesson_scan(lesson, raw)
        fenced_blocks += scan["fenced"]
        scan["uses"] = symbol_uses(scan["stripped"])
        for use in scan["uses"]:
            use["line"] += scan["prefix"]
        scan["acronyms"] = acronym_uses(scan["stripped"])
        for use in scan["acronyms"]:
            use["line"] += scan["prefix"]
        scans.append(scan)

    if not concepts_lessons and lessons_scanned:
        warnings.append(
            "NO lesson in this bundle declares a '## Concepts to teach' section - "
            "the 'some lesson names it' column is BLIND for this bundle AND the "
            "concept-phrase candidate source does not exist here. Every candidate "
            "below is reported as un-introduced by that channel because the "
            "channel does not exist, not because a reader checked it."
        )

    candidates: list[dict] = []

    # ----------------------------------------------------------------------
    # Channel 1: short backticked tokens (tutorail-authoring#14).
    #
    # Every distinct symbol is looked for in EVERY lesson, so that a
    # definition in a different lesson is a column of its own rather than an
    # absence that would make `design-md-only` lie (see `_BINDING_ORDER`).
    # ----------------------------------------------------------------------
    all_symbols = sorted({use["symbol"] for scan in scans for use in scan["uses"]})
    token_defs: dict[str, dict[str, list[dict]]] = {}
    for symbol in all_symbols:
        cues = _definition_cues(_symbol_span(symbol))
        per_rel: dict[str, list[dict]] = {}
        for scan in scans:
            rows = find_definitions_in(scan["index"], cues)
            if rows:
                per_rel[scan["rel"]] = [dict(r, line=r["line"] + scan["prefix"]) for r in rows]
        token_defs[symbol] = per_rel

    for scan in scans:
        seen: set[str] = set()
        for use in scan["uses"]:
            symbol = use["symbol"]
            if symbol in seen:
                continue
            seen.add(symbol)
            candidates.append(
                _candidate_row(
                    channel="short-token",
                    symbol=symbol,
                    declared_as=None,
                    mention=None,
                    scan=scan,
                    use=use,
                    definitions=token_defs[symbol].get(scan["rel"], []),
                    definitions_by_lesson=token_defs[symbol],
                    concepts_hits=concepts_named.get(symbol, []),
                    in_theory=None,
                    design_hit=(
                        None
                        if design_index.get(symbol) is None
                        else {
                            "line": design_index[symbol]["line"],
                            "text": design_index[symbol]["text"],
                            "anchors": design_index[symbol]["anchors"],
                        }
                    ),
                )
            )

    # ----------------------------------------------------------------------
    # Channel 2: multi-word `## Concepts to teach` terms (#18).
    # ----------------------------------------------------------------------
    word_owners: dict[str, set[str]] = {}
    for key in declared:
        for word in key.split():
            word_owners.setdefault(word, set()).add(key)

    concept_probes: list[tuple[str, str, str, dict]] = []
    for key in sorted(declared):
        words = key.split()
        if len(words) < 2 or "`" in key:
            continue
        hit = _first_match(scans, "outside", _term_use_re(key))
        if hit is not None:
            concept_probes.append((key, key, "phrase", hit))
            continue
        if len(words) != 2:
            continue
        declaring = {row["rel"] for row in declared[key]}
        for word in words:
            if len(word) < _CONCEPT_MIN_WORD or len(word_owners.get(word, ())) != 1:
                continue
            own = [scan for scan in scans if scan["rel"] in declaring]
            hit = _first_match(own, "outside", _term_use_re(word))
            if hit is not None:
                concept_probes.append((key, word, "partial", hit))
                break

    for key, probe, mention, hit in concept_probes:
        span = _term_span(probe)
        cues = _definition_cues(span, bare_word=True) if span else []
        per_rel: dict[str, list[dict]] = {}
        for scan in scans:
            rows = find_definitions_in(scan["index"], cues)
            if rows:
                per_rel[scan["rel"]] = [dict(r, line=r["line"] + scan["prefix"]) for r in rows]
        use_scan = next(scan for scan in scans if scan["rel"] == hit["rel"])
        candidates.append(
            _candidate_row(
                channel="concept-phrase",
                symbol=probe,
                declared_as=declared[key][0]["term"],
                mention=mention,
                scan=use_scan,
                use=hit,
                definitions=per_rel.get(hit["rel"], []),
                definitions_by_lesson=per_rel,
                concepts_hits=[
                    {
                        "rel": row["rel"],
                        "line": row["line"],
                        "text": row["text"],
                        "form": row["form"],
                    }
                    for row in declared[key]
                ],
                in_theory=_first_match(scans, "theory", _term_use_re(probe)),
                design_hit=design_mention(design_lines, design_anchor_at, _term_use_re(probe)),
            )
        )

    # ----------------------------------------------------------------------
    # Channel 3: all-capitals acronyms of 2 to 5 letters (#18).
    # ----------------------------------------------------------------------
    all_acronyms = sorted({use["symbol"] for scan in scans for use in scan["acronyms"]})
    acronym_concepts: dict[str, list[dict]] = {}
    for scan in scans:
        raw = bl.read_text(scan["lesson"].path)
        if raw is None:
            continue
        section, base, _body_line = _concepts_section(raw)
        if section is None:
            continue
        for i, line in enumerate(section.splitlines()):
            for m in _ACRONYM_RE.finditer(line):
                if _ACRONYM_FILE_TAIL_RE.match(line[m.end() :]):
                    continue
                acronym_concepts.setdefault(m.group(1), []).append(
                    {
                        "rel": scan["rel"],
                        "line": base + i,
                        "text": line.strip(),
                        "form": "bare" if "`" not in m.group(0) else "backticked",
                    }
                )

    acronym_defs: dict[str, dict[str, list[dict]]] = {}
    for acronym in all_acronyms:
        cues = _acronym_cues(acronym)
        per_rel = {}
        for scan in scans:
            rows = find_definitions_in(scan["index"], cues)
            if rows:
                per_rel[scan["rel"]] = [dict(r, line=r["line"] + scan["prefix"]) for r in rows]
        acronym_defs[acronym] = per_rel

    for scan in scans:
        seen = set()
        for use in scan["acronyms"]:
            acronym = use["symbol"]
            if acronym in seen:
                continue
            seen.add(acronym)
            candidates.append(
                _candidate_row(
                    channel="acronym",
                    symbol=acronym,
                    declared_as=None,
                    mention=None,
                    scan=scan,
                    use=use,
                    definitions=acronym_defs[acronym].get(scan["rel"], []),
                    definitions_by_lesson=acronym_defs[acronym],
                    concepts_hits=acronym_concepts.get(acronym, []),
                    # Recorded, and deliberately NOT a binding: `WAL` is
                    # written into a Theory paragraph of
                    # rust-automaton-db/lessons/10-storage-durability.md and
                    # is still introduced nowhere. See `_BINDING_ORDER`.
                    in_theory=_first_match(scans, "theory", _acronym_word_re(acronym)),
                    design_hit=design_mention(
                        design_lines, design_anchor_at, _acronym_word_re(acronym)
                    ),
                )
            )

    candidates.sort(
        key=lambda c: (c["lesson"], c["first_use"]["line"], c["channel"], c["symbol"])
    )

    by_channel = {name: 0 for name in _CHANNELS}
    for c in candidates:
        by_channel[c["channel"]] += 1

    if lessons_scanned == 0:
        status = "nothing-to-check"
        warnings.append(
            "NO lesson text could be read at all - nothing was checked. This is "
            "not a clean result."
        )
    elif not candidates:
        status = "nothing-to-check"
        warnings.append(
            f"NO candidate was found by ANY of the three channels in the "
            f"{lessons_scanned} lesson(s) scanned ({fenced_blocks} fenced code "
            f"block(s) were skipped, as the short-token channel only reads INLINE "
            f"backticked spans). 'No candidate found' is NOT 'no undefined "
            f"symbol' - read the lessons."
        )
    elif warnings:
        status = "checked-with-blind-channels"
    else:
        status = "checked"

    summary = {name: 0 for name in _BINDING_ORDER}
    for c in candidates:
        summary[c["binding"]] += 1

    return {
        "status": status,
        "rule": SYMBOL_RULE,
        "rules": {
            "short-token": SYMBOL_RULE,
            "concept-phrase": CONCEPT_RULE,
            "acronym": ACRONYM_RULE,
        },
        "window": SYMBOL_WINDOW,
        "disclaimer": SYMBOL_DISCLAIMER,
        "concepts_disclaimer": CONCEPT_DISCLAIMER,
        "warnings": warnings,
        "scan": {
            "lessons_scanned": lessons_scanned,
            "lessons_unreadable": unreadable,
            "fenced_blocks_skipped": fenced_blocks,
            "lessons_with_concepts_section": concepts_lessons,
            "lessons_without_concepts_section": without_concepts,
            "design_md_present": design_present,
            "design_md_readable": design_text is not None,
            "design_md_symbols": sorted(design_index),
            "concept_terms_declared": len(declared),
            "concept_terms_probed": len(concept_probes),
            "acronyms_seen": all_acronyms,
            "candidate_rows": len(candidates),
            "candidate_rows_by_channel": by_channel,
            "distinct_symbols": sorted({c["symbol"] for c in candidates}),
        },
        "summary_by_binding": summary,
        "candidates": candidates,
    }


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
        "symbol_evidence": build_symbol_evidence(bundle),
        "notes": {
            "toil_scanner": CANDIDATE_DISCLAIMER,
            "topic_matching": TOPIC_DISCLAIMER,
            "symbol_evidence": SYMBOL_DISCLAIMER,
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
    elif not cov["topics"] and cov["scan"]["body_lines"]:
        # tutorail-authoring#10. THIS branch is the one the old code got
        # wrong: it printed "the author never filled it in" over a section
        # that held 45 topics in a fence. Never say what the author did or
        # did not write when nothing was read - say that nothing was read.
        out.append(
            f'COURSE.md has a coverage-list heading, "{cov["heading"]}", with '
            f'{cov["scan"]["body_lines"]} non-empty line(s) under it, and THIS SCRIPT '
            f"COULD NOT READ A TOPIC out of any of them. Do NOT report that the course "
            f"declares no topics, and do NOT report that the author left the section "
            f"empty - neither is known. Read COURSE.md by hand."
        )
    elif not cov["topics"]:
        out.append(
            f'COURSE.md has a coverage-list heading, "{cov["heading"]}", and NOTHING '
            f"at all under it. This is a DIFFERENT finding from declaring none "
            f"at all: the author started this section and never filled it in."
        )
    else:
        out.append(
            f'Under "{cov["heading"]}" ({len(cov["topics"])} topic(s), read from '
            f'{cov["scan"]["topic_source"]}):'
        )
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
    if cov is not None:
        out.append("")
        out.append(f"status: {cov['status']}")
        if cov["warnings"]:
            out.append("")
            out.append("Warnings - an evidence channel here was blind:")
            for text_line in cov["warnings"]:
                out.append(f"  - {text_line}")
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

    out.extend(render_symbol_evidence(data["symbol_evidence"]))

    out.append(f"DESIGN.md anchors ({len(data['anchors'])}): {', '.join(data['anchors']) or '(none)'}")
    return "\n".join(out)


_CHANNEL_LABELS = {
    "short-token": "a 1-2 character token in a backticked expression",
    "concept-phrase": "a multi-word '## Concepts to teach' term the course also uses",
    "acronym": "a 2-5 letter all-capitals run",
}

_BINDING_HEADINGS = {
    "none": "Used, and introduced NOWHERE this scanner can see",
    "theory-mention": "concept-phrase only: the lesson's own '## Theory' section mentions it, but no sentence DEFINES it - read the mention and decide whether it introduces the concept",
    "design-md-only": "Bound ONLY in DESIGN.md - the runner loads an anchor for the TUTOR, not for the learner, so this does NOT introduce the symbol to a learner",
    "lesson-prose-elsewhere": "A defining sentence exists in the same lesson but OUTSIDE the near-the-first-use window - is it early enough? A reader decides",
    "other-lesson-prose": "No same-lesson introduction: the only defining sentence is in a DIFFERENT lesson. A learner who reaches this lesson without that one has met no definition",
    "lesson-prose-in-window": "A defining sentence is near the first use - read the sentence and decide whether it really defines the symbol",
    "concepts": "NAMED in some lesson's '## Concepts to teach' and DEFINED by no sentence anywhere - a Concepts bullet declares vocabulary, it does not introduce it, so this is a row to read and not a clean result",
}


def render_symbol_evidence(ev: dict) -> list[str]:
    out: list[str] = []
    out.append("## Short symbols a lesson uses")
    out.append("")
    out.append(f"status: {ev['status']}")
    out.append("")
    for name in _CHANNELS:
        out.append(f"Candidate rule [{name}]: {ev.get('rules', {}).get(name, ev['rule'])}")
        out.append("")
    out.append(f"Window: {ev['window']}")
    out.append("")
    out.append(ev["disclaimer"])
    out.append("")
    if ev.get("concepts_disclaimer"):
        out.append(ev["concepts_disclaimer"])
        out.append("")

    scan = ev["scan"]
    out.append(
        f"Scanned {scan['lessons_scanned']} lesson(s); "
        f"{len(scan['lessons_with_concepts_section'])} declare '## Concepts to teach'; "
        f"{scan['fenced_blocks_skipped']} fenced code block(s) skipped; "
        f"DESIGN.md present={scan['design_md_present']} readable={scan['design_md_readable']}; "
        f"{scan['candidate_rows']} candidate row(s) over "
        f"{len(scan['distinct_symbols'])} distinct symbol(s)."
    )
    by_channel = scan.get("candidate_rows_by_channel", {})
    if by_channel:
        out.append(
            "Rows by channel: "
            + "; ".join(f"{name} {by_channel.get(name, 0)}" for name in _CHANNELS)
            + f". {scan.get('concept_terms_declared', 0)} concept term(s) declared, "
            f"{scan.get('concept_terms_probed', 0)} of them reached the candidate rule; "
            f"{len(scan.get('acronyms_seen', []))} distinct acronym(s) seen."
        )
    out.append("")

    if ev["warnings"]:
        out.append("NOTHING-TO-CHECK / BLIND-CHANNEL WARNINGS - read these before")
        out.append("reading an empty list below as a clean result:")
        for text in ev["warnings"]:
            out.append(f"  !! {text}")
        out.append("")

    if ev["status"] == "nothing-to-check":
        out.append(
            "This section checked NOTHING. That is a different result from "
            "'checked and clean', and the warnings above say why."
        )
        out.append("")
        return out

    for binding in _BINDING_ORDER:
        rows = [c for c in ev["candidates"] if c["binding"] == binding]
        out.append(f"### {binding} ({len(rows)})")
        out.append("")
        out.append(_BINDING_HEADINGS[binding])
        out.append("")
        if not rows:
            if binding == "none":
                out.append(
                    "(no candidate fell in this bucket - with every channel above "
                    "alive, that is 'checked and clean' for this bucket, not "
                    "'nothing was checked'.)"
                )
            else:
                out.append("(none)")
            out.append("")
            continue
        for c in rows:
            use = c["first_use"]
            channel = c.get("channel", "short-token")
            out.append(
                f"- [{channel}] `{c['symbol']}` first used at {use['rel']}:{use['line']} "
                f"(written `{use['span']}`)"
            )
            if c.get("declared_as") and c["declared_as"].lower() != c["symbol"].lower():
                out.append(
                    f"    declared as the concept `{c['declared_as']}` - only the part "
                    f"`{c['symbol']}` is used in prose (mention: {c.get('mention')})"
                )
            out.append(f"    {use['text']}")
            for hit in c["named_in_concepts"]:
                label = "declared in concepts" if channel == "concept-phrase" else "concepts"
                out.append(
                    f"    {label}: {hit['rel']}:{hit['line']} [{hit['form']}] {hit['text']}"
                )
            if c["defined_in_window"]:
                d = c["defined_in_window"]
                out.append(
                    f"    definition in window: {d['rel']}:{d['line']} "
                    f"({d['offset_lines']:+d} lines) [{d['cue']}] {d['sentence']}"
                )
            for d in c["defined_elsewhere_in_lesson"]:
                out.append(
                    f"    definition elsewhere in lesson: {d['rel']}:{d['line']} "
                    f"[{d['cue']}] {d['sentence']}"
                )
            for d in c["defined_in_other_lessons"]:
                out.append(
                    f"    definition in ANOTHER lesson: {d['rel']}:{d['line']} "
                    f"[{d['cue']}] {d['sentence']}"
                )
            if c.get("mentioned_in_theory"):
                t = c["mentioned_in_theory"]
                out.append(
                    f"    mentioned in '## Theory': {t['rel']}:{t['line']} {t['text']} "
                    f"- a mention is NOT a definition"
                )
            if c["design_md"]:
                anchors = ", ".join(c["design_md"]["anchors"]) or "(no anchor)"
                out.append(
                    f"    DESIGN.md:{c['design_md']['line']} under {anchors} - "
                    f"TUTOR-ONLY, does not introduce the symbol to a learner"
                )
            else:
                out.append("    DESIGN.md: no mention")
        out.append("")
    return out


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
