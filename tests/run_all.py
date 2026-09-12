#!/usr/bin/env python3
"""Run every tutorail-authoring test suite.

    python3 tests/run_all.py            run them all
    python3 tests/run_all.py renumber   run only suites whose name matches

Each suite is also a plain runner on its own - `python3 tests/test_x.py` -
because pytest is not installed and adding a dependency to run the tests of a
stdlib-only toolkit would be its own kind of joke.

Exit code 0 only when every suite exits 0.

PIN THE VALIDATOR WHEN A RESULT HAS TO BE ATTRIBUTABLE.

Every suite runs the tutorAIl runner's `validate_bundle.py`, found by the
same search the toolkit uses - and on a developer machine that search leads,
through `~/.agents/skills/tutorail`, to a CHECKOUT OF THE RUNNER THAT SOMEONE
MAY BE EDITING. That happened during this suite's own development: the runner
gained an `optional_lessons` format extension while these tests were running,
and for a few minutes its validator raised

    TypeError: check_lesson_list() missing 1 required positional argument

mid-edit. Three suites went red for a reason that had nothing to do with the
code under test, and a reader who had not looked would have believed them.

So when a run has to mean something - a verification before finishing, a
result quoted to someone - pin it to a validator that is not moving:

    git -C <tutorAIl> show HEAD:skills/tutorail/scripts/validate_bundle.py > /tmp/v/validate_bundle.py
    git -C <tutorAIl> show HEAD:skills/tutorail/scripts/yamlite.py         > /tmp/v/yamlite.py
    TUTORAIL_VALIDATOR=/tmp/v/validate_bundle.py python3 tests/run_all.py

`yamlite.py` has to come too: the validator imports it from its own
directory. Every suite prints which validator it used, so the pin is visible
in the output rather than assumed.

Two suites are ABOUT the search itself and must see a clean environment:
test_validator_discovery.py sets `$TUTORAIL_VALIDATOR` per case to prove
search location 1 works, and test_yamlite_drift.py resolves the runner's own
`yamlite.py` through `find_runner_root()`. This runner therefore unsets the
pin for exactly those two and says so, rather than letting an ambient pin
quietly decide what they measure.

ENVIRONMENT NOISE, so a reader does not mistake it for a failure: this
machine's pyenv build of CPython 3.11.9 prints

    ERROR:root:code for hash blake2s was not found.

on `import hashlib`, followed by a traceback. It comes from the interpreter's
own hashlib import, not from anything here, and sha256 - which the suites
actually use - works. It appears on stderr before any suite output.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Suites that measure the validator SEARCH rather than using its result. An
# ambient $TUTORAIL_VALIDATOR answers search location 1 for every case in
# them, so they would report on the pin instead of on the search.
NEEDS_CLEAN_SEARCH = {"test_validator_discovery.py", "test_yamlite_drift.py"}


def main(argv: list[str]) -> int:
    pattern = argv[1] if len(argv) > 1 else ""
    suites = sorted(HERE.glob("test_*.py"))
    if pattern:
        suites = [s for s in suites if pattern in s.name]
    if not suites:
        print(f"no suite matches {pattern!r}", file=sys.stderr)
        return 2

    pinned = os.environ.get("TUTORAIL_VALIDATOR")
    results: list[tuple[str, int]] = []
    for suite in suites:
        env = dict(os.environ)
        print("=" * 72)
        print(f"== {suite.name}")
        if suite.name in NEEDS_CLEAN_SEARCH and pinned:
            env.pop("TUTORAIL_VALIDATOR", None)
            print("== $TUTORAIL_VALIDATOR unset: this suite measures the search itself")
        print("=" * 72)
        done = subprocess.run([sys.executable, str(suite)], env=env)
        results.append((suite.name, done.returncode))
        print()

    print("=" * 72)
    failed = [name for name, code in results if code != 0]
    for name, code in results:
        print(f"  {'ok  ' if code == 0 else 'FAIL'}  {name}  (exit {code})")
    print("=" * 72)
    if failed:
        print(f"{len(failed)} of {len(results)} suite(s) failed: {', '.join(failed)}")
        return 1
    print(f"all {len(results)} suite(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
