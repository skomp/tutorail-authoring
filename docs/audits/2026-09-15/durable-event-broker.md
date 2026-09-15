# Course-quality audit: `durable-event-broker`

Audited read-only on 2026-09-15. Nothing in the bundle was created, edited, staged or
deleted; `git status --porcelain` in `skomp/tutorail-bundles` was empty before this audit
began and empty after it finished.

## Provenance

Reproduced verbatim from the run's provenance record, because a green validator line is a
claim about a machine on a day unless it records which copy of the validator and which YAML
reader produced it.

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

Re-run here for this bundle alone, against the pinned directory, and confirmed:

```
tutorAIl validator - mode: bundle
target:      /Users/robert/src/github.com/skomp/tutorail-bundles/durable-event-broker
yaml reader: restricted (built in, stdlib only)
...
  [22] ran     supplies entries are well-formed, and every 'from' resolves where the
               runner will look for it  (1 supplies entry across 1 declaration site)
...
PASS - every applicable check ran and found nothing.
EXIT=0
```

That is a real run, not a `FAIL - 0 finding(s)`: 26 checks are listed by name, check 22
reports the count of supplies entries it inspected, and the exit code is 0. **The validator
was not changed and no finding in this report may reject a bundle.** Structural validity
and teaching quality are different questions; "the validator passes" was never an input to
any figure below.

**Baseline for every delta:** `docs/audits/2026-09-13/durable-event-broker.md`, which scored
this bundle at commit `4df2624` — course total **128**, main path **108**.

---

## The rubric, printed

Printed in full because a reader given only a number argues with the number.

### The scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises. Course-level, counted once PER UNSERVED OBJECTIVE |
| **`required_for` on an optional lesson** | −3 **per gate** | the author declared something load-bearing and then made it skippable. Scored **and** raised (course-level) |

### The rulings that decide this bundle, restated

- **The toil row's last clause is load-bearing.** Setup that needs the network, a toolchain
  or an account is the learner's work and is not toil: no `supplies:` entry can create
  `node_modules`. The question at every candidate is not "is this boring?" but **"could this
  bundle have shipped the result?"**
- **A project skeleton is toil — the tiebreak, ruled 2026-09-13.** Where the shippability
  test and the toolchain test disagree, **shippability wins**. Asked in its full form:
  *could the bundle have shipped one set of files for each language the course supports?*
- **The exception: setup that is itself the subject.** *Is the setup step the ONLY element
  serving the objective that names it?* **Yes** — the setup is the subject, handing it over
  would strand the objective and cost −3, so score it as what it teaches. **No** — it is a
  part of a larger goal, and it is toil. A conjunctive objective is almost never sole-served.
  **Enumerate; do not judge from the objective's wording.**
- **A step the tutor performs is not an element** — not toil, not evidence. The objective it
  served does not disappear with it; a sole-served objective is then unserved at −3.
- **A branch point scores `evidence`, 0.** **A tutor-addressed element scores `teaching`,
  +2, when the learner must decide or construct in response.**
- **An anchor is served by what lessons DO, not by what they CITE.**

### Rows a reader answers, and a script never scores — six of them

1. a `design_refs` entry that does not answer the question its lesson raises;
2. a lesson that introduces a type or concept nothing later uses;
3. a symbol or term a lesson uses and no lesson introduces — `file:line` of the **first
   use**, and "bound only in `DESIGN.md`" kept separate from "bound nowhere", because a
   `DESIGN.md` anchor is loaded for the **tutor** and not for the learner, and appearing in
   `## Concepts to teach` is not itself a definition;
4. whether the lesson equips the tutor to end a turn with one concrete action — **the row
   passes when both conditions hold**: the lesson names the first concrete action (a file, a
   command or an artifact, and not only the outcome), **and** the lesson separates decisions
   from actions, keeping a design decision out of the closing action. **Grade the lesson
   FILE, never the tutor's turns**;
5. a lesson far outside the course's usual size, in either direction;
6. a must-cover topic that only an optional lesson teaches — a **question**, permanently.

### The invariant no structural check can reach

> **A course carrying optional lessons must be completable by a learner who declines every
> offer.**

All six rows and the invariant are answered in writing in section 6.

### Scoring frame used here, stated so it can be argued with

Carried unchanged from the 2026-09-13 report, so the two totals are comparable. This
bundle's house style is uniform, so one frame applies to all 18 lessons:

- every clause of `## Suggested progression` is an element;
- every bullet of `## Completion conditions` is an element;
- `## On completion, persist` is one element per lesson, scored **0 (evidence)** — it
  records decisions the learner already made;
- `## Theory`, `## Concepts to teach`, `## Constraints` and `## Optional deeper paths` are
  **not** elements. They are context and rules, not assignments;
- a completion condition that merely checks work already scored in the progression is **0
  (evidence)**, to avoid counting the same work twice; one that demands construction or a
  decision the progression never assigned is scored on its own merits.

**Totals are comparable within this course, not against another one.** A lesson's figure
tracks how finely its progression enumerates clauses. Do not set 131 beside another
bundle's number.

---

## 1. The course and its total

| | |
|---|---|
| Bundle id | `durable-event-broker` |
| Title | Build a Durable Event Broker in Go |
| Main-path lessons | 15 |
| Optional lessons | 3 |
| Lesson rows scored | 18 |
| Bundle commit | `221c164` |
| Validator | PASS, exit 0, pinned copy — and irrelevant to every figure below by design |

### Arithmetic

Main-path lesson sum, re-added element by element for this audit and not carried from the
old report:

```
L00  7      <- was 4 (2026-09-13); the only lesson that moved
L01  7
L02  5
L03  6
L04  9
L05  9
L06  9
L07  6
L08  6
L09  6
L10  9
L11  8
L12  7
L13  8
L14  9
---------
     111
```

Optional lesson sum:

```
page-cache-experiments    6
property-based-framing    7
tcp-transport             7
---------
                         20
```

Course-level penalties, each named:

```
lesson sum (main path 111 + optional 20)          131
unserved objectives and anchors    0 gaps x -3      0
required_for gates on optional lessons  0 x -3      0
--------------------------------------------------------
COURSE TOTAL                                      131
```

**Main path alone: 111.** That is the figure a learner who declines every offer earns. It is
reported because it is the honest number for that learner, not because prose and manifest
disagree — they do not; see section 6.

**Zero confirmed toil sites this run**, so there is no −2 inside any lesson figure. The one
site confirmed on 2026-09-13 has been handed over by the bundle; see sections 2 and 4.

**131 is a summary of the inventory in sections 2 to 4 and must not be quoted without it.**

### The two counts in the evidence header

`audit.py` prints "15 lesson(s), 3 optional" above a table of 18 rows. Nothing was dropped:
`lesson_count` counts the main path, the rows cover main path plus optional. The toil scan
covered all 18. Confirmed.

### Delta from 2026-09-13: 128 → 131

One lesson moved, for one cause. Every delta is enumerated in section 7.

---

## 2. The per-lesson table

The **closing action** column answers rubric row 4 for every lesson, pass or fail, no
blanks. It is not a score and is never added into one. Every `fail` is carried into section
6 with its `file:line` and the failing sentence.

| Lesson | Score | Objectives served | Toil found | Closing action |
|---|---|---|---|---|
| `00-running-broker.md` | **7** | 3 of 3 | none *(1 site handed over since 2026-09-13)* | **pass** |
| `01-offsets-and-replay.md` | **7** | 4 of 4 | none | **pass** |
| `02-record-framing.md` | **5** | 4 of 4 | none | **pass** |
| `03-recovery.md` | **6** | 4 of 4 | none | **pass** |
| `04-durability-contract.md` | **9** | 4 of 4 | none | **pass** |
| `05-partition-ownership.md` | **9** | 4 of 4 | none | **pass** (thinnest; §6) |
| `06-group-commit.md` | **9** | 4 of 4 | none | **pass** |
| `07-segments.md` | **6** | 4 of 4 | none | **pass** |
| `08-sparse-indexes.md` | **6** | 4 of 4 | none | **pass** |
| `09-retention.md` | **6** | 4 of 4 | none | **pass** |
| `10-topics-and-partitions.md` | **9** | 4 of 4 | none | **pass** |
| `11-http-api.md` | **8** | 4 of 4 | none | **FAIL** — `:52` (§6) |
| `12-long-polling-and-overload.md` | **7** | 4 of 4 | none | **pass** |
| `13-observability-and-load.md` | **8** | 4 of 4 | none | **pass** |
| `14-asynchronous-follower.md` | **9** | 5 of 5 | none (1 candidate rejected, §4) | **pass** |
| `page-cache-experiments.md` *(optional)* | **6** | 4 of 4 | none | **pass** |
| `property-based-framing.md` *(optional)* | **7** | 4 of 4 | none | **pass** |
| `tcp-transport.md` *(optional)* | **7** | 4 of 4 | none | **pass** |

No lesson scores at or below zero, so no lesson is carried to the author as a "what is this
lesson for?" question.

### Element breakdowns

Every element carries its `file:line` and the sentence it scored. Paths are relative to
`lessons/`. Every line number below was taken from the bundle at `221c164` and verified
against the file, not copied from the 2026-09-13 report or from an issue.

#### `00-running-broker.md` — 7 *(was 4; the lesson the supplies entry changed)*

| file:line | Sentence | Score |
|---|---|---|
| `00-running-broker.md:53` | "Write a minimal broker executable against the supplied module declaration." | +1 |
| `00-running-broker.md:53`–`:54` | "Add a directly testable record and log implementation." | +2 |
| `00-running-broker.md:54`–`:55` | "Append several opaque records, fetch them, and verify insertion order and copying behaviour." | +1 |
| `00-running-broker.md:55`–`:56` | "Keep the executable on the same path by making it exercise the API." | +1 |
| `00-running-broker.md:62` | "A test proves mutation of caller or returned byte slices cannot alter stored records." | +2 |
| `:60`, `:61`, `:63`, `:64`, `:68` | validators; order test; executable-on-path check; no-dead-code check; persist | 0 x 5 |

Sum: 1+2+1+1+2 = **7**.

Three judgements in that table are worth arguing with, so they are stated rather than
buried.

**`:53` is no longer toil, and it is no longer the old sentence.** The old clause read
"Create the module and a minimal broker executable." — two acts, of which `go mod init` was
the confirmed −2 of 2026-09-13. `tutorial.yaml:73`–`:76` now declares
`supplies/go.mod -> go.mod`, and the clause was rewritten to start the learner at the
broker. What remains assigned is writing the executable, and the full shippability question
answers itself in the negative: the executable must "exercise the same implementation used
by the tests" (`:63`) and stay "on the same path" (`:55`–`:56`), against a broker API the
learner has not designed yet. **The bundle could not have shipped that result** — only an
empty `main` stub, which `:63` would reject. So this is not the project skeleton any more
and the tiebreak does not reach it.

**`:53` scores +1 and not +2.** The learner constructs, and the clause serves objectives
`:21` and `:23`, but the instructive wrong answer here — putting the broker logic inside
`main` — is not decided at this clause. It is decided one clause later, when the "directly
testable record and log implementation" needs a home, and it is checked at `:64`. Scoring
`:53` at +2 would count that decision twice. A reader who credits the entry-point decision
to `:53` instead of to `:53`–`:54` would score the clause +2 and the lesson **8**; that is a
legitimate disagreement and it is named here rather than hidden. It does not change any
conclusion in this report.

**`:53` scores +1 and not the old +2-before-the-ruling.** The pre-ruling figure of 8 came
from scoring "create the module **and** a minimal broker executable" as one +2 element. The
clause now asks for strictly less work, and the part removed was the part with no teaching
in it, so the lesson does not simply return to 8.

#### `01-offsets-and-replay.md` — 7

| file:line | Sentence | Score |
|---|---|---|
| `01-offsets-and-replay.md:48` | "Add broker-assigned metadata to stored records." | +2 |
| `01-offsets-and-replay.md:48`–`:49` | "Extend append to return the assigned offset, then implement bounded fetch." | +2 |
| `01-offsets-and-replay.md:49` | "Test boundary cases before changing the executable" | +1 |
| `01-offsets-and-replay.md:49`–`:50` | "to demonstrate two independent replay positions." | +2 |
| `:54`–`:58`, `:62` | five completion conditions plus persist | 0 x 6 |

Sum: 2+2+1+2 = **7**.

#### `02-record-framing.md` — 5 *(the lowest figure in the course)*

| file:line | Sentence | Score |
|---|---|---|
| `02-record-framing.md:50` | "Write the format down, including byte order and checksum range." | +2 |
| `02-record-framing.md:50`–`:51` | "Implement encoding, then decoding with explicit errors." | +2 |
| `02-record-framing.md:51`–`:52` | "Test empty keys and payloads, binary zero bytes, maximum accepted sizes, truncation at several boundaries, version mismatch, and corruption." | +1 |
| `:56`–`:60`, `:64` | five completion conditions plus persist | 0 x 6 |

Sum: **5**. Broken out in full because the figure misleads on its own. This is one of the
most design-dense lessons in the course — `DESIGN.md:19`–`:20` explicitly defers field
widths and byte order to it — and it scores lowest purely because its progression is three
fat clauses where L04's is four thin ones. That is the granularity artefact the rubric
warns about, visible inside one course. **I would refuse a proposal that split L02's prose
merely to raise the number.**

#### `03-recovery.md` — 6

| file:line | Sentence | Score |
|---|---|---|
| `03-recovery.md:50` | "Open or create the log, append encoded frames, and rebuild in-memory metadata on reopen." | +2 |
| `03-recovery.md:51` | "Create deterministic tests that cut a valid file at several tail positions" | +1 |
| `03-recovery.md:51`–`:52` | "and another that corrupts an interior frame." | +2 |
| `03-recovery.md:52` | "Add a manual kill/restart experiment after the tests." | +1 |
| `:56`–`:60`, `:64` | five completion conditions plus persist | 0 x 6 |

Sum: **6**. The interior-corruption test earns +2 rather than +1 because the learner must
decide what the program does with it, and the tempting wrong answer (skip and continue) is
exactly what Theory `:27`–`:29` says destroys offset continuity.

#### `04-durability-contract.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `04-durability-contract.md:49` | "Instrument the existing append path, establish its current acknowledgement point," | +1 |
| `04-durability-contract.md:49`–`:50` | "then move the point behind explicit synchronisation." | +2 |
| `04-durability-contract.md:50`–`:51` | "Measure a repeatable sequence of durable appends and capture latency and throughput." | +1 |
| `04-durability-contract.md:51`–`:52` | "Discuss why different environments may produce different numbers without invalidating the contract." | +2 |
| `04-durability-contract.md:57` | "A forced sync error reaches the caller where the platform permits deterministic injection." | +1 |
| `04-durability-contract.md:59` | "The acknowledgement contract is written precisely and does not claim replication." | +2 |
| `:56`, `:58`, `:60`, `:64` | ack-ordering test; recording the measurement; validators; persist | 0 x 4 |

Sum: 1+2+1+2+1+2 = **9**. `:51` is scored under the tutor-addressed rule: "Discuss"
addresses the tutor, and what it makes the learner do is defend a contract against
overclaiming.

#### `05-partition-ownership.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `05-partition-ownership.md:52` | "Identify all mutable append state," | +2 |
| `05-partition-ownership.md:52`–`:53` | "then wrap append submissions in request values carrying a private result path." | +2 |
| `05-partition-ownership.md:53` | "Start and stop the owner explicitly." | +2 |
| `05-partition-ownership.md:53`–`:55` | "Add concurrent tests for offset uniqueness and ordering, followed by cancellation and shutdown cases under the race detector." | +1 |
| `05-partition-ownership.md:63` | "The learner can state the ownership invariant and why a channel serves it." | +2 |
| `:59`–`:62`, `:67` | four completion conditions plus persist | 0 x 5 |

Sum: **9**.

#### `06-group-commit.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `06-group-commit.md:50` | "Measure the existing owner," | 0 |
| `06-group-commit.md:50` | "add a size-only batch," | +2 |
| `06-group-commit.md:50`–`:51` | "then add a time bound so sparse traffic does not wait forever." | +2 |
| `06-group-commit.md:51` | "Test threshold edges, storage failures, cancellation, and shutdown." | +1 |
| `06-group-commit.md:52` | "Repeat the earlier workload and compare distributions rather than quoting one best run." | +1 |
| `06-group-commit.md:57` | "A sync spy or equivalent evidence proves one sync may cover several acknowledgements." | +1 |
| `06-group-commit.md:60` | "The learner records a comparable before/after measurement and explains the trade-off." | +2 |
| `:56`, `:58`, `:59`, `:64` | batch-trigger tests; exactly-once resolution; race tests; persist | 0 x 4 |

Sum: 0+2+2+1+1+1+2 = **9**.

#### `07-segments.md` — 6

| file:line | Sentence | Score |
|---|---|---|
| `07-segments.md:49` | "Introduce a segment type around the existing single-file mechanics," | +1 |
| `07-segments.md:49`–`:50` | "then make a partition manage an ordered collection." | +2 |
| `07-segments.md:50` | "Add rollover with tiny deterministic limits," | +2 |
| `07-segments.md:50`–`:51` | "reopen tests, and invalid-directory-layout tests." | +1 |
| `:55`–`:59`, `:63` | five completion conditions plus persist | 0 x 6 |

Sum: **6**.

#### `08-sparse-indexes.md` — 6

| file:line | Sentence | Score |
|---|---|---|
| `08-sparse-indexes.md:49` | "Measure or count frames scanned by the existing fetch." | 0 |
| `08-sparse-indexes.md:49`–`:50` | "Add periodic index entries, floor lookup, and forward scan." | +2 |
| `08-sparse-indexes.md:50`–`:51` | "Test exact hits, between-entry lookups, boundaries, missing indexes, and corruption." | +1 |
| `08-sparse-indexes.md:51` | "Compare scan work at more than one interval." | +2 |
| `08-sparse-indexes.md:57` | "Deleting an index and reopening rebuilds usable derived state." | +1 |
| `:55`, `:56`, `:58`, `:59`, `:63` | four completion conditions plus persist | 0 x 5 |

Sum: 0+2+1+2+1 = **6**. Broken out because `:49` scoring 0 is a call worth checking:
establishing a baseline scan count is reading a number, and the decision it feeds is scored
at `:51`.

#### `09-retention.md` — 6

| file:line | Sentence | Score |
|---|---|---|
| `09-retention.md:49` | "Expose earliest available offset," | +1 |
| `09-retention.md:49` | "implement size retention," | +2 |
| `09-retention.md:49`–`:50` | "then age retention with a deterministic clock." | +2 |
| `09-retention.md:50`–`:51` | "Test all-history-fits, several deletions, active-only history, restart, and fetches below, at, and above the retained boundary." | +1 |
| `:55`–`:59`, `:63` | five completion conditions plus persist | 0 x 6 |

Sum: **6**.

#### `10-topics-and-partitions.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `10-topics-and-partitions.md:51` | "Wrap the existing partition behind broker lookup," | +1 |
| `10-topics-and-partitions.md:51`–`:52` | "create a topic with a fixed count, and address appends explicitly first." | +1 |
| `10-topics-and-partitions.md:52` | "Add keyed selection" | +2 |
| `10-topics-and-partitions.md:52`–`:53` | "and then a documented unkeyed strategy." | +2 |
| `10-topics-and-partitions.md:53` | "Exercise independent owners under the race detector and restart the whole broker." | +1 |
| `10-topics-and-partitions.md:59` | "Invalid names cannot escape the broker data directory." | +2 |
| `:57`, `:58`, `:60`, `:61`, `:65` | four completion conditions plus persist | 0 x 5 |

Sum: 1+1+2+2+1+2 = **9**. `:59` earns +2 and not 0 because the progression never assigns
path validation anywhere — the requirement appears only in Constraints `:44` and this
completion condition — and a naive filesystem join is exactly the instructive wrong answer.

#### `11-http-api.md` — 8

| file:line | Sentence | Score |
|---|---|---|
| `11-http-api.md:52` | "Define the smallest external contract," | +2 |
| `11-http-api.md:52`–`:53` | "implement single append and bounded fetch," | +1 |
| `11-http-api.md:53` | "then batch append and metadata." | +1 |
| `11-http-api.md:53`–`:54` | "Add handler tests for success, malformed input, excessive bodies, unknown resources, expired offsets, cancellation, and storage errors." | +1 |
| `11-http-api.md:54`–`:55` | "Exercise the server with small producer and consumer commands that use the HTTP API." | +1 |
| `11-http-api.md:61` | "Domain errors map to documented stable status and body shapes." | +2 |
| `:59`, `:60`, `:62`, `:63`, `:67` | four completion conditions plus persist | 0 x 5 |

Sum: 2+1+1+1+1+2 = **8**. Note that `:52` scores +2 as teaching *and* fails the
closing-action row (§6). Those are different questions: the clause makes the learner take a
real design decision, and it takes that decision exactly where the tutor's next action
should be.

#### `12-long-polling-and-overload.md` — 7

| file:line | Sentence | Score |
|---|---|---|
| `12-long-polling-and-overload.md:51` | "Add a wait-capable internal fetch operation," | +2 |
| `12-long-polling-and-overload.md:51` | "then expose it through HTTP." | +1 |
| `12-long-polling-and-overload.md:51`–`:52` | "Test data already present, append-after-wait, timeout, client cancellation, shutdown, and several waiters." | +1 |
| `12-long-polling-and-overload.md:52`–`:54` | "Saturate a deliberately tiny append queue and confirm overload behaviour under the race detector." | +2 |
| `12-long-polling-and-overload.md:59` | "Timeout and cancellation return promptly without leaking waiters." | +1 |
| `:58`, `:60`, `:61`, `:62`, `:66` | four completion conditions plus persist | 0 x 5 |

Sum: 2+1+1+2+1 = **7**.

#### `13-observability-and-load.md` — 8

| file:line | Sentence | Score |
|---|---|---|
| `13-observability-and-load.md:51`–`:52` | "Add measurements around queueing, batching, write, sync, fetch, segments, retention, and errors." | +2 |
| `13-observability-and-load.md:52` | "Build a load command with fixed-duration and fixed-count modes," | +1 |
| `13-observability-and-load.md:52`–`:53` | "then add a JSON log producer representing several fictional services." | +1 |
| `13-observability-and-load.md:53`–`:54` | "Run below saturation, near saturation, and above capacity; explain the change in metrics and errors." | +2 |
| `13-observability-and-load.md:59` | "The load generator reports offered, accepted, acknowledged, rejected, and consumed work." | +2 |
| `:58`, `:60`, `:61`, `:62`, `:66` | four completion conditions plus persist | 0 x 5 |

Sum: 2+1+1+2+2 = **8**. `:62` ("Observations connect queue depth, batches, sync duration,
latency, and overload") scores 0 only to avoid double-counting the synthesis already scored
at `:53`; on its own it would be +2.

#### `14-asynchronous-follower.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `14-asynchronous-follower.md:54`–`:55` | "Reuse the internal fetch and append mechanics through a replication-specific boundary that can preserve assigned metadata." | +2 |
| `14-asynchronous-follower.md:55` | "Copy existing history, follow new records," | +1 |
| `14-asynchronous-follower.md:55`–`:56` | "interrupt and restart the follower," | +1 |
| `14-asynchronous-follower.md:56` | "and expose lag." | +1 |
| `14-asynchronous-follower.md:56`–`:57` | "Finally delay replication, acknowledge new leader records, terminate the leader, and inspect which records the follower lacks." | +2 |
| `14-asynchronous-follower.md:66` | "The learner explains why this system has neither quorum durability nor safe failover." | +2 |
| `:61`–`:65`, `:70` | five completion conditions plus persist | 0 x 6 |

Sum: 2+1+1+1+2+2 = **9**.

#### `page-cache-experiments.md` (optional) — 6

| file:line | Sentence | Score |
|---|---|---|
| `page-cache-experiments.md:52` | "Diagram the layers a record crosses," | +2 |
| `page-cache-experiments.md:52` | "measure append and sync separately," | +1 |
| `page-cache-experiments.md:52`–`:53` | "and inspect the system calls on a supported platform." | 0 |
| `page-cache-experiments.md:53` | "Compare ordinary process termination and abrupt process kill," | +1 |
| `page-cache-experiments.md:54` | "then state what neither experiment can prove about sudden machine power loss." | +2 |
| `:58`–`:61`, `:65` | four completion conditions plus persist | 0 x 5 |

Sum: 2+1+0+1+2 = **6**. The tracer clause scores 0 as evidence (run a tool, read output),
and Constraints `:46` makes it explicitly optional and platform-dependent.

#### `property-based-framing.md` (optional) — 7

| file:line | Sentence | Score |
|---|---|---|
| `property-based-framing.md:56` | "State the properties in plain language," | +2 |
| `property-based-framing.md:56` | "add the valid-record round trip," | +1 |
| `property-based-framing.md:56`–`:57` | "then exercise the decoder with arbitrary and truncated bytes." | +1 |
| `property-based-framing.md:57` | "Inspect any reduced counterexample, repair the codec," | +2 |
| `property-based-framing.md:57`–`:58` | "and retain a deterministic regression case before continuing generation." | +1 |
| `:62`–`:66`, `:70` | five completion conditions plus persist | 0 x 6 |

Sum: **7**. The repair clause earns +2 because Constraints `:52` forbids the tempting wrong
answer outright — "Repairs happen in the framing implementation named by `repair_in`, not
as test exclusions."

#### `tcp-transport.md` (optional) — 7

| file:line | Sentence | Score |
|---|---|---|
| `tcp-transport.md:54` | "Define a minimal append and fetch envelope," | +2 |
| `tcp-transport.md:54` | "implement exact framed I/O," | +2 |
| `tcp-transport.md:54`–`:55` | "and test using a connection that deliberately fragments and combines writes." | +1 |
| `tcp-transport.md:55`–`:56` | "Add request identifiers if more than one outstanding request is supported." | 0 |
| `tcp-transport.md:56` | "Propagate disconnect and deadlines," | +1 |
| `tcp-transport.md:56`–`:57` | "then exercise concurrent connections and shutdown under the race detector." | +1 |
| `:61`–`:65`, `:69` | five completion conditions plus persist | 0 x 6 |

Sum: 2+2+1+0+1+1 = **7**. `:55` is the course's only **branch point** and is scored 0 under
the rubric's settled rule: the clause offers a choice of paths, and whichever path the
learner takes is scored on its own.

---

## 3. Goal gaps

**Zero gaps. Penalty: 0 x −3 = 0.**

That is an unusual result, so this section records how each class was decided rather than
asserting it. The supplied `go.mod` made the enumeration of objective `00:21` load-bearing
this run, and it is done first and in full.

### The stranding check on `00-running-broker.md:21`, enumerated

Objective `00:21` reads:

> "Create a small Go module and executable without speculative package structure."

It is a **conjunction** of three conjuncts:

- (a) create a small Go module
- (b) create an executable
- (c) without speculative package structure

The rubric is explicit that a conjunctive objective is almost never sole-served and that a
reader must enumerate rather than judge from the wording. Here is every element that serves
it now, under this report's scoring frame:

| Element | Conjunct served | Scored | Still present after the supplies commit? |
|---|---|---|---|
| `:53` "Write a minimal broker executable against the supplied module declaration." | (b) | +1 | **yes** — rewritten, not removed |
| `:53`–`:54` "Add a directly testable record and log implementation." | (c) — the package-boundary decision, governed by Theory `:31` "Introduce Go packages only when both executable and tests need the code" | +2 | yes, unchanged |
| `:64` "No declared production function or type is disconnected from the running path." | (c) — a declared type nothing uses **is** speculative structure; this condition enforces the rule | 0 | yes, unchanged |
| `:68` "Record the package boundary, record representation, and byte-ownership rule…" | (c) — records the decision the objective demands | 0 | **yes, narrowed** — the clause "the chosen module path" was removed, and `:69` now says "The module path is supplied and is not the learner's choice." |
| — | (a) | — | **no longer a learner element.** The module is declared at `tutorial.yaml:74`–`:76` |

**Answer: `00:21` is still served, by three remaining elements. It is NOT stranded and the
course pays no −3.** The 2026-09-13 audit found four servers (`00:53` both clauses, `00:63`,
`00:67`); supplying the skeleton removed one of the four by rewriting `:53`'s first clause,
and the surviving three serve conjuncts (b) and (c) directly. The sole-server test therefore
still answers "No", exactly as it did on 2026-09-13 — which is the same answer, reached for
a different reason, and it is the reason the exception does not fire and the bundle was
free to ship the skeleton without incurring a stranding penalty. A bundle cannot be charged
−2 for assigning a step and −3 for supplying it, and this bundle is now charged neither.

**One honest caveat, raised as a proposal and not as a penalty.** Conjunct (a) — "Create a
small Go module" — is no longer work the learner performs. The objective is still exercised,
so the unserved-objective row does not fire: the row's test is "a stated objective that no
task exercises", and tasks exercise (b) and (c). But the objective's **first verb now
describes something the bundle does**, and the 2026-09-13 report's proposal P5 asked for it
to be reworded in the same change that supplied the file. That half of P5 was not done. See
**P1** in section 5. A reader who ruled that a per-conjunct test applies would find (a)
unserved and charge −3, taking the course to 128; I do not read the row that way — it is
written per objective, not per conjunct, and the rubric's own worked examples credit an
objective to any element that serves it. The disagreement is named so the author can settle
it rather than discover it at the next audit.

### DESIGN.md anchors — 15 of 15 served

Decided by **what lessons make the learner do**, never by searching `design_refs` for the
anchor name.

| Anchor | Served by | How I decided |
|---|---|---|
| `#record-model` | L00, L01, L11 | L00 `:53`–`:55` builds the opaque key/payload record and `:62` forbids exposing mutable storage; L11 `:46` carries arbitrary bytes over HTTP. |
| `#offset-semantics` | L01, L09 | L01 `:48`–`:50` assigns offsets and implements inclusive bounded fetch; L09 `:57` gives the expired-offset result the anchor demands. |
| `#record-framing` | L02 | `:50` writes the format down; the anchor explicitly defers widths and byte order to this lesson. |
| `#recovery-policy` | L03 | `:51` cuts the tail, `:51`–`:52` corrupts the interior, `:58` refuses to treat interior damage as tail damage. |
| `#acknowledgement-contract` | L04, L06 | L04 `:49`–`:50` moves the ack behind sync; L06 `:44`/`:57` keeps a batch one durability unit. |
| `#partition-ownership` | L05, L10 | L05 `:52`–`:53` gives one goroutine the mutable state; L10 `:53` runs independent owners under `-race`. (See §6 for the one thin sentence in this anchor.) |
| `#group-commit` | L06 | `:50` builds size and time thresholds; `:57` evidences one sync covering several acks. |
| `#segment-layout` | L07 | `:49`–`:50` names segments by base offset and rolls on a target; `:57` keeps only the newest open. |
| `#sparse-index-contract` | L08 | `:49`–`:50` builds floor lookup and forward scan; `:57`–`:58` requires rebuild and forbids an index validating a bad log. |
| `#retention-semantics` | L09 | `:49` deletes whole closed segments; `:57` returns an explicit out-of-range result with the earliest offset. |
| `#topic-partition-model` | L10 | `:52`–`:53` adds keyed routing with a documented stable hash and a documented unkeyed strategy. |
| `#transport-boundary` | L11, L12, tcp | L11 `:47` forbids storage packages importing HTTP; tcp `:46` reuses the same internal operations. |
| `#backpressure-contract` | L05, L12 | L05 `:47` bounds the request channel; L12 `:52`–`:54` saturates it and `:60` requires a documented overload response. |
| `#observability-contract` | L13, L09, L14 | L13 `:51` instruments the whole path and `:58` requires the anchor's measurements by name; "earliest available offset" comes from L09 `:49`, "replica lag" from L14 `:56`. |
| `#replication-boundary` | L14 | `:54`–`:57` builds the read-only follower, resumes it, and demonstrates the acknowledged-but-unreplicated record; `:66` makes the learner state the missing guarantees. |

No anchor describes project setup, a toolchain or project layout. That was checked directly
rather than assumed, because it is the other half of the skeleton exception test: had one
existed, supplying `go.mod` could have stranded it.

### COURSE.md coverage list — 26 of 26 taught

23 are taught on the main path, one-to-one with the main-path map at `COURSE.md:35`–`:49`,
each confirmed against a task rather than a keyword. The remaining three — property-based
record-framing tests, length-prefixed TCP protocols, operating-system page-cache behaviour
— are taught **only by an optional lesson**. Under the rubric those are **not** a scored
gap; they are reader-answered row 6, answered in section 6. The course names all three
itself at `COURSE.md:95`–`:97`.

`topic_candidates` was used only as a place to look. Two of its suggestions are word-overlap
noise rejected on reading: "missing quorum and failover guarantees" matched
`page-cache-experiments.md` on the shared word "guarantees" when it is L14 `:66` that serves
it, and "Go goroutine ownership" matched `00-running-broker.md`, which contains no goroutine
at all.

### Per-lesson learning objectives — 69 of 69 exercised

Every objective in all 18 lessons was walked against a scored task or completion condition.
All are exercised. Five are served marginally enough to name, so the author can disagree:

- **`00-running-broker.md:21`** "Create a small Go module and executable without speculative
  package structure." Enumerated above. Served by `:53`, `:53`–`:54` and `:64`; its first
  conjunct is now supplied. **New this run**, and the one the author should look at first.
- `01-offsets-and-replay.md:22` "Distinguish a log cursor from a byte position or queue
  acknowledgement." No task says this. Ruled served by `:49`–`:50` ("demonstrate two
  independent replay positions") plus Constraints `:44` ("Do not expose slice indexes as the
  public offset contract"). The explicit comparison sits in Optional deeper paths `:66`,
  which is not a task.
- `06-group-commit.md:22` "Measure throughput, latency distribution, and actual batch
  sizes." The batch-size half is served by `:57`'s sync spy rather than by a metric; the
  metric itself arrives in L13 `:51`.
- `11-http-api.md:23` "Bound request bodies and close them correctly." The bounding half is
  tested at `:53`/`:62`; the "close them correctly" half is asserted nowhere.
- `09-retention.md:20` "Define deterministic ordering when several segments qualify."
  Answered by Constraints `:43` ("Size policy removes oldest eligible segments first") and
  exercised by the "several deletions" case at `:50`.

None crosses the line into "no task exercises it", so none costs −3.

---

## 4. The toil inventory

**Confirmed toil sites: ZERO. 0 x −2 = 0.**

That is a change from 2026-09-13, which confirmed one site. The change is in the bundle, not
in the rubric and not in the reading.

### The site that was confirmed on 2026-09-13, and is now handed over

`lessons/00-running-broker.md:53` read, at commit `4df2624`:

> "Create the module and a minimal broker executable."

It was scored **−2** under the ruling of 2026-09-13: a project skeleton is toil, because the
bundle could have shipped one set of files per supported language.

At commit `221c164` the bundle has done exactly that. `tutorial.yaml:73`–`:76` declares:

```yaml
supplies:
  - from: supplies/go.mod
    to: go.mod
    describe: "go.mod: the module declaration, so lesson 00 starts at the broker rather than at go mod init"
```

`supplies/go.mod` exists and contains `module broker` / `go 1.22`. Validator check 22 ran
and resolved the `from` path. The lesson text was changed in the same commit (`dc3ba72`) and
**matches the manifest**, which was checked rather than assumed:

- `:53` now reads "Write a minimal broker executable against the supplied module
  declaration." — it names the supplied file rather than asking the learner to create it;
- `:68`–`:69` now reads "Record the package boundary, record representation, and
  byte-ownership rule in the learner instance's design and state. **The module path is
  supplied and is not the learner's choice.**" — the old clause "Record the chosen module
  path" is gone, which is the tell that the hand-over is declared in the lesson and not only
  in the manifest.

**The charge is removed, not moved.** The rubric's two guards were checked:

1. *The learner must not still do it.* The learner does not create the module. The work that
   remains — writing the executable — is different work with a different result, and it is
   scored on its merits at +1.
2. *The hand-over must be declared in the bundle.* It is declared twice: in `supplies:` at
   `tutorial.yaml:73`–`:76`, and in the lesson prose at `:53` and `:69`. A reviewer can point
   at both.

Note that this is the **supplied-file** route, not the tutor-performs-it route. The element
does not disappear; it shrinks. `:53` remains a scored element because the learner still
writes the executable.

**Is anything of the skeleton still assigned?** Yes — `main.go`. And it is **not** toil,
because the bundle could not have shipped the result: `:63` requires "The executable
exercises the same implementation used by the tests" and `:55`–`:56` requires keeping it "on
the same path by making it exercise the API", against a broker API that does not exist until
the learner designs it in the next clause. A shipped `main.go` could only have been an empty
stub, which `:63` rejects. That is the shippability test answering in the negative, which
is the rubric's own definition of "not toil".

### The one script candidate, examined

`audit.py` produced exactly one toil candidate across all 18 lessons.

- **`lessons/14-asynchronous-follower.md:55`**, pattern `copy`. The script's `text` field is
  one physical line and stops mid-clause: *"can preserve assigned metadata. Copy existing
  history, follow new records, interrupt and"*. The actual sentence, opened in the lesson:

  > "Copy existing history, follow new records, interrupt and restart the follower, and
  > expose lag."

  **Rejected — not toil, for the second audit running.** "Copy" is what the learner's
  follower does at runtime, not something the learner transcribes. The bundle could not have
  shipped the result: the history is generated by the learner's own broker during the lesson,
  and the copying mechanism *is* the thing being taught (`#replication-boundary`; objectives
  `:20`–`:24`). The "interrupt and restart" clause carries the lesson's hardest decision —
  idempotent resume without gaps or duplicates. Scored +1/+1/+1, never −2.

### Candidates the script has no pattern for, examined by hand and rejected

The scanner is a candidate generator over a fixed verb list, so its near-silence is evidence
about the pattern and not about the course. All 18 lessons were read looking for assigned
work that is deterministic, decision-free, and shippable.

- **`lessons/13-observability-and-load.md:52`–`:53`** — "then add a JSON log producer
  representing several fictional services." The closest thing in this course to shippable
  material: inventing plausible service names and log fields teaches nothing about brokers.
  **Rejected anyway**, because what the lesson requires is a *producer* with bounded
  concurrency and a documented workload (`:45`), not a static corpus, and that generator is
  the teaching. Carried into section 5 as an optional improvement explicitly labelled **not
  a finding**.
- **The 18 `## On completion, persist` blocks.** Rejected. They record decisions the learner
  made, into `tutorial/DESIGN.md` and `tutorial/STATE.md`, which are `tutor_owned`
  (`tutorial.yaml:59`) and therefore the runner's work to write. Scored 0 (evidence)
  uniformly, never −2.
- **The repeated "Validators pass" / "`go build ./...` … succeed" completion conditions**
  (L00 `:60`, L01 `:58`, L02 `:60`, L03 `:60`, L04 `:60`, L06 `:59`, L07 `:59`, L09 `:59`,
  L10 `:61`, L11 `:63`, L12 `:62`, L14 `:64`, tcp `:65`). **Rejected** — running a validator
  and reading its output is the rubric's definition of **evidence, 0**. It is never toil.
- **The test enumerations** (e.g. L02 `:51`–`:52`, L09 `:50`–`:51`, L12 `:51`–`:52`).
  **Rejected.** They are practice, +1: each case is a decision about what the code should do
  at a boundary, and no bundle could ship tests against an implementation the learner has
  not written yet. **This is a rejection because the bundle could not have supplied the
  result**, and it is named as such.
- **`lessons/00-running-broker.md:53`, the residual `main.go`.** Rejected, for the reason
  given above: the bundle could not have supplied an executable that exercises an API the
  learner has not designed.

### On the `supplies:` block, now present

`audit.py` reports one supplies entry, manifest-scope. That is the right scope: a
`--lesson`-scoped `--from` must live inside that lesson's own folder, and this bundle's
lessons are flat files (`lessons/00-running-broker.md`), not directories, so lesson scope is
not available in this layout without a layout change first.

Two consistency points, both checked and both fine:

- `tutorial.yaml:60` still lists `go.mod` under `learner_owned`, while `:74`–`:75` supplies
  it. **Not a conflict.** Supplies places the file; ownership governs who may edit it
  afterwards, and `ownership_policy: tutor-must-not-edit-learner-owned` (`:61`) keeps the
  tutor out of it once placed. A learner adding a `require` line later is exactly the case
  `learner_owned` is for.
- `workspace_kind: new-repository` (`:58`) and Constraints `00:45` "Begin from a fresh
  repository" are unaffected: supplies materialise into the fresh workspace.

One genuinely new thing the supplied file introduces is raised as **P2** in section 5:
`supplies/go.mod` asserts `go 1.22`, and `COURSE.md:139`–`:144` names no minimum Go version.

### Statement required by the skill

The `audit.py` toil scan is a **candidate generator over a fixed list of verbs**, and its
`pattern` field says only which verb fired. It cannot see toil it has no pattern for and it
fires on prose that is not toil. **This inventory came from reading all 18 lessons**, not
from the candidate list; the candidate list contributed one line, which was opened and
rejected.

---

## 5. Proposals

Every one is a proposal the author may refuse. None has been applied; applying any goes back
through the `tutorail-authoring` skill and its toolkit.

**P1 — Reword objective `00-running-broker.md:21`. The other half of last audit's P5.**
The bundle took P5's first half — it shipped the skeleton — and left the objective as it
was. `:21` still reads "Create a small Go module and executable without speculative package
structure", and its first verb now describes work the bundle performs at
`tutorial.yaml:74`–`:76`, not work the learner performs. Concrete action: change `:21` to

> "Extend the supplied module with an executable and a testable broker API, without
> speculative package structure."

That keeps the two conjuncts three elements actually serve — `:53` (the executable),
`:53`–`:54` and `:64` (the package-structure rule) — and drops the one the bundle now
serves itself. This is **not** currently a scored gap (§3 explains why) and rewording it
costs the course nothing; leaving it is a row waiting to fire at whichever future audit
reads the objective per conjunct.

**P2 — State the minimum Go version in `COURSE.md`, now that the bundle asserts one.**
`supplies/go.mod:3` declares `go 1.22`. `COURSE.md:143` asks only for "A local Go toolchain
capable of running the race detector", and `COURSE.md:142` for "Basic familiarity with Go
syntax". Before `dc3ba72` the learner chose their own directive with `go mod init`; now the
bundle chooses it for them, and a learner on an older toolchain meets the failure at the
first `go build` with nothing in the course explaining it. Concrete action: add one bullet
under `## Prerequisites` — "Go 1.22 or newer; the supplied `go.mod` declares that version."
**New this run, caused by the supplies commit.** It is not a quality finding against the
teaching and it rejects nothing.

**P3 — Give `11-http-api.md:52` a deliverable, and close the one failing closing-action
row.** `:52` opens the progression with "Define the smallest external contract," — a real
design decision (objective `:20`, persist `:67`) with no named artifact and no stated
landing place, sitting where the tutor's first concrete action should be. Concrete action,
either: (a) change `:52` to "**Write down** the smallest external contract — the routes,
the request and response representations, and the size limits — **in the learner design**,
then implement single append and bounded fetch."; or (b) add one completion condition
mirroring `02-record-framing.md:59`, "The external contract is recorded under
`#transport-boundary` in the learner design", which gives the decision a home the way L02
already gives one to the frame. (a) is the smaller change and fixes the row directly. This
answers section 6's closing-action failure; see there.

**P4 — Give `#record-model` the byte-ownership rule, or give L00 an anchor that has it.**
`lessons/00-running-broker.md:4` cites `design_refs: [record-model]`. The lesson's sharpest
teaching is defensive ownership of byte slices (Theory `:31`–`:33`, Constraints `:47`–`:48`,
completion `:62`), and `DESIGN.md:3`–`:7` says nothing about it. A learner who follows the
citation to find out *why* fetch must not expose mutable storage finds four sentences about
JSON and headers. Concrete action, either: (a) append one sentence to `#record-model` in
`DESIGN.md` — "The broker owns its copy of the key and payload; neither an appending caller
nor a fetching caller may hold storage the broker will read or write later" — or (b) add a
`#byte-ownership` anchor and add it to L00's `design_refs`. (a) is smaller and matches how
`#record-framing` already defers detail to the instance. Carried unchanged from 2026-09-13;
the sentences are the same and only the completion-condition line moved, `:61` → `:62`.

**P5 — Define "base offset" in `lessons/07-segments.md`.** First use at `07-segments.md:19`,
"Name and order segments by base logical offset." The term is used four times in that lesson
(`:19`, `:32`, `:41`, `:58`) and is **bound nowhere** — not in a lesson, and not in
`DESIGN.md`, whose `#segment-layout` at `:50`–`:51` uses it without defining it. Concrete
action: add one sentence to L07's `## Theory`, before `:26`'s existing text — "A segment's
base offset is the logical offset of its first record; it names the file and orders the
sequence." This is reader-answered row 3 and is not scored; see section 6.

**P6 — Decide what the append timestamp is for, or move it.**
`lessons/02-record-framing.md:42` puts an append timestamp in the frame. No main-path lesson
makes a decision that depends on it until `lessons/14-asynchronous-follower.md:46` requires
the follower to preserve it, and L09's age retention uses a clock seam (`:44`) rather than
record timestamps. Concrete action, either: extend `09-retention.md:49` so age retention is
evaluated from the newest record timestamp in a segment — which would make the field
load-bearing eleven lessons earlier — or move the field's introduction out of L02 and into
L14 where it is first used. This is section 6's "concept nothing later uses" row; the field
*is* eventually used, so it is a question and not a finding.

**P7 — Make the read path's concurrency explicit.** `DESIGN.md:39`–`:40` says "Reads may use
immutable closed segments and carefully published active-state snapshots without mutating
append state." No lesson has a completion condition requiring a concurrent
fetch-while-appending test; the property is exercised only incidentally by L10 `:53` and L12
`:52`–`:54`, both under `-race`. Concrete action: add one completion condition to
`05-partition-ownership.md` — "A race-enabled test fetches from a partition concurrently
with appends and never mutates append state" — or to `12-long-polling-and-overload.md`
alongside `:62`. The anchor is served, so this costs nothing today; it closes the thinnest
seam in the course.

**P8 — Optionally hand over the JSON workload corpus. Explicitly NOT a toil finding.**
`13-observability-and-load.md:52`–`:53` asks the learner to invent "several fictional
services". If the author wants that part handed over, the entry would be manifest-scope:

```
python3 scripts/supplies.py add \
  /Users/robert/src/github.com/skomp/tutorail-bundles/durable-event-broker \
  --from testdata/service-logs.jsonl \
  --to testdata/service-logs.jsonl \
  --describe "Fictional multi-service JSON application logs, used as one opaque broker workload" \
  --check
```

run from the `tutorail-authoring` skill's own directory, not this one. Two honest caveats,
both unchanged since 2026-09-13. First, **`testdata/service-logs.jsonl` does not exist in
the bundle** — the skill names that as the tell that something was never toil, and here it
means the author would have to author the corpus before declaring it. Second, a
`--lesson`-scoped entry is not available in this layout, because lesson-scope `--from` must
live inside that lesson's own folder and this bundle's lessons are flat files. Manifest
scope, or a layout change first. No prose would be deleted either way: `:52`–`:53` would
change from "add a JSON log producer representing several fictional services" to "drive the
supplied service-log corpus through the broker", and the bounded-concurrency generator
requirement at `:45` stays.

**P9 — No `required_for` gate exists, so the rubric's warning is not triggered.** See
section 6.

**No lesson scores at or below zero**, so no lesson is carried back to the author as a "what
is this lesson for?" question. The lowest figure is `02-record-framing.md` at 5, and section
2 explains at length why that is a clause-granularity artefact rather than a weakness.

---

## 6. The questions only a reader can answer

Six reader-answered rows plus the completability invariant, each answered in writing. None
is scored. All of them change what the author does next.

### Row 1 — a `design_refs` entry that does not answer the question its lesson raises

**Two instances: one clear, one weaker.**

- **`lessons/00-running-broker.md:4` → `#record-model` (`DESIGN.md:3`–`:7`).** The lesson's
  live question is byte-slice ownership — Theory `:31`–`:33`, Constraints `:47`–`:48`,
  completion `:62` — and the anchor answers a different question (JSON, headers, schema
  registries). The reference resolves, the validator is green, and the learner still does
  not find out why fetch must not expose mutable storage. **Proposal P4.**
- **`lessons/12-long-polling-and-overload.md:4` → `#backpressure-contract`
  (`DESIGN.md:81`–`:85`).** The anchor answers bounded queues and explicit overload well. It
  does not answer the lesson's other question, raised at Constraints `:45`: "Notification
  cannot be lost in a way that leaves available data waiting indefinitely." No anchor covers
  wait predicates or notification coalescing; the lesson's own Theory `:26`–`:29` answers it
  instead. Weaker, because the learner is not left without an answer — only without one in
  `DESIGN.md`.

All other 16 lessons: checked, and their `design_refs` answer their lessons' questions.
`#transport-boundary` for L11 and tcp, `#replication-boundary` for L14, and
`#recovery-policy` for L03 are the clearest positive cases.

### Row 2 — a lesson that introduces a type or concept nothing later uses

**One instance worth raising, plus two weaker candidates; none is fatal.**

- **The append timestamp, `lessons/02-record-framing.md:42`.** Introduced into the frame in
  L02 and, on the main path, never *decided with* — only carried. Its first real use is
  `lessons/14-asynchronous-follower.md:46`, twelve lessons later, where it is preserved and
  asserted at `:61`. L09's age retention explicitly uses a clock or metadata seam (`:44`)
  rather than record timestamps, which is where a reader would expect the field to earn its
  keep. It *is* used, so this is a question and not a finding. **Proposal P6.**
- **The format version field, `lessons/02-record-framing.md:42`.** Nothing on the main path
  ever bumps it. But rejecting an unsupported version is a use, and it is tested at `:57`
  and recovered around at L03 — ruled **used**.
- **The metadata operation, `lessons/11-http-api.md:53`.** "then batch append and metadata"
  introduces a metadata endpoint no later lesson's completion condition requires. L13's load
  generator plausibly consumes it and L09's earliest-available-offset is the obvious thing it
  exposes, but neither is stated. Worth a sentence from the author.

**Nothing the supplied `go.mod` introduces falls under this row.** `module broker` /
`go 1.22` introduces no type or concept; it removes one (the module-path choice), and the
lesson's persist block was edited in the same commit to stop asking for it.

### Row 3 — a symbol or term a lesson uses and no lesson introduces

**`audit.py` returned NOTHING-TO-CHECK, not "clean".** Its own words:

> Scanned 18 lesson(s); 18 declare '## Concepts to teach'; 0 fenced code block(s) skipped;
> DESIGN.md present=True readable=True; 0 candidate row(s) over 0 distinct symbol(s).
>
> `!!` NO candidate symbol was found in any of the 18 lesson(s) scanned … 'No candidate
> found' is NOT 'no undefined symbol' - read the lessons.
>
> This section checked NOTHING. That is a different result from 'checked and clean'.

**That is reported as nothing-to-check and is NOT written up as a pass.** It is the same
status the 2026-09-15 brief flagged, and it recurred. The reason it recurred was established
rather than guessed: every backticked span in the whole bundle was enumerated, and there are
26 distinct ones — `go test ./...`, `go build ./...`, `go vet ./...`, `go test`, `pprof`,
`repair_in`, `bundle-format.md`, `#record-framing`, `#observability-contract`,
`frame-decoder-breaks-on-arbitrary-input`, and 16 lesson ids. **Not one contains a
one-or-two-character identifier token**, which is the scanner's candidate rule, so it had
nothing to sort. The blindness is a property of this bundle's house style — it writes its
concepts in prose, not in backticks — and not of the scanner failing to run.

**So the row was answered by hand, over prose, and it did find something.** Sorted on the
author's boundary of 2026-09-13: a parameter of the concept being taught is owed to the
learner; an identifier of the language the learner already chose is not.

**Bound nowhere** — the meaning has not been decided anywhere in the bundle:

- **"base offset" / "base logical offset". First use: `lessons/07-segments.md:19`** — "Name
  and order segments by base logical offset." Used again at `:32` (`## Concepts to teach`,
  which the rubric says is not a definition), `:41` ("Segment filenames sort or parse
  deterministically by base offset") and `:58` ("duplicate base offset"). **No lesson says
  what it is**, and `DESIGN.md:50`–`:51` uses it without defining it either, so this is
  "bound nowhere" and not "bound only in `DESIGN.md`". It is squarely a parameter of the
  subject: the learner did not bring it from Go, and the lesson makes them name files by it
  (`:41`) and detect overlaps and gaps in it (`:43`, `:58`). Getting it wrong — reading it as
  the segment's last offset, or as a byte position — breaks the whole lesson.
  **Proposal P5.**
- **"metadata seam". First use and only use: `lessons/09-retention.md:44`** — "Age tests use
  a controllable clock or metadata seam, not sleeps." Weaker than the one above: "seam" is
  test-design vocabulary rather than broker vocabulary, and the alternative in the same
  sentence ("a controllable clock") carries the meaning, with `## Concepts to teach` `:36`
  naming "Injectable clocks for deterministic tests". Raised for completeness; the author may
  reasonably leave it.

**Bound only in `DESIGN.md`: none found.** This was checked directly rather than assumed —
every term the anchors introduce is also introduced by the lesson that cites the anchor.

**Candidates examined and rejected**, so the next reader does not re-litigate them:

- **"torn tail"** — first use `03-recovery.md:21`, defined six lines later in the same
  lesson's Theory at `:27` ("end-of-file inside the final frame is a torn tail"), before any
  task. In-lesson and in time. Rejected.
- **"floor entry" / "floor lookup"** — first use `08-sparse-indexes.md:20`, defined in the
  same lesson's Theory at `:26`–`:27` ("the greatest indexed offset not greater than the
  target"). Rejected.
- **"durability unit"** — first use `06-group-commit.md:45`. Constraints `:44` immediately
  above it ("No request is acknowledged before the batch sync succeeds") defines it
  operationally one line earlier. Marginal, and rejected.
- **"offered load" / "accepted load"** — first use `13-observability-and-load.md:21`,
  distinguished by contrast in Theory `:26`–`:28` and enumerated in completion `:59`.
  Rejected.
- **"replica lag"** — first use `14-asynchronous-follower.md:23`. Deliberately *not* defined:
  persist `:70` asks the learner to record their own "lag definition" and completion `:63`
  tests the behaviour. That is a decision assigned, not a symbol left dangling. Rejected.
- **"coordinated omission"** — `13-observability-and-load.md:35`, in `## Concepts to teach`
  and nowhere else. `## Concepts to teach` is not a definition under this row, but it is also
  the only occurrence: the learner is never asked to act on the term, and the entry is an
  instruction to the tutor to introduce it. Rejected as a symbol, noted here so the
  distinction is on the record.
- **"short writes" / "exact-write loops"** (`03-recovery.md:34`), **"exact framed I/O"**
  (`tcp-transport.md:54`) — these belong to the `io.Writer`/`io.Reader` contract of the
  language the learner already chose, the `bool`/`New`/`go` side of the author's line.
  Rejected.

**The sort above is the reader's, candidate by candidate, and no rule of shape performed
it.** A future `DESIGN.md` convention marking a conceptual parameter apart from a type would
make it mechanical; that is a bundle-format question owned by `skomp/tutorAIl` and is not
settled here.

### Row 4 — does the lesson equip the tutor to end a turn with one concrete action?

Answered pass/fail for every lesson in the section 2 table. **The lesson FILE was graded, not
any tutor turn** — no transcript exists for this bundle and none would have changed a row
here, because an author can change a file and cannot change a tutor's behaviour from this
repository.

The test applied, stated so the author can argue with it rather than with a verdict:

- **Condition 1** passes when the first clause of `## Suggested progression` names one act on
  a named file, command or artifact — not only an outcome.
- **Condition 2** passes when that first act does not require an unsettled design decision to
  be taken in the same breath, and when the lesson's design decisions are marked and have a
  home other than the closing action.

**17 pass. One fails.**

- **`lessons/11-http-api.md:52` — FAIL.** The failing sentence:

  > "Define the smallest external contract, implement single append and bounded fetch, then
  > batch append and metadata."

  **Condition 1 fails**: "Define the smallest external contract" names an outcome — a
  contract, defined — and no file, command or artifact. The lesson never says what form the
  definition takes: a routes list, handler stubs, prose in the learner design. The tutor
  asking "define the contract" has handed the learner a question, not a next step.
  **Condition 2 fails too**: the contract is a real design decision (objective `:20` "Adapt
  HTTP requests to the internal append, batch, fetch, and metadata operations"; persist
  `:67` "Record routes, request and response representations, size limits, error mapping"),
  and it is sitting exactly where the closing action should be. The decision's only home is
  the end-of-lesson persist block, eleven lines later. **Proposal P3.**

  The contrast that decided it is inside this same course. `02-record-framing.md:50` has the
  same shape — "Write the format down, including byte order and checksum range." — and
  **passes**, because it names the act (write), names the fields, and completion `:59` says
  exactly where the result lands: "The concrete frame decision is recorded under
  `#record-framing` in the learner design." L11 has no equivalent of `:59`. That is the whole
  difference, and it is why P3 proposes adding one.

Three passes worth showing the working for, since they are the ones a reader would challenge:

- **`00-running-broker.md:53` — pass, and it is a pass the supplies commit created.** The old
  first clause, "Create the module and a minimal broker executable.", is precisely the
  rubric's first named defect — a progression bullet carrying two actions, which the tutor
  must split before either half can be a next step, with the lesson nowhere saying to split
  it. The new clause is one act on one named artifact, against a file the bundle supplies.
  `dc3ba72` repaired this row as a side effect of removing the toil. **Delta from
  2026-09-13**, although the row did not exist then to record it.
- **`05-partition-ownership.md:52` — pass, and the thinnest in the course.** "Identify all
  mutable append state," produces an enumeration rather than a file. It passes because the
  enumeration is itself the deliverable and persist `:67` gives it a home ("Record owned
  state, request/result shape, channel capacity, closure owner, and shutdown order"), but a
  reader who insists on a file, a command or an artifact would fail it. Named so the author
  can decide.
- **`tcp-transport.md:54` — pass, marginally.** "Define a minimal append and fetch envelope,"
  is the same verb as L11's failing clause, but an envelope is an artifact — a wire frame
  layout — its parts are specified by Constraints `:45` and `## Concepts to teach`
  `:35`–`:37`, and persist `:69` names where it lands. L11's "contract" has none of those
  three.

**One structural property of this course deserves naming, because it is the rubric's second
failure mode not happening.** The rubric's other named defect is "an open question with no
home": a `## Optional deeper paths` section that invites a discussion and never says it does
not close a turn. All 18 lessons here carry that section, and **every one of them closes it
with an explicit boundary clause** — L00 `:74` "Do not replace the broker payload with
strings"; L03 `:69` "while keeping automatic recovery conservative"; L06 `:69` "do not add it
without a measurable goal"; L07 `:68` "without making either part of correctness"; L09
`:67`–`:68` "only to distinguish them from this course's deletion policy"; L10 `:71` "do not
add cluster placement here"; L12 `:71` "without adding a second main-path transport"; L13
`:72` "Do not perform speculative zero-copy refactors without evidence"; L14 `:76`–`:77`
"without implementing them here"; tcp `:74`–`:75` "do not treat protocol overhead as the
broker's storage throughput". That is 18 for 18, and it is the reason only one lesson fails
this row.

### Row 5 — a lesson far outside the course's usual size

**None found, in either direction.** All 18 lesson files fall between 66 and 77 lines (mean
71.1; `01-offsets-and-replay.md` at 66 and both `14-asynchronous-follower.md` and
`property-based-framing.md` at 77 are the extremes). `00-running-broker.md` grew by one line
in `dc3ba72`, from 73 to 74, which changes nothing here. Every lesson carries the same nine
headings and scored element counts run 5 to 9. Nothing is "usually two lessons" and nothing
is "usually a paragraph of the lesson beside it".

The corollary matters for reading section 2: because the size is uniform, the spread in
lesson figures (5 to 9) reflects **clause granularity inside `## Suggested progression`**
almost entirely, not depth. `02-record-framing.md` writes three fat clauses and scores 5;
`04-durability-contract.md` writes four thin ones plus two substantive completion conditions
and scores 9. They teach comparable amounts.

### Row 6 — a must-cover topic that only an optional lesson teaches

**Three, and the question is put to the author.**

| Coverage topic (`COURSE.md`) | Taught only by |
|---|---|
| `:127` property-based record-framing tests | `lessons/property-based-framing.md` |
| `:128` length-prefixed TCP protocols | `lessons/tcp-transport.md` |
| `:129` operating-system page-cache behaviour | `lessons/page-cache-experiments.md` |

> **Is that acceptable for this course, given that a learner who declines every offer never
> meets them?**

A question and not a score, deliberately and permanently. My reading, which the author may
overrule: **yes, and this course has already answered it better than most.**
`COURSE.md:89`–`:100` names all three explicitly, separates **complete** from **covered**,
and gives the reason they are in the list — "They are in the list because the course does
teach them and a tutor may offer them. They are not on the main path because the course
finishes without them." That is exactly the outcome the rubric's declined-row note exists to
protect: the topics stay in the coverage list, so a tutor offers the authored lesson instead
of improvising a replacement. The one thing the author might reconsider is TCP framing
specifically — `#transport-boundary` (`DESIGN.md:75`–`:79`) treats the optional TCP transport
as a first-class citizen of the design, which is a slightly stronger claim than "optional".

### `required_for` on an optional lesson — 0 gates

`tutorial.yaml` was opened and its `optional_lessons:` block worked through by hand, keyed
off the **presence of the key** at `:29` and never off `optional_lesson_count`:

| Optional lesson | `offer_at` | `anticipates` | `repair_in` | `required_for` |
|---|---|---|---|---|
| `lessons/property-based-framing.md` | `:31` L02 | `:36` `frame-decoder-breaks-on-arbitrary-input` | `:37` L02 | **absent** |
| `lessons/tcp-transport.md` | `:39` L11 | absent | absent | **absent** |
| `lessons/page-cache-experiments.md` | `:45` L04 | absent | absent | **absent** |

`grep -n "required_for" tutorial.yaml` returns nothing, with `repair_in` at `:37` as the
positive control proving the grep can find a key in that block. **Zero gates, so the row
scores 0 x −3 = 0 and there is no score for the rubric's warning to sit beside.** For the
record, the warning that would have been required — **not triggered here** — is:

> This gate cost the course 3 points and may still be correct. If the lesson genuinely
> cannot be completed while its failure stands, the gate is doing its job — say so and keep
> it. Do not delete a gate to improve a score. A course that drops a justified gate lets a
> learner finish a lesson whose failure is still standing, which is worse than the toil this
> rubric hunts.

The absence is itself a small positive finding. `property-based-framing` declares
`anticipates` **without** `required_for`, so a learner who declines the offer can still
finish `02-record-framing` with the anticipated failure mode standing, and the `repair_in`
points back to a main-path lesson (`:37`), which is the correct direction.

### Prose optionality vs manifest optionality

**They agree. No discrepancy, and no alternative total is needed.**

- All three optional lessons carry `optional: true` in frontmatter
  (`page-cache-experiments.md:4`, `property-based-framing.md:4`, `tcp-transport.md:4`) **and**
  appear under `optional_lessons:` rather than in `lessons:`.
- No lesson in `lessons:` describes itself as optional. Every hit of the word "optional" in
  the 15 main-path files was checked: 15 are the `## Optional deeper paths` headings, three
  are conditional pointers to the authored optional lessons
  (`02-record-framing.md:69`, `04-durability-contract.md:69`, `11-http-api.md:72`, each
  "when the learner accepts it"), and two are about the record's key field
  (`00-running-broker.md:22`, `02-record-framing.md:42`).

This is the opposite of the failure the rubric records from the webgl bundle. The
main-path-only figure of **111** is reported in section 1 because it is genuinely useful, not
because the manifest and the prose disagree.

### The completability invariant, asked out loud

> **Can a learner who declines every offer still finish this course?**

**Yes.** Checked against the lessons, not only against the manifest.

- *Does any main-path completion condition depend on something only an optional lesson builds
  or explains?* No. All 75 main-path completion conditions were read.
  `02-record-framing.md:58` ("No malformed input causes a panic or unbounded allocation") is
  the one that looks as if it might need `property-based-framing`, and it does not: it is
  satisfiable from the hand-written truncation, version-mismatch and corruption tests
  assigned at `:51`–`:52`. `04-durability-contract.md:56`–`:60` needs no page-cache tracing.
  `11-http-api.md:59`–`:63`, L12, L13 and L14 name only HTTP;
  `14-asynchronous-follower.md:54` builds on "the internal fetch and append mechanics", which
  are L11/L12 main-path work, never the TCP transport.
- *Does any main-path lesson's prose assume the learner took an offer?* No. The only three
  cross-references are the conditional ones listed above.
- The author states this claim themselves at `COURSE.md:87`–`:100`, separating **complete**
  from **covered** while doing it. The claim was checked rather than accepted, and it holds.

The supplies entry does not touch this: `supplies/go.mod` is manifest-scope and is placed for
every learner, whichever offers they decline.

### Dry-run evidence

No dry-run harness was run for this audit and none was supplied, so there is no stall to cite
either way. **Absence of a dry run is not evidence about the course**, in either direction.

---

## 7. Every delta from 2026-09-13, and its cause

The baseline is `docs/audits/2026-09-13/durable-event-broker.md` at bundle commit `4df2624`
— course **128**, main path **108**. The bundle is now at `221c164`. `git diff
4df2624..221c164 -- durable-event-broker` touches exactly three files, across two commits
(`ae5ccac`, `dc3ba72`): `lessons/00-running-broker.md` (+6/−5), `supplies/go.mod` (new, 3
lines), `tutorial.yaml` (+4). **The other 17 lessons, `COURSE.md` and `DESIGN.md` are
byte-identical.** Every element figure for those 17 was nonetheless re-added from the files
for this report; all 18 sums and both subtotals reproduce.

| # | Delta | Cause |
|---|---|---|
| 1 | Course total **128 → 131**; main path **108 → 111** | **Bundle changed.** Entirely from L00; see rows 2–4. |
| 2 | `00-running-broker.md` **4 → 7** | **Bundle changed.** |
| 3 | `00-running-broker.md:53` **−2 → +1** | **Bundle changed.** The confirmed toil site of 2026-09-13 was handed over. `tutorial.yaml:73`–`:76` declares `supplies/go.mod -> go.mod`, and `dc3ba72` rewrote the clause from "Create the module and a minimal broker executable." to "Write a minimal broker executable against the supplied module declaration." The `go mod init` act is gone; what remains is writing the executable, which the bundle could not have shipped (it must exercise an API the learner has not designed). +3 of the +3. |
| 4 | Confirmed toil sites **1 → 0** | **Bundle changed.** Same cause. The −2 was an element score inside L00's figure, never a course-level row, so removing it moves L00 and the totals and nothing else. |
| 5 | L00 line numbers shift by +1 from `:54` onward (`:59`→`:60` … `:67`→`:68`) | **Bundle changed.** The progression grew from three wrapped lines to four. Cited line numbers in this report were taken from the file at `221c164`, not from the old report. |
| 6 | L00 persist element re-read: "Record the chosen module path, package boundary, …" → "Record the package boundary, … The module path is supplied and is not the learner's choice." | **Bundle changed.** Score unchanged at 0 (evidence). It is the evidence that the hand-over is declared in the lesson text and not only in the manifest. |
| 7 | Objective `00:21` servers **4 → 3** | **Bundle changed.** The 2026-09-13 enumeration found `00:53` (both clauses), `00:63` and `00:67`. `:53`'s skeleton clause no longer serves conjunct (a); `:53`'s executable clause, `:53`–`:54`, `:64` and `:68` remain. **The objective is still served and is NOT stranded; no −3.** Enumerated in full in section 3. |
| 8 | `## Supplies declared` in the evidence output: **0 entries → 1** | **Bundle changed.** Validator check 22 ran against it and resolved the `from` path. |
| 9 | Section 4's paragraph "On the absent `supplies:` block" is retired | **Bundle changed.** It said the bundle "should still ship the skeleton it asks the learner to type". It now does. |
| 10 | 2026-09-13 proposal **P5** is half-applied | **Bundle changed, incompletely.** P5 asked for the skeleton to be supplied **and** for objective `00:21` to be reworded in the same change. The first half was done; the second was not. Re-raised as **P1**, and explicitly not scored. |
| 11 | New rows in section 2 and 6: a **closing-action** column for all 18 lessons, and the **undefined-symbol** row | **Rubric changed.** The reader-answered rows went from four to six for this run. The old report answered four. |
| 12 | New finding: `11-http-api.md:52` fails the closing-action row | **Rubric changed.** The lesson sentence is unchanged since `4df2624`; the row that catches it did not exist on 2026-09-13. |
| 13 | New finding: "base offset" bound nowhere, first use `07-segments.md:19` | **Rubric changed.** Same: the lesson is unchanged and the row is new. |
| 14 | New finding (P2): `supplies/go.mod:3` asserts `go 1.22` while `COURSE.md:139`–`:144` names no minimum Go version | **Bundle changed.** A direct consequence of `dc3ba72`: the module directive used to be the learner's to choose. |
| 15 | Section 6 gains an explicit **nothing-to-check** answer for the symbol row | **Rubric changed**, and the status recurred. `audit.py` found 0 candidates over 18 lessons for the second run. Reported as nothing-to-check, with the cause established (no backticked span in the bundle contains a 1–2-character identifier) and the row then answered by hand. |
| 16 | P4, P6, P7, P8 (was P1, P2, P3, P4) carry forward with their sentences unchanged | **No change.** Only `00-running-broker.md:61` → `:62` moved, in P4. |
| 17 | Zero unserved objectives and anchors; zero `required_for` gates | **No change.** Both re-enumerated from the bundle rather than carried. |

### The settled argument, not reopened

The 2026-09-13 report recorded a disagreement with a **draft** of the rubric's worked table,
which had listed this bundle as sole-served and therefore as taking the skeleton exception.
The report applied the rubric's own operational test, found four servers for `00:21`, and
ruled **toil**; the rubric's table was then rebuilt by enumerating elements and now agrees,
naming the same four servers. **There is no disagreement left, and nothing here reopens it.**
This audit re-ran the same enumeration against the changed bundle and reached "not
sole-served" again, which is what made the hand-over safe: because the exception never fired,
supplying the skeleton could not strand the objective.

The rubric's worked table (`references/rubric.md`, "Worked: the five bundles, 2026-09-13")
lists this bundle's servers as `00:53` both clauses, `00:63` and `00:67`. **Those line
numbers are now stale** — `:63` is `:64` and `:67` is `:68` at `221c164`, and `:53`'s first
clause has been rewritten. The table says of itself that every `file:line` in it was correct
on 2026-09-13 and that line numbers must be taken from the bundle. This audit did that, and
this row is the notification that a third of the table's `durable-event-broker` entry has
moved.

---

## Closing note, as the skill requires

The validator was run, from the pinned scripts directory named in the provenance block, and
it passed with exit 0. **Its result was not an input to any figure above.** Structural
validity and teaching quality are different questions: the validator answers "is this a
bundle?", and this report answers "does this teach?". `validate_bundle.py` was not changed,
and no finding in this report may reject a bundle — every one of them is a proposal the
author can accept or refuse, and applying any goes back through the `tutorail-authoring`
skill and its toolkit.

**This report proposes and changed nothing.** The bundle is byte-identical to commit
`221c164`; `git status --porcelain` in `skomp/tutorail-bundles` was empty before this audit
and empty after it.
