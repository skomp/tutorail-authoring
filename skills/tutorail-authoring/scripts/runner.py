#!/usr/bin/env python3
"""Locate the installed tutorAIl runner, so nothing has to guess at its path.

Usage:
    runner.py                         print every resolved path, labelled
    runner.py --root                  the runner's skill directory
    runner.py --validator             its validate_bundle.py
    runner.py --reference <name>      a file in its references/ directory
    runner.py --bundle-format         shorthand for --reference bundle-format.md

This project depends on the runner and says so (design section 2): the bundle
format contract and the validator both live in `skomp/tutorAIl`, and are not
duplicated here. That leaves the authoring skill needing to READ files whose
path it cannot know - the runner may be a Codex symlink, a Claude Code plugin
cache, or a checkout pointed at by an environment variable.

The search order is the one the mutating scripts already use for the
validator, and it is implemented once, in bundlelib.find_validator:

    1. $TUTORAIL_VALIDATOR                (its skill root is two levels up)
    2. ~/.agents/skills/tutorail/scripts/validate_bundle.py
    3. ~/.claude/skills/tutorail/scripts/validate_bundle.py
    4. the newest ~/.claude/plugins/**/tutorail/**/scripts/validate_bundle.py

A path is printed only when it exists. When the runner cannot be found, this
prints the install message on stderr and exits 2 - it never prints a guess,
because a guessed path sends a reader to a file that is not there, or to
nothing at all, with no sign that anything went wrong.

Exit codes:
    0  every requested path resolved and was printed on stdout
    2  the runner is not installed, or the requested file is not in it
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import bundlelib as bl
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import bundlelib as bl

BUNDLE_FORMAT = "bundle-format.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="runner.py",
        description="Print paths inside the installed tutorAIl runner.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--root", action="store_true", help="print the runner's skill directory"
    )
    group.add_argument(
        "--validator", action="store_true", help="print its validate_bundle.py"
    )
    group.add_argument(
        "--reference", metavar="NAME", help="print references/NAME inside the runner"
    )
    group.add_argument(
        "--bundle-format",
        action="store_true",
        help=f"shorthand for --reference {BUNDLE_FORMAT}",
    )
    args = parser.parse_args(argv)

    if args.root:
        root, _ = bl.find_runner_root()
        print(root)
        return 0
    if args.validator:
        validator, _ = bl.find_validator()
        print(validator)
        return 0
    name = BUNDLE_FORMAT if args.bundle_format else args.reference
    if name:
        path, _ = bl.find_runner_reference(name)
        print(path)
        return 0

    root, how = bl.find_runner_root()
    validator, _ = bl.find_validator()
    print(f"root       {root}")
    print(f"found by   {how}")
    print(f"validator  {validator}")
    try:
        reference, _ = bl.find_runner_reference(BUNDLE_FORMAT)
        print(f"format     {reference}")
    except bl.ToolError as exc:
        print(f"format     NOT FOUND - {str(exc).splitlines()[0]}", file=sys.stderr)
        return 2
    references = bl.list_dir(root / "references")
    if references:
        print(f"references {' '.join(references)}")
    return 0


if __name__ == "__main__":
    sys.exit(bl.run_main(main))
