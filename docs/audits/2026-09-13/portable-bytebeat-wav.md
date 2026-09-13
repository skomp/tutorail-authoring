# Course quality audit: `portable-bytebeat-wav`

> ## RULED 2026-09-13 — a project skeleton is toil. This report has been re-scored.
>
> **What was asked.** `skomp/tutorail-bundles#3` reported a learner who reached this class
> of step, said *"can you create the base setup for me, there is no learning in that"*, and
> changed `ownership_policy` in their own instance so the tutor would do it. That happened
> twice, in two different courses. As first published, this report rejected the step as toil
> on the ground that **the bundle could not have supplied the result** — and the rubric
> carried two tests that disagreed on exactly this candidate:
>
> - *"could this bundle have shipped the result?"* — for a project skeleton, **yes**. It is
>   a handful of files. A portable bundle can ship one set per supported language and let
>   the tutor choose after the learner picks; this report assumed a single fixed `--from`
>   path and concluded no path existed.
> - *"setup that needs the network, a toolchain or an account is the learner's work"* —
>   **also yes**. `go mod init`, `cargo new` and `npm init` all need the toolchain.
>
> `npm install` was unambiguous under both tests, because `node_modules` cannot ship. A
> project skeleton was not, and the rubric did not say which test wins. Filed as
> `skomp/tutorail-authoring#11`.
>
> **What the author ruled, 2026-09-13.** When the two tests disagree, **the shippability
> test wins: a project skeleton is toil.** The shippability question is asked in its full
> form — *"could the bundle have shipped one set of files for each language the course
> supports?"*, not *"one file"* — and a portable bundle can, with the tutor selecting the
> set after the learner selects the language. `npm install` is unaffected and stays the
> learner's work.
>
> **The exception, and how this course falls under it.** A setup step is teaching, not toil,
> when the course's own objectives make the setup the thing being taught. An objective that
> merely names the setup is **not** enough — otherwise any author could cancel a toil charge
> by writing "create the project" into the objective list. The operational test is:
> *is the setup step the only element serving the objective that names it?* If yes, the setup
> is the subject and handing it over would strand the objective at −3; if other elements serve
> it too, the skeleton is a part of a larger goal and is toil. A draft of the rubric's worked
> table marked **this bundle borderline** and left the call to the reviewer; the table was
> rebuilt from the element list below and now rules it **toil**, with four servers. This
> report and the rubric agree.
>
> **The call, made on the element list: the exception does not apply.** Lesson 00's objective
> `:23` is a conjunction — "Establish an idiomatic **project and test loop** in the chosen
> language" — and **four** elements serve it: `:57` and `:65` (the project), `:60` and
> `:67-68` (the test loop). The lesson's own `validators: [project-runs, tests-pass]` states
> the same split. Not sole-served, so the skeleton is toil. Section 4 carries the full
> evidence, the argument for the opposite reading, and what would overturn it.
>
> **Where the ruling lives.** `skills/course-quality/references/rubric.md`, section
> *"A project skeleton is toil — the tiebreak, ruled 2026-09-13"*. That section is the
> authority; the paragraphs above summarise it.
>
> **What changed here.** `lessons/00-language-and-waveform.md:57` moves from **+2 to −2** and
> lesson 00 from **12 to 8**. Re-adding every element to verify that change also exposed an
> **unrelated addition error**: lesson 01 was published as 12 and its rows sum to 10. The
> course total moves from **54 to 48** — 50 from the ruling, and 48 once lesson 01 adds up.
> No element score was changed to reach either figure. Every figure in this report is the
> re-scored one. The question is recorded above rather than deleted so a reader can still see
> what was open and why the first published figures differed.

Audited 2026-09-13 against `tutorail-authoring:course-quality` v0.3.0 and its rubric.
Read-only: no file in `/Users/robert/src/github.com/skomp/tutorail-bundles` was created,
edited, staged or deleted. Bundle checksums taken at the start and end of the audit are
identical and `git status` is clean, so nothing changed under me.

Every finding below is a **proposal**. Applying any of them is the `tutorail-authoring`
skill's job, after the author says yes.

---

## The rubric (printed as required)

### Scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises (course-level, counted once per gap) |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised |

### Two elements settled by the rubric, not by me

- **A branch point** (the lesson offers the learner a choice of paths) scores **evidence, 0**.
  The teaching is in whichever branch is taken, and that branch is scored on its own.
- **A tutor-addressed element scores teaching, +2, when the learner must decide or construct
  in response.** Grammatical person does not change what the learner does.

### Rows a reader answers and a script never scores

- a `design_refs` entry that does not answer the question its lesson raises;
- a lesson that introduces a type or concept nothing later uses;
- a lesson far outside the course's usual size, in either direction;
- a must-cover topic that only an optional lesson teaches — **a question, permanently, not a score**.

### The invariant no structural check can reach

> A course carrying optional lessons must be completable by a learner who declines every offer.

All five are answered in writing in section 6.

### Scoring conventions I applied (so the author can argue with them)

- I scored every `## Suggested progression` bullet, every `## Completion conditions` bullet,
  and any `## Constraints` line that imposes a distinct learner action not already in the
  progression.
- A completion condition that merely **re-checks** work already scored in the progression is
  scored **0 (evidence)**, not +2 again. Scoring it twice would double-count one piece of work.
- A completion condition of the form "the learner can explain X" is scored **+2**: the learner
  constructs the explanation, a wrong one is instructive, and each such line maps to a stated
  objective.
- Where one physical line carries two clauses of different kinds ("… and listen"), I split it
  and scored the clauses separately, marked `a`/`b`.

**Totals are comparable within this course, never against another course.**

---

## 1. The course and its total

| | |
|---|---|
| Bundle id | `portable-bytebeat-wav` |
| Title | Make Music with Integer Arithmetic |
| Main-path lessons | 4 |
| Optional lessons | 1 (`lessons/stereo-bytebeat.md`) |
| Lesson rows scored | 5 |
| `supplies:` entries | 0 |
| `DESIGN.md` anchors | 7 |
| Coverage list | present, 13 topics (`COURSE.md:51-65`) |

**Arithmetic**

```
  lesson 00-language-and-waveform    8   (was 12; :57 re-scored −2 by the 2026-09-13 ruling)
  lesson 01-write-a-tone            10   (was 12; published addition error, no element changed)
  lesson 02-bytebeat-rhythm         15
  lesson 03-compose-and-export       8
  lesson stereo-bytebeat [optional] 10
  --------------------------------------
  sum of lessons                    51
  − unserved objectives (1 × −3)    −3   (03-compose-and-export objective 4)
  − unserved anchors    (0 × −3)     0
  − required_for gates  (0 × −3)     0
  --------------------------------------
  COURSE TOTAL                      48
```

**Two corrections are folded into that figure, and they are independent of each other.** The
ruling of 2026-09-13 costs lesson 00 four points (`:57`, +2 -> −2). Separately, re-adding every
element to check the ruling's effect exposed an addition error in the published lesson 01 figure:
its eleven rows sum to 10 and it was published as 12. No element score was changed to reach
either figure. Had only the ruling been applied, this report would read **50** — the figure the
open question predicted — over a table that adds to 48, which is the exact defect this re-score
exists to remove. The lesson 01 correction is set out under that lesson's breakdown in section 2,
including the one reading that would restore 12.

**Main path only** (a learner who declines the stereo offer, which is the supported outcome):
8 + 10 + 15 + 8 = 41, − 3 = **38**. Prose and manifest agree about which lesson is optional
(see section 6), so this figure is informational rather than a correction.

**No `required_for` gate exists**, so the rubric's `required_for` row does not fire and its
warning is not printed. `tutorial.yaml:18-24` carries `offer_at` and `offer_because` only —
no `required_for`, no `anticipates`, no `repair_in`. I read the manifest rather than trusting
`optional_lesson_count`, as the skill requires.

**The validator would be green and the course still has a real defect** (section 6, the
completability discussion): `output-wav` is `{ kind: file-exists, path: output.wav }`
(`tutorial.yaml:49`), which a stereo file satisfies just as well as a mono one. The conflict
is with a human completion condition, and no structural check can see it.

---

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil found |
|---|---:|---|---|
| `lessons/00-language-and-waveform.md` — Turn time into samples | **8** | 4 of 4 | **1** (`:57`, the project skeleton) |
| `lessons/01-write-a-tone.md` — Put a tone in a WAV file | **10** | 4 of 4 | none |
| `lessons/02-bytebeat-rhythm.md` — Find rhythm in the bits | **15** | 4 of 4 | none |
| `lessons/03-compose-and-export.md` — Shape a tiny composition | **8** | 3 of 4 | none |
| `lessons/stereo-bytebeat.md` *(optional)* — Compose in two channels | **10** | 4 of 4 | none |

No lesson scores at or below zero. Full element breakdowns follow for all five, because no figure
in this column is obvious from the row, and because two of them (00 at 8, 01 at 10) differ from
the figures this report carried at first publication.

### `lessons/00-language-and-waveform.md` — 8 (joint lowest)

| file:line | Sentence | Score |
|---|---|---:|
| `:49` | "Ask the learner to choose TypeScript, JavaScript, Python, Go, or Kotlin before setup." | 0 |
| `:57` | "Select the language track and create its smallest conventional runnable project." (project clause; the select clause is the branch at `:49`) | **−2** (toil) |
| `:58` | "Generate a short sequence from a deliberately simple function of `t`." | +2 |
| `:59` | "Reduce every value to 0–255 using an idiom correct for the language." | +2 |
| `:60` | "Add a small deterministic test or inspectable assertion for several known samples." | +2 |
| `:61` | "Ask the learner to predict how changing the expression changes the sequence." | +2 |
| `:65` | "The project runs with the selected toolchain." | 0 |
| `:66` | "It produces a deterministic sequence of values, all in the range 0–255." | 0 |
| `:67-68` | "At least a few known indices are checked automatically or by clear executable evidence." | 0 |
| `:69` | "The learner can explain the relationship among `t`, sample rate, and elapsed time." | +2 |

Sum: 0−2+2+2+2+2+0+0+0+2 = **8**.

Two calls worth arguing with. `:49` is the course's language fork, and the rubric settles a
branch point at 0 even though it is the element that serves the `supported-language selection`
topic — **serving a topic and scoring points are different questions**. `:57`'s project clause
was scored +2 at first publication, on the reasoning that `Establish an idiomatic project and
test loop in the chosen language` is a stated objective (`:23`) and the learner picks the
layout and test runner. **The ruling of 2026-09-13 overrides that: a project skeleton is
toil, −2**, because the bundle could have shipped one set of files per supported track and
let the tutor choose after the learner picks. The exception was tested against this lesson's
objectives and does not apply — see section 4.

**Objective `:23` is still served, and the −3 unserved-objective row does not fire.** It has
four servers — `:57`, `:60`, `:65` and `:67-68` — and that plurality is exactly what decides
the toil call against the exception; section 4 sets the test out in full. Scoring `:57` as
toil does not unserve anything: the learner still performs it, and three other elements would
still serve `:23` if the bundle supplied it instead (proposal 7). Serving and scoring are
independent, as `:49` already shows in the opposite direction.

### `lessons/01-write-a-tone.md` — 10 (corrected from 12; see the note under the table)

| file:line | Sentence | Score |
|---|---|---:|
| `:58` | "Generate a square wave with a predictable period." | +2 |
| `:59` | "Sketch the three required WAV regions before encoding fields." | +2 |
| `:60` | "Write the header and then the sample bytes." | +2 |
| `:61` | "Inspect the file size and, where available, use an installed file-inspection tool." | 0 |
| `:62` | "Play the completed file with an existing player chosen by the learner." | 0 |
| `:63` | "Add a focused check for header fields or total size appropriate to the language." | +2 |
| `:67` | "`output.wav` exists and its size agrees with header plus sample data." | 0 |
| `:68` | "A standard player or inspection tool recognises it as mono 8-bit PCM at 8,000 Hz." | 0 |
| `:69` | "Playback produces the expected steady tone rather than silence or malformed noise." | 0 |
| `:70` | "Relevant tests pass." | 0 |
| `:71` | "The learner can explain how period determines the tone's frequency." | +2 |

Sum: 2+2+2+0+0+2+0+0+0+0+2 = **10**. `:59` is the best-constructed element in the course — the
learner builds a model of the container before writing a byte, and a wrong sketch fails visibly
at `:68`.

> **Correction, found while re-adding the elements for the 2026-09-13 re-score.** This lesson
> was published as **12**. Its eleven rows sum to **10**: five elements at +2 and six at 0.
> **No element score has been changed** — the published figure was an addition error, and it
> propagated into the course total. Section 6.3 corroborates the row count rather than the
> figure: it states eleven scored elements for this lesson, which is exactly the table above,
> so no twelfth element was scored and then dropped.
>
> The only reading that restores 12 is scoring the constraint at `:52` ("Derive RIFF and data
> sizes from the generated duration") as a distinct element at +2. The scoring conventions do
> admit constraints, and lesson 00 scores one (`:49`). I did not add it, because `:60` and
> `:67` already impose that derivation and because inventing a twelfth element to make a
> published total come out is the defect this correction exists to remove. **If the author
> rules `:52` a distinct element, this lesson returns to 12, the course total rises by 2, and
> section 6.3's element count for this lesson becomes twelve.** That is the author's call, not
> the auditor's.

### `lessons/02-bytebeat-rhythm.md` — 15 (highest)

| file:line | Sentence | Score |
|---|---|---:|
| `:58a` | "Begin with a minimal expression based on `t` …" | +1 |
| `:58b` | "… and listen to its ramp-like result." | 0 |
| `:59` | "Multiply `t` and compare the perceived pitch." | +2 |
| `:60` | "Introduce one right-shifted term and listen for slower structure." | +2 |
| `:61` | "Combine one additional masked or bitwise term." | +2 |
| `:62` | "Add tests for selected `t` values to keep the expression portable and deterministic." | +2 |
| `:63` | "Ask the learner to explain which subexpression contributes pitch or rhythm." | +2 |
| `:67` | "`output.wav` contains the Bytebeat-generated samples and remains structurally valid." | 0 |
| `:68` | "The expression uses at least one shift and one intentional bitwise combination." | 0 |
| `:69` | "Selected sample values are checked deterministically." | 0 |
| `:70` | "The learner can connect at least two parts of the expression to audible behaviour." | +2 |
| `:71` | "The learner can explain why only the low eight bits are written." | +2 |

Sum: 1+0+2+2+2+2+2+0+0+0+2+2 = **15**. `:58a` is practice, not teaching: writing `t` applies
the writer already built in lesson 01 and makes no new decision. The high figure is earned —
`:59`-`:61` are a controlled one-variable-at-a-time experiment loop, and `:62` forces the
learner to compute expected sample values by hand across whichever language they chose.

### `lessons/03-compose-and-export.md` — 8 (joint lowest, with lesson 00)

| file:line | Sentence | Score |
|---|---|---:|
| `:54` | "Decide what should change over the duration and derive a coarse time value." | +2 |
| `:55` | "Add one intentional section change or evolving control term." | +2 |
| `:56` | "Regenerate and listen from beginning to end." | 0 |
| `:57` | "Run tests and inspect the final WAV metadata and duration." | 0 |
| `:58` | "Ask the learner to explain the composition in terms of `t` and its subexpressions." | +2 |
| `:59` | "Before the first required task, make the authored stereo offer from the manifest." | 0 (branch point) |
| `:60-63` | "After the main-path completion conditions are met, offer a generated live-playback side lesson. …" | 0 (branch point) |
| `:67` | "`output.wav` is a valid mono 8-bit PCM WAV at 8,000 Hz with the intended duration." | 0 |
| `:68` | "It contains at least two recognisable sections or one deliberate evolving structure." | 0 |
| `:69` | "All deterministic sample and format tests pass." | 0 |
| `:70-71` | "The learner can explain how coarse time changes the output and identify which parts of the result are subjective musical choices." | +2 |
| `:72` | "The core project remains usable without third-party audio playback dependencies." | 0 |

Sum: **8**. This is not a bad lesson — it is a lesson carrying **two branch points and six
evidence conditions**, which is what a closing lesson does. Twelve elements, the same count as
lesson 02, but only four of them ask the learner to construct anything. It does not score at or
below zero, so the rubric does not require a what-is-this-for question; the shape is worth the
author's attention anyway (proposal 2).

### `lessons/stereo-bytebeat.md` *(optional)* — 10

| file:line | Sentence | Score |
|---|---|---:|
| `:54` | "Separate “sample at `t`” from “frame at `t`” in the design." | +2 |
| `:55` | "Derive left and right values for a few known frames." | +2 |
| `:56` | "Interleave them and update the header calculations." | +2 |
| `:57` | "Inspect metadata, file size, and initial data bytes." | 0 |
| `:58a` | "Listen on stereo-capable output …" | 0 |
| `:58b` | "… and refine one controlled channel difference." | +2 |
| `:62` | "`output.wav` is recognised as two-channel 8-bit PCM at 8,000 Hz." | 0 |
| `:63` | "Header sizes, byte rate, block alignment, and data length agree." | 0 |
| `:64` | "Tests establish left-right interleaving for known frames." | 0 |
| `:65` | "Playback presents an intentional audible difference between the channels." | 0 |
| `:66` | "The learner can explain the distinction between sample rate and bytes per second." | +2 |

Sum: **10**.

---

## 3. Goal gaps

Every per-lesson learning objective (20 across 5 lessons), every `COURSE.md` coverage topic
(13) and every `DESIGN.md` anchor (7) was checked against **what the lessons make the learner
do**, never against `design_refs` citations and never against `topic_candidates` word overlap.

**One gap, −3.**

- **`lessons/03-compose-and-export.md:23` — "Distinguish the authored course from
  environment-specific extensions" — −3.**
  How I decided: I looked for an element where the learner does something that depends on the
  distinction and where getting it wrong is visible. There is none. `:60-63` is the tutor
  narrating the boundary to the learner ("Explain that it is outside the 60–90 minute
  estimate"); `:59` and `:60` are branch points the rubric scores 0, and accepting or declining
  an offer is not exercising the distinction; `:72` ("The core project remains usable without
  third-party audio playback dependencies") is a property of the project that holds whether or
  not the learner understands why. The other three objectives of this lesson are each exercised
  by `:54`/`:55`, `:55`/`:68` and `:57`/`:69`. The author may reasonably argue this one back —
  the argument would be that `:70-71`'s "identify which parts of the result are subjective"
  carries it, which I rejected because that sentence is about musical subjectivity, not about
  the authored/generated boundary.

**Checked and ruled served — the close calls, with reasoning:**

- **`#generated-live-playback-extension` (`DESIGN.md:34-42`) — served**, despite the gap above,
  and the two rulings are not in conflict. The anchor asks the *course* to bound the extension;
  `lessons/03:49` ("Do not require live audio libraries or device APIs"), `:60-63` and `:72` do
  exactly what it describes. The objective asks the *learner* to distinguish, and nothing makes
  them. Different tests, different answers. (One clause of the anchor is not carried into any
  lesson — see section 6 and proposal 3.)
- **`#stereo-layout` (`DESIGN.md:44-48`) — served, but only by the optional lesson**
  (`lessons/stereo-bytebeat.md:54-56`, `:63-64`). Tasks do exercise it, so no −3. That it is
  reachable only by accepting an offer is raised as the rubric's permanently-unscored question
  in section 6.
- **`little-endian binary encoding` (`COURSE.md:58`) — served**, by `lessons/01:60` ("Write the
  header and then the sample bytes") plus `:68` (a player recognising the file is only possible
  if the byte order is right). It is served *implicitly*: no element names endianness as a thing
  to check, and `:63`'s focused check is on "header fields or total size". Served, thinly —
  proposal 6.
- **`integer overflow and masking` (`COURSE.md:60`) — served**, on the masking half without
  argument (`lessons/00:59`, `lessons/02:61`) and on the overflow half by `lessons/02:71` ("The
  learner can explain why only the low eight bits are written"), which is the wraparound idea
  stated as an explanation the learner must produce. Worth naming that machine-word overflow —
  the reason `t*t` behaves differently in Python and Go — appears only as tutor-facing theory at
  `lessons/00:34-36` and is never something the learner is made to observe. Compound topic, one
  half strong, so not a −3.
- **`supported-language selection` (`COURSE.md:53`) — served** by `lessons/00:49`+`:57`, even
  though `:49` scores 0 and `:57` now scores −2. Serving and scoring are independent: an element
  charged as toil is still an element the learner performs.
- The remaining eight coverage topics (`discrete audio samples`, `sample rate`,
  `unsigned 8-bit PCM`, `WAV containers`, `Bytebeat expressions`, `bitwise shifts`,
  `audible pitch and rhythm`, `deterministic generation`, `basic artifact validation`) are each
  served by named progression or completion elements in lessons 00–03 and needed no judgement call.
- The other five anchors — `#supported-tracks`, `#sample-model`, `#wav-contract`,
  `#expression-boundary`, `#composition-scope` — are each served by lessons doing what they
  describe (`lessons/00:49`/`:57`; `lessons/00:59` + `lessons/01:51`; `lessons/01:52`/`:59-60`;
  `lessons/02:50-51` + `:71`; `lessons/03:46-47` + `:70-71`).
- All 16 objectives in lessons 00, 01, 02 and stereo are served; the breakdowns above carry the
  element for each.

**The portable-bundle trap, checked: no coverage topic is taught by only one language track.**
Every topic is stated in language-neutral terms and every element that could have been
track-specific is hedged to the chosen track — `lessons/00:59` "using an idiom correct for the
language", `lessons/01:22` "the selected language's standard library", `lessons/01:63` "appropriate
to the language", `lessons/02:62` "to keep the expression portable". All five tracks have a
standard-library little-endian binary writer, so `COURSE.md:58` is reachable from each. The two
environment-dependent steps (`lessons/01:61` file-inspection tool, `:62` a player) vary by
operating system, not by language, and both are hedged ("where available", "chosen by the
learner"). Nothing found.

**Gaps listed: 1. Subtracted: −3. This agrees with section 1.**

---

## 4. The toil inventory

**Confirmed toil sites: one — `lessons/00-language-and-waveform.md:57`, the project skeleton,
−2.** This section was published with an empty inventory; the ruling of 2026-09-13 moved one
candidate out of the rejected list and into it.

The scanner reported 0 candidates. **The scanner is a candidate generator over a fixed verb
list, and its silence is evidence about the verb list, not about the course.** This inventory
comes from opening all five lessons and reading every progression bullet, constraint and
completion condition — 56 scored elements — against the rubric's toil test.

One structural fact still shapes the inventory: **this bundle ships no files at all.**
`supplies:` is empty, the bundle contains nothing but `COURSE.md`, `DESIGN.md`,
`tutorial.yaml`, `STATE.template.md` and five lesson files. What the ruling changes is the
reading of that fact. An empty `supplies:` is not evidence that nothing was shippable; here it
means the one shippable result — the project skeleton, in five language variants — was assigned
to the learner instead of handed over. The other deterministic, unambiguous piece of work in
the course, laying out the RIFF header bytes, is the thing the course exists to teach and stays
out of the inventory on the first half of the test.

**The confirmed site:**

- `lessons/00-language-and-waveform.md:57` — "Select the language track and create its smallest
  conventional runnable project." **Toil, −2.** The bundle supports five tracks
  (`DESIGN.md` `#supported-tracks`), so it could have shipped five skeletons and let the tutor
  select one after the learner picks the language. The first publication of this report
  rejected the site on the ground that a runnable project needs a toolchain; the ruling holds
  that the toolchain is what *runs* the project, not what writes `go.mod`, and that where the
  two tests disagree the shippability test wins. Note that this report had scored the act +2
  where the rate-limiter report scored the same act +1 (`skomp/tutorail-bundles#3`); both are
  now −2. The remedy is proposal 7.

  **The exception was tested and does not apply. This was the judgement call in this report,
  so here is the whole evidence.** A draft of the rubric's worked table marked this bundle
  **borderline** and handed the decision to the reviewer, noting that *"idiomatic … in the
  chosen language"* leans toward the exception. The table was afterwards rebuilt from the
  element list below and now rules this bundle **toil** outright. The operational test is not
  whether an objective names the setup — it does — but:

  > Is the setup step the **only** element serving the objective that names it?

  The objective is lesson 00's fourth, `:23` **"Establish an idiomatic project and test loop
  in the chosen language."** It is a conjunction: a project **and** a test loop. Every element
  in the lesson that serves it:

  | Element | Sentence | Half of `:23` it serves |
  |---|---|---|
  | `:57` | "Select the language track and create its smallest conventional runnable project." | the project |
  | `:60` | "Add a small deterministic test or inspectable assertion for several known samples." | the test loop |
  | `:65` | "The project runs with the selected toolchain." | the project |
  | `:67-68` | "At least a few known indices are checked automatically or by clear executable evidence." | the test loop |

  **Four elements, not one. The answer to the operational test is *no*, so the skeleton is a
  part of a larger goal and not the goal: toil, −2.** The lesson's own front matter states the
  same split independently — `validators: [project-runs, tests-pass]` (`:5`) is one validator
  per half of the objective, and `tests-pass` is discharged by `:60` and `:67-68`, not by
  `:57`. Handing the skeleton over therefore strands nothing: `:23` keeps three of its four
  servers, so the −3 unserved-objective row does not fire against the remedy, and the rubric's
  consistency condition ("a bundle cannot be charged −2 for assigning a step and −3 for
  supplying it") is satisfied. (The "project" half would still be thinned — see proposal 7.)

  **The argument for the exception, and why I rejected it.** *"Idiomatic … in the chosen
  language"* does ask the learner to know what is conventional for their track, which sounds
  like a decision rather than a chore. But the same phrase recurs at `:59` ("using an idiom
  correct for the language"), an element that is not setup at all — so idiomatic-for-the-track
  is a property this whole lesson carries, not the subject `:57` uniquely teaches. Compare the
  two ends of the rubric's table: `rust-automaton-db`'s "Create and run a Cargo binary project"
  is a single act with a single server, and takes the exception; the rate-limiter's "Establish
  a fast run-and-test feedback loop" has four servers, and is toil. This
  objective is built like the second — an *Establish … and …* conjunction whose second half is
  exercised elsewhere — and it is scored like the second.

  **What would overturn this.** A reader who judges `:65` and `:67-68` to be evidence *about*
  the objective rather than servers *of* it would be left with `:57` and `:60`, which is still
  two, so the ruling is stable unless the test-loop half is also read out of `:23`. If the
  author intends `:23` to mean the project alone, the objective is sole-served, the exception
  fires, `:57` returns to +2 and the course to 52. Saying so here rather than adjusting the
  number silently, as the rubric's "residual hole" paragraph requires.

**Candidates I examined and rejected, so the next reader does not re-litigate them:**

- `lessons/01-write-a-tone.md:61` — "Inspect the file size and, where available, use an installed
  file-inspection tool." **Rejected: could not have been supplied** (the tool is in the learner's
  environment, and the clause says "where available" precisely because it may not be). Scored 0.
- `lessons/01-write-a-tone.md:62` — "Play the completed file with an existing player chosen by
  the learner." **Rejected: could not have been supplied** — an OS audio player is not shippable.
  Scored 0.
- `lessons/01-write-a-tone.md:59-60` — "Sketch the three required WAV regions before encoding
  fields." / "Write the header and then the sample bytes." **This is the one place in the bundle
  where the bundle genuinely could have shipped the result** — a WAV writer is a small file and a
  `supplies:` entry could hand it over. It is nonetheless **not toil**, because it fails the first
  half of the test decisively: the learner decides the layout, a wrong header is instructive and
  visible at `:68`, and it serves three stated objectives (`:21`, `:22`, `:23`). Handing this over
  would delete the course. Named here because "could the bundle have shipped it?" answering *yes*
  is unusual and a later reader will otherwise ask.
- `lessons/02-bytebeat-rhythm.md:62` and `lessons/00:60` — adding tests with known expected sample
  values. Looks mechanical; **rejected**, because the expected values must be derived by the learner
  from the expression and the chosen language's integer semantics, which is the objective at
  `lessons/02:22`.
- `lessons/03-compose-and-export.md:60-63` — the four environment questions before generating the
  live-playback lesson. **Rejected: this is the tutor's work, not an assignment to the learner.**

**One element in this course is charged −2: `lessons/00-language-and-waveform.md:57`. Every
other candidate above is rejected and scores what it actually is.**

---

## 5. Proposals

Each names a concrete action. All are refusable.

**Proposal 1 — fix the stereo offer's timing, which currently puts an accepting learner in
conflict with a main-path completion condition. (Highest value finding in this audit.)**

`lessons/03-compose-and-export.md:59` says "Before the first required task, make the authored
stereo offer from the manifest." `lessons/stereo-bytebeat.md:48` requires "Update every WAV field
affected by the channel count" and `:62` requires `output.wav` to be "recognised as two-channel
8-bit PCM". But `lessons/03-compose-and-export.md:67` requires "`output.wav` is a valid **mono**
8-bit PCM WAV at 8,000 Hz" and `:48` requires "Preserve mono unsigned 8-bit PCM at 8,000 Hz on the
main path". A learner who accepts the offer where the lesson tells the tutor to make it — *before*
lesson 03's required work — converts the writer to stereo and then cannot satisfy lesson 03.

Note what this defeats: `tutorial.yaml:49` declares `output-wav: { kind: file-exists, path:
output.wav }`, which a stereo file satisfies. **The validator stays green through the whole
conflict.** Two ways to fix it, both one-line:

- (a) Move the offer to after the main-path conditions are met, alongside the live-playback offer —
  change `lessons/03:59` to read, e.g., "After the main-path completion conditions are met, make
  the authored stereo offer from the manifest." `offer_at: [lessons/03-compose-and-export.md]` in
  `tutorial.yaml:20` remains correct either way.
- (b) Keep the early offer and make the stereo lesson write a different artifact: add a constraint
  to `lessons/stereo-bytebeat.md` "Write the stereo result to `output-stereo.wav` and leave the mono
  `output.wav` path intact", and adjust `:62` accordingly. This also keeps `lessons/03:50` ("Keep
  the final output at `output.wav`") true.

(a) is smaller; (b) preserves the ability to explore stereo early. The author picks.

**Proposal 2 — close the unserved objective at `lessons/03-compose-and-export.md:23`.** Either:

- (a) give it a learner-facing element — add one completion condition after `:72`, e.g. "The
  learner can state which parts of the finished project would still work on another machine with
  no audio hardware, and why live playback is not part of the authored course." That converts a
  narrated boundary into something the learner constructs, and recovers the −3; or
- (b) drop the objective from `:23` and let `COURSE.md:67-73` ("Explicit extension boundary") carry
  the idea as course framing rather than as a per-lesson objective. Also recovers the −3, and is
  the honest option if the author's intent was always that the tutor explains the boundary.

Both are acceptable outcomes. Leaving it named and unaddressed is not.

**Proposal 3 — carry the missing `DESIGN.md` clause into the lesson that must honour it.**
`DESIGN.md:41-42` requires the generated live-playback lesson to "preserve the working offline WAV
path, **state any external dependency before installation**, and count its time separately".
`lessons/03:60-63` reproduces the first and third of those and not the second. Add "state any
external dependency before installing it" to the instruction at `:62-63`, so a tutor generating the
side lesson from the lesson text alone still honours the design decision.

**Proposal 4 — decide, in writing, whether `stereo PCM` may live only in an optional lesson.**
`COURSE.md:65` lists `stereo PCM` under "Topics this course must cover", and the only lesson that
teaches it is optional. This is the rubric's permanently-unscored question, so it costs nothing;
the author's answer changes what happens next. If the topic must be met: promote the material to
the main path (or fold a two-channel section into lesson 03). If the offer is the right home for it:
say so in `COURSE.md` — e.g. mark the bullet "*(taught in the optional stereo lesson)*" — so a
learner who declines is not left thinking a must-cover topic was skipped by accident.

**Proposal 5 — align the stereo lesson's prerequisite with where it is offered.**
`lessons/stereo-bytebeat.md:16` says "Lesson `02-bytebeat-rhythm` is complete", while
`tutorial.yaml:20` offers the lesson at `lessons/03-compose-and-export.md`. Not wrong — 02 is
complete by then — but under proposal 1(a) the real prerequisite becomes lesson 03, and the prose
should say so.

**Proposal 6 — make little-endian encoding something the learner checks, not only something the
file implies.** `lessons/01:22` states it as an objective and `:63` asks for "a focused check for
header fields or total size". Extend `:63` to name the byte order, e.g. "Add a focused check that a
multi-byte header field (sample rate or byte rate) is written least-significant byte first." One
sentence, and the objective stops depending on a player's tolerance to prove it.

**Proposal 7 — hand the project skeleton over, and re-point the objective that currently rests on
it.** This proposal did not exist at first publication; it follows from the ruling of 2026-09-13
that a project skeleton is toil (see the block at the head of this report and section 4).

`lessons/00-language-and-waveform.md:57` charges the learner −2 for work the bundle can ship. The
bundle supports five tracks, so the remedy is five skeletons, not one: add a `supplies:` entry per
track holding the smallest runnable project and its test command, and let the tutor copy the set
that matches the language chosen at `:49`. The progression bullet then reads, e.g., "Select the
language track; the tutor supplies the matching project skeleton." That removes the −2 and lifts
lesson 00 from 8 to 10 — the course total from 48 to 50 — without touching any element that teaches.

**The objective this rests on survives the change — that is precisely why the step is toil.**
Objective `:23`, "Establish an idiomatic project and test loop in the chosen language", has four
servers (section 4). Supplying the skeleton removes one, `:57`, and leaves `:60`, `:65` and
`:67-68`, so **the −3 unserved-objective row does not fire** and the rubric's consistency
condition holds: this bundle is not charged −2 for assigning the step and −3 for supplying it.
Had `:57` been the sole server, the exception would have applied and this proposal would be
wrong.

Worth the author's eye anyway: after the change the *project* half of `:23` is exercised only by
`:65` ("The project runs with the selected toolchain"), which is an evidence condition. If the
author wants that half to stay learner-work, the honest edit is to narrow `:23` to "Establish a
test loop in the chosen language" — which `:60` and `:67-68` exercise directly — rather than to
keep a wider objective propped up by a validator run.

**The other result this bundle could have shipped stays where it is.** The WAV writer
(`lessons/01:59-60`) is a small file and a `supplies:` entry could hand it over — and must not.
It fails the first half of the toil test decisively and is the teaching the course exists for;
section 4 records that reasoning in full.

---

## 6. The questions only a reader can answer

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

**None found.** All 16 `design_refs` entries across the five lessons resolve to an anchor that
speaks to something the lesson actually raises:
`lessons/00:4` → `#supported-tracks` (which track, `:49`), `#sample-model` (why 0–255, `:59`),
`#expression-boundary` (what `t` maps to, `:58`);
`lessons/01:4` → `#sample-model`, `#wav-contract` (`:52`, `:59-60`);
`lessons/02:4` → `#sample-model`, `#expression-boundary` (`:50-51`), `#wav-contract` (`:52`);
`lessons/03:4` → `#wav-contract`, `#expression-boundary`, `#composition-scope` (`:46-47`),
`#generated-live-playback-extension` (`:60-63`);
`lessons/stereo-bytebeat.md:4` → all four, including `#stereo-layout` for `:54-56`.

**One partial, in the opposite direction** — worth the author's eye: `lessons/03:4` cites
`#generated-live-playback-extension`, and the anchor carries a requirement (`DESIGN.md:41-42`,
"state any external dependency before installation") that the lesson never restates. The reference
answers the lesson's question; the lesson drops one of the reference's obligations. Proposal 3.

The weakest citation is `lessons/03:4` → `#wav-contract`: lesson 03 raises no new container
question beyond "do not break what lesson 01 built" (`:48`, `:50`). Near-vacuous, not wrong.

### 6.2 A lesson that introduces a type or concept nothing later uses

**None found.** The closest candidate, examined and cleared: `lessons/01-write-a-tone.md:43`
introduces **"square waves"**, and lesson 02 immediately discards the square wave
(`lessons/02:10-11`, "Replace the regular test tone with a compact Bytebeat expression"). The
*artifact* is discarded; the *concept* is not. Period-and-frequency reasoning from `lessons/01:29`
is what makes `lessons/02:59` ("Multiply `t` and compare the perceived pitch") legible, and it
resurfaces in `lessons/stereo-bytebeat.md:66` ("explain the distinction between sample rate and
bytes per second"). That is scaffolding used later, not a dead concept.

Also checked and cleared: `lessons/00:45` "selected-language integer semantics" → used at
`lessons/02:62` (portable deterministic tests); `lessons/03:41` "subjective versus objective
completion criteria" → used in that lesson's own `:70-71`; `lessons/stereo-bytebeat.md:39-41`
"block alignment", "byte rate" → used in that lesson's own `:63` and `:66`. The last two are in
terminal lessons, so "nothing later" is structural rather than a defect.

### 6.3 A lesson far outside the course's usual size, in either direction

**None found.** The five lessons carry 10, 11, 12, 12 and 11 scored elements respectively, run
79 / 82 / 81 / 85 / 76 lines, and share an identical section structure. There is no candidate for
splitting and none for folding into a neighbour.

The outliers are **scores**, not sizes: `lessons/03-compose-and-export.md` and
`lessons/00-language-and-waveform.md` both score 8, against 10, 15 and 10. They are outliers for
different reasons, and only one is a shape worth the author's attention.

Lesson 03 reaches 8 from the same 12-element count as lesson 02. The cause is visible in its
breakdown — two branch points (`:59`, `:60-63`) and six evidence conditions, against four
constructive elements. That is a defensible shape for a closing lesson that has to land the
artifact and make two offers, and it is above zero, so the rubric does not require a
what-is-this-for question. Raised anyway, because if the author wants the composition work to
carry more weight, `:54-55` is where to add it.

Lesson 00 reaches 8 only because one element is charged −2 (`:57`, the project skeleton). Its
other nine elements sum to 10, which is an ordinary shape for an opening lesson. This outlier is
answered by proposal 7, not by a restructuring.

### 6.4 A must-cover topic that only an optional lesson teaches

**Found: one.** `COURSE.md:65` lists **`stereo PCM`** under "Topics this course must cover". The
only lesson teaching it is `lessons/stereo-bytebeat.md`, which `tutorial.yaml:18-24` makes optional.
`DESIGN.md:44-48` (`#stereo-layout`) is likewise served only there.

Asked as the rubric requires, and **not scored** — the rubric settled in the negative on scoring
this row, and that decision stands:

> Is that acceptable for this course, given that a learner who declines every offer never meets
> `stereo PCM` at all, while `COURSE.md` tells them the course must cover it?

It may well be acceptable: the format is explicit that a topic an optional lesson teaches *is* in the
course, and listing it is what makes the tutor offer the authored lesson instead of improvising. The
author's answer drives proposal 4 either way.

### 6.5 The completability invariant

> **Can a learner who declines every offer still finish this course?**

**Yes — with one timing defect that should be fixed anyway (proposal 1).**

Answered from the main-path lessons, not from the manifest:

- **Does any main-path completion condition depend on something only an optional lesson builds or
  explains?** No. Lesson 03's conditions (`:67-72`) require mono 8-bit PCM at 8,000 Hz, two sections
  or an evolving structure, passing tests, an explanation, and no third-party playback dependency.
  Every one of those is built by lessons 00–02 and 03 itself. Nothing requires frames, interleaving,
  block alignment or a second channel.
- **Does any main-path lesson's prose assume the learner took an offer?** No — and the course goes
  out of its way not to. `lessons/03:77-79` instructs the tutor to record whether the stereo and
  live-playback offers "were declined, deferred, or accepted", so declining is an explicitly
  anticipated path. `COURSE.md:10-12` puts live playback outside the time estimate, and
  `lessons/03:72` makes independence from playback dependencies a *condition*, not a caveat.
- **`required_for` gates on optional lessons:** **none.** I read `tutorial.yaml:18-24` directly
  rather than trusting `optional_lesson_count` — the block contains `offer_at` and `offer_because`
  only, with no `required_for`, no `anticipates` and no `repair_in`. The rubric's −3 row does not
  fire and its warning is therefore not printed.

**Prose optionality vs manifest optionality: they agree here.** The one lesson the manifest makes
optional (`lessons/stereo-bytebeat.md`) also declares `optional: true` in its own front matter
(`:6`), is titled and described as an extension, and is named as optional in `COURSE.md:44-45`. No
lesson sitting in `lessons:` calls itself optional in its prose. The "Optional deeper paths" sections
at the foot of all five lessons are conditional discussion topics ("If asked…"), not lessons, and the
live-playback extension is generated on request and is not a bundle lesson at all
(`DESIGN.md:34-39`) — so neither creates a prose/manifest disagreement. **The total in section 1
therefore needs no restatement**; the main-path-only figure of 38 is given there for information,
not as a correction.

**The defect the invariant question surfaced is the mirror image of the usual one.** The course is
completable by a learner who *declines*. It is the learner who *accepts*, at the moment the course
tells the tutor to offer, who is broken — see proposal 1. A validator walking the main path sees
nothing, and `output-wav`'s `file-exists` check passes on a stereo file, so this was only ever going
to be found by reading.

### 6.6 Dynamic evidence

No dry-run harness was run against this bundle for this audit, so there is no stall to cite either
way. Nothing here rests on dynamic evidence.

---

## Note on the audit brief

Two assertions in the dispatch, checked:

- Every measurement the brief pre-supplied is correct: 4 main-path lessons, 1 optional, 5 lesson
  rows, 0 toil candidates, 7 `DESIGN.md` anchors, 0 `supplies:` entries, coverage list present.
- The brief's statement that "a `required_for` gate on an optional lesson is −3 each **and** must be
  raised with the warning printed verbatim" is right about the rule and does not apply: this bundle
  declares no such gate, so neither the score nor the warning fires.
- The brief's first scratchpad path was correct and its in-brief "correction" named a directory that
  does not exist (session id `…83f435a75604`). The only session directory present is
  `…83f835a75604`, which the coordinator's later message confirmed. This report is written to
  `/private/tmp/claude-501/-Users-robert-src-github-com-skomp-tutorail-bundles/02117994-91ab-407b-b475-83f835a75604/scratchpad/audit-portable-bytebeat-wav.md`.
