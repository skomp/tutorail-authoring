# Course quality audit — `portable-fixed-window-rate-limiter`

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

Audited 2026-09-13 against `tutorail-authoring:course-quality` v0.3.0 and its
`references/rubric.md`. Read-only: no file in the bundle was created, edited or staged.

Bundle path: `/Users/robert/src/github.com/skomp/tutorail-bundles/portable-fixed-window-rate-limiter`

Evidence gathered with:

```
cd /Users/robert/.claude/plugins/cache/tutorail-authoring/tutorail-authoring/0.3.0/skills/course-quality
python3 scripts/audit.py /Users/robert/src/github.com/skomp/tutorail-bundles/portable-fixed-window-rate-limiter
```

All four lessons, `tutorial.yaml`, `COURSE.md`, `DESIGN.md` and `STATE.template.md` were
opened in full. The score below comes from the lessons, not from the script.

---

## The rubric (printed in full, as the skill requires)

### The scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises (course-level, counted once per gap) |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised (course-level) |

### Two elements settled by the rubric rather than by the auditor

- **A branch point scores `evidence`, 0** — the teaching is in whichever branch is taken,
  and that branch is scored on its own.
- **A tutor-addressed element scores `teaching`, +2 when the learner must decide or
  construct in response.** Grammatical person does not change what the learner does.

### Rows a reader answers, and a script never scores

- a `design_refs` entry that does not answer the question its lesson raises;
- a lesson that introduces a type or concept nothing later uses;
- a lesson far outside the course's usual size, in either direction;
- a must-cover topic that only an optional lesson teaches — **a question, permanently, not
  a score.**

### The invariant no structural check can reach

> A course carrying optional lessons must be completable by a learner who declines every
> offer.

All of these are answered in section 6.

### Scoring conventions used here, stated so they can be checked

The rubric's figures are comparable *within one course's house style*. This course's house
style is a `## Suggested progression` bullet list plus a `## Completion conditions` bullet
list, so **each bullet in those two sections is one element**, plus the one free-standing
tutor-addressed paragraph at `lessons/02-boundaries-and-evidence.md:59-60`.

Two consistent exclusions, applied to all four lessons:

- `## On completion, persist` is tutor bookkeeping into tutor-owned files
  (`tutorial.yaml:26` lists `tutorial/STATE.md` and `tutorial/DESIGN.md` as `tutor_owned`).
  It assigns the learner nothing and is not scored in any lesson.
- `## Optional deeper paths` is conditional on the learner asking and is not scored in any
  lesson.

One consistent de-duplication rule, from the branch-point row's reasoning (*scoring the
fork as teaching would count the same instruction twice*): **a completion condition that
restates a progression step already scored in the same lesson scores `evidence`, 0.** A
completion condition demanding something no progression step demanded is scored on its own
merits. This matters most in lesson 02, where the burst explanation appears in both
sections; it is scored once.

**Do not set this course's total beside another course's.** Three fat lessons enumerated
this finely are not on the same ruler as a fifteen-lesson course.

---

## 1. The course and its total

| | |
|---|---|
| Bundle id | `portable-fixed-window-rate-limiter` |
| Title | Build a Fixed-Window Rate Limiter |
| Main-path lessons | 3 |
| Optional lessons | 1 (`lessons/concurrent-callers.md`) |
| `DESIGN.md` anchors | 5 |
| `supplies:` entries | 0 |
| Coverage topics declared | 10 |

**Arithmetic**

```
lesson 00-contract-and-language    +9
lesson 01-windowed-counting       +10
lesson 02-boundaries-and-evidence  +8
lesson concurrent-callers (opt)    +8
                                  ----
sum of lessons                     35

course-level penalties:
  unserved objectives        0 x -3 =  0
  unserved DESIGN.md anchors 0 x -3 =  0
  required_for gates on an
    optional lesson          0 x -3 =  0
                                  ----
COURSE TOTAL                       35
```

**Total as a learner who declines every offer earns it: 27.** The optional lesson banks 8
points that such a learner never sees. Reported separately, per the rubric's
prose-optionality section, so the headline figure cannot be mistaken for what the main path
alone teaches. Here the manifest and the prose agree that the lesson is optional (see
section 6), so the 35 is not the inflated figure that section warns about — but 27 is the
number to quote when comparing the main path against anything.

**Two statements the skill asks for plainly:** the bundle loads cleanly and would almost
certainly pass the structural validator; that is not what this report measures. And the
script's toil scanner returned zero candidates; that is a fact about the scanner's verb
list, not about the course. The zero in section 4 is mine, from the lessons.

---

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil found |
|---|---|---|---|
| `lessons/00-contract-and-language.md` — Make the decision precise | **+9** | 3 of 3 | none |
| `lessons/01-windowed-counting.md` — Count requests in deterministic windows | **+10** | 4 of 4 | none |
| `lessons/02-boundaries-and-evidence.md` — Attack the boundaries | **+8** | 4 of 4 | none |
| `lessons/concurrent-callers.md` *(optional)* — Make one decision atomic | **+8** | 4 of 4 | none |

No lesson scores at or below zero, so no lesson triggers the rubric's "what is this lesson
for?" question. Full element breakdowns follow for all four anyway, because three of the
four figures (9, 8, 8) are not obvious from their rows.

### `lessons/00-contract-and-language.md` — +9

| `file:line` | Sentence scored | Element | Score |
|---|---|---|---|
| `:50` | "Ask which language the learner wants and why; adapt all later guidance to it." | teaching | +2 |
| `:51-52` | "Create the smallest conventional runnable project and initialise version control if the learner wants it." | practice | +1 |
| `:53` | "Define the public contract in prose and then as an API signature or stub." | teaching | +2 |
| `:54` | "Add one focused test or executable example covering the budget within one window." | teaching | +2 |
| `:58` | "The project runs using the normal toolchain for the selected language." | evidence | 0 |
| `:59` | "The public API accepts a client key and exposes an allow/reject decision." | evidence | 0 |
| `:60-61` | "A test or executable example states that the first `N` requests are allowed and request `N + 1` is rejected." | evidence | 0 |
| `:62-63` | "The learner can explain which parts are contract and which remain implementation choices." | teaching | +2 |
| | | **sum** | **+9** |


Notes on the two elements most easily scored differently:

- `:50` is **not** the rubric's branch point. The branch-point row exists so an authored
  fork is not counted twice — once at the fork and once in the branch that is scored on its
  own. There are no authored language branches here: the choice is made once, nothing else
  in the course scores it, and the learner must justify it ("and why"). It is a decision
  whose wrong answer is instructive (a language with no concurrency model makes the optional
  lesson meaningless, per `lessons/concurrent-callers.md:16-17`). Teaching, +2.
- `:51-52` is setup, and setup is not automatically practice. It scores +1 rather than 0
  because "smallest **conventional**" requires the learner to apply their own language's
  conventions, and rather than −2 because the bundle cannot ship the result — see section 4.

### `lessons/01-windowed-counting.md` — +10

| `file:line` | Sentence scored | Element | Score |
|---|---|---|---|
| `:54` | "Introduce the replaceable time source and prove the test controls it." | teaching | +2 |
| `:55` | "Represent one client's current window and count." | teaching | +2 |
| `:56` | "Generalise the state to multiple client keys." | practice | +1 |
| `:57` | "Make the existing budget example pass." | practice | +1 |
| `:58` | "Add a test that advances into a new window and observes a fresh budget." | teaching | +2 |
| `:62` | "The first `N` requests for a key in one window are allowed and `N + 1` is rejected." | evidence | 0 |
| `:63` | "A request at the exact start of the following window is allowed." | evidence | 0 |
| `:64` | "Two distinct keys receive independent budgets." | evidence | 0 |
| `:65` | "The relevant test suite passes without real-time waiting." | evidence | 0 |
| `:66` | "The learner can describe the stored state and the average cost of one decision." | teaching | +2 |
| | | **sum** | **+10** |

`:55` is teaching rather than practice because the lesson's own Theory (`:27-29`) refuses to
give the formula — "the course specifies semantics rather than a formula" — so the
representation is the learner's decision. `:56` is its generalisation into a keyed container
and `:57` is making an already-written example green; both apply what `:55` decided, which
is the practice row exactly.

This is the highest-scoring lesson in the course and it is the one that earns it: four of
its five progression steps put a construction or a decision in the learner's hands.

### `lessons/02-boundaries-and-evidence.md` — +8

| `file:line` | Sentence scored | Element | Score |
|---|---|---|---|
| `:53` | "Ask the learner to predict the boundary behaviour before running it." | teaching | +2 |
| `:54` | "Add or sharpen the smallest set of tests that distinguishes correct semantics." | teaching | +2 |
| `:55` | "Review names and public API clarity in the selected language." | teaching | +2 |
| `:56` | "Run the complete test suite and a small demonstration." | evidence | 0 |
| `:57` | "Have the learner explain the boundary burst and retained-state limitation." | teaching | +2 |
| `:59-60` | "Before the first task, make the authored optional lesson offer from the manifest. A learner who declines it must still be able to complete this lesson and the course." | evidence (branch point) | 0 |
| `:64` | "All contract, rollover, boundary, and client-isolation tests pass." | evidence | 0 |
| `:65` | "The project runs through its documented commands without unexplained failures." | evidence | 0 |
| `:66` | "The learner can explain the `2N` boundary burst and why it follows from fixed windows." | evidence (restates `:57`) | 0 |
| `:67-68` | "The learner can identify at least fixed-window burstiness and inactive-key retention as limitations without claiming the implementation solves them." | evidence (restates `:57`) | 0 |
| | | **sum** | **+8** |

Two scoring calls worth arguing with:

- `:53` is tutor-addressed ("Ask the learner to…") and scores +2 under the rubric's settled
  row: predict-then-run is the single most instructive wrong answer in the course, because
  a learner who predicts "the limit holds across the boundary" discovers the `2N` burst by
  being wrong about it.
- `:59-60` **is** the rubric's branch point — take the optional lesson or skip it — and
  scores 0. The teaching lives in `lessons/concurrent-callers.md`, which is scored on its
  own. Note that this element is also the thing that discharges the completability
  invariant in prose; scoring it 0 is not a criticism of it.
- `:66` and `:67-68` restate `:57` and score 0 under the de-duplication rule above. Under a
  rule that scored every completion condition on its own merits this lesson would total
  +12, making it the course's strongest. Either rule is defensible; the one used here is
  applied identically to all four lessons, and lessons 00 and 01 have explanation
  conditions that are *not* restatements and do score +2. The author should know that this
  lesson's +8 is a consequence of the lesson saying the same excellent thing twice, not of
  the lesson being weak.

### `lessons/concurrent-callers.md` *(optional)* — +8

| `file:line` | Sentence scored | Element | Score |
|---|---|---|---|
| `:55` | "Inspect the existing decision path and mark its critical section." | teaching | +2 |
| `:56` | "Choose the smallest idiomatic synchronisation mechanism." | teaching | +2 |
| `:57` | "Launch more than `N` concurrent attempts against one key and collect decisions." | teaching | +2 |
| `:58` | "Confirm exactly `N` successes, then rerun the sequential suite." | evidence | 0 |
| `:59` | "Discuss contention and possible finer-grained designs without requiring them." | evidence | 0 |
| `:63-64` | "Concurrent attempts against one key never produce more than `N` allowed decisions in the exercised test." | evidence (restates `:58`) | 0 |
| `:65` | "The sequential contract and boundary tests still pass." | evidence | 0 |
| `:66-67` | "The learner can explain why the original implementation could race and what now makes a decision atomic." | teaching | +2 |
| | | **sum** | **+8** |

`:59` scores 0 rather than +2 because the lesson explicitly attaches no requirement to it
("without requiring them") — nothing is decided, constructed or demonstrated. `:66-67` is
not a restatement of anything in the progression and demands a new articulation (memory
safety versus behavioural atomicity, `:22`), so it scores +2.

---

## 3. Goal gaps

**No unserved objectives and no unserved anchors. The gap penalty is 0 × −3 = 0, and
section 1's arithmetic agrees.**

This contradicts the expectation in the audit brief that three lessons against ten coverage
topics would leave "some genuine gaps". It does not, and the reasoning for every topic and
every anchor is below so the ruling can be checked rather than taken. The brief is right
that three lessons is a thin budget for ten topics; the reason it works here is that the
topics are unusually tightly nested — six of the ten are aspects of the one vertical slice
built in lesson 01.

Each item is judged on **what a task makes the learner do**, never on whether a
`design_refs` list cites it.

### The 15 lesson learning objectives

| Objective (`file:line`) | Served by | Verdict |
|---|---|---|
| 00 `:20` Separate a behavioural contract from an implementation strategy | `00:53`, `00:62-63` | served |
| 00 `:21` Choose an API shape that is idiomatic in the selected language | `00:50`, `00:53`, `02:55` | served |
| 00 `:22` Establish a fast run-and-test feedback loop | `00:51-52`, `00:54`, `00:58`, `01:65` | served |
| 01 `:20` Derive a stable fixed-window identifier from time | `01:55` | served |
| 01 `:21` Maintain independent state per client key | `01:56`, `01:64` | served |
| 01 `:22` Inject nondeterminism at a narrow boundary | `01:54` | served |
| 01 `:23` Test time-dependent behaviour deterministically | `01:58`, `01:65` | served |
| 02 `:19` Select tests that establish semantics rather than inflate coverage | `02:54` | served |
| 02 `:20` Recognise the burst characteristic at adjacent fixed-window boundaries | `02:53`, `02:57` | served |
| 02 `:21` Review an implementation against its stated contract | `02:55`, `02:64` | served, thinly — see proposal 4 |
| 02 `:22` Communicate scope and limitations precisely | `02:57`, `02:67-68` | served |
| opt `:21` Identify the read-modify-write critical section | `opt:55` | served |
| opt `:22` Choose synchronisation appropriate to the selected language | `opt:56` | served |
| opt `:23` Distinguish memory safety from behavioural atomicity | `opt:66-67` | served |
| opt `:24` Design a concurrency test that can reveal over-admission | `opt:57` | served |

`02:21` is the only one I nearly ruled against. "Review an implementation against its stated
contract" is broader than `02:55`'s "Review names and public API clarity", which reviews the
API surface rather than the implementation. It survives because `02:64` requires the whole
contract suite to pass and `02:53` makes the learner predict behaviour against the contract
before observing it. It is served by a task, so it is not a −3; it is weak enough to
propose sharpening.

### The 10 `COURSE.md` coverage topics

| Topic | Ruling | How I decided |
|---|---|---|
| implementation-language selection | served | `00:50` is a task and the learner decides, with a justification demanded. |
| behavioural API contracts | served | `00:53` constructs one, `00:62-63` makes the learner defend its boundary, `02:55` reviews it. |
| fixed-window rate limiting | served | `01:55`, `01:57`, `01:62` build and demonstrate the counter itself. |
| per-client state | served | `01:56` generalises state to keys; `01:64` requires independent budgets. |
| dependency injection for time | served | `01:54` builds the injection point and proves the test drives it. |
| deterministic tests | served | `01:49` forbids sleeping, `01:58` adds the clock-advancing test, `01:65` requires the suite to pass without real-time waiting. |
| boundary conditions | served | `02:53` predict, `02:54` sharpen, `02:45-46` constrains what the tests must cover, `01:63` requires the exact-boundary case. |
| client isolation | served | `01:64` and `02:47` both require it, with a test. |
| algorithmic trade-offs | served — closest call in the audit | See below. |
| concurrency safety | served **only by the optional lesson** — raised as a question, not scored | `lessons/concurrent-callers.md` is the only lesson with a task. Rubric row; see section 6. |

**`algorithmic trade-offs`, and why it is not a −3.** A sceptical reading says a trade-off
needs an alternative to trade against, and every comparison with sliding logs, sliding
counters and token buckets is fenced behind "if asked" (`01:75-76`) or "discuss—but do not
implement" (`02:77-78`). On that reading the topic is unserved and the course total is 32,
not 35. I rule it served because the course's own definition of the phrase is narrower and
is stated twice: `COURSE.md:30-31` glosses lesson 02 as "explain the trade-offs" and
`COURSE.md:38-39` as "the learner can explain what the algorithm does not guarantee". That
is exercised by required tasks — `02:57` and `02:67-68` make the learner name the `2N` burst
and unbounded key retention as costs of *this* algorithm, and `02:26-30` insists the burst
is a property rather than a bug. Comparative trade-offs are explicitly out of scope at
`COURSE.md:59-63`. The author may disagree; the arithmetic for the other ruling is stated
above so the disagreement is cheap to settle.

### The 5 `DESIGN.md` anchors

Judged on what lessons make the learner do, not on `design_refs`.

| Anchor | Ruling | Evidence |
|---|---|---|
| `#behavioural-contract` | served | `00:53` writes the contract, `00:60-61` and `01:62` require exactly the `N`-allowed / `N+1`-rejected behaviour the anchor specifies. |
| `#window-semantics` | served | The anchor's load-bearing clause is "a request exactly at a boundary belongs to the new window"; `01:48`, `01:63` and `02:46` make the learner test precisely that. |
| `#state-model` | served | Per-key in-memory state built at `01:55-56`; the anchor's "must not scan all recorded requests" clause is exercised by `01:46` (constant-time constraint) and `01:66` (describe the average cost of one decision). |
| `#time-source` | served | `01:54` builds the replaceable source, `01:49` and `01:65` forbid waiting on wall-clock time. |
| `#concurrency-boundary` | served, with the same caveat as the coverage topic | The anchor is half a scoping decision and half an extension. Its scoping half is honoured on the main path by `01:50` ("Keep the implementation in memory and single-process") and by the offer at `02:59-60`; its active half — actually synchronising — is done only in the optional lesson. Not a −3: main-path tasks do what the anchor says the main path does. Raised in section 6 alongside `concurrency safety`. |

Notably `#concurrency-boundary` is cited only by the optional lesson's `design_refs`
(`lessons/concurrent-callers.md:4`) and yet is honoured by main-path lessons that never cite
it — the exact pattern the rubric warns not to decide by grep.

---

## 4. The toil inventory

**Confirmed toil sites: none. −2 was applied zero times.**

`audit.py` returned `(none found)` for toil candidates. As the skill and the script both
say, that is evidence about the scanner's fixed verb list, not about the course. **This
inventory comes from opening all four lessons and reading every element**, all 36 of them,
listed with `file:line` in section 2. The scanner's silence played no part in the ruling.

### Candidates I examined myself and rejected, so the next reader need not re-litigate

The scanner produced nothing to reject, so these are mine, taken from the lessons.

| `file:line` | Sentence | Why it is not toil |
|---|---|---|
| `00:51-52` | "Create the smallest conventional runnable project and initialise version control if the learner wants it." | **Rejected because the bundle could not have supplied the result.** This is a portable bundle: the language is unknown until `00:50` executes, so there is no `--from` path that could ship a `go.mod`, a `package.json`, a `Cargo.toml` or a `pyproject.toml`. Setup needing a toolchain is the learner's work under the toil row's last clause. Scored +1 for what it is. |

| `00:54`, `01:58`, `02:54` | "Add one focused test…", "Add a test that advances into a new window…", "Add or sharpen the smallest set of tests…" | The learner chooses the assertions and, in `02:54`, which tests are worth having at all. Not deterministic, not unambiguous, and a mistake is instructive. |
| `01:57` | "Make the existing budget example pass." | The implementation being made to pass is the learner's own and does not exist yet. Practice, +1. |
| `02:56` | "Run the complete test suite and a small demonstration." | This is the evidence step the format is built around, not a result the bundle could have shipped. Scored 0. |
| `opt:58` | "Confirm exactly `N` successes, then rerun the sequential suite." | Same: reading a result, scored 0. |
| `00:67-68`, `01:70-71`, `02:72-73`, `opt:71-72` | the four `## On completion, persist` blocks | Addressed to the tutor and writing into `tutor_owned` files (`tutorial.yaml:26`). They assign the learner nothing, so there is no learner task to call toil. |

### Why there is nothing to propose a `supplies.py` command for

`audit.py` reports **0 `supplies:` entries**, and that is correct rather than an omission.
The skill notes that "`--from` naming a file the bundle does not contain is the tell that
this was never toil". Here the bundle contains no source file at all — only `COURSE.md`,
`DESIGN.md`, `STATE.template.md`, `tutorial.yaml` and four lessons. Every artifact the
course produces is language-dependent and chosen at runtime by the learner, so there is
nothing the author could have shipped and did not. **No supplies proposal is made in
section 5, deliberately**, and the absence of `supplies:` is not a finding against this
bundle.

---

> **OPEN, `tutorail-authoring#11` — the `00:51-52` rejection above.** It assumed one fixed
> `--from` path. A portable bundle can ship one skeleton per supported language and let the
> tutor choose after `00:50`. If the author rules the step toil, the element goes +1 -> -2
> and the course scores **32**, not 35. A learner hit exactly this step and asked for the
> setup (`skomp/tutorail-bundles#3`).

## 5. Proposals

Every one is a concrete action, and every one is refusable. Applying any of them is the
`tutorail-authoring` skill's job, not this one's; nothing in the bundle was changed here.

### Proposal 1 — give lesson 02's retention limitation an anchor that answers it

**Finding** (also section 6, row 1). `lessons/02-boundaries-and-evidence.md:4` declares
`design_refs: [behavioural-contract, window-semantics, state-model]`. The lesson raises two
limitations and requires the learner to name both: the `2N` burst and inactive-key
retention (`:32-33`, `:49`, `:67-68`). `#window-semantics` answers the burst. **Nothing in
`DESIGN.md` answers the retention question** — `#state-model` (`DESIGN.md:18-22`) says state
is per-key, in-memory and non-scanning, and says nothing about growth, eviction or cleanup.
A learner who follows the citation to find out why cleanup is not required does not find
out.

**Action.** Through `tutorail-authoring`, either extend `#state-model` with the retention
decision, or add a new anchor and cite it:

```
## Retention limits {#retention-limits}

State for a key persists after its window ends. Bounded-memory eviction is a production
concern and is deliberately outside this course; the limitation is named rather than
solved, so that a learner does not present the component as bounded in memory.
```

then add `retention-limits` to `lessons/02-boundaries-and-evidence.md:4`. This also
strengthens `02:67-68`, which currently requires the learner to state a limitation the
design document never states.

### Proposal 2 — decide what to do about `concurrency safety` (author's call, not a score)

**Finding** (section 6, row 4). `concurrency safety` is in `COURSE.md:57` as a must-cover
topic and the only lesson that teaches it is the optional `lessons/concurrent-callers.md`.
**This costs the course nothing in the total and must not**; the rubric settled that
permanently. It is a question the author answers.

If the answer is "acceptable", record it and change nothing — the case is strong:
`DESIGN.md:30-34` argues the mechanisms vary too much between runtimes to put on a portable
main path, and `COURSE.md:9` budgets the main path at 60–90 minutes.

If the answer is "not acceptable", the recommended action is **not** to promote the lesson
and **not** to drop the topic from the coverage list — dropping it produces the outcome the
bundle format calls worse, a tutor improvising material the author already wrote. Instead
add one main-path completion condition to `lessons/02-boundaries-and-evidence.md` that
requires the learner to *name* the race without fixing it, leaving the fix optional:

> - The learner can identify the read-modify-write sequence in one decision as a critical
>   section, and say why the sequential implementation is not safe under concurrent callers.

That serves the topic on the main path in one element, keeps the fix in the optional lesson
where the language-specific mechanisms belong, and leaves the `2N`-burst-style "name the
limitation" pattern the course already uses twice.

### Proposal 3 — sharpen `02:55` so it serves its objective fully

**Finding** (section 3). The objective at `lessons/02-boundaries-and-evidence.md:21` is
"Review an implementation against its stated contract"; the only task serving it,
`:55`, reads "Review names and public API clarity in the selected language" — an API-surface
review, not a review against the contract. Not a gap, because `:53` and `:64` reach it
indirectly, but the objective promises more than the task asks.

**Action.** Replace `:55` with something like:

> - Review the implementation against the contract recorded in `DESIGN.md`, naming any
>   behaviour the contract does not cover and any name that misleads about it.

This also converts a +2 element into one that genuinely earns it, and it pairs with
Proposal 1 by giving the learner a reason to read `DESIGN.md` at this point.

### Proposal 4 — drop or land "evidence-based completion"

**Finding** (section 6, row 2). `lessons/02-boundaries-and-evidence.md:41` lists
"evidence-based completion" under `## Concepts to teach`, and no task in the lesson teaches
it. It is the runner's mechanism (`tutorial.yaml:51`, `advance_on: validated-evidence-only`)
rather than a concept about rate limiting, and the other four entries in that list all have
tasks.

**Action.** Either delete the bullet, or — if the author wants the learner to internalise it
— fold it into `02:57` as "…and explain what evidence would convince a reviewer that the
limiter is correct". The first is the smaller change and is probably right.

### Proposal 5 — no toil fix, and no `supplies:` entry, on purpose

Stated as a proposal so it is not mistaken for an omission: **there is nothing to propose
here.** Section 4 explains why a portable bundle that ships no source file has no toil the
rubric can charge it for. If a future revision starts shipping a reference test harness or
a language-specific starter, this row becomes live again.

### Not proposed: any lesson deletion or restructure

No lesson scores at or below zero, no lesson is far outside the course's usual size, and
the course's ratio of decisions to evidence steps is high — 17 of 36 elements are `teaching`.
There is no structural proposal worth making.

### One observation, below the level of a proposal

Both validators are `kind: manual` (`tutorial.yaml:45-47`) while `advance_on:
validated-evidence-only` (`:51`). Every completion condition in the course therefore rests
on the tutor's judgement rather than on a command's exit status. For a portable bundle that
cannot know the test runner, that is the only available design and it is not a finding — but
it does mean the course's `evidence` elements are only as good as the tutor reading them,
which is worth the author knowing when they consider Proposal 2's "the learner can
identify…" wording.

---

## 6. The questions only a reader can answer

None of these is scored. All of them are answered.

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

**One instance found.**

- **`lessons/02-boundaries-and-evidence.md:4`** — `state-model`, as the citation covering
  the inactive-key retention limitation the lesson raises at `:32-33` ("State for inactive
  keys can also grow without bound"), constrains at `:49` and requires the learner to
  articulate at `:67-68`. `DESIGN.md:18-22` says nothing about retention, growth or
  cleanup. The anchor exists, the reference resolves, the validator is green, and a learner
  who follows it to find out why cleanup is not required still does not find out. Proposal
  1 addresses it.

Checked and clear: `lessons/00-contract-and-language.md:4` (`behavioural-contract` answers
exactly the contract question the lesson raises, including the "extra information such as
remaining capacity is a learner choice" clause at `DESIGN.md:9-10` that `00:72-73` leans
on); `lessons/01-windowed-counting.md:4` (all four anchors answer questions the lesson
raises, and `#time-source` answers the "why not sleep" question directly);
`lessons/concurrent-callers.md:4` (`#concurrency-boundary` answers the lesson's own "why is
this optional" question at `DESIGN.md:30-34`).

Worth noting in the other direction, which the rubric says is fine and not a finding:
`lessons/02-boundaries-and-evidence.md` honours `#concurrency-boundary` at `:59-60` by making
the offer, without citing it.

### 6.2 A lesson that introduces a type or concept nothing later uses

**One minor instance found.**

- **`lessons/02-boundaries-and-evidence.md:41`** — "evidence-based completion" is listed as
  a concept to teach and no task in that lesson or anywhere later uses it as a concept. It
  is the runner's advancement mechanism, not subject matter. Small, but it cost a line in
  the one list the tutor reads to decide what to say. Proposal 4.

Everything else traces forward. `00:37` "public API versus internal representation" is used
by `01:55-56` and reviewed at `02:55`. `01:39` "half-open intervals and exact boundaries" is
the thing `02:54` and `02:64` test. `01:40` "maps or dictionaries keyed by client identity"
is required by `01:64` and `02:47`. `01:41` "injected clocks, functions, or interfaces" runs
through `01:65` and into every later test. `00:72-73`'s remaining-capacity discussion is
explicitly fenced as optional and as a learner choice, so it is not an introduced concept
left dangling. Within the optional lesson, all five of `opt:39-43` are used by its own
tasks.

### 6.3 A lesson far outside the course's usual size

**None found.** The course is unusually uniform in both measures:

| Lesson | Lines | Scored elements | Score |
|---|---|---|---|
| `00-contract-and-language.md` | 73 | 8 | +9 |
| `01-windowed-counting.md` | 76 | 10 | +10 |
| `02-boundaries-and-evidence.md` | 78 | 10 | +8 |
| `concurrent-callers.md` | 77 | 8 | +8 |

Nothing here is a lesson that should be two lessons, and nothing is a paragraph that has
been given its own file. No action.

### 6.4 A must-cover topic that only an optional lesson teaches

**One instance, and it is the rubric's canonical case.**

`COURSE.md:57` lists **`concurrency safety`** among "Topics this course must cover". The
only lesson with a task that teaches it is `lessons/concurrent-callers.md`, which
`tutorial.yaml:17-23` declares optional and `lessons/concurrent-callers.md:6` marks
`optional: true`. The main path actively steers away from it: `lessons/01-windowed-counting.md:50`
instructs "Keep the implementation in memory and single-process", and `DESIGN.md:30-34`
makes the exclusion a design decision rather than an oversight.

**This is deliberately a question and not a score. It costs this course nothing** — the
rubric records that scoring this row was proposed on the first real run, cost one course
−6, and was declined permanently, because penalising it pushes authors to delete the topic
from the coverage list and so to have the tutor improvise material the author had already
written. The audit brief was right to flag this and right about the handling.

So, asked in the rubric's words:

> **Is it acceptable for this course that `concurrency safety` is taught only by an
> optional lesson, given that a learner who declines every offer never meets it?**

My reading of the evidence, offered as input and not as a ruling: the case for yes is
strong. `DESIGN.md:30-34` gives a reason that is about the subject rather than about
convenience — synchronisation mechanisms and the tests worth writing for them vary strongly
between runtimes, and a portable course that mandated one would either prescribe a mutex
recipe across languages (which `lessons/concurrent-callers.md:33-35` explicitly forbids) or
exclude languages whose model does not fit. `COURSE.md:9` budgets 60–90 minutes for the main
path, which the three main lessons already fill. Against it: "must cover" is what the
heading says, and a learner who finishes the main path has a limiter they might reasonably
believe is safe to share, having never been told it is not.

That middle position is what Proposal 2 is for: name the race on the main path, fix it
optionally. The decision is the author's.

The same question, in its anchor form, applies to **`#concurrency-boundary`**
(`DESIGN.md:30`): its scoping half is honoured on the main path, its active half only in the
optional lesson. It is scored served (section 3) and raised here for the same answer.

### 6.5 The completability invariant

`tutorial.yaml` contains an `optional_lessons:` key (`:17`), so the invariant is live. I
keyed off the key's presence in the manifest, not off `optional_lesson_count`.

> **Can a learner who declines every offer still finish this course?**

**Yes.** Answered from the main-path lessons, on all three tests:

1. **Does any main-path completion condition depend on something only an optional lesson
   builds or explains?** No. `00:58-63`, `01:62-66` and `02:64-68` were read in full. Lesson
   02's four completion conditions require the contract/rollover/boundary/isolation tests to
   pass, the project to run, the `2N` burst explained and the two limitations named. None
   mentions atomicity, synchronisation, threads or concurrent callers. The limitations the
   learner must name at `02:67-68` are "fixed-window burstiness and inactive-key retention"
   — deliberately not the race.
2. **Does any main-path lesson's prose assume the learner took an offer?** No, and the
   course goes further than not assuming it: `lessons/01-windowed-counting.md:50` positively
   removes the dependency ("Keep the implementation in memory and single-process"), and
   `lessons/02-boundaries-and-evidence.md:59-60` states the invariant in the lesson itself —
   "A learner who declines it must still be able to complete this lesson and the course."
   That is the obligation from `bundle-format.md` section 13 written into the material by the
   author. It is the best-handled instance of this invariant I can point at in this bundle.
3. **Prose optionality versus manifest optionality.** They agree, in all four places.
   `lessons/concurrent-callers.md` carries `optional: true` in its front matter (`:6`), sits
   under `optional_lessons:` in `tutorial.yaml:18`, is listed under `## Optional lessons` in
   `COURSE.md:41-44` and is marked *(optional)* in that entry's own text. No main-path lesson
   calls itself optional anywhere in its prose. There is no disagreement to report, so the
   35 in section 1 is not the inflated figure the rubric's prose-optionality section warns
   about. The 27 that a declining learner earns is reported alongside it regardless.

### 6.6 `required_for`, `anticipates` and `repair_in` — read from the manifest directly

The audit brief correctly noted that `audit.py` does not report these, so I opened
`tutorial.yaml` and read the `optional_lessons:` block (`:17-23`) in full. It contains
exactly two keys under `lessons/concurrent-callers.md`: `offer_at` (`:19`) and
`offer_because` (`:20-23`).

**No `required_for`, no `anticipates` and no `repair_in` appear anywhere in the manifest.**
Verified against the whole file, not only that block. The −3 gate row therefore fires zero
times and the rubric's gate warning is not printed as a live finding — the course has no
gate to justify or to defend.

For the record, had one existed the report would carry the rubric's warning verbatim beside
the −3; the brief was right to require it and right that the count of optional lessons found
on disk is the wrong thing to key off.

### 6.7 Dynamic evidence

No dry-run harness transcript was available for this bundle, so no stall is cited either
way. The absence of one is not evidence the course completes; it is an absence.

---

## Closing note on what this report is

The validator would almost certainly pass this bundle, and that is not an argument about
anything above. What the lessons show is a small course with an unusually high proportion of
learner decisions — 17 of 36 scored elements are `teaching` — that honours all five of its
design anchors and serves all 15 of its lesson objectives, and whose weakest points are a
citation that does not answer its lesson's question, one objective promised more broadly
than its task delivers, and one must-cover topic parked behind an optional offer.

Every finding above is a proposal the author may refuse, and every one carries a `file:line`
and a quoted sentence so it can be checked rather than believed.
