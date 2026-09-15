# Course-quality audit, 2026-09-13 — every bundle in `skomp/tutorail-bundles`

> **SUPERSEDED on 2026-09-15.** The catalogue changed after this audit: five of its six
> confirmed toil sites were repaired, two portable bundles moved their setup step to the
> tutor, and two bundles began shipping a skeleton. The current audit is
> [`2026-09-15-course-quality-all-bundles.md`](2026-09-15-course-quality-all-bundles.md).
>
> This report stays as the audit of record for `skomp/tutorail-bundles` as it stood on
> 2026-09-13, and for the project-skeleton ruling made that day. Its figures are correct for
> the files it audited and are **not** current. Its `file:line` citations have moved.


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

> ## RULED 2026-09-13 — a project skeleton is toil
>
> ### What was asked, kept so the ruling can be read against it
>
> Four of these five reports rejected a create-the-project step with the same words,
> "the bundle could not have supplied the result", and scored it +2 (broker), +2
> (bytebeat), +1 (rate limiter) and 0 (rust). A learner had already voted the other way
> twice: `skomp/tutorail-bundles#3` records them saying *"can you create the base setup
> for me, there is no learning in that"* and changing `ownership_policy` in their own
> instance so the tutor would do it.
>
> The rubric was the reason the four auditors went the other way. It carried two tests that
> disagree for a skeleton — *could the bundle have shipped the result?* (yes: a skeleton is a
> handful of files, and a portable bundle can ship one set per supported language) and
> *setup that needs the network, a toolchain or an account is the learner's work* (also yes:
> `go mod init` needs the toolchain). `npm install` is unambiguous under both. A skeleton was
> not, and the rubric did not say which test wins.
>
> **Neither instrument detected the gap.** The validator does not require a `supplies:` entry,
> the toil scanner has no pattern for it, and the rubric told each auditor to reject the
> candidate. The learner found it; the tooling did not. **That half of
> `tutorail-authoring#11` is still open**: the ruling settles the rubric question and not the
> detection question, and nothing in the toolkit yet finds a missing skeleton on its own.
>
> ### What the author ruled
>
> **When the two tests disagree, the shippability test wins. A project skeleton is toil.**
> The shippability question is asked in its full form — not *"could the bundle have shipped
> one file?"* but *"could the bundle have shipped one set of files for each language the
> course supports?"* A portable bundle can, with the tutor selecting the set after the
> learner selects the language. `npm install` is unaffected and stays the learner's work,
> because `node_modules` cannot ship under any language.
>
> **The exception:** the setup is teaching, not toil, when the course's own objectives make
> the setup the subject. An objective that merely *names* the setup is not enough; the test
> is operational — **is the setup step the ONLY element serving the objective that names
> it?** If it is, supplying the result would strand that objective at −3, so the step scores
> as what it teaches.
>
> **The ruling lives in `skills/course-quality/references/rubric.md`**, section *"A project
> skeleton is toil — the tiebreak, ruled 2026-09-13"*, which carries a worked table of all
> five bundles built by enumerating elements. That section is the authority; this block
> records only what was open, why, and how it closed.
>
> ### Which courses moved, and which did not
>
> Every report was re-checked element by element against the ruling and every one is now
> final. The exception fired **once in five**.
>
> | Course | Setup element | Servers | Ruling | Total |
> |---|---|---|---|---|
> | `rust-automaton-db` | `00:76` | **1** | **exception** — not toil | 355, **unchanged** |
> | `durable-event-broker` | `00:53` | 4 | toil, +2 -> −2 | 132 -> **128** |
> | `portable-bytebeat-wav` | `00:57` | 4 | toil, +2 -> −2 | 54 -> **50**, and see below |
> | `portable-fixed-window-rate-limiter` | `00:51-52` | 4 | toil, +1 -> −2 | 35 -> **32** |
> | `webgl-typescript-scene` | `00:34` | — | already toil before the ruling | 260, **unchanged** |
>
> `webgl-typescript-scene` never reached the tiebreak: its skeleton ships as `starter/`
> files, so the plain shippability test already answered yes and the copy instruction was
> scored toil at first publication. The question above predicted rate limiter 32, bytebeat
> 50, broker 128 and rust **353**; three of the four held, and rust did not move, because it
> is the one bundle whose setup objective is sole-served.
>
> ### Two figures below moved for reasons that are NOT the ruling
>
> - **`portable-bytebeat-wav`: the ruling accounts for 54 -> 50 and no more.** The further
>   50 -> **48** is a **pre-existing addition error**, exposed by re-adding every element to
>   check the ruling's effect: lesson 01's eleven rows sum to 10 and were published as 12.
>   No element score was changed to reach it. Its report sets this out under lesson 01,
>   including the one reading that would restore 12.
> - **`portable-fixed-window-rate-limiter` also corrected a pre-existing miscount**, "17 of
>   36 elements are teaching" to **16 of 36**. It moves no total, but it was wrong at first
>   publication.

## The totals are not a league table

The rubric says a lesson's figure tracks how finely its `## Suggested progression`
enumerates clauses, so two courses with different house styles are not measured with the
same ruler. **Every total below is comparable only against its own course's lessons.**
`rust-automaton-db` scores 355 and `portable-bytebeat-wav` scores 48 because one has 23
lessons and the other has 5, not because one teaches better.

Every figure in this table is the one its report carries after the ruling above.

| Course | Lessons | Lesson sum | Course-level penalties | Total | Declining every offer |
|---|---|---|---|---|---|
| `durable-event-broker` | 15 + 3 optional | 128 | none | **128** | 108 |
| `portable-bytebeat-wav` | 4 + 1 optional | 51 | −3 (1 unserved objective) | **48** | 38 |
| `portable-fixed-window-rate-limiter` | 3 + 1 optional | 32 | none | **32** | 24 |
| `rust-automaton-db` | 23 + 0 optional | 370 | −15 (5 unserved topics) | **355** | 355 |
| `webgl-typescript-scene` | 18 + 1 optional | 260 | none | **260** | 243 |

Across 69 scored lessons there are **six confirmed toil sites** and **six unserved
goals**. The six toil sites are one each in `durable-event-broker` (`00:53`),
`portable-bytebeat-wav` (`00:57`), `portable-fixed-window-rate-limiter` (`00:51-52`) and
`rust-automaton-db` (`22:63`), and two in `webgl-typescript-scene` (`00:34` and `13:39`).
Four of the six are project skeletons, and three of those four were charged for the first
time by the ruling above — `webgl-typescript-scene`'s was toil already. No course has a
`required_for` gate on an optional lesson, so that −3 row fires nowhere and its warning is
printed nowhere.

## What each course owes

### `durable-event-broker` — 128, nothing owed at course level

15/15 anchors, 26/26 coverage topics and 69/69 lesson objectives are served, so no
course-level penalty fires. Its one confirmed toil site is the project skeleton at
`00-running-broker.md:53`, "Create the module and a minimal broker executable.", which
the ruling above moved from +2 to −2; that −2 sits inside lesson 00's figure of 4 and is
not charged again at course level. The rest of the findings are about threads that are
carried but never pulled: the append timestamp is introduced at `02:42` and first used
twelve lessons later at `14:46`, and lesson 00's sharpest teaching — byte-slice
ownership — has no `DESIGN.md` anchor that answers it. Three coverage topics are taught
only by optional lessons; the course argues that case itself at `COURSE.md:95-97`, and
the auditor accepts it except for TCP, which `#transport-boundary` treats as
first-class.

### `portable-bytebeat-wav` — 48, and one real defect

One confirmed toil site, the project skeleton at `00-language-and-waveform.md:57`, moved
+2 to −2 under the ruling. Of the drop from 54, the ruling accounts for four points and a
pre-existing addition error in lesson 01 for the other two — see the note in the ruled
block above.

The defect is not a score. `lessons/03-compose-and-export.md:59` tells the tutor to make
the stereo offer **before the first required task**, and the stereo lesson converts the
writer to two channels (`stereo-bytebeat.md:46`), while lesson 03's completion condition
requires **mono** `output.wav` (`03:67`). A learner who accepts the offer cannot finish the
lesson. `tutorial.yaml:49` only checks that `output.wav` exists, so the validator stays
green through the whole conflict — the green-validator-and-bad-course case this skill
exists for.

The −3 is `lessons/03-compose-and-export.md:23`, "Distinguish the authored course from
environment-specific extensions": no task depends on the distinction.

### `portable-fixed-window-rate-limiter` — 32, the smallest and most uniform course

Every objective, every coverage topic and every anchor is served, so it owes nothing at
course level, and it does it in four lessons of 73 to 78 lines. It carries one toil
site, the project skeleton at `00-contract-and-language.md:51-52`, which the ruling
above moved from +1 to −2 and which is the whole of the drop from 35. Its open question
is `concurrency safety` (`COURSE.md:57`), which only the optional
`concurrent-callers.md` teaches: a learner who declines never learns that their limiter
is unsafe to share. The rubric makes that a question and not a score, deliberately.

### `rust-automaton-db` — 355, five coverage topics owed

Five topics the course names and no lesson exercises: **interior mutability**
(`COURSE.md:248`), **atomics** (`:250`), **associated types** (`:242`), **Cargo
workspaces** (`:267`) and **refactoring across crate boundaries** (`:269`). Verified
independently: `interior mutab|RefCell` matches nothing in any lesson, and `atomics`
appears once, in a concepts list at `12:36`, with no clause requiring one.

One confirmed toil site, `22-hardening-performance.md:63` "Build CI and reproducible
clusters" — the CI half is a file the bundle could ship.

This is the one bundle that takes the ruling's exception. `00:24` "Create and run a Cargo
binary project." is served by `00:76` alone — the declared `cargo-run` validator is never
invoked in a completion condition — so supplying the skeleton would strand the objective,
and the step keeps the score it had. The total is unchanged by the ruling.

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

The ruling above moved nothing here. `00:34` is this course's skeleton step and it was
already toil: the five files sit in the bundle at `lessons/00-project-setup/starter/`, so
the plain shippability test answered yes and the tiebreak never fired. `npm install` at
`00:42` stays the learner's work, as the ruling says by name.

## Two things that are about the tooling, not the courses

**`audit.py` silently reports no coverage list for `rust-automaton-db`.** The 46 topics at
`COURSE.md:225-271` are inside a fenced ` ```text ` block and the parser reads Markdown
list items only, so `coverage_list.topics` comes back `[]`. That is indistinguishable from
a course that declared no boundary, and taken at face value it hides all five gaps above.
Filed as `tutorail-authoring#10`.

**The toil scanner found 5 candidates across 69 lessons and 3 of the 5 were false
positives; 4 of the 6 confirmed sites it never saw.** Both sites it did find are in
`webgl-typescript-scene`; it returned nothing at all for `portable-bytebeat-wav` and
`portable-fixed-window-rate-limiter`, and its one candidate in each of the other two
courses was rejected. It has no pattern for a project skeleton, which is four of the six
sites. Its silence is evidence about its verb list, exactly as the skill says. Every figure
here came from opening the lessons.

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
| `tutorail-authoring#11` | the rubric question is **ruled** (2026-09-13, a skeleton is toil); the issue stays open for the half nothing detects — no validator rule and no scanner pattern finds a missing setup |
| `tutorail-bundles#3` | the field report that raised it — per-language setup for the two portable bundles |
