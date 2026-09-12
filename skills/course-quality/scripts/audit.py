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
# of a sentence, of an introductory clause set off by a comma, or right
# after "must"/"should"/"then" - so that a noun phrase like "a direct-copy
# composition shader" does not fire just because it contains the word
# "copy", and so that "Do not copy X" (an instruction NOT to do something)
# does not fire either, since "copy" there follows "not ", not a lead.
#
# The comma alternative is load-bearing. Real toil in the corpus reads
# "Before starting, copy every file under `model/` ..." - an introductory
# clause, so the verb is neither at the start of the line nor after a full
# stop. Without it the scanner misses
# webgl-typescript-scene/lessons/13-load-gltf-model/LESSON.md:40, which is
# one of the two sites this script is required to find.
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
    r"(?:^|^[-*]\s+|(?<=[.!?]\s)|(?<=,\s)|"
    r"(?<=\bmust\s)|(?<=\bshould\s)|(?<=\bthen\s))"
)

_TOIL_PATTERNS = {
    name: re.compile(_LEAD + r"\b(?:" + verb + r")\b", re.IGNORECASE)
    for name, verb in TOIL_VERBS.items()
}


def scan_toil(rel: str, text: str) -> list[dict]:
    """Candidate toil sites in `text`, scanned one physical line at a time.

    Each hit carries the whole raw line as `text`, not just the matched
    span, so a reader (or a test) can see the sentence the verb sits in.
    """
    candidates: list[dict] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for name, pattern in _TOIL_PATTERNS.items():
            if pattern.search(line):
                candidates.append(
                    {
                        "rel": rel,
                        "line": lineno,
                        "text": line.strip(),
                        "pattern": name,
                    }
                )
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
    """The bundle's coverage list, or None when it declares none.

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
    "Explicit boundaries", "Prerequisites", ...) do not. A heading match
    with no bullet list under it is not a coverage list - keep looking.
    """
    if course_text is None:
        return None
    for heading, body in _sections(course_text):
        if "cover" not in heading.lower():
            continue
        topics = _bullets(body)
        if topics:
            return {"heading": heading, "topics": topics}
    return None


def learning_objectives(lesson_text: str) -> list[str]:
    """The bullets under a lesson's `## Learning objectives` section."""
    _, body = bl.split_frontmatter(lesson_text)
    for heading, section_body in _sections(body):
        if heading.strip().lower() == "learning objectives":
            return _bullets(section_body)
    return []


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


def _lesson_tokens(lesson: bl.Lesson, fm: dict) -> set[str]:
    parts = [str(fm.get("title", "")), lesson.slug]
    parts.extend(as_names(fm.get("design_refs")))
    text = bl.read_text(lesson.path)
    if text is not None:
        parts.extend(learning_objectives(text))
    return _tokenize(" ".join(parts))


def topic_candidates_for(
    topics: list[str], lesson_tokens: list[tuple[bl.Lesson, set[str]]]
) -> dict:
    """Possible topic-to-lesson matches, from word overlap alone.

    Never claims a topic is covered (see TOPIC_DISCLAIMER). An empty hit
    list for a topic is itself worth a human's attention - it says no
    lesson's title, slug, design_refs or learning objectives share a
    meaningful word with it - but it is not proof the topic goes untaught;
    a lesson may teach it under different words entirely.
    """
    out: dict[str, list[dict]] = {}
    for topic in topics:
        topic_tokens = _tokenize(topic)
        hits = []
        for lesson, tokens in lesson_tokens:
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
            "COURSE.md declares no coverage list. This is a finding, not an "
            "empty result: the course has no declared boundary for a tutor "
            "to check a blocked learner's topic against."
        )
    else:
        out.append(f'Under "{cov["heading"]}":')
        out.extend(f"- {topic}" for topic in cov["topics"])
        out.append("")
        out.append(TOPIC_DISCLAIMER)
        for topic, hits in data["topic_candidates"].items():
            if hits:
                names = ", ".join(h["rel"] for h in hits[:3])
                out.append(f"  - {topic}: candidate lesson(s) -> {names}")
            else:
                out.append(
                    f"  - {topic}: no candidate lesson found "
                    f"(a possible gap - read the course before concluding that)"
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
