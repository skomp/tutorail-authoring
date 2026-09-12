#!/usr/bin/env python3
"""yamlite.py is a VENDORED VERBATIM COPY - prove it has not drifted.

Run it:  python3 tests/test_yamlite_drift.py

skills/tutorail-authoring/scripts/yamlite.py is a byte-for-byte copy of the
runner's skills/tutorail/scripts/yamlite.py, with a provenance banner of
comment lines prepended. It is copied rather than imported so index.py and
catalog.py, which mutate nothing, work without the runner installed.

A vendored copy that drifts is worse than no copy at all: two readers that
disagree about one document mean the authoring tool and the validator
certify different things, and nothing anywhere reports it. That is the whole
reason this file exists.

It checks the same claim twice, by two independent methods:

  * TEXT      - the vendored file ends with the runner's file, byte for byte,
                and everything above that is comment lines.
  * BEHAVIOUR - both readers parse the same documents to the same values, and
                REJECT the same documents with the same message. A drift that
                somehow survived a byte comparison would still have to survive
                this.

Both checks carry a positive control: a deliberately perturbed copy, run
through the SAME comparison, which must report drift. A comparison nobody has
seen fail is not a comparison.

If the runner cannot be found, this suite does NOT pass. A silently skipped
drift check is a false oracle - it reads as "no drift" forever.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from harness import (  # noqa: E402
    FIXTURES,
    SCRIPTS,
    case,
    check,
    check_in,
    has_exactly,
    note,
    report,
)

import bundlelib as bl  # noqa: E402  (harness put the scripts dir on sys.path)

VENDORED = SCRIPTS / "yamlite.py"


# --------------------------------------------------------------------------
# The comparison, written once so the positive control can reuse it
# --------------------------------------------------------------------------


def drift_reason(vendored_text: str, runner_text: str) -> str:
    """Return "" when there is no drift, else why there is.

    The split is worked out from the files rather than from a hard-coded line
    count: the copied region is exactly the runner's file, so the vendored
    text must END WITH it, and whatever precedes it must be comment lines.
    Nothing here needs to know how long the banner is.
    """
    if not runner_text:
        return "the runner's yamlite.py is empty"
    if not vendored_text.endswith(runner_text):
        # Locate the divergence so the message is actionable rather than "no".
        tail = vendored_text[-len(runner_text) :]
        position = next(
            (i for i, (a, b) in enumerate(zip(tail, runner_text)) if a != b),
            min(len(tail), len(runner_text)),
        )
        return (
            f"the vendored file does not end with the runner's file; the last "
            f"{len(runner_text)} characters first differ at offset {position}: "
            f"vendored {tail[position:position + 30]!r} vs runner "
            f"{runner_text[position:position + 30]!r}"
        )
    banner = vendored_text[: len(vendored_text) - len(runner_text)]
    offenders = [
        line
        for line in banner.split("\n")
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if offenders:
        return (
            f"the region above the copied text is not all comment lines; "
            f"{len(offenders)} line(s) are code, first: {offenders[0]!r}"
        )
    return ""


def banner_of(vendored_text: str, runner_text: str) -> str:
    return vendored_text[: len(vendored_text) - len(runner_text)]


def load_by_path(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------
# The documents both readers must agree about
# --------------------------------------------------------------------------


def parseable_documents() -> dict[str, str]:
    manifest = (FIXTURES / "rust-automaton-db" / "tutorial.yaml").read_text(
        encoding="utf-8"
    )
    lesson = (FIXTURES / "rust-automaton-db" / "lessons" / "00-foundations.md").read_text(
        encoding="utf-8"
    )
    frontmatter, _ = bl.split_frontmatter(lesson)
    assert frontmatter is not None, "fixture drifted: 00-foundations.md has no frontmatter"
    return {
        "the real rust-automaton-db tutorial.yaml": manifest,
        "a real lesson's frontmatter": frontmatter,
        "a flow sequence": "subjects: [rust, databases, distributed-systems]\n",
        "a flow mapping": (
            "validators:\n"
            "  cargo-check: { kind: command, command: [cargo, check] }\n"
            "  manual: { kind: manual }\n"
        ),
        "a '>' folded block scalar": (
            "reason: >\n"
            "  The learner could not get the borrow checker to accept their\n"
            "  RowRef, and nothing on the main path teaches lifetime elision.\n"
            "after: lessons/03-first-refactor.md\n"
        ),
        "a '|' literal block scalar": (
            "description: |\n"
            "  Line one, kept as written.\n"
            "    Line two, indented further.\n"
            "\n"
            "  Line four, after a blank.\n"
            "id: kept\n"
        ),
    }


def rejected_documents() -> dict[str, str]:
    """Documents the restricted reader must REFUSE, in both copies.

    A comparison where neither reader raises proves nothing about rejection,
    so each of these is asserted to have actually raised on both sides before
    the messages are compared.
    """
    return {
        "an anchor (&name)": "id: &base rust-automaton-db\ntitle: t\n",
        "a tab in the indentation": "lessons:\n\t- lessons/00-foundations.md\n",
        "an alias (*name)": "id: x\ntitle: *base\n",
        "a tag (!name)": "id: !!str 17\n",
    }


# --------------------------------------------------------------------------


def main() -> int:
    print("test_yamlite_drift.py - the vendored yamlite.py against the runner's")
    print()

    # -- locate the runner. A miss here must NOT read as "no drift".
    try:
        runner_root, how = bl.find_runner_root()
    except bl.ToolError as exc:
        print("!" * 72)
        print("SKIPPED - AND THAT IS A FAILURE, NOT A PASS.")
        print("The tutorAIl runner could not be found, so the vendored yamlite.py")
        print("has NOT been compared against anything. A drift check that silently")
        print("skips reads as 'no drift' forever, which is the false oracle this")
        print("whole suite exists to avoid.")
        print()
        print(str(exc))
        print("!" * 72)
        return 2

    runner_yamlite = runner_root / "scripts" / "yamlite.py"
    if not has_exactly(runner_root / "scripts", "yamlite.py"):
        print("!" * 72)
        print("FAILED - the runner was found but its yamlite.py was not.")
        print(f"  runner: {runner_root}  ({how})")
        print(f"  looked for: {runner_yamlite}")
        print(f"  scripts/ holds: {sorted(bl.list_dir(runner_root / 'scripts'))}")
        print("!" * 72)
        return 2

    note(f"runner: {runner_root}  ({how})")
    note(f"compared: {VENDORED}")
    note(f"     against: {runner_yamlite}")

    vendored_text = VENDORED.read_text(encoding="utf-8")
    runner_text = runner_yamlite.read_text(encoding="utf-8")

    with case("1  the vendored file is the runner's file with a comment banner"):
        reason = drift_reason(vendored_text, runner_text)
        check(reason == "", f"no drift: {reason or 'the copied region is identical'}")
        banner = banner_of(vendored_text, runner_text)
        check(
            len(banner) > 0,
            f"there is a banner above the copied region ({len(banner)} characters)",
        )
        check(
            len(vendored_text) == len(banner) + len(runner_text),
            f"the vendored file is exactly banner + runner file "
            f"({len(banner)} + {len(runner_text)} = {len(vendored_text)})",
        )
        # The banner has to say where the copy came from, or the next reader
        # has no way to re-copy it.
        check_in(
            "tutorAIl/skills/tutorail/scripts/yamlite.py",
            banner,
            "the banner names the upstream file it was copied from",
        )
        check_in(
            "byte-identical",
            banner,
            "the banner states the byte-identity claim this suite checks",
        )
        check_in(
            "Do not edit below this line",
            banner,
            "the banner tells the next reader to re-copy rather than edit",
        )

    with case("2  POSITIVE CONTROL: the same comparison reports drift when there is drift"):
        # One character. If the comparison cannot see this it cannot see
        # anything, and case 1's clean result would mean nothing.
        marker = "a tab is used for indentation"
        check_in(
            marker,
            runner_text,
            "positive control setup: the marker string is in the runner's file",
        )
        one_character = runner_text.replace(marker, marker[:-1] + "m", 1)
        check(
            len(one_character) == len(runner_text) and one_character != runner_text,
            "the perturbed copy differs from the runner's file by exactly one "
            "character, and nothing else",
        )
        reason = drift_reason(vendored_text, one_character)
        check(
            reason != "",
            f"the SAME comparison reports drift for the one-character change "
            f"(reason: {reason[:120]!r})",
        )
        check_in(
            "first differ at offset",
            reason,
            "the drift report says where the two files diverge",
        )

        # Whitespace only, because a comparison that normalised whitespace
        # would pass the test above and still miss a real edit.
        trailing_space = runner_text.replace("\nclass YamlError", " \nclass YamlError", 1)
        check(
            trailing_space != runner_text,
            "positive control setup: the whitespace perturbation changed something",
        )
        check(
            drift_reason(vendored_text, trailing_space) != "",
            "the comparison is byte-exact: one added space is drift",
        )

        # A truncation, which is the shape a bad re-copy actually takes.
        truncated = runner_text[: len(runner_text) // 2]
        check(
            drift_reason(vendored_text, truncated) != "",
            "a truncated runner file is reported as drift",
        )

        # And the OTHER half of the comparison: code smuggled into the banner.
        # Without this the banner check could be dead code and case 1 would
        # never notice.
        polluted = "import os  # not a comment\n" + vendored_text
        polluted_reason = drift_reason(polluted, runner_text)
        check(
            polluted_reason != "",
            f"a non-comment line above the copied region is reported as drift "
            f"(reason: {polluted_reason[:120]!r})",
        )
        check_in(
            "not all comment lines",
            polluted_reason,
            "the banner half of the comparison says what is wrong",
        )
        # Control for the control: the unpolluted text still reads clean, so
        # the assertion above is about the added line and nothing else.
        check(
            drift_reason(vendored_text, runner_text) == "",
            "control for the control: without the added line the same call is "
            "still clean",
        )

    # ------------------------------------------------------------------
    # Behavioural equivalence - the second, independent check
    # ------------------------------------------------------------------

    vendored_mod = load_by_path("vendored_yamlite", VENDORED)
    runner_mod = load_by_path("runner_yamlite", runner_yamlite)

    with case("3  both copies load, and the toolkit really uses the vendored one"):
        import yamlite as imported  # the module bundlelib gets

        check(
            Path(imported.__file__).resolve() == VENDORED.resolve(),
            f"a plain `import yamlite` from the scripts directory resolves to "
            f"the vendored file (got {imported.__file__})",
        )
        check(
            Path(runner_mod.__file__).resolve() == runner_yamlite.resolve(),
            f"the second module really is the runner's file "
            f"(got {runner_mod.__file__})",
        )
        check(
            vendored_mod.YAML_READER == runner_mod.YAML_READER,
            f"both report the same reader backend "
            f"({vendored_mod.YAML_READER!r} vs {runner_mod.YAML_READER!r})",
        )

    with case("4  both readers parse the same documents to the same values"):
        results: dict[str, object] = {}
        for label, document in parseable_documents().items():
            mine = vendored_mod.load_yaml(document, label)
            theirs = runner_mod.load_yaml(document, label)
            check(
                mine == theirs,
                f"{label}: identical parse "
                f"({str(mine)[:80]!r} vs {str(theirs)[:80]!r})",
            )
            results[label] = mine

        # The values themselves, not just the agreement: two readers that both
        # returned None for everything would agree perfectly.
        manifest = results["the real rust-automaton-db tutorial.yaml"]
        check(
            isinstance(manifest, dict) and manifest.get("id") == "rust-automaton-db",
            f"the manifest parsed to a mapping with the right id "
            f"(got {type(manifest).__name__})",
        )
        check(
            isinstance(manifest, dict) and len(manifest.get("lessons", [])) == 23,
            "the manifest's lessons list has its 23 entries",
        )
        flow_seq = results["a flow sequence"]
        check(
            flow_seq == {"subjects": ["rust", "databases", "distributed-systems"]},
            f"the flow sequence parsed to its three items (got {flow_seq!r})",
        )
        flow_map = results["a flow mapping"]
        check(
            isinstance(flow_map, dict)
            and flow_map["validators"]["cargo-check"]["command"] == ["cargo", "check"],
            f"the nested flow mapping parsed to a nested structure "
            f"(got {flow_map!r})",
        )
        folded = results["a '>' folded block scalar"]
        check(
            isinstance(folded, dict)
            and folded["reason"].startswith("The learner could not get")
            and "\n" not in folded["reason"].rstrip("\n")
            and folded["after"] == "lessons/03-first-refactor.md",
            f"the folded scalar folded its two lines into one and the next key "
            f"still parsed (got {folded!r})",
        )
        literal = results["a '|' literal block scalar"]
        check(
            isinstance(literal, dict)
            and literal["description"].splitlines()[1] == "  Line two, indented further."
            and literal["id"] == "kept",
            f"the literal scalar kept its relative indentation and its blank "
            f"line (got {literal!r})",
        )

        # POSITIVE CONTROL for the equality operator itself: show it reporting
        # a difference. Comparing the vendored reader's parse of one document
        # against the runner's parse of ANOTHER must not come out equal.
        mismatch = vendored_mod.load_yaml(
            "subjects: [rust, databases, distributed-systems]\n", "a"
        ) == runner_mod.load_yaml("subjects: [rust]\n", "b")
        check(
            not mismatch,
            "positive control: the same equality check reports a difference when "
            "the two readers are given different documents",
        )

    with case("5  both readers REJECT the same documents, with the same message"):
        for label, document in rejected_documents().items():
            mine_error = None
            theirs_error = None
            try:
                parsed = vendored_mod.load_yaml(document, label)
            except vendored_mod.YamlError as exc:
                mine_error = exc
            else:
                check(False, f"{label}: the vendored reader did NOT raise (got {parsed!r})")
            try:
                parsed = runner_mod.load_yaml(document, label)
            except runner_mod.YamlError as exc:
                theirs_error = exc
            else:
                check(False, f"{label}: the runner's reader did NOT raise (got {parsed!r})")

            # Both must actually have raised. A comparison of two None values
            # would otherwise pass while proving nothing about rejection.
            check(
                mine_error is not None and theirs_error is not None,
                f"{label}: BOTH readers raised, so the comparison below is real",
            )
            if mine_error is None or theirs_error is None:
                continue
            check(
                type(mine_error).__name__ == type(theirs_error).__name__ == "YamlError",
                f"{label}: both raised YamlError "
                f"({type(mine_error).__name__} vs {type(theirs_error).__name__})",
            )
            check(
                str(mine_error) == str(theirs_error),
                f"{label}: identical message ({str(mine_error)[:90]!r} vs "
                f"{str(theirs_error)[:90]!r})",
            )
            # The value, not the shape: the message has to say which line and
            # what the construct was, or it is not the message that helps.
            check(
                "line " in str(mine_error),
                f"{label}: the message names a line number "
                f"({str(mine_error)[:90]!r})",
            )

        # POSITIVE CONTROL: the readers do not reject everything. A reader that
        # raised YamlError on every input would satisfy case 5 completely.
        accepted = vendored_mod.load_yaml("id: x\ntitle: y\n", "control")
        check(
            accepted == {"id": "x", "title": "y"},
            f"positive control: a supported document is accepted, so the "
            f"rejections above are selective (got {accepted!r})",
        )
    return report("test_yamlite_drift.py")


if __name__ == "__main__":
    sys.exit(main())
