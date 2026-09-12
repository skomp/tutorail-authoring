#!/usr/bin/env python3
"""dryrun.py - the harness that walks a course with an agent playing the learner.

Run: python3 tests/test_dryrun.py

COST
====

`COST = "cheap"`. THIS SUITE SPENDS NO TOKENS, and one of its cases is the
guard that keeps that true: a tripwire named `claude` is put first on `$PATH`,
a whole run is driven against the stub, and the tripwire must not have fired.
The same case then runs a POSITIVE CONTROL that makes the tripwire fire, so
the absence in the first half is an absence the probe could actually have
seen. An unfired tripwire nobody has watched fire is not a tripwire.

Phase 2 - the real `claude -p` turns - is a separate suite that will declare
`COST = "tokens"`. It does not exist yet and must not be bolted onto this one.

WHAT THIS SUITE IS ACTUALLY ABOUT
=================================

One property carries the whole harness: **an agent that has read the lesson
cannot play the learner.** So the isolation is structural - the learner's cwd
is a mirror that never contains `tutorial/` - and the guard that proves it
runs before every learner turn and ABORTS rather than warns.

A guard nobody has watched fire is not a guard, so every refusal case here has
a positive control on an input differing only in the thing under test:

  * a planted lesson fires the guard  /  an ordinary learner workspace is clean
  * a renamed lesson fires it         /  a near-miss file with ONE lesson-ish
                                         heading does not
  * a stubbed run leaves the tripwire /  an unstubbed run trips it
    untouched
  * a payload with no usage records   /  a payload with usage records ints
    nulls
  * the stall report carries no       /  the same probe fires on wording that
    verdict wording                      does rule

The stall cases matter for the same reason in reverse: the detector must be
shown NOT firing on a learner who is working, or "stalled" would just mean
"a turn happened".
"""

from __future__ import annotations

COST = "cheap"

import importlib.util
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    DRYRUN,
    FIXTURES,
    Workspace,
    case,
    check,
    check_in,
    listing,
    note,
    report,
    run,
)

# dryrun.py is loaded BY PATH, not by putting its directory on sys.path.
# harness.py says at length why course-quality's scripts directory must not
# join tutorail-authoring's on one path, and that reasoning does not stop
# being true because this suite would find an import statement convenient.
# The module still resolves `bundlelib` normally, because harness.py has
# already put the authoring scripts on the path.
_spec = importlib.util.spec_from_file_location("dryrun_under_test", DRYRUN)
assert _spec is not None and _spec.loader is not None
dryrun = importlib.util.module_from_spec(_spec)
# sys.modules must hold it BEFORE exec: @dataclass resolves a field's type
# through sys.modules[cls.__module__], and a module that is not registered
# makes every frozen dataclass in the file raise at import time.
sys.modules["dryrun_under_test"] = dryrun
_spec.loader.exec_module(dryrun)

INSTANCE_FIXTURE = "dryrun-instance"
STUB_AGENT = FIXTURES / "dryrun-stub-agent.py"
TRIPWIRE_BIN = FIXTURES / "dryrun-tripwire-bin"
LESSON_00 = "lessons/00-first-steps.md"
LESSON_01 = "lessons/01-second-steps.md"


# --------------------------------------------------------------------------
# The in-process stub. No process starts, so no token is spent.
# --------------------------------------------------------------------------


class StubAgent(dryrun.Agent):
    """The seam, substituted.

    Its payloads go through the real `parse_agent_json`, so the accounting
    path under test is the same one a real turn would take - only the process
    is gone.
    """

    name = "stub"

    def __init__(self, tutor=None, learner=None) -> None:
        self.tutor = tutor or (lambda n, cwd: f"Task {n}: do the next step.")
        self.learner = learner or (lambda n, cwd: "I could not see what to change.")
        self.calls: list[dict] = []

    def run(self, prompt, *, cwd, role, resume=None):
        self.calls.append(
            {"role": role, "cwd": Path(cwd), "resume": resume, "prompt": prompt}
        )
        nth = sum(1 for call in self.calls if call["role"] == role)
        text = (self.tutor if role == "tutor" else self.learner)(nth, Path(cwd))
        payload = {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "duration_ms": 1000 + nth,
            "num_turns": 1,
            "result": text,
            "session_id": f"stub-{role}-session",
            "total_cost_usd": 0.0,
            "usage": {
                "input_tokens": 1000 + nth,
                "output_tokens": 100 + nth,
                "cache_read_input_tokens": 7,
                "cache_creation_input_tokens": 3,
            },
        }
        return dryrun.parse_agent_json(
            json.dumps(payload), role=role, argv=["stub", role], wall_ms=1
        )


class StubValidators(dryrun.ValidatorProbe):
    """A validator probe driven by a list of passing sets, one per call."""

    def __init__(self, sequence=()) -> None:
        self.sequence = [frozenset(item) for item in sequence]
        self.calls = 0

    def state(self, lesson):
        index = min(self.calls, len(self.sequence) - 1) if self.sequence else -1
        self.calls += 1
        passing = self.sequence[index] if self.sequence else frozenset()
        return dryrun.ValidatorState(passing, frozenset({"probe"}), frozenset())


def drive(instance: Path, mirror: Path, log: Path, agent, validators=None, **config):
    """Run the driver in process over one lesson. Returns (outcome, log records)."""
    settings = {"max_turns": 4, "stall_after": 3}
    settings.update(config)
    wanted = settings.pop("lesson", LESSON_00)
    cfg = dryrun.Config(instance=instance, mirror=mirror, log=log, **settings)
    run_log = dryrun.RunLog(log)
    lessons = dryrun.read_lessons(instance / "tutorial")
    chosen = [lesson for lesson in lessons if lesson.rel == wanted] or [lessons[0]]
    with open(os.devnull, "w", encoding="utf-8") as quiet:
        driver = dryrun.DryRun(
            cfg, agent, validators or StubValidators(), run_log,
            course="dryrun-fixture", out=quiet,
        )
        outcome = driver.walk(chosen)
    records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    return outcome, records


def plant_lesson(mirror: Path, rel: str, *, strip_frontmatter: bool = False) -> Path:
    """Put a REAL lesson into the mirror under a name that hides it."""
    source = FIXTURES / INSTANCE_FIXTURE / "tutorial" / LESSON_00
    text = source.read_text(encoding="utf-8")
    if strip_frontmatter:
        _front, text = dryrun.bl.split_frontmatter(text)
    target = mirror / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target


def learner_workspace(root: Path) -> Path:
    """An ordinary learner mirror: the positive control for every guard case."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text("# my work\n\nNotes to self.\n", encoding="utf-8")
    (root / "src").mkdir(exist_ok=True)
    (root / "src" / "main.py").write_text('print("hello")\n', encoding="utf-8")
    return root


# --------------------------------------------------------------------------
# 1. The isolation guard
# --------------------------------------------------------------------------


def guard_case_clean() -> None:
    """The positive control: an ordinary learner workspace comes back clean."""
    with Workspace() as ws:
        mirror = learner_workspace(ws.path("mirror"))
        findings = dryrun.check_isolation(mirror)
        check(findings == [], f"an ordinary learner mirror has no findings (got {findings})")
        try:
            dryrun.assert_learner_isolated(mirror)
            check(True, "assert_learner_isolated returns on a clean mirror")
        except dryrun.IsolationBreach as exc:
            check(False, f"assert_learner_isolated raised on a clean mirror: {exc}")


def guard_case_tutorial_dir() -> None:
    with Workspace() as ws:
        mirror = learner_workspace(ws.path("mirror"))
        (mirror / "tutorial").mkdir()
        findings = dryrun.check_isolation(mirror)
        rels = [f.rel for f in findings]
        check(
            any(rel.startswith("tutorial") for rel in rels),
            f"an EMPTY tutorial/ directory fires the guard (got {rels})",
        )


def guard_case_planted_lesson() -> None:
    """THE CASE THE WHOLE DESIGN RESTS ON.

    A lesson copied into the mirror under an innocent name. A guard that only
    looked at path names would miss this, and a learner reading
    `notes/reading.md` has read the answer just as surely as one reading
    `tutorial/lessons/00-first-steps.md`.
    """
    with Workspace() as ws:
        mirror = learner_workspace(ws.path("mirror"))
        plant_lesson(mirror, "notes/reading.md")
        findings = dryrun.check_isolation(mirror)
        rels = [f.rel for f in findings]
        check(
            "notes/reading.md" in rels,
            f"a lesson planted as notes/reading.md fires the guard (got {rels})",
        )
        reasons = [f.reason for f in findings if f.rel == "notes/reading.md"]
        check(
            any("frontmatter" in reason for reason in reasons),
            f"the finding says WHY it is a lesson (got {reasons})",
        )
        raised = False
        try:
            dryrun.assert_learner_isolated(mirror)
        except dryrun.IsolationBreach as exc:
            raised = True
            check_in("notes/reading.md", str(exc), "the breach message names the file")
        check(raised, "assert_learner_isolated raises on a planted lesson")


def guard_case_stripped_lesson() -> None:
    """A lesson with its frontmatter cut off is still a lesson."""
    with Workspace() as ws:
        mirror = learner_workspace(ws.path("mirror"))
        plant_lesson(mirror, "scratch.txt", strip_frontmatter=True)
        findings = [f for f in dryrun.check_isolation(mirror) if f.rel == "scratch.txt"]
        check(bool(findings), "a lesson body with no frontmatter still fires the guard")
        check(
            any("headings" in f.reason for f in findings),
            f"the finding names the body headings (got {[f.reason for f in findings]})",
        )


def guard_case_near_miss() -> None:
    """The control that keeps the sniff from being useless.

    A guard that fired on the words `## Learning objectives` alone would fire
    on a learner's own notes, and a harness that aborts on the learner's notes
    is a harness nobody runs.
    """
    with Workspace() as ws:
        mirror = learner_workspace(ws.path("mirror"))
        (mirror / "plan.md").write_text(
            "# My plan\n\n## Learning objectives\n\n- get better at this\n",
            encoding="utf-8",
        )
        findings = [f for f in dryrun.check_isolation(mirror) if f.rel == "plan.md"]
        check(
            findings == [],
            f"one lesson-ish heading in the learner's own notes is NOT a lesson (got {findings})",
        )
        (mirror / "plan.md").write_text(
            "# My plan\n\n## Learning objectives\n\n- x\n\n## Suggested progression\n\n- y\n",
            encoding="utf-8",
        )
        findings = [f for f in dryrun.check_isolation(mirror) if f.rel == "plan.md"]
        check(
            bool(findings),
            "the SAME file with a second lesson heading added does fire - so the "
            "first result was the sniff deciding, not the sniff being blind",
        )


def guard_case_sync_never_copies_course() -> None:
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        mirror = ws.path("mirror")
        dryrun.sync_to_mirror(instance, mirror)
        entries = listing(mirror)
        check("tutorial" not in entries, f"sync_to_mirror never copies tutorial/ (got {entries})")
        check("README.md" in entries, "sync_to_mirror does copy the learner's files")
        check(
            (mirror / "src" / "main.py").exists(),
            "sync_to_mirror copies the learner's nested files",
        )
        check(
            dryrun.check_isolation(mirror) == [],
            "a mirror built by sync_to_mirror passes the guard",
        )


def guard_case_sync_excludes_the_log() -> None:
    """The run log holds every task the tutor has written. It is not the learner's."""
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        (instance / "dryrun-dryrun-fixture.jsonl").write_text(
            '{"kind":"turn","role":"tutor"}\n', encoding="utf-8"
        )
        (instance / "notes.jsonl").write_text('{"mine":true}\n', encoding="utf-8")
        mirror = ws.path("mirror")
        dryrun.sync_to_mirror(instance, mirror)
        entries = listing(mirror)
        check(
            "dryrun-dryrun-fixture.jsonl" not in entries,
            f"the run log is never copied to the learner (got {entries})",
        )
        check(
            "notes.jsonl" in entries,
            "a jsonl file that is NOT a run log still reaches the learner - so the "
            "exclusion is by pattern, not by extension",
        )


def guard_case_run_aborts() -> None:
    """A breach stops the run. It is not a warning in the log."""
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        mirror = ws.path("mirror")
        plant_lesson(mirror, "cheatsheet.md")
        agent = StubAgent(learner=lambda n, cwd: "done")
        log = ws.path("run.jsonl")
        raised = None
        try:
            drive(instance, mirror, log, agent)
        except dryrun.IsolationBreach as exc:
            raised = exc
        check(raised is not None, "a planted lesson aborts the whole run")
        roles = [call["role"] for call in agent.calls]
        check(
            "learner" not in roles,
            f"the learner turn never happens after a breach (calls: {roles})",
        )
        records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
        kinds = [r["kind"] for r in records]
        check("run-end" in kinds, "the run log is closed even when the run aborts")


# --------------------------------------------------------------------------
# 2. The agent seam and the accounting
# --------------------------------------------------------------------------


def seam_case_parse_usage() -> None:
    payload = {
        "type": "result",
        "is_error": False,
        "duration_ms": 5123,
        "num_turns": 3,
        "result": "Task 1: write the file.",
        "session_id": "abc-123",
        "total_cost_usd": 0.0431,
        "usage": {
            "input_tokens": 4200,
            "output_tokens": 311,
            "cache_read_input_tokens": 18000,
            "cache_creation_input_tokens": 900,
        },
    }
    result = dryrun.parse_agent_json(json.dumps(payload), role="tutor", argv=["x"], wall_ms=5200)
    check(result.session_id == "abc-123", "the session id is parsed")
    check(result.input_tokens == 4200, "input tokens are parsed")
    check(result.output_tokens == 311, "output tokens are parsed")
    check(result.cache_read_input_tokens == 18000, "cache-read tokens are parsed")
    check(result.duration_ms == 5123, "the reported duration is parsed")
    check(result.total_cost_usd == 0.0431, "the reported cost is parsed")
    check(result.usage_present is True, "usage_present is true when usage is there")
    check(result.text.startswith("Task 1"), "the result text is parsed")


def seam_case_missing_usage_is_null_not_zero() -> None:
    """A missing count is null. A zero is a number someone would add up."""
    payload = {"result": "hi", "session_id": "s", "is_error": False}
    result = dryrun.parse_agent_json(json.dumps(payload), role="tutor", argv=["x"], wall_ms=1)
    check(result.input_tokens is None, f"a missing input_tokens is None, not 0 (got {result.input_tokens!r})")
    check(result.output_tokens is None, "a missing output_tokens is None, not 0")
    check(result.usage_present is False, "usage_present is false when usage is absent")
    record = dryrun.turn_record(
        run_id="r", course="c", turn=1, role="tutor", lesson=LESSON_00, result=result, resumed=False
    )
    line = json.dumps(record)
    check_in('"input_tokens": null', line, "the log line carries null, not 0")
    check(json.loads(line)["usage_present"] is False, "the log line says usage was absent")


def seam_case_refuses_garbage() -> None:
    raised = False
    try:
        dryrun.parse_agent_json("not json at all", role="tutor", argv=["x"], wall_ms=1)
    except dryrun.AgentError:
        raised = True
    check(raised, "stdout that is not JSON is refused, not defaulted to zeros")
    raised = False
    try:
        dryrun.parse_agent_json("", role="tutor", argv=["x"], wall_ms=1)
    except dryrun.AgentError:
        raised = True
    check(raised, "empty stdout is refused")
    # The positive control: the same call on valid JSON must NOT raise, or the
    # two cases above would pass against a parser that refuses everything.
    ok = dryrun.parse_agent_json('{"result":"x","session_id":"s"}', role="tutor", argv=["x"], wall_ms=1)
    check(ok.text == "x", "the same parser accepts a valid payload")


def seam_case_argv() -> None:
    agent = dryrun.CliAgent(command="claude", extra_args=["--permission-mode", "acceptEdits"])
    cold = agent.build_argv("hello", None)
    warm = agent.build_argv("hello", "sess-1")
    check("--output-format" in cold and cold[cold.index("--output-format") + 1] == "json",
          "the argv asks for --output-format json")
    check("--resume" not in cold, f"no resume means no --resume in the argv (got {cold})")
    check(warm[warm.index("--resume") + 1] == "sess-1", "a session id becomes --resume <id>")
    check(cold[-2:] == ["--permission-mode", "acceptEdits"], "extra agent args are passed through")


# --------------------------------------------------------------------------
# 3. The stall detector. It localises and never rules.
# --------------------------------------------------------------------------


def stall_case_fires() -> None:
    detector = dryrun.StallDetector(3)
    for turn in (1, 2, 3):
        detector.observe(
            dryrun.StallObservation(
                turn=turn,
                lesson=LESSON_00,
                workspace_changed=False,
                validators_advanced=False,
                task="Task 3: write src/answer.txt.",
            )
        )
    check(detector.stalled, "three quiet turns at threshold 3 is a stall")
    report_ = detector.report()
    check(report_ is not None, "a stall produces a report")
    assert report_ is not None
    check(report_.lesson == LESSON_00, "the report localises the lesson")
    check(report_.first_quiet_turn == 1, "the report localises the first quiet turn")
    check(report_.last_turn == 3, "the report localises the last turn observed")
    text = report_.render()
    check_in("Task 3: write src/answer.txt.", text, "the report quotes the last task")
    check_in(dryrun.STALL_DISCLAIMER, text, "the report carries the disclaimer")


def stall_case_does_not_fire() -> None:
    """The control. Without it, "stalled" would just mean "a turn happened"."""
    detector = dryrun.StallDetector(3)
    detector.observe(dryrun.StallObservation(1, LESSON_00, False, False))
    detector.observe(dryrun.StallObservation(2, LESSON_00, True, False))
    detector.observe(dryrun.StallObservation(3, LESSON_00, False, False))
    check(not detector.stalled, "a workspace change resets the count")
    check(detector.report() is None, "no stall, no report")

    detector = dryrun.StallDetector(2)
    detector.observe(dryrun.StallObservation(1, LESSON_00, False, False))
    detector.observe(dryrun.StallObservation(2, LESSON_00, False, True))
    check(not detector.stalled, "validator progress with no file change also resets the count")

    detector = dryrun.StallDetector(2)
    detector.observe(dryrun.StallObservation(1, LESSON_00, False, False))
    detector.observe(dryrun.StallObservation(2, LESSON_00, False, False))
    check(detector.stalled, "the SAME detector does fire when both signals stay quiet")


def stall_case_no_verdict_wording() -> None:
    """The harness's own words must not rule on anything."""
    report_ = dryrun.StallReport(
        lesson=LESSON_00,
        first_quiet_turn=4,
        last_turn=6,
        quiet_turns=3,
        threshold=3,
        last_task="",
    )
    hits = dryrun.verdict_language(report_.render())
    check(hits == [], f"the stall report's own wording carries no verdict (got {hits})")
    check_in(
        dryrun.STALL_DISCLAIMER,
        report_.render(),
        "and it says out loud that it cannot tell the two cases apart",
    )
    check_in(
        "not a finding",
        report_.render(),
        "the heading says the report is a localisation, not a finding",
    )
    # The positive control. The same probe on wording that DOES rule must
    # fire, or the clean result above is the probe being blind.
    ruled = "STALL: lesson 00 has an unsatisfiable completion condition. The lesson is wrong."
    hits = dryrun.verdict_language(ruled)
    check(bool(hits), f"the same probe fires on wording that rules (got {hits})")
    # And the quoted task is quoted verbatim, which is a limit worth knowing:
    # a tutor whose task says "fix the broken parser" puts that word in the
    # report. The probe covers the harness's words, not the tutor's.
    quoting = dryrun.StallReport(LESSON_00, 1, 2, 2, 2, "Fix the broken parser.")
    check(
        bool(dryrun.verdict_language(quoting.render())),
        "a task quoted verbatim can carry words the harness itself would never write",
    )


def stall_case_in_a_run() -> None:
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        mirror = ws.path("mirror")
        log = ws.path("run.jsonl")
        agent = StubAgent()  # the learner changes nothing, ever
        outcome, records = drive(instance, mirror, log, agent, stall_after=2, max_turns=6)
        check(bool(outcome.stalls), "a learner who changes nothing produces a stall")
        stalls = [r for r in records if r["kind"] == "stall"]
        check(len(stalls) == 1, f"one stall record is logged (got {len(stalls)})")
        if stalls:
            check(stalls[0]["lesson"] == LESSON_00, "the stall record names the lesson")
            check(stalls[0]["disclaimer"] == dryrun.STALL_DISCLAIMER,
                  "the stall record carries the disclaimer, not a diagnosis")
            check_in("Task", stalls[0]["last_task"], "the stall record carries the last task")
        turns = [r for r in records if r["kind"] == "turn" and r["role"] == "learner"]
        check(len(turns) == 2, f"the run stops at the threshold (learner turns: {len(turns)})")


def stall_case_working_learner() -> None:
    """The positive control for the case above, differing only in the learner."""
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        mirror = ws.path("mirror")
        log = ws.path("run.jsonl")
        written = {"n": 0}

        def learner(n, cwd):
            written["n"] += 1
            (cwd / "src").mkdir(parents=True, exist_ok=True)
            (cwd / "src" / "answer.txt").write_text(f"turn {n}\n", encoding="utf-8")
            return "I wrote src/answer.txt."

        agent = StubAgent(learner=learner)
        outcome, records = drive(instance, mirror, log, agent, stall_after=2, max_turns=3)
        check(not outcome.stalls, "a learner who changes the workspace never stalls")
        check(
            not any(r["kind"] == "stall" for r in records),
            "and no stall record is written",
        )
        check(
            (instance / "src" / "answer.txt").exists(),
            "the learner's work is synced back into the instance, so the tutor sees it",
        )


# --------------------------------------------------------------------------
# 4. The tutor is cold. The learner is not.
# --------------------------------------------------------------------------


def session_case_tutor_cold_learner_warm() -> None:
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        mirror = ws.path("mirror")
        log = ws.path("run.jsonl")

        def learner(n, cwd):
            (cwd / f"work-{n}.txt").write_text(f"{n}\n", encoding="utf-8")
            return "done"

        agent = StubAgent(learner=learner)
        drive(instance, mirror, log, agent, max_turns=3, stall_after=9)
        tutor_resumes = [call["resume"] for call in agent.calls if call["role"] == "tutor"]
        learner_resumes = [call["resume"] for call in agent.calls if call["role"] == "learner"]
        check(
            tutor_resumes and all(value is None for value in tutor_resumes),
            f"the tutor is started cold on every turn (resumes: {tutor_resumes})",
        )
        check(
            learner_resumes[0] is None,
            "the learner's first turn has nothing to resume",
        )
        check(
            len(learner_resumes) > 1 and learner_resumes[1] == "stub-learner-session",
            f"the learner's later turns resume its session (resumes: {learner_resumes})",
        )
        tutor_cwds = {call["cwd"] for call in agent.calls if call["role"] == "tutor"}
        learner_cwds = {call["cwd"] for call in agent.calls if call["role"] == "learner"}
        check(tutor_cwds == {instance}, f"the tutor works in the instance (got {tutor_cwds})")
        check(learner_cwds == {mirror}, f"the learner works in the mirror (got {learner_cwds})")


def session_case_log_fields() -> None:
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        mirror = ws.path("mirror")
        log = ws.path("run.jsonl")
        def learner(n, cwd):
            (cwd / f"w{n}.txt").write_text("x\n", encoding="utf-8")
            return "I wrote a file."

        agent = StubAgent(
            tutor=lambda n, cwd: ("LESSON COMPLETE" if n >= 3 else f"Task {n}."),
            learner=learner,
        )
        outcome, records = drive(instance, mirror, log, agent, max_turns=6, stall_after=9)
        kinds = [r["kind"] for r in records]
        check(kinds[0] == "run-start", "the log opens with a run-start record")
        check(kinds[-1] == "run-end", "the log closes with a run-end record")
        turns = [r for r in records if r["kind"] == "turn"]
        check(len(turns) == 5, f"five turn records for 3 tutor + 2 learner turns (got {len(turns)})")
        required = {
            "turn", "role", "lesson", "session_id", "input_tokens", "output_tokens",
            "duration_ms", "wall_ms", "total_cost_usd", "resumed", "run_id", "course",
        }
        missing = sorted(required - set(turns[0]))
        check(not missing, f"a turn record carries what a cost decision needs (missing {missing})")
        check(
            all(isinstance(r["input_tokens"], int) for r in turns),
            "every turn records its input tokens as a number",
        )
        learner_turns = [r for r in turns if r["role"] == "learner"]
        check(
            all("workspace_changed" in r for r in learner_turns),
            "a learner turn records whether the workspace changed",
        )
        check(
            all("validators_probed" in r for r in learner_turns),
            "a learner turn records WHICH validators were probed, so a lesson with "
            "no probeable validator is visible rather than silently quiet",
        )
        check(
            outcome.completed == [LESSON_00],
            f"the completion marker ends the lesson (got {outcome.completed})",
        )


# --------------------------------------------------------------------------
# 5. The CLI, and the tripwire that keeps this suite free
# --------------------------------------------------------------------------


def cli_env(sentinel: Path, **extra) -> dict:
    env = {
        "PATH": f"{TRIPWIRE_BIN}{os.pathsep}{os.environ.get('PATH', '')}",
        "DRYRUN_TRIPWIRE_SENTINEL": str(sentinel),
    }
    env.update(extra)
    return env


def cli_case_never_runs_claude() -> None:
    """The guard that keeps `COST = "cheap"` true, with its positive control."""
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        mirror = ws.path("mirror")
        log = ws.path("run.jsonl")
        sentinel = ws.path("tripwire.txt")
        argv_log = ws.path("stub-argv.jsonl")
        done = run(
            DRYRUN,
            instance,
            "--from",
            LESSON_00,
            "--mirror",
            mirror,
            "--log",
            log,
            "--agent-command",
            STUB_AGENT,
            "--max-turns",
            "3",
            "--stall-after",
            "9",
            env=cli_env(
                sentinel,
                DRYRUN_STUB_ARGV=str(argv_log),
                DRYRUN_STUB_TOUCH="src/answer.txt",
                DRYRUN_STUB_COMPLETE_AFTER="3",
            ),
        )
        check(done.returncode == 0, f"the stubbed run exits 0 (got {done.returncode}):\n{done.output}")
        check(
            not sentinel.exists(),
            f"the stubbed run never reached the real `claude` (sentinel: "
            f"{sentinel.read_text() if sentinel.exists() else 'absent'})",
        )
        check(argv_log.exists(), "the stub agent was the thing that ran")

        # THE POSITIVE CONTROL. The same invocation without --agent-command
        # must trip the wire. Without this half, "the sentinel is absent"
        # says nothing: a sentinel that can never be written is absent too.
        sentinel2 = ws.path("tripwire2.txt")
        done = run(
            DRYRUN,
            instance,
            "--from",
            LESSON_00,
            "--mirror",
            ws.path("mirror2"),
            "--log",
            ws.path("run2.jsonl"),
            "--max-turns",
            "1",
            env=cli_env(sentinel2),
        )
        check(
            sentinel2.exists(),
            "the SAME run with the default agent command does reach `claude` - so "
            "the absence above was the probe seeing nothing, not the probe being blind",
        )
        check(done.returncode != 0, "and that run fails rather than reporting a turn")


def cli_case_tutor_never_resumes_over_the_cli() -> None:
    """Decision 1, proved at the argv level rather than in the driver's head."""
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        argv_log = ws.path("stub-argv.jsonl")
        sentinel = ws.path("tripwire.txt")
        done = run(
            DRYRUN,
            instance,
            "--from",
            LESSON_00,
            "--mirror",
            ws.path("mirror"),
            "--log",
            ws.path("run.jsonl"),
            "--agent-command",
            STUB_AGENT,
            "--max-turns",
            "4",
            "--stall-after",
            "9",
            env=cli_env(
                sentinel,
                DRYRUN_STUB_ARGV=str(argv_log),
                DRYRUN_STUB_TOUCH="src/answer.txt",
                DRYRUN_STUB_COMPLETE_AFTER="4",
            ),
        )
        check(done.returncode == 0, f"the run exits 0 (got {done.returncode}):\n{done.output}")
        calls = [json.loads(line) for line in argv_log.read_text(encoding="utf-8").splitlines()]
        tutor = [c for c in calls if c["role"] == "tutor"]
        learner = [c for c in calls if c["role"] == "learner"]
        check(len(tutor) >= 3, f"the tutor ran more than once (got {len(tutor)})")
        check(
            all("--resume" not in c["argv"] for c in tutor),
            "no tutor process is ever given --resume",
        )
        check(
            any("--resume" in c["argv"] for c in learner),
            "a learner process IS given --resume - so the check above is a probe "
            "that can see --resume when it is there",
        )
        check(
            all(c["cwd"].endswith("mirror") for c in learner),
            f"every learner process runs in the mirror (got {[c['cwd'] for c in learner]})",
        )


def cli_case_learner_cwd_has_no_course() -> None:
    """After a whole CLI run, the learner's directory still holds no course."""
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        mirror = ws.path("mirror")
        run(
            DRYRUN,
            instance,
            "--from",
            LESSON_00,
            "--mirror",
            mirror,
            "--log",
            ws.path("run.jsonl"),
            "--agent-command",
            STUB_AGENT,
            "--max-turns",
            "3",
            "--stall-after",
            "9",
            env=cli_env(
                ws.path("tripwire.txt"),
                DRYRUN_STUB_ARGV=str(ws.path("argv.jsonl")),
                DRYRUN_STUB_TOUCH="src/answer.txt",
                DRYRUN_STUB_COMPLETE_AFTER="3",
            ),
        )
        entries = listing(mirror)
        check("tutorial" not in entries, f"the mirror has no tutorial/ (got {entries})")
        check(
            dryrun.check_isolation(mirror) == [],
            f"the mirror passes the guard after a full run: {dryrun.check_isolation(mirror)}",
        )
        check(
            "tutorial" in listing(instance),
            "and the instance still has its course - the sync did not move it",
        )


def cli_case_plan_spends_nothing() -> None:
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        sentinel = ws.path("tripwire.txt")
        done = run(DRYRUN, instance, "--plan", env=cli_env(sentinel))
        check(done.returncode == 0, f"--plan exits 0 (got {done.returncode}):\n{done.output}")
        check(not sentinel.exists(), "--plan starts no agent process")
        check_in(LESSON_01, done.stdout, "--plan names the lesson it would walk")
        check_in("spent nothing", done.stdout, "--plan says so out loud")


# --------------------------------------------------------------------------
# 6. The lesson range
# --------------------------------------------------------------------------


def range_case_default_is_one_lesson() -> None:
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        lessons = dryrun.read_lessons(instance / "tutorial")
        active = dryrun.active_lesson(instance / "tutorial")
        chosen = dryrun.select_lessons(lessons, None, None, active)
        check(len(chosen) == 1, f"the default range is one lesson (got {len(chosen)})")
        check(
            chosen[0].rel == LESSON_01,
            f"and it is STATE.md's active lesson, not the first (got {chosen[0].rel})",
        )
        # The control: with no STATE.md the same call must pick the FIRST
        # lesson, or the assertion above would pass against a function that
        # always returns lessons[0] on a fixture whose active lesson is 01.
        (instance / "tutorial" / "STATE.md").unlink()
        chosen = dryrun.select_lessons(lessons, None, None, dryrun.active_lesson(instance / "tutorial"))
        check(
            chosen[0].rel == LESSON_00,
            f"with no STATE.md the default is the first lesson (got {chosen[0].rel})",
        )


def range_case_from_to() -> None:
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        lessons = dryrun.read_lessons(instance / "tutorial")
        chosen = dryrun.select_lessons(lessons, LESSON_00, LESSON_01, None)
        check([l.rel for l in chosen] == [LESSON_00, LESSON_01], "--from/--to is inclusive")
        chosen = dryrun.select_lessons(lessons, "00-first-steps", None, None)
        check(
            [l.rel for l in chosen] == [LESSON_00],
            "--from alone walks exactly that one lesson",
        )
        chosen = dryrun.select_lessons(lessons, "01-second-steps", None, None)
        check([l.rel for l in chosen] == [LESSON_01], "a lesson is resolvable by its slug")
        raised = False
        try:
            dryrun.select_lessons(lessons, LESSON_01, LESSON_00, None)
        except dryrun.DryRunError as exc:
            raised = True
            check_in("comes before", str(exc), "the refusal says what is wrong")
        check(raised, "--to before --from is refused")
        raised = False
        try:
            dryrun.select_lessons(lessons, "no-such-lesson", None, None)
        except dryrun.DryRunError:
            raised = True
        check(raised, "an unknown lesson is refused")


def range_case_not_an_instance() -> None:
    """A bundle is not an instance. The refusal says which one it wanted."""
    with Workspace() as ws:
        bundle = ws.copy("durable-event-broker-mini")
        done = run(DRYRUN, bundle, "--plan", env=cli_env(ws.path("tripwire.txt")))
        check(done.returncode == 2, f"a bundle path is refused (exit {done.returncode})")
        check_in("tutorial/", done.output, "the refusal names what was missing")
        # The control: the instance fixture, which differs only by having a
        # tutorial/ directory, is accepted by the same code path.
        instance = ws.copy(INSTANCE_FIXTURE)
        done = run(DRYRUN, instance, "--plan", env=cli_env(ws.path("tripwire2.txt")))
        check(done.returncode == 0, "and an instance is accepted by the same check")


def seed_case_unit_rule() -> None:
    """--from past the first lesson needs --seed. --from at the first does not."""
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        lessons = dryrun.read_lessons(instance / "tutorial")
        second = [l for l in lessons if l.rel == LESSON_01]
        first = [l for l in lessons if l.rel == LESSON_00]

        raised = False
        try:
            dryrun.require_seed(lessons, second, None, explicit_from=True)
        except dryrun.DryRunError as exc:
            raised = True
            check_in("--seed", str(exc), "the refusal names the flag that fixes it")
            check_in(
                "artefact of how the run was started",
                str(exc),
                "and says WHY: the harness would manufacture the finding",
            )
            check_in(LESSON_00, str(exc), "and names the lessons whose work is missing")
        check(raised, "--from lessons/01 with no --seed is refused")

        # Three positive controls, each differing from the refusal in exactly
        # one thing. Without them the refusal could be a function that always
        # raises.
        try:
            dryrun.require_seed(lessons, second, Path("/tmp/prepared"), explicit_from=True)
            check(True, "the SAME call with --seed supplied is allowed")
        except dryrun.DryRunError as exc:
            check(False, f"--seed should have satisfied the rule: {exc}")
        try:
            dryrun.require_seed(lessons, first, None, explicit_from=True)
            check(True, "--from at the course's first lesson needs no --seed")
        except dryrun.DryRunError as exc:
            check(False, f"the first lesson should need no seed: {exc}")
        try:
            dryrun.require_seed(lessons, second, None, explicit_from=False)
            check(True, "a run with no --from at all is not affected by the rule")
        except dryrun.DryRunError as exc:
            check(False, f"the default range should need no seed: {exc}")


def seed_case_cli_refuses() -> None:
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        done = run(
            DRYRUN, instance, "--from", LESSON_01, "--plan",
            env=cli_env(ws.path("tripwire.txt")),
        )
        check(done.returncode == 2, f"the CLI refuses --from 01 with no --seed (exit {done.returncode})")
        check_in("--seed", done.output, "the CLI refusal names --seed")
        check(
            not ws.path("tripwire.txt").exists(),
            "and it refuses before any agent process could start",
        )
        # THE POSITIVE CONTROL: the same invocation with --seed supplied runs.
        prepared = learner_workspace(ws.path("prepared"))
        done = run(
            DRYRUN, instance, "--from", LESSON_01, "--seed", prepared, "--plan",
            env=cli_env(ws.path("tripwire2.txt")),
        )
        check(done.returncode == 0, f"the same invocation with --seed is allowed (exit {done.returncode}):\n{done.output}")
        check_in(str(prepared), done.stdout, "--plan says which workspace it would seed from")
        # And the other axis: the first lesson still needs nothing.
        done = run(
            DRYRUN, instance, "--from", LESSON_00, "--plan",
            env=cli_env(ws.path("tripwire3.txt")),
        )
        check(done.returncode == 0, "--from at the first lesson still needs no --seed")


def seed_case_applied_and_logged() -> None:
    """A seeded run copies the workspace in, skips the course, and says so."""
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        prepared = learner_workspace(ws.path("prepared"))
        (prepared / "src" / "answer.txt").write_text("42\n", encoding="utf-8")
        # A seed carrying its own course must not overwrite the instance's.
        plant_lesson(prepared, "tutorial/lessons/00-first-steps.md")
        (prepared / "tutorial" / "STATE.md").write_text("---\nfake: true\n---\n", encoding="utf-8")
        log = ws.path("run.jsonl")
        done = run(
            DRYRUN, instance,
            "--from", LESSON_01,
            "--seed", prepared,
            "--mirror", ws.path("mirror"),
            "--log", log,
            "--agent-command", STUB_AGENT,
            "--max-turns", "2",
            "--stall-after", "9",
            env=cli_env(
                ws.path("tripwire.txt"),
                DRYRUN_STUB_ARGV=str(ws.path("argv.jsonl")),
                DRYRUN_STUB_TOUCH="src/second.txt",
                DRYRUN_STUB_COMPLETE_AFTER="2",
            ),
        )
        check(done.returncode == 0, f"the seeded run exits 0 (got {done.returncode}):\n{done.output}")
        check(
            (instance / "src" / "answer.txt").read_text(encoding="utf-8") == "42\n",
            "the seed's learner files are in the instance",
        )
        check(
            "fake: true" not in (instance / "tutorial" / "STATE.md").read_text(encoding="utf-8"),
            "a seed carrying its own course NEVER overwrites the instance's course",
        )
        records = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
        start = [r for r in records if r["kind"] == "run-start"][0]
        check(start["seed"] == str(prepared), "the run log records which workspace seeded the run")
        check(
            start["seeded_files"] >= 2,
            f"and how many files it brought (got {start.get('seeded_files')})",
        )
        # The control: an unseeded run records a null seed, so a reader can
        # tell a walked run from a seeded one.
        log2 = ws.path("run2.jsonl")
        run(
            DRYRUN, instance,
            "--from", LESSON_00,
            "--mirror", ws.path("mirror2"),
            "--log", log2,
            "--agent-command", STUB_AGENT,
            "--max-turns", "1",
            "--stall-after", "9",
            env=cli_env(
                ws.path("tripwire2.txt"),
                DRYRUN_STUB_ARGV=str(ws.path("argv2.jsonl")),
                DRYRUN_STUB_COMPLETE_AFTER="1",
            ),
        )
        records = [json.loads(line) for line in log2.read_text(encoding="utf-8").splitlines()]
        start = [r for r in records if r["kind"] == "run-start"][0]
        check(start["seed"] is None, "an unseeded run records a null seed")


# --------------------------------------------------------------------------
# 7. The validator probe
# --------------------------------------------------------------------------


def validator_case_probes_and_unprobeables() -> None:
    with Workspace() as ws:
        instance = ws.copy(INSTANCE_FIXTURE)
        manifest, _text = dryrun.bl.load_manifest(instance / "tutorial")
        probe = dryrun.CommandValidators(instance, manifest)
        lessons = {l.rel: l for l in dryrun.read_lessons(instance / "tutorial")}

        before = probe.state(lessons[LESSON_00])
        check(before.passing == frozenset(), f"nothing passes yet (got {set(before.passing)})")
        check(
            before.probed == frozenset({"has-answer", "reads-back"}),
            f"both of lesson 00's validators are probeable (got {set(before.probed)})",
        )
        (instance / "src").mkdir(exist_ok=True)
        (instance / "src" / "answer.txt").write_text("42\n", encoding="utf-8")
        after = probe.state(lessons[LESSON_00])
        check(
            after.passing == frozenset({"has-answer", "reads-back"}),
            f"both pass once the file is there (got {set(after.passing)})",
        )
        check(after.advanced_over(before), "that counts as validator progress")
        check(not after.advanced_over(after), "and running twice with no change does not")

        manual = probe.state(lessons[LESSON_01])
        check(
            "by-hand" in manual.unprobeable,
            f"a manual validator is UNPROBEABLE, not failing (got {set(manual.unprobeable)})",
        )
        check(
            "by-hand" not in manual.probed,
            "so it never contributes progress, and the log says which were probed",
        )


# --------------------------------------------------------------------------


def main() -> int:
    print(f"dryrun.py:  {DRYRUN}")
    print(f"stub agent: {STUB_AGENT}")
    print(f"cost:       {COST} - this suite spends no tokens")
    print()

    if not os.access(STUB_AGENT, os.X_OK):
        print(f"FATAL: {STUB_AGENT} is not executable; the CLI cases cannot run.")
        return 2
    if not os.access(TRIPWIRE_BIN / "claude", os.X_OK):
        print(f"FATAL: {TRIPWIRE_BIN / 'claude'} is not executable; the tripwire cannot fire.")
        return 2

    with case("an ordinary learner mirror passes the guard"):
        guard_case_clean()
    with case("an empty tutorial/ directory fires the guard"):
        guard_case_tutorial_dir()
    with case("a lesson planted under an innocent name fires the guard"):
        guard_case_planted_lesson()
    with case("a lesson stripped of its frontmatter still fires the guard"):
        guard_case_stripped_lesson()
    with case("the learner's own notes do not fire the guard"):
        guard_case_near_miss()
    with case("sync_to_mirror never copies course material"):
        guard_case_sync_never_copies_course()
    with case("sync_to_mirror never copies the run log"):
        guard_case_sync_excludes_the_log()
    with case("a breach aborts the run before the learner turn"):
        guard_case_run_aborts()

    with case("the accounting parses a real-shaped payload"):
        seam_case_parse_usage()
    with case("a payload with no usage records nulls, never zeros"):
        seam_case_missing_usage_is_null_not_zero()
    with case("stdout that is not JSON is refused"):
        seam_case_refuses_garbage()
    with case("the CLI argv asks for JSON and resumes only when told to"):
        seam_case_argv()

    with case("the stall detector fires on consecutive quiet turns"):
        stall_case_fires()
    with case("the stall detector does not fire on a learner who is working"):
        stall_case_does_not_fire()
    with case("the stall report localises and never rules"):
        stall_case_no_verdict_wording()
    with case("a driven run stops at the stall threshold"):
        stall_case_in_a_run()
    with case("the same run with a working learner never stalls"):
        stall_case_working_learner()

    with case("the tutor starts cold every turn and the learner resumes"):
        session_case_tutor_cold_learner_warm()
    with case("the run log carries what a cost decision needs"):
        session_case_log_fields()

    with case("a stubbed run never reaches the real claude"):
        cli_case_never_runs_claude()
    with case("no tutor process is ever given --resume"):
        cli_case_tutor_never_resumes_over_the_cli()
    with case("the learner's directory holds no course after a whole run"):
        cli_case_learner_cwd_has_no_course()
    with case("--plan spends nothing"):
        cli_case_plan_spends_nothing()

    with case("the default range is one lesson, the active one"):
        range_case_default_is_one_lesson()
    with case("--from and --to select an inclusive range"):
        range_case_from_to()
    with case("a bundle is refused, an instance is accepted"):
        range_case_not_an_instance()

    with case("--from past the first lesson requires --seed"):
        seed_case_unit_rule()
    with case("the CLI refuses a seedless --from and allows a seeded one"):
        seed_case_cli_refuses()
    with case("a seeded run copies the workspace in, skips the course, and logs it"):
        seed_case_applied_and_logged()

    with case("the validator probe separates unprobeable from failing"):
        validator_case_probes_and_unprobeables()

    note("no `claude` process was started: the tripwire on $PATH was watched firing "
         "in its positive control and stayed silent in every other case.")
    return report("test_dryrun.py")


if __name__ == "__main__":
    sys.exit(main())
