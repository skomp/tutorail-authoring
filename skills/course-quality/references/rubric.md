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

##### The table is dated, and two of its bundles have already moved

Within hours of the ruling, `skomp/tutorail-bundles` acted on it. Commit `a67de21` gave
`portable-fixed-window-rate-limiter`'s setup step to the tutor and declared
`ownership_policy: on-request`; commit `c80d8e3` did the same for `portable-bytebeat-wav`.

So in both bundles the skeleton step is **no longer an element at all** — see *A step the
tutor performs is not an element* below — and the `00:51-52` server named in the table's
rate-limiter row no longer exists. Their audit reports of 2026-09-13 are dated audits of the
state before those commits, and are superseded rather than wrong.

**Read this table as the worked reasoning, not as a current description of the catalogue.**
Every `file:line` in it was correct on 2026-09-13 and several have since moved. Take line
numbers from the bundle, never from this table or from an issue.

That the ruling changed two bundles the same day is the row working: the toil charge existed
to move mechanical work off the learner, and it did.

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

This row governs a course with a **closed** set of tracks. `portable-bytebeat-wav` names
five, so it can ship five skeletons and shed the charge that way.

A course with a **genuinely open** choice cannot, and the format is not the reason. The set
is unbounded, so no `supplies` key of any shape helps: a bundle cannot ship a skeleton for a
language it has never heard of. The author ruled on 2026-09-13 that
`portable-fixed-window-rate-limiter` keeps its open choice and the **tutor** creates the
project instead. That route is scored by the next section, not by this one — the step stops
being an element rather than stopping being toil.

#### A step the tutor performs is not an element

The open-choice row above has two cases: the course declares options and supplies a set for
each (not toil), or a learner picks outside the declared set (not toil, the learner's
setup). There is a third, and it is the one that matters most.

**A course can hand the setup to the TUTOR rather than to a supplied file.** The tutor
creates the project after the learner answers, in a language the bundle never heard of and
could not have shipped.

Score it as nothing. **It is not an element at all** — not toil, and not evidence at 0.

The toil row charges a course for work it **assigns to the learner** that the bundle could
have handed over. Evidence at 0 is still something the learner does: run a validator, read
the output, report what happened. A step the learner never performs is neither. There is no
act to score.

This is not a loophole, it is the row working. The purpose of the toil row is to get
mechanical work off the learner. A course that moves the work to the tutor has done exactly
what the charge exists to demand. Charging it anyway would score the mechanism instead of
the outcome.

##### The two guards

The charge disappears only when the work genuinely changes hands:

1. **The learner must not still do it.** If the lesson has the tutor generate the project
   and then requires the learner to review it, repair it, or fill it in, that remaining act
   IS an element and scores as whatever it is. Read what the lesson asks of the learner
   after the tutor finishes.
2. **The hand-over must be declared in the bundle**, in the lesson text and in the
   `ownership_policy` the bundle sets — not assumed from the tutor's good nature. A reviewer
   who cannot point at the declaration should score the step as assigned to the learner,
   because that is what an unmodified runner will do.

##### The objective does not disappear with the element

Removing the element does not remove the objective it served, and the sole-server test still
applies. If the tutor-performed step was **the only element serving an objective**, that
objective is now served by nothing and the course pays **−3**, exactly as it would if the
step had been supplied as a file.

That is the correct signal, not a penalty for doing the right thing: it tells the author to
rewrite the objective in the same change that moves the work. `rust-automaton-db` is the
course in the catalogue where this bites, because `00:24` has one server.

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

**This row is not the reader-answered repair row below**, and the two are easy to merge by
accident because both mention an anticipated failure. This one fires on the presence of a
`required_for` gate and costs −3 whether or not the failure is ever repaired. That one
fires with no gate anywhere in sight, asks whether a lesson repairs the failure an
`anticipates` entry declares, and scores nothing at all.

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

None of these is mechanically decidable. None is scored. **None of them, and nothing else
in this file, rejects a bundle**: a quality finding is a proposal its author may refuse, and
`validate_bundle.py` — whose findings stop a course from starting — is not where a teaching
judgement belongs. Each one is raised in the report as a question, with its `file:line`.

- **a `design_refs` entry that does not answer the question its lesson raises.** The
  anchor exists, the reference resolves, the validator is green, and the learner who
  follows it still does not find out why the code is shaped that way.
- **a lesson that introduces a type or concept nothing later uses.** It cost the learner
  attention and bought the course nothing. Either something later should use it, or it
  should go.
- **a symbol or term a lesson uses and no lesson introduces.** The mirror of the row above,
  and the more expensive of the two: the learner meets the symbol for the first time in the
  tutor's explanation, and has to guess. **The row passes when every symbol a lesson uses
  has been introduced to the learner, in a lesson, at or before its first use.** A binding
  that exists only in a `DESIGN.md` anchor does not pass it. Report the `file:line` of the
  first use. See below.
- **a lesson that does not equip the tutor to end a turn with one concrete action.** **The
  row passes when both conditions hold: the lesson names the first concrete action — a
  file, a command or an artifact, and not only the outcome; and the lesson separates the
  decisions from the actions, marking a design decision the learner must make and keeping
  that decision out of the closing action.** Fail either and the turn ends with a list of
  deliverables, or with an open question, in place of a next step. Grade the lesson file.
  See below.
- **a lesson far outside the course's usual size.** Both directions matter: one that is
  much larger is usually two lessons, and one that is much smaller is usually a paragraph
  of the lesson beside it.
- **an optional lesson that anticipates a failure mode no lesson repairs.** `anticipates`
  names a failure the course expects a learner to hit; the repair is what turns that
  expectation into teaching, and without one the learner is left standing in the failure
  the author saw coming. Check 19 proves the opposite direction only — that every
  `failure_modes` entry is named by some optional lesson's `anticipates`, or it is dead
  weight — and no check anywhere asks whether a repair exists. Judge it the way the anchor
  row is judged, by what a lesson makes the learner **do**: a `repair_in` naming a lesson
  whose prose never touches the failure fails this row, and a course carrying no
  `repair_in` at all passes it when some lesson repairs the failure anyway. Report the
  failure-mode id and the `file:line` of the `anticipates` entry in `tutorial.yaml`.
  **This is not the −3 `required_for` row above.** That row fires on a gate, costs the
  course 3 points, and fires whether or not a repair exists; this row needs no gate, asks
  only whether the anticipated failure is ever repaired, and scores nothing.
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

### A symbol bound only in `DESIGN.md` has not been introduced

The runner loads a `DESIGN.md` anchor **for the tutor, and not for the learner**. An anchor
that binds a symbol has therefore told the person explaining and never the person learning.
That is the whole row. A reader who asks *"is this symbol defined somewhere in the bundle?"*
passes every case the row exists to catch; the question is **"does a LESSON introduce it, at
or before its first use?"**

Report each instance as one of two kinds, and never merge them, because they ask the author
for different repairs:

- **bound only in `DESIGN.md`** — the meaning exists and sits in the document the learner
  never reads. The repair moves or restates it in the lesson that first uses the symbol.
- **bound nowhere** — the course has not decided what the symbol means. The repair is a
  decision, not a move.

Give the `file:line` of the **first use**, not of the definition that is missing: the first
use is the line the author edits, and the missing definition has no line.

#### What counts as a symbol: the author's ruling of 2026-09-13

Sorting the candidates is the part no script does, and this row must not imply otherwise. A
script can collect every short backticked string in a lesson, and a lesson is full of them:
`bool`, `New` and `go` are not symbols under this row.

The boundary the author ruled on:

> A symbol such as `N` or `W` is a **parameter of the concept being taught** — part of what
> a fixed-window rate limiter IS. An identifier such as `bool`, `New` or `go` belongs to the
> **language the learner already chose**, and the course did not invent it.

The course owes the learner the first kind and owes nothing for the second. A learner who
picked Go brought `go` with them. Nobody brings `N`.

**The reader sorts on that boundary, candidate by candidate, and no rule of shape does it
for them.** "A single uppercase letter" is close enough to be tempting and wrong in both
directions: it admits `T` for a type parameter the language supplies, and it misses a course
whose parameters are spelled `limit` and `window`.

A future `DESIGN.md` convention that marks a conceptual parameter apart from a type would
make the sort mechanical. That is a **bundle-format question, owned by `skomp/tutorAIl`**,
and it is not settled here. Until it is, the sort is the reader's and the report says so.

#### The case that produced this row, and was then repaired

`portable-fixed-window-rate-limiter` is where a learner met this, on 2026-09-13: "the tutor
throws in variables N and W and doesn't explain them". `DESIGN.md:6` was the only binding of
either symbol, three lessons used `N`, and no lesson used `W` at all.

**That bundle is repaired.** `tutorail-bundles` commit `a67de21` defines both symbols in the
`## Theory` of `lessons/00-contract-and-language.md:31-36`, lists them under
`## Concepts to teach` at `:44`, and tells the tutor to define them before either symbol
appears in a task, an example or a test. `DESIGN.md:6` is unchanged and is still the
contract; it is no longer the only place the meaning lives.

Cite it as the case that produced this row, never as a current finding.
`tutorail-authoring#14` still carries the pre-repair evidence in its body, because an issue
records the state at filing and this one was filed before the repair. **Re-read the lessons;
do not re-quote the issue.**

### The closing-action row grades the lesson FILE, never the tutor's turns

A learner stopped `portable-fixed-window-rate-limiter/lessons/00-contract-and-language.md`
on 2026-09-13 with these words: "you need to steer me more to the next step. there is no
call to action in this step." Asked afterwards, they named one defect: **the turn never ends
with one plain imperative sentence.**

The row is not asking the tutor for something new. The runner's own turn loop already
requires it: step 6 of the per-turn sequence in the tutorAIl runner's
`skills/tutorail/SKILL.md` is "give exactly one actionable task". **This row asks whether
the lesson file makes that possible.** A lesson that hands the tutor a bundle of
deliverables and an open design question has left the runner's rule unsatisfiable from the
material, and the learner is the one who finds out.

The temptation is to grade that turn. **Do not.** An author can change a lesson file and
cannot change a tutor's behaviour from this repository, so a row that grades live behaviour
reports a defect its reader cannot fix — and every finding in this report exists to carry a
`file:line` the author can act on. Grade the file. A transcript is evidence about the file,
the way a dry-run stall is; see **Dynamic evidence is evidence, not a verdict** below.

So look for the properties of the file that leave the tutor with nothing to close on. Two of
them, from the lesson above, and both still standing after that bundle's other repairs:

- **a progression bullet carrying two actions.** `00-contract-and-language.md:66` reads
  "Define the public contract in prose and then as an API signature or stub." The tutor
  must split that bullet before either half can be a next step, and the lesson nowhere says
  to split it.
- **an open question with no home.** `## Optional deeper paths`, at `:83-86`, invites a
  discussion of alternative return values. The tutor raised it at the end of a turn, and the
  question took the place of the action. The section never says that it does not close a
  turn.

`tutorail-authoring#13` quotes those two sites as `:53` and `:70-73`. The sentences are the
same; the file grew above them and the lines moved. **Take line numbers from the lesson, not
from the issue.**

Condition 2 is the one an auditor skips. A lesson that makes the learner choose — a
language, a representation, a return shape — is doing its job, and this row does not object
to the decision. It objects to a decision left standing **where the action should be**.
Marked as a decision, and settled before the closing action, the same lesson passes.

### Both of these rows are questions, and stay questions

Both were filed with the scored-or-asked choice left open, in `tutorail-authoring#13` and
`tutorail-authoring#14`. **The author ruled on 2026-09-13 that both are reader-answered**,
and that is recorded here so the next auditor does not re-open it.

The reason is the one the must-cover row above already gives: a scored row buys
comparability and pays for it with a mechanical judgement about teaching. Both of these are
teaching judgements end to end — one asks whether a lesson steers, the other asks whether a
definition arrived in time for a learner — and neither needs a number to do its work. What
they need is a `file:line` and an author.

There is a second cost, recorded so it is not rediscovered: five course totals were
published against this rubric on 2026-09-13, in
`docs/audits/2026-09-13-course-quality-all-bundles.md`. Any new scored row changes all five
and forces a third re-audit of the catalogue. That is not why either row is asked rather
than scored, and it is the reason to be sure before turning any future question into a
score.

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
