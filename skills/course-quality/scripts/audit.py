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
  * `symbol_evidence` TABULATES every short backticked symbol a lesson uses
    and fills in four evidence columns for each: does any lesson's `##
    Concepts to teach` name it, is there a defining sentence near the first
    use, is there one elsewhere in the same lesson, and does only `DESIGN.md`
    bind it. It does NOT decide whether a two-character backticked token is a
    parameter of the subject (`N`, `W`) or an identifier of the chosen
    language (`go`, `fn`) - that distinction is categorical and a reader
    makes it, so there is no keyword denylist and no uppercase-only rule
    here. Its `status` separates "nothing to check" from "checked and
    clean", and its `warnings` name any evidence channel that was blind.

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

_FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")


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


def _definition_cues(symbol: str) -> list[tuple[str, re.Pattern[str]]]:
    sym = re.escape(symbol)
    span = r"`[^`\n]*(?<![A-Za-z0-9_])" + sym + r"(?![A-Za-z0-9_])[^`\n]*`"
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
                r"\b(?:let|call|write|denote|define)\b[^.]{0,48}?" + span, re.IGNORECASE
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


def find_definitions(symbol: str, text: str) -> list[dict]:
    """Every defining sentence for `symbol` in `text`, with its line and cue.

    `text` must already have its fenced blocks blanked. The match is decided
    against a SENTENCE inside a word-unwrapped paragraph block, because this
    corpus hard-wraps its prose and a definition routinely straddles two
    physical lines; the reported line is still the physical one a reader
    opens their editor to, and `block` is the index of the paragraph block
    the sentence came from, which is what the near-the-first-use window is
    measured in.
    """
    lines = text.splitlines()
    cues = _definition_cues(symbol)
    found: list[dict] = []
    for block_index, indices in enumerate(_paragraph_blocks(lines)):
        joined, spans = _join_block(lines, indices)
        for offset, sentence in _sentences(joined):
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


def _block_of_line(blocks: list[list[int]], line_index: int) -> int | None:
    for i, indices in enumerate(blocks):
        if line_index in indices:
            return i
    return None


# --------------------------------------------------------------------------
# The `## Concepts to teach` index and the DESIGN.md index.
# --------------------------------------------------------------------------


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
    _, body = bl.split_frontmatter(lesson_text)
    section: str | None = None
    for heading, section_body in _sections(body):
        if heading.strip().lower() == "concepts to teach":
            section = section_body
            break
    if section is None:
        return False, {}

    offset = body.index(section)
    first_line = body.count("\n", 0, offset) + 1
    frontmatter_lines = lesson_text.count("\n", 0, lesson_text.index(body)) if body else 0

    named: dict[str, dict] = {}
    backticked: set[str] = set()
    for lineno, line in enumerate(section.splitlines(), start=first_line):
        real_line = lineno + frontmatter_lines
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
    for lineno, line in enumerate(section.splitlines(), start=first_line):
        real_line = lineno + frontmatter_lines
        stripped = _INLINE_CODE_RE.sub(" ", line)
        for word in re.findall(r"(?<![A-Za-z0-9_])([A-Za-z_][A-Za-z0-9_]*)(?![A-Za-z0-9_])", stripped):
            if len(word) <= _MAX_SYMBOL_LEN and word not in backticked:
                bare.setdefault(word, {"line": real_line, "text": line.strip(), "form": "bare"})
    for symbol, hit in bare.items():
        named.setdefault(symbol, hit)
    return True, named


def design_symbol_index(design_text: str) -> dict[str, dict]:
    """Where DESIGN.md mentions each candidate symbol, and under which anchor.

    A DESIGN.md mention NEVER introduces a symbol to a learner - the runner
    loads an anchor for the TUTOR - so this index exists only to separate
    "bound solely in DESIGN.md" from "bound nowhere at all", which the issue
    requires be reported distinctly.
    """
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
_BINDING_ORDER = [
    "concepts",
    "lesson-prose-in-window",
    "lesson-prose-elsewhere",
    "other-lesson-prose",
    "design-md-only",
    "none",
]


def build_symbol_evidence(bundle: bl.Bundle) -> dict:
    """Per lesson, per candidate symbol: the evidence, never a verdict.

    `status` separates NOTHING TO CHECK from CHECKED AND CLEAN. A bundle
    whose lessons declare no `## Concepts to teach` section anywhere, or
    whose `DESIGN.md` could not be read, has lost an evidence channel, and an
    empty `unbound` list from such a bundle means something entirely
    different from an empty list produced with every channel alive. The same
    goes for a bundle in which no candidate symbol was found at all. Both are
    reported as `status` plus a populated `warnings` list, never as silence.
    """
    warnings: list[str] = []

    design_text = bl.read_text(bundle.root / "DESIGN.md")
    design_present = (bundle.root / "DESIGN.md").exists()
    if design_text is None:
        design_index: dict[str, dict] = {}
        warnings.append(
            "DESIGN.md could not be read"
            + (" (the file is present but unreadable)" if design_present else " (no such file)")
            + " - the 'defined only in DESIGN.md' column is BLIND for this bundle, "
            "so every symbol it would have bound is reported as bound nowhere."
        )
    else:
        design_index = design_symbol_index(design_text)

    lessons_scanned = 0
    unreadable: list[str] = []
    fenced_blocks = 0
    concepts_lessons: list[str] = []
    without_concepts: list[str] = []
    concepts_named: dict[str, list[dict]] = {}
    # (lesson, body with fences blanked, uses, paragraph blocks, frontmatter
    # line offset). Every line number inside the stripped BODY is offset by
    # `prefix` to become a line number in the lesson FILE, which is what a
    # reader opens their editor to.
    per_lesson: list[tuple[bl.Lesson, str, list[dict], list[list[int]], int]] = []

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

        _, body = bl.split_frontmatter(raw)
        prefix_lines = raw.count("\n", 0, raw.index(body)) if body else 0
        stripped, opened = strip_fenced_blocks(body)
        fenced_blocks += opened
        uses = symbol_uses(stripped)
        for use in uses:
            use["line"] += prefix_lines
        per_lesson.append(
            (lesson, stripped, uses, _paragraph_blocks(stripped.splitlines()), prefix_lines)
        )

    if not concepts_lessons and lessons_scanned:
        warnings.append(
            "NO lesson in this bundle declares a '## Concepts to teach' section - "
            "the 'some lesson names it' column is BLIND for this bundle. Every "
            "candidate below is reported as un-introduced by that channel because "
            "the channel does not exist here, not because a reader checked it."
        )

    # Every distinct candidate symbol, looked for in EVERY lesson, so that a
    # definition in a different lesson is a column of its own rather than an
    # absence that would make `design-md-only` lie (see `_BINDING_ORDER`).
    all_symbols = sorted({use["symbol"] for _, _, uses, _, _ in per_lesson for use in uses})
    definitions_by_lesson: dict[str, dict[str, list[dict]]] = {}
    for lesson, stripped, _uses, _blocks, prefix in per_lesson:
        found: dict[str, list[dict]] = {}
        for symbol in all_symbols:
            rows = find_definitions(symbol, stripped)
            if rows:
                found[symbol] = [dict(row, line=row["line"] + prefix) for row in rows]
        definitions_by_lesson[lesson.rel] = found

    candidates: list[dict] = []
    for lesson, stripped, uses, blocks, prefix in per_lesson:
        seen: set[str] = set()
        for use in uses:
            symbol = use["symbol"]
            if symbol in seen:
                continue
            seen.add(symbol)

            definitions = definitions_by_lesson[lesson.rel].get(symbol, [])

            use_block = _block_of_line(blocks, use["line"] - prefix - 1)
            in_window: dict | None = None
            elsewhere: list[dict] = []
            for d in definitions:
                row = {
                    "rel": lesson.rel,
                    "line": d["line"],
                    "cue": d["cue"],
                    "sentence": d["sentence"],
                }
                near = use_block is not None and abs(d["block"] - use_block) <= 1
                if near and in_window is None:
                    row["offset_lines"] = row["line"] - use["line"]
                    in_window = row
                elif not near:
                    elsewhere.append(row)

            other_lessons: list[dict] = []
            for rel, found in definitions_by_lesson.items():
                if rel == lesson.rel:
                    continue
                for d in found.get(symbol, []):
                    other_lessons.append(
                        {"rel": rel, "line": d["line"], "cue": d["cue"], "sentence": d["sentence"]}
                    )

            concepts_hits = concepts_named.get(symbol, [])
            design_hit = design_index.get(symbol)

            if concepts_hits:
                binding = "concepts"
            elif in_window is not None:
                binding = "lesson-prose-in-window"
            elif elsewhere:
                binding = "lesson-prose-elsewhere"
            elif other_lessons:
                binding = "other-lesson-prose"
            elif design_hit is not None:
                binding = "design-md-only"
            else:
                binding = "none"

            candidates.append(
                {
                    "symbol": symbol,
                    "lesson": lesson.rel,
                    "first_use": {
                        "rel": lesson.rel,
                        "line": use["line"],
                        "span": use["span"],
                        "text": use["text"],
                    },
                    "named_in_concepts": concepts_hits,
                    "defined_in_window": in_window,
                    "defined_elsewhere_in_lesson": elsewhere,
                    "defined_in_other_lessons": other_lessons,
                    "design_md": (
                        None
                        if design_hit is None
                        else {
                            "line": design_hit["line"],
                            "text": design_hit["text"],
                            "anchors": design_hit["anchors"],
                        }
                    ),
                    "binding": binding,
                }
            )

    candidates.sort(key=lambda c: (c["lesson"], c["first_use"]["line"], c["symbol"]))

    if lessons_scanned == 0:
        status = "nothing-to-check"
        warnings.append(
            "NO lesson text could be read at all - nothing was checked. This is "
            "not a clean result."
        )
    elif not candidates:
        status = "nothing-to-check"
        warnings.append(
            f"NO candidate symbol was found in any of the {lessons_scanned} lesson(s) "
            f"scanned ({fenced_blocks} fenced code block(s) were skipped, as this "
            f"scanner only reads INLINE backticked spans). 'No candidate found' is "
            f"NOT 'no undefined symbol' - read the lessons."
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
        "window": SYMBOL_WINDOW,
        "disclaimer": SYMBOL_DISCLAIMER,
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
            "candidate_rows": len(candidates),
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

    out.extend(render_symbol_evidence(data["symbol_evidence"]))

    out.append(f"DESIGN.md anchors ({len(data['anchors'])}): {', '.join(data['anchors']) or '(none)'}")
    return "\n".join(out)


_BINDING_HEADINGS = {
    "none": "Used, and introduced NOWHERE this scanner can see",
    "design-md-only": "Bound ONLY in DESIGN.md - the runner loads an anchor for the TUTOR, not for the learner, so this does NOT introduce the symbol to a learner",
    "lesson-prose-elsewhere": "A defining sentence exists in the same lesson but OUTSIDE the near-the-first-use window - is it early enough? A reader decides",
    "other-lesson-prose": "No same-lesson introduction: the only defining sentence is in a DIFFERENT lesson. A learner who reaches this lesson without that one has met no definition",
    "lesson-prose-in-window": "A defining sentence is near the first use - read the sentence and decide whether it really defines the symbol",
    "concepts": "Some lesson's '## Concepts to teach' names it - read the bullet and decide whether it really introduces the symbol",
}


def render_symbol_evidence(ev: dict) -> list[str]:
    out: list[str] = []
    out.append("## Short symbols a lesson uses")
    out.append("")
    out.append(f"status: {ev['status']}")
    out.append("")
    out.append(f"Candidate rule: {ev['rule']}")
    out.append("")
    out.append(f"Window: {ev['window']}")
    out.append("")
    out.append(ev["disclaimer"])
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
            out.append(f"- `{c['symbol']}` first used at {use['rel']}:{use['line']} (written `{use['span']}`)")
            out.append(f"    {use['text']}")
            for hit in c["named_in_concepts"]:
                out.append(
                    f"    concepts: {hit['rel']}:{hit['line']} [{hit['form']}] {hit['text']}"
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
