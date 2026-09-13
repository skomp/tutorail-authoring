# Dry-run harness — checkpoint, 2026-09-12

Issue: skomp/tutorail-authoring#5. Read the issue first; it carries measured facts about
`claude -p` that must not be re-derived.

This file exists so the work can continue without the session that started it.

---

## What exists and is done

**Phase 1 is built, tested, committed and costs nothing to run.**

- `skills/course-quality/scripts/dryrun.py` — the driver.
- `tests/test_dryrun.py` — 30 cases, 133 assertions, `COST = "cheap"`.
- Commits `60136f3`, `6b9bb26`, `1a1297f`.

It never starts a `claude` process. Every test drives a stub behind one seam, and a test
asserts that no real agent is invoked when the seam is stubbed.

What phase 1 does:

- **Structural isolation.** The tutor works in the instance directory, which holds
  `tutorial/`. The learner works in a mirror that never holds it. Files sync back after each
  turn. Before every learner turn the harness asserts the mirror carries no lesson, and
  aborts if it does. This is enforcement, not instruction — "do not read ahead" in a prompt
  is unverifiable, and an agent that has read the lesson cannot play the learner.
- **Cost accounting.** One JSON line per turn: role, lesson, turn number, session id, input
  and output tokens, duration. This is the input to any later decision about how often the
  harness earns its cost.
- **Stall detection**, reported and never diagnosed.
- **Cold tutor every turn**, resumable learner.
- `--from` / `--to`, defaulting to one lesson.

**`--from` past the first lesson requires `--seed <path>`.** To start at lesson 10 the
workspace must already hold what lessons 0 to 9 built. Without the seed the learner meets
lesson 10 with none of the code it assumes, every completion condition fails, and the
harness reports a course defect it manufactured itself. The refusal has a test and a
control.

Open question recorded in the run log rather than solved: a seeded workspace was built by
someone who had read the lessons, so a seeded run tests a different thing from a walked run.

---

## Settled by Robert, 2026-09-12

### A finding is a claim about the course. A stall is evidence.

When a learner fails to finish a lesson, two causes look identical from outside: the course
is broken, or the learner agent is bad at the subject.

**The harness reports a defect only when it can point at the course itself** — for example,
lesson 07's completion condition names a symbol that no earlier lesson introduces. That is
true whether the learner was excellent or hopeless.

Everything else is a **stall**: localised to a lesson and a turn, reported with the log,
never adjudicated by the tool.

Two alternatives were considered and rejected, both for the same reason. Running one lesson
with five learners and calling five stalls a defect, or running a strong learner against a
weak one, each end by asserting something about learner ability that nothing can verify.
An unverifiable claim presented as a finding is the failure this project met repeatedly on
2026-09-12.

**The accepted cost:** the harness will never say "lesson 07 is too hard". It says "the
learner did not get past 07, here is what happened", and the judgement stays with a person.

---

## The open question, which gates phase 2

**If a finding must hold regardless of learner skill, most findings need no learner.**

"Lesson 07 names `computeNormals()` and no earlier lesson mentions normals" is two greps
over the lesson files. `audit.py` could find it today, free, across all five courses.

The dynamic run adds exactly one thing that static reading cannot reach: **the tutor's task
text does not exist until the tutor writes it.** A lesson says "Suggested progression:
acquire the context, resize the buffer, clear it". The task actually handed to the learner
is improvised from that, cold, every turn. If the tutor asks for something the course never
taught, that is a real defect and no amount of reading the bundle will find it, because the
sentence was never written by the author.

Three options were put to Robert and the answer was not recorded before the session ended:

1. **Static first.** Build the learner-independent checks into `audit.py`, free, run them
   across five courses, and build the harness only for what is left. The count of what
   remains is the number that should decide whether phase 2 is built at all. Also serves
   issues #3 and #4.
2. **Build the harness now**, accepting that some of what it finds was findable for nothing.
3. **Drop the harness** and invest in static analysis alone.

The recommendation on the table was 1, with its risk stated: it can become an excuse never
to build the harness, and the tutor-improvisation gap is real.

**Resume here.**

---

## Also unresolved, and smaller

- **Lesson completion depends on the tutor emitting `LESSON COMPLETE`** — a convention this
  harness invented, which the runner skill does not speak. So the harness would be testing a
  tutor following a protocol no real tutor follows. The proposal on the table is to detect
  completion from `STATE.md`, which the runner genuinely maintains, and which needs no change
  in another repository.
- `--agent-arg` applies to both roles, so the tutor inherits the learner's permission mode
  when it only needs to read.
- `skills/course-quality/SKILL.md` has no entry for `dryrun.py`.

---

## Before the first token is spent

The issue says to measure one lesson before running a course. Nineteen lessons times several
turns times two sessions is hundreds of invocations against one subscription.

The command, which has never been run:

```
python3 skills/course-quality/scripts/dryrun.py <instance> \
    --mirror /tmp/dryrun-learner --log /tmp/dryrun-run.jsonl \
    --max-turns 3 --stall-after 2 \
    --agent-arg --permission-mode --agent-arg acceptEdits
```

`--plan` prints the plan and spends nothing. `--max-turns 3` caps a run at six invocations.
Drop `--from`/`--seed` to walk an instance from where its own `STATE.md` says the learner is.

---

## Traps that cost time on 2026-09-12

- **Pin the whole runner scripts directory**, never one file. `validate_bundle.py` imports
  `yamlite` and `catalogs` from beside itself. A single-file pin cannot run and fails in a
  way that reads as product defects. The tell is `FAIL - 0 finding(s)`.
- **`grep` here is ugrep 7.8.4.** Under `-E`, a digit class mixed with `\b` silently matches
  nothing and exits 1, which is indistinguishable from an honest zero. Use `-P`, and plant a
  positive control before believing any zero.
- **`git commit` commits the whole index**, not the paths you just added. An agent's own
  `git add` lands in the same index. Run `git status --short` between staging and committing.
