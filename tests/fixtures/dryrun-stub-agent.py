#!/usr/bin/env python3
"""A stand-in for `claude -p --output-format json`. Spends nothing.

`dryrun.py --agent-command <this file>` drives a whole run against it, so the
subprocess-level cases in tests/test_dryrun.py exercise the real CLI seam -
argv construction, JSON parsing, the accounting - without a token being
spent and without the real binary being reachable.

It decides which part it is playing from the opening sentence of the prompt,
because those two sentences are constants in dryrun.py for exactly this
reason. It keys off nothing else, so a change to the rest of either prompt
does not silently change what the suite measures.

Environment:

  DRYRUN_STUB_ARGV       append one JSON line per invocation to this file:
                         the argv, the cwd and the role. This is how a test
                         proves the tutor never got --resume and the learner
                         did.
  DRYRUN_STUB_TOUCH      on a learner turn, create this file (relative to the
                         cwd) with fresh bytes, so the workspace changes.
                         Absent means the learner changes nothing, which is
                         what a stall looks like.
  DRYRUN_STUB_COMPLETE_AFTER
                         emit the completion marker on tutor turn N and after.
  DRYRUN_STUB_NO_USAGE   omit the `usage` object, so a test can prove the
                         accounting records nulls rather than zeros.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

MARKER = "LESSON COMPLETE"
TUTOR_OPENING = "You are the tutor in a dry run of a tutorAIl course."
LEARNER_OPENING = "You are the learner in a dry run of a tutorAIl course."


def prompt_of(argv: list[str]) -> str:
    if "-p" in argv:
        index = argv.index("-p")
        if index + 1 < len(argv):
            return argv[index + 1]
    return ""


def counter(path: Path, role: str) -> int:
    """How many times this role has been called, from the argv log."""
    if not path.exists():
        return 1
    seen = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            if json.loads(line).get("role") == role:
                seen += 1
        except json.JSONDecodeError:
            continue
    return seen + 1


def main() -> int:
    argv = sys.argv[1:]
    prompt = prompt_of(argv)
    if prompt.startswith(TUTOR_OPENING):
        role = "tutor"
    elif prompt.startswith(LEARNER_OPENING):
        role = "learner"
    else:
        print(f"stub agent: unrecognised prompt opening: {prompt[:80]!r}", file=sys.stderr)
        return 9

    log = os.environ.get("DRYRUN_STUB_ARGV")
    nth = counter(Path(log), role) if log else 1
    if log:
        with open(log, "a", encoding="utf-8") as handle:
            handle.write(
                json.dumps({"role": role, "argv": sys.argv[1:], "cwd": os.getcwd()}) + "\n"
            )
            handle.flush()

    if role == "tutor":
        complete_after = os.environ.get("DRYRUN_STUB_COMPLETE_AFTER")
        if complete_after and nth >= int(complete_after):
            text = MARKER
        else:
            text = f"Task {nth}: create the file the lesson asks for."
    else:
        touch = os.environ.get("DRYRUN_STUB_TOUCH")
        if touch:
            target = Path(os.getcwd()) / touch
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"learner turn {nth} at {time.time_ns()}\n", encoding="utf-8")
            text = f"I created {touch}."
        else:
            text = "I read the task and could not see what to change."

    payload = {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "duration_ms": 4200 + nth,
        "num_turns": 1,
        "result": text,
        "session_id": f"stub-{role}-session",
        "total_cost_usd": 0.0,
    }
    if not os.environ.get("DRYRUN_STUB_NO_USAGE"):
        payload["usage"] = {
            "input_tokens": 1000 + nth,
            "output_tokens": 100 + nth,
            "cache_read_input_tokens": 10,
            "cache_creation_input_tokens": 5,
        }
    print(json.dumps(payload))
    return 0


if __name__ == "__main__":
    sys.exit(main())
