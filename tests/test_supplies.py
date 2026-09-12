#!/usr/bin/env python3
"""Test suite for bundlelib's supplies-entry writer: the unit half.

Run it with:  python3 tests/test_supplies.py

`supplies:` is what tells a runner which files a course hands the learner's
workspace, so no lesson ever assigns "copy these files" as a task. This
suite covers the three functions bundlelib gives every caller that needs to
write one:

  emit_scalar             a single YAML scalar, quoted only when it has to be
  render_supplies_item    the lines for one supplies entry
  add_supplies            append an entry to a manifest or a frontmatter block

A second half - the `supplies.py` command-line tool built on top of these -
is a later task and appends to this same file.

The central risk here is silent corruption: an emitter that writes bytes
which parse into something the author did not type. So every case in this
file is a ROUND TRIP - the emitted text is parsed back through this
project's own restricted loader, `yamlite.load_yaml`, and the parsed value
is compared against what went in. A test that only checked "it looks quoted"
would miss exactly the bug this file exists to catch.
"""

from __future__ import annotations

import sys
from pathlib import Path

import harness as h
from harness import case, check, report

sys.path.insert(0, str(h.SCRIPTS))
import bundlelib as bl  # noqa: E402  (harness put the scripts dir on sys.path)
from bundlelib import load_yaml  # noqa: E402


# --------------------------------------------------------------------------
# emit_scalar
# --------------------------------------------------------------------------


def test_emit_scalar_round_trips_the_hard_cases() -> None:
    for value in [
        "npm workspace",
        "Duck.glb: the sample model",              # a colon
        "the #1 thing this lesson needs",          # a hash
        "  leading and trailing  ",                # whitespace that YAML would eat
        'she said "copy it"',                      # quotes
        "a - b",                                   # a dash
        "{not a flow mapping}",                    # a brace
    ]:
        emitted = bl.emit_scalar(value)
        doc = f"describe: {emitted}\n"
        back = load_yaml(doc, "probe")
        check(back["describe"] == value, f"emit_scalar round-trips {value!r} (emitted {emitted!r})")


def test_emit_scalar_does_not_confuse_a_string_for_the_thing_it_looks_like() -> None:
    """The defect found in this task's proposed implementation.

    A character-class regex ("anything in [A-Za-z0-9 ._/-] is safe unquoted")
    was proposed for emit_scalar and never run. Measured against yamlite, it
    is wrong: "123", "true", "null" and similar all satisfy that regex and
    all come back as the WRONG PYTHON TYPE - an int, a bool, or None -
    instead of the string that was given. That is silent corruption of
    exactly the kind emit_scalar exists to prevent, and it would not have
    been caught by the round-trip cases above, none of which look like a
    YAML literal.

    emit_scalar as implemented asks the loader directly instead of guessing,
    so every one of these must come back as the identical string.
    """
    for value in [
        "123",
        "0",
        "3.14",
        "true",
        "True",
        "TRUE",
        "false",
        "False",
        "FALSE",
        "null",
        "Null",
        "NULL",
        "~",
        "",
    ]:
        emitted = bl.emit_scalar(value)
        doc = f"describe: {emitted}\n"
        back = load_yaml(doc, "probe")
        check(
            back["describe"] == value and isinstance(back["describe"], str),
            f"emit_scalar round-trips look-alike {value!r} as a string "
            f"(emitted {emitted!r}, got back {back['describe']!r})",
        )

    # POSITIVE CONTROL: a value that is NOT a look-alike is still left
    # unquoted. Without this, the loop above would pass identically if
    # emit_scalar quoted every value unconditionally, which would prove
    # nothing about the actual defect.
    plain = bl.emit_scalar("npm workspace")
    check(
        plain == "npm workspace",
        f"positive control: an ordinary value is still left unquoted (got {plain!r})",
    )


# --------------------------------------------------------------------------
# render_supplies_item
# --------------------------------------------------------------------------


def test_render_supplies_item_orders_keys_and_indents_two_spaces() -> None:
    entry = {"from": "supplies/workspace/", "to": ".", "describe": "the workspace"}
    lines = bl.render_supplies_item(entry)
    check(lines[0] == "  - from: supplies/workspace/", f"first line carries 'from' at the item marker (got {lines[0]!r})")
    check(lines[1] == "    to: .", f"second line carries 'to', four-space indented (got {lines[1]!r})")
    check(lines[2] == "    describe: the workspace", f"third line carries 'describe' (got {lines[2]!r})")
    check(len(lines) == 3, "exactly one line per key")


def test_render_supplies_item_refuses_a_missing_key() -> None:
    try:
        bl.render_supplies_item({"from": "x/", "to": "y/"})
        check(False, "a supplies entry missing 'describe' raises ToolError")
    except bl.ToolError as exc:
        check(True, "a supplies entry missing 'describe' raises ToolError")
        check("describe" in str(exc), f"the message names the missing key (got {exc!r})")

    # POSITIVE CONTROL beside the refusal: the same shape, complete, does not raise.
    complete = bl.render_supplies_item({"from": "x/", "to": "y/", "describe": "z"})
    check(len(complete) == 3, "positive control: a complete entry renders fine")


# --------------------------------------------------------------------------
# add_supplies
# --------------------------------------------------------------------------


def test_add_supplies_creates_the_block_then_appends_to_it() -> None:
    text = "bundle_format: 1\nid: x\n"
    entry = {"from": "supplies/workspace/", "to": ".", "describe": "the workspace"}
    once = bl.add_supplies(text, entry, frontmatter=False)
    twice = bl.add_supplies(once, {"from": "m/", "to": "models/",
                                   "describe": "the model"}, frontmatter=False)
    parsed = load_yaml(twice, "probe")
    check(len(parsed["supplies"]) == 2, "two entries after two adds")
    check(parsed["supplies"][0] == entry, "the first entry survived the second add")
    check(parsed["id"] == "x", "the rest of the manifest is untouched")


def test_add_supplies_in_frontmatter_leaves_the_body_alone() -> None:
    text = "---\nid: 00-x\ntitle: X\n---\n\n## Purpose\n\nTeach something.\n"
    out = bl.add_supplies(text, {"from": "lessons/00-x/model/", "to": "models/",
                                 "describe": "the model"}, frontmatter=True)
    fm, body = bl.split_frontmatter(out)
    check(load_yaml(fm, "probe")["supplies"][0]["to"] == "models/", "entry is in the frontmatter")
    check(body.strip().startswith("## Purpose"), "the body is unchanged")


def test_add_supplies_refuses_an_inline_supplies_value() -> None:
    """`supplies: []` (or any other inline value) is not guessed at.

    Mirrors replace_lessons_list's refusal of a non-empty inline `lessons:`:
    rewriting an author's inline flow value into block form is a bigger
    change than "append one entry", so this raises ManifestEditError
    instead.
    """
    text = "bundle_format: 1\nsupplies: []\nid: x\n"
    entry = {"from": "x/", "to": "y/", "describe": "z"}
    try:
        bl.add_supplies(text, entry, frontmatter=False)
        check(False, "an inline 'supplies: []' raises ManifestEditError")
    except bl.ManifestEditError:
        check(True, "an inline 'supplies: []' raises ManifestEditError")

    # POSITIVE CONTROL: the block form of the same manifest is not refused.
    block_text = "bundle_format: 1\nsupplies:\n  - from: a/\n    to: b/\n    describe: c\nid: x\n"
    out = bl.add_supplies(block_text, entry, frontmatter=False)
    check(
        load_yaml(out, "probe")["supplies"][-1] == entry,
        "positive control: the block form is appended to normally",
    )


def test_add_supplies_catches_a_broken_emitter() -> None:
    """The round-trip check inside add_supplies is a real check, not a comment.

    render_supplies_item is monkeypatched to write bytes that do not match
    the given entry, and add_supplies must refuse to return them. A check
    that has never been shown firing has not been tested - this is that
    demonstration for add_supplies's own honesty check.
    """
    original = bl.render_supplies_item
    text = "bundle_format: 1\nid: x\n"
    entry = {"from": "real/", "to": "real-to/", "describe": "real describe"}
    try:
        bl.render_supplies_item = lambda _entry: [
            "  - from: wrong",
            "    to: also-wrong",
            "    describe: nope",
        ]
        try:
            bl.add_supplies(text, entry, frontmatter=False)
            check(False, "add_supplies raises when the written entry does not match what was given")
        except bl.ToolError:
            check(True, "add_supplies raises when the written entry does not match what was given")
    finally:
        bl.render_supplies_item = original

    # POSITIVE CONTROL: with the real emitter restored, the identical call succeeds.
    out = bl.add_supplies(text, entry, frontmatter=False)
    check(
        load_yaml(out, "probe")["supplies"][-1] == entry,
        "positive control: the same call succeeds once the emitter is restored",
    )


# --------------------------------------------------------------------------


def main() -> int:
    print("bundlelib supplies-entry writer test suite (unit half)")
    print()
    with case("emit_scalar round-trips the hard cases"):
        test_emit_scalar_round_trips_the_hard_cases()
    with case("emit_scalar does not confuse a string for the thing it looks like"):
        test_emit_scalar_does_not_confuse_a_string_for_the_thing_it_looks_like()
    with case("render_supplies_item orders keys and indents two spaces"):
        test_render_supplies_item_orders_keys_and_indents_two_spaces()
    with case("render_supplies_item refuses a missing key"):
        test_render_supplies_item_refuses_a_missing_key()
    with case("add_supplies creates the block, then appends to it"):
        test_add_supplies_creates_the_block_then_appends_to_it()
    with case("add_supplies in frontmatter leaves the body alone"):
        test_add_supplies_in_frontmatter_leaves_the_body_alone()
    with case("add_supplies refuses an inline supplies value"):
        test_add_supplies_refuses_an_inline_supplies_value()
    with case("add_supplies catches a broken emitter"):
        test_add_supplies_catches_a_broken_emitter()
    return report("test_supplies.py")


if __name__ == "__main__":
    sys.exit(main())
