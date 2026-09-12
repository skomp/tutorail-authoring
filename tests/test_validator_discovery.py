#!/usr/bin/env python3
"""Validator discovery - the false-oracle guard for the whole toolkit.

Run it:  python3 tests/test_validator_discovery.py

The toolkit makes exactly one safety promise: a mutating operation never
leaves a bundle broken and reports it as done. That promise IS the runner's
validator. So when the validator cannot be found there is only one honest
answer - refuse - and the thing this file exists to prove is that the refusal
really happens, on every mutating entry point, before any file is touched.

A run that silently skipped validation would be the worst possible outcome:
it would report a success it had never checked, which is precisely the shape
of failure this project has been bitten by before.

Every negative here therefore has a POSITIVE CONTROL: the identical command
in the normal environment, succeeding. "It failed with the runner hidden" is
not evidence unless the same command is shown passing with the runner there -
a typo in the argv, a bad fixture or an unrelated bug fails identically.

`harness.no_runner_env` is the hiding mechanism: HOME is redirected at an
empty directory, so search locations 2, 3 and 4 all resolve under it and
miss, and $TUTORAIL_VALIDATOR is unset so location 1 does not answer either.
bundlelib uses os.path.expanduser, which reads HOME, so this exercises the
same code path a machine without the runner installed would.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from harness import (  # noqa: E402
    LESSON,
    PROMOTE,
    RUNNER,
    Workspace,
    case,
    check,
    check_in,
    check_not_in,
    has_exactly,
    listing,
    no_runner_env,
    report,
    run,
    tree_digest,
)

import bundlelib as bl  # noqa: E402  (harness put the scripts dir on sys.path)

# The four search locations, in the order bundlelib.find_validator tries them.
# Asserting the ORDER, not just the presence, is the point: a reader who has
# the runner in ~/.agents and a stale copy in a plugin cache needs to know
# which one answered.
SEARCH_LOCATIONS = (
    "1. $TUTORAIL_VALIDATOR",
    "2. ~/.agents/skills/tutorail/scripts/validate_bundle.py",
    "3. ~/.claude/skills/tutorail/scripts/validate_bundle.py",
    "4. the newest ~/.claude/plugins/**/tutorail/**/scripts/validate_bundle.py",
)

ADDED = "23-extra-topic.md"
PROMOTED = "04-lifetimes-and-borrows.md"

STUB = """#!/usr/bin/env python3
import sys
print("stub validator: {label}")
print("target: " + sys.argv[-1])
sys.exit(0)
"""


def stub_at(path: Path, label: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(STUB.format(label=label), encoding="utf-8")
    return path


def needs_renumber(bundle: Path) -> None:
    """Swap two manifest entries so `renumber` has real work to do.

    Without this the renumber path short-circuits with "Nothing to do" and
    exits 1 BEFORE the validator search runs - which would look like a
    refusal and prove nothing at all. The swap is the positive control for
    the renumber probe itself.
    """
    path = bundle / "tutorial.yaml"
    text = path.read_text(encoding="utf-8")
    before = (
        "  - lessons/03-first-refactor.md\n  - lessons/04-richer-typed-schemas.md\n"
    )
    after = (
        "  - lessons/04-richer-typed-schemas.md\n  - lessons/03-first-refactor.md\n"
    )
    assert before in text, "fixture drifted: the manifest pair to swap is not there"
    path.write_text(text.replace(before, after), encoding="utf-8")


def install_message_is_complete(output: str, label: str) -> None:
    check_in(
        "The tutorAIl runner is not installed",
        output,
        f"{label}: the message says the runner is not installed",
    )
    check_in(
        "Install the runner plugin (skomp/tutorAIl)",
        output,
        f"{label}: the message says how to install it",
    )
    check_in(
        "Running without it is not offered",
        output,
        f"{label}: the message says skipping validation is not on offer",
    )
    for location in SEARCH_LOCATIONS:
        check_in(
            location,
            output,
            f"{label}: the message lists search location {location.split('.')[0]}",
        )
    positions = [output.find(location) for location in SEARCH_LOCATIONS]
    check(
        all(a < b for a, b in zip(positions, positions[1:])) and positions[0] >= 0,
        f"{label}: the four locations are listed IN ORDER (offsets {positions})",
    )


def mutating_commands(ws: Workspace, tag: str):
    """The three mutating entry points, each with its own fresh bundle.

    Returned as (label, argv-maker, bundle, "did it happen?" probe).
    """
    add_bundle = ws.copy("rust-automaton-db", f"{tag}-add")
    renumber_bundle = ws.copy("rust-automaton-db", f"{tag}-renumber")
    needs_renumber(renumber_bundle)
    promote_bundle = ws.copy("rust-automaton-db", f"{tag}-promote")
    instance = ws.copy("instance-with-generated", f"{tag}-instance")

    return [
        (
            "lesson.py add",
            (LESSON, "add", add_bundle, "--id", "extra-topic", "--title", "Extra topic"),
            add_bundle,
            lambda: has_exactly(add_bundle / "lessons", ADDED),
        ),
        (
            "lesson.py renumber",
            (LESSON, "renumber", renumber_bundle),
            renumber_bundle,
            lambda: has_exactly(renumber_bundle / "lessons", "03-richer-typed-schemas.md"),
        ),
        (
            "promote.py",
            (PROMOTE, instance, "lifetimes-and-borrows", promote_bundle),
            promote_bundle,
            lambda: has_exactly(promote_bundle / "lessons", PROMOTED),
        ),
    ]


def main() -> int:
    print("test_validator_discovery.py - the toolkit refuses when it cannot validate")
    print()

    with case("1  no runner: every mutating entry point refuses and writes nothing"):
        with Workspace() as ws:
            empty_home = ws.path("empty-home")
            empty_home.mkdir()
            check(
                listing(empty_home) == [],
                "the fake HOME really is empty, so all four locations must miss",
            )
            for label, argv, bundle, happened in mutating_commands(ws, "hidden"):
                before = tree_digest(bundle)
                done = run(*argv, env=no_runner_env(empty_home))
                check(
                    done.returncode != 0,
                    f"{label}: non-zero exit with the runner hidden "
                    f"(got {done.returncode})",
                )
                install_message_is_complete(done.output, label)
                check(
                    tree_digest(bundle) == before,
                    f"{label}: the bundle is BYTE-IDENTICAL after the refusal",
                )
                check(
                    not happened(),
                    f"{label}: the operation did not proceed - its output file is "
                    f"not in lessons/",
                )
            # The renumber probe is the one that could pass for the wrong
            # reason: an already-ordered bundle exits 1 with "Nothing to do"
            # before the search ever runs. Prove that is not what happened.
            renumber = [c for c in mutating_commands(ws, "guard") if c[0] == "lesson.py renumber"][0]
            done = run(*renumber[1], env=no_runner_env(empty_home))
            check_not_in(
                "Nothing to do",
                done.output,
                "lesson.py renumber: the refusal came from the validator search, "
                "not from an empty renumber plan",
            )

    with case("2  POSITIVE CONTROL: the same three commands succeed normally"):
        with Workspace() as ws:
            for label, argv, bundle, happened in mutating_commands(ws, "normal"):
                before = tree_digest(bundle)
                done = run(*argv)
                check(
                    done.returncode == 0,
                    f"{label}: exit 0 in the normal environment "
                    f"(got {done.returncode}: {done.output.strip()[-300:]})",
                )
                check_not_in(
                    "The tutorAIl runner is not installed",
                    done.output,
                    f"{label}: no install message when the runner is there",
                )
                check(
                    tree_digest(bundle) != before,
                    f"{label}: the bundle really changed, so case 1's "
                    f"byte-identical assertion is a claim about the refusal",
                )
                check(
                    happened(),
                    f"{label}: the operation's output file is in lessons/",
                )
                check_in(
                    "validator:",
                    done.output,
                    f"{label}: the run names the validator it used",
                )

    with case("3  $TUTORAIL_VALIDATOR pointing at something that is not a file"):
        with Workspace() as ws:
            bundle = ws.copy("rust-automaton-db", "bundle")
            missing = ws.path("nowhere", "validate_bundle.py")
            before = tree_digest(bundle)
            done = run(
                LESSON,
                "add",
                bundle,
                "--id",
                "extra-topic",
                "--title",
                "Extra topic",
                env={"TUTORAIL_VALIDATOR": str(missing)},
            )
            check(done.returncode != 0, f"non-zero exit (got {done.returncode})")
            check_in(
                "$TUTORAIL_VALIDATOR is set to",
                done.output,
                "the error names the environment variable",
            )
            check_in(
                str(missing),
                done.output,
                "the error quotes the bad path back",
            )
            check_in(
                "which is not a file",
                done.output,
                "the error says what is wrong with it",
            )
            check_in(
                "or unset it to search the installed plugins",
                done.output,
                "the error says how to get back to the search",
            )
            check(
                tree_digest(bundle) == before,
                "the bundle is byte-identical",
            )
            check(
                not has_exactly(bundle / "lessons", ADDED),
                "the lesson was not created",
            )
            # A directory is not a file either, and it is the likelier typo -
            # pointing the variable at the scripts/ directory rather than at
            # the script. The same refusal must fire.
            done_dir = run(
                LESSON,
                "add",
                bundle,
                "--id",
                "extra-topic",
                "--title",
                "Extra topic",
                env={"TUTORAIL_VALIDATOR": str(ws.root)},
            )
            check(
                done_dir.returncode != 0,
                f"a directory is refused too (got {done_dir.returncode})",
            )
            check_in(
                "which is not a file",
                done_dir.output,
                "the directory case gets the same actionable message",
            )
            check(
                tree_digest(bundle) == before,
                "the bundle is byte-identical after the directory case too",
            )

    with case("4  $TUTORAIL_VALIDATOR pointing at a REAL validator somewhere else"):
        with Workspace() as ws:
            # Location 1 is the only one that can point outside the two
            # installed layouts, and it is the one a checkout uses. Proving it
            # works rather than being dead code needs a real validator in a
            # place the search would otherwise never look. The validator
            # imports yamlite from its own directory, so both files move.
            installed, _ = bl.find_validator()
            elsewhere = ws.path("a-checkout", "scripts")
            elsewhere.mkdir(parents=True)
            for name in ("validate_bundle.py", "yamlite.py"):
                (elsewhere / name).write_bytes((installed.parent / name).read_bytes())
            alt = elsewhere / "validate_bundle.py"
            check(
                alt.resolve() != installed.resolve(),
                f"the copy is at a different path from the installed validator "
                f"({alt} vs {installed})",
            )
            check(
                has_exactly(elsewhere, "yamlite.py"),
                "the validator's yamlite.py travelled with it",
            )

            bundle = ws.copy("rust-automaton-db", "bundle")
            before = tree_digest(bundle)
            done = run(
                LESSON,
                "add",
                bundle,
                "--id",
                "extra-topic",
                "--title",
                "Extra topic",
                env={"TUTORAIL_VALIDATOR": str(alt)},
            )
            check(
                done.returncode == 0,
                f"the mutating operation succeeds (got {done.returncode}: "
                f"{done.output.strip()[-300:]})",
            )
            check_in(
                str(alt),
                done.output,
                "the output names the validator it actually used, by path",
            )
            check_in(
                "($TUTORAIL_VALIDATOR)",
                done.output,
                "the output says WHICH search location answered",
            )
            check_not_in(
                str(installed),
                done.output,
                "the installed validator was not used instead",
            )
            check(
                has_exactly(bundle / "lessons", ADDED),
                "the lesson really was created",
            )
            check(tree_digest(bundle) != before, "the bundle really changed")

    with case("5  search order: ~/.agents beats ~/.claude/skills beats the plugins"):
        with Workspace() as ws:
            home = ws.path("home")
            agents = stub_at(
                home / ".agents/skills/tutorail/scripts/validate_bundle.py", "agents"
            )
            claude_skills = stub_at(
                home / ".claude/skills/tutorail/scripts/validate_bundle.py",
                "claude-skills",
            )
            plugins = stub_at(
                home
                / ".claude/plugins/cache/acme/tutorail/skills/tutorail/scripts"
                / "validate_bundle.py",
                "plugins",
            )
            # All three stubs exist and exit 0, so whichever one is chosen the
            # operation completes and prints the path it used. That printed
            # path is the observation; nothing here depends on the stub's own
            # output reaching the caller.
            for path in (agents, claude_skills, plugins):
                check(
                    has_exactly(path.parent, "validate_bundle.py"),
                    f"stub in place: {path}",
                )

            def chosen(step: str) -> tuple[str, str]:
                bundle = ws.copy("rust-automaton-db", f"bundle-{step}")
                done = run(
                    LESSON,
                    "add",
                    bundle,
                    "--id",
                    f"topic-{step}",
                    "--title",
                    "Topic",
                    env={"HOME": str(home), "TUTORAIL_VALIDATOR": None},
                )
                check(
                    done.returncode == 0,
                    f"{step}: the operation completed (got {done.returncode}: "
                    f"{done.output.strip()[-300:]})",
                )
                locator = run(
                    RUNNER,
                    "--validator",
                    env={"HOME": str(home), "TUTORAIL_VALIDATOR": None},
                )
                check(
                    locator.returncode == 0,
                    f"{step}: runner.py --validator exits 0 (got {locator.returncode})",
                )
                return done.output, locator.stdout.strip()

            output, located = chosen("all-three")
            check(
                located == str(agents),
                f"with all three present, ~/.agents wins (got {located})",
            )
            check_in(
                f"validator: {agents}  (~/.agents)",
                output,
                "the mutating operation used the ~/.agents stub and labelled it",
            )

            os.remove(agents)
            output, located = chosen("no-agents")
            check(
                located == str(claude_skills),
                f"with ~/.agents gone, ~/.claude/skills wins - it beats the "
                f"plugins path (got {located})",
            )
            check_in(
                f"validator: {claude_skills}  (~/.claude/skills)",
                output,
                "the mutating operation used the ~/.claude/skills stub",
            )

            os.remove(claude_skills)
            output, located = chosen("plugins-only")
            check(
                located == str(plugins),
                f"with both skill locations gone, the plugins copy is used "
                f"(got {located})",
            )
            check_in(
                f"validator: {plugins}  (~/.claude/plugins (newest))",
                output,
                "the mutating operation used the plugins stub",
            )

            # POSITIVE CONTROL for the whole ordering probe: with every stub
            # removed the SAME calls must refuse. Otherwise the three results
            # above could be reporting something other than the search.
            os.remove(plugins)
            locator = run(
                RUNNER, "--validator", env={"HOME": str(home), "TUTORAIL_VALIDATOR": None}
            )
            check(
                locator.returncode != 0,
                f"positive control: with all three stubs removed the locator "
                f"refuses (got {locator.returncode})",
            )
            check(
                locator.stdout.strip() == "",
                f"positive control: and prints nothing on stdout "
                f"(got {locator.stdout!r})",
            )

    # ------------------------------------------------------------------
    # runner.py - the path locator the authoring skill calls
    # ------------------------------------------------------------------

    with case("6a runner.py --root prints the runner's skill directory"):
        done = run(RUNNER, "--root")
        check(done.returncode == 0, f"exit 0 (got {done.returncode})")
        printed = done.stdout.strip()
        check(printed != "", "a path was printed on stdout")
        root = Path(printed)
        check(root.is_dir(), f"the printed path is a directory ({root})")
        entries = listing(root)
        check(
            "scripts" in entries,
            f"the directory holds a 'scripts' entry (holds {entries})",
        )
        check(
            "references" in entries,
            f"the directory holds a 'references' entry (holds {entries})",
        )

    with case("6b runner.py --validator prints a file named exactly validate_bundle.py"):
        done = run(RUNNER, "--validator")
        check(done.returncode == 0, f"exit 0 (got {done.returncode})")
        printed = Path(done.stdout.strip())
        # By listing, not by .exists(): a case-insensitive filesystem would
        # resolve Validate_Bundle.py here and fail on Linux later.
        check(
            has_exactly(printed.parent, "validate_bundle.py"),
            f"{printed.parent} holds an entry named exactly validate_bundle.py",
        )
        check(
            printed.name == "validate_bundle.py",
            f"the printed name is exactly 'validate_bundle.py' (got {printed.name!r})",
        )

    with case("6c runner.py --bundle-format prints the normative contract"):
        done = run(RUNNER, "--bundle-format")
        check(done.returncode == 0, f"exit 0 (got {done.returncode})")
        printed = Path(done.stdout.strip())
        check(
            has_exactly(printed.parent, "bundle-format.md"),
            f"{printed.parent} holds an entry named exactly bundle-format.md",
        )
        check(
            printed.name == "bundle-format.md",
            f"the printed name is exactly 'bundle-format.md' (got {printed.name!r})",
        )
        text = printed.read_text(encoding="utf-8")
        # Reading the file is the difference between "a path was printed" and
        # "the contract was found". These two phrases are normative text from
        # the sections this toolkit implements; a stand-in file with the right
        # name would not carry them.
        check_in(
            "## 8. Generated lessons, and how to promote one",
            text,
            "the file carries section 8, the promotion procedure",
        )
        check_in(
            "A bundle **MUST NOT** contain a `lessons.generated/` directory",
            text,
            "the file carries section 8's normative MUST NOT",
        )
        check(
            done.stderr.strip() == "",
            f"nothing was written to stderr (got {done.stderr!r})",
        )
        # The same call by its long form must name the same file.
        long_form = run(RUNNER, "--reference", "bundle-format.md")
        check(
            long_form.returncode == 0 and long_form.stdout == done.stdout,
            "--reference bundle-format.md prints the identical path",
        )

    with case("6d runner.py --reference <missing> refuses and prints NO path"):
        done = run(RUNNER, "--reference", "no-such-reference.md")
        check(done.returncode != 0, f"non-zero exit (got {done.returncode})")
        # The failure mode this guards is a GUESSED path: a reader sent to a
        # file that is not there is worse off than a reader told it is missing.
        check(
            done.stdout.strip() == "",
            f"stdout is empty - no guessed path was printed (got {done.stdout!r})",
        )
        check_in(
            "no-such-reference.md",
            done.output,
            "the error names the file that is missing",
        )
        check_in(
            "does not exist",
            done.output,
            "the error says the file is not there",
        )
        check_in(
            "it may be an older version than this toolkit expects",
            done.output,
            "the error offers the likely cause",
        )

    with case("6e runner.py with no runner: every mode fails, and prints nothing"):
        with Workspace() as ws:
            empty_home = ws.path("empty-home")
            empty_home.mkdir()
            env = no_runner_env(empty_home)
            modes = {
                "--root": ("--root",),
                "--validator": ("--validator",),
                "--bundle-format": ("--bundle-format",),
                "--reference bundle-format.md": ("--reference", "bundle-format.md"),
                "(no arguments)": (),
            }
            for label, argv in modes.items():
                done = run(RUNNER, *argv, env=env)
                check(
                    done.returncode != 0,
                    f"{label}: non-zero exit (got {done.returncode})",
                )
                check(
                    done.stdout.strip() == "",
                    f"{label}: stdout is empty (got {done.stdout!r})",
                )
                install_message_is_complete(done.output, f"runner.py {label}")

    with case("6f POSITIVE CONTROL: every runner.py mode prints a path normally"):
        modes = {
            "--root": ("--root",),
            "--validator": ("--validator",),
            "--bundle-format": ("--bundle-format",),
            "--reference bundle-format.md": ("--reference", "bundle-format.md"),
        }
        for label, argv in modes.items():
            done = run(RUNNER, *argv)
            check(done.returncode == 0, f"{label}: exit 0 (got {done.returncode})")
            printed = done.stdout.strip()
            check(printed != "", f"{label}: a path was printed on stdout")
            check(
                Path(printed).is_absolute(),
                f"{label}: the printed path is absolute ({printed})",
            )
        # The no-argument form prints a labelled report rather than one path.
        summary = run(RUNNER)
        check(summary.returncode == 0, f"(no arguments): exit 0 (got {summary.returncode})")
        for field in ("root ", "found by ", "validator ", "format ", "references "):
            check_in(
                field,
                summary.stdout,
                f"(no arguments): the report carries a {field.strip()!r} line",
            )

    return report("test_validator_discovery.py")


if __name__ == "__main__":
    sys.exit(main())
