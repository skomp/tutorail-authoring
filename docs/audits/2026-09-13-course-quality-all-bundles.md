# Course-quality audit, 2026-09-13 — every bundle in `skomp/tutorail-bundles`

Five courses, audited against `skills/course-quality/references/rubric.md` as it stands
today. The repository was at `4df2624` and **no bundle was changed**: everything below is a
proposal the author accepts or refuses.

One auditor per bundle, each running the `course-quality` skill: `audit.py` for evidence,
then every lesson opened and scored element by element. The full six-section report for
each course is in `2026-09-13/`, and the per-element evidence — `file:line` plus the
sentence scored — lives there. This file is the index, not a substitute for it.

| Course | Report |
|---|---|
| `durable-event-broker` | [`2026-09-13/durable-event-broker.md`](2026-09-13/durable-event-broker.md) |
| `portable-bytebeat-wav` | [`2026-09-13/portable-bytebeat-wav.md`](2026-09-13/portable-bytebeat-wav.md) |
| `portable-fixed-window-rate-limiter` | [`2026-09-13/portable-fixed-window-rate-limiter.md`](2026-09-13/portable-fixed-window-rate-limiter.md) |
| `rust-automaton-db` | [`2026-09-13/rust-automaton-db.md`](2026-09-13/rust-automaton-db.md) |
| `webgl-typescript-scene` | [`2026-09-13/webgl-typescript-scene.md`](2026-09-13/webgl-typescript-scene.md) |

> ## OPEN QUESTION, raised the same day — is a project skeleton toil?
>
> Four of these five reports rejected a create-the-project step with the same words, "the
> bundle could not have supplied the result", and scored it +2, +1, +1 and 0. A learner had
> already voted the other way twice: `skomp/tutorail-bundles#3` records them saying *"can you
> create the base setup for me, there is no learning in that"* and changing
> `ownership_policy` in their own instance so the tutor would do it.
>
> The rubric is the reason the four auditors went the other way. It carries two tests that
> disagree for a skeleton — *could the bundle have shipped the result?* (yes: a skeleton is a
> handful of files, and a portable bundle can ship one set per supported language) and
> *setup that needs the network, a toolchain or an account is the learner's work* (also yes:
> `go mod init` needs the toolchain). `npm install` is unambiguous under both. A skeleton is
> not.
>
> **Neither instrument detects the gap.** The validator does not require a `supplies:` entry,
> the toil scanner has no pattern for it, and the rubric told each auditor to reject the
> candidate. The learner found it; the tooling did not.
>
> If the author rules the step toil: rate limiter **32** not 35, bytebeat **50** not 54,
> broker **128** not 132, rust **353** not 355. Nothing is re-scored here — the ruling is the
> author's, and each report states the consequence beside the element it affects. Filed as
> `tutorail-authoring#11`.

## The totals are not a league table

The rubric says a lesson's figure tracks how finely its `## Suggested progression`
enumerates clauses, so two courses with different house styles are not measured with the
same ruler. **Every total below is comparable only against its own course's lessons.**
`rust-automaton-db` scores 355 and `portable-bytebeat-wav` scores 54 because one has 23
lessons and the other has 5, not because one teaches better.

| Course | Lessons | Lesson sum | Course-level penalties | Total | Declining every offer |
|---|---|---|---|---|---|
| `durable-event-broker` | 15 + 3 optional | 132 | none | **132** | 112 |
| `portable-bytebeat-wav` | 4 + 1 optional | 57 | −3 (1 unserved objective) | **54** | 44 |
| `portable-fixed-window-rate-limiter` | 3 + 1 optional | 35 | none | **35** | 27 |
| `rust-automaton-db` | 23 + 0 optional | 370 | −15 (5 unserved topics) | **355** | 355 |
| `webgl-typescript-scene` | 18 + 1 optional | 260 | none | **260** | 243 |

Across 69 scored lessons there are **three confirmed toil sites** and **six unserved
goals**. No course has a `required_for` gate on an optional lesson, so that −3 row fires
nowhere and its warning is printed nowhere.

## What each course owes

### `durable-event-broker` — 132, nothing owed at course level

15/15 anchors, 26/26 coverage topics and 69/69 lesson objectives are served, and the
auditor found no toil. The findings are about threads that are carried but never pulled:
the append timestamp is introduced at `02:42` and first used twelve lessons later at
`14:46`, and lesson 00's sharpest teaching — byte-slice ownership — has no `DESIGN.md`
anchor that answers it. Three coverage topics are taught only by optional lessons; the
course argues that case itself at `COURSE.md:95-97`, and the auditor accepts it except for
TCP, which `#transport-boundary` treats as first-class.

### `portable-bytebeat-wav` — 54, and one real defect

The defect is not a score. `lessons/03-compose-and-export.md:59` tells the tutor to make
the stereo offer **before the first required task**, and the stereo lesson converts the
writer to two channels (`stereo-bytebeat.md:46`), while lesson 03's completion condition
requires **mono** `output.wav` (`03:67`). A learner who accepts the offer cannot finish the
lesson. `tutorial.yaml:49` only checks that `output.wav` exists, so the validator stays
green through the whole conflict — the green-validator-and-bad-course case this skill
exists for.

The −3 is `lessons/03-compose-and-export.md:23`, "Distinguish the authored course from
environment-specific extensions": no task depends on the distinction.

### `portable-fixed-window-rate-limiter` — 35, the tightest course in the repository

Every objective, every coverage topic and every anchor is served, with no toil and no
gaps, in four lessons of 73 to 78 lines. Its open question is `concurrency safety`
(`COURSE.md:57`), which only the optional `concurrent-callers.md` teaches: a learner who
declines never learns that their limiter is unsafe to share. The rubric makes that a
question and not a score, deliberately.

### `rust-automaton-db` — 355, five coverage topics owed

Five topics the course names and no lesson exercises: **interior mutability**
(`COURSE.md:248`), **atomics** (`:250`), **associated types** (`:242`), **Cargo
workspaces** (`:267`) and **refactoring across crate boundaries** (`:269`). Verified
independently: `interior mutab|RefCell` matches nothing in any lesson, and `atomics`
appears once, in a concepts list at `12:36`, with no clause requiring one.

One confirmed toil site, `22-hardening-performance.md:63` "Build CI and reproducible
clusters" — the CI half is a file the bundle could ship.

The structural finding is a seam: lessons 00-04 average 109 lines with named prerequisites
and bespoke deeper paths, and lessons 05-22 average 74 lines with the placeholder
prerequisite "The preceding course lesson." and one boilerplate sentence repeated 18 times.

### `webgl-typescript-scene` — 260, and the repair of `49af681` holds

Lesson 14 is genuinely optional now: it sits in `optional_lessons:`, its prose agrees, and
the completability invariant holds. The dropped objective left no dangling references. The
rubric's worked figures of 194 and 183 describe the pre-repair bundle and are superseded by
260 and 243; do not compare them.

Both confirmed toil sites are the same omission — the bundle declares **zero `supplies:`
entries** while shipping nine workspace-bound files, so it assigns two copy instructions
(`00-project-setup/LESSON.md:34` and `13-load-gltf-model/LESSON.md:39`) that
`supplies.py` could hand over. That is what puts lesson 00 at **−1**, the only negative
lesson in the repository.

## Two things that are about the tooling, not the courses

**`audit.py` silently reports no coverage list for `rust-automaton-db`.** The 46 topics at
`COURSE.md:225-271` are inside a fenced ` ```text ` block and the parser reads Markdown
list items only, so `coverage_list.topics` comes back `[]`. That is indistinguishable from
a course that declared no boundary, and taken at face value it hides all five gaps above.
Filed as `tutorail-authoring#10`.

**The toil scanner found 5 candidates across 69 lessons and 3 of the 5 were false
positives; 2 of the 3 confirmed sites it never saw.** Its silence is evidence about its
verb list, exactly as the skill says. Every figure here came from opening the lessons.

## What no one ran

No dry-run. `dryrun.py` walks a course with an agent playing the learner, which is five
full courses of work, and nothing in this report rests on a stall.

## Where the findings are tracked

One issue per bundle, in `skomp/tutorail-bundles`, plus the tooling defect here:

| Issue | Covers |
|---|---|
| `tutorail-bundles#5` | `portable-bytebeat-wav` — the stereo offer blocks lesson 03 |
| `tutorail-bundles#6` | `webgl-typescript-scene` — two toil sites, no `supplies:` entries |
| `tutorail-bundles#7` | `rust-automaton-db` — five coverage topics with no task |
| `tutorail-bundles#8` | `durable-event-broker` — three unused threads made load-bearing |
| `tutorail-bundles#9` | `portable-fixed-window-rate-limiter` — the retention anchor, and where concurrency safety belongs |
| `tutorail-authoring#10` | `audit.py` does not read a fenced coverage list |
| `tutorail-authoring#11` | the rubric does not settle whether a project skeleton is toil, and nothing detects the missing setup |
| `tutorail-bundles#3` | the field report that raised it — per-language setup for the two portable bundles |
