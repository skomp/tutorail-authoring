# Course quality audit: `rust-automaton-db` — 2026-09-15

Read-only audit. Nothing in `skomp/tutorail-bundles` was created, edited, staged or
deleted; `git status --porcelain` in that repository was empty at the start of this audit
and empty at the end. Every finding below is a **proposal** the author may accept or
refuse; applying one goes back through the `tutorail-authoring` skill and its toolkit.
No finding here rejects a bundle, and `validate_bundle.py` was not modified.

Audited at: `/Users/robert/src/github.com/skomp/tutorail-bundles/rust-automaton-db`
Baseline compared against: `docs/audits/2026-09-13/rust-automaton-db.md`

## Provenance

```
Audit provenance, 2026-09-15 — identical for all five bundles

bundles     skomp/tutorail-bundles @ 221c164 (== origin/main, tree clean)
rubric      skomp/tutorail-authoring @ 86c2bc7, plugin 0.4.0
            skills/course-quality/references/rubric.md
validator   pinned copy of the WHOLE scripts directory from the source checkout
            skomp/tutorAIl @ 717c575  ->  /private/tmp/claude-501/-Users-robert-src-github-com-skomp-tutorail-authoring/19f2342f-a334-4dd6-9b45-348b60a85a2d/scratchpad/pin/validate_bundle.py
            (10 validate_bundle.py copies exist on this machine; this is the source one)
yaml reader restricted built-in, ALWAYS — tutorAIl#29 decided at 7419722,
            "Parse YAML with the restricted reader always, never PyYAML".
            PyYAML 6.0.3 is importable here and is deliberately not used.
verdicts    all five bundles: PASS - every applicable check ran and found nothing. exit 0
```

A green validator line is a claim about a machine on a day unless it records which copy of
the validator and which YAML reader produced it. The block above records both. It is also
not an input to any figure in this report: the validator answers *"is this a bundle?"* and
this report answers *"does this teach?"*.

Evidence script: `skills/course-quality/scripts/audit.py`, both forms
(`<bundle>` and `<bundle> --json`), exit 0 for each.

---

## The rubric, printed in full as the skill requires

### The scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises. Course-level, counted once PER UNSERVED OBJECTIVE |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised |

### The rulings inside the scored table that decide elements here

- **A project skeleton is toil** when the two tests disagree; the shippability test wins.
- **The exception**: a setup step is teaching, not toil, when it is the **ONLY element
  serving the objective that names it**. Handing the result over would strand the objective
  and cost −3, and a bundle cannot be charged −2 for assigning a step and −3 for supplying
  it. The operational test is *enumeration*, never the objective's wording.
- **A step the tutor performs is not an element at all** — not toil, not evidence. The
  objective it served does not disappear with it.
- **Setup that needs the network, a toolchain or an account is the learner's work.**
- **A branch point scores `evidence`, 0.** The teaching is in whichever branch is taken.
- **A tutor-addressed element scores `teaching`, +2** when the learner must decide or
  construct in response. Score by what the learner does.

### Rows a reader answers, and a script never scores — **six** of them

1. a `design_refs` entry that does not answer the question its lesson raises;
2. a lesson that introduces a type or concept nothing later uses;
3. **a symbol or term a lesson uses and no lesson introduces** — `file:line` of the **first
   use**, and "bound only in `DESIGN.md`" kept separate from "bound nowhere";
4. **a lesson that does not equip the tutor to end a turn with one concrete action** —
   answered pass/fail for **every** lesson, grading the lesson **FILE**;
5. a lesson far outside the course's usual size, in either direction;
6. a must-cover topic that only an optional lesson teaches — a **question, permanently not
   a score**.

Rows 3 and 4 are new since the 2026-09-13 run, which carried four. Both are answered in
section 6, and row 4 also occupies a column of the section 2 table.

### The invariant no structural check can reach

> A course carrying optional lessons must be completable by a learner who declines every
> offer.

Answered in 6.6, against the lessons and not only against the manifest.

### Scoring unit, stated so the arithmetic can be checked

Identical to the 2026-09-13 run, so the two are comparable element for element:

1. every numbered clause of `## Suggested progression`; plus
2. every `## Completion conditions` line that adds a **distinct** requirement the
   progression does not already carry — in practice the validator lines (`cargo check`,
   `cargo test`, `src/lib.rs` exists: evidence, 0) and the "the learner can explain X"
   lines (teaching, +2).

Completion conditions that merely restate a progression step are not scored twice. A
clause containing two different things is split and each half scored. `## Constraints`,
`## Theory`, `## Concepts to teach`, `## On completion, persist` and
`## Optional deeper paths` are **not** scored elements: the first three are addressed to
the tutor and assign the learner nothing, the fourth is tutor-owned bookkeeping
(`tutorial.yaml:38`), and the fifth is an offer, not a task.

**Comparable within this course, not between courses.** Nothing in this report is set
beside `durable-event-broker`, `webgl-typescript-scene` or any other bundle.

---

## 1. The course and its total

| Field | Value |
|---|---|
| Bundle id | `rust-automaton-db` |
| Title | Learn Rust by Building AutomatonDB |
| Main-path lessons | 23 |
| Optional lessons | **0** — no `optional_lessons:` key in `tutorial.yaml` |
| `supplies:` entries | **1** (was 0 on 2026-09-13) — `tutorial.yaml:53-56` |
| `DESIGN.md` anchors | 23 |
| Files shipped as course material | **1** — `supplies/Cargo.toml`, 4 lines |
| Bundle prose | 1,872 lesson lines across 23 files |

### Arithmetic

```
Sum of the 23 lessons                                            370
  − unserved coverage topic: interior mutability                  −3
  − unserved coverage topic: atomics                              −3
  − unserved coverage topic: associated types                     −3
  − unserved coverage topic: Cargo workspaces                     −3
  − unserved coverage topic: refactoring across crate boundaries  −3
  − required_for gates on optional lessons (0 gates × −3)          0
                                                    ------------------
COURSE TOTAL                                                     355
MAIN-PATH TOTAL                                                  355
```

**The course total and the main-path total are the same number**, because every one of the
23 lessons is on the main path. There is no second total to report: no lesson is optional
in the manifest, and none is optional in its own prose either (6.6).

Five gaps are listed in section 3, −3 each, −15 subtracted. The list and the arithmetic
agree. **The lesson sum was re-added element by element from the lesson files in this
audit, not carried over** — the per-lesson visible sums are in section 2 and the running
total is printed there.

### One factual correction to the 2026-09-13 report and to this audit's brief

Both state that the coverage block at `COURSE.md:225-271` contains **46** topics. It
contains **45**: the fence opens at `:225` and closes at `:271`, and lines `:226-270` are
45 non-blank topic lines, counted one per line. The count changes nothing — the five gaps
are named individually and each carries its own −3 — but a report that asks the reader to
re-add its own arithmetic should not hand them a wrong denominator.

---

## 2. The per-lesson table

**Closing action** is the rubric's row 4, answered pass or fail for every lesson, grading
the lesson **file**. It is not a score and is never added into one. Every `fail` is carried
into 6.4 with its `file:line` and the failing sentence.

| Lesson | Score | Objectives served | Toil found | Closing action |
|---|---:|---|---|---|
| 00 — Rust foundations through an in-memory KV store | 21 | 11 of 11 | none | pass |
| 01 — Rows, cells, and temporal visibility | 18 | 8 of 8 | none | **fail** — `01:79-:80` |
| 02 — Typed keys and the table hierarchy | 26 | 10 of 10 | none | pass |
| 03 — The first deliberate refactor | 15 | 7 of 7 (one thinly) | none | pass |
| 04 — Tables and richer typed schemas | 14 | 7 of 7 | none | **fail** — `04:93` |
| 05 — Canonical ordered binary keys | 15 | 7 of 7 | none | pass |
| 06 — Define the data and query algebra | 15 | 5 of 5 | none | pass |
| 07 — Ordered querying before automata | 13 | 5 of 5 | none | pass |
| 08 — Build the automaton machinery | 23 | 9 of 9 | none | pass |
| 09 — Automaton-native typed key queries | 12 | 7 of 7 | none | pass |
| 10 — Storage engine I: durability | 16 | 7 of 7 | none | pass |
| 11 — Storage engine II: automaton-aware segments | 16 | 7 of 7 | none | pass |
| 12 — Concurrency and async Rust | 19 | 8 of 8 | none | pass |
| 13 — gRPC server and Rust driver | 16 | 8 of 8 | none | pass |
| 14 — Static distributed cluster and placement | 14 | 8 of 8 | none | pass |
| 15 — Eventual replication and causal versions | 15 | 8 of 8 | none | pass |
| 16 — General quorum systems | 17 | 7 of 7 | none | pass |
| 17 — Convergence and repair | 16 | 8 of 8 | none | pass |
| 18 — Gossip and membership | 13 | 7 of 7 | none | pass |
| 19 — Live cluster reconfiguration | 15 | 8 of 8 | none | **fail** — `19:58` |
| 20 — Online schema evolution | 14 | 7 of 7 | none | pass |
| 21 — Strong consistency mode | 16 | 8 of 8 | none | pass |
| 22 — Hardening and performance | 11 | 10 of 10 | **1 site, `22:63`** | pass |
| **Sum** | **370** | | 1 | 20 pass / 3 fail |

Running sum, so a reader can check it without re-adding from scratch:
21, 39, 65, 80, 94, 109, 124, 137, 160, 172, 188, 204, 223, 239, 253, 268, 285, 301, 314,
329, 343, 359, **370**.

No lesson scores at or below zero, so the mandatory breakdown rule for zero-or-below fires
for none of them. Breakdowns follow for every lesson anyway, because every lesson's figure
depends on at least one `+1` or `0` a reader would otherwise have to guess at.

### 00 — 21 points

Lesson 00 is the only lesson whose line numbers moved since 2026-09-13. Commit `26c0eb9`
inserted a three-line constraint at `:71-:73`, so every element below `:70` shifted by +3.
The elements themselves are the same elements.

| `file:line` | Sentence | Score |
|---|---|---|
| `lessons/00-foundations.md:79` | "Write the entry point for the supplied `automaton-db` crate and run the binary." | **0** |
| `:80` | "Experiment with bindings, `String`, `&str`, function arguments, moves, and borrows." | +2 |
| `:81` | "Introduce a small entry struct and a `Vec<Entry>`." | +2 |
| `:82` | "Implement insertion and exact lookup by iterating the vector." | +2 |
| `:83` | "Use `Option` to represent missing keys." | +2 |
| `:84` | "Encounter and reason about returning a borrowed value from stored data." | +2 |
| `:85` | "Move behavior into a `Database` type with methods using `&self` and `&mut self`." | +2 |
| `:86` | "Replace the linear entry vector with `BTreeMap<String, String>`." | +2 |
| `:87` | "Add tests that protect insert/replace/lookup semantics." | +2 |
| `:88` | "Remove obsolete representations once the map replaces them." | +1 |
| `:92` | "`cargo check` succeeds." | 0 |
| `:93` | "`cargo test` succeeds." | 0 |
| `:98-:99` | "The learner can explain the difference between moving `String`, borrowing `&String`, and borrowing `&str`." | +2 |
| `:100` | "The learner can explain why a returned borrowed value cannot outlive the database." | +2 |

`0 + (8 × 2) + 1 + 0 + 0 + 2 + 2 = 21`.

`:88` is practice: the decision about what is obsolete was already made at `:86`, and
`COURSE.md:41-44` makes the cleanup a house rule rather than a fresh judgement. `:79` is
the headline of this audit and is argued in full in section 4.

### 01 — 18 points

`:69 +2` "Introduce `Cell` with an owned value and optional validity bounds." ·
`:70 +2` "Add constructors/builders only when they are immediately exercised." ·
`:71 +2` "Implement and test `Cell::is_visible_at`." ·
`:72 +2` "Introduce `Row` as a map from cell name to `Cell`." ·
`:73 +1` "Add row expiry." · `:74 +2` "Implement insertion/replacement semantics for a named
cell." · `:75 +1` "Implement row visibility." · `:76 +2` "Implement lookup that combines row
and cell visibility." · `:77-:78 +2` "Add tests for missing cells, row expiry, cell expiry,
not-yet-valid cells, and exact boundaries." · `:79-:80 0` "Discuss tombstones conceptually
and defer their storage representation until the surrounding update model is ready." ·
`:84 0` validator · `:91 +2` "The learner can explain why explicit-time visibility is easier
to test and extend."

`2+2+2+2+1+2+1+2+2+0+0+2 = 18`. `:73` and `:75` re-apply the half-open bound pattern
constructed at `:69`/`:71` at a second nesting level; the repetition is the point and the
decision is not new.

### 02 — 26 points, the highest in the course

Eleven progression clauses at `:89-:102`, every one a construction or a decision, +2 each
(= 22): `:89` `KeyValue` enum · `:90` distinct composite key types · `:91-:92` "Add only the
traits demanded by `HashMap` and `BTreeMap`, using compiler diagnostics to understand
recursive trait bounds." · `:93` `Partition` · `:94-:95` "Introduce `KeyType` and `KeyColumn`
only when they are immediately used to validate runtime key values." · `:96` `Table` ·
`:97` `KeyColumn::matches` · `:98` hierarchical write path · `:99` table errors · `:100`
"Validate shape and type before mutating the table." · `:101-:102` the five-case test set.

Plus `:106 0` validator, `:114-:115 +2` "The learner can explain why the local `HashMap`
hash is unrelated to future placement hashing.", `:116 +2` "The learner can explain the
temporary meaning of derived enum ordering."

`22 + 0 + 2 + 2 = 26`.

### 03 — 15 points

`+2` at `:70-:71`, `:72-:73`, `:74`, `:75-:76`, `:78` (= 10) · `+1` at `:77` "Move code in
small increments and keep tests passing." — executes the boundary decision taken at `:75` ·
`0` at `:79` "Inspect the final diff for accidental behavior changes or representation
leaks." — read the diff, which is what the `git-diff` validator at `:5` is for · `0` at
`:83` "`src/lib.rs` exists.", `:84` "`cargo check` succeeds.", `:85` "`cargo test`
succeeds." · `+2` at `:90` and `:91`, the two explain-conditions.

`10 + 1 + 0 + 0 + 4 = 15`.

**Objective served thinly**, unchanged from 2026-09-13: `03:27-:28` "Recognize when warnings
reveal structural problems versus ordinary private implementation detail." No progression
clause and no completion condition mentions warnings; the only warning content is the
constraint at `:66`. Ruled **served, thinly** rather than a −3 gap, because the constraint
binds the learner throughout `:70-:78` and `COURSE.md:41-44` makes dead-code warnings a
course-wide signal. A reader could defensibly charge −3 and take the course to 352.

### 04 — 14 points

`+2` at `:63` "Refine primitive key types and decide which ones belong in the first stable
set." · `:64` "Add named typed value-column definitions." · `:66` "Add schema version
identity." · `:67` "Model permitted append-only schema changes." · `:68-:69` "Introduce
codec-shaped abstractions for values only when a concrete typed value needs conversion." ·
`:70` "Test valid and invalid schema evolution operations." (= 12)

`+1` at `:62` "Introduce explicit table identity." (extends the `Table` built at `02:96`)
and `:65` "Validate table schema construction." (second application of the
validate-before-mutate pattern taught at `02:100`).

`0` at `:74` validator and `:81-:82` "The unresolved appended-clustering-component semantics
remains documented rather than silently assumed." — a recorded deferral, no construction.

`12 + 1 + 1 + 0 + 0 = 14`.

### 05 — 15 points

`+2` at `:49, :50, :52, :53, :54, :55, :56` (= 14) · `+1` at `:51` "Add the remaining
fixed-width types." — explicitly the repetition of `:50` · `0` at `:60` validator and `:65`
"The type-tag decision is recorded." (already scored at `:56`).

`14 + 1 + 0 + 0 = 15`.

### 06 — 15 points

`+2` at `:45, :46, :47, :49, :50, :51` (= 12) · `+1` at `:48` "Define value post-filter
predicates." — the same shape as `:47`, one layer out · `+2` at `:58` "The learner can
explain which operations belong to logical semantics and which belong to execution."

`12 + 1 + 2 = 15`. Lesson 06 has **no** validator line in its completion conditions,
although its frontmatter declares `cargo-check` and `cargo-test` — see 6.7.

### 07 — 13 points, and the smallest progression in the course

`+2` at `:47, :48, :49, :50, :51` (= 10) · `+1` at `:46` "Implement exact ordered
traversal." — `BTreeMap` lookup was built at `00:86` and `02:110`, so this is the third
application · `0` at `:55` validator · `+2` at `:58` "The learner can identify the class of
middle-key predicates that motivates automata."

`10 + 1 + 0 + 2 = 13`.

### 08 — 23 points, the second highest

All ten progression clauses at `:54-:63` score +2 (= 20), every one a construction with an
instructive wrong answer, including `:54` "Review current Rust regex/automata/FST crates and
select comparison targets." — a selection, hence teaching, and the course's first ecosystem
checkpoint. Plus `:71 +2` "Benchmarks or measurements inform at least one representation
decision." (a decision, distinct from the measuring at `:63`) and `:72 +1` "A replacement
checkpoint compares the implementation with mature crates." (repeats the method established
at `:54`).

`20 + 2 + 1 = 23`.

### 09 — 12 points, the second lowest

`+2` at `:47, :48, :50, :51, :53` (= 10) · `+1` at `:49` "Add fixed-byte predicates if
present in the schema." — conditional repetition of `:47-:48`, and the condition may not
hold at all · `+1` at `:52` "Stream results." — iterator streaming was constructed at
`07:49` · `0` at `:57` validator.

`10 + 1 + 1 + 0 = 12`.

This is the lesson the whole course exists to reach (`COURSE.md:8`) and it scores
second-lowest, on seven terse clauses. That is a sequencing observation, not a scoring
defect: 05-08 do the construction and 09 assembles it. Proposal 7 carries it as a question.

### 10 — 16 points

All eight progression clauses at `:50-:57` score +2 (= 16). `:65` "The durability
acknowledgement contract is documented." scores 0 — recording a contract already decided at
`:55`. `16 + 0 = 16`.

### 11 — 16 points

Eight of nine progression clauses score +2 (`:50-:57`, = 16). `:58` "Measure heap usage and
traversal performance." scores 0 — measure and report. `16 + 0 = 16`.

### 12 — 19 points

`+2 × 9`: `:56` threads with owned data · `:57` "Share engine state through `Arc`." · `:58`
"Add the smallest justified synchronization." · `:59` channels · `:60` "Inspect
`Send`/`Sync` compiler constraints." · `:61` "Build/inspect simple futures and polling." ·
`:62` "Explain wakers and pinning." · `:64` cancellation/backpressure · `:65` "Stress-test
concurrent operations." (= 18)

`:62` is +2 as a **tutor-addressed element** under the rubric's settled rule: the sentence is
written at the tutor and the learner must construct the explanation, which `:72` then checks.
`:71` and `:72` are therefore not scored again — they are the completion checks on `:60` and
`:62`. `+1` at `:63` "Adopt Tokio." — constraint `:51` already settles the choice. `0` at
`:70` validator.

`18 + 1 + 0 = 19`.

### 13 — 16 points

`+2 × 7` at `:50, :51, :52, :53, :54, :56, :57` (= 14) · `+1` at `:49` "Review current gRPC
crates." — third instance of the ecosystem-checkpoint method, and constraint `:42` narrows
the answer to essentially one crate · `+1` at `:55` "Add cancellation/backpressure." —
constructed at `12:64`.

`14 + 1 + 1 = 16`.

### 14 — 14 points

`+2 × 6` at `:50, :51, :52, :53, :54, :55` (= 12) · `+1` at `:49` "Define static cluster
config and node IDs." (config plumbing around the model decisions that follow) · `+1` at
`:57` "Exercise mixed host/container debugging." (constraint `:44` makes it real work, but
the concept was fixed at `:54`) · `0` at `:56` "Run multi-process and Compose clusters." —
run it and see.

`12 + 1 + 1 + 0 = 14`.

### 15 — 15 points

`+2 × 7` at `:49, :50, :51, :52, :53, :55, :56` (= 14) · `+1` at `:54` "Return siblings
through the driver." — plumbing an already-decided representation through the driver built
at `13:52`. `14 + 1 = 15`.

### 16 — 17 points

`+2 × 7` at `:47, :48, :50, :51, :52, :53, :54` (= 14) · `+1` at `:49` "Implement weighted
quorums." — the second construction through the interface defined at `:47`, and the
repetition is the point of the lesson · `+2` at `:61` "The learner can explain how topology
and availability change the trade-offs."

`14 + 1 + 2 = 17`.

### 17 — 16 points

All eight progression clauses at `:50-:57` score +2. `16`.

### 18 — 13 points

`+2 × 6` at `:48, :49, :50, :51, :53, :55` (= 12) · `+1` at `:54` "Compare with mature
membership designs." (fourth ecosystem checkpoint) · `0` at `:52` "Observe false positives."
— observe and report, which `:60` then checks. `12 + 1 + 0 = 13`.

### 19 — 15 points

`+2 × 7` at `:50, :51, :52, :53, :55, :56, :57` (= 14) · `+1` at `:54` "Refresh/redirect
stale clients." — stale routing generations were constructed at `14:55` · **`0` at `:58`
"Evaluate a stronger reconfiguration protocol as an advanced path."** — a branch point, and
the rubric settles branch points at evidence, 0. `14 + 1 + 0 = 15`.

### 20 — 14 points

`+2 × 6` at `:48, :49, :51, :52, :53, :54` (= 12) · `+1` at `:47` "Distribute schema version
identity." (constructed at `04:66`) · `+1` at `:50` "Append value columns." (the append-only
rules were modelled at `04:67`). `12 + 1 + 1 = 14`.

### 21 — 16 points

All eight progression clauses at `:49-:56` score +2. `16`.

### 22 — 11 points, the lowest in the course, and the only lesson carrying toil

| `file:line` | Sentence (or clause) | Score |
|---|---|---|
| `lessons/22-hardening-performance.md:55` | "Establish benchmark baselines." | 0 |
| `:56` | "Profile allocation and CPU hot spots." | +2 |
| `:57` | "Benchmark automaton and storage paths." | +1 |
| `:58` | "Add fuzz targets." | +2 |
| `:59` | "Automate crash tests." | +1 |
| `:60` | "Inject network faults/partitions." | +1 |
| `:61` | "Add model/invariant tests." | +2 |
| `:62` | "Instrument metrics/tracing." | +1 |
| `:63` (first half) | "Build CI…" | **−2** |
| `:63` (second half) | "…and reproducible clusters." | +1 |
| `:64` | "Perform a final architecture/replacement review." | +2 |

`0 + 2 + 1 + 2 + 1 + 1 + 2 + 1 − 2 + 1 + 2 = 11`.

`:56` is +2 rather than 0 because `:71` turns reading a profile into a decision. `:57`,
`:59` and `:60` are practice: they re-apply methods constructed at `:55`/`08:63`, `10:56`
and `15:56`/`17:46`/`18:51`. `:63` is split and argued in section 4.

---

## 3. Goal gaps

**Five gaps, −3 each, −15 total.** The list and section 1's arithmetic agree: 5 gaps
listed, −15 subtracted.

All five are against the course's own declared coverage list at `COURSE.md:225-271`,
introduced by `COURSE.md:223`: "The main path should eventually exercise:". That is a
statement of required coverage, and each line in the fenced block is a stated objective.

### The fenced-list defect DID affect the script's reading of this bundle

`audit.py --json` returns `coverage_list: {"heading": "Rust coverage requirements",
"topics": []}` and its Markdown form prints:

> COURSE.md has a coverage-list heading, "Rust coverage requirements", but it names no
> topics. This is a DIFFERENT finding from declaring none at all: the author started this
> section and never filled it in.

**That is false about this course, and it is `tutorail-authoring#10` — still open.** The
coverage list is present and complete: `COURSE.md:221` is the heading, `:225` opens a
```` ```text ```` fence, `:226-270` name 45 topics one per line, `:271` closes it. The
script's topic extractor reads list items and not fenced blocks, so it reported zero
topics. The same blindness applies to the milestone block at `COURSE.md:187-209`.

**Taken at face value the script's prose would have suppressed this entire section and the
whole −15.** The gaps below come from reading `COURSE.md` directly, exactly as the brief
required. This is a defect in the `course-quality` skill, not in `rust-automaton-db`.

### The five gaps

| # | Gap | `file:line` | How I decided | Score |
|---|---|---|---|---|
| G1 | **interior mutability** | `COURSE.md:248` | `grep -rniE "interior mutab\|RefCell\|Rc<\|UnsafeCell\|std::cell"` across `lessons/`, `COURSE.md` and `DESIGN.md` returns **exactly one line: `COURSE.md:248` itself**. The concept appears in no `## Concepts to teach`, no progression clause and no completion condition. Lesson 01's domain type `Cell` (`01:69`) is the database cell, not `std::cell::Cell`, and is not a false positive I mistook for coverage. | −3 |
| G2 | **atomics** | `COURSE.md:250` | Named once in the whole `lessons/` tree, at `12:36` ("- atomics") inside `## Concepts to teach`. No progression clause and no completion condition requires one; `12:58` "Add the smallest justified synchronization." is satisfiable — and under constraint `12:49` most naturally satisfied — by a `Mutex` alone. A concept listed for the tutor to mention is not a task the learner performs. The other `atomic` hits are the `#atomicity` anchor (`DESIGN.md:126`, `01:4`, `10:4`, `12:4`, `10:22/:28/:54/:63`), a different thing entirely, served at `10:54`. | −3 |
| G3 | **associated types** | `COURSE.md:242` | Named once, at `04:47` ("- associated types when justified"), inside `## Concepts to teach` and behind the author's own hedge. No progression clause requires one, and constraint `04:56` pushes against it. Lesson 16's "policy traits" (`16:34`) is the one place a `type Output` would be natural, and `16:47` does not ask for it. | −3 |
| G4 | **Cargo workspaces** | `COURSE.md:267` | The only mentions in the whole bundle are `COURSE.md:67` (teaching philosophy), `COURSE.md:267` (the coverage line itself), and `00:70`, which is a **prohibition**: "Do not introduce modules/workspaces merely for style." No later lesson lifts it. Lesson 03, the one structural-refactor lesson, produces `src/lib.rs` + `src/main.rs` — two targets in one package, not a workspace. | −3 |
| G5 | **refactoring across crate boundaries** | `COURSE.md:269` | Same evidence as G4, and listed as its own coverage line, so counted as its own gap under the per-gap rule. Lesson 03 refactors across a **target** boundary inside one crate (`03:33`). The course never has more than one crate, so a cross-crate refactor is not possible in it as written. One lesson would close G4 and G5 together; they are still two stated objectives and are counted as two. | −3 |

All five persist unchanged from 2026-09-13, which is what `tutorail-bundles#7` predicts
while it stays open — but each was re-verified against the lessons in this audit rather
than carried over.

### Coverage-list topics checked and ruled **served**, so the next reader does not redo it

- **smart pointers** (`COURSE.md:246`) — listed separately from `Arc`, so `Arc` alone does
  not discharge it. Served anyway: `06:50` and `08:55` both require a **recursive enum**
  (`06:31`, `08:34` name recursive enums explicitly), and a recursive enum cannot compile in
  Rust without heap indirection. `Box` is never named in the bundle, but a task forces the
  learner to meet one.
- **macros and derive usage** (`COURSE.md:266`) — the line says *usage*, not authoring.
  Derive usage is pervasive (`02:64`), macro usage likewise (`02:63`, `02:127`).
- **platform/FFI APIs if naturally required** (`COURSE.md:270`) — carries its own hedge;
  `11:53` "Add mmap." and `22:50` satisfy it.
- **RAII and Drop** (`COURSE.md:260`) — `10:35-:36` names both and `10:45` makes `Drop`
  semantics load-bearing in a task.
- **unit/integration/property testing** — unit at `00:87`, property at `05:55`, integration
  on the main path at `13:57` and `20:54`.
- **Cargo and crates** (`COURSE.md:226`) — **re-checked this audit because of the supplies
  change**, and still served: `00:79` has the learner write the entry point for the supplied
  crate and run it, and `cargo check`/`cargo test` run in nine lessons. Shipping the manifest
  did not open a sixth gap.

### `DESIGN.md` anchors: all 23 served

Judged on what tasks make the learner **do**, never on `design_refs`. Lesson 00 carries no
`design_refs` key at all and serves no anchor — correctly, since it is pure Rust
foundations. The 23 anchors and 23 lessons coincide arithmetically and there is no
one-to-one mapping: `#table-model` and `#key-ordering` are cited by seven lessons each,
`#membership` and `#networking` by one each.

`#table-model` 02:93/:96/:98 · `#partition-key` 02:90, 14:51 · `#clustering-key` 02:90,
05:53, 07:48, 09:50 · `#key-component-types` 04:63, 05:51, Unresolved item resolved at
05:56 · `#key-ordering` 05:49-:53 · `#row-cell-model` 01:69/:72, 02:93 · `#values` 04:64,
04:68 · `#temporal-semantics` 01:71/:75/:76, 06:49, 11:56 · `#deletion` 11:56, 17:55/:56 ·
`#atomicity` 10:54 · `#conditional-operations` 15:55, 21:53 · `#durability` 10:55, 15:50 ·
`#automaton-index` 08:60/:61/:62, 09:51, 11:52 · `#placement` 14:51/:52/:53 ·
`#smart-clients` 13:52, 14:54 · `#networking` 13:50/:51 · `#replication` 15:49 ·
`#quorums` 16:47-:54 · `#strong-consistency` 21:49/:51/:52 · `#membership` 18:48-:50 ·
`#live-reconfiguration` 19:50-:57 · `#topology` 14:50, 16:52 · `#schema-evolution` 04:67,
20:51/:52.

### Two partial gaps: named, argued, and deliberately **not** charged −3

Both are real defects. Neither meets the rubric's test ("an anchor that **no** task
exercises"), so charging −3 would be dishonest arithmetic.

**P1 — `#deletion`: tombstones are integrated for a delete path the learner is never asked
to build.** `DESIGN.md:118-124` opens "Support row deletion and individual-cell deletion
using tombstone semantics so replicas can distinguish deletion from absence." Grepping every
lesson for `delete`/`deletion`/`tombstone` this audit returns hits in lessons 01, 10, 11 and
17 only, and **not one of them is a progression clause asking the learner to implement a
delete operation**: `01:79-:80` defers it, `10:4` is a `design_refs` entry and nothing else
in lesson 10, `11:56` says "Integrate tombstones/expiry." and `17:55-:56` say "Integrate
tombstones." and "Define and test safe tombstone collection." `06:45-:51` defines
projection, predicates and post-filters and no delete; `13:49-:57` has no Delete RPC. The
anchor **is** exercised, by 11 and 17, so no −3 — but the course asks the learner to
garbage-collect tombstones that nothing in the course produces.

**P2 — `#values` is the one anchor whose declared Unresolved item no lesson resolves.**
`DESIGN.md:4-5` sets the contract: "Deliberately unresolved items are marked explicitly and
are expected to be resolved in later lessons." There are exactly three, at `DESIGN.md:51`,
`:85` and `:275`. `#key-component-types` is resolved by a task (`05:56`).
`#schema-evolution` is resolved by a task (`20:52`, reinforced by constraint `20:42`).
`#values` (`DESIGN.md:85-86`, "exact boundary between schema-level typed values and
storage-level opaque bytes") is resolved by **no** task: `04:54` forbids settling it,
`grep -rn "opaque\|boundary between" lessons/` returns **nothing**, and no later lesson
returns to it. Two of three land; the third never does.

---

## 4. The toil inventory

### The project skeleton at `00:79` — the headline of this audit

Since 2026-09-13 the bundle has changed here, and it is the single most consequential
change for this report. Commit `26c0eb9`, "rust: ship Cargo.toml instead of assigning
cargo new":

- added `supplies/Cargo.toml` (4 lines: `[package]`, `name = "automaton-db"`,
  `version = "0.1.0"`, `edition = "2021"`);
- declared it at `tutorial.yaml:53-56`, manifest scope, `from: supplies/Cargo.toml`,
  `to: Cargo.toml`, `describe: "Cargo.toml: the crate manifest for automaton-db, so lesson
  00 starts at Rust rather than at cargo new"`;
- added the constraint at `00:71-:73`;
- **rewrote the progression step**, from "Create `automaton-db` with Cargo and run the
  generated binary." to "Write the entry point for the supplied `automaton-db` crate and
  run the binary.";
- and **did not touch objective `00:24`.**

#### Was objective `00:24` rewritten? No.

`lessons/00-foundations.md:24` reads today, verbatim and unchanged since the bundle was
received:

> - Create and run a Cargo binary project.

`git show 26c0eb9` touches two files and five lines; none is in the `## Learning
objectives` block at `:22-:34`. The commit message says so in its own words: *"objective 1,
'Create and run a Cargo binary project', keeps a server and needs no rewrite — which is why
this commit does not touch it. An earlier plan to rewrite that objective assumed the whole
skeleton would ship."*

#### Is `00:24` now stranded? No — and the brief's premise for that conclusion does not hold.

The brief instructed: *"If the skeleton is now supplied and the objective was NOT rewritten,
the objective is stranded and the course pays −3."* **The antecedent is only half true, so
the conclusion does not follow, and I am saying so with evidence rather than subtracting a
−3 I cannot justify.** The skeleton was not supplied. One file of it was.

`cargo new --bin` produces two files: `Cargo.toml` and `src/main.rs`. The bundle ships the
first and not the second; `tutorial.yaml:39` keeps `src/**` learner-owned and no `supplies:`
entry names `src/main.rs`. What the learner is assigned at `00:79` is therefore **the other
half of the skeleton plus the run**, and both halves of the objective still have an act
behind them: *create* a binary project (write its entry point — a crate with a manifest and
no `src/main.rs` is not yet a binary project and will not build) and *run* it.

#### Enumeration of every element serving `00:24`, done fresh and not reused

The rubric is explicit that this is settled by enumerating, never by reading the objective's
wording. Lesson 00 states eleven objectives at `:24-:34` and this audit scored fourteen
elements. The mapping:

| Element | Sentence | Objective(s) it serves |
|---|---|---|
| `:79` | "Write the entry point for the supplied `automaton-db` crate and run the binary." | **`:24` — create and run a Cargo binary project** |
| `:80` | "Experiment with bindings, `String`, `&str`, function arguments, moves, and borrows." | `:25`, `:26` |
| `:81` | "Introduce a small entry struct and a `Vec<Entry>`." | `:28`, `:29` |
| `:82` | "Implement insertion and exact lookup by iterating the vector." | `:29` |
| `:83` | "Use `Option` to represent missing keys." | `:30` |
| `:84` | "Encounter and reason about returning a borrowed value from stored data." | `:31` |
| `:85` | "Move behavior into a `Database` type with methods using `&self` and `&mut self`." | `:27`, `:28`, `:32` |
| `:86` | "Replace the linear entry vector with `BTreeMap<String, String>`." | `:33` |
| `:87` | "Add tests that protect insert/replace/lookup semantics." | `:34` |
| `:88` | "Remove obsolete representations once the map replaces them." | `:33` |
| `:92` | "`cargo check` succeeds." | none directly — verifies `:80-:88` |
| `:93` | "`cargo test` succeeds." | `:34` |
| `:98-:99` | "The learner can explain the difference between moving `String`…" | `:25`, `:26` |
| `:100` | "The learner can explain why a returned borrowed value cannot outlive the database." | `:31` |

**Sole server: still yes.** `:79` is the only element serving `:24`. Two near misses were
re-checked and rejected:

- **`:92` "`cargo check` succeeds."** presupposes a Cargo project rather than creating one,
  and it verifies the code written at `:80-:88`. It does not run the binary.
- **The `cargo-run` validator at `00:4`.** The prior finding is **still true, verified this
  audit**: `lessons/00-foundations.md:4` reads `validators: [cargo-check, cargo-run,
  cargo-test, manual]`, lesson 00 is the **only** lesson in the bundle whose frontmatter
  declares `cargo-run`, and the completion conditions at `:92-:100` name `cargo check` and
  `cargo test` and never `cargo run`. So the *run* half of `:24` still rests on `:79` alone.
  The author wired a validator for the objective and still never calls it.

#### Therefore the exception still fires, and `00:79` is **not** toil

Under the rubric's operational test, `:79` is the only element serving the objective that
names the setup, so the setup is the subject: handing the remaining half over would strand
`00:24` and cost −3 against the −2 it would save, and a bundle cannot be charged −2 for
assigning a step and −3 for supplying it. **`00:79` keeps `evidence`, 0** — what the
exception says to score it as, what it actually is, and what the same element scored on
2026-09-13.

**Where a reader may disagree, stated openly.** "Write the entry point" is a construction,
and a reader could score it `teaching`, +2, on the ground that the learner now writes a file
rather than running a generator. I keep it at 0 because what the step asks for is an empty
`fn main`, which the learner performs rather than decides, and because scoring it +2 would
make the one element that changed text the only thing moving in a 370-point total. If the
author reads it as +2, lesson 00 becomes 23 and the course becomes **357**. The figure is
the reader's judgement and the inventory above lets the author overturn it.

**The residual hole, named again rather than silently priced in.** The rubric says an author
can still take the exception by writing a sole-served objective around a step that teaches
nothing, and names "Create and run a Cargo binary project" as close to that line. It is
closer now than it was, not further: the commit removed the mechanical half of the step and
left the perform-not-decide half, and the objective that saves it is unchanged. Proposal 9.

**One thing the change did right, worth saying.** `00:71-:73` — "The crate manifest is
supplied. If the learner's repository already carries a `Cargo.toml`, the supplied one is
not placed and their own crate stands; check it builds before the first task." —
handles the `workspace_kind: existing-or-new-repository` case explicitly instead of
assuming a manifest appeared. That is the kind of thing a supplies entry usually forgets.

### Confirmed toil: one site, unchanged

**`lessons/22-hardening-performance.md:63`** — the exact sentence, quoted whole:

> `9. Build CI and reproducible clusters.`

Split, as the skill instructs, and only the first half charged:

- **"Build CI" — toil, −2.** The first CI file for a Rust project (a workflow running
  `cargo build`, `cargo test`, `cargo fmt --check`, `cargo clippy` on push) is deterministic,
  has essentially one right answer, and a mistake in it teaches YAML indentation rather than
  Rust, automata, storage or distributed systems. The toil row's last clause is satisfied:
  **the bundle could have shipped it.** A CI workflow is static text inside the bundle and
  needs no network, toolchain or account at authoring time. `22:73` ("CI protects
  correctness and compatibility.") makes it a required deliverable rather than an aside.
  **The bundle now ships files, so this is no longer even a hypothetical**: `supplies:`
  exists at `tutorial.yaml:53`, and adding a second entry is a two-line change.
- **"…and reproducible clusters" — practice, +1.** Deciding what "reproducible" means for a
  multi-process cluster under fault injection is real engineering building on `14:56` and
  `18:51`.

**Where a reader may disagree, stated openly:** CI for *this* course is not only boilerplate
— `22:69` and `22:73` want crash, partition and compatibility gates running reproducibly,
and wiring those in is genuine work. My ruling charges the boilerplate half and credits the
rest. An author who reads `:63` as entirely the hard half should say so; the −2 comes off,
lesson 22 becomes 13 and the course 357.

### Script candidates examined and rejected

The scanner produced **one** candidate across all 23 lessons.

| Candidate | Verdict |
|---|---|
| `lessons/03-first-refactor.md:23` — pattern `move` — "Move engine code out of `main.rs` without changing behavior." | **Rejected, and not even a task.** The line is item 2 of `## Learning objectives` (`03:20-:29`), not a progression clause. The move *is* the lesson: `03:74` and `03:75` are decisions with instructive wrong answers (marking everything `pub`, which constraint `03:62` names directly). And the bundle could not have shipped the result: the code being moved is the learner's own, written across lessons 00-02, and `tutorial.yaml:39` puts `src/**` under `learner_owned`. Scored +2 at `03:70`. |

### Candidates raised from reading the lessons, and rejected

Named so the next reader does not re-litigate them. Those marked **could not have supplied**
are rejections of exactly the kind the skill asks to be named as such.

| Site | Sentence | Verdict |
|---|---|---|
| `00:79` | "Write the entry point for the supplied `automaton-db` crate and run the binary." | **Rejected — the tiebreak's exception applies**, on a fresh enumeration above. Score `evidence`, 0. |
| `03:77` | "Move code in small increments and keep tests passing." | **Rejected — could not have supplied.** The code is the learner's, from lessons 00-02. Practice, +1. |
| `13:50` | "Define a minimal protobuf schema." | **Rejected.** A `.proto` file is exactly what a bundle can ship, but constraint `13:44` and theory `13:29` ("Internal Rust types should not leak directly into the protocol merely because serialization is convenient") make the schema's shape the lesson's central decision. Shipping it would delete the teaching. +2. |
| `14:56` | "Run multi-process and Compose clusters." | **Rejected as written, with a caveat that becomes proposal 3.** *Running* a cluster is evidence, 0. The `docker-compose.yml` and multi-process launcher this clause presupposes are never assigned by any clause and are not supplied. Unassigned toil is not chargeable toil; it is a hole. |
| `22:62` | "Instrument metrics/tracing." | **Rejected.** Repetitive, but `22:72` requires deciding *what* is major. Practice, +1. |
| `22:55` | "Establish benchmark baselines." | **Rejected — could not have supplied.** The baselines are of the learner's own implementation. Evidence, 0. |
| Every `## On completion, persist` section, e.g. `21:68` | "Persist the strong-mode guarantee/protocol in `DESIGN.md`; record consistency/protocol concepts in `STATE.md`." | **Rejected — not the learner's work at all.** `tutorial.yaml:38` makes `tutorial/STATE.md` and `tutorial/DESIGN.md` tutor-owned. Twenty-three near-identical bookkeeping instructions look like busywork, but the learner does nothing in response, so they are **not scored** rather than +2. |
| The `## Optional deeper paths` block in lessons 05-22 | "Offer relevant papers, proofs, implementation archaeology, or formal models when the learner asks and the material would deepen the topic without replacing the main path." | **Rejected as toil** — it assigns the learner nothing and is unscorable. It is a quality finding all the same: verbatim in 18 of 23 lessons. Proposal 5. |

### The scanner is a candidate generator

`audit.py` fires on a fixed list of verbs in imperative position and reports which verb
fired. It cannot see toil it has no pattern for, and its one hit here was a false positive
in a `## Learning objectives` block. **Its silence across 23 lessons is evidence about the
verb list, not about this course.** This inventory came from opening all 23 lessons and
scoring 191 elements — every progression clause and every distinct completion condition.

The structural fact about toil in this bundle has changed since 2026-09-13 and is worth
stating precisely. It used to ship zero files and declare zero `supplies:` entries, so the
toil row's last clause disarmed nearly every candidate before it was raised. **It now ships
one file and declares one entry**, which removes that blanket defence: the author has
demonstrated the mechanism works in this bundle, so "the bundle could have shipped it" is no
longer arguable anywhere. `22:63` is the one place it bites.

---

## 5. Proposals

Every one is a concrete action, all are refusable, and applying any of them is the
`tutorail-authoring` skill's job.

**Proposal 1 — ship the CI workflow and delete the boilerplate half of `22:63`.** The one
toil fix, and now a strictly smaller change than it was on 2026-09-13, because
`tutorial.yaml:53` already carries a `supplies:` block to append to.

```
python3 scripts/supplies.py add /Users/robert/src/github.com/skomp/tutorail-bundles/rust-automaton-db \
  --from ci.yml \
  --to .github/workflows/ci.yml \
  --describe "Baseline CI workflow: cargo build, test, fmt --check and clippy on push and PR. Extend it in this lesson with the fuzz, crash and partition jobs." \
  --check
```

Manifest scope, deliberately: **the bundle has no lesson folders** (lessons are flat files,
`lessons/22-hardening-performance.md`), and a `--lesson`-scoped `--from` must live inside
that lesson's own folder under `lessons/`, because materialization copies only `lessons/`
into the instance. A lesson-scoped entry therefore needs lesson 22 restructured into
`lessons/22-hardening-performance/LESSON.md` plus `ci.yml`, and `tutorial.yaml:35` rewritten
— a toolkit job. Manifest scope avoids all of that at the cost of placing the file when the
course opens rather than when lesson 22 does. The existing `supplies/Cargo.toml` entry is
manifest-scoped for the same reason, so this is the house pattern.

Prose to delete once the entry exists: change `lessons/22-hardening-performance.md:63` from
`9. Build CI and reproducible clusters.` to `9. Extend the supplied CI workflow with fuzz,
crash and partition jobs, and make the test clusters reproducible in it.` Completion
condition `:73` stays as it is. **Do not remove the clause without adding the entry**, or
the learner reaches `:73` with no CI at all.

**Proposal 2 — close the five coverage gaps, and note that four of the five want one new
lesson between 03 and 04.** G4 and G5 are the same missing material; G3 and G2 are homeless
concepts a second refactor lesson naturally houses. One of:

- **(a) Add `lessons/04-workspace-split.md`, renumbering 04-22 upward.** After 03 and before
  the schema lesson, where `COURSE.md:66-68` says structure should evolve under pressure.
  It teaches: split the package into a workspace with at least two crates, decide the
  dependency direction, move the tests that follow the code, and meet the
  `pub`/`pub(crate)` boundary again where the compiler enforces it harder. Closes G4 and G5.
  Costs a renumber across `tutorial.yaml:12-34` and 19 lesson files — through the toolkit,
  never by hand.
- **(b) Argue the two lines out of `COURSE.md`.** A defensible case exists: a single-package
  course with a clean `lib.rs`/`main.rs` split teaches module boundaries well, and a
  workspace added to tick a coverage line is the front-loading `COURSE.md:68` warns against.
  Then **delete lines 267 and 269 from the coverage block** rather than leaving them stated
  and unserved.

Per topic, for the other three:

- **atomics** — add a progression clause to lesson 12 between `:58` and `:59`: "Replace one
  lock-protected counter or flag with an atomic, and state the ordering you chose and why."
  It is a decision, it has instructive wrong answers, and `12:36` already promises it.
- **interior mutability** — add a clause where a reader cache or a lazily built segment
  index behind `&self` genuinely needs it; `11:55` "Merge memtable/segments in reads." is
  the natural site. Do not add a synthetic exercise: `COURSE.md:273-274` permits one as a
  fallback, but this course has a real place for it.
- **associated types** — lesson 16's quorum policy trait (`16:47`) is the one place an
  associated type is justified rather than decorative. Say so in `16:47`, or strike
  `COURSE.md:242`.

**Proposal 3 — declare the cluster harness lesson 14 presupposes.** `14:56` says "Run
multi-process and Compose clusters." and `14:65` requires "The development cluster works in
at least local multi-process and Compose modes." — but no clause asks the learner to *write*
a Compose file or a launcher, and the bundle does not supply one. Either the learner
silently spends an hour on YAML the lesson never admits to assigning (toil that would then
be chargeable), or they stall.

```
python3 scripts/supplies.py add /Users/robert/src/github.com/skomp/tutorail-bundles/rust-automaton-db \
  --from docker-compose.yml \
  --to docker-compose.yml \
  --describe "Three-node development cluster. Node identity and advertised address come from environment variables the learner wires up in this lesson." \
  --check
```

The teaching is preserved deliberately: the file supplies the *topology*, and constraint
`14:44` ("Address advertisement must work across host and container environments") stays the
learner's problem, which is where the lesson's difficulty lives.

**Proposal 4 — fix the four `design_refs` citations that answer nothing, and close the
delete-path hole (P1).**

- Remove `conditional-operations` from `lessons/13-grpc-driver.md:4`, or add a clause to
  `13:49-:57` defining the conditional-write RPC. Remove `atomicity` from
  `lessons/01-rows-cells-temporal.md:4` and `lessons/12-concurrency-async.md:4`, or give
  each a clause that exercises it. Remove `deletion` from
  `lessons/10-storage-durability.md:4`, or give lesson 10 a tombstone WAL record. Detail and
  `file:line` in 6.1.
- **P1**: add "Implement row and cell deletion with tombstone records." as a clause in
  lesson 01 (replacing the pure deferral at `01:79-:80`, which can keep its "defer the
  *storage* representation" half), add a delete node to the query algebra at `06:45-:51`,
  and add a Delete RPC to `13:49-:57`. **This also repairs lesson 01's closing-action
  failure** (6.4), so it is two findings for one edit. Without it, `11:56` and `17:55` ask
  the learner to compact and garbage-collect tombstones the course never taught them to
  create.

**Proposal 5 — give lessons 05-22 real `## Optional deeper paths`, or drop the section.**
The identical sentence appears verbatim in 18 lessons, while `00:111-:113`, `01:103-:106`,
`02:127-:130`, `03:103-:105` and `04:93-:94` each name concrete excursions. A tutor reading
the generic form has nothing to offer that it did not already know. Lesson 08 alone wants
Myhill-Nerode and Hopcroft by name, lesson 21 wants Paxos/Raft/ABD, lesson 17 wants Merkle
trees and the Dynamo paper, lesson 18 wants SWIM and φ-accrual. This costs the score nothing
and is the cheapest quality win in the bundle.

**Proposal 6 — resolve `#values`'s Unresolved item somewhere (P2).** `DESIGN.md:4-5`
promises every unresolved item is resolved in a later lesson; two of three are and
`DESIGN.md:85-86` is not. Add "Fix the boundary between schema-level typed values and
storage-level opaque bytes, and record it." as a clause in lesson 11 after `11:50`, where the
segment layout forces the question anyway, plus the matching completion condition.
Alternatively strike the **Unresolved** marker from `DESIGN.md:85-86` and state the boundary
— but then `04:68` should stop calling codecs provisional.

**Proposal 7 — a question for the author about lesson 09, not a deletion proposal.** Lesson
09 scores 12, second-lowest, and it is the lesson the whole course exists to reach
(`COURSE.md:8`, `:14-:15`). Two of its seven clauses are practice (`:49`, which may not fire
at all; `:52`, built at `07:49`), it has one validator line and no "the learner can explain"
condition, unlike 00, 01, 02, 03, 06, 07, 12 and 16. **Is 09 thin because 05-08 correctly did
the construction and 09 assembles, or because the assembly step was written in a hurry?** If
the former, nothing needs to change. If the latter, the cheapest fix is an explain-condition
at `09:55-:60` — for example "The learner can explain why the composed automaton prunes
where a prefix scan plus post-filter would not."

**Proposal 8 — `tutorail-authoring#10` is confirmed live against this bundle, with a
measured cost.** `audit.py` reads coverage-list topics from list items only, returned
`coverage_list.topics == []` for a 45-topic fenced block, and printed prose asserting the
author "started this section and never filled it in." For this bundle that statement is
false, and taken at face value it would have suppressed the entire five-gap finding and the
whole −15 — a 4% swing in the course total, silently. Worth attaching this measurement to
the open issue.

**Proposal 9 — a question about `00:24`, not a score change.** `00:79` keeps its 0 because
`00:24` is served by that element and no other. The rubric names the hole that shape of
objective leaves open and asks a reviewer who suspects it to say so. Saying so, and more
firmly than in 2026-09-13: `26c0eb9` removed the mechanical half of the step and left the
half that asks the learner to **perform** rather than **decide**, which is unlike the other
ten objectives at `:25-:34`, every one of which names a distinction, a prediction or a
construction. Two ways to close it, both cheap, and both refusable:

- **Keep the objective and make it earn its place.** Rewrite `:79` so the learner decides
  something the next lessons use — for example "Write the entry point for the supplied
  `automaton-db` crate, run the binary, and say which files a Cargo binary target needs and
  which the supplied manifest gave you." That converts a command into a reading of the
  package layout, and `Cargo workspaces` (G4) is the topic it opens onto.
- **Or finish the job: ship `src/main.rs` too and rewrite `00:24` in the same commit.** This
  is the edit `26c0eb9` deliberately stopped short of. It costs −3 for an unserved `00:24`
  unless `00:24` changes at the same time, so the two edits are one edit. A replacement
  objective that survives the change: "Read a Cargo binary project's layout and explain what
  each file the toolchain needs is for."

**Proposal 10 — invoke the `cargo-run` validator, or drop it.** `lessons/00-foundations.md:4`
declares `cargo-run`; no completion condition at `:92-:100` invokes it. Either add "`cargo
run` succeeds and the binary prints something the learner chose." to the completion
conditions — which would give `00:24`'s *run* half a second server and is a one-line edit —
or remove `cargo-run` from `:4`. Leaving it declared and uncalled is what made `00:79`
sole-served in the first place, and an author who does not intend the exception to keep
firing should start here.

---

## 6. The questions only a reader can answer

None of these is scored. All of them change what the author does next. **Six rows**, up from
four on 2026-09-13; rows 6.3 and 6.4 are new.

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

**Four instances found**, all re-verified against the lessons this audit. Each is a citation
that resolves, in a lesson whose tasks never go near what the anchor decides. The validator
is green for all four.

| `file:line` | The citation | Why it answers nothing |
|---|---|---|
| `lessons/13-grpc-driver.md:4` | `conditional-operations` | `DESIGN.md:136-142` requires compare-and-set, `IF NOT EXISTS` and read-modify-write, and insists "Do not present conditional syntax without stating its consistency semantics." `grep -n "conditional\|CAS\|compare-and-set\|IF NOT EXISTS" lessons/13-grpc-driver.md` returns **exactly one line: `:4` itself**. `13:51` serves put/get; `13:53` adds typed query messages. A learner who follows the reference finds a design decision the lesson never touches. |
| `lessons/01-rows-cells-temporal.md:4` | `atomicity` | `DESIGN.md:128-129`: "Multiple changed cells in one row commit atomically." The string `atomic` does not appear in lesson 01 outside that frontmatter line. `01:74` is "Implement insertion/replacement semantics for **a named cell**" — single-cell, the opposite of the multi-cell guarantee. The anchor is served, but at `10:54`, nine lessons later. |
| `lessons/12-concurrency-async.md:4` | `atomicity` | Same test, same result: `atomic` appears in lesson 12 only at `:36` ("- atomics", the unrelated Rust primitive, itself gap G2). The concurrency lesson is exactly where "one logical row write is atomic" becomes interesting under `Arc` and locks, and `12:69` gestures at it without naming it. |
| `lessons/10-storage-durability.md:4` | `deletion` | `delete`, `deletion` and `tombstone` appear in lesson 10 **only** in that frontmatter line — not in `## Theory`, not in `## Concepts to teach`, not in the eight progression clauses at `:50-:57`, not in the completion conditions. The WAL is where a tombstone record would first become physical. |

The pattern across all four: the anchor is served **somewhere**, and the citing lesson is not
where. Fixes in proposal 4.

### 6.2 A lesson that introduces a type or concept nothing later uses

**One clear instance, plus two weaker ones named for completeness.**

**Timestamps as a key component type.** `lessons/05-canonical-ordered-keys.md:20` states the
objective "encode unsigned integers, fixed bytes, UTF-8 components, and timestamps", and
`05:51` ("Add the remaining fixed-width types.") makes the learner build a timestamp encoder
and its ordering tests. Nothing later uses it. `lessons/09-automaton-native-key-queries.md`
compiles exactly three predicate kinds — `:47` UTF-8, `:48` integer equality/ranges, `:49`
fixed-byte — and never a timestamp predicate. `grep -rn timestamp lessons/` returns exactly
two lines this audit: `05:20` and an optional deeper path at `01:103`. `DESIGN.md:43-44` is
the source of the mismatch: it puts timestamps among "likely later additions", not the
initial set, and `04:63` explicitly lets the learner decide the first stable set — after
which `05:20` mandates the encoder regardless of what they decided. **It cost the learner
attention and bought the course nothing.** Either add a timestamp predicate to `09:47-:49`
(a range-over-canonical-bytes predicate on a time component is a genuinely good exercise and
would strengthen the course's flagship lesson), or make `05:20`'s timestamp clause
conditional on the stable set chosen at `04:63`, the way `09:49` already is.

**Weaker, named so they are not re-found.** `Display` and `Formatter<'_>` at `01:51` are
introduced in `## Concepts to teach` and never used again — `grep -rn "Display\|Formatter"
lessons/` returns that one line and nothing else in the bundle. `Debug` recurs through
derives; `Display` does not. And the provisional derived-enum ordering at `02:51-:53` looks
like a dead end but is **not** one: it is explicitly temporary (`02:77`), it is what lesson
05 replaces, and `02:116` makes the learner explain its temporary meaning. That one is
correct as written.

### 6.3 A symbol or term a lesson uses and no lesson introduces — **NEW ROW**

The script's `symbol_evidence` block offered three distinct candidates — `T`, `E`, `Eq` —
all in its `concepts` bucket, none in `design-md-only` and none in `none`. **All three are
rejected on the author's boundary, and the row's real content in this bundle is elsewhere.**
The sort below is mine, candidate by candidate, as the rubric says it must be.

#### The script's candidates, sorted and rejected

| Candidate | First use | Ruling |
|---|---|---|
| `T` | `lessons/00-foundations.md:29`, "Use `Vec<T>`, slices, iterators, and closures." | **Not a symbol under this row.** `T` in `Vec<T>` is Rust's own generic-parameter notation — an identifier of the language the learner already chose, in the author's words, not a parameter of the concept being taught. A learner who picked Rust brought `T` with them. Same ruling for its second appearance at `02:65`. |
| `E` | `lessons/02-typed-keys-table-hierarchy.md:69`, "`Result<T, E>`" | **Not a symbol.** Same ground: `Result<T, E>` is the standard library's own spelling. |
| `Eq` | `lessons/02-typed-keys-table-hierarchy.md:64`, "`PartialEq`, `Eq`, `Hash`, `PartialOrd`, `Ord`" | **Not a symbol.** A standard-library trait name. Also note that `02:91-:92` makes deriving these traits a task, so even on a looser reading the lesson introduces it. |

The script's own note says it cannot make this distinction and a reader must. The
distinction it cannot make is the whole of its output here.

#### What the script's candidate rule misses, and what the hand sort found

The script's rule requires a **1-2 character identifier inside a backticked span**. This
course's real unbound terms are 2-5 character **acronyms in plain prose**, so every one of
them is invisible to it. Sorted on the author's boundary — a term the course's subject
supplies against one the learner's chosen language supplies — the acronyms below are all of
the first kind. Nobody brings `WAL`.

**Bound only in `DESIGN.md`** — the meaning exists, in the document the learner never reads.
The repair moves or restates it in the lesson that first uses the symbol.

| Symbol | `file:line` of **first use** | Evidence |
|---|---|---|
| `CAS` | `lessons/21-strong-consistency.md:22`, "- support strong CAS/conditional writes" | The only expansion anywhere in the bundle is `DESIGN.md:138`, "Single-row operations should eventually support compare-and-set/version conditions". No lesson expands it: `grep -rn "compare-and-set" lessons/` returns nothing. `21:36` uses `CAS` again in `## Concepts to teach`, which the rubric says is not itself a definition. The runner loads `#conditional-operations` for the **tutor**, so the learner meets `CAS` cold. This is the textbook case for this row. |

**Bound nowhere** — the course has not decided what the term means for the learner. The
repair is a decision, not a move.

| Symbol | `file:line` of **first use** | Evidence |
|---|---|---|
| `WAL` | `lessons/10-storage-durability.md:18`, "- design a WAL" | `grep -rn "write-ahead" lessons/ COURSE.md DESIGN.md` returns **nothing**. The acronym is used six times (`10:18, :22, :28, :50, :69`, `COURSE.md:122`) and expanded zero. `10:28` describes what a WAL *does* ("converts in-memory mutation into an ordered durable record stream") without ever saying what the letters are. A learner who has not met a write-ahead log before gets the mechanism and not the name. |
| `FST` | `lessons/08-automaton-machinery.md:54`, "1. Review current Rust regex/automata/FST crates and select comparison targets." | `grep -rn "transducer"` returns **nothing** in the whole bundle. `DESIGN.md:173` uses the acronym too and does not expand it, so this is not even a `DESIGN.md`-only binding. It is also the one acronym here naming an object the course does **not** build — a finite state transducer is not a DFA or a DAFSA — so the learner cannot infer it from the lesson either. It sits in the lesson's **first** progression step, where the tutor's first turn lands. |

**Examined and passed**, so the next reader does not re-raise them:

- `LWW` — first use `lessons/15-eventual-replication.md:42`. Expanded at `15:10`, "instead
  of hiding conflicts with last-write-wins", same lesson, 32 lines **before** first use.
- `RF` — first use `lessons/19-live-reconfiguration.md:38`. Expanded at `19:23`, "change
  replication factor", same lesson, before first use.
- `GC` — first use `lessons/17-repair-convergence.md:38`. Expanded at `17:24`,
  "garbage-collect tombstones safely", and again at `17:29`, both before first use.
- `NFA`, `DFA` — first use `lessons/08-automaton-machinery.md:19` and `:21`. Never expanded,
  but the objection does not survive the row's test: lesson 08 **is** the introduction of
  these objects (`:30` explains their behaviour, `:56-:59` construct them), and the row asks
  whether a lesson introduces the thing, not whether it expands the initialism. Passed, with
  the note that expanding them once in `08:30` would cost one clause.
- `DAFSA` — first use `lessons/08-automaton-machinery.md:24`. Glossed in the same lesson at
  `:61`, "Merge equivalent continuation states into an acyclic deterministic automaton",
  which is the expansion in all but letters — but **37 lines after first use**, and the
  acronym is never tied to the gloss. Passed as found-and-late rather than failed; a reader
  who wanted to fail it would be defensible.
- `AST` — first use `lessons/06-data-query-algebra.md:22`. "abstract syntax" appears nowhere
  in the bundle. **Passed on the boundary, not on the evidence**: `COURSE.md:22-23` makes
  "substantial prior programming experience" and "familiarity with basic data structures and
  algorithms" a prerequisite, which puts `AST` on the learner's side of the line the way
  `bool` is. A reader who reads the prerequisite more narrowly should move it to
  *bound nowhere*.

### 6.4 Does the lesson equip the tutor to end a turn with one concrete action? — **NEW ROW**

Answered pass or fail for every lesson in the section 2 table. **Grading the lesson file, as
the rubric insists** — there is no transcript of this course in evidence and it would not be
the subject if there were.

**20 pass, 3 fail.** The three failures are below with `file:line` and the failing sentence.

#### Condition 1 — the lesson names the first concrete action — passes in all 23

This is a real strength of the bundle and the reason the failure count is low. Every
`## Suggested progression` opens with an imperative naming a file, a type, a command or an
artifact, never only an outcome: `00:79` "Write the entry point…", `01:69` "Introduce
`Cell`…", `02:89` "Introduce a `KeyValue` enum…", `03:70` "Introduce `lib.rs` and move…",
`04:62` "Introduce explicit table identity.", `05:49` "Specify ordering invariants before
writing encoders.", `06:45` "Write precise definitions for data entities.", `07:46`
"Implement exact ordered traversal.", `08:54` "Review current Rust regex/automata/FST crates
and select comparison targets.", `09:47` "Compile one UTF-8 component predicate.", `10:50`
"Specify WAL record invariants.", `11:50` "Specify segment blocks and index mapping.",
`12:56` "Introduce threads with owned data.", `13:49` "Review current gRPC crates.", `14:49`
"Define static cluster config and node IDs.", `15:49` "Replicate writes in parallel.",
`16:47` "Define policy interface and required guarantees.", `17:50` "Add hinted handoff.",
`18:48` "Disseminate static membership via gossip.", `19:50` "Version ownership metadata.",
`20:47` "Distribute schema version identity.", `21:49` "Specify the strong guarantee and
failure model.", `22:55` "Establish benchmark baselines."

#### The rubric's first failure property is closed at the course level here, and that is worth recording

The rate-limiter case failed partly on "a progression bullet carrying two actions… and the
lesson nowhere says to split it." Bullets carrying two actions exist in this bundle —
`00:79` ("write the entry point **and** run the binary"), `03:70-:71`, `22:63` ("Build CI
**and** reproducible clusters"), `16:47`, `17:57` — but **`COURSE.md:70-72` says to split
them, course-wide**:

> A bundle lesson may span multiple conversational task cycles. The tutor should break its
> suggested progression into small learner-sized steps rather than dumping the whole lesson
> at once.

That is the instruction the rate-limiter lesson lacked, and it is in the bundle the author
edits. So a two-action bullet here does not leave the tutor with nothing to close on; it
leaves them with two closes. The sites above are still the sites to split, and `22:63` is
the one where splitting also exposes a toil charge.

#### The rubric's second failure property — an open question with no home — and how 18 lessons escape it

The rate-limiter's `## Optional deeper paths` "invites a discussion of alternative return
values… The section never says that it does not close a turn." Lessons 05-22 carry the
generic form, and its wording defuses exactly this: "Offer relevant papers, proofs,
implementation archaeology, or formal models **when the learner asks**…" The conditional is
doing the work the rate-limiter's section lacked — the excursion cannot displace the tutor's
action because it is gated on the learner initiating it. Lessons 00-03 carry concrete,
un-gated bullets, and were checked one at a time: `00:111-:113`, `01:103-:106`,
`02:127-:130` and `03:103-:105` are all *inspect/compare/explore* actions about Rust or the
standard library, and none of them reopens a decision the lesson's own progression settled.
They pass. Lesson 04's does not — see below.

#### The three failures

**Lesson 01 — fail.** `lessons/01-rows-cells-temporal.md:79-:80`, the **final** progression
step:

> `10. Discuss tombstones conceptually and defer their storage representation until the`
> `    surrounding update model is ready.`

Condition 2. The lesson's last step is a discussion with no deliverable, and no completion
condition at `:84-:91` mentions tombstones or deletion, so nothing anchors it. A tutor
working the progression in order reaches the end of lesson 01 holding a design question —
what a tombstone is and how it will be stored — precisely where the closing action should
be. The decision is marked as deferred, which is good authoring, but marking it does not
give the turn an act. Proposal 4's P1 repair fixes this and the delete-path hole together:
replace the clause with "Implement row and cell deletion with tombstone records." and keep
the "defer the *storage* representation" half as a constraint.

**Lesson 04 — fail.** `lessons/04-richer-typed-schemas.md:93`, in `## Optional deeper paths`:

> `- Compare enum-based dynamic values with generic compile-time table APIs.`

Condition 2, and this is the rate-limiter's exact shape. Lesson 04's progression settles the
value-representation question at `:62-:70` — `:64` "Add named typed value-column
definitions." and `:68-:69` codec-shaped abstractions — and this bullet reopens it, un-gated
by any "when the learner asks", in the section the runner reaches at the end of the lesson.
`:94` ("Explore zero-sized marker types and phantom types as an alternative API style.") is
the same shape one layer out. The repair is one word: gate both bullets on the learner
asking, as lessons 05-22 already do, or move them into `## Theory` as a note on what was
decided and why.

**Lesson 19 — fail.** `lessons/19-live-reconfiguration.md:58`, the **final** progression step:

> `9. Evaluate a stronger reconfiguration protocol as an advanced path.`

Condition 2. An open-ended evaluation with no named artifact, no criteria and no completion
condition at `:62-:66` covering it — the lesson's last turn ends with a question instead of
an act. Scored 0 as a branch point, correctly, and the branch point is legitimate; what
fails this row is that the branch is the **last thing in the progression** and nothing in
the lesson says it does not close the lesson. The repair is to move it into
`## Optional deeper paths` with the "when the learner asks" gate, which is where lessons
05-18 and 20-22 put material of exactly this kind.

### 6.5 A lesson far outside the course's usual size, in either direction

Answered on two measures, because they disagree and the disagreement is the finding.

**By scored elements — the measure the rubric cares about — the course is remarkably
uniform.** Progression clauses per lesson, sorted: 6, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9,
9, 9, 9, 10, 10, 10, 10, 10, 11. Median 8, range 6-11, a 1.8× spread with no outlier. Scores
run 11 to 26, median 15. **No lesson is far outside the course's usual size on this
measure.**

**By prose length the distribution is bimodal, and that is a house-style seam rather than an
outlier.** Measured this audit:

| Band | Lessons | Lines |
|---|---|---|
| Long-form | 00, 01, 02, 03, 04 | 113, 106, **130**, 105, 94 |
| Terse | 05-22 | **67** to 83, median 73.5 |

- **Upper outlier: `lessons/02-typed-keys-table-hierarchy.md`, 130 lines** — 1.78× the
  course median of 73 and the largest lesson by every measure: 10 objectives, 11 progression
  clauses, 10 completion conditions, 26 points. **Ruling: it is one lesson and should stay
  one.** Every piece is forced by the single act of stopping treating a row key as a string,
  and splitting it would leave the first half with a key type no storage path uses. It is
  large because that step is large. Worth telling the tutor so: `COURSE.md:70-72` already
  says a lesson may span multiple task cycles, and 02 is the clearest case in the course.
- **Lower outliers: `06-data-query-algebra.md` and `07-ordered-querying.md`, 67 lines each**,
  with 07 also carrying the smallest progression (6 clauses). The rubric's note — "one that
  is much smaller is usually a paragraph of the lesson beside it" — **does not hold for 06**,
  a deliberate semantics-before-execution firebreak (`06:26`: "Automata are an execution
  technique, not query semantics… This prevents the automaton engine from accidentally
  defining the public model."). That is a real architectural decision and earns its own
  lesson. For **07** the case is closer, and the ruling is still **keep it separate**: the
  learner needs working range queries in hand before automata are justified, and folding it
  into 08 would make the course's largest concept jump larger.
- **The real size finding is the seam, not any single lesson.** Lessons 00-04 average 110
  lines and carry lesson-specific `Prerequisites` (`01:18` names `00-foundations`), rich
  `Theory`, and bespoke deeper paths. Lessons 05-22 average 74 lines and carry the
  placeholder "- The preceding course lesson." (`05:14` and 17 more) and one generic
  deeper-path sentence. The course reads as hand-written through 04 and generated from 05
  on. It changes no score — the progression clauses are uniformly good — but it is the thing
  an author would most want to know. Proposal 5 is the cheap half of the fix; naming the real
  prerequisite lesson id in each of the 18 terse lessons, as `01:18` and `02:26` do, is the
  other half.

### 6.6 A must-cover topic that only an optional lesson teaches

**Not applicable, and no instance is possible.** The course declares no optional lessons, so
no topic in the coverage block at `COURSE.md:225-271` can be reachable only through an offer
a learner may decline. The rubric's question — *is that acceptable for this course, given
that a learner who declines every offer never meets it?* — has no subject here.

For the avoidance of doubt about a near-miss: `COURSE.md:276-284` is headed "Optional paths"
and lists historical/as-of reads, secondary indexes, partition splitting, a textual query
language and a dozen more. **These are not optional lessons and not coverage-list topics.**
They are framed as "Optional later work" beyond the course, are named in no manifest key, and
no lesson exists for any of them. They sit outside the coverage boundary, so nothing is owed
for them. Likewise the 23 `## Optional deeper paths` sections are within-lesson excursions,
not lessons.

### 6.7 The completability invariant, asked out loud

> **Can a learner who declines every offer still finish this course?**

**Not applicable — no optional lessons are declared.** Checked against the lessons and not
only against the manifest, as the rubric requires:

- **Manifest.** `tutorial.yaml` has no `optional_lessons:` key: `:12-:34` is a flat
  `lessons:` list of 23 files and the next key is `workspace_kind:` at `:36`. Keyed off the
  **presence of the key**, not off `optional_lesson_count` — that count is of optional
  lessons found on disk and would report zero for a manifest naming a file that does not
  exist. A grep for `optional_lessons|required_for|anticipates|repair_in` over
  `tutorial.yaml` returns nothing, against a positive control on `supplies:` which hits at
  `:53`. **No `required_for`, `anticipates` or `repair_in` field exists anywhere in the
  bundle.**
- **Consequence for the score.** Zero `required_for` gates, so the −3 gate row fires zero
  times and contributes 0 to section 1's arithmetic. The rubric's accompanying warning is
  not printed because no gate exists to which it could apply.
- **Prose check — prose optionality is not optionality.** All 23 lessons were read looking
  for the webgl failure mode: a lesson its own text calls optional while sitting in
  `lessons:`. **None found.** No lesson title contains "optional"; no `## Purpose` or prose
  describes its own lesson as skippable; no `## Prerequisites` allows for the previous lesson
  having been skipped — all 23 name a predecessor, by id in 01-04 and as "The preceding
  course lesson." in 05-22. The word "optional" occurs only as (a) the
  `## Optional deeper paths` heading in all 23 lessons, offering excursions *within* a
  required lesson, (b) `COURSE.md:276` "Optional paths", work beyond the course, (c)
  `COURSE.md:51` "Nightly features may be optional excursions", (d) `19:58`, a branch point
  inside a required lesson, scored 0, and (e) ordinary uses of `Option<T>` and "optional
  temporal bounds". **The manifest and the prose agree. There is no second total to report,
  and the 355 in section 1 is the only total this course has.**
- **The invariant itself.** No main-path completion condition can depend on something only an
  optional lesson builds, because there are none. Every prerequisite chain is linear
  (00 → 01 → … → 22), and a learner who declines nothing is the only learner this course
  describes. **Invariant not at risk.**

### 6.8 One observation this audit adds, outside the six rows

**Fourteen of 23 lessons declare `cargo-check` and `cargo-test` in frontmatter and invoke
neither in a completion condition.** Explicit validator lines exist only in lessons 00
(`:92`, `:93`), 01 (`:84`), 02 (`:106`), 03 (`:83`, `:84`, `:85`), 04 (`:74`), 05 (`:60`),
07 (`:55`), 09 (`:57`) and 12 (`:70`). Lessons 06, 08, 10, 11, 13, 14, 15, 16, 17, 18, 19,
20, 21 and 22 declare validators no completion condition names.

This is not a scored finding and no element moves because of it — those lessons' completion
conditions are substantive in other ways. It matters because it is the general form of the
`cargo-run` fact that decides this report's headline: the bundle's habit is to declare
validators in frontmatter and let the completion conditions speak about behaviour instead.
`00:4`'s uninvoked `cargo-run` is that habit, not an isolated slip — and it is what keeps
`00:79` the sole server of `00:24`. Proposal 10 is the one-line fix if the author would
rather the exception stopped firing.

---

## 7. Every delta from 2026-09-13, and its cause

| # | Delta | Cause |
|---|---|---|
| D1 | `tutorial.yaml` now declares a `supplies:` entry at `:53-:56`; `supplies/Cargo.toml` (4 lines) is new. `supplies:` count 0 → 1; files shipped 0 → 1. | **Bundle changed** — `26c0eb9`. |
| D2 | `00:76` → **`00:79`**, and its text changed from "Create `automaton-db` with Cargo and run the generated binary." to "Write the entry point for the supplied `automaton-db` crate and run the binary." **Score unchanged at 0.** | **Bundle changed** — `26c0eb9`. |
| D3 | New constraint at `00:71-:73` handling a learner repository that already has a `Cargo.toml`. Not a scored element (constraints never are). | **Bundle changed** — `26c0eb9`. |
| D4 | Every lesson-00 element below `:70` shifted +3: `:77-:85` → `:80-:88`, `:89-:90` → `:92-:93`, `:95` → `:98`, `:97` → `:100`. Lesson 00 is 113 lines, was 110; the bundle is 1,872 lesson lines, was 1,869. | **Bundle changed** — `26c0eb9`. Line numbers only; the elements are the same elements. |
| D5 | `00:24` — **no change.** The objective reads exactly as it did, and `26c0eb9` does not touch the `## Learning objectives` block. | **Nothing changed.** Recorded because the brief predicted a rewrite, the bundles session had planned one, and its absence is the headline. |
| D6 | Lessons 10 and 11 titles are now quoted: `title: "Storage engine I: durability"` and `title: "Storage engine II: automaton-aware immutable segments"`. **No content changed with them** — `git show 1609d43` is four lines, two removed and two added, and both titles read exactly as before. No score moves; the 2026-09-13 report already printed both titles correctly. | **Bundle changed** — `1609d43`, so the bundle validates. Confirmed as instructed. |
| D7 | Section 2 gains a **closing-action** column, and section 6 gains **two** rows (6.3 undefined symbol, 6.4 closing action), taking the reader-answered count from four to six. | **Rubric and `SKILL.md` changed** since 2026-09-13. |
| D8 | The undefined-symbol row's answer is **not** the script's `T`/`E`/`Eq`. Those three are rejected on the author's boundary; `CAS` is reported as bound only in `DESIGN.md`, `WAL` and `FST` as bound nowhere. | **New row, and the hand sort the rubric demands.** The script's candidate rule cannot see plain-prose acronyms. |
| D9 | Three lessons — 01, 04, 19 — **fail** the closing-action row. | **New row.** Nothing in those lessons changed; the question was not asked in 2026-09-13. |
| D10 | The coverage block holds **45** topics, not the 46 both the 2026-09-13 report and this audit's brief state. | **Old report wrong** — an off-by-one in a count nothing depended on. Corrected here, and it changes no figure. |
| D11 | The `audit.py` fenced-coverage-list defect is confirmed still live, now with a measured cost: it would have suppressed the entire −15. | **Nothing changed** — `tutorail-authoring#10` is still open and the script still returns `topics: []`. |
| D12 | The five unserved coverage topics **persist**, all five, re-verified by grep with positive controls rather than carried over. | **Nothing changed** — `tutorail-bundles#7` is still open. |
| D13 | The `cargo-run` validator at `00:4` is **still** declared and **still** invoked by no completion condition. | **Nothing changed.** Re-verified, and now set in the wider pattern at 6.8. |
| D14 | Lesson sum **370**, penalties **−15**, course total **355**, main-path total **355** — identical to 2026-09-13, re-added element by element rather than carried over. | **Nothing changed in the arithmetic.** The one element whose text moved kept its score, for a reason that had to be re-derived rather than reused. |
| D15 | Proposal 10 is new (invoke or drop `cargo-run`). Proposal 9 is sharpened: the objective is now *closer* to the rubric's residual hole, not further from it. Proposals 1 and 3 are cheaper, because a `supplies:` block now exists to append to. | **Bundle changed** — `26c0eb9` — and this audit's own reading. |

**Nothing in the bundle changed that moves a score.** The one element whose text changed
kept its figure, and it kept it for a reason that had to be established fresh — the
enumeration in section 4 — rather than inherited from the report that first established it.

---

## Closing note on method

The bundle loads cleanly, the validator is green under the pinned copy recorded at the top
of this report, and neither fact appears anywhere in the 355. The validator answers "is this
a bundle?"; this report answers "does this teach?".

On the evidence of 191 scored elements across 23 lessons, it teaches well. The density of
`teaching` elements is high throughout, the course consistently makes the learner decide
rather than transcribe, every lesson opens on a concrete imperative, and it carries a single
confirmed toil site in 1,872 lines. Its weaknesses are five coverage topics it stated and
never assigned, four citations pointing at decisions their lessons never make, a delete
operation it garbage-collects but never builds, three lessons that end a turn on a question
instead of an act, and a visible seam at lesson 05 where the writing changes hands.

The headline is a change that did the right thing and stopped one file short of finishing
it. Shipping `Cargo.toml` removed the `cargo new` from the learner's first turn, which is
exactly what the toil row exists to cause. Leaving `src/main.rs` unshipped is what keeps
`00:24` served, keeps the skeleton exception firing, and keeps this course the one bundle in
the catalogue still taking it. Whether that is the intended resting place or a half-landed
edit is the author's call, and proposal 9 puts it to them as one.

Every figure here is checkable against a `file:line` and a quoted sentence, and every one of
them is a proposal the author may refuse.
