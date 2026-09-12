# Dry-run harness, phase 1

Date: 2026-09-12. Commit: `60136f3`. Issue: skomp/tutorail-authoring#5.

Status: **done and green**. `python3 tests/run_all.py` passes all 11 suites.
`tests/test_dryrun.py` contributes **133 assertions** across 30 cases and declares
`COST = "cheap"`. **No `claude -p` process ran at any point in this work.**

## What was built

| Path | What it is |
|---|---|
| `skills/course-quality/scripts/dryrun.py` | the driver, the isolation guard, the accounting, the stall detector |
| `tests/test_dryrun.py` | 30 cases, 133 assertions, stdlib only, no pytest |
| `tests/fixtures/dryrun-instance/` | a two-lesson materialized instance: `tutorial/` plus learner files |
| `tests/fixtures/dryrun-stub-agent.py` | a stand-in for `claude -p --output-format json` |
| `tests/fixtures/dryrun-tripwire-bin/claude` | a tripwire that records being reached |
| `tests/harness.py` | one line: `DRYRUN = QUALITY_SCRIPTS / "dryrun.py"` |

`tests/run_all.py` needed no edit; it globs `test_*.py`.

## The structural isolation

The instance is a learner workspace with the course in `<instance>/tutorial/`, so by
default the lessons sit in the learner's own directory. The harness therefore runs the
two roles in two different directories:

- the **tutor**'s cwd is the instance, where `tutorial/` is;
- the **learner**'s cwd is a **mirror** built by `sync_to_mirror()`, which never copies
  anything `is_course_material()` calls course material, and never copies the run log
  (which holds every task the tutor has written so far);
- after each learner turn `sync_from_mirror()` puts the learner's work back into the
  instance, so the tutor sees it on its next cold start;
- `assert_learner_isolated()` runs **before every learner turn** and raises
  `IsolationBreach`, which aborts the run. It is not a warning and not a log note. A run
  that continued past a breach would produce numbers indistinguishable from honest ones.

The guard uses **two independent signals**, because a name check alone is defeated by a
rename and a content check alone is defeated by an empty `tutorial/` that a later turn
fills in:

1. path names — `tutorial/`, `lessons/`, `tutorial.yaml`, `COURSE.md`, `DESIGN.md`,
   `STATE.md`, `LESSON.md`;
2. content — `looks_like_a_lesson()` fires on lesson frontmatter (`id` plus
   `design_refs`/`validators`/`learning_objectives`) **or** on two or more lesson body
   headings.

Its limit is stated in the source: this stops an accident and the obvious rename. It does
not stop someone who is trying.

## A range that does not start at lesson 0 needs a seed

Added after the coordinator closed a hole a reviewer had raised, and it was a real one.

To start a run at lesson 10, the workspace must already hold everything lessons 0 to 9
build. There are two honest ways to get there and there is no third:

1. walk from lesson 0, paying the tokens of every lesson you are not testing;
2. start from a workspace someone prepared, handed over with `--seed <path>`.

So **`--from` naming anything but the course's first lesson refuses without `--seed`**,
and the refusal says why:

> `lessons/01-second-steps.md` is not the first lesson of this course, so this run needs
> `--seed <path>` [...] Starting it against a workspace that does not hold what it assumes
> makes every completion condition fail for a reason that has nothing to do with the
> course. The harness would then report a course defect that is entirely an artefact of how
> the run was started, which is worse than reporting nothing.

The check runs before `--plan` too: a plan for a run that would manufacture its own
findings is not a plan worth printing.

A run with **no** `--from` is not affected. It walks the instance from where its own
`STATE.md` says the learner is, and that workspace holds the earlier lessons' work because
the learner did it. `--from` is the caller *overriding* where the run starts, so the burden
of saying where the state came from is the caller's.

`apply_seed()` copies the seed's learner files into the instance and **skips course
material**: the instance's own `tutorial/` is the course of record, and a seed carrying its
own copy would quietly become the thing under test. That is tested with a seed that
deliberately carries a `tutorial/STATE.md`.

### Open question for the spec — recorded, not solved

**A seeded workspace was built by someone who had read the lessons, so a run starting from
one is testing a different thing from a run walked from lesson 0.** That difference has to
be stated wherever a finding from a seeded run is reported.

No mechanism for it was built, deliberately. What exists is the evidence a reader needs to
tell the two apart: the `run-start` record carries `seed` (the path, or `null`) and
`seeded_files` (how many files it brought), and a test asserts that an unseeded run records
`null` so the distinction cannot be lost by accident. Deciding what a report must say about
a seeded finding belongs to the spec, not to this script.

## Guards watched failing before they passed

Each was broken deliberately in a working copy, the suite was run, the break was reverted,
and `dryrun.py` was diffed byte-for-byte against the pre-break copy afterwards.

The assertion totals in breaks 1 to 3 below are lower than 133 because those runs were made
before the `--seed` cases existed. They are verbatim transcripts, not recounted figures.

### 1. The isolation guard, with the content sniff removed

Replaced `reason = looks_like_a_lesson(text)` with `reason = None`. Six assertions failed,
and the last two are the ones that matter:

```
FAILED - test_dryrun.py: 8 of 113 assertions:
  - a lesson planted as notes/reading.md fires the guard (got [])
  - the finding says WHY it is a lesson (got [])
  - assert_learner_isolated raises on a planted lesson
  - a lesson body with no frontmatter still fires the guard
  - the finding names the body headings (got [])
  - the SAME file with a second lesson heading added does fire - so the first
    result was the sniff deciding, not the sniff being blind
  - a planted lesson aborts the whole run
  - the learner turn never happens after a breach
    (calls: ['tutor', 'learner', 'tutor', 'learner', 'tutor', 'learner'])
```

The last line is the failure worth reading: with the sniff gone, the run completed **three
learner turns with a real lesson sitting in the learner's own directory**. That is exactly
the worthless run the whole design exists to prevent, and the guard is what stops it.

### 2. The stall detector, with the quiet counter disabled

Replaced `self.count += 1` with `self.count = 0`:

```
FAILED - test_dryrun.py: 7 of 107 assertions:
  - three quiet turns at threshold 3 is a stall
  - a stall produces a report
  - the SAME detector does fire when both signals stay quiet
  - a learner who changes nothing produces a stall
  - one stall record is logged (got 0)
  - the run stops at the threshold (learner turns: 6)
```

### 3. The tutor's cold start, and the accounting's refusal to invent zeros

Two breaks at once — the tutor given `resume=self.learner_session`, and `_int_or_none`
returning `0` instead of `None`:

```
FAILED - test_dryrun.py: 5 of 114 assertions:
  - a missing input_tokens is None, not 0 (got 0)
  - a missing output_tokens is None, not 0
  - the log line carries null, not 0
  - the tutor is started cold on every turn
    (resumes: [None, 'stub-learner-session', 'stub-learner-session'])
  - no tutor process is ever given --resume
```

The last one is the argv-level check: it reads the stub agent's argv log, so it proves the
property where it is observable rather than where the driver believes it.

### 4. The seed rule, disabled

An early `return` at the top of `require_seed`:

```
FAILED - test_dryrun.py: 3 of 130 assertions:
  - --from lessons/01 with no --seed is refused
  - the CLI refuses --from 01 with no --seed (exit 0)
  - the CLI refusal names --seed
```

`exit 0` is the failure to read: with the rule off, `--from lessons/01` against a workspace
holding none of lesson 00's work was accepted and would have run.

### 5. The tripwire, watched firing on every run

`cli_case_never_runs_claude` does not need breaking, because its positive control fires
every time the suite runs. A tripwire named `claude` goes first on `$PATH`; a full run
with `--agent-command <stub>` must leave the sentinel absent, and then **the same
invocation without `--agent-command` must create it**. Without that second half, "the
sentinel is absent" would be a negative from an instrument nobody had tested.

`verdict_language()` has the same shape: the stall report's own wording must produce no
hits, and the same probe must fire on `"lesson 00 has an unsatisfiable completion
condition. The lesson is wrong."`.

## The stall detector reports and never diagnoses

A stall is N consecutive learner turns (`--stall-after`, default 3) in which the mirror's
`tree_digest` does not change **and** no validator that was failing starts passing. The
report localises: lesson, first quiet turn, last turn, quiet count, threshold, and the last
task verbatim. It then carries `STALL_DISCLAIMER`:

> A stall cannot distinguish an unsatisfiable completion condition from a learner having a
> bad run. This harness localises a stall and does not rule on one. The ruling stays with
> whoever reads this log.

The heading reads `STALL REPORT - a localisation, not a finding`. Exit code 3 means "the
run stopped early and a stall report was written", and the `--help` epilog says in words
that this is not a verdict.

One honest limit, tested and documented: the report quotes the tutor's task verbatim, so a
task that says "fix the broken parser" puts the word "broken" in the report. The probe
covers the harness's own words, not the tutor's.

## The accounting

One JSON line per event, flushed and fsynced as it happens, so a killed run still accounts
for every turn it paid for. Kinds: `run-start`, `turn`, `stall`, `run-end`.

A `turn` record carries `turn`, `role`, `lesson`, `session_id`, `resumed`, `input_tokens`,
`output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`,
`usage_present`, `total_cost_usd`, `duration_ms`, `wall_ms`, `num_turns`, `is_error`,
`text_chars`, `run_id`, `course` — and for a learner turn also `workspace_changed`,
`validators_passing`, `validators_probed`, `validators_unprobeable` and `quiet_turns`.

Two deliberate choices:

- **A missing usage object records `null`, never `0`.** A zero is a number someone would
  add up. The parser refuses outright on stdout it cannot parse rather than defaulting.
- **`validators_probed` is recorded separately from `validators_passing`.** A `kind:
  manual` or `kind: git-diff` validator cannot be probed, so it can never contribute
  progress. Without the `probed` field, a lesson whose only validator is manual would be
  indistinguishable in the log from a learner who is genuinely stuck.

## The decisions from the issue

- **Decision 1 — the tutor starts cold every turn.** `resume=None` is passed at the one
  call site, and the argv-level test reads the stub's argv log to prove no tutor process
  ever receives `--resume`. The learner resumes, because a learner carries context; the
  learner's session is dropped between lessons.
- **Decision 2 — a run is limited to a lesson range.** `--from` / `--to`, inclusive,
  resolvable by path, filename, slug or id. **The default is one lesson**: `STATE.md`'s
  `active_lesson` when there is one, otherwise the first. `--to` before `--from` is
  refused by name, and `--from` past the course's first lesson is refused without
  `--seed` (see above).
- **Decision 3 — how a stall is detected.** As above: no workspace change and no validator
  progress for N consecutive learner turns.

## What phase 1 deliberately does not have

- **No real `claude -p` run.** That is phase 2 and needs the owner's approval.
- No report renderer and no multi-lesson orchestration beyond walking the range in order.
- A file the learner **deletes** in the mirror is not deleted in the instance. Creations
  and edits sync both ways; deletions do not.
- Lesson completion is signalled by the tutor emitting `LESSON COMPLETE`. That is a
  convention this harness asks for in its prompt, not something the runner skill emits
  today. It is the most likely thing to need changing on the first real run.
- `--agent-arg` applies to both roles, so a permission mode given for the learner is also
  given to the tutor. The tutor only needs to read; a read-only tutor is a phase-2
  refinement.
- `skills/course-quality/SKILL.md` has no entry for `dryrun.py` yet. Its "Where a dry-run
  harness has walked the course" paragraph already anticipates one. That edit was outside
  this task's file ownership.

## The first real turn

**Not run.** This is the command, and it spends tokens.

First, see the plan for free — this calls no agent:

```bash
python3 skills/course-quality/scripts/dryrun.py \
    ~/src/github.com/skomp/<the-instance> --plan
```

Then the first real turn, one lesson, a pinned mirror and log, and a low turn cap so the
cost of one lesson is measured before a course is:

```bash
python3 skills/course-quality/scripts/dryrun.py \
    ~/src/github.com/skomp/<the-instance> \
    --from lessons/04-richer-typed-schemas.md \
    --seed ~/src/github.com/skomp/<the-prepared-workspace> \
    --mirror /tmp/dryrun-learner \
    --log /tmp/dryrun-run.jsonl \
    --max-turns 3 \
    --stall-after 2 \
    --agent-arg --permission-mode --agent-arg acceptEdits
```

Before running it:

- `--from` past the course's first lesson **requires** `--seed`. Drop both flags to walk
  the instance from where its own `STATE.md` says the learner is, which needs no seed.
- A finding from a seeded run must be reported as coming from a seeded run. See the open
  question above.
- `--mirror` must be **outside** the instance; the script refuses otherwise.
- `--max-turns 3` is the cost cap. Three turns is six agent invocations at most.
- Read `/tmp/dryrun-run.jsonl` afterwards. `input_tokens` plus `output_tokens` per turn,
  and `wall_ms`, are what the "is this worth running" decision needs.
- Exit 3 means a stall report was written. It is a localisation. It is not a verdict on
  the lesson.
