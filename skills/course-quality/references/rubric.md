# The course-quality rubric

Print this table with every report. A reader who can see the rubric argues with the
scoring; a reader given only a number argues with the number, or worse, believes it.

## What a score is for

A score makes a judgement **legible and comparable across a long course**. It does not
replace the judgement. Nothing in this file is computed by a script: `audit.py` gathers
evidence and refuses to rule, and every figure below comes from someone who opened the
lessons and decided.

**Comparable within one course's house style, not between courses.** A lesson's figure
tracks how finely its `## Suggested progression` enumerates clauses, so a course that
writes six terse steps and a course that writes three fat ones are not on the same scale,
and their totals must not be set side by side. This costs the rubric nothing it was for:
comparing a course against itself, lesson by lesson, is exactly what the report does. Left
unsaid, it invites a false comparison between two totals that were never measured with the
same ruler.

Two failure modes this rubric is shaped against:

- **a bare total.** It invites gaming and hides which signal fired.
- **an unexplained element.** A score with no `file:line` and no quoted sentence cannot be
  checked, so it cannot be disagreed with.

## The scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises. Course-level rather than per-lesson, but counted once PER UNSERVED OBJECTIVE — a course owing twelve topics is not the same course as one owing a single topic, and a rubric whose purpose is comparability must not score them alike |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised — see below (course-level) |

### The toil row's last clause is load-bearing

Without it the test literally catches `npm install`, and **no `supplies:` entry can create
`node_modules`.** Scoring that −2 charges a course for something its author has no way to
remove, which is a rubric punishing an author for the format's reach rather than for their
teaching.

So: **setup that needs the network, a toolchain or an account is the learner's work, and is
not toil under this rubric.** The bundle format is explicit that supplies reach only as far
as the bundle itself; this clause aligns the rubric with that contract. The question to ask
at every candidate is not "is this boring?" but **"could this bundle have shipped the
result?"** If it could and it did not, that is toil. If it could not, it is the learner's
setup and it scores as whatever it actually is.

### A project skeleton is toil — the tiebreak, ruled 2026-09-13

The two tests above disagree for one candidate, and the disagreement is not theoretical: it
changed four scores in the audit of 2026-09-13. A lesson that tells the learner to create
the smallest conventional project for their language passes **both** tests. It is a handful
of files, so the bundle could have shipped it. It also needs the toolchain, because
`go mod init`, `cargo new` and `npm init` are toolchain commands.

**When the two tests disagree, the shippability test wins. A project skeleton is toil.**

Ask the shippability question in its full form. It is not *"could the bundle have shipped
one file?"* but **"could the bundle have shipped one set of files for each language the
course supports?"** A portable bundle can. The tutor selects the set after the learner
selects the language. The toolchain is what *runs* the project; it is not what *writes*
`go.mod`, and the learner who types `go mod init` learns nothing that the next lesson uses.

`npm install` is unaffected and stays the learner's work, because `node_modules` cannot
ship under any language. The clause above still governs every candidate the two tests agree
on. This section governs only the skeleton, where they do not.

#### The exception: setup that is itself the subject

A setup step is **teaching**, not toil, when the course's own objectives make the setup the
thing being taught. A course on Forth, on a build system, on linkers or on packaging is a
course where assembling the environment *is* the material, and handing the result over
would remove the lesson rather than the chore.

The test is the objective, not the author's intent and not the difficulty of the step. But
**an objective that merely names the setup is not enough.** If it were, any author could
cancel a toil charge by writing "create the project" into the objective list, and the row
would stop meaning anything.

Use the operational test, which is the one the unserved-objective row already implies:

> **Is the setup step the ONLY element serving the objective that names it?**
>
> - **Yes** — the setup is the subject. Handing the result over would strand the objective
>   and cost −3. Score the step as what it teaches. This is the exception.
> - **No** — other elements serve that objective too, so the skeleton is a *part* of a
>   larger goal and not the goal. It is toil.

The two rows are consistent by construction: the exception fires exactly where the toil
charge and the unserved-objective charge would otherwise contradict each other. A bundle
cannot be charged −2 for assigning a step and −3 for supplying it.

#### Worked: the five bundles, 2026-09-13

An earlier draft of this section claimed every course in the catalogue treats the skeleton
as ground, and a second draft replaced it with a table of guesses. **Both were wrong.** The
table below is the third version and the first built by enumerating elements. Each row was
settled by listing every element that serves the objective, in the bundle, one report at a
time.

| Bundle | The objective that names the setup | Servers found | Ruling |
|---|---|---|---|
| `rust-automaton-db` | `00:24` "Create and run a Cargo binary project." | **1** — `00:76` alone | **exception**, not toil. Score unchanged |
| `durable-event-broker` | `00:21` "Create a small Go module and executable without speculative package structure." | 4 — `00:53` both clauses, `00:63`, `00:67` | **toil** |
| `portable-bytebeat-wav` | `00:23` "Establish an idiomatic project and test loop in the chosen language." | 4 — `00:57`, `00:60`, `00:65`, `00:67-68` | **toil** |
| `portable-fixed-window-rate-limiter` | `00:22` "Establish a fast run-and-test feedback loop." | 4 — `00:51-52`, `00:54`, `00:58`, `01:65` | **toil** |
| `webgl-typescript-scene` | none; `DESIGN.md` anchor `#platform-toolchain` describes the platform, not the act | — | **toil** on the plain test; its skeleton ships as `starter/` files, so the tiebreak never fires |

So the exception fires **once in five**, not three or four times. No `DESIGN.md` anchor in the
other four bundles names setup, toolchain or project layout.

##### The pattern worth carrying forward: a conjunctive objective is almost never sole-served

Three of the four toil rulings above share one shape. The objective is a **conjunction** —
"a project *and* a test loop", "a module *and* an executable *without* speculative
structure", "run *and* test" — and the setup step serves one conjunct while later elements
serve the others. An objective built from two halves is served by the elements that satisfy
both halves, so the setup step is a part by construction.

`rust-automaton-db` reads like a conjunction too ("create *and* run"), and it is the
exception anyway, because **no element serves the other half either**: the bundle declares
a `cargo-run` validator at `00:4` and never invokes it in a completion condition. That is
what makes `00:76` sole-served, and it is visible only by enumerating.

**Enumerate. Do not judge this from the objective's wording.** Two reviewers reading the
same four objective lists, without listing elements, got two of these four rows wrong in
opposite directions.

#### A course that lets the learner choose a language

A portable course asks the learner to pick a language, and the skeleton it could ship
depends on the answer. Score the step **against the set of languages the course declares it
supports**, not against the one a particular learner picked. The rubric scores a course, not
a run.

- The course declares a set and ships a skeleton for each member → the work is handed over
  for every learner the course claims to support. **Not toil.**
- A learner picks a language outside the declared set → the set is unbounded, the bundle
  genuinely could not have shipped that result, and the existing clause applies: it is the
  learner's setup. **Not toil**, and not a gap in the course either.

**The waiver is earned by options that are declared AND supplied.** A course that declares
no options, or declares options with no skeletons behind them, is charged exactly as
before. Otherwise the row becomes a loophole: promise every language, ship none, pay
nothing.

This holds however the format ends up expressing the choice. As of 2026-09-13 it cannot
express it at all — `supplies` entries have no selector and are placed before the learner
answers — which is why the two portable bundles in the catalogue are charged today. That
gap is `tutorail-authoring#11` item 4, and the contract for it is proposed in `tutorAIl#25`.

#### The residual hole

An author can still take the exception by writing a sole-served objective around a step
that teaches nothing — "Create and run a Cargo binary project" is close to that line, since
it asks the learner to *perform* rather than to *decide*. This rubric does not close that
hole, and no mechanical check will. A reviewer who suspects it should say so in the report
rather than adjust the number silently.

### An anchor is served by what lessons DO, not by what they CITE

The obvious mechanical proxy for the unserved-anchor row is *does some `design_refs` name
this anchor?*, and it is **wrong**. On the first course audited, `#unresolved-decisions`
appears in no lesson's `design_refs` at all and is nonetheless served, by four lessons that
do what it describes.

`design_refs` is a citation, and an anchor is a decision the course must honour. A lesson
can honour one without citing it, and — the other reader-answered row below — can cite one
without honouring it. Judge the row on what the lessons make the learner do.

A lesson's score is the sum of its own elements. The course score is the sum of the
lessons minus the course-level gap penalties — **one penalty per unserved objective or
anchor**, plus one per `required_for` gate on an optional lesson. They are counted
separately and shown separately; they are never folded into a lesson's figure.

Scoring the *fact* of having gaps once, rather than each gap, would make a course owing
twelve topics score identically to one owing a single topic. That fights the whole purpose
of the rubric, and it fights the decomposition rule below: twelve gaps folded into one −3
is exactly the hidden aggregate that rule exists to forbid.

## Two elements that are easy to score wrong

Neither needs a new row. Both were scored by elimination on the first real run, which means
two auditors would have scored them differently, so both are settled here.

- **A branch point — where the lesson offers the learner a choice of paths — scores
  `evidence`, 0.** The example is `webgl 14/LESSON.md:48`, "Choose or skip the path." It is
  a real step and it teaches nothing by itself; the teaching is in whichever branch the
  learner takes, and that branch is scored on its own. Scoring the fork as teaching would
  count the same instruction twice.
- **A tutor-addressed element scores `teaching`, +2, when the learner must decide or
  construct in response.** Lesson 11's "the tutor MUST explicitly ask" block is an
  instruction to the tutor, not to the learner, and it is load-bearing teaching all the
  same. **The fact that a sentence addresses the tutor does not change what the learner
  does.** Score the element by what it makes the learner do, at whatever grammatical person
  the author wrote it in.

## The decomposition is mandatory, not a nicety

The total is **never reported alone**. A single number invites gaming and hides which
signal fired, and a later reader will otherwise be tempted to print the total by itself.
So, in every report:

- every element carries its own score, its `file:line`, and the sentence it scored;
- a lesson's figure is the **visible sum** of its own elements, so a reader can add them
  up and get the same answer;
- course-level gaps are counted separately rather than folded in.

The top-line figure is a summary of an inventory the reader already has. **If it ever
appears without that inventory, the report is defective.**

## `required_for` scores and is raised, both

This row does two things at once, by decision of the repository owner on 2026-09-12,
after a disagreement. Doing only one of them is wrong in a different direction each way.

**It scores −3, unconditionally.** An author who writes `required_for` on an optional
lesson has declared something load-bearing and then made it skippable, and the material
usually belongs on the main path. The cost is visible in the total, the way every other
signal is.

**It is also raised, every time, as a question the author answers.** The format
deliberately permits the case where the gate is correct: a lesson that genuinely cannot
be completed while its anticipated failure stands. The runner's settled semantics are
that **the gate is on the failure** — it binds once the failure is observed, and it is
lifted by the repair, not by taking the lesson. No script can tell a justified gate from
an unjustified one.

**Print this warning beside the score, in these words or better:**

> This gate cost the course 3 points and may still be correct. If the lesson genuinely
> cannot be completed while its failure stands, the gate is doing its job — say so and
> keep it. Do not delete a gate to improve a score. A course that drops a justified gate
> lets a learner finish a lesson whose failure is still standing, which is worse than the
> toil this rubric hunts.

Without that sentence the score teaches exactly the behaviour the objection warned
about. The author **may record the gate as justified**; the score stands anyway, and the
justification stands beside it, because a rubric that let a reader argue a signal down to
zero would stop being comparable across courses.

## Rows a reader answers, and a script never scores

None of these is mechanically decidable. None is scored. Each one is raised in the report
as a question, with its `file:line`.

- **a `design_refs` entry that does not answer the question its lesson raises.** The
  anchor exists, the reference resolves, the validator is green, and the learner who
  follows it still does not find out why the code is shaped that way.
- **a lesson that introduces a type or concept nothing later uses.** It cost the learner
  attention and bought the course nothing. Either something later should use it, or it
  should go.
- **a lesson far outside the course's usual size.** Both directions matter: one that is
  much larger is usually two lessons, and one that is much smaller is usually a paragraph
  of the lesson beside it.
- **a must-cover topic that only an optional lesson teaches.** Ask it as a question, in
  these words or better: *is that acceptable for this course, given that a learner who
  declines every offer never meets it?* Some courses will answer yes with good reason.

### Why that last one is a question and not a scored row

The first real run proposed scoring it, at a cost of −6 to one course. **Declined, and it
stays declined** — this is recorded here so the next auditor does not re-open it.

The bundle format is explicit that a topic an optional lesson teaches **is in the course**,
and that it belongs in the coverage list precisely so the tutor offers the authored lesson
instead of improvising a replacement. A row penalising that would push authors toward
dropping the topic from the coverage list, which produces the outcome the format calls
worse: a tutor improvising material an author had already written. Asking the question gets
the author's judgement without prejudging it.

## The invariant no structural check can reach

> **A course carrying optional lessons must be completable by a learner who declines
> every offer.**

`bundle-format.md` section 13 states this as an authoring obligation, and it says why: no
mechanical check can reach it. An optional lesson is never on the main path, so a
validator that walks the main path sees nothing wrong, and a runner too old to know about
`optional_lessons` never offers one at all. The only way the invariant is ever checked is
that someone reads the course and asks.

So ask it, as a course-level question, every audit:

- does any **main-path** lesson's completion condition depend on something only an
  optional lesson builds or explains?
- does any main-path lesson's prose assume the learner took an offer?
- if the answer to either is yes, the material belongs on the main path. `required_for`
  is for a mistake the learner has already made, never for a prerequisite.

A course with no optional lessons answers this in one line: none declared, invariant not
at risk. **Check that claim against the lessons, not only against the manifest.**

### Prose optionality is not optionality

The sharpest thing the first real run found. In the catalogue's webgl bundle, lesson 14 is
called optional in three separate places of prose — its title, its own text, its neighbours
— and sits in `lessons:`, not in `optional_lessons:`. Everything downstream follows the
manifest: the tooling reports "0 optional", the completability machinery never engages, and
the rubric banks that lesson's 11 points into a course total of 194 when a learner who takes
the course at its word and skips it earns 183. (Both totals are the ones that first run
published; its correction note supersedes them. The 11-point gap is the point here, and it
holds whatever the totals become.)

So a course whose prose offers a lesson while its manifest requires one is **both** scored
wrongly and unchecked for the invariant above, and neither failure announces itself. When
the prose and the manifest disagree about whether a lesson is optional, say so in the
report, score the course as the manifest has it, and state what the total would be without
the lesson.

## Dynamic evidence is evidence, not a verdict

A dry-run harness that walks a course can report that a lesson **stalled**. Cite a stall
as **evidence, never as a verdict**, and say in the report which it is.

A stall cannot distinguish an unsatisfiable completion condition from a learner having a
bad day. The two look identical from outside: the lesson did not complete. One is a
defect in the course and one is a Tuesday. The ruling stays with whoever reads the lesson
and the transcript, and the report says what the harness observed, not what it concluded.

The same applies in the other direction: a course every dry run finished is not thereby a
course that teaches. It is a course nothing got stuck in.
