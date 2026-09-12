#!/usr/bin/env python3
"""dryrun.py - walk a course one task at a time, with an agent playing the learner.

Usage:
    dryrun.py <instance> [--from <lesson>] [--to <lesson>] [options]
    dryrun.py <instance> --plan          # print the plan, call no agent, spend nothing

An instance is a LEARNER WORKSPACE: the materialized course sits in
`<instance>/tutorial/` and the learner's own files sit beside it. This script
drives two headless sessions over that workspace - a TUTOR that reads the
course and writes exactly one task, and a LEARNER that reads only the task and
the workspace - and records what each turn cost.

THE PROPERTY THE WHOLE THING RESTS ON
=====================================

An agent that has read the lesson cannot play the learner. It has read the
answer, so every finding from its run is worthless. Therefore the isolation
here is STRUCTURAL and not an instruction:

  * The tutor runs with its cwd set to the instance, where `tutorial/` is.
  * The learner runs with its cwd set to a MIRROR that never contains
    `tutorial/` and never contains a lesson file.
  * `assert_learner_isolated()` runs before EVERY learner turn and aborts the
    whole run when it finds anything. Not a warning, not a note in the log -
    an abort, because a run that continued would produce numbers that look
    exactly like honest ones.

"Do not read ahead" in a prompt is unverifiable, and an unverifiable guard is
the false oracle this project keeps being bitten by. The guard here is watched
firing in tests/test_dryrun.py, against a mirror with a lesson planted in it
under an innocent name, and it has a positive control beside it: an ordinary
learner workspace, which must come back clean.

THE STALL DETECTOR REPORTS AND NEVER DIAGNOSES
==============================================

A stall is N consecutive learner turns that change no byte of the workspace
and advance no validator. This script localises one - which lesson, which
turn, what the last task was - and then stops. It does not say why, and it
must not: a stall cannot distinguish an unsatisfiable completion condition
from a learner having a bad run. `STALL_DISCLAIMER` says so in every stall
report, and `verdict_language()` is the probe that keeps the rest of the
report free of verdict wording. The ruling belongs to whoever reads the log.

THE PROCESS CALL IS BEHIND ONE SEAM
===================================

`CliAgent` is the only place in this module that starts an agent process.
Everything else takes an `Agent` and calls `.run()`. That is what lets the
test suite substitute a stub and spend nothing, and it is why the suite can
assert - with a tripwire `claude` on `$PATH` - that a stubbed run never
reaches the real binary.

ACCOUNTING IS FOR A DECISION, NOT FOR A LOG
===========================================

The run log exists so someone can later decide how often this harness is
worth running. So each turn records what that decision needs: both token
directions, both cache directions, the reported cost, the reported duration
AND the wall time, the session id, the role, the lesson, the turn number,
whether the session resumed, and what the turn changed. Where the agent
reports no usage the fields are `null` and `usage_present` is false. They are
never zero: a zero is a number someone would add up.

KNOWN GAPS, PHASE 1
===================

  * A file the learner DELETES in the mirror is not deleted in the instance.
    Creations and edits sync both ways; deletions do not.
  * Lesson completion is signalled by `LESSON_COMPLETE_MARKER` in the tutor's
    text. That is a convention this harness asks for, not something the
    runner skill emits today.
  * `kind: manual` and `kind: git-diff` validators cannot be probed, so they
    can never contribute progress. Each turn logs which validators were
    probed, so a lesson whose validators are all unprobeable is visible in
    the log rather than silently indistinguishable from a stalled one.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path

# dryrun.py lives in the course-quality skill; bundlelib.py belongs to
# tutorail-authoring. Reach across to it the way audit.py already does,
# rather than duplicating manifest parsing and lesson discovery here.
_SCRIPTS_DIR = Path(__file__).resolve().parent
_AUTHORING_SCRIPTS = _SCRIPTS_DIR.parents[1] / "tutorail-authoring" / "scripts"

try:
    import bundlelib as bl
except ImportError:  # pragma: no cover - only when sys.path lacks that dir
    sys.path.insert(0, str(_AUTHORING_SCRIPTS))
    import bundlelib as bl


SCHEMA = 1

INSTANCE_SUBDIR = "tutorial"

LESSON_COMPLETE_MARKER = "LESSON COMPLETE"

STALL_DISCLAIMER = (
    "A stall cannot distinguish an unsatisfiable completion condition from a "
    "learner having a bad run. This harness localises a stall and does not "
    "rule on one. The ruling stays with whoever reads this log."
)


class DryRunError(Exception):
    """A refusal with a message worth printing."""


class AgentError(DryRunError):
    """The agent process ran but its output could not be accounted for."""


class IsolationBreach(DryRunError):
    """The learner's mirror held course material. The run aborts."""

    def __init__(self, mirror: Path, findings: "list[Finding]") -> None:
        self.mirror = mirror
        self.findings = findings
        lines = [
            f"{mirror}: the learner's mirror holds course material, so this "
            f"run is aborted before the learner turn.",
            "",
            "A learner that can read the lesson has read the answer, and every "
            "finding from such a run is worthless. Nothing is salvageable by "
            "continuing, so nothing continues.",
            "",
        ]
        for finding in findings:
            lines.append(f"  {finding.rel}: {finding.reason}")
        super().__init__("\n".join(lines))


# --------------------------------------------------------------------------
# The workspace: digest and sync
# --------------------------------------------------------------------------

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", "target"}


def _walk_files(root: Path):
    """Every file under `root`, relative-path sorted, skipping SKIP_DIRS."""
    out: list[tuple[str, Path]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        here = Path(dirpath)
        for name in sorted(filenames):
            path = here / name
            out.append((path.relative_to(root).as_posix(), path))
    out.sort(key=lambda pair: pair[0])
    return out


def tree_digest(root: Path) -> str:
    """A hash over every relative path and every byte under `root`.

    This is what "the learner changed nothing" means. A weaker check - a file
    count, an mtime - would call an edit that rewrote a file in place no
    change at all, and the stall detector would then count a working learner
    as a stalled one.
    """
    digest = hashlib.sha256()
    if not root.is_dir():
        return digest.hexdigest()
    for rel, path in _walk_files(root):
        digest.update(b"\0path\0")
        digest.update(rel.encode("utf-8"))
        if path.is_symlink():
            digest.update(b"\0link\0")
            digest.update(os.readlink(path).encode("utf-8"))
            continue
        digest.update(b"\0body\0")
        try:
            digest.update(path.read_bytes())
        except OSError as exc:  # pragma: no cover - unreadable file
            digest.update(f"\0unreadable{exc.errno}\0".encode("utf-8"))
    return digest.hexdigest()


def _copy_file(source: Path, target: Path) -> bool:
    """Copy when the bytes differ. True when anything was written."""
    if target.exists() and not target.is_symlink():
        try:
            if target.read_bytes() == source.read_bytes():
                return False
        except OSError:
            pass
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return True


HARNESS_ARTEFACTS = ("dryrun-*.jsonl",)


def is_harness_artefact(rel: str) -> bool:
    """True for a file this harness writes into the instance.

    The run log lands in the instance by default, and it carries every task
    the tutor has written so far. Copying it into the mirror would hand the
    learner a transcript of the lesson one step at a time, which is a smaller
    version of exactly the leak this whole design exists to prevent.
    """
    name = rel.split("/")[-1]
    return any(fnmatch(name, pattern) for pattern in HARNESS_ARTEFACTS)


def sync_to_mirror(instance: Path, mirror: Path, exclude: "frozenset[str]" = frozenset()) -> list[str]:
    """Put the learner-visible part of the instance into the mirror.

    Course material is NEVER copied: `is_course_material()` decides, and the
    same predicate is what `check_isolation()` looks for afterwards. Files the
    learner made in the mirror are left alone - they are the in-flight work.
    """
    mirror.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for rel, path in _walk_files(instance):
        if is_course_material(rel) or is_harness_artefact(rel) or rel in exclude:
            continue
        if _copy_file(path, mirror / rel):
            written.append(rel)
    return written


def sync_from_mirror(mirror: Path, instance: Path) -> list[str]:
    """Put the learner's work back into the instance, so the tutor sees it.

    Refuses to write anything the isolation predicate calls course material.
    The guard has already run by this point, so such a path cannot be there;
    the refusal is here so that a future change to the guard cannot turn this
    function into the thing that plants a lesson in the instance's own
    `tutorial/`.
    """
    written: list[str] = []
    for rel, path in _walk_files(mirror):
        if is_course_material(rel):
            raise IsolationBreach(mirror, [Finding(rel, "course material in the mirror")])
        if _copy_file(path, instance / rel):
            written.append(rel)
    return written


# --------------------------------------------------------------------------
# The isolation guard
#
# Two independent signals, because a name check alone is defeated by a rename
# and a content check alone is defeated by an empty `tutorial/` directory that
# a later turn fills in.
# --------------------------------------------------------------------------

COURSE_DIR_NAMES = {"tutorial", "lessons", "lessons.generated"}

COURSE_FILE_NAMES = {
    "tutorial.yaml",
    "COURSE.md",
    "DESIGN.md",
    "STATE.md",
    "STATE.template.md",
    "LESSON.md",
}

# Which files the content sniff opens. A planted lesson is a text file; this
# is a guard against an accident and against the obvious rename, and it says
# so rather than claiming to stop someone who is trying.
SNIFF_SUFFIXES = {".md", ".markdown", ".mdx", ".txt", ".text", ""}
SNIFF_MAX_BYTES = 1 << 20

_LESSON_BODY_HEADINGS = (
    re.compile(r"(?mi)^#{1,6}\s+Learning objectives\s*$"),
    re.compile(r"(?mi)^#{1,6}\s+Suggested progression\s*$"),
    re.compile(r"(?mi)^#{1,6}\s+Completion condition\s*$"),
    re.compile(r"(?mi)^#{1,6}\s+Concepts to teach\s*$"),
)


@dataclass(frozen=True)
class Finding:
    rel: str
    reason: str


def is_course_material(rel: str) -> bool:
    """True for a path that belongs to the course and not to the learner.

    `rel` is a POSIX relative path. This is the single predicate that both
    the sync and the guard use, so the two can never disagree about what a
    lesson is.
    """
    parts = rel.split("/")
    # Only the DIRECTORY segments are checked against COURSE_DIR_NAMES. A
    # learner file that happens to be named `tutorial` is the learner's.
    if any(part in COURSE_DIR_NAMES for part in parts[:-1]):
        return True
    return parts[-1] in COURSE_FILE_NAMES


def looks_like_a_lesson(text: str) -> str | None:
    """Why this text reads as a lesson, or None.

    Two signals. A frontmatter block carrying a lesson's own keys, and a body
    carrying the headings the bundle format gives a lesson. Either is enough:
    a lesson stripped of its frontmatter is still a lesson, and a frontmatter
    block with the body cut off still tells the learner which validators the
    tutor is about to ask for.
    """
    front, body = bl.split_frontmatter(text)
    if front is not None:
        try:
            parsed = bl.load_yaml(front, "frontmatter")
        except Exception:  # a non-parsing block is not evidence either way
            parsed = None
        if isinstance(parsed, dict):
            keys = {str(k) for k in parsed}
            marks = keys & {"design_refs", "validators", "learning_objectives"}
            if "id" in keys and marks:
                return f"lesson frontmatter (id + {', '.join(sorted(marks))})"
    hits = [pattern for pattern in _LESSON_BODY_HEADINGS if pattern.search(body)]
    if len(hits) >= 2:
        return "lesson body headings"
    return None


def check_isolation(mirror: Path) -> list[Finding]:
    """Everything in `mirror` that a learner must not be able to read.

    Empty means clean. This function is the guard; `assert_learner_isolated`
    is the guard with teeth.
    """
    findings: list[Finding] = []
    if not mirror.exists():
        return findings
    for dirpath, dirnames, _filenames in os.walk(mirror):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        here = Path(dirpath)
        for name in list(dirnames):
            if name in COURSE_DIR_NAMES:
                rel = (here / name).relative_to(mirror).as_posix()
                findings.append(Finding(rel + "/", f"a directory named {name!r}"))
    for rel, path in _walk_files(mirror):
        name = rel.split("/")[-1]
        if is_course_material(rel):
            findings.append(Finding(rel, "a course path by name"))
            continue
        if path.suffix.lower() not in SNIFF_SUFFIXES:
            continue
        try:
            if path.stat().st_size > SNIFF_MAX_BYTES:
                continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        reason = looks_like_a_lesson(text)
        if reason is not None:
            findings.append(Finding(rel, reason))
    findings.sort(key=lambda f: (f.rel, f.reason))
    return findings


def assert_learner_isolated(mirror: Path) -> None:
    """Raise IsolationBreach when the mirror holds any course material."""
    findings = check_isolation(mirror)
    if findings:
        raise IsolationBreach(mirror, findings)


# --------------------------------------------------------------------------
# The agent seam
# --------------------------------------------------------------------------


@dataclass
class AgentResult:
    role: str
    text: str
    session_id: str | None
    input_tokens: int | None
    output_tokens: int | None
    cache_read_input_tokens: int | None
    cache_creation_input_tokens: int | None
    total_cost_usd: float | None
    duration_ms: int | None
    num_turns: int | None
    is_error: bool
    usage_present: bool
    wall_ms: int
    argv: list[str]
    raw: dict = field(default_factory=dict)


def _int_or_none(value) -> int | None:
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _float_or_none(value) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def parse_agent_json(stdout: str, *, role: str, argv: list[str], wall_ms: int) -> AgentResult:
    """Turn one `--output-format json` payload into an AgentResult.

    Refuses rather than guesses. A payload this cannot parse raises, because
    the alternative - defaulting the usage fields to zero - would put a
    number into the run log that someone would later add up. Missing usage in
    a payload that DID parse is recorded as null with `usage_present` false,
    which is a different fact and is kept as one.
    """
    stripped = stdout.strip()
    if not stripped:
        raise AgentError(f"{role}: the agent printed nothing on stdout.")
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise AgentError(
            f"{role}: the agent's stdout is not the JSON that "
            f"--output-format json promises: {exc}\n---\n{stripped[:2000]}"
        ) from exc
    if not isinstance(payload, dict):
        raise AgentError(
            f"{role}: --output-format json returned a "
            f"{type(payload).__name__}, not an object."
        )
    usage = payload.get("usage")
    usage_present = isinstance(usage, dict)
    usage = usage if usage_present else {}
    text = payload.get("result")
    if not isinstance(text, str):
        text = payload.get("text") if isinstance(payload.get("text"), str) else ""
    return AgentResult(
        role=role,
        text=text,
        session_id=payload.get("session_id") if isinstance(payload.get("session_id"), str) else None,
        input_tokens=_int_or_none(usage.get("input_tokens")),
        output_tokens=_int_or_none(usage.get("output_tokens")),
        cache_read_input_tokens=_int_or_none(usage.get("cache_read_input_tokens")),
        cache_creation_input_tokens=_int_or_none(usage.get("cache_creation_input_tokens")),
        total_cost_usd=_float_or_none(payload.get("total_cost_usd")),
        duration_ms=_int_or_none(payload.get("duration_ms")),
        num_turns=_int_or_none(payload.get("num_turns")),
        is_error=bool(payload.get("is_error")),
        usage_present=usage_present,
        wall_ms=wall_ms,
        argv=list(argv),
        raw=payload,
    )


class Agent:
    """The seam. Everything in this module talks to one of these."""

    name = "agent"

    def run(self, prompt: str, *, cwd: Path, role: str, resume: str | None = None) -> AgentResult:
        raise NotImplementedError


class CliAgent(Agent):
    """THE ONLY PLACE THIS MODULE STARTS AN AGENT PROCESS.

    Keeping it to one class is what makes the suite's "this run spent
    nothing" assertion checkable: substitute another Agent and no process can
    start, no matter what the rest of the driver does.
    """

    def __init__(
        self,
        command: str = "claude",
        extra_args: "tuple[str, ...] | list[str]" = (),
        timeout: int = 1800,
    ) -> None:
        self.command = command
        self.extra_args = list(extra_args)
        self.timeout = timeout
        self.name = command

    def build_argv(self, prompt: str, resume: str | None) -> list[str]:
        argv = [self.command, "-p", prompt, "--output-format", "json"]
        if resume:
            argv += ["--resume", resume]
        argv += self.extra_args
        return argv

    def run(self, prompt: str, *, cwd: Path, role: str, resume: str | None = None) -> AgentResult:
        argv = self.build_argv(prompt, resume)
        started = time.monotonic()
        try:
            done = subprocess.run(
                argv, cwd=str(cwd), capture_output=True, text=True, timeout=self.timeout
            )
        except FileNotFoundError as exc:
            raise AgentError(
                f"{role}: {self.command!r} is not on $PATH ({exc}). Install the "
                f"Claude Code CLI, or pass --agent-command."
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise AgentError(f"{role}: {self.command!r} did not return within {self.timeout}s.") from exc
        wall_ms = int((time.monotonic() - started) * 1000)
        if done.returncode != 0 and not done.stdout.strip():
            raise AgentError(
                f"{role}: {self.command!r} exited {done.returncode} and printed "
                f"no JSON.\n---\n{done.stderr[-2000:]}"
            )
        return parse_agent_json(done.stdout, role=role, argv=argv, wall_ms=wall_ms)


# --------------------------------------------------------------------------
# The validator probe
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ValidatorState:
    passing: frozenset = frozenset()
    probed: frozenset = frozenset()
    unprobeable: frozenset = frozenset()

    def advanced_over(self, previous: "ValidatorState") -> bool:
        """True when a validator passes now that did not pass before."""
        return bool(self.passing - previous.passing)


class ValidatorProbe:
    """The second seam. Substituted in tests so no toolchain is needed."""

    def state(self, lesson: "LessonRef") -> ValidatorState:
        raise NotImplementedError


class CommandValidators(ValidatorProbe):
    """Run the lesson's declared validators in the instance directory.

    `kind: manual` and `kind: git-diff` are reported as UNPROBEABLE rather
    than as failing. That distinction is the whole point: a lesson whose only
    validator is manual can never show progress, and a probe that returned an
    empty `passing` set for it would be indistinguishable from a probe
    watching a learner who is genuinely stuck. The turn record carries
    `validators_probed` so the difference is visible in the log.
    """

    def __init__(self, instance: Path, manifest: dict, timeout: int = 600) -> None:
        self.instance = instance
        raw = manifest.get("validators")
        self.declared = raw if isinstance(raw, dict) else {}
        self.timeout = timeout

    def state(self, lesson: "LessonRef") -> ValidatorState:
        passing: set = set()
        probed: set = set()
        unprobeable: set = set()
        for name in lesson.validators:
            spec = self.declared.get(name)
            if not isinstance(spec, dict):
                unprobeable.add(name)
                continue
            kind = spec.get("kind")
            if kind == "command":
                command = spec.get("command")
                if not isinstance(command, list) or not command:
                    unprobeable.add(name)
                    continue
                probed.add(name)
                if self._exit_zero([str(part) for part in command]):
                    passing.add(name)
            elif kind == "file-exists":
                rel = spec.get("path")
                if not isinstance(rel, str):
                    unprobeable.add(name)
                    continue
                probed.add(name)
                if (self.instance / rel).exists():
                    passing.add(name)
            else:
                unprobeable.add(name)
        return ValidatorState(frozenset(passing), frozenset(probed), frozenset(unprobeable))

    def _exit_zero(self, command: list[str]) -> bool:
        try:
            done = subprocess.run(
                command,
                cwd=str(self.instance),
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
        except (OSError, subprocess.SubprocessError):
            return False
        return done.returncode == 0


# --------------------------------------------------------------------------
# The stall detector. It localises and never diagnoses.
# --------------------------------------------------------------------------

VERDICT_WORDS = (
    r"broken",
    r"unsatisfiable",
    r"impossible",
    r"defect",
    r"\bbugs?\b",
    r"at fault",
    r"blame",
    r"root cause",
    r"caused by",
    r"fails because",
    r"is wrong",
    r"cannot be satisfied",
    r"unteachable",
)

_VERDICT_RE = re.compile("|".join(VERDICT_WORDS), re.IGNORECASE)


def verdict_language(text: str, *, allow: str = STALL_DISCLAIMER) -> list[str]:
    """Verdict words in `text`, ignoring those inside `allow`.

    The disclaimer has to name the two possibilities it refuses to choose
    between, so it contains the word "unsatisfiable" itself. Removing it
    before scanning is what lets this probe be strict everywhere else. Any
    non-empty return is a stall report that has started ruling on something.
    """
    scanned = text.replace(allow, " ") if allow else text
    return [match.group(0) for match in _VERDICT_RE.finditer(scanned)]


@dataclass
class StallObservation:
    turn: int
    lesson: str
    workspace_changed: bool
    validators_advanced: bool
    task: str = ""


@dataclass
class StallReport:
    lesson: str
    first_quiet_turn: int
    last_turn: int
    quiet_turns: int
    threshold: int
    last_task: str

    def render(self) -> str:
        task = self.last_task.strip() or "(the tutor's task text was empty)"
        indented = "\n".join(f"    {line}" for line in task.splitlines()[:40])
        return "\n".join(
            [
                "STALL REPORT - a localisation, not a finding",
                f"  lesson:             {self.lesson}",
                f"  first quiet turn:   {self.first_quiet_turn}",
                f"  last turn observed: {self.last_turn}",
                f"  quiet turns:        {self.quiet_turns} (threshold {self.threshold})",
                "  quiet means: no byte of the learner's workspace changed and no",
                "  validator that was failing started passing.",
                "",
                "  the last task the tutor gave the learner:",
                indented,
                "",
                f"  {STALL_DISCLAIMER}",
            ]
        )

    def to_json(self) -> dict:
        return {
            "kind": "stall",
            "lesson": self.lesson,
            "first_quiet_turn": self.first_quiet_turn,
            "last_turn": self.last_turn,
            "quiet_turns": self.quiet_turns,
            "threshold": self.threshold,
            "last_task": self.last_task,
            "disclaimer": STALL_DISCLAIMER,
        }


class StallDetector:
    """Counts consecutive quiet learner turns. Reports. Never rules."""

    def __init__(self, threshold: int) -> None:
        if threshold < 1:
            raise DryRunError("--stall-after must be 1 or more.")
        self.threshold = threshold
        self.count = 0
        self._first_quiet: StallObservation | None = None
        self._last: StallObservation | None = None

    def observe(self, observation: StallObservation) -> None:
        self._last = observation
        if observation.workspace_changed or observation.validators_advanced:
            self.count = 0
            self._first_quiet = None
            return
        self.count += 1
        if self._first_quiet is None:
            self._first_quiet = observation

    @property
    def stalled(self) -> bool:
        return self.count >= self.threshold

    def report(self) -> StallReport | None:
        if not self.stalled or self._first_quiet is None or self._last is None:
            return None
        return StallReport(
            lesson=self._last.lesson,
            first_quiet_turn=self._first_quiet.turn,
            last_turn=self._last.turn,
            quiet_turns=self.count,
            threshold=self.threshold,
            last_task=self._last.task,
        )

    def reset(self) -> None:
        self.count = 0
        self._first_quiet = None
        self._last = None


# --------------------------------------------------------------------------
# Accounting
# --------------------------------------------------------------------------


class RunLog:
    """One JSON object per line, appended and flushed as it happens.

    Flushed per line on purpose: a run that is killed half way through still
    leaves every turn it paid for on disk, and the cost of a run nobody can
    account for is the one number this log exists to prevent.
    """

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lines = 0

    def append(self, record: dict) -> dict:
        record = dict(record)
        record.setdefault("schema", SCHEMA)
        record.setdefault("at", datetime.now(timezone.utc).isoformat(timespec="seconds"))
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        self.lines += 1
        return record


def turn_record(
    *,
    run_id: str,
    course: str,
    turn: int,
    role: str,
    lesson: str,
    result: AgentResult,
    resumed: bool,
    workspace_changed: bool | None = None,
    validators: ValidatorState | None = None,
    quiet_turns: int | None = None,
) -> dict:
    """One turn, in the shape a later decision needs.

    The decision this feeds is "how often is this harness worth running", so
    both token directions, both cache directions, the reported cost, the
    reported duration and the wall clock are all here - and so is what the
    turn bought, which is the workspace change and the validator movement.
    """
    record = {
        "kind": "turn",
        "run_id": run_id,
        "course": course,
        "turn": turn,
        "role": role,
        "lesson": lesson,
        "session_id": result.session_id,
        "resumed": resumed,
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "cache_read_input_tokens": result.cache_read_input_tokens,
        "cache_creation_input_tokens": result.cache_creation_input_tokens,
        "usage_present": result.usage_present,
        "total_cost_usd": result.total_cost_usd,
        "duration_ms": result.duration_ms,
        "wall_ms": result.wall_ms,
        "num_turns": result.num_turns,
        "is_error": result.is_error,
        "text_chars": len(result.text),
    }
    if workspace_changed is not None:
        record["workspace_changed"] = workspace_changed
    if validators is not None:
        record["validators_passing"] = sorted(validators.passing)
        record["validators_probed"] = sorted(validators.probed)
        record["validators_unprobeable"] = sorted(validators.unprobeable)
    if quiet_turns is not None:
        record["quiet_turns"] = quiet_turns
    return record


# --------------------------------------------------------------------------
# Lessons and the range
# --------------------------------------------------------------------------


@dataclass
class LessonRef:
    rel: str
    slug: str
    path: Path
    lesson_id: str
    title: str
    validators: list = field(default_factory=list)


def read_lessons(instance_dir: Path) -> list[LessonRef]:
    """The instance's lessons, in manifest order."""
    bundle = bl.load_bundle(instance_dir)
    refs: list[LessonRef] = []
    for lesson in bundle.ordered:
        front_text = bl.read_text(lesson.path) or ""
        front, _body = bl.split_frontmatter(front_text)
        parsed: dict = {}
        if front is not None:
            try:
                candidate = bl.load_yaml(front, lesson.rel)
                if isinstance(candidate, dict):
                    parsed = candidate
            except Exception:
                parsed = {}
        raw_validators = parsed.get("validators")
        validators = (
            [str(v) for v in raw_validators] if isinstance(raw_validators, list) else []
        )
        refs.append(
            LessonRef(
                rel=lesson.rel,
                slug=lesson.slug,
                path=lesson.path,
                lesson_id=str(parsed.get("id", lesson.slug)),
                title=str(parsed.get("title", lesson.slug)),
                validators=validators,
            )
        )
    return refs


def active_lesson(instance_dir: Path) -> str | None:
    """`active_lesson:` from STATE.md, or None when there is no state yet."""
    text = bl.read_text(instance_dir / "STATE.md")
    if text is None:
        return None
    front, _body = bl.split_frontmatter(text)
    if front is None:
        return None
    try:
        parsed = bl.load_yaml(front, "STATE.md")
    except Exception:
        return None
    if isinstance(parsed, dict):
        value = parsed.get("active_lesson")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def resolve_lesson(lessons: list[LessonRef], token: str) -> LessonRef:
    """Find one lesson by rel path, filename, slug or id. Ambiguity refuses."""
    token = token.strip()
    exact = [l for l in lessons if l.rel == token]
    if exact:
        return exact[0]
    hits = [
        l
        for l in lessons
        if token in (l.slug, l.lesson_id, l.path.name, l.rel, l.rel.rsplit("/", 1)[-1])
    ]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        known = "\n".join(f"  {l.rel}" for l in lessons)
        raise DryRunError(f"{token!r}: no lesson matches. The lessons are:\n{known}")
    names = ", ".join(l.rel for l in hits)
    raise DryRunError(f"{token!r}: matches more than one lesson ({names}). Use the full path.")


def select_lessons(
    lessons: list[LessonRef], frm: str | None, to: str | None, default_rel: str | None
) -> list[LessonRef]:
    """The inclusive range to walk. ONE LESSON BY DEFAULT.

    Decision 2 of the issue: measure the cost of one lesson before running a
    whole course. So a bare invocation walks exactly one, and running more is
    something the caller asks for in writing.
    """
    if not lessons:
        raise DryRunError("this instance has no lessons.")
    if frm is None and to is None:
        if default_rel:
            try:
                return [resolve_lesson(lessons, default_rel)]
            except DryRunError:
                pass
        return [lessons[0]]
    start = resolve_lesson(lessons, frm) if frm else (resolve_lesson(lessons, to) if to else lessons[0])
    end = resolve_lesson(lessons, to) if to else start
    first = lessons.index(start)
    last = lessons.index(end)
    if last < first:
        raise DryRunError(
            f"--to {end.rel} comes before --from {start.rel} in the manifest order."
        )
    return lessons[first : last + 1]


# --------------------------------------------------------------------------
# Prompts
#
# The opening sentences are constants because the stub agent in the test
# fixtures keys off them to decide which canned payload to print. Changing
# one changes what the suite exercises.
# --------------------------------------------------------------------------

TUTOR_PROMPT_OPENING = "You are the tutor in a dry run of a tutorAIl course."
LEARNER_PROMPT_OPENING = "You are the learner in a dry run of a tutorAIl course."

TUTOR_PROMPT = """{opening}

Your working directory is the learner's workspace. The course is materialized
in `{subdir}/`.

Read `{subdir}/STATE.md` and the one lesson named below. Read no other lesson.

    lesson: {lesson_rel}

Then give the learner EXACTLY ONE task: the next single step of that lesson.
Write the task as an instruction addressed to the learner. Do not write the
learner's code, do not paste a solution, and do not give two steps.

The learner cannot see the lesson, `COURSE.md`, `DESIGN.md` or `{subdir}/`.
Anything the task depends on must be in the task itself.

When the lesson's completion condition is already met by the workspace as it
stands, reply with the single line `{marker}` and nothing else.

This is turn {turn} of this lesson.
"""

LEARNER_PROMPT = """{opening}

Your working directory is your own workspace. Do the task below.

You have no lesson text, no course outline and no design notes, and there is
none to find here - the harness gives you a directory that never contains
them. That is deliberate: you are standing where a real learner stands.

Task:

{task}

Do the work in your workspace. Then report, briefly: what you changed, what
you ran, and anything the task did not give you that you needed. If you could
not make progress, say so plainly and say what stopped you.
"""


def tutor_prompt(lesson: LessonRef, turn: int, subdir: str = INSTANCE_SUBDIR) -> str:
    return TUTOR_PROMPT.format(
        opening=TUTOR_PROMPT_OPENING,
        subdir=subdir,
        lesson_rel=lesson.rel,
        marker=LESSON_COMPLETE_MARKER,
        turn=turn,
    )


def learner_prompt(task: str) -> str:
    return LEARNER_PROMPT.format(opening=LEARNER_PROMPT_OPENING, task=task.strip())


def lesson_is_complete(text: str) -> bool:
    return LESSON_COMPLETE_MARKER in text


# --------------------------------------------------------------------------
# The driver
# --------------------------------------------------------------------------

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_STALL = 3
EXIT_ISOLATION = 4


@dataclass
class Config:
    instance: Path
    mirror: Path
    log: Path
    max_turns: int = 12
    stall_after: int = 3
    subdir: str = INSTANCE_SUBDIR


@dataclass
class RunOutcome:
    run_id: str
    lessons: list = field(default_factory=list)
    turns: int = 0
    stalls: list = field(default_factory=list)
    completed: list = field(default_factory=list)
    exhausted: list = field(default_factory=list)


class DryRun:
    def __init__(
        self,
        config: Config,
        agent: Agent,
        validators: ValidatorProbe,
        log: RunLog,
        course: str = "",
        out=sys.stdout,
    ) -> None:
        self.config = config
        self.agent = agent
        self.validators = validators
        self.log = log
        self.course = course
        self.out = out
        self.run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
        self.turn = 0
        self.learner_session: str | None = None
        # The run log carries every task the tutor has written. When it sits
        # inside the instance it is excluded from the sync by name as well as
        # by the `dryrun-*.jsonl` pattern, so a --log the caller named
        # something else still never reaches the learner.
        try:
            rel = self.log.path.resolve().relative_to(config.instance).as_posix()
            self._exclude = frozenset({rel})
        except ValueError:
            self._exclude = frozenset()

    def say(self, text: str = "") -> None:
        print(text, file=self.out)

    def walk(self, lessons: list[LessonRef]) -> RunOutcome:
        outcome = RunOutcome(run_id=self.run_id, lessons=[l.rel for l in lessons])
        self.log.append(
            {
                "kind": "run-start",
                "run_id": self.run_id,
                "course": self.course,
                "instance": str(self.config.instance),
                "mirror": str(self.config.mirror),
                "lessons": [l.rel for l in lessons],
                "max_turns": self.config.max_turns,
                "stall_after": self.config.stall_after,
                "agent": getattr(self.agent, "name", type(self.agent).__name__),
            }
        )
        try:
            for lesson in lessons:
                self._walk_lesson(lesson, outcome)
                if outcome.stalls:
                    break
        finally:
            self.log.append(
                {
                    "kind": "run-end",
                    "run_id": self.run_id,
                    "turns": outcome.turns,
                    "lessons_completed": list(outcome.completed),
                    "lessons_exhausted": list(outcome.exhausted),
                    "stalled_lessons": [report["lesson"] for report in outcome.stalls],
                }
            )
        return outcome

    def _walk_lesson(self, lesson: LessonRef, outcome: RunOutcome) -> None:
        self.say(f"== {lesson.rel}  ({lesson.title})")
        stall = StallDetector(self.config.stall_after)
        # A learner carries context inside one lesson and starts fresh at the
        # next: the session id is dropped here, not kept across lessons.
        self.learner_session = None
        before_state = self.validators.state(lesson)
        for lesson_turn in range(1, self.config.max_turns + 1):
            self.turn += 1
            outcome.turns = self.turn

            # THE TUTOR IS COLD EVERY TURN. Decision 1 of the issue: the
            # runner keeps its state in STATE.md, and a harness that resumed
            # the tutor would be testing a tutor that remembers what it just
            # said - an easier case than a learner ever meets. `resume` is
            # not passed here and must never be.
            tutor = self.agent.run(
                tutor_prompt(lesson, lesson_turn, self.config.subdir),
                cwd=self.config.instance,
                role="tutor",
                resume=None,
            )
            self.log.append(
                turn_record(
                    run_id=self.run_id,
                    course=self.course,
                    turn=self.turn,
                    role="tutor",
                    lesson=lesson.rel,
                    result=tutor,
                    resumed=False,
                )
            )
            task = tutor.text
            if lesson_is_complete(task):
                self.say(f"   turn {lesson_turn}: the tutor reports the lesson complete.")
                outcome.completed.append(lesson.rel)
                return

            # The learner never sees the instance. Sync what a learner may
            # see, then prove it before the turn rather than after.
            sync_to_mirror(self.config.instance, self.config.mirror, self._exclude)
            assert_learner_isolated(self.config.mirror)

            digest_before = tree_digest(self.config.mirror)
            learner = self.agent.run(
                learner_prompt(task),
                cwd=self.config.mirror,
                role="learner",
                resume=self.learner_session,
            )
            resumed = self.learner_session is not None
            if learner.session_id:
                self.learner_session = learner.session_id
            digest_after = tree_digest(self.config.mirror)
            changed = digest_after != digest_before

            sync_from_mirror(self.config.mirror, self.config.instance)
            after_state = self.validators.state(lesson)
            advanced = after_state.advanced_over(before_state)
            before_state = after_state

            stall.observe(
                StallObservation(
                    turn=lesson_turn,
                    lesson=lesson.rel,
                    workspace_changed=changed,
                    validators_advanced=advanced,
                    task=task,
                )
            )
            self.log.append(
                turn_record(
                    run_id=self.run_id,
                    course=self.course,
                    turn=self.turn,
                    role="learner",
                    lesson=lesson.rel,
                    result=learner,
                    resumed=resumed,
                    workspace_changed=changed,
                    validators=after_state,
                    quiet_turns=stall.count,
                )
            )
            self.say(
                f"   turn {lesson_turn}: workspace changed={changed} "
                f"validators passing={sorted(after_state.passing) or '-'} "
                f"quiet={stall.count}"
            )

            if stall.stalled:
                report = stall.report()
                assert report is not None
                self.log.append({**report.to_json(), "run_id": self.run_id, "turn": self.turn})
                outcome.stalls.append(report.to_json())
                self.say()
                self.say(report.render())
                return

        outcome.exhausted.append(lesson.rel)
        self.say(
            f"   the turn limit ({self.config.max_turns}) was reached with no "
            f"completion marker. This is a limit, not a finding."
        )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dryrun.py",
        description=(
            "Walk a tutorAIl course one task at a time with an agent playing "
            "the learner. The learner works in a mirror that never holds the "
            "course, and the guard that proves it aborts the run rather than "
            "warning."
        ),
        epilog=(
            "exit codes: 0 the run finished; 2 a usage error; 3 the run "
            "stopped early and a stall report was written (a localisation, "
            "not a verdict); 4 the isolation guard fired and the run was "
            "aborted."
        ),
    )
    parser.add_argument("instance", type=Path, help="the learner workspace holding tutorial/")
    parser.add_argument("--from", dest="frm", help="first lesson of the range")
    parser.add_argument("--to", dest="to", help="last lesson of the range (default: the same one)")
    parser.add_argument("--mirror", type=Path, help="the learner's directory (default: a temp dir)")
    parser.add_argument("--log", type=Path, help="the run log (default: <instance>/dryrun-<run>.jsonl)")
    parser.add_argument("--max-turns", type=int, default=12, help="turns per lesson before stopping")
    parser.add_argument("--stall-after", type=int, default=3, help="quiet learner turns that make a stall")
    parser.add_argument("--agent-command", default="claude", help="the CLI to run (default: claude)")
    parser.add_argument(
        "--agent-arg",
        action="append",
        default=[],
        help="one extra argument for the agent CLI; repeat for more",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="print what the run would do, call no agent, and spend nothing",
    )
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv[1:])
    try:
        return _run(args)
    except IsolationBreach as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ISOLATION
    except DryRunError as exc:
        print(f"dryrun.py: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except bl.ToolError as exc:
        print(f"dryrun.py: {exc}", file=sys.stderr)
        return EXIT_USAGE


def _run(args) -> int:
    instance = args.instance.resolve()
    if not instance.is_dir():
        raise DryRunError(f"{instance}: not a directory.")
    instance_dir = instance / INSTANCE_SUBDIR
    if not instance_dir.is_dir():
        raise DryRunError(
            f"{instance}: there is no {INSTANCE_SUBDIR}/ here, so this is not a "
            f"materialized instance. Point this at the learner's workspace, not "
            f"at the bundle."
        )

    lessons = read_lessons(instance_dir)
    chosen = select_lessons(lessons, args.frm, args.to, active_lesson(instance_dir))

    mirror = (args.mirror.resolve() if args.mirror else Path(tempfile.mkdtemp(prefix="dryrun-learner-")))
    if mirror == instance or instance in mirror.parents or mirror in instance.parents:
        raise DryRunError(
            f"{mirror}: the learner's mirror must not be inside the instance and "
            f"the instance must not be inside it. One would sync into the other."
        )

    manifest, _text = bl.load_manifest(instance_dir)
    course = str(manifest.get("id", instance_dir.name))
    log_path = args.log.resolve() if args.log else instance / f"dryrun-{course}.jsonl"

    if args.plan:
        print(f"instance:     {instance}")
        print(f"course:       {course}")
        print(f"mirror:       {mirror}")
        print(f"log:          {log_path}")
        print(f"agent:        {args.agent_command} {' '.join(args.agent_arg)}".rstrip())
        print(f"max turns:    {args.max_turns} per lesson")
        print(f"stall after:  {args.stall_after} quiet learner turns")
        print("lessons:")
        for lesson in chosen:
            print(f"  {lesson.rel}  validators={lesson.validators or '-'}")
        print()
        print("--plan called no agent and spent nothing.")
        return EXIT_OK

    config = Config(
        instance=instance,
        mirror=mirror,
        log=log_path,
        max_turns=args.max_turns,
        stall_after=args.stall_after,
    )
    agent = CliAgent(command=args.agent_command, extra_args=args.agent_arg)
    probe = CommandValidators(instance, manifest)
    run_log = RunLog(log_path)

    print(f"mirror: {mirror}")
    print(f"log:    {log_path}")
    driver = DryRun(config, agent, probe, run_log, course=course)
    outcome = driver.walk(chosen)
    print()
    print(f"{outcome.turns} turn(s) over {len(outcome.lessons)} lesson(s). Log: {log_path}")
    return EXIT_STALL if outcome.stalls else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv))
