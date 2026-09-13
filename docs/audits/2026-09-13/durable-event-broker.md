# Course-quality audit: `durable-event-broker`

Audited read-only on 2026-09-13 against
`tutorail-authoring:course-quality` 0.3.0 and its `references/rubric.md`.
Bundle path: `/Users/robert/src/github.com/skomp/tutorail-bundles/durable-event-broker`
at commit `4df2624`. Nothing in the bundle was created, edited, staged or deleted;
`git status --porcelain` was empty before and after.

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
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises (course-level, counted once per gap) |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised (course-level) |

### Two elements settled by the rubric rather than by me

- **A branch point scores `evidence`, 0.** The teaching is in whichever branch the learner
  takes, and that branch is scored on its own.
- **A tutor-addressed element scores `teaching`, +2, when the learner must decide or
  construct in response.** Score the element by what it makes the learner do, at whatever
  grammatical person the author wrote it in.

### Rows a reader answers, and a script never scores

- a `design_refs` entry that does not answer the question its lesson raises;
- a lesson that introduces a type or concept nothing later uses;
- a lesson far outside the course's usual size, in either direction;
- a must-cover topic that only an optional lesson teaches — **a question, permanently, not
  a scored row.**

### The invariant no structural check can reach

> **A course carrying optional lessons must be completable by a learner who declines every
> offer.**

All five of these are answered in writing in section 6.

### Scoring frame used here, stated so it can be argued with

The rubric says to score "each task, each step, each completion condition". This bundle has
a very uniform house style, so I applied one frame to all 18 lessons:

- every clause of `## Suggested progression` is an element;
- every bullet of `## Completion conditions` is an element;
- `## On completion, persist` is one element per lesson, scored **0 (evidence)** every
  time — it records decisions the learner already made;
- `## Theory`, `## Concepts to teach`, `## Constraints` and `## Optional deeper paths` are
  **not** scored as elements. They are context and rules, not assignments. Where a
  constraint is the only place a real decision lives, I say so in section 6 rather than
  quietly scoring it.
- A completion condition that merely checks a task already scored in the progression is
  **0 (evidence)**, to avoid counting the same work twice. A completion condition that
  demands construction or a decision the progression never assigned is scored on its own
  merits, and those are the ones broken out below.

**Totals are comparable within this course, not against another one.** A lesson's figure
tracks how finely its progression enumerates clauses. This course's clause granularity is
unusually even, which is why the figures cluster between 5 and 9.

---

## 1. The course and its total

| | |
|---|---|
| Bundle id | `durable-event-broker` |
| Title | Build a Durable Event Broker in Go |
| Main-path lessons | 15 |
| Optional lessons | 3 |
| Lesson rows scored | 18 |
| Validator status | not run here; irrelevant to this report by design |

### Arithmetic

Main-path lesson sum:

```
L00  8
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
     112
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
lesson sum (main path 112 + optional 20)          132
unserved objectives and anchors    0 gaps x -3      0
required_for gates on optional lessons  0 x -3      0
--------------------------------------------------------
COURSE TOTAL                                      132
```

**Main path alone: 112.** That figure is the one a learner who declines every offer earns,
and it is reported because it is the honest number for that learner — not because prose and
manifest disagree (they do not; see section 6).

**132 is a summary of the inventory in sections 2 to 4, and must not be quoted without it.**

### Note on the two counts in the evidence header

`audit.py` prints "15 lesson(s), 3 optional" above a table of 18 rows. These do not
contradict each other and nothing was dropped: `lesson_count` counts the main path,
the rows cover main path plus optional. The toil scan covered all 18. Confirmed.

---

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil found |
|---|---|---|---|
| `00-running-broker.md` | **8** | 3 of 3 | none |
| `01-offsets-and-replay.md` | **7** | 4 of 4 | none |
| `02-record-framing.md` | **5** | 4 of 4 | none |
| `03-recovery.md` | **6** | 4 of 4 | none |
| `04-durability-contract.md` | **9** | 4 of 4 | none |
| `05-partition-ownership.md` | **9** | 4 of 4 | none |
| `06-group-commit.md` | **9** | 4 of 4 | none |
| `07-segments.md` | **6** | 4 of 4 | none |
| `08-sparse-indexes.md` | **6** | 4 of 4 | none |
| `09-retention.md` | **6** | 4 of 4 | none |
| `10-topics-and-partitions.md` | **9** | 4 of 4 | none |
| `11-http-api.md` | **8** | 4 of 4 | none |
| `12-long-polling-and-overload.md` | **7** | 4 of 4 | none |
| `13-observability-and-load.md` | **8** | 4 of 4 | none |
| `14-asynchronous-follower.md` | **9** | 5 of 5 | none (1 candidate rejected, §4) |
| `page-cache-experiments.md` *(optional)* | **6** | 4 of 4 | none |
| `property-based-framing.md` *(optional)* | **7** | 4 of 4 | none |
| `tcp-transport.md` *(optional)* | **7** | 4 of 4 | none |

No lesson scores at or below zero, so no lesson is carried into section 5 as a
"what is this lesson for?" question.

### Element breakdowns

Every element carries its `file:line` and the sentence it scored. Paths are relative to
`lessons/`. Elements scoring 0 that are pure "validators pass" or pure task-confirmation are
summarised as a count rather than listed line by line, except where they are the only thing
holding a figure down.

#### `00-running-broker.md` — 8

| file:line | Sentence | Score |
|---|---|---|
| `00-running-broker.md:53` | "Create the module and a minimal broker executable." | +2 |
| `00-running-broker.md:53` | "Add a directly testable record and log implementation." | +2 |
| `00-running-broker.md:54` | "Append several opaque records, fetch them, and verify insertion order and copying behaviour." | +1 |
| `00-running-broker.md:54` | "Keep the executable on the same path by making it exercise the API." | +1 |
| `00-running-broker.md:61` | "A test proves mutation of caller or returned byte slices cannot alter stored records." | +2 |
| `:59`, `:60`, `:62`, `:63`, `:67` | validators; order test; executable-on-path check; no-dead-code check; persist | 0 x 5 |

Sum: 2+2+1+1+2 = **8**. The +2 at `:61` is the aliasing proof: it is a distinct piece of
adversarial construction the progression only gestured at, and a wrong answer (retaining
the caller's slice) is exactly the instructive bug.

#### `01-offsets-and-replay.md` — 7

| file:line | Sentence | Score |
|---|---|---|
| `01-offsets-and-replay.md:48` | "Add broker-assigned metadata to stored records." | +2 |
| `01-offsets-and-replay.md:48` | "Extend append to return the assigned offset, then implement bounded fetch." | +2 |
| `01-offsets-and-replay.md:49` | "Test boundary cases before changing the executable" | +1 |
| `01-offsets-and-replay.md:49` | "to demonstrate two independent replay positions." | +2 |
| `:54`–`:58`, `:62` | five completion conditions plus persist | 0 x 6 |

Sum: **7**.

#### `02-record-framing.md` — 5 (lowest figure in the course)

| file:line | Sentence | Score |
|---|---|---|
| `02-record-framing.md:50` | "Write the format down, including byte order and checksum range." | +2 |
| `02-record-framing.md:50` | "Implement encoding, then decoding with explicit errors." | +2 |
| `02-record-framing.md:51` | "Test empty keys and payloads, binary zero bytes, maximum accepted sizes, truncation at several boundaries, version mismatch, and corruption." | +1 |
| `:56`–`:60`, `:64` | five completion conditions plus persist | 0 x 6 |

Sum: **5**. Broken out in full because the figure is misleading on its own. This is one of
the most design-dense lessons in the course — the DESIGN anchor `#record-framing` explicitly
defers field widths and byte order to it — and it scores lowest purely because its
progression is written as three fat clauses where L04's is written as four thin ones. This
is the granularity artefact the rubric warns about, visible inside a single course. It is
**not** evidence that lesson 02 teaches less than lesson 04, and I would not accept a
proposal that split L02's prose merely to raise the number.

#### `03-recovery.md` — 6

| file:line | Sentence | Score |
|---|---|---|
| `03-recovery.md:50` | "Open or create the log, append encoded frames, and rebuild in-memory metadata on reopen." | +2 |
| `03-recovery.md:51` | "Create deterministic tests that cut a valid file at several tail positions" | +1 |
| `03-recovery.md:51` | "and another that corrupts an interior frame." | +2 |
| `03-recovery.md:52` | "Add a manual kill/restart experiment after the tests." | +1 |
| `:56`–`:60`, `:64` | five completion conditions plus persist | 0 x 6 |

Sum: **6**. The interior-corruption test earns +2 rather than +1 because the learner must
decide what the program does with it, and the tempting wrong answer (skip and continue) is
precisely what Theory at `:26`–`:29` warns destroys offset continuity.

#### `04-durability-contract.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `04-durability-contract.md:49` | "Instrument the existing append path, establish its current acknowledgement point," | +1 |
| `04-durability-contract.md:49` | "then move the point behind explicit synchronisation." | +2 |
| `04-durability-contract.md:50` | "Measure a repeatable sequence of durable appends and capture latency and throughput." | +1 |
| `04-durability-contract.md:51` | "Discuss why different environments may produce different numbers without invalidating the contract." | +2 |
| `04-durability-contract.md:57` | "A forced sync error reaches the caller where the platform permits deterministic injection." | +1 |
| `04-durability-contract.md:59` | "The acknowledgement contract is written precisely and does not claim replication." | +2 |
| `:56`, `:58`, `:60`, `:64` | ack-ordering test; recording the measurement; validators; persist | 0 x 4 |

Sum: 1+2+1+2+1+2 = **9**. `:51` is scored under the rubric's tutor-addressed rule: "Discuss"
addresses the tutor, and what it makes the learner do is defend a contract against
overclaiming.

#### `05-partition-ownership.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `05-partition-ownership.md:52` | "Identify all mutable append state," | +2 |
| `05-partition-ownership.md:52` | "then wrap append submissions in request values carrying a private result path." | +2 |
| `05-partition-ownership.md:53` | "Start and stop the owner explicitly." | +2 |
| `05-partition-ownership.md:53` | "Add concurrent tests for offset uniqueness and ordering, followed by cancellation and shutdown cases under the race detector." | +1 |
| `05-partition-ownership.md:63` | "The learner can state the ownership invariant and why a channel serves it." | +2 |
| `:59`–`:62`, `:67` | four completion conditions plus persist | 0 x 5 |

Sum: **9**.

#### `06-group-commit.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `06-group-commit.md:50` | "Measure the existing owner," | 0 |
| `06-group-commit.md:50` | "add a size-only batch," | +2 |
| `06-group-commit.md:50` | "then add a time bound so sparse traffic does not wait forever." | +2 |
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
| `07-segments.md:49` | "then make a partition manage an ordered collection." | +2 |
| `07-segments.md:50` | "Add rollover with tiny deterministic limits," | +2 |
| `07-segments.md:50` | "reopen tests, and invalid-directory-layout tests." | +1 |
| `:55`–`:59`, `:63` | five completion conditions plus persist | 0 x 6 |

Sum: **6**.

#### `08-sparse-indexes.md` — 6

| file:line | Sentence | Score |
|---|---|---|
| `08-sparse-indexes.md:49` | "Measure or count frames scanned by the existing fetch." | 0 |
| `08-sparse-indexes.md:49` | "Add periodic index entries, floor lookup, and forward scan." | +2 |
| `08-sparse-indexes.md:50` | "Test exact hits, between-entry lookups, boundaries, missing indexes, and corruption." | +1 |
| `08-sparse-indexes.md:51` | "Compare scan work at more than one interval." | +2 |
| `08-sparse-indexes.md:57` | "Deleting an index and reopening rebuilds usable derived state." | +1 |
| `:55`, `:56`, `:58`, `:59`, `:63` | four completion conditions plus persist | 0 x 5 |

Sum: 0+2+1+2+1 = **6**. Broken out because `:49` scoring 0 is the kind of call worth
checking: establishing a baseline scan count is reading a number, and the decision it feeds
is scored at `:51`.

#### `09-retention.md` — 6

| file:line | Sentence | Score |
|---|---|---|
| `09-retention.md:49` | "Expose earliest available offset," | +1 |
| `09-retention.md:49` | "implement size retention," | +2 |
| `09-retention.md:49` | "then age retention with a deterministic clock." | +2 |
| `09-retention.md:50` | "Test all-history-fits, several deletions, active-only history, restart, and fetches below, at, and above the retained boundary." | +1 |
| `:55`–`:59`, `:63` | five completion conditions plus persist | 0 x 6 |

Sum: **6**.

#### `10-topics-and-partitions.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `10-topics-and-partitions.md:51` | "Wrap the existing partition behind broker lookup," | +1 |
| `10-topics-and-partitions.md:51` | "create a topic with a fixed count, and address appends explicitly first." | +1 |
| `10-topics-and-partitions.md:52` | "Add keyed selection" | +2 |
| `10-topics-and-partitions.md:52` | "and then a documented unkeyed strategy." | +2 |
| `10-topics-and-partitions.md:52` | "Exercise independent owners under the race detector and restart the whole broker." | +1 |
| `10-topics-and-partitions.md:59` | "Invalid names cannot escape the broker data directory." | +2 |
| `:57`, `:58`, `:60`, `:61`, `:65` | four completion conditions plus persist | 0 x 5 |

Sum: 1+1+2+2+1+2 = **9**. `:59` earns +2 and not 0 because the progression never assigns
path validation anywhere — the requirement appears only in Constraints `:44` and this
completion condition — and a naive filesystem join is exactly the instructive wrong answer.

#### `11-http-api.md` — 8

| file:line | Sentence | Score |
|---|---|---|
| `11-http-api.md:52` | "Define the smallest external contract," | +2 |
| `11-http-api.md:52` | "implement single append and bounded fetch," | +1 |
| `11-http-api.md:52` | "then batch append and metadata." | +1 |
| `11-http-api.md:53` | "Add handler tests for success, malformed input, excessive bodies, unknown resources, expired offsets, cancellation, and storage errors." | +1 |
| `11-http-api.md:54` | "Exercise the server with small producer and consumer commands that use the HTTP API." | +1 |
| `11-http-api.md:61` | "Domain errors map to documented stable status and body shapes." | +2 |
| `:59`, `:60`, `:62`, `:63`, `:67` | four completion conditions plus persist | 0 x 5 |

Sum: 2+1+1+1+1+2 = **8**.

#### `12-long-polling-and-overload.md` — 7

| file:line | Sentence | Score |
|---|---|---|
| `12-long-polling-and-overload.md:51` | "Add a wait-capable internal fetch operation," | +2 |
| `12-long-polling-and-overload.md:51` | "then expose it through HTTP." | +1 |
| `12-long-polling-and-overload.md:51` | "Test data already present, append-after-wait, timeout, client cancellation, shutdown, and several waiters." | +1 |
| `12-long-polling-and-overload.md:52` | "Saturate a deliberately tiny append queue and confirm overload behaviour under the race detector." | +2 |
| `12-long-polling-and-overload.md:59` | "Timeout and cancellation return promptly without leaking waiters." | +1 |
| `:58`, `:60`, `:61`, `:62`, `:66` | four completion conditions plus persist | 0 x 5 |

Sum: 2+1+1+2+1 = **7**.

#### `13-observability-and-load.md` — 8

| file:line | Sentence | Score |
|---|---|---|
| `13-observability-and-load.md:51` | "Add measurements around queueing, batching, write, sync, fetch, segments, retention, and errors." | +2 |
| `13-observability-and-load.md:52` | "Build a load command with fixed-duration and fixed-count modes," | +1 |
| `13-observability-and-load.md:52` | "then add a JSON log producer representing several fictional services." | +1 |
| `13-observability-and-load.md:53` | "Run below saturation, near saturation, and above capacity; explain the change in metrics and errors." | +2 |
| `13-observability-and-load.md:59` | "The load generator reports offered, accepted, acknowledged, rejected, and consumed work." | +2 |
| `:58`, `:60`, `:61`, `:62`, `:66` | four completion conditions plus persist | 0 x 5 |

Sum: 2+1+1+2+2 = **8**. `:62` ("Observations connect queue depth, batches, sync duration,
latency, and overload") scores 0 only to avoid double-counting the synthesis already scored
at `:53`; on its own it would be +2.

#### `14-asynchronous-follower.md` — 9

| file:line | Sentence | Score |
|---|---|---|
| `14-asynchronous-follower.md:54` | "Reuse the internal fetch and append mechanics through a replication-specific boundary that can preserve assigned metadata." | +2 |
| `14-asynchronous-follower.md:55` | "Copy existing history, follow new records," | +1 |
| `14-asynchronous-follower.md:55` | "interrupt and restart the follower," | +1 |
| `14-asynchronous-follower.md:56` | "and expose lag." | +1 |
| `14-asynchronous-follower.md:56` | "Finally delay replication, acknowledge new leader records, terminate the leader, and inspect which records the follower lacks." | +2 |
| `14-asynchronous-follower.md:66` | "The learner explains why this system has neither quorum durability nor safe failover." | +2 |
| `:61`–`:65`, `:70` | five completion conditions plus persist | 0 x 6 |

Sum: 2+1+1+1+2+2 = **9**.

#### `page-cache-experiments.md` (optional) — 6

| file:line | Sentence | Score |
|---|---|---|
| `page-cache-experiments.md:52` | "Diagram the layers a record crosses," | +2 |
| `page-cache-experiments.md:52` | "measure append and sync separately," | +1 |
| `page-cache-experiments.md:52` | "and inspect the system calls on a supported platform." | 0 |
| `page-cache-experiments.md:53` | "Compare ordinary process termination and abrupt process kill," | +1 |
| `page-cache-experiments.md:54` | "then state what neither experiment can prove about sudden machine power loss." | +2 |
| `:58`–`:61`, `:65` | four completion conditions plus persist | 0 x 5 |

Sum: 2+1+0+1+2 = **6**. The tracer clause scores 0 as evidence (run a tool, read output),
and Constraints `:46` makes it explicitly optional and platform-dependent.

#### `property-based-framing.md` (optional) — 7

| file:line | Sentence | Score |
|---|---|---|
| `property-based-framing.md:55` | "State the properties in plain language," | +2 |
| `property-based-framing.md:56` | "add the valid-record round trip," | +1 |
| `property-based-framing.md:56` | "then exercise the decoder with arbitrary and truncated bytes." | +1 |
| `property-based-framing.md:56` | "Inspect any reduced counterexample, repair the codec," | +2 |
| `property-based-framing.md:57` | "and retain a deterministic regression case before continuing generation." | +1 |
| `:62`–`:66`, `:70` | five completion conditions plus persist | 0 x 6 |

Sum: **7**. The `:56` repair clause earns +2 because Constraints `:52` forbids the tempting
wrong answer outright — "Repairs happen in the framing implementation named by `repair_in`,
not as test exclusions."

#### `tcp-transport.md` (optional) — 7

| file:line | Sentence | Score |
|---|---|---|
| `tcp-transport.md:54` | "Define a minimal append and fetch envelope," | +2 |
| `tcp-transport.md:54` | "implement exact framed I/O," | +2 |
| `tcp-transport.md:54` | "and test using a connection that deliberately fragments and combines writes." | +1 |
| `tcp-transport.md:55` | "Add request identifiers if more than one outstanding request is supported." | 0 |
| `tcp-transport.md:56` | "Propagate disconnect and deadlines," | +1 |
| `tcp-transport.md:56` | "then exercise concurrent connections and shutdown under the race detector." | +1 |
| `:61`–`:65`, `:69` | five completion conditions plus persist | 0 x 6 |

Sum: 2+2+1+0+1+1 = **7**. `:55` is the course's only **branch point** and is scored 0 under
the rubric's settled rule: the clause offers a choice of paths, and whichever path the
learner takes is scored on its own. Scoring the fork as teaching would count the same
instruction twice.

---

## 3. Goal gaps

**Zero gaps. Penalty: 0 x −3 = 0.**

That is an unusual result and I looked for gaps rather than for confirmation. How each
class was decided:

### DESIGN.md anchors — 15 of 15 served

I decided each anchor by **what lessons make the learner do**, never by searching
`design_refs` for the anchor name. The rubric is explicit that citation is not service in
either direction.

| Anchor | Served by | How I decided |
|---|---|---|
| `#record-model` | L00, L01, L11 | L00 `:53`–`:54` builds the opaque key/payload record and `:61` forbids exposing mutable storage; L11 `:46` carries arbitrary bytes over HTTP. |
| `#offset-semantics` | L01, L09 | L01 `:48`–`:49` assigns offsets and implements inclusive bounded fetch; L09 `:57` gives the expired-offset result the anchor demands. |
| `#record-framing` | L02 | `:50` writes the format down; the anchor explicitly defers widths and byte order to this lesson. |
| `#recovery-policy` | L03 | `:51` cuts the tail, `:51`–`:52` corrupts the interior, `:58` refuses to treat interior damage as tail damage. |
| `#acknowledgement-contract` | L04, L06 | L04 `:49` moves the ack behind sync; L06 `:44`/`:57` keeps a batch one durability unit. |
| `#partition-ownership` | L05, L10 | L05 `:52`–`:53` gives one goroutine the mutable state; L10 `:52` runs independent owners under `-race`. (See §6 for the one thin sentence in this anchor.) |
| `#group-commit` | L06 | `:50` builds size and time thresholds; `:57` evidences one sync covering several acks. |
| `#segment-layout` | L07 | `:49`–`:50` names segments by base offset and rolls on a target; `:57` keeps only the newest open. |
| `#sparse-index-contract` | L08 | `:49`–`:50` builds floor lookup and forward scan; `:57`–`:58` requires rebuild and forbids an index validating a bad log. |
| `#retention-semantics` | L09 | `:49` deletes whole closed segments; `:57` returns an explicit out-of-range result with the earliest offset. |
| `#topic-partition-model` | L10 | `:52` adds keyed routing with a documented stable hash and a documented unkeyed strategy. |
| `#transport-boundary` | L11, L12, tcp | L11 `:47` forbids storage packages importing HTTP; tcp `:46` reuses the same internal operations. |
| `#backpressure-contract` | L05, L12 | L05 `:47` bounds the request channel; L12 `:52`–`:54` saturates it and `:60` requires a documented overload response. |
| `#observability-contract` | L13, L09, L14 | L13 `:51` instruments the whole path and `:58` requires the anchor's measurements by name; `earliest available offset` comes from L09 `:49`, `replica lag` from L14 `:56`. |
| `#replication-boundary` | L14 | `:54`–`:57` builds the read-only follower, resumes it, and demonstrates the acknowledged-but-unreplicated record; `:66` makes the learner state the missing guarantees. |

### COURSE.md coverage list — 26 of 26 taught

23 are taught on the main path; the mapping is one-to-one with the main-path map at
`COURSE.md:35`–`:49` and I confirmed each against a task, not a keyword. The remaining
three — property-based record-framing tests, length-prefixed TCP protocols,
operating-system page-cache behaviour — are taught **only by an optional lesson**. Under the
rubric these are **not** a scored gap: they are the reader-answered question, answered in
section 6. The course names all three itself at `COURSE.md:95`–`:97`.

`topic_candidates` from the script was used only as a place to look. Two of its suggestions
are word-overlap noise that I rejected on reading: "missing quorum and failover guarantees"
matched `page-cache-experiments.md` (shared word "guarantees") when it is L14 `:66` that
serves it, and "Go goroutine ownership" matched `00-running-broker.md` when L00 contains no
goroutine at all.

### Per-lesson learning objectives — 69 of 69 exercised

I walked every objective in all 18 lessons against a scored task or completion condition.
All are exercised. Four are served marginally enough to name, so the author can disagree:

- `01-offsets-and-replay.md:22` "Distinguish a log cursor from a byte position or queue
  acknowledgement." No task says this. I ruled it served by `:49` ("demonstrate two
  independent replay positions" — the non-destructive-dequeue point) plus Constraints `:44`
  ("Do not expose slice indexes as the public offset contract"). The explicit comparison
  sits in Optional deeper paths `:66`, which is not a task.
- `06-group-commit.md:22` "Measure throughput, latency distribution, and actual batch
  sizes." The batch-size half is served by `:57`'s sync spy rather than by a metric; the
  metric itself arrives in L13 `:51`.
- `11-http-api.md:23` "Bound request bodies and close them correctly." The bounding half is
  tested at `:53`/`:62`; the "close them correctly" half is asserted nowhere.
- `09-retention.md:20` "Define deterministic ordering when several segments qualify."
  Answered by Constraints `:43` ("Size policy removes oldest eligible segments first") and
  exercised by the "several deletions" case at `:50`.

None of these crosses the line into "no task exercises it", so none costs −3. They are the
four I would look at first if the author wants the margin widened.

---

## 4. The toil inventory

**Confirmed toil sites: none. 0 x −2 = 0.**

### The one script candidate, examined

`audit.py` produced exactly one candidate.

- **`lessons/14-asynchronous-follower.md:55`**, pattern `copy`. The script's `text` field is
  one physical line and stops mid-clause: *"can preserve assigned metadata. Copy existing
  history, follow new records, interrupt and"*. The actual sentence, from the lesson:

  > "Copy existing history, follow new records, interrupt and restart the follower, and
  > expose lag."

  **Rejected — not toil.** "Copy" here is what the learner's follower does at runtime, not
  something the learner transcribes. The bundle could not have shipped the result: the
  history is generated by the learner's own broker during the lesson, and the copying
  mechanism *is* the thing being taught (`#replication-boundary`; objectives `:20`–`:24`).
  The "interrupt and restart" clause carries the lesson's hardest decision — idempotent
  resume without gaps or duplicates. I scored this clause +1/+1/+1, not −2.

### Candidates the script has no pattern for, examined by hand and rejected

The scanner is a candidate generator over a fixed verb list. Its near-silence is evidence
about the pattern, not about the course, so I read all 18 lessons looking for assigned work
that is deterministic, decision-free, and shippable.

- **`lessons/00-running-broker.md:53`** — "Create the module and a minimal broker
  executable." **Rejected because the bundle could not have supplied the result.** A Go
  module needs the toolchain and the network; `go.mod` is `learner_owned`
  (`tutorial.yaml:60`), `workspace_kind` is `new-repository` (`:58`), and the module path is
  a decision the learner records at `:67`. This is the learner's setup, scored as what it
  actually is (+2), not charged as toil. This rejection is the same shape as the `npm
  install` case the rubric's last clause exists for.
- **`lessons/13-observability-and-load.md:52`** — "then add a JSON log producer representing
  several fictional services." The closest thing in this course to shippable material:
  inventing plausible service names and log fields teaches nothing about brokers. Rejected
  anyway, because what the lesson requires is a *producer* with bounded concurrency and a
  documented workload (`:46`), not a static corpus — and that generator is the teaching.
  Carried into section 5 as an optional improvement explicitly labelled **not a finding**.
- **The 18 `## On completion, persist` blocks.** Rejected. They record decisions the learner
  made themselves into `tutorial/DESIGN.md` and `tutorial/STATE.md`, which are `tutor_owned`
  (`tutorial.yaml:59`) and therefore the runner's work to write. Scored 0 (evidence)
  uniformly, never −2.
- **The repeated "Validators pass" / "`go build ./...` … succeed" completion conditions**
  (L00 `:59`, L01 `:58`, L02 `:60`, L03 `:60`, L04 `:60`, L06 `:59`, L07 `:59`, L09 `:59`,
  L10 `:61`, L11 `:63`, L12 `:62`, L14 `:64`, tcp `:65`). Rejected. Running a validator and
  reading its output is the rubric's definition of **evidence, 0** — it is never toil.
- **The test enumerations** (e.g. L02 `:51`, L09 `:50`, L12 `:51`). Rejected. They are
  practice, +1: each case is a decision about what the code should do at a boundary, and
  no bundle could ship tests against an implementation the learner has not written yet.

### On the absent `supplies:` block

`audit.py` reports 0 supplies entries and the bundle ships no data files at all. **That is
coherent for this course, not an omission.** Every artefact in it is either the learner's
toolchain or code the learner writes; there is nothing a supplies entry could hand over.
A bundle with no supplies and no toil is the expected shape for a build-it-from-nothing
course.

### Statement required by the skill

The `audit.py` toil scan is a **candidate generator over a fixed list of verbs**, and its
`pattern` field says only which verb fired. It cannot see toil it has no pattern for and it
fires on prose that is not toil. **This inventory came from reading all 18 lessons**, not
from the candidate list; the candidate list contributed one line, which I opened and
rejected.

---

## 5. Proposals

Every one of these is a proposal the author may refuse. None has been applied; applying any
of them goes back through the `tutorail-authoring` skill and its toolkit.

**P1 — Give `#record-model` the byte-ownership rule, or give L00 an anchor that has it.**
`lessons/00-running-broker.md:4` cites `design_refs: [record-model]`. Its sharpest teaching
is defensive ownership of byte slices (Constraints `:47`–`:48`, completion `:61`,
Theory `:32`–`:33`), and `DESIGN.md:3`–`:7` says nothing about it. A learner who follows the
citation to find out *why* fetch must not expose mutable storage finds four sentences about
JSON and headers. Concrete action, either:
(a) append one sentence to `#record-model` in `DESIGN.md` — "The broker owns its copy of the
key and payload; neither an appending caller nor a fetching caller may hold storage the
broker will read or write later" — or
(b) add a `#byte-ownership` anchor and add it to L00's `design_refs`.
(a) is smaller and matches how `#record-framing` already defers detail to the instance.
This proposal answers the first section-6 question; see there.

**P2 — Decide what the append timestamp is for, or move it.** `lessons/02-record-framing.md:42`
puts an append timestamp in the frame. No main-path lesson makes a decision that depends on
it until `lessons/14-asynchronous-follower.md:46` requires the follower to preserve it, and
L09's age retention uses a clock seam (`:44`) rather than record timestamps. Concrete
action, either: extend `09-retention.md:49` so age retention is evaluated from the newest
record timestamp in a segment (which would make the field load-bearing eleven lessons
earlier), or move the field's introduction out of L02 and into L14 where it is first used.
This is the section-6 "concept nothing later uses" row; the field *is* eventually used, so
it is a question and not a finding.

**P3 — Make the read path's concurrency explicit.** `DESIGN.md:39`–`:40` says "Reads may use
immutable closed segments and carefully published active-state snapshots without mutating
append state." No lesson has a completion condition that requires a concurrent
fetch-while-appending test; the property is exercised only incidentally by L10 `:52` and
L12 `:52`, both under `-race`. Concrete action: add one completion condition to
`05-partition-ownership.md` — "A race-enabled test fetches from a partition concurrently
with appends and never mutates append state" — or to `12-long-polling-and-overload.md`
alongside `:62`. The anchor is served, so this costs nothing today; it closes the thinnest
seam in the course.

**P4 — Optionally hand over the JSON workload corpus. Explicitly not a toil finding.**
`13-observability-and-load.md:52` asks the learner to invent "several fictional services".
If the author wants that part handed over, the entry would be manifest-scope:

```
python3 scripts/supplies.py add \
  /Users/robert/src/github.com/skomp/tutorail-bundles/durable-event-broker \
  --from testdata/service-logs.jsonl \
  --to testdata/service-logs.jsonl \
  --describe "Fictional multi-service JSON application logs, used as one opaque broker workload" \
  --check
```

run from the `tutorail-authoring` skill's own directory, not this one. Two honest caveats.
First, **`testdata/service-logs.jsonl` does not exist in the bundle** — the skill names that
as the tell that something was never toil, and here it means the author would have to
author the corpus before declaring it. Second, a `--lesson`-scoped entry is **not available
in this bundle's layout**: lesson-scope `--from` must live inside that lesson's own folder,
and this bundle's lessons are flat files (`lessons/13-observability-and-load.md`), not
directories. Manifest scope, or a layout change first. No prose would be deleted either
way: `:52` would change from "add a JSON log producer representing several fictional
services" to "drive the supplied service-log corpus through the broker", and the generator
requirement at `:46` stays.

**P5 — No lesson scores at or below zero**, so no lesson is carried back to the author with
"what is this for?". The lowest figure is `02-record-framing.md` at 5, and section 2
explains at length why that number is a clause-granularity artefact rather than a weakness.
I would refuse a proposal to split L02's progression purely to raise it.

**P6 — No `required_for` gate exists, so the rubric's warning is not triggered.** See the
next section; this contradicts an expectation in the audit brief and is worth the author's
attention in its own right.

---

## 6. The questions only a reader can answer

### Correction to the audit brief, first

The brief stated: *"It declares `optional_lessons`, so the completability invariant is live
… A `required_for` gate on an optional lesson is −3 each AND must be raised with the
rubric's warning printed verbatim beside the score."*

The first half is right and is answered below. **The second half did not materialise.**
I opened `tutorial.yaml` and worked through the `optional_lessons:` block by hand rather
than trusting `optional_lesson_count`, as the skill instructs. The block spans
`tutorial.yaml:29`–`:49` and contains:

| Optional lesson | `offer_at` | `anticipates` | `repair_in` | `required_for` |
|---|---|---|---|---|
| `lessons/property-based-framing.md` | `:31` L02 | `:36` `frame-decoder-breaks-on-arbitrary-input` | `:37` L02 | **absent** |
| `lessons/tcp-transport.md` | `:39` L11 | absent | absent | **absent** |
| `lessons/page-cache-experiments.md` | `:45` L04 | absent | absent | **absent** |

`grep -n "required_for" tutorial.yaml` returns nothing. **Zero gates, so the row scores
0 x −3 = 0 and there is no score to print the warning beside.** For the record, the warning
the rubric would have required — **not triggered here** — is:

> This gate cost the course 3 points and may still be correct. If the lesson genuinely
> cannot be completed while its failure stands, the gate is doing its job — say so and
> keep it. Do not delete a gate to improve a score. A course that drops a justified gate
> lets a learner finish a lesson whose failure is still standing, which is worse than the
> toil this rubric hunts.

The absence is itself a small positive finding. `property-based-framing` declares
`anticipates` **without** `required_for`, which means a learner who declines the offer can
still finish `02-record-framing` with the anticipated failure mode standing — and the
`repair_in` points back to a main-path lesson (`:37`), which is the correct direction. That
is the shape the format wants when the gate is not genuinely load-bearing.

### Prose optionality vs manifest optionality

**They agree. No discrepancy found, and no alternative total is needed.**

- All three optional lessons carry `optional: true` in frontmatter
  (`page-cache-experiments.md:4`, `property-based-framing.md:4`, `tcp-transport.md:4`)
  **and** appear in `optional_lessons:` rather than `lessons:`.
- No lesson in `lessons:` describes itself as optional. Every main-path lesson carries a
  `## Optional deeper paths` heading, which is a section offering further reading, not a
  claim that the lesson is skippable. I checked every hit of the word "optional" in the 15
  main-path files: the others are `00-running-broker.md:22` ("an optional key") and
  `02-record-framing.md:42` ("optional key"), both about the record's key field.
- The three main-path references to optional lessons — `02-record-framing.md:69`,
  `04-durability-contract.md:69`, `11-http-api.md:72` — are all inside
  `## Optional deeper paths` and all conditional ("when the learner accepts it").

This is the opposite of the failure the rubric records from the webgl bundle. The
main-path-only figure of **112** is reported in section 1 because it is genuinely useful,
not because the manifest and the prose disagree.

### The completability invariant

> **Can a learner who declines every offer still finish this course?**

**Yes.** Checked against the lessons, not only against the manifest.

- *Does any main-path completion condition depend on something only an optional lesson
  builds or explains?* No. I read all 75 main-path completion conditions.
  `02-record-framing.md:58` ("No malformed input causes a panic or unbounded allocation") is
  the one that looks like it might need `property-based-framing`, and it does not: it is
  satisfiable from the hand-written truncation, version-mismatch and corruption tests
  assigned at `:51`–`:52`. `04-durability-contract.md:56`–`:60` needs no page-cache tracing.
  `11-http-api.md:59`–`:63`, `12`, `13` and `14` name only HTTP;
  `14-asynchronous-follower.md:54` builds on "the internal fetch and append mechanics", which
  are L11/L12 main-path work, never the TCP transport.
- *Does any main-path lesson's prose assume the learner took an offer?* No. The only three
  cross-references are the conditional ones listed above.
- The author has stated this claim themselves at `COURSE.md:87`–`:100`, and separated
  **complete** from **covered** while doing it. I checked the claim rather than accepting
  it, and it holds.

### A `design_refs` entry that does not answer the question its lesson raises

**One clear instance and one weaker one.**

- **`lessons/00-running-broker.md:4` → `#record-model` (`DESIGN.md:3`–`:7`).** The lesson's
  live question is byte-slice ownership — Theory `:32`–`:33`, Constraints `:47`–`:48`,
  completion `:61` — and the anchor answers a different question (JSON, headers, schema
  registries). The reference resolves, the validator would be green, and the learner does
  not find out why fetch must not expose mutable storage. Proposal P1.
- **`lessons/12-long-polling-and-overload.md:4` → `#backpressure-contract` (`DESIGN.md:81`–
  `:85`).** The anchor answers bounded queues and explicit overload well. It does not answer
  the lesson's other question, raised at Constraints `:45`: "Notification cannot be lost in a
  way that leaves available data waiting indefinitely." No anchor covers wait predicates or
  notification coalescing; the lesson's own Theory `:27`–`:30` answers it instead. Weaker,
  because the learner is not left without an answer — only without one in `DESIGN.md`.

All other 16 lessons: checked, and their `design_refs` answer their lessons' questions.
`#transport-boundary` for L11 and tcp, `#replication-boundary` for L14, and
`#recovery-policy` for L03 are the clearest positive cases.

### A lesson that introduces a type or concept nothing later uses

**One instance worth raising, plus two weaker candidates; none is fatal.**

- **The append timestamp, `lessons/02-record-framing.md:42`.** Introduced into the frame in
  lesson 02 and, on the main path, never *decided with* — only carried. Its first real use
  is `lessons/14-asynchronous-follower.md:46`, twelve lessons later, where it is preserved
  and asserted at `:61`. L09's age retention explicitly uses a clock or metadata seam
  (`:44`) rather than record timestamps, which is where a reader would expect the field to
  earn its keep. It *is* used, so this is a question and not a finding. Proposal P2.
- **The format version field, `lessons/02-record-framing.md:42`.** Nothing on the main path
  ever bumps it. But rejecting an unsupported version is a use, and it is tested at `:57`
  and recovered around at L03 — ruled **used**.
- **The metadata operation, `lessons/11-http-api.md:52`.** "then batch append and metadata"
  introduces a metadata endpoint that no later lesson's completion condition requires. L13's
  load generator plausibly consumes it and L09's earliest-available-offset is the obvious
  thing it exposes, but neither is stated. Worth a sentence from the author.

### A lesson far outside the course's usual size

**None found, in either direction.** This bundle's house style is the most uniform I could
ask for: all 18 lesson files fall between 66 and 77 lines (mean 70.5, `02` at 70 and `14` at
77 being the extremes), every one carries the same nine headings, and scored element counts
run 5 to 9. Nothing here is "usually two lessons" and nothing is "usually a paragraph of the
lesson beside it".

The corollary matters for reading section 2: because the size is uniform, the spread in
lesson figures (5 to 9) reflects **clause granularity inside `## Suggested progression`**
almost entirely, not depth. `02-record-framing.md` writes three fat clauses and scores 5;
`04-durability-contract.md` writes four thin ones plus two substantive completion conditions
and scores 9. They teach comparable amounts.

### A must-cover topic that only an optional lesson teaches

**Three, and the question is put to the author.**

| Coverage topic (`COURSE.md`) | Taught only by |
|---|---|
| `:127` property-based record-framing tests | `lessons/property-based-framing.md` |
| `:128` length-prefixed TCP protocols | `lessons/tcp-transport.md` |
| `:129` operating-system page-cache behaviour | `lessons/page-cache-experiments.md` |

> **Is that acceptable for this course, given that a learner who declines every offer never
> meets them?**

This is a question and not a score, permanently, and I am not scoring it. My own reading —
which the author is free to overrule — is **yes, and this course has already answered it
better than most**: `COURSE.md:89`–`:100` names all three explicitly, states the distinction
between complete and covered, and gives the reason they are in the list ("They are in the
list because the course does teach them and a tutor may offer them. They are not on the main
path because the course finishes without them."). That is exactly the outcome the rubric's
declined-row note wanted to protect: the topics stay in the coverage list, so a tutor offers
the authored lesson instead of improvising a replacement. The one thing the author might
reconsider is TCP framing specifically — `#transport-boundary` (`DESIGN.md:75`–`:79`) treats
the optional TCP transport as a first-class citizen of the design, which is a slightly
stronger claim than "optional".

### Dry-run evidence

No dry-run harness was run for this audit and none was supplied, so there is no stall to
cite either way. Absence of a dry run is not evidence about the course.

---

## Closing note, as the skill requires

I did not run the bundle validator and its result would not change anything above.
Structural validity and teaching quality are different questions: the validator answers
"is this a bundle?", and this report answers "does this teach?". In this case both answers
happen to be favourable — but "the validator passes" was never an input to any figure here.

**This report proposes and changed nothing.** The bundle is byte-identical to commit
`4df2624`.
