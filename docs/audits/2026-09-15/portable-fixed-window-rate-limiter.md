# Course quality audit — `portable-fixed-window-rate-limiter`

**Date: 2026-09-15.** Supersedes `docs/audits/2026-09-13/portable-fixed-window-rate-limiter.md`
(total 32, main path 24). Every delta from that report is explained in the section *Deltas
from 2026-09-13* below, with its cause named as one of three: the bundle changed, the rubric
changed, or the earlier report was wrong.

---

## Provenance

Reproduced verbatim from the audit-run provenance record, which is identical for all five
bundles in this run:

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

Confirmed for this bundle specifically, by running the pinned validator myself:

```
tutorAIl validator - mode: bundle
target:      .../tutorail-bundles/portable-fixed-window-rate-limiter
yaml reader: restricted (built in, stdlib only)
...
PASS - every applicable check ran and found nothing.
exit=0
```

The whole `scripts/` directory was pinned, not just `validate_bundle.py`, because that file
imports `yamlite` and `catalogs` from beside itself; a single-file pin produces a validator
that cannot run and fails in a way that reads as product defects (`FAIL - 0 finding(s)`).
The run above reports a real check inventory and exit 0, so it ran.

**A green validator is not a good course.** The validator answers *is this a bundle?* This
report answers *does this teach?* Nothing below rejects the bundle, and
`validate_bundle.py` is unchanged by this audit.

**Bundles repo state.** `git status --porcelain` in `skomp/tutorail-bundles` was empty at the
start of this audit and empty at the end. Nothing in that repository was created, edited or
staged. This audit wrote exactly one file, in `skomp/tutorail-authoring`:
`docs/audits/2026-09-15/portable-fixed-window-rate-limiter.md`.

---

## The rubric (printed in full, as the skill requires)

### The scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises; course-level, counted once per unserved objective |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable; scored **and** raised |

Key clauses carried from the rubric's prose, because they decide this bundle:

- **The toil row's last clause is load-bearing.** Setup that needs the network, a toolchain
  or an account is the learner's work and is not toil. The question is never *"is this
  boring?"* but *"could this bundle have shipped the result?"*
- **A project skeleton is toil — the tiebreak, ruled 2026-09-13.** Where shippability and
  "needs the toolchain" disagree, shippability wins, asked in its full form: *could the
  bundle have shipped one set of files for each language the course supports?*
- **The exception: setup that is itself the subject.** Operational test — *is the setup step
  the ONLY element serving the objective that names it?* Yes → exception. No → toil.
- **A step the tutor performs is not an element.** Not toil, not evidence at 0. **No act to
  score.** Two guards: (1) the learner must not still do it; (2) the hand-over must be
  declared in the lesson text **and** in `ownership_policy`.
- **The objective does not disappear with the element.** If the tutor-performed step was the
  only server of an objective, that objective now pays −3.
- **A branch point scores `evidence`, 0.** **A tutor-addressed element scores `teaching`,
  +2, when the learner must decide or construct in response.**
- **The decomposition is mandatory.** Every element carries its own score, `file:line` and
  sentence; a lesson's figure is the visible sum of its elements; course-level gaps are shown
  separately. **Totals are comparable within one course's house style, never between courses.**

### The six rows a reader answers, and a script never scores

1. a `design_refs` entry that does not answer the question its lesson raises;
2. a lesson that introduces a type or concept nothing later uses;
3. a symbol or term a lesson uses and no lesson introduces — **a `DESIGN.md`-only binding
   does not count**, because the runner loads an anchor for the tutor and not for the
   learner; report the `file:line` of the **first use**, and keep *bound only in `DESIGN.md`*
   separate from *bound nowhere*;
4. a lesson that does not equip the tutor to end a turn with one concrete action — passes
   when **both** hold: the lesson names the first concrete action (a file, a command or an
   artifact, not only the outcome), **and** the lesson separates decisions from actions,
   keeping a design decision the learner must make out of the closing action. **Grade the
   lesson FILE, never the tutor's turns.**
5. a lesson far outside the course's usual size, in either direction;
6. a must-cover topic that only an optional lesson teaches — *is that acceptable for this
   course, given that a learner who declines every offer never meets it?*

Rows 3 and 4 are new since the report this one supersedes; that report answered four rows,
this one answers six.

### The invariant no structural check can reach

> **A course carrying optional lessons must be completable by a learner who declines every
> offer.**

### `required_for` — the warning the rubric requires beside any such score

> This gate cost the course 3 points and may still be correct. If the lesson genuinely cannot
> be completed while its failure stands, the gate is doing its job — say so and keep it. Do
> not delete a gate to improve a score.

This course has **no** `required_for` gate (verified in section 6.7), so the warning is
printed here for completeness and fires against nothing.

### Scoring conventions used here, stated so they can be checked

These are **identical to the conventions of the 2026-09-13 report**, deliberately, so the two
totals are measured with the same ruler and the deltas below mean something.

This course's house style is a `## Suggested progression` bullet list plus a
`## Completion conditions` bullet list, so **each bullet in those two sections is one
element**, plus the one free-standing tutor-addressed paragraph at
`lessons/02-boundaries-and-evidence.md:59-60`.

Two consistent exclusions, applied to all four lessons:

- `## On completion, persist` is tutor bookkeeping into tutor-owned files
  (`tutorial.yaml:26` lists `tutorial/STATE.md` and `tutorial/DESIGN.md` as `tutor_owned`).
  It assigns the learner nothing.
- `## Optional deeper paths` is conditional on the learner asking and is not scored.

`## Purpose`, `## Theory`, `## Concepts to teach` and `## Constraints` are exposition and
constraint, not assigned elements, and are not scored in any lesson. **This matters for one
delta:** commit `a67de21` added a seven-line Theory paragraph to lesson 00
(`:31-36`) defining `N` and `W`. It is a definition the learner receives, not something the
learner decides or constructs, so it adds no scored element. It is scored nowhere and it
repairs reader-answered row 3 — see section 6.3.

One consistent de-duplication rule, from the branch-point row's reasoning: **a completion
condition that restates a progression step already scored in the same lesson scores
`evidence`, 0.**

**Do not set this course's total beside another course's.** Three fat lessons enumerated this
finely are not on the same ruler as a fifteen-lesson course.

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
| `ownership_policy` | `on-request` (`tutorial.yaml:43`) |

**Arithmetic**

```
lesson 00-contract-and-language    +8   (7 elements)
lesson 01-windowed-counting       +10   (10 elements)
lesson 02-boundaries-and-evidence  +8   (10 elements)
lesson concurrent-callers (opt)    +8   (8 elements)
                                  ----
sum of lessons                     34   (35 elements)

course-level penalties:
  unserved objectives        0 x -3 =  0
  unserved DESIGN.md anchors 0 x -3 =  0
  required_for gates on an
    optional lesson          0 x -3 =  0
                                  ----
COURSE TOTAL                       34
```

**Total as a learner who declines every offer earns it: 26.** The optional lesson banks 8
points such a learner never sees. The manifest and the prose agree that the lesson is optional
(section 6.8), so 34 is not the inflated figure the rubric's prose-optionality section warns
about — but **26 is the number to quote when comparing the main path against anything.**

The 34 and the 26 were each re-added from the element tables in section 2 rather than carried
from the earlier report. They sum. 8 + 10 + 8 + 8 = 34; 8 + 10 + 8 = 26.

**Two statements the skill asks for plainly:** the bundle passes the structural validator (run
above), and that is not what this report measures. And `audit.py`'s toil scanner returned
`(none found)`; that is a fact about the scanner's verb list, not about the course. The toil
inventory in section 4 is mine, from the lessons, and the scanner played no part in it.

---

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil found | **Closing action** |
|---|---|---|---|---|
| `lessons/00-contract-and-language.md` — Make the decision precise | **+8** | 3 of 3 | none | **FAIL** — `:66`, `:83-86` |
| `lessons/01-windowed-counting.md` — Count requests in deterministic windows | **+10** | 4 of 4 | none | **pass** |
| `lessons/02-boundaries-and-evidence.md` — Attack the boundaries | **+8** | 4 of 4 | none | **pass** |
| `lessons/concurrent-callers.md` *(optional)* — Make one decision atomic | **+8** | 4 of 4 | none | **pass** |

No lesson scores at or below zero, so no lesson triggers the rubric's "what is this lesson
for?" question. Full element breakdowns follow for all four anyway, because none of the four
figures is obvious from its row. The one **fail** in the closing-action column is carried into
section 6.4 with its `file:line` and the failing sentences.

### `lessons/00-contract-and-language.md` — +8

| `file:line` | Sentence scored | Element | Score |
|---|---|---|---|
| `:58` | "Ask which language the learner wants and why; adapt all later guidance to it." | teaching | +2 |
| `:59-65` | "Offer to set the project up yourself, and say what you would create before you create it: … If the learner would rather do it themselves, let them, and continue once it runs." | **not an element** — a step the tutor performs | **—** |
| `:66` | "Define the public contract in prose and then as an API signature or stub." | teaching | +2 |
| `:67` | "Add one focused test or executable example covering the budget within one window." | teaching | +2 |
| `:71` | "The project runs using the normal toolchain for the selected language." | evidence | 0 |
| `:72` | "The public API accepts a client key and exposes an allow/reject decision." | evidence | 0 |
| `:73-74` | "A test or executable example states that the first `N` requests are allowed and request `N + 1` is rejected." | evidence | 0 |
| `:75-76` | "The learner can explain which parts are contract and which remain implementation choices." | teaching | +2 |
| | | **sum** | **+8** |

Seven scored elements; `:59-65` is excluded rather than scored, and the exclusion is argued in
full in section 4. Notes on the two elements most easily scored differently:

- `:58` is **not** the rubric's branch point. The branch-point row exists so an authored fork
  is not counted twice. There are no authored language branches here: the choice is made once,
  nothing else in the course scores it, and the learner must justify it ("and why"). A wrong
  answer is instructive — a language with no meaningful concurrency model makes the optional
  lesson unreachable, per `lessons/concurrent-callers.md:16-17`. Teaching, +2.
- `:75-76` is a completion condition that restates no progression bullet and demands a new
  articulation. Teaching, +2, under the de-duplication rule.

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

Re-derived, not copied. `:55` is teaching rather than practice because the lesson's own Theory
(`:27-29`) refuses to give the formula — "the course specifies semantics rather than a
formula" — so the representation is the learner's decision. `:56` generalises that decision
into a keyed container and `:57` makes an already-written example green; both apply what `:55`
decided, which is the practice row exactly. `:63` is not a restatement of `:58` (`:58` asks for
rollover, `:63` for the *exact* boundary) but it is a test result either way, so it scores 0 on
its own merits and the de-duplication rule does not need to be reached.

This is still the highest-scoring lesson in the course: four of its five progression steps put
a construction or a decision in the learner's hands.

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

- `:53` is tutor-addressed ("Ask the learner to…") and scores +2 under the rubric's settled
  row: predict-then-run is the most instructive wrong answer in the course, because a learner
  who predicts "the limit holds across the boundary" discovers the `2N` burst by being wrong.
- `:59-60` **is** the rubric's branch point and scores 0. The teaching lives in
  `lessons/concurrent-callers.md`, scored on its own. Scoring it 0 is not a criticism: this is
  also the element that discharges the completability invariant in the material itself.
- `:66` and `:67-68` restate `:57` and score 0 under the de-duplication rule. Under a rule that
  scored every completion condition on its own merits this lesson would total +12 and be the
  course's strongest. The author should read this +8 as a consequence of the lesson saying the
  same excellent thing twice, not of the lesson being weak.

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

`:57` is teaching rather than evidence because designing a concurrency test that can actually
reveal over-admission is the lesson's fourth objective (`:24`) and a wrong answer — a test that
never really races — is the instructive failure the lesson is about. `:59` scores 0 because the
lesson attaches no requirement to it ("without requiring them"): nothing is decided,
constructed or demonstrated. `:66-67` restates nothing in the progression and demands a new
articulation (memory safety versus behavioural atomicity, `:22`), so it scores +2.

**Teaching density: 16 of 35 scored elements are `teaching`.** That is the number worth
carrying, not the total.

---

## 3. Goal gaps

**No unserved objectives and no unserved anchors. The gap penalty is 0 × −3 = 0, and
section 1's arithmetic agrees.**

Each item is judged on **what a task makes the learner do**, never on whether a `design_refs`
list cites it. All 15 lesson objectives, all 10 coverage topics and all 5 anchors were
re-enumerated against the current files; lesson 00's servers moved because that file changed.

### The 15 lesson learning objectives

| Objective (`file:line`) | Served by | Verdict |
|---|---|---|
| 00 `:20` Separate a behavioural contract from an implementation strategy | `00:66`, `00:75-76` | served |
| 00 `:21` Choose an API shape that is idiomatic in the selected language | `00:58`, `00:66`, `02:55` | served |
| 00 `:22` Establish a fast run-and-test feedback loop | `00:67`, `00:71`, `01:65` | **served — re-enumerated, 3 servers** |
| 01 `:20` Derive a stable fixed-window identifier from time | `01:55`, `01:63` | served |
| 01 `:21` Maintain independent state per client key | `01:56`, `01:64` | served |
| 01 `:22` Inject nondeterminism at a narrow boundary | `01:54` | served |
| 01 `:23` Test time-dependent behaviour deterministically | `01:58`, `01:65` | served |
| 02 `:19` Select tests that establish semantics rather than inflate coverage | `02:54` | served |
| 02 `:20` Recognise the burst characteristic at adjacent fixed-window boundaries | `02:53`, `02:57`, `02:66` | served |
| 02 `:21` Review an implementation against its stated contract | `02:55`, `02:64`, `02:53` | served, thinly — see proposal 3 |
| 02 `:22` Communicate scope and limitations precisely | `02:57`, `02:67-68` | served |
| opt `:21` Identify the read-modify-write critical section | `opt:55` | served |
| opt `:22` Choose synchronisation appropriate to the selected language | `opt:56` | served |
| opt `:23` Distinguish memory safety from behavioural atomicity | `opt:66-67` | served |
| opt `:24` Design a concurrency test that can reveal over-admission | `opt:57`, `opt:63-64` | served |

**`00:22` "Establish a fast run-and-test feedback loop" — re-enumerated, not reused.** The
2026-09-13 report found four servers: `00:51-52`, `00:54`, `00:58`, `01:65`. The first of those
no longer exists: the setup step moved to the tutor and is not an element. Enumerating the
current file:

| `file:line` | Sentence | How it serves `00:22` |
|---|---|---|
| `00:67` | "Add one focused test or executable example covering the budget within one window." | makes the loop a *test* loop rather than a run loop |
| `00:71` | "The project runs using the normal toolchain for the selected language." | requires the loop to actually run |
| `01:65` | "The relevant test suite passes without real-time waiting." | requires it to stay **fast**, which is the word the objective turns on |

**Three servers, so the objective is not stranded and no −3 falls due.** Even discounting
`01:65` as belonging to another lesson, `00:67` and `00:71` remain, so the objective is not
sole-served under any reading. This is the check the rubric's *"The objective does not
disappear with the element"* clause demands, and this course passes it. `rust-automaton-db` is
the catalogue's course where that clause bites; this one is not.

### The 10 `COURSE.md` coverage topics

| Topic | Ruling | How I decided |
|---|---|---|
| implementation-language selection | served | `00:58` is a task, the learner decides, and a justification is demanded. |
| behavioural API contracts | served | `00:66` constructs one, `00:75-76` makes the learner defend its boundary, `02:55` reviews it. |
| fixed-window rate limiting | served | `01:55`, `01:57`, `01:62` build and demonstrate the counter itself. |
| per-client state | served | `01:56` generalises state to keys; `01:64` requires independent budgets. |
| dependency injection for time | served | `01:54` builds the injection point and proves the test drives it. |
| deterministic tests | served | `01:49` forbids sleeping, `01:58` adds the clock-advancing test, `01:65` requires the suite to pass without real-time waiting. |
| boundary conditions | served | `02:53` predict, `02:54` sharpen, `02:45-46` constrain what tests must cover, `01:63` requires the exact-boundary case. |
| client isolation | served | `01:64` and `02:47` both require it, with a test. |
| algorithmic trade-offs | served — closest call in the audit | See below. |
| concurrency safety | served **only by the optional lesson** — raised as a question, not scored | `lessons/concurrent-callers.md` is the only lesson with a task. Section 6.6. |

**`algorithmic trade-offs`, and why it is not a −3.** A sceptical reading says a trade-off needs
an alternative to trade against, and every comparison with sliding logs, sliding counters and
token buckets is fenced behind "if asked" (`01:75-76`) or "discuss—but do not implement"
(`02:77-78`). On that reading the topic is unserved, a −3 falls due, and the course total is
**31 rather than 34**. I rule it served, on the same reasoning as 2026-09-13 and re-checked
against the current files: the course's own gloss of the phrase is narrower and is stated twice
— `COURSE.md:30-31` ("explain the trade-offs") and `COURSE.md:38-39` ("the learner can explain
what the algorithm does not guarantee") — and that is exercised by required tasks at `02:57` and
`02:67-68`, which make the learner name the `2N` burst and unbounded key retention as costs of
*this* algorithm. Comparative trade-offs are explicitly out of scope at `COURSE.md:59-63`. The
author may disagree; the arithmetic for the other ruling is stated so the disagreement is cheap
to settle.

### The 5 `DESIGN.md` anchors

Judged on what lessons make the learner do, not on `design_refs`.

| Anchor | Ruling | Evidence |
|---|---|---|
| `#behavioural-contract` | served | `00:66` writes the contract; `00:73-74` and `01:62` require exactly the `N`-allowed / `N+1`-rejected behaviour the anchor specifies. |
| `#window-semantics` | served | The anchor's load-bearing clause is "a request exactly at a boundary belongs to the new window"; `01:48`, `01:63` and `02:46` make the learner test precisely that. |
| `#state-model` | served | Per-key in-memory state built at `01:55-56`; the "must not scan all recorded requests" clause is exercised by `01:46` (constant-time constraint) and `01:66` (describe the average cost of one decision). |
| `#time-source` | served | `01:54` builds the replaceable source; `01:49` and `01:65` forbid waiting on wall-clock time. |
| `#concurrency-boundary` | served, with the caveat below | The anchor is half a scoping decision and half an extension. Its scoping half is honoured on the main path by `01:50` ("Keep the implementation in memory and single-process") and by the offer at `02:59-60`; its active half — actually synchronising — is done only in the optional lesson. Not a −3: main-path tasks do what the anchor says the main path does. Raised in section 6.6 alongside `concurrency safety`. |

`#concurrency-boundary` is cited only by the optional lesson's `design_refs`
(`lessons/concurrent-callers.md:4`) and is nonetheless honoured by main-path lessons that never
cite it — the exact pattern the rubric warns not to decide by grep.

**No anchor reaches project setup, layout, build files or version control.** All five are about
the limiter. This matters twice below: it is why the project-skeleton exception could not have
fired through an anchor (section 4), and it is the basis of proposal 2.

---

## 4. The toil inventory

**Confirmed toil sites: zero. −2 was applied zero times. The course total carries no toil
charge.**

The 2026-09-13 report confirmed exactly one site, at `00:51-52`. **That site no longer exists.**
`skomp/tutorail-bundles` commit `a67de21` ("rate limiter: define N and W, and let the tutor set
the project up", 2026-09-13) replaced it. What follows is the ruling on the replacement, which
is the judgement this bundle turns on.

### Ruling: the setup step at `00:59-65` is not an element

The current bullet, quoted in full from `lessons/00-contract-and-language.md:59-65`:

> - Offer to set the project up yourself, and say what you would create before you
>   create it: the smallest conventional runnable project for that language, its test
>   target, and version control if the learner wants it. Wait for the learner to accept;
>   create nothing under their files until they have. On acceptance, create that skeleton
>   yourself and show it to them — the skeleton only, never any part of the limiter, which
>   stays theirs to write. If the learner would rather do it themselves, let them, and
>   continue once it runs.

The rubric's section *A step the tutor performs is not an element* governs this directly:
**score it as nothing — not toil, and not evidence at 0.** There is no act to score. Both guards
are met, and each is checked against a `file:line` rather than assumed:

**Guard 1 — the learner must not still do it.** After the tutor finishes, the lesson requires
nothing of the learner about the skeleton. The bullet says "create that skeleton yourself and
show it to them"; *being shown* is not a task. No later element asks the learner to review,
repair or fill in the skeleton: the next two progression bullets (`:66`, `:67`) are about the
contract and a test, and the four completion conditions (`:71-76`) are about the project
running, the API shape, one test assertion and one explanation — none of which is skeleton work
handed back. `00:71` "The project runs using the normal toolchain for the selected language" is
an evidence step about the whole project, and it reads identically whichever branch was taken.

**Guard 2 — the hand-over is declared in the bundle.** In the lesson text, at `:59-65`, quoted
above. And in `ownership_policy`, at `tutorial.yaml:43`: `on-request`, changed from
`tutor-must-not-edit-learner-owned` by the same commit. A reviewer can point at both. The
runner's own format document treats this bundle as the worked example of exactly this pattern —
`skills/tutorail/references/bundle-format.md:278-293` in `skomp/tutorAIl` names
`portable-fixed-window-rate-limiter`, cites `COURSE.md`'s promise that the learner "writes every
implementation", and quotes this lesson's limiting clause ("the skeleton only, never any part of
the limiter, which stays theirs to write") as the thing that holds the two together. The
declaration is not assumed from the tutor's good nature; it is the documented case.

**The tiebreak is not reached.** *A project skeleton is toil* decides between two disagreeing
toil tests. It applies to a step the course **assigns to the learner**. This course no longer
assigns one, so the step stops being an element rather than stopping being toil — which is the
route the rubric itself names for this bundle, and the route the author took.

**The sole-server test still runs, and passes.** Removing the element does not remove the
objective. `00:22` is re-enumerated in section 3 above: three servers remain, so nothing is
stranded and no −3 falls due.

**This is not the rubric's residual hole.** The hole the rubric leaves open is an author writing
a sole-served objective around a step that teaches nothing, so as to claim the *exception*. This
course claims no exception: it removed the step from the learner entirely, and its setup
objective still has three other servers. Nothing here needed the exception to survive.

### Ruling: the decline branch at `00:64-65` is not a second element

> "If the learner would rather do it themselves, let them, and continue once it runs."

**I follow the precedent set by this report's 2026-09-13 predecessor, one section over.** That
report ruled, of `initialise version control if the learner wants it` inside the very same
bullet: *"it is conditional on the learner asking and is not a second element"*
(`docs/audits/2026-09-13/portable-fixed-window-rate-limiter.md:468`). The decline branch has the
same shape — one clause, inside one bullet, conditional on the learner electing it — and is
ruled the same way.

**I depart from nothing, but the precedent is not a perfect fit and the difference should be on
the record.** The version-control clause was an *addition* conditional on the learner asking.
The decline branch is a *substitution*: it puts back on the learner precisely the work the
hand-over removed. So the question is fair — does a course get the hand-over's benefit while a
declining learner still does the toil?

Three reasons it does, and none of them is the precedent alone:

1. **The rubric's guard is about what the lesson requires, not about what a learner may
   choose.** Guard 1 reads "the learner must not still do it", and its worked example is a
   lesson that *"has the tutor generate the project and then requires the learner to review it,
   repair it, or fill it in"*. Nothing here requires the learner to do the setup. The lesson
   offers to remove the work; the learner may keep it.
2. **The rubric already rules this shape elsewhere.** Its open-choice section handles the
   learner who picks a language outside the declared set: *"not toil, and not a gap in the
   course either"*. That is the same structure — the learner's own election takes the work
   back — and it is explicitly not charged.
3. **Charging it would score the mechanism instead of the outcome.** The toil row exists to move
   mechanical work off the learner. This course moved it, and made the offer mandatory and
   explicit ("Wait for the learner to accept; create nothing under their files until they
   have"). Charging −2 because a learner may refuse help would score the course for the
   learner's decision.

**Where the author could reasonably disagree, and what it would cost.** If the decline branch
were scored as a second element it would be toil, −2, and lesson 00 would fall from +8 to +6,
the course from 34 to 32 and the main path from 26 to 24 — coincidentally the 2026-09-13
figures. If the author wants that branch scored separately, the change that would force it is
making it its own progression bullet; as written it is one bullet and one hand-over. The
arithmetic for the other ruling is stated here so the disagreement is cheap to settle.

### Candidates examined and rejected, so the next reader need not re-litigate

`audit.py` produced **no** toil candidates. As the skill and the script both say, that is
evidence about the scanner's fixed verb list, not about the course. Everything below is mine,
from opening all four lessons and reading all 35 elements listed in section 2.

| `file:line` | Sentence | Why it is not toil |
|---|---|---|
| `00:59-65` | the setup offer, quoted above | **Not an element at all** — a step the tutor performs, both guards met. Not a rejection on the shippability test; a rejection because there is no learner act to score. |
| `00:64-65` | "If the learner would rather do it themselves, let them, and continue once it runs." | Not a second element — precedent followed, reasoning above. |
| `00:67`, `01:58`, `02:54` | "Add one focused test…", "Add a test that advances into a new window…", "Add or sharpen the smallest set of tests…" | The learner chooses the assertions and, at `02:54`, which tests are worth having at all. Not deterministic, not unambiguous, and a mistake is instructive. |
| `01:57` | "Make the existing budget example pass." | The implementation being made to pass is the learner's own and does not exist yet. Practice, +1. |
| `02:56` | "Run the complete test suite and a small demonstration." | The evidence step the format is built around, not a result the bundle could have shipped. Scored 0. |
| `opt:58` | "Confirm exactly `N` successes, then rerun the sequential suite." | Same: reading a result. Scored 0. |
| `00:78-81`, `01:68-71`, `02:70-73`, `opt:69-72` | the four `## On completion, persist` blocks | Addressed to the tutor and writing into `tutor_owned` files (`tutorial.yaml:26`). They assign the learner nothing, so there is no learner task to call toil. |

**Rejected because the bundle could not have supplied the result: none, and that is itself the
finding.** The 2026-09-13 report's `supplies:` discussion is now moot for the skeleton. The
route this bundle took is the third one — hand the work to the tutor — which the rubric says
is available precisely because the language choice is *genuinely open* (`00:50` "Let the learner
choose any general-purpose implementation language"), so no `supplies:` entry of any shape could
ship a skeleton for a language the bundle has never heard of. **There is therefore no
`supplies.py` command to propose for this bundle**, and proposal 5 of the 2026-09-13 report is
withdrawn as superseded rather than as wrong.

`audit.py` still reports **0 `supplies:` entries**, and that is now correct rather than an
omission. The bundle contains no source file — only `COURSE.md`, `DESIGN.md`,
`STATE.template.md`, `tutorial.yaml` and four lessons — and every artifact the course produces
is the learner's own code, which no `supplies:` entry could or should pre-empt.

---

## 5. Proposals

Every proposal is a concrete action the author may accept or refuse. None of them rejects the
bundle and none of them changes a score by itself.

### Proposal 1 — give lesson 02's retention limitation an anchor that answers it

Carried unchanged from 2026-09-13; it was not addressed by `a67de21` and the evidence still
stands (section 6.1). `lessons/02-boundaries-and-evidence.md:4` cites `state-model` as the
anchor behind the inactive-key retention limitation the lesson raises at `:32-33`, constrains at
`:49` and requires the learner to articulate at `:67-68`. `DESIGN.md:18-22` says nothing about
retention, growth or cleanup.

**Action:** add an anchor to `DESIGN.md` and cite it from that lesson, along these lines —

```markdown
## Retention limits {#retention-limits}

State for a client key persists after that key stops sending requests. This course does
not implement eviction, expiry or a bounded cache. That is a deliberate scope decision:
a correct eviction policy needs a production traffic model this course does not have.
The learner must be able to name the limitation, not solve it.
```

— then add `retention-limits` to `lessons/02-boundaries-and-evidence.md:4`. The work goes
through the `tutorail-authoring` skill and its toolkit, not through this one.

### Proposal 2 — record the setup hand-over in `DESIGN.md`, and align lesson 00's framing text

New this run, and it follows directly from the hand-over. The hand-over is now the most
consequential design decision in lesson 00, and three places still describe the old arrangement
in which the learner establishes the project:

| `file:line` | Text | Problem |
|---|---|---|
| `lessons/00-contract-and-language.md:10-11` | "Choose the implementation language, **establish its smallest conventional project**, and turn "rate limit a client" into an observable contract…" | The `## Purpose` still assigns the establishment to the lesson's reader. A tutor reading the Purpose alone would assign it. |
| `lessons/00-contract-and-language.md:46` | "language-idiomatic project and test structure" under `## Concepts to teach` | Half of this concept — the project half — is now demonstrated by the tutor rather than practised by the learner. Not wrong (the tutor shows the skeleton), but the list no longer says which half is which. |
| `COURSE.md:27-28` | "**Contract and language** — establish a runnable project and make the observable decision precise." | The learner-facing main-path summary does not mention that the tutor offers to do the first half. |

None of these breaks guard 2 — the hand-over is declared where the rubric requires it, in the
lesson's own progression and in `ownership_policy` — so **none of them changes any score**. They
are a consistency repair.

**Action, two parts.** (a) Reword `00:10-11` and `COURSE.md:27-28` so the establishment is
described as offered rather than assigned. (b) Add a `DESIGN.md` anchor recording the decision
and cite it from `lessons/00-contract-and-language.md:4`, which currently cites only
`behavioural-contract`:

```markdown
## Project setup {#project-setup}

The implementation language is the learner's open choice, so no project skeleton can ship
with this course. The tutor offers to create the smallest conventional runnable project for
the chosen language and waits for the learner to accept. The tutor creates the skeleton
only, never any part of the limiter. A learner who prefers to set the project up
themselves does so, and the course continues once it runs.
```

This is the one anchor the bundle now lacks: section 3 records that all five existing anchors
are about the limiter and none reaches project setup. It would also give the tutor the decision
in the document the runner loads for it.

### Proposal 3 — sharpen `02:55` so it serves its objective fully

Carried from 2026-09-13, unchanged and still standing. `lessons/02-boundaries-and-evidence.md:21`
promises "Review an implementation against its stated contract"; `:55` delivers "Review names and
public API clarity in the selected language", which reviews the API surface rather than the
implementation. The objective survives as served (`:64` requires the whole contract suite to
pass, `:53` makes the learner predict behaviour against the contract), so it is not a −3 — it is
weak enough to be worth one clause.

**Action:** extend `:55` to name the implementation, for example "Review names and public API
clarity in the selected language, and check the implementation against each clause of the stated
contract."

### Proposal 4 — drop or land "evidence-based completion"

Carried from 2026-09-13, unchanged. `lessons/02-boundaries-and-evidence.md:41` lists
"evidence-based completion" under `## Concepts to teach` and no task in that lesson or later uses
it as a concept. It is the runner's advancement mechanism (`tutorial.yaml:51`
`advance_on: validated-evidence-only`), not subject matter, and it costs a line in the one list
the tutor reads to decide what to say.

**Action:** delete the bullet, or give it a task — a sentence asking the learner to say what
evidence would convince a reviewer the limiter is correct would make it real and would serve
`02:19` at the same time.

### Proposal 5 — split `00:66`, and fence `00:83-86` out of the closing action

New this run, and it is the action behind the one **fail** in the section 2 closing-action
column. Both sites are named by the rubric itself as the properties that leave the tutor with
nothing to close on, and both are still present.

**Action, two parts.**

(a) Split `lessons/00-contract-and-language.md:66` — "Define the public contract in prose and
then as an API signature or stub." — into two bullets, so each half is one turn's closing
action:

```markdown
- Define the public contract in prose: what goes in, what comes out, what the caller may rely on.
- Turn that prose contract into an API signature or stub in the selected language.
```

(b) Add one clause to `## Optional deeper paths` at `lessons/00-contract-and-language.md:85-86`
saying the section does not close a turn — for example "…they are not needed by the main path,
and this discussion never replaces the lesson's current task." The same clause would do no harm
in the other three lessons, though only lesson 00's section invites a decision about the artifact
the learner is building in that lesson, which is why only lesson 00 fails the row (section 6.4).

### Proposal 6 — decide what to do about `concurrency safety` (author's call, not a score)

Carried from 2026-09-13. `COURSE.md:57` lists `concurrency safety` among "Topics this course must
cover" and only the optional lesson teaches it. This is deliberately a question and permanently
not a score; it costs this course nothing. The middle position, if the author wants one: name the
race on the main path (one sentence in `lessons/02-boundaries-and-evidence.md`'s Theory, and one
more limitation at `:67-68`) and keep the fix optional. Section 6.6 puts the question.

### Not proposed

No lesson deletion and no restructure. No lesson scores at or below zero, no lesson is far
outside the course's usual size, and the course has no `required_for` gate to argue about.

---

## 6. The questions only a reader can answer

None of these is scored. All of them are answered in writing.

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

**One instance found. Unchanged since 2026-09-13; `a67de21` did not touch it and `DESIGN.md` is
unmodified.**

- **`lessons/02-boundaries-and-evidence.md:4`** — `state-model`, as the citation covering the
  inactive-key retention limitation the lesson raises at `:32-33` ("State for inactive keys can
  also grow without bound"), constrains at `:49` and requires the learner to articulate at
  `:67-68`. `DESIGN.md:18-22` says nothing about retention, growth or cleanup. The anchor exists,
  the reference resolves, the validator is green, and a learner who follows it to find out why
  cleanup is not required still does not find out. **Proposal 1.**

Checked and clear: `lessons/00-contract-and-language.md:4` (`behavioural-contract` answers the
contract question the lesson raises, including the "extra information such as remaining capacity
is a learner choice" clause at `DESIGN.md:9-10` that `00:85-86` leans on);
`lessons/01-windowed-counting.md:4` (all four anchors answer questions the lesson raises, and
`#time-source` answers the "why not sleep" question directly);
`lessons/concurrent-callers.md:4` (`#concurrency-boundary` answers the lesson's own "why is this
optional" question at `DESIGN.md:30-34`).

**One new near-instance, raised and not filed as this row.** Lesson 00 now raises a question its
`design_refs` cannot answer — *who creates the project, and where does the tutor stop?* — but it
raises it without citing any anchor for it, because no anchor covers setup. This row is about a
citation that fails to answer; here there is no citation to fail. It is proposal 2 instead.

Worth noting in the other direction, which the rubric says is fine and not a finding:
`lessons/02-boundaries-and-evidence.md` honours `#concurrency-boundary` at `:59-60` by making the
offer, without citing it.

### 6.2 A lesson that introduces a type or concept nothing later uses

**One minor instance found, unchanged from 2026-09-13.**

- **`lessons/02-boundaries-and-evidence.md:41`** — "evidence-based completion" is listed as a
  concept to teach and no task in that lesson or anywhere later uses it as a concept. It is the
  runner's advancement mechanism, not subject matter. **Proposal 4.**

**One new borderline, examined and not filed.** `lessons/00-contract-and-language.md:46`
"language-idiomatic project and test structure" now has its project half demonstrated by the
tutor rather than practised by the learner. It is not a dangling concept — the lesson requires the
tutor to "show it to them" (`:63`), the test half is used by `00:67`, `00:71` demands the project
run, and `02:55` reviews idiom in the selected language — so it does not fail this row. It is a
framing inconsistency, and it is part (b) of proposal 2.

Everything else traces forward, re-checked against the current files. `00:44` "the symbols `N`
(request limit) and `W` (window duration)" is used by `00:52`, `00:73-74`, `01:28`, `01:62`,
`02:66` and `opt:50`, `opt:57`, `opt:58`, `opt:63-64` — the new concept is the opposite of
dangling and is the most-used symbol pair in the course. `00:45` "public API versus internal
representation" is used by `01:55-56` and reviewed at `02:55`. `01:39` "half-open intervals and
exact boundaries" is what `02:54` and `02:64` test. `01:40` "maps or dictionaries keyed by client
identity" is required by `01:64` and `02:47`. `01:41` "injected clocks, functions, or interfaces"
runs through `01:65` and into every later test. `00:85-86`'s remaining-capacity discussion is
explicitly fenced as optional and as a learner choice, so it is not an introduced concept left
dangling. Within the optional lesson, all five of `opt:39-43` are used by its own tasks.

### 6.3 A symbol or term a lesson uses and no lesson introduces

**This row is new since 2026-09-13. Answer: no instance in either bucket.**

- **bound only in `DESIGN.md` — none found.**
- **bound nowhere — none found.**

This is the row's canonical case, and this bundle is where it came from: a learner said on
2026-09-13 that "the tutor throws in variables N and W and doesn't explain them", and at that
time `DESIGN.md:6` was the only binding of either symbol. **That is repaired, and I verified the
repair in the current lessons rather than re-quoting `tutorail-authoring#14`:**

| Symbol | First use in a lesson | Introduced to the learner at | Verdict |
|---|---|---|---|
| `N` | `lessons/00-contract-and-language.md:31` | the same sentence — `:31-33`, "`N` is the request limit: the number of requests the limiter allows for one client key in one window." | introduced at first use |
| `W` | `lessons/00-contract-and-language.md:33` | the same sentence — `:33`, "`W` is the window duration: the length of the interval that budget applies to." | introduced at first use |

Both are restated at `00:44` under `## Concepts to teach` and used in a constraint at `00:52`.
`00:34-36` additionally instructs the tutor to define them "before using `N` or `W` in a task, an
example, or a test". Every later use is downstream of lesson 00 on the main path
(`01:28` `W`; `01:62` `N`; `02:66` `2N`; `opt:50`, `opt:57`, `opt:58`, `opt:63-64` `N`), and the
ordering holds for a learner who skips nothing and for one who takes the optional lesson, since
`01:15` requires lesson 00 and `opt:16` requires lesson 01.

**`## Concepts to teach` is not itself a definition, and it is not what passes this row here.**
`00:44` alone would not pass it; `00:31-33` does, because those are defining sentences in prose
the tutor teaches from. `DESIGN.md:6` still binds both symbols and is still the contract — it is
simply no longer the only place the meaning lives, and it was never a binding the learner could
reach.

**The sort, done by hand, since no script draws this line.** `audit.py` tabulated six candidate
rows over two distinct symbols (`N`, `W`) and correctly refused to rule. I sorted the remaining
short backticked strings and the multi-word terms myself, on the rubric's boundary — a parameter
of the concept being taught against an identifier of the language the learner already chose:

- **In scope and passing:** `N`, `W`, `2N` (`02:66`; a composite of `N`, and the burst it names
  is explained at `02:26-27`), `N + 1` (`00:73-74`, `01:62`).
- **Out of scope as language identifiers the learner brought:** nothing of this kind appears —
  this bundle is language-agnostic by construction and names no language's identifiers anywhere.
- **Two multi-word terms raised as borderlines, ruled not failures, so the author can overrule
  me.** Both are standard CS vocabulary rather than course-invented parameters, and both have
  their operative content given in the same lesson before any task depends on them:
  - **"half-open intervals"**, first appearing at `lessons/01-windowed-counting.md:39` under
    `## Concepts to teach`. The term is never glossed. Its operative content — that a request at
    the exact boundary belongs to the new window — is at `01:48`, nine lines later, before the
    progression and before any task. A one-clause gloss at `:39` would close it.
  - **"read-modify-write"**, first appearing at `lessons/concurrent-callers.md:21`. Its content
    is given in that lesson's Theory at `:28-29` ("reads a client's window and count, decides,
    and sometimes writes new state"), before the progression.

Neither is filed as a failure, because the row asks whether a symbol the *course invented* was
introduced, and the course invented neither. Both are named with a `file:line` so the author can
disagree cheaply.

### 6.4 Does each lesson equip the tutor to end a turn with one concrete action?

**This row is new since 2026-09-13. Answered for every lesson in the section 2 table, and
repeated here with `file:line` and the failing sentences. Graded from the lesson FILES.** No
transcript was used; the learner quotations below come from the rubric's own record of what
produced the row, and they are evidence about the file, not the finding.

| Lesson | Condition 1 — names the first concrete action | Condition 2 — decisions kept out of the closing action | Verdict |
|---|---|---|---|
| `00-contract-and-language.md` | **fail** — `:66` | **fail** — `:83-86` | **FAIL** |
| `01-windowed-counting.md` | pass | pass | **pass** |
| `02-boundaries-and-evidence.md` | pass | pass | **pass** |
| `concurrent-callers.md` *(optional)* | pass | pass | **pass** |

**`lessons/00-contract-and-language.md` — FAIL, on both conditions, at two sites.** Both are the
sites the rubric names, both are still present, and I took the line numbers from the file rather
than from `tutorail-authoring#13`:

- **Condition 1 — a progression bullet carrying two actions.** `:66` reads:

  > "Define the public contract in prose and then as an API signature or stub."

  Two deliverables in explicit sequence ("and then"), and they are two separate turns: a prose
  contract, then a signature. The tutor must split the bullet before either half can be a next
  step, and the lesson nowhere says to split it. **Proposal 5(a).**

- **Condition 2 — an open question with no home.** `## Optional deeper paths` at `:83-86`:

  > "Discuss alternative return values such as remaining capacity or reset time only if the
  > learner asks; they are not needed by the main path."

  This is a live design decision about the artifact the learner is building **in this lesson** —
  what the limiter returns — and the section never says that it does not close a turn. Fail
  condition 2: a decision left standing where the action should be. **Proposal 5(b).**

  Note that the gating on "only if the learner asks" is not what saves or condemns it. What
  condemns it is that the question is about *this lesson's own deliverable*.

**The discriminator I used, stated so it can be checked.** The rubric's test for a two-action
bullet is its own sentence: *"The tutor must split that bullet before either half can be a next
step."* I applied that — do the two halves need to be two turns? — rather than counting verbs,
because counting verbs fails every lesson in this bundle and makes the column useless. The four
nearest misses, all examined and all ruled pass, with `file:line` so the author can overrule me:

| `file:line` | Sentence | Why it is one turn |
|---|---|---|
| `01:54` | "Introduce the replaceable time source and prove the test controls it." | The proof is the acceptance evidence for the artifact just written, not a second deliverable. |
| `02:56` | "Run the complete test suite and a small demonstration." | Two commands, one turn: both are running the project and reporting. |
| `02:57` | "Have the learner explain the boundary burst and retained-state limitation." | Two explanations, one closing discussion. |
| `opt:58` | "Confirm exactly `N` successes, then rerun the sequential suite." | The closest to `00:66` in shape, and the only near miss carrying "then". Ruled pass because both halves are reading results of runs, not separate deliverables, and `opt:57` has already produced the run. This is the one I would most expect the author to disagree with. |

**And for condition 2 in the other three lessons**, each has its own `## Optional deeper paths`
and each is fenced away from the lesson's deliverable in a way lesson 00's is not:
`01:75-76` says "Keep those comparisons conceptual rather than replacing the project algorithm";
`02:77-78` says "discuss—but do not implement" and is scoped to "where to go afterward";
`opt:76-77` fires "only when they are relevant to the chosen language and requested by the
learner". None invites a decision about the artifact under construction. Positively, each of the
three marks its decisions and sequences them: `01:27-29` marks the representation decision in
Theory and `01:55` turns it into a construction; `02:53` makes the prediction its own step before
`02:54` acts on it; `opt:55` produces a marked critical section before `opt:56` asks for the
choice. `02:59-60` is the clearest sequencing instruction in the bundle — "Before the first task,
make the authored optional lesson offer from the manifest."

**One observation below the level of a finding.** The new setup bullet at `00:59-65` *helps* this
row: "Offer to set the project up yourself… Wait for the learner to accept" is one concrete
action a tutor can close a turn on, and it did not exist on 2026-09-13. Lesson 00 fails the row
anyway, on the two sites above, which is exactly what the rubric predicted when it said both were
"still standing after that bundle's other repairs".

### 6.5 A lesson far outside the course's usual size

**None found.** The course remains unusually uniform in both measures.

| Lesson | Lines (2026-09-13 → now) | Scored elements (then → now) | Score (then → now) |
|---|---|---|---|
| `00-contract-and-language.md` | 73 → **86** | 8 → **7** | +6 → **+8** |
| `01-windowed-counting.md` | 76 → 76 | 10 → 10 | +10 → +10 |
| `02-boundaries-and-evidence.md` | 78 → 78 | 10 → 10 | +8 → +8 |
| `concurrent-callers.md` | 77 → 77 | 8 → 8 | +8 → +8 |

Lesson 00 grew 13 lines and is now the longest file with the fewest scored elements — the
arithmetic consequence of adding a definition and a hand-over, neither of which assigns the
learner anything. Nothing here is a lesson that should be two lessons, and nothing is a paragraph
that has been given its own file. **No action.**

### 6.6 A must-cover topic that only an optional lesson teaches

**One instance, and it is the rubric's canonical case. Unchanged since 2026-09-13.**

`COURSE.md:57` lists **`concurrency safety`** among "Topics this course must cover". The only
lesson with a task that teaches it is `lessons/concurrent-callers.md`, which `tutorial.yaml:17-23`
declares optional and `lessons/concurrent-callers.md:6` marks `optional: true`. The main path
actively steers away from it: `lessons/01-windowed-counting.md:50` instructs "Keep the
implementation in memory and single-process", and `DESIGN.md:30-34` makes the exclusion a design
decision rather than an oversight.

**This is deliberately a question and not a score, and it costs this course nothing.** The rubric
records that scoring this row was proposed on the first real run at a cost of −6 to one course,
and was declined permanently.

> **Is it acceptable for this course that `concurrency safety` is taught only by an optional
> lesson, given that a learner who declines every offer never meets it?**

My reading of the evidence, offered as input and not as a ruling: the case for *yes* is strong.
`DESIGN.md:30-34` gives a reason about the subject rather than about convenience —
synchronisation mechanisms and the tests worth writing for them vary strongly between runtimes,
and a portable course that mandated one would either prescribe a mutex recipe across languages
(which `lessons/concurrent-callers.md:33-35` explicitly forbids) or exclude languages whose model
does not fit. `COURSE.md:9` budgets 60–90 minutes for the main path, which the three main lessons
already fill. Against it: "must cover" is what the heading says, and a learner who finishes the
main path has a limiter they might reasonably believe is safe to share, having never been told it
is not. Proposal 6 is the middle position. **The decision is the author's.**

The same question, in its anchor form, applies to **`#concurrency-boundary`** (`DESIGN.md:30`):
its scoping half is honoured on the main path, its active half only in the optional lesson. It is
scored served (section 3) and raised here for the same answer.

### 6.7 `required_for`, `anticipates` and `repair_in` — read from the manifest directly

`audit.py` does not report these, so I opened `tutorial.yaml` and read the `optional_lessons:`
block (`:17-23`) in full. **I keyed off the presence of the `optional_lessons:` key at
`tutorial.yaml:17`, never off `optional_lesson_count`.** The block contains exactly two keys under
`lessons/concurrent-callers.md`: `offer_at` (`:19`) and `offer_because` (`:20-23`).

**No `required_for`, no `anticipates` and no `repair_in` appear anywhere in the manifest.**
Verified against the whole file, not only that block, with a positive control in the same search
(`offer_at` matched at `:19`, so the search was live and the zero is a real zero, not a silent
pattern failure). The −3 gate row fires **zero** times, and the rubric's gate warning — printed
in the rubric section above — has nothing to fire against.

### 6.8 The completability invariant

`tutorial.yaml` contains an `optional_lessons:` key (`:17`), so the invariant is live.

> **Can a learner who declines every offer still finish this course?**

**Yes.** Answered from the main-path lessons, on all three tests, and re-checked against the
changed lesson 00.

1. **Does any main-path completion condition depend on something only an optional lesson builds
   or explains?** No. `00:71-76`, `01:62-66` and `02:64-68` were read in full. Lesson 02's four
   conditions require the contract/rollover/boundary/isolation tests to pass, the project to run,
   the `2N` burst explained and two limitations named. None mentions atomicity, synchronisation,
   threads or concurrent callers. The limitations the learner must name at `02:67-68` are
   "fixed-window burstiness and inactive-key retention" — deliberately not the race.
2. **Does any main-path lesson's prose assume the learner took an offer?** No, and the course goes
   further than not assuming it: `lessons/01-windowed-counting.md:50` positively removes the
   dependency ("Keep the implementation in memory and single-process"), and
   `lessons/02-boundaries-and-evidence.md:59-60` states the invariant in the lesson itself — "A
   learner who declines it must still be able to complete this lesson and the course." That is the
   obligation from `bundle-format.md` section 13 written into the material by the author.
3. **Prose optionality versus manifest optionality.** They agree, in all four places.
   `lessons/concurrent-callers.md` carries `optional: true` in its front matter (`:6`), sits under
   `optional_lessons:` at `tutorial.yaml:18`, is listed under `## Optional lessons` at
   `COURSE.md:41-44` and is marked *(optional)* in that entry's own text. No main-path lesson
   calls itself optional anywhere in its prose. There is no disagreement to report, so the 34 in
   section 1 is not the inflated figure the rubric's prose-optionality section warns about. The 26
   a declining learner earns is reported alongside it regardless.

**A fourth test, new this run, because the course now contains a second offer.** Lesson 00's
setup hand-over at `:59-65` is an offer the learner may decline, and it is *not* an
`optional_lessons` offer, so the invariant above does not formally reach it. Asked anyway: **can a
learner who declines the setup offer still finish?** Yes — the bullet's own decline branch
("let them, and continue once it runs") keeps the lesson moving, and the completion condition
that depends on it, `00:71` "The project runs using the normal toolchain for the selected
language", reads identically whichever branch was taken. No later element distinguishes the two
branches. **No finding.**

### 6.9 Dynamic evidence

**No dry-run harness transcript was available for this bundle in this run, so no stall is cited
either way.** The absence of one is not evidence the course completes; it is an absence.

The learner quotations that produced rows 6.3 and 6.4 — "the tutor throws in variables N and W
and doesn't explain them" and "you need to steer me more to the next step. there is no call to
action in this step" — reach this report through the rubric's record of them, and are **evidence
about the lesson files, not verdicts**. The first is discharged by the repair verified in 6.3;
the second is discharged against the file in 6.4, where it produces two `file:line` findings the
author can act on. Neither is a finding about a tutor's behaviour, which an author cannot change
from this repository.

---

## Deltas from 2026-09-13, each with its cause

The baseline is `docs/audits/2026-09-13/portable-fixed-window-rate-limiter.md` (course total 32,
main path 24). Every figure below was re-derived from the current files; none was carried.

**One change to the bundle and one change to the rubric account for every delta.**

- **Bundle:** `skomp/tutorail-bundles` commit `a67de21` (2026-09-13), touching three files —
  `lessons/00-contract-and-language.md` (+16/−3), `lessons/01-windowed-counting.md` (prose only,
  3 lines rewrapped with `W` inserted, no line-number shift), and `tutorial.yaml`
  (`ownership_policy: tutor-must-not-edit-learner-owned` → `on-request`). No commit has touched
  this bundle since; it is at `221c164`, and `lessons/02-boundaries-and-evidence.md`,
  `lessons/concurrent-callers.md`, `COURSE.md`, `DESIGN.md` and `STATE.template.md` are
  byte-identical to the versions the baseline audited.
- **Rubric:** gained the section *A step the tutor performs is not an element* (with its two
  guards and its "the objective does not disappear with the element" clause), and gained the two
  reader-answered rows on closing actions and undefined symbols, taking that list from four to
  six.

| # | Delta | Cause |
|---|---|---|
| 1 | **Course total 32 → 34** (+2) | **Bundle and rubric together.** The element at old `00:51-52` scored toil, −2; the bullet that replaced it is not an element at all. Neither change alone produces this: without the bundle change the old text is still toil, and without the rubric's new section there is no rule under which the new text scores nothing. |
| 2 | **Main-path total 24 → 26** (+2) | Same. The optional lesson is unchanged at +8, so both totals move by the same 2. |
| 3 | **Lesson 00 +6 → +8** | Same. The whole delta is in this lesson; the other three are unchanged. |
| 4 | **Lesson 00 element count 8 → 7** | Bundle changed. One element became no element. |
| 5 | **Course element count 36 → 35** | Bundle changed. Consequence of #4. |
| 6 | **Confirmed toil sites 1 → 0** | Bundle changed. `a67de21` moved the step to the tutor, which is the outcome the toil row exists to demand. |
| 7 | **Every `file:line` in lesson 00 below `:31` unchanged; every one above it shifted** | Bundle changed. Progression and completion lines moved +8 and then +13: `00:50 → :58`, `00:51-52 → :59-65`, `00:53 → :66`, `00:54 → :67`, `00:58 → :71`, `00:59 → :72`, `00:60-61 → :73-74`, `00:62-63 → :75-76`, and the old `## Optional deeper paths` at `:70-73` is now `:83-86`. |
| 8 | **Objective `00:22` servers 4 → 3** | Bundle changed. `00:51-52` was one of the four and is gone. Re-enumerated in section 3 rather than reused, exactly as the brief required. Still not sole-served, so no −3, and the course pays nothing for the hand-over. |
| 9 | **Lesson 00 line count 73 → 86; longest file, fewest elements** | Bundle changed. |
| 10 | **`supplies:` proposal withdrawn** | Bundle changed. The baseline's proposal 5 asked for one skeleton per supported language; this course keeps a genuinely open language choice, so no `supplies:` entry is possible and the tutor route is the answer. Superseded, not wrong. |
| 11 | **Reader-answered rows 4 → 6; two new answers (6.3, 6.4)** | Rubric changed. 6.3 answers clean, because `a67de21` repaired the `N`/`W` case that produced the row. 6.4 answers **fail for lesson 00** at `:66` and `:83-86`, pass for the other three. |
| 12 | **A closing-action column now appears in the section 2 table** | Rubric changed (the skill's report template now requires it for every lesson, no blanks). |
| 13 | **Rows 6.1, 6.2, 6.6, 6.7, 6.8 answer identically to 2026-09-13** | Nothing changed. The files behind them are byte-identical. The two open findings — `02:4` and `02:41` — are carried forward unrepaired. |

**No delta is caused by the earlier report being wrong.** I re-added all four lesson sums from
the current files and re-derived every element, and the baseline's figures for lessons 01, 02 and
`concurrent-callers` (+10, +8, +8) are correct; its lesson 00 figure of +6 was correct for the
file as it then stood. Its element classifications, its objective and anchor rulings, and its two
open reader-answered findings all survive re-examination. The one thing it claimed that is now
untrue — that this course carries a confirmed toil site at `00:51-52` — was true when it was
written and was overtaken by a commit made the same day.

**Where a sceptic could move the number, with the arithmetic stated so the argument is cheap:**

| Alternative ruling | Effect | Where it is argued |
|---|---|---|
| The decline branch at `00:64-65` is a second element, and it is toil | 34 → 32, main path 26 → 24 | Section 4 |
| `algorithmic trade-offs` is unserved | 34 → 31 | Section 3 |
| Both | 34 → 29 | — |

---

## Closing note on what this report is

The validator passes this bundle, and that is not an argument about anything above.

What the lessons show is a small course with an unusually high proportion of learner decisions —
**16 of 35 scored elements are `teaching`** — that honours all five of its design anchors, serves
all 15 of its lesson objectives, and now carries **no toil at all**, having moved its one
mechanical step to the tutor in the way the rubric's newest section describes. Its remaining weak
points are four, all small and all carrying a `file:line`: a citation that does not answer its
lesson's question (`02:4`), a concept no task uses (`02:41`), one objective promised more broadly
than its task delivers (`02:21`), one must-cover topic parked behind an optional offer
(`COURSE.md:57`), and the one lesson that does not leave the tutor a single action to close a turn
on (`00:66`, `00:83-86`).

Every finding above is a proposal the author may refuse, and every one carries a `file:line` and a
quoted sentence so it can be checked rather than believed. Nothing here rejects the bundle, and
`validate_bundle.py` was not modified by this audit.
