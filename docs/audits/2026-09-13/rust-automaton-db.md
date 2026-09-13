# Course quality audit: `rust-automaton-db`

> ## OPEN QUESTION, raised 2026-09-13 after publication — the project-skeleton rulings are unsettled
>
> `skomp/tutorail-bundles#3` reports a learner who reached this class of step, said *"can
> you create the base setup for me, there is no learning in that"*, and changed
> `ownership_policy` in their own instance so the tutor would do it. That happened twice, in
> two different courses.
>
> This report rejected the step as toil on the ground that **the bundle could not have
> supplied the result**. That reasoning is incomplete, and the rubric is the reason: it
> carries two tests that disagree here.
>
> - *"could this bundle have shipped the result?"* — for a project skeleton, **yes**. It is
>   a handful of files. A portable bundle can ship one set per supported language and let
>   the tutor choose after the learner picks; this report assumed a single fixed `--from`
>   path and concluded no path existed.
> - *"setup that needs the network, a toolchain or an account is the learner's work"* —
>   **also yes**. `go mod init`, `cargo new` and `npm init` all need the toolchain.
>
> `npm install` is unambiguous under both tests, because `node_modules` cannot ship. A
> project skeleton is not, and the rubric does not say which test wins. Filed as
> `skomp/tutorail-authoring#11`.
>
> **The score consequence is stated below with each affected element.** Nothing is
> re-scored here: the ruling belongs to the author, and a report patched to agree with a
> ruling that has not been made would be worse than one that says it is open.

Read-only audit. Nothing in the bundle was created, edited, staged or deleted. Every
finding below is a **proposal** the author may accept or refuse; applying one goes back
through the `tutorail-authoring` skill and its toolkit.

Audited at: `/Users/robert/src/github.com/skomp/tutorail-bundles/rust-automaton-db`
Evidence script: `scripts/audit.py` from the `course-quality` skill, both forms.

---

## The rubric (printed in full, as the skill requires)

### Scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises. Course-level, counted once per unserved objective |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised |

### Two elements that are easy to score wrong (settled by the rubric, not by me)

- **A branch point scores `evidence`, 0.** The teaching is in whichever branch the learner
  takes, and that branch is scored on its own.
- **A tutor-addressed element scores `teaching`, +2, when the learner must decide or
  construct in response.** Score by what the learner does, at whatever grammatical person
  the author wrote it in.

### Rows a reader answers, and a script never scores

- a `design_refs` entry that does not answer the question its lesson raises;
- a lesson that introduces a type or concept nothing later uses;
- a lesson far outside the course's usual size, in either direction;
- a must-cover topic that only an optional lesson teaches — a **question, permanently not a
  score**.

### The invariant no structural check can reach

> A course carrying optional lessons must be completable by a learner who declines every
> offer.

All four reader-answered rows and the invariant are answered in **section 6**.

### Method notes the rubric insists on

- **An anchor is served by what lessons DO, not by what they CITE.** Every anchor below was
  judged on progression steps and completion conditions, never on `design_refs`.
- **Totals are comparable within one course, not between two.** Nothing here is set beside
  `webgl-typescript-scene`, `durable-event-broker` or any other bundle. Every comparison in
  this report is between lessons of `rust-automaton-db`.
- **A green validator is not a good course.** The bundle loads cleanly and the structural
  tooling is happy. That is not an input to any figure below.

### Scoring unit used, stated so the arithmetic can be checked

Consistently across all 23 lessons, the scored elements are:

1. every numbered clause of `## Suggested progression`; plus
2. every `## Completion conditions` line that adds a **distinct** requirement the
   progression does not already carry — in practice the validator lines (`cargo check`,
   `cargo test`: evidence, 0) and the "the learner can explain X" lines (teaching, +2).

Completion conditions that merely restate a progression step are **not** scored twice.
Where a single clause contains two different things, it is split and each half scored, as
the skill instructs.

---

## 1. The course and its total

| Field | Value |
|---|---|
| Bundle id | `rust-automaton-db` |
| Title | Learn Rust by Building AutomatonDB |
| Main-path lessons | 23 |
| Optional lessons | 0 (no `optional_lessons:` key in `tutorial.yaml`) |
| `supplies:` entries | 0 |
| `DESIGN.md` anchors | 23 |
| Files shipped as course material | 0 — the bundle is entirely prose |

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
```

Five gaps listed in section 3, −3 each, −15 subtracted. The list and the arithmetic agree.

### A correction to the evidence script's own output, before anything is built on it

`audit.py` printed:

> COURSE.md has a coverage-list heading, "Rust coverage requirements", but it names no
> topics. This is a DIFFERENT finding from declaring none at all: the author started this
> section and never filled it in.

**That is wrong, and it is the script's parser, not the course.** `COURSE.md:221` is the
heading and `COURSE.md:225-271` is a fenced ```` ```text ```` block containing 46 named Rust
topics. The script's topic extractor evidently reads list items and not fenced blocks, so
it reported `topics: []` and `topic_candidates` for nothing. The same blindness applies to
the milestone block at `COURSE.md:187-209`.

The course **does** declare a boundary, in full, and section 3 below is scored against it.
The brief's assertion that "a coverage list is present" is the correct one; the script's
prose is the thing that is wrong. Worth reporting upstream to the skill's author, because
any future audit of a course that fences its coverage list will silently under-report.

---

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil found |
|---|---:|---|---|
| 00 — Rust foundations through an in-memory KV store | 21 | 11 of 11 | none |
| 01 — Rows, cells, and temporal visibility | 18 | 8 of 8 | none |
| 02 — Typed keys and the table hierarchy | 26 | 10 of 10 | none |
| 03 — The first deliberate refactor | 15 | 7 of 7 (one thinly — see below) | none |
| 04 — Tables and richer typed schemas | 14 | 7 of 7 | none |
| 05 — Canonical ordered binary keys | 15 | 7 of 7 | none |
| 06 — Define the data and query algebra | 15 | 5 of 5 | none |
| 07 — Ordered querying before automata | 13 | 5 of 5 | none |
| 08 — Build the automaton machinery | 23 | 9 of 9 | none |
| 09 — Automaton-native typed key queries | 12 | 7 of 7 | none |
| 10 — Storage engine I: durability | 16 | 7 of 7 | none |
| 11 — Storage engine II: automaton-aware segments | 16 | 7 of 7 | none |
| 12 — Concurrency and async Rust | 19 | 8 of 8 | none |
| 13 — gRPC server and Rust driver | 16 | 8 of 8 | none |
| 14 — Static distributed cluster and placement | 14 | 8 of 8 | none |
| 15 — Eventual replication and causal versions | 15 | 8 of 8 | none |
| 16 — General quorum systems | 17 | 7 of 7 | none |
| 17 — Convergence and repair | 16 | 8 of 8 | none |
| 18 — Gossip and membership | 13 | 7 of 7 | none |
| 19 — Live cluster reconfiguration | 15 | 8 of 8 | none |
| 20 — Online schema evolution | 14 | 7 of 7 | none |
| 21 — Strong consistency mode | 16 | 8 of 8 | none |
| 22 — Hardening and performance | 11 | 10 of 10 | **1 site, `22:63`** |
| **Sum** | **370** | | |

No lesson scores at or below zero, so the mandatory "every lesson ≤ 0 gets a breakdown"
rule fires for none of them. Breakdowns are given below for the lessons whose figure is not
obvious from the row: the two highest (02, 08), the lowest (22, 09), and every lesson
carrying a `+1` or `0` that a reader would otherwise have to guess at.

### 00 — 21 points

| `file:line` | Sentence | Score |
|---|---|---|
| `lessons/00-foundations.md:76` | "Create `automaton-db` with Cargo and run the generated binary." | 0 |
| `:77` | "Experiment with bindings, `String`, `&str`, function arguments, moves, and borrows." | +2 |
| `:78` | "Introduce a small entry struct and a `Vec<Entry>`." | +2 |
| `:79` | "Implement insertion and exact lookup by iterating the vector." | +2 |
| `:80` | "Use `Option` to represent missing keys." | +2 |
| `:81` | "Encounter and reason about returning a borrowed value from stored data." | +2 |
| `:82` | "Move behavior into a `Database` type with methods using `&self` and `&mut self`." | +2 |
| `:83` | "Replace the linear entry vector with `BTreeMap<String, String>`." | +2 |
| `:84` | "Add tests that protect insert/replace/lookup semantics." | +2 |
| `:85` | "Remove obsolete representations once the map replaces them." | +1 |
| `:89-:90` | "`cargo check` succeeds." / "`cargo test` succeeds." | 0 |
| `:95` | "The learner can explain the difference between moving `String`, borrowing `&String`, and borrowing `&str`." | +2 |
| `:97` | "The learner can explain why a returned borrowed value cannot outlive the database." | +2 |


`0 + (8 × 2) + 1 + 0 + 2 + 2 = 21`.

`:76` is the `npm install` case of this course and is discussed under rejected candidates
in section 4. `:85` is practice: the decision about what is obsolete was already made at
`:83`, and `COURSE.md:41-44` makes the cleanup a house rule rather than a fresh judgement.

### 01 — 18 points

Ten progression clauses at `:69-:80`, one validator line at `:84`, one explain-condition at
`:91`.

+2 each: `:69` "Introduce `Cell` with an owned value and optional validity bounds."; `:70`
"Add constructors/builders only when they are immediately exercised."; `:71` "Implement and
test `Cell::is_visible_at`."; `:72` "Introduce `Row` as a map from cell name to `Cell`.";
`:74` "Implement insertion/replacement semantics for a named cell."; `:76` "Implement lookup
that combines row and cell visibility."; `:77` "Add tests for missing cells, row expiry,
cell expiry, not-yet-valid cells, and exact boundaries."; `:91` "The learner can explain why
explicit-time visibility is easier to test and extend."

+1: `:73` "Add row expiry." and `:75` "Implement row visibility." — both re-apply the
half-open bound pattern constructed at `:69`/`:71` at a second nesting level. The repetition
is the point; the decision is not new.

0: `:79` "Discuss tombstones conceptually and defer their storage representation until the
surrounding update model is ready." — a deliberate deferral with no learner deliverable.
`:84` validator.

`(7 × 2) + 1 + 1 + 0 + 0 = 16`… restated in full: `:69 +2, :70 +2, :71 +2, :72 +2, :73 +1,
:74 +2, :75 +1, :76 +2, :77 +2, :79 0, :84 0, :91 +2` = **18**.

### 02 — 26 points, the highest in the course

Eleven progression clauses at `:89-:102`, every one of them a construction or a decision,
scored +2 each (= 22): `:89` `KeyValue` enum; `:90` distinct composite key types; `:91` "Add
only the traits demanded by `HashMap` and `BTreeMap`, using compiler diagnostics to
understand recursive trait bounds."; `:93` `Partition`; `:94` "Introduce `KeyType` and
`KeyColumn` only when they are immediately used to validate runtime key values."; `:96`
`Table`; `:97` `KeyColumn::matches`; `:98` hierarchical write path; `:99` table errors;
`:100` "Validate shape and type before mutating the table."; `:101` the five-case test set.

Plus `:106` validator (0), `:114` "The learner can explain why the local `HashMap` hash is
unrelated to future placement hashing." (+2), `:116` "The learner can explain the temporary
meaning of derived enum ordering." (+2).

`22 + 0 + 2 + 2 = 26`. See section 6 on whether this lesson is a size outlier.

### 03 — 15 points

+2: `:70` "Introduce `lib.rs` and move the existing engine implementation/tests out of the
binary while preserving compilation."; `:72` "Make the binary depend on the package library
through a deliberately small public API."; `:74` "Use compiler visibility errors to decide
what truly needs `pub`."; `:75` "Identify the first natural module boundaries among model,
keys/schema, and table responsibilities."; `:78` "Re-export only the API that the binary or
future clients should consume."; `:90` "The learner can explain why at least one `pub`
boundary was necessary."; `:91` "The learner can explain how the package can contain both
library and binary targets."

+1: `:77` "Move code in small increments and keep tests passing." — executes the boundary
decision taken at `:75`; the increments are discipline, not a new decision.

0: `:79` "Inspect the final diff for accidental behavior changes or representation leaks."
(read the diff — this is what the `git-diff` validator is for); `:83-:85` validators.

`(5 × 2) + 1 + 0 + 0 + (2 × 2) = 15`.

**Objective served thinly:** `:27` "Recognize when warnings reveal structural problems
versus ordinary private implementation detail." No progression clause and no completion
condition mentions warnings; the only warning content in the lesson is the constraint at
`:66`, "Use warnings as input, but do not suppress them wholesale with `allow(dead_code)`."
I ruled this **served, thinly** rather than a −3 gap: the constraint binds the learner
during `:70-:78`, which is a task, and `COURSE.md:41-44` makes dead-code warnings a
course-wide signal. A reader could defensibly disagree and charge −3; the proposal in
section 5 removes the ambiguity instead.

### 04 — 14 points

+2: `:63` "Refine primitive key types and decide which ones belong in the first stable
set."; `:64` "Add named typed value-column definitions."; `:66` "Add schema version
identity."; `:67` "Model permitted append-only schema changes."; `:68` "Introduce
codec-shaped abstractions for values only when a concrete typed value needs conversion.";
`:70` "Test valid and invalid schema evolution operations."

+1: `:62` "Introduce explicit table identity." (extends the `Table` built at `02:96`; no new
decision) and `:65` "Validate table schema construction." (second application of the
validate-before-mutate pattern taught at `02:100`).

0: `:74` validator; `:82` "The unresolved appended-clustering-component semantics remains
documented rather than silently assumed." — a recorded deferral, no construction.

`(6 × 2) + 1 + 1 + 0 + 0 = 14`.

### 05 — 15 points

+2: `:49` "Specify ordering invariants before writing encoders."; `:50` "Implement one
fixed-width type and test its order."; `:52` "Design and test variable-length UTF-8
framing."; `:53` "Compose components into tuple keys."; `:54` "Implement decoding and
malformed-input errors."; `:55` "Add property-based tests over generated keys."; `:56`
"Resolve the type-tag decision."

+1: `:51` "Add the remaining fixed-width types." — explicitly the repetition of `:50`.

0: `:60` validator; `:65` "The type-tag decision is recorded." (already scored at `:56`; the
recording is the evidence of it).

`(7 × 2) + 1 + 0 + 0 = 15`.

### 06 — 15 points

+2: `:45` "Write precise definitions for data entities."; `:46` "Define projection."; `:47`
"Define typed component predicates."; `:49` "Define temporal visibility interaction."; `:50`
"Represent the algebra as a typed Rust AST."; `:51` "Write semantic tests against the
existing in-memory engine."; `:58` "The learner can explain which operations belong to
logical semantics and which belong to execution."

+1: `:48` "Define value post-filter predicates." — the same shape as `:47`, one layer out.

`(7 × 2) + 1 = 15`.

### 07 — 13 points, and the smallest progression in the course

+2: `:47` "Add range bounds."; `:48` "Add prefix-like leading-component access."; `:49`
"Introduce a streaming query iterator."; `:50` "Combine several component constraints.";
`:51` "Measure or reason about the cases that still require scanning."; `:58` "The learner
can identify the class of middle-key predicates that motivates automata."

+1: `:46` "Implement exact ordered traversal." — `BTreeMap` lookup was built at `00:83` and
`02:110`; this is the third application.

0: `:55` validator.

`(6 × 2) + 1 + 0 = 13`.

### 08 — 23 points, the second highest

All ten progression clauses at `:54-:63` score +2 (= 20). Every one is a construction with a
wrong answer that teaches: `:54` "Review current Rust regex/automata/FST crates and select
comparison targets." (a selection, hence teaching not practice — this is the course's first
ecosystem checkpoint and it establishes the method); `:55` regex AST; `:56` Thompson NFA;
`:57` epsilon closure and subset construction; `:58` execute and test DFAs; `:59` DFA
minimization; `:60` finite-key trie; `:61` "Merge equivalent continuation states into an
acyclic deterministic automaton."; `:62` product/intersection traversal; `:63` "Compare
transition representations and allocations."

+2: `:71` "Benchmarks or measurements inform at least one representation decision." — a
decision, distinct from the measuring at `:63`.

+1: `:72` "A replacement checkpoint compares the implementation with mature crates." —
repeats the method established at `:54`.

`20 + 2 + 1 = 23`.

### 09 — 12 points, the second lowest

+2: `:47` "Compile one UTF-8 component predicate."; `:48` "Compile integer equality/ranges.";
`:50` "Compose multiple components through canonical framing."; `:51` "Connect product
traversal to row lookup."; `:53` "Benchmark a query whose selective predicate occurs after
an unconstrained/weak leading component."

+1: `:49` "Add fixed-byte predicates if present in the schema." — conditional repetition of
`:47-:48`, and the condition may not even hold. `:52` "Stream results." — iterator streaming
was constructed at `07:49`.

0: `:57` validator.

`(5 × 2) + 1 + 1 + 0 = 12`.

This is the lesson the whole course exists to reach — `COURSE.md:8` names automaton-native
ordered queries as the point of AutomatonDB — and it scores second-lowest, on seven terse
clauses. That is a sequencing observation, not a defect in the scoring: lessons 05, 06, 07
and 08 did the construction and 09 assembles it. It is nonetheless worth the author's
attention, and section 5 proposes what to do about it.

### 10 — 16 points

All eight progression clauses at `:50-:57` score +2 (= 16). `:65` "The durability
acknowledgement contract is documented." scores 0 — recording a contract already decided at
`:55`. `16 + 0 = 16`.

### 11 — 16 points

Eight of nine progression clauses score +2 (`:50-:57`, = 16). `:58` "Measure heap usage and
traversal performance." scores 0 — measure and report. `16 + 0 = 16`.

### 12 — 19 points

+2 ×9: `:56` threads with owned data; `:57` "Share engine state through `Arc`."; `:58` "Add
the smallest justified synchronization."; `:59` "Use channels for ownership transfer where
natural."; `:60` "Inspect `Send`/`Sync` compiler constraints."; `:61` "Build/inspect simple
futures and polling."; `:62` "Explain wakers and pinning."; `:64` "Add
cancellation/backpressure and a blocking-I/O strategy."; `:65` "Stress-test concurrent
operations."

`:62` is scored **+2 as a tutor-addressed element** under the rubric's settled rule: the
sentence is written at the tutor, and the learner must construct the explanation — which
`:72` "The learner can explain polling, wakeups, and why `Pin` exists at a practical level."
confirms. `:71` and `:72` are therefore **not** scored again; they are the completion checks
on `:60` and `:62`.

+1: `:63` "Adopt Tokio." — constraint `:51` already settles the choice ("Use Tokio after
understanding the conceptual model"), so no decision remains.

`(9 × 2) + 1 + 0 = 19`.

### 13 — 16 points

+2 ×7: `:50` protobuf schema; `:51` single-node put/get; `:52` Rust client; `:53` typed
query messages; `:54` result streaming; `:56` "Map errors deliberately."; `:57` "Add
compatibility tests."

+1: `:49` "Review current gRPC crates." — third instance of the ecosystem-checkpoint method,
and constraint `:42` ("use a mature Rust gRPC/protobuf stack") narrows the answer to
essentially one crate. `:55` "Add cancellation/backpressure." — constructed at `12:64`.

`(7 × 2) + 1 + 1 = 16`.

### 14 — 14 points

+2 ×6: `:50` failure domains/datacenters; `:51` "Implement stable partition hashing."; `:52`
"Compare/select placement strategy."; `:53` "Compute replica sets."; `:54` "Expose routing
metadata to the client."; `:55` "Add routing generation handling."

+1: `:49` "Define static cluster config and node IDs." (config plumbing around the model
decisions that follow) and `:57` "Exercise mixed host/container debugging." (constraint `:44`
"Address advertisement must work across host and container environments" makes it real work,
but the concept was already fixed at `:54`).

0: `:56` "Run multi-process and Compose clusters." — run it and see. Section 5 proposes a
`supplies:` entry here so this clause **stays** evidence instead of quietly becoming an hour
of YAML the lesson never admits to assigning.

`(6 × 2) + 1 + 1 + 0 = 14`.

### 15 — 15 points

+2 ×7 at `:49, :50, :51, :52, :53, :55, :56`. +1 at `:54` "Return siblings through the
driver." — plumbing an already-decided representation through the driver built at `13:52`.
`(7 × 2) + 1 = 15`.

### 16 — 17 points

+2 ×7: `:47` "Define policy interface and required guarantees."; `:48` majority; `:50` grid;
`:51` tree/hierarchical; `:52` topology/datacenter composition; `:53` "Test failure and
latency scenarios."; `:54` "Implement one learner-defined policy behind the same interface."
Plus `:61` "The learner can explain how topology and availability change the trade-offs."
(+2).

+1: `:49` "Implement weighted quorums." — the second construction through the interface
defined at `:47`; the repetition is exactly the point of the lesson.

`(7 × 2) + 1 + 2 = 17`.

### 17 — 16 points

All eight progression clauses at `:50-:57` score +2. `16`.

### 18 — 13 points

+2 ×6 at `:48, :49, :50, :51, :53, :55`. +1 at `:54` "Compare with mature membership
designs." (fourth ecosystem checkpoint). 0 at `:52` "Observe false positives." — observe and
report, which is what `:60` then checks. `(6 × 2) + 1 + 0 = 13`.

### 19 — 15 points

+2 ×7 at `:50, :51, :52, :53, :55, :56, :57`. +1 at `:54` "Refresh/redirect stale clients."
— stale routing generations were constructed at `14:55`. **0 at `:58` "Evaluate a stronger
reconfiguration protocol as an advanced path."** — this is a branch point, and the rubric
settles branch points at evidence, 0; the teaching is in whichever branch the learner takes.
`(7 × 2) + 1 + 0 = 15`.

### 20 — 14 points

+2 ×6 at `:48, :49, :51, :52, :53, :54`. +1 at `:47` "Distribute schema version identity."
(schema version identity was constructed at `04:66`; this distributes it) and `:50` "Append
value columns." (the append-only rules were modelled at `04:67`). `(6 × 2) + 1 + 1 = 14`.

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

`:56` is +2 rather than 0 because `:71` "Profiling has informed concrete changes." turns
reading a profile into a decision. `:57`, `:59` and `:60` are practice: they re-apply
methods already constructed at `:55`/`08:63`, `10:56` and `15:56`/`17:46`/`18:51`
respectively. `:63` is split; the toil half is argued in full in section 4.

---

## 3. Goal gaps

Five gaps, −3 each, −15 total. The list and section 1's arithmetic agree.

The gaps are all against the course's own declared coverage list at `COURSE.md:225-271`,
introduced by `COURSE.md:223`: "The main path should eventually exercise:". That is a
statement of required coverage, and each line in the fenced block is a stated objective.

| # | Gap | `file:line` | How I decided | Score |
|---|---|---|---|---|
| G1 | **interior mutability** | `COURSE.md:248` | `grep -rin "interior mutab\|RefCell\|Rc<"` across all 23 lessons returns nothing. The concept is named in no `## Concepts to teach`, no progression clause and no completion condition. Note that lesson 01 defines a domain type called `Cell` (`01:69`) — that is the database cell, not `std::cell::Cell`, and it is not a false positive I mistook for coverage. | −3 |
| G2 | **atomics** | `COURSE.md:250` | Named exactly once in the course, at `12:36` ("- atomics") inside `## Concepts to teach`. No progression clause and no completion condition requires one. `12:58` "Add the smallest justified synchronization." is satisfiable — and, given constraint `12:49`, most naturally satisfied — by a `Mutex` alone. A concept listed for the tutor to mention is not a task the learner performs. (The other `grep` hits for "atomic" are the `#atomicity` anchor, a different thing entirely, served at `10:54`.) | −3 |
| G3 | **associated types** | `COURSE.md:242` | Named once, at `04:47` ("- associated types when justified"), inside `## Concepts to teach` and behind an author's hedge. No progression clause requires one, and constraint `04:56` ("Avoid generic abstractions that are not exercised by real schema/value operations") pushes actively against introducing one. Lesson 16's "policy traits" (`16:33`) is the one place a `type Output` would be natural, and `16:47` does not ask for it. | −3 |
| G4 | **Cargo workspaces** | `COURSE.md:267` | The only two mentions in the bundle are `COURSE.md:67` (teaching philosophy: refactors should teach "workspaces") and `00:70`, which is a **prohibition**: "Do not introduce modules/workspaces merely for style." No later lesson ever lifts that prohibition. Lesson 03, the course's one structural-refactor lesson, produces `src/lib.rs` + `src/main.rs` — two targets in one package, not a workspace. | −3 |
| G5 | **refactoring across crate boundaries** | `COURSE.md:269` | Same evidence as G4 and listed as its own line in the coverage block, so counted as its own gap per the rubric's per-gap rule. Lesson 03 refactors across a **target** boundary inside one crate (`03:33` "src/main.rs is the root of a binary target. src/lib.rs is the root of the package's library target."). The course never has more than one crate, so a cross-crate refactor is not possible in it as written. One lesson would close G4 and G5 together; they are still two stated objectives and are counted as two. | −3 |

### Coverage-list topics I checked and ruled **served**, so the next reader does not redo it

- **smart pointers** (`COURSE.md:246`) — listed separately from `Arc`, so `Arc` alone does
  not discharge it. It is nonetheless served: `06:50` "Represent the algebra as a typed Rust
  AST." and `08:55` "Define a small regex AST." both require a **recursive enum**
  (`06:33`, `08:34` name recursive enums explicitly), and a recursive enum cannot compile in
  Rust without heap indirection. `Box` is never named in the bundle, but a task forces the
  learner to meet one. Served, and worth naming explicitly in lesson 06.
- **macros and derive usage** (`COURSE.md:266`) — the line says *usage*, not authoring.
  Derive usage is pervasive (`02:64` "`PartialEq`, `Eq`, `Hash`, `PartialOrd`, `Ord`"),
  macro usage likewise (`02:62` "`matches!`", `02:127` "Compare `matches!` with a full
  `match` expression"). Served.
- **platform/FFI APIs if naturally required** (`COURSE.md:270`) — the line carries its own
  hedge. `11:53` "Add mmap." and `22:50` "Include Linux-specific I/O experiments where
  production behavior differs from macOS." satisfy it. Served.
- **RAII and Drop** (`COURSE.md:260`) — `10:35-36` names both, and `10:45` "Do not rely on
  destructor timing alone for durability guarantees." makes `Drop` semantics load-bearing in
  a task. Served.
- **unit/integration/property testing** — unit at `00:84`, property at `05:55`, integration
  at `03:103` (optional deeper path) and, on the main path, at `13:57` "Add compatibility
  tests." and `20:54` "Run mixed-version tests." Served.

### `DESIGN.md` anchors: all 23 served — and the brief's premise about them does not hold

The brief warned that "23 anchors and 23 lessons is a suspiciously tidy one-to-one" and told
me to expect the mapping to break. **The premise is wrong, and I am saying so rather than
working around it.** The two counts coincide arithmetically and there is no one-to-one
mapping at all, tidy or otherwise:

- lesson 00 carries **no `design_refs` at all** (`lessons/00-foundations.md:1-5` has no such
  key) and serves no anchor — correctly, since it is pure Rust foundations;
- `#table-model` is cited by 7 lessons and `#key-ordering` by 7, while `#membership` and
  `#networking` are each cited by exactly one;
- the citation counts total 89 `design_refs` entries across 22 lessons.

So there was never a 1:1 structure to break. Judged the right way — on what tasks make the
learner **do**, never on `design_refs` — **all 23 anchors are served**, and I charge none of
them. The per-anchor rulings, each naming the task rather than the citation:

`#table-model` 02:93/:96/:98 · `#partition-key` 02:90, 14:51 · `#clustering-key` 02:90,
05:53, 07:48, 09:50 · `#key-component-types` 04:63, 05:51, with its Unresolved item resolved
at 05:56 · `#key-ordering` 05:49-:53 · `#row-cell-model` 01:69/:72, 02:93 · `#values` 04:64,
04:68 · `#temporal-semantics` 01:71/:75/:76, 06:49, 11:56 · `#deletion` 11:56, 17:55/:56 —
see the partial gap below · `#atomicity` 10:54 · `#conditional-operations` 15:55, 21:53 ·
`#durability` 10:55, 15:50 · `#automaton-index` 08:60/:61/:62, 09:51, 11:52 · `#placement`
14:51/:52/:53 · `#smart-clients` 13:52, 14:54 · `#networking` 13:50/:51 · `#replication`
15:49 · `#quorums` 16:47-:54 · `#strong-consistency` 21:49/:51/:52 · `#membership`
18:48-:50 · `#live-reconfiguration` 19:50-:57 · `#topology` 14:50, 16:52 ·
`#schema-evolution` 04:67, 20:51/:52.

### Two partial gaps: named, argued, and deliberately **not** charged −3

Both are real defects. Neither meets the rubric's test ("an anchor that **no** task
exercises"), so charging −3 would be dishonest arithmetic. Both get proposals in section 5.

**P1 — `#deletion`: tombstones are integrated for a delete path the learner is never asked
to build.** `DESIGN.md:118-124` opens "Support row deletion and individual-cell deletion
using tombstone semantics so replicas can distinguish deletion from absence." Grepping every
progression clause and completion condition in all 23 lessons for `delete`/`deletion` as an
**operation** returns nothing. `01:79` explicitly defers it ("Discuss tombstones conceptually
and defer their storage representation"). `06:43-:51`, the query-algebra lesson, defines
projection, predicates and post-filters — and no delete. `13:51` serves "single-node put/get
operations" only; there is no Delete RPC anywhere in `13:49-:57`. Yet `11:56` says "Integrate
tombstones/expiry." and `17:55-:56` say "Integrate tombstones." and "Define and test safe
tombstone collection." The anchor **is** exercised — by 11 and 17 — so no −3. But the course
asks the learner to garbage-collect tombstones that nothing in the course produces.

**P2 — `#values` is the one anchor whose declared Unresolved item no lesson resolves.**
`DESIGN.md:5` sets the contract: "Deliberately unresolved items are marked explicitly and
are expected to be resolved in later lessons." There are exactly three such items.
`#key-component-types` (`DESIGN.md:51-52`) is resolved by a task: `05:56` "Resolve the
type-tag decision." `#schema-evolution` (`DESIGN.md:275-277`) is resolved by a task: `20:52`
"Resolve semantics for pre-existing rows.", reinforced by constraint `20:42`. `#values`
(`DESIGN.md:85-86`, "exact boundary between schema-level typed values and storage-level
opaque bytes") is resolved by **no** task: `04:54` forbids settling it ("Do not finalize
canonical bytes in this lesson"), lesson 11 designs the segment layout at `11:50` without
ever naming the boundary, and no later lesson returns to it. Two of three unresolved items
land; the third never does.

---

## 4. The toil inventory

### Confirmed toil: one site

**`lessons/22-hardening-performance.md:63`** — the exact sentence, quoted whole:

> `9. Build CI and reproducible clusters.`

The clause is split, as the skill instructs, and only the first half is charged:

- **"Build CI" — toil, −2.** The first CI file for a Rust project (a workflow that runs
  `cargo build`, `cargo test`, `cargo fmt --check`, `cargo clippy` on push) is deterministic,
  has essentially one right answer, and a mistake in it teaches nothing about Rust,
  automata, storage or distributed systems — it teaches YAML indentation. And the last
  clause of the toil row is satisfied: **the bundle could have shipped it.** A CI workflow is
  a static text file inside the bundle; nothing about it needs the network, a toolchain or an
  account at authoring time. The course ships zero files and declares zero `supplies:`
  entries, so it did not. Completion condition `22:73` ("CI protects correctness and
  compatibility.") makes it a required deliverable rather than an aside.
- **"…and reproducible clusters" — practice, +1.** Deciding what "reproducible" means for a
  multi-process cluster under fault injection is real engineering that builds on `14:56` and
  `18:51`. Not toil.

**Where a reader may disagree, stated openly:** CI for *this* course is not only the
boilerplate half — `22:73` also wants compatibility gates and `22:69` wants crash and
network-partition tests running reproducibly, and wiring those into CI is genuine work. My
ruling charges the boilerplate half and credits the rest. An author who reads `:63` as
entirely the hard half should say so and the −2 comes off, taking lesson 22 to 13 and the
course to 357. The split is the honest reading of a clause that contains both.

### Script candidates examined and rejected

The scanner produced **one** candidate across 23 lessons. I opened it and rejected it, and
then opened every lesson anyway.

| Candidate | Verdict |
|---|---|
| `lessons/03-first-refactor.md:23` — pattern `move` — "Move engine code out of `main.rs` without changing behavior." | **Rejected, and not even a task.** The line is item 2 of `## Learning objectives` (`03:20-:29`), not a progression clause. More to the point, the move *is* the lesson: `03:74` "Use compiler visibility errors to decide what truly needs `pub`." and `03:75` "Identify the first natural module boundaries among model, keys/schema, and table responsibilities." are decisions with instructive wrong answers (marking everything `pub`, which constraint `03:62` names directly). And the bundle could not have shipped the result: the code being moved is the learner's own, written across lessons 00-02, and `tutorial.yaml:39` puts `src/**` under `learner_owned`. Scored +2 at `03:70`. |

### Candidates I raised myself from reading the lessons, and rejected

Named here so the next reader does not re-litigate them. The three marked **could not have
supplied** are rejections of exactly the kind the skill asks to be named as such.

| Site | Sentence | Verdict |
|---|---|---|
| `00:76` | "Create `automaton-db` with Cargo and run the generated binary." | **Rejected — could not have supplied.** This is this course's `npm install`. `cargo new` needs the toolchain, and `tutorial.yaml:39` makes `Cargo.toml` and `Cargo.lock` learner-owned by design. No `supplies:` entry can create a Cargo project in a workspace the bundle does not own. Setup that needs a toolchain is the learner's work. Scored **evidence, 0** — what it actually is. |

| `03:77` | "Move code in small increments and keep tests passing." | **Rejected — could not have supplied.** The code is the learner's, from lessons 00-02. Practice, +1. |
| `13:50` | "Define a minimal protobuf schema." | **Rejected.** A `.proto` file is exactly the kind of thing a bundle can ship — but constraint `13:44` and theory `13:29` ("Internal Rust types should not leak directly into the protocol merely because serialization is convenient") make the schema's shape the lesson's central decision. Shipping it would delete the teaching. +2. |
| `14:56` | "Run multi-process and Compose clusters." | **Rejected as written, with a caveat that becomes a proposal.** *Running* a cluster is evidence, 0. But the `docker-compose.yml` and the multi-process launcher this clause presupposes are never assigned by any clause, and they are precisely what a `supplies:` entry is for. Unassigned toil is not chargeable toil; it is a hole. See proposal 3. |
| `22:62` | "Instrument metrics/tracing." | **Rejected.** Adding `tracing` spans is repetitive, but `22:72` ("Metrics/tracing expose major system behavior.") requires deciding *what* is major. Practice, +1, not toil. |
| `22:55` | "Establish benchmark baselines." | **Rejected.** Running benchmarks and recording numbers is evidence, 0, not toil — nothing here could have been shipped, since the baselines are of the learner's own implementation. |
| Every lesson's `## On completion, persist` section, e.g. `21:68` | "Persist the strong-mode guarantee/protocol in `DESIGN.md`; record consistency/protocol concepts in `STATE.md`." | **Rejected — not the learner's work at all.** `tutorial.yaml:38` makes `tutorial/STATE.md` and `tutorial/DESIGN.md` tutor-owned. Twenty-three near-identical bookkeeping instructions look like busywork, but they are addressed to the tutor and the learner does nothing in response, so the rubric's tutor-addressed rule sends them to **not scored** rather than to +2. |
| The `## Optional deeper paths` block in lessons 05-22 | "Offer relevant papers, proofs, implementation archaeology, or formal models when the learner asks and the material would deepen the topic without replacing the main path." | **Rejected as toil** — it assigns the learner nothing and is therefore unscorable. It is a **quality finding** all the same: this exact sentence is repeated verbatim in 18 of 23 lessons, while lessons 00-04 each carry three specific, lesson-shaped deeper paths (`00:108-110`, `01:103-106`, `02:127-130`, `03:103-105`, `04:93-94`). See proposal 5. |

### The scanner is a candidate generator

`audit.py` fires on a fixed list of verbs in imperative position and reports which verb
fired; it cannot see toil it has no pattern for, and its one hit here was a false positive in
a `## Learning objectives` block. **Its silence across 23 lessons is evidence about the
verb list, not about this course.** The inventory above came from opening all 23 lessons and
scoring 191 elements — every progression clause and every distinct completion condition.

The genuinely notable fact about toil in this bundle is structural: **it ships zero files
and declares zero `supplies:` entries**, so almost nothing in it *could* have been handed
over, and the toil row's last clause disarms nearly every candidate before it is raised. The
one place it does not disarm is `22:63`.

---

> **OPEN, `tutorail-authoring#11` — the `00:76` rejection above.** A single-language course
> can ship a `Cargo.toml` and a `src/` skeleton outright, so "could not have supplied" is
> too strong here as well. The element scored 0, so a toil ruling moves the course to
> **353** (`skomp/tutorail-bundles#3`).

## 5. Proposals

Every one is a concrete action. All are refusable, and applying any of them is the
`tutorail-authoring` skill's job, not this one's.

**Proposal 1 — ship the CI workflow and delete the boilerplate half of `22:63`.** This is
the report's one toil fix.

```
cd /Users/robert/.claude/plugins/cache/tutorail-authoring/tutorail-authoring/0.3.0/skills/tutorail-authoring
python3 scripts/supplies.py add /Users/robert/src/github.com/skomp/tutorail-bundles/rust-automaton-db \
  --from lessons/22-hardening-performance/ci.yml \
  --to .github/workflows/ci.yml \
  --describe "Baseline CI workflow: cargo build, test, fmt --check and clippy on push and PR. Extend it in this lesson with the fuzz, crash and partition jobs." \
  --lesson 22-hardening-performance \
  --check
```

Two things must happen before that command can run, and both are part of the fix:

1. **The bundle has no lesson folders.** Lessons are flat files (`lessons/22-hardening-performance.md`).
   A `--lesson`-scoped `--from` must live inside that lesson's own folder under `lessons/`,
   because materialization copies only `lessons/` into the instance. So lesson 22 becomes a
   directory: `lessons/22-hardening-performance/LESSON.md` plus `ci.yml`. That is a
   `tutorail-authoring` restructure, and it should be done through the toolkit so
   `tutorial.yaml:35` is rewritten consistently.
2. If the author prefers not to restructure, use a **manifest-scope** entry instead — drop
   `--lesson` and put `ci.yml` at the bundle root. Manifest scope has no `lessons/`
   restriction. The trade-off is that the file is placed when the course opens rather than
   when lesson 22 does.

Prose to delete once the entry exists: in `lessons/22-hardening-performance.md:63`, change
`9. Build CI and reproducible clusters.` to `9. Extend the supplied CI workflow with fuzz,
crash and partition jobs, and make the test clusters reproducible in it.` Completion
condition `:73` ("CI protects correctness and compatibility.") stays as it is — it is then
about the part that teaches. **Do not remove the clause without adding the supplies entry**,
or the learner reaches `:73` with no CI at all.

**Proposal 2 — close the five coverage gaps, and note that four of the five want one new
lesson between 03 and 04.** G4 (Cargo workspaces) and G5 (refactoring across crate
boundaries) are the same missing material; G3 (associated types) and G2 (atomics) are
homeless concepts that a second refactor lesson naturally houses. Concretely, one of:

- **(a) Add `lessons/04-workspace-split.md`, renumbering 04-22 upward.** Placement: after 03
  and before the schema lesson, where `COURSE.md:66-68` says structure should evolve under
  pressure. It cites `#table-model` and teaches: split the package into a workspace with at
  least two crates (an `automaton-db-core` and the binary), decide the dependency direction,
  move the tests that follow the code, and meet the `pub`/`pub(crate)` boundary a second time
  at a boundary the compiler enforces harder. That closes G4 and G5. This is the honest fix,
  and it costs a renumber across `tutorial.yaml:16-35` and 19 lesson files — do it through
  the toolkit, never by hand.
- **(b) Argue the two lines out of `COURSE.md`.** A defensible case exists: a single-package
  course with a clean `lib.rs`/`main.rs` split teaches module boundaries well, and a
  workspace added only to tick a coverage line is the "front-loading a final architecture"
  that `COURSE.md:68` warns against. If the author takes this route, **delete lines 267 and
  269 from the coverage block** rather than leaving them stated and unserved. Both outcomes
  are acceptable; leaving the gap named and unaddressed is not.

For **G1 (interior mutability)**, **G2 (atomics)** and **G3 (associated types)**, the same
choice applies per topic. My recommendation, in one line each:

- **atomics** — add a progression clause to lesson 12 between `:58` and `:59`: "Replace one
  lock-protected counter or flag with an atomic, and state the ordering you chose and why."
  It is a decision, it has instructive wrong answers, and `12:37` already promises it.
- **interior mutability** — add a clause to lesson 11 or 12 where a reader cache or a lazily
  built segment index behind `&self` genuinely needs it; `11:55` "Merge memtable/segments in
  reads." is the natural site. Do **not** add a synthetic exercise: `COURSE.md:273-274`
  permits "a compact side exercise" as the fallback, but this course has a real place for it.
- **associated types** — lesson 16's quorum policy trait (`16:47`) is the one place an
  associated type is genuinely justified rather than decorative. Either say so in `16:47`, or
  strike `COURSE.md:242`.

**Proposal 3 — declare the cluster harness lesson 14 presupposes.** `14:56` says "Run
multi-process and Compose clusters." and `14:65` requires "The development cluster works in
at least local multi-process and Compose modes." — but no clause ever asks the learner to
*write* a Compose file or a launcher, and the bundle does not supply one. Either the learner
silently spends an hour on YAML the lesson never admits to assigning (toil that would then be
chargeable), or they stall. Ship it:

```
cd /Users/robert/.claude/plugins/cache/tutorail-authoring/tutorail-authoring/0.3.0/skills/tutorail-authoring
python3 scripts/supplies.py add /Users/robert/src/github.com/skomp/tutorail-bundles/rust-automaton-db \
  --from lessons/14-static-cluster-placement/docker-compose.yml \
  --to docker-compose.yml \
  --describe "Three-node development cluster. Node identity and advertised address come from environment variables the learner wires up in this lesson." \
  --lesson 14-static-cluster-placement \
  --check
```

Same folder restructure caveat as proposal 1. The teaching is preserved deliberately: the
compose file supplies the *topology*, and constraint `14:44` ("Address advertisement must
work across host and container environments") stays the learner's problem, which is where the
lesson's difficulty actually lives.

**Proposal 4 — fix the four `design_refs` citations that answer nothing, and close the
delete-path hole (P1).** Two edits, both small:

- Remove `conditional-operations` from `lessons/13-grpc-driver.md:4`, or add a clause to
  `13:49-:57` defining the conditional-write RPC. Remove `atomicity` from
  `lessons/01-rows-cells-temporal.md:4` and `lessons/12-concurrency-async.md:4`, or give each
  a clause that exercises it. Remove `deletion` from `lessons/10-storage-durability.md:4`, or
  give lesson 10 a tombstone WAL record. Detail and `file:line` for each in section 6.
- **P1**: add "Implement row and cell deletion with tombstone records." as a clause in
  lesson 01 (replacing the pure deferral at `01:79`, which can keep its "defer the *storage*
  representation" half), add a delete node to the query algebra at `06:43-:51`, and add a
  Delete RPC to `13:49-:57`. Without this, `11:56` and `17:55` ask the learner to compact and
  garbage-collect tombstones that the course never taught them to create.

**Proposal 5 — give lessons 05-22 real `## Optional deeper paths`, or drop the section.**
The identical sentence "Offer relevant papers, proofs, implementation archaeology, or formal
models when the learner asks…" appears verbatim in 18 lessons, while `00:108-110`,
`01:103-106`, `02:127-130`, `03:103-105` and `04:93-94` each name three concrete excursions.
A tutor reading the generic form has nothing to offer that it did not already know.
Lesson 08 alone wants Myhill-Nerode and Hopcroft by name, lesson 21 wants Paxos/Raft/ABD,
lesson 17 wants Merkle trees and the Dynamo paper, lesson 18 wants SWIM and φ-accrual. This
costs the score nothing and is the cheapest quality win in the bundle.

**Proposal 6 — resolve `#values`'s Unresolved item somewhere (P2).** `DESIGN.md:5` promises
every unresolved item is resolved in a later lesson; two of three are, and
`DESIGN.md:85-86` is not. Add "Fix the boundary between schema-level typed values and
storage-level opaque bytes, and record it." as a clause in lesson 11 (after `11:50`, where
the segment layout forces the question anyway), and add the matching completion condition.
Alternatively, strike the **Unresolved** marker from `DESIGN.md:85-86` and state the boundary
in the design document — but then `04:68` should stop calling codecs provisional.

**Proposal 7 — a question for the author about lesson 09, not a deletion proposal.**
Lesson 09 scores 12, second-lowest in the course, and it is the lesson the whole course
exists to reach (`COURSE.md:8`, `COURSE.md:14-15`). Its seven clauses are `09:47-:53`, two of
which are practice (`:49` "Add fixed-byte predicates **if present in the schema**." — which
may not fire at all; `:52` "Stream results." — built at `07:49`), and it has one validator
line and no "the learner can explain" condition, unlike 00, 01, 02, 03, 06, 07, 12 and 16.
The question: **is 09 thin because 05-08 correctly did the construction and 09 assembles, or
because the assembly step was written in a hurry?** If the former, say so and nothing needs
to change. If the latter, the cheapest fix is an explain-condition at `09:55-:60` — for
example "The learner can explain why the composed automaton prunes where a prefix scan plus
post-filter would not." — which converts the lesson's central insight from something the
learner might absorb into something they must state.

**Proposal 8 — report the coverage-list parser bug upstream.** `audit.py` reads coverage-list
topics from list items only and returns `topics: []` for a fenced block, then prints prose
asserting the author "started this section and never filled it in." For this bundle that
statement is false and, taken at face value, would have suppressed the entire five-gap
finding in section 3. This is a defect in the `course-quality` skill's script, not in
`rust-automaton-db`, and it belongs in that skill's issue tracker.

---

## 6. The questions only a reader can answer

None of these is scored. All of them change what the author does next.

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

**Four instances found.** Each is a citation that resolves, in a lesson whose tasks never go
near what the anchor decides. The validator is green for all four.

| `file:line` | The citation | Why it answers nothing |
|---|---|---|
| `lessons/13-grpc-driver.md:4` | `conditional-operations` | `DESIGN.md:136-142` requires compare-and-set, `IF NOT EXISTS` and read-modify-write, and insists "Do not present conditional syntax without stating its consistency semantics." Grepping lesson 13 for `conditional`, `CAS`, `compare-and-set` and `IF NOT EXISTS` returns **only the `design_refs` line itself**. `13:51` serves "single-node put/get operations"; `13:53` adds "typed query messages". A learner who follows this reference finds a design decision the lesson never touches. |
| `lessons/01-rows-cells-temporal.md:4` | `atomicity` | `DESIGN.md:126-134`: "Multiple changed cells in one row commit atomically." The word `atomic` does not appear in lesson 01 outside that frontmatter line. `01:74` is "Implement insertion/replacement semantics for **a named cell**" — single-cell, the opposite of the multi-cell guarantee the anchor states. The anchor is genuinely served, but at `10:54`, nine lessons later. |
| `lessons/12-concurrency-async.md:4` | `atomicity` | Same test, same result: `atomic` appears in lesson 12 only at `:36` ("- atomics", the unrelated Rust primitive, and itself gap G2). The concurrency lesson is exactly where "one logical row write is atomic" becomes interesting under `Arc` and locks, and `12:69` ("Concurrent local operations preserve documented invariants.") gestures at it without naming it. |
| `lessons/10-storage-durability.md:4` | `deletion` | `deletion`, `delete` and `tombstone` appear in lesson 10 **only** in that frontmatter line — not in `## Theory`, not in `## Concepts to teach`, not in any of the eight progression clauses at `:50-:57`, not in the completion conditions. The WAL is where a tombstone record would first become physical. |

The pattern across all four: the anchor is served **somewhere**, and the citing lesson is not
where. Fixes are in proposal 4.

### 6.2 A lesson that introduces a type or concept nothing later uses

**One clear instance, plus two weaker ones named for completeness.**

**Timestamps as a key component type.** `lessons/05-canonical-ordered-keys.md:20` states the
objective "encode unsigned integers, fixed bytes, UTF-8 components, and **timestamps**", and
`05:51` ("Add the remaining fixed-width types.") makes the learner build a timestamp encoder
and its ordering tests. Nothing later uses it. `lessons/09-automaton-native-key-queries.md`
compiles exactly three predicate kinds — `:47` UTF-8, `:48` integer equality/ranges, `:49`
fixed-byte — and never a timestamp predicate. `grep -rin timestamp` across all 23 lessons
returns `05:20`, an optional deeper path at `01:103` about wall-clock semantics, and nothing
else. `DESIGN.md:43-44` is the source of the mismatch: it puts timestamps among "**likely
later additions**", not the initial set, and `04:63` ("Refine primitive key types and decide
which ones belong in the first stable set.") explicitly lets the learner decide — after which
`05:20` mandates the encoder regardless of what they decided. **It cost the learner attention
and bought the course nothing.** Either add a timestamp predicate to `09:47-:49` (a
range-over-canonical-bytes predicate on a time component is a genuinely good exercise and
would strengthen the course's flagship lesson), or make `05:20`'s timestamp clause
conditional on the stable set chosen at `04:63`, the way `09:49` is already conditional
("if present in the schema").

**Weaker, named so they are not re-found:** `Display` and `Formatter<'_>` at `01:51` are
introduced in `## Concepts to teach` and never used again — `Debug` recurs through derives,
`Display` does not. And the provisional derived-enum ordering at `02:51-:53` looks like a
dead end but is **not** one: it is explicitly temporary (`02:77` "Do not pretend derived enum
ordering is the final physical key encoding"), it is the thing lesson 05 replaces, and
`02:116` makes the learner explain its temporary meaning. That one is correct as written.

### 6.3 A lesson far outside the course's usual size, in either direction

Answered on two measures, because they disagree and the disagreement is the finding.

**By scored elements (the measure the rubric cares about), the course is remarkably
uniform.** Progression clauses per lesson: 6, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9,
10, 10, 10, 10, 10, 11. Median 8, range 6-11 — a 1.8× spread with no outlier. Scores run 11
to 26, median 15. **No lesson is far outside the course's usual size on this measure.**

**By prose length, the distribution is bimodal, and that is a house-style seam rather than an
outlier.** Line counts:

| Band | Lessons | Lines |
|---|---|---|
| Long-form | 00, 01, 02, 03, 04 | 110, 106, **130**, 105, 94 |
| Terse | 05-22 | **67** to 83, median 73.5 |

- **Upper outlier: `lessons/02-typed-keys-table-hierarchy.md:1-130`**, 130 lines — 1.94× the
  course median (73) and the largest lesson by every measure: 10 objectives, 11 progression
  clauses, 10 completion conditions, 26 points. Content: `KeyValue` enums, composite
  partition/clustering key types, derived trait bounds, `HashMap` vs `BTreeMap`, the `Entry`
  API, `KeyType`/`KeyColumn` schema, `Table`, `Result` and a domain error enum, and
  validation-before-mutation. The rubric's note applies: a lesson much larger than its
  neighbours is usually two. **My ruling: it is one lesson and should stay one.** Every piece
  of it is forced by the single act of stopping treating a row key as a string, and splitting
  it would leave the first half with a key type no storage path uses. It is large because
  that step is large. Worth telling the tutor so, though: `COURSE.md:70-72` already says a
  lesson may span multiple task cycles, and lesson 02 is the clearest case of it in the
  course.
- **Lower outliers: `lessons/06-data-query-algebra.md:1-67` and
  `lessons/07-ordered-querying.md:1-67`**, 67 lines each, and `07` also has the course's
  smallest progression (6 clauses, `07:46-:51`). The rubric's note — "one that is much
  smaller is usually a paragraph of the lesson beside it" — **does not hold for 06**, which
  is a deliberate semantics-before-execution firebreak (`06:26` "Automata are an execution
  technique, not query semantics… This prevents the automaton engine from accidentally
  defining the public model."). That is a real architectural decision and it earns its own
  lesson. For **07** the case is closer: its six clauses are the ordered-access baseline whose
  whole purpose is to motivate lesson 08, and `07:58` ("The learner can identify the class of
  middle-key predicates that motivates automata.") is arguably the last paragraph of 06 or
  the first of 08. **My ruling: keep 07 separate.** The learner needs working range queries in
  hand before automata are justified, and folding it into 08 would make the course's largest
  concept jump larger.
- **The real size finding is the seam, not any single lesson.** Lessons 00-04 average 109
  lines and carry lesson-specific `Prerequisites` (`01:18` "`00-foundations`"), rich `Theory`,
  and three bespoke deeper paths each. Lessons 05-22 average 74 lines and carry the
  placeholder `Prerequisites` "- The preceding course lesson." (`05:14` and 17 more) and one
  generic deeper-path sentence. The course reads as hand-written through 04 and generated
  from 05 on. It does not change any score — the progression clauses are uniformly good
  — but it is the thing an author would most want to know, and proposal 5 is the cheap half
  of the fix. Naming the real prerequisite lesson id in each of the 18 terse lessons, as
  `01:18` and `02:26` do, is the other half.

### 6.4 A must-cover topic that only an optional lesson teaches

**Not applicable, and no instance is possible.** The course declares no optional lessons at
all (see 6.5), so no topic in the coverage block at `COURSE.md:225-271` can be reachable only
through an offer a learner may decline. The rubric's question — *is that acceptable for this
course, given that a learner who declines every offer never meets it?* — has no subject here.

For the avoidance of doubt about a near-miss: `COURSE.md:276-284` is headed "Optional paths"
and lists historical/as-of reads, secondary indexes, partition splitting, a textual query
language and a dozen more. **These are not optional lessons and not coverage-list topics.**
They are explicitly framed as "Optional later work" beyond the course, they are named in no
manifest key, and no lesson exists for any of them. They are outside the coverage boundary,
so nothing is owed for them. Likewise the 18 `## Optional deeper paths` sections are
within-lesson excursions offered by the tutor, not lessons.

### 6.5 The completability invariant, asked out loud

> **Can a learner who declines every offer still finish this course?**

**Not applicable — no optional lessons are declared.** And, as the rubric requires, that
claim is checked against the lessons and not only against the manifest:

- **Manifest.** `tutorial.yaml` has no `optional_lessons:` key at all — `:12-:35` is a flat
  `lessons:` list of 23 files and the next key is `workspace_kind:` at `:37`. I keyed this off
  the **presence of the key**, not off the script's `optional_lesson_count`, precisely
  because that count is of optional lessons found on disk and would report zero for a
  manifest naming a file that does not exist. The key is absent, so there is nothing to
  mis-count and **no `required_for`, `anticipates` or `repair_in` fields exist anywhere in
  the bundle.**
- **Consequence for the score.** Zero `required_for` gates, so the rubric's −3 gate row fires
  zero times and contributes 0 to the arithmetic in section 1. The warning that accompanies
  that row is not printed because no gate exists to which it could apply.
- **Prose check — prose optionality is not optionality.** I read all 23 lessons looking for
  the webgl failure mode: a lesson its own text calls optional while sitting in `lessons:`.
  **None found.** No lesson title contains "optional"; no lesson's `## Purpose` or prose
  describes the lesson itself as skippable; no lesson's `## Prerequisites` says the previous
  lesson may have been skipped. The only uses of the word "optional" in the bundle are (a)
  the `## Optional deeper paths` heading in all 23 lessons, which offers excursions *within*
  a required lesson, (b) `COURSE.md:276` "Optional paths", which lists work beyond the course
  entirely, (c) `COURSE.md:51` "Nightly features may be optional excursions", (d)
  `19:58` "Evaluate a stronger reconfiguration protocol as an advanced path", a branch point
  inside a required lesson, scored 0, and (e) ordinary uses of `Option<T>` and "optional
  temporal bounds". **The manifest and the prose agree.** There is no second total to report,
  and the 355 in section 1 is the only total this course has.
- **The invariant itself.** No main-path completion condition can depend on something only an
  optional lesson builds, because there are no optional lessons. Every one of the 23 lessons
  is required, every prerequisite chain is linear (`00 → 01 → 02 → 03 → 04 → …`, stated at
  `01:18`, `02:26`, `03:18`, `04:15` and as "The preceding course lesson." in 05-22), and
  a learner who declines nothing and skips nothing is the only learner this course describes.
  **Invariant not at risk.**

---

## Closing note on method

The bundle loads cleanly and its structural tooling is satisfied. That fact appears nowhere
in the 355 above and is not an answer to anything in this report: the validator answers "is
this a bundle?", and this report answers "does this teach?". On the evidence of 191 scored
elements across 23 lessons, it teaches well — the density of `teaching` elements is high
throughout, the course consistently makes the learner decide rather than transcribe, and it
carries a single confirmed toil site in 1,869 lines. Its weaknesses are five coverage topics
it stated and never assigned, four citations that point at decisions their lessons never
make, a delete operation it garbage-collects but never builds, and a visible seam at lesson
05 where the writing changes hands.

Every figure here is checkable against a `file:line` and a quoted sentence, and every one of
them is a proposal the author may refuse.
