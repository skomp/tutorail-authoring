# Course quality audit: `portable-bytebeat-wav`

Audited 2026-09-15 against `tutorail-authoring:course-quality` and its rubric.

Every finding below is a **proposal**. Applying any of them is the `tutorail-authoring`
skill's job, after the author says yes. Nothing in this report rejects the bundle, and
`validate_bundle.py` is unchanged.

---

## Provenance

Reproduced verbatim from the run's provenance record, which is identical for all five
bundles audited on this date:

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

**Confirmed for this bundle by running it.** The pinned validator against
`portable-bytebeat-wav` printed `yaml reader: restricted (built in, stdlib only)`, ran 19
checks and reported 9 as `n/a`, and ended `PASS - every applicable check ran and found
nothing.` with `exit=0`. The whole scripts directory was pinned because
`validate_bundle.py` imports `yamlite` and `catalogs` from beside itself; the pin holds
`validate_bundle.py`, `yamlite.py` and `catalogs.py`. A `FAIL - 0 finding(s)` would have
been the tell that the validator did not run. It did not appear.

**A green validator is not a good course.** The two questions are separate, deliberately.
The validator's own output says so at length. Every judgement below comes from the lessons.

### Read-only confirmation

`git status --porcelain` in `/Users/robert/src/github.com/skomp/tutorail-bundles` was
**empty at the start of this audit and empty at the end**. Nothing in that repository was
created, edited, staged, committed or stashed. The only file this audit wrote is the one
you are reading.

---

## The rubric (printed as required)

### The scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises. Course-level, counted once **per** unserved objective |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised |

### The rulings that decide elements, not left to me

- **A project skeleton is toil** when the two tests disagree; the shippability test wins.
  Asked in its full form: *could the bundle have shipped one set of files for each language
  the course supports?*
- **The exception**: a setup step is teaching when it is the **only** element serving the
  objective that names it. Enumerate; never judge it from the objective's wording.
- **A step the tutor performs is not an element at all** — not toil, not evidence at 0.
  Two guards: the learner must not still do it, and the hand-over must be declared in the
  lesson text **and** in `ownership_policy`.
- **The objective does not disappear with the element.** If a tutor-performed step was the
  sole server of an objective, that objective now costs −3.
- **A branch point scores evidence, 0.** The teaching is in whichever branch is taken.
- **A tutor-addressed element scores teaching, +2**, when the learner must decide or
  construct in response. Grammatical person does not change what the learner does.
- **An anchor is served by what lessons DO, not by what they CITE.**

### The six rows a reader answers, and a script never scores

1. a `design_refs` entry that does not answer the question its lesson raises;
2. a lesson that introduces a type or concept nothing later uses;
3. a symbol or term a lesson uses and no lesson introduces — the row passes when every
   symbol has been introduced **in a lesson**, at or before its first use. A binding that
   exists only in a `DESIGN.md` anchor does not pass it, because the runner loads an anchor
   for the **tutor** and not for the learner. Report the `file:line` of the **first use**,
   and keep "bound only in `DESIGN.md`" separate from "bound nowhere";
4. a lesson that does not equip the tutor to end a turn with one concrete action — passes
   when **both** hold: the lesson names the first concrete action (a file, a command or an
   artifact, not only the outcome), **and** the lesson separates decisions from actions,
   keeping a design decision out of the closing action. **Grade the lesson FILE, never the
   tutor's turns**;
5. a lesson far outside the course's usual size, in either direction;
6. a must-cover topic that only an optional lesson teaches — **a question, permanently,
   not a score**.

### The invariant no structural check can reach

> A course carrying optional lessons must be completable by a learner who declines every
> offer.

All six rows and the invariant are answered in writing in section 6.

### Scoring conventions I applied (so the author can argue with them)

These are the conventions the 2026-09-13 report set. I kept them unchanged, because
changing the ruler and the course in the same re-audit would make every delta unreadable.

- I scored every `## Suggested progression` bullet, every `## Completion conditions`
  bullet, and any `## Constraints` line imposing a distinct learner action not already in
  the progression.
- A completion condition that merely **re-checks** work already scored in the progression
  is **0 (evidence)**, not +2 again.
- A completion condition of the form "the learner can explain X" is **+2**.
- Where one physical line carries two clauses of different kinds, I split it and scored the
  clauses separately, marked `a`/`b`.

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
| `ownership_policy` | `on-request` (`tutorial.yaml:44`) |

**Arithmetic**

```
  lesson 00-language-and-waveform    12   (was 8; bundle changed at c80d8e3, see below)
  lesson 01-write-a-tone             10   (unchanged; re-added independently, confirms 10)
  lesson 02-bytebeat-rhythm          15   (unchanged)
  lesson 03-compose-and-export        8   (unchanged figure; two elements' text changed)
  lesson stereo-bytebeat [optional]  10   (unchanged)
  --------------------------------------
  sum of lessons                     55
  − unserved objectives (1 × −3)     −3   (03-compose-and-export objective 4, `:23`)
  − unserved anchors    (0 × −3)      0
  − required_for gates  (0 × −3)      0
  --------------------------------------
  COURSE TOTAL                       52
```

`12 + 10 = 22`; `+ 15 = 37`; `+ 8 = 45`; `+ 10 = 55`; `55 − 3 = 52`.

**Main path only** (a learner who declines the stereo offer, which is a supported outcome
and now a clean one): `12 + 10 + 15 + 8 = 45`, `− 3 = **42**`. Prose and manifest agree
about which lesson is optional (section 6.5), so this figure is informational rather than a
correction.

**Every element is listed in section 2, and the lesson figures there are visible sums.** I
re-added all five lessons from the files rather than inheriting any figure, including the
2026-09-13 report's own corrected ones. My lesson 01 arithmetic independently reproduces
**10**, which confirms that report's correction and confirms that its first-published **12**
was an addition error rather than a lost element.

**No `required_for` gate exists.** `tutorial.yaml:18-24` carries `offer_at` and
`offer_because` only — no `required_for`, no `anticipates`, no `repair_in`. I read the
`optional_lessons:` block in the manifest rather than trusting `optional_lesson_count`, as
the skill requires. The rubric's −3 row does not fire, and its warning is therefore not
printed.

---

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil found | Closing action |
|---|---:|---|---|---|
| `lessons/00-language-and-waveform.md` — Turn time into samples | **12** | 4 of 4 | **none** (the skeleton moved to the tutor at `c80d8e3`) | **pass** |
| `lessons/01-write-a-tone.md` — Put a tone in a WAV file | **10** | 4 of 4 | none | **pass** |
| `lessons/02-bytebeat-rhythm.md` — Find rhythm in the bits | **15** | 4 of 4 | none | **pass** |
| `lessons/03-compose-and-export.md` — Shape a tiny composition | **8** | 3 of 4 | none | **fail** — `:54` |
| `lessons/stereo-bytebeat.md` *(optional)* — Compose in two channels | **10** | 4 of 4 | none | **pass** |

No lesson scores at or below zero. Full element breakdowns follow for all five, because no
figure in this column is obvious from its row.

The one **fail** in the closing-action column is carried into section 6.4 with its
`file:line` and its failing sentence.

### `lessons/00-language-and-waveform.md` — 12 (was 8)

| file:line | Sentence | Score |
|---|---|---:|
| `:49` | "Ask the learner to choose TypeScript, JavaScript, Python, Go, or Kotlin before setup." | 0 (branch point) |
| `:57-58` | "Have the learner select the language track; it fixes project layout, run and test commands, and integer semantics for the rest of the course." | **+2** (teaching — see the ruling below) |
| `:59-60` | "Offer to create the smallest conventional runnable project for that track, and create it only once the learner accepts. If they would rather set it up themselves, let them." | **0** (the creation is **not an element**; the accept/decline is a branch point — see below) |
| `:61` | "Generate a short sequence from a deliberately simple function of `t`." | +2 |
| `:62` | "Reduce every value to 0–255 using an idiom correct for the language." | +2 |
| `:63` | "Add a small deterministic test or inspectable assertion for several known samples." | +2 |
| `:64` | "Ask the learner to predict how changing the expression changes the sequence." | +2 |
| `:68` | "The project runs with the selected toolchain." | 0 |
| `:69` | "It produces a deterministic sequence of values, all in the range 0–255." | 0 |
| `:70-71` | "At least a few known indices are checked automatically or by clear executable evidence." | 0 |
| `:72` | "The learner can explain the relationship among `t`, sample rate, and elapsed time." | +2 |

Sum: `0 + 2 + 0 + 2 + 2 + 2 + 2 + 0 + 0 + 0 + 2` = **12**. Eleven elements.

#### How I scored the tutor-performed creation bullet, `:59-60`

**Not an element. It contributes nothing — not −2, and not 0 as evidence.** Both of the
rubric's guards were checked against the file rather than assumed:

- **Guard 1, the learner must not still do it.** After the tutor finishes, the lesson asks
  the learner nothing about the project. There is no review step, no repair step and no
  fill-in-the-blank. The next progression bullet, `:61`, is generation work that would exist
  whoever created the directory. The one clause that could have re-assigned the work — "If
  they would rather set it up themselves, let them" (`:60`) — is a **permission the learner
  may take**, not an assignment the course makes. The rubric scores a course, not a run, and
  this course assigns nothing here.
- **Guard 2, the hand-over is declared in the bundle.** It is declared twice: in the lesson
  text at `:59-60` ("Offer to create … and create it only once the learner accepts"), and in
  the manifest at `tutorial.yaml:44`, `ownership_policy: on-request`. Before `c80d8e3` that
  key read `tutor-must-not-edit-learner-owned`, under which an unmodified runner could not
  have performed the step at all. A reviewer can point at both declarations, which is what
  the guard demands.

The learner's remaining act — accepting or declining the offer — **is** an act, and it is a
choice of paths, so I scored it as the rubric settles a branch point: **0**. Two readings
are available here and they agree on the number, so the arithmetic does not turn on the
choice: read strictly, the creation is "not an element" and the accept/decline is a branch
point at 0; read loosely, the whole bullet is one tutor-performed non-element. Either way
`:59-60` contributes 0. I say which reading I took because the element **count** differs
between them, and section 6.5's element counts use the first.

#### How I scored the selection bullet, `:57-58` — the judgement call in this report

**+2, teaching.** This is the one figure in this audit a reader is most likely to contest,
so here is the whole argument and the counter-argument.

The 2026-09-13 report scored the language choice at **0** in total: it put the fork at
`:49` (a branch point) and folded the select clause into the old conjunctive bullet, whose
project half it charged −2. The bullet the learner meets is now different text:

> "Have the learner select the language track; it fixes project layout, run and test
> commands, and integer semantics for the rest of the course."

Against the teaching test, clause by clause:

- **the learner decides** — yes, and this is the course's one irreversible decision. It is
  taken once and every later element is written against it.
- **a wrong answer is instructive** — this is what changed. The bare fork at `:49` names
  five languages and no consequence. `:57-58` names three consequences, and the lesson makes
  all three bite later: layout and commands at `:68` ("The project runs with the selected
  toolchain"), and integer semantics at `:34-36` ("Do not assume that JavaScript numbers,
  Python integers, Go integers, and Kotlin integers overflow or shift identically") and
  again at `lessons/02:62`, where the learner must compute expected sample values by hand in
  whichever language they chose. A learner who chooses without weighing integer semantics
  finds out in lesson 02, and the lesson told them in advance that they would.
- **it serves a stated objective** — `:23`, and the coverage topic `supported-language
  selection` at `COURSE.md:53`.

**Why the branch-point carve-out does not swallow it.** The carve-out exists to stop one
instruction being counted twice: "the teaching is in whichever branch the learner takes,
**and that branch is scored on its own**." The webgl example is a fork into a lesson and
no-lesson, each scored elsewhere. Here there is no second count available. This course has
no per-track elements — every later element is written once and hedged to the chosen track
(`:62` "using an idiom correct for the language", `lessons/01:22` "the selected language's
standard library", `lessons/01:63` "appropriate to the language", `lessons/02:62` "to keep
the expression portable"). No branch is scored on its own, so scoring `:57-58` as teaching
double-counts nothing.

**The counter-argument, and what it costs.** A reader who applies the carve-out by its
first clause alone — *the lesson offers the learner a choice of paths* — scores `:57-58` at
0, exactly as the 2026-09-13 report scored the choice. Under that reading **lesson 00 is 8,
the course total is 48 and the main path is 38**, which are by coincidence the 2026-09-13
figures, reached by a completely different route. I did not take that reading, because the
carve-out's stated purpose is not met by it here, and because the bullet's second clause is
subject matter the course goes on to depend on. I record the alternative rather than adjust
the number silently.

**I also kept `:49` at 0 rather than folding it into `:57-58`.** They are different
sentences doing different work: `:49` is a constraint fixing the closed set of five tracks
and the *timing* ("before setup"); `:57-58` is the decision with its consequences. Scoring
`:49` at 0 keeps the report's treatment of it identical to 2026-09-13, so the delta on this
lesson is attributable to one element and not two.

#### The sole-server test, re-enumerated

The brief is right that this must be re-enumerated rather than carried over: the lesson has
changed, and the 2026-09-13 table's row for this bundle ("4 servers, toil") described the
pre-`c80d8e3` file.

Objective `:23` is **"Establish an idiomatic project and test loop in the chosen
language."** It is a conjunction — a project **and** a test loop. Every element in the
lesson that serves it, after the change:

| Element | Sentence | Half of `:23` it serves |
|---|---|---|
| `:57-58` | "Have the learner select the language track; it fixes project layout, run and test commands, and integer semantics…" | both, by determining them |
| `:63` | "Add a small deterministic test or inspectable assertion for several known samples." | the test loop |
| `:68` | "The project runs with the selected toolchain." | the project |
| `:70-71` | "At least a few known indices are checked automatically or by clear executable evidence." | the test loop |

The old fourth server — the skeleton creation — is gone from this list, because it is no
longer an element. **Three servers remain even if a reader declines to count `:57-58`.**

Two consequences, and they are the ones that matter:

- **The −3 unserved-objective row does not fire.** The rubric is explicit that removing an
  element does not remove the objective, and that a sole-served objective now costs −3. This
  objective was never sole-served: it had four servers and it has three or four still. The
  lesson's own front matter states the same split independently — `validators: [project-runs,
  tests-pass]` at `:5` is one validator per half.
- **The toil exception is moot, not declined.** In 2026-09-13 the exception had to be tested
  and rejected, because there was a setup element to score. There is no setup element now, so
  there is nothing for the exception to except. The bundle is charged −2 for nothing and −3
  for nothing, which is exactly the consistency condition the rubric builds the two rows to
  satisfy.

**The residual-hole note the rubric asks for.** Worth the author's eye: after the change,
the *project* half of `:23` is exercised by `:68` alone, which is an evidence condition, plus
whatever weight `:57-58` carries. The 2026-09-13 report raised this under its proposal 7 and
it survives the different repair the author chose. The honest edit, if the author wants that
half to stay learner-work, is to narrow `:23` to the test loop rather than keep a wider
objective propped up by a validator run. This is a proposal (section 5), not a charge.

### `lessons/01-write-a-tone.md` — 10 (file unchanged since 2026-09-13)

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

Sum: `2 + 2 + 2 + 0 + 0 + 2 + 0 + 0 + 0 + 0 + 2` = **10**. Eleven elements, five at +2 and
six at 0.

**I re-added this lesson from the file without reference to either published figure, and
got 10.** That independently confirms the 2026-09-13 correction and its account of the
cause: eleven elements, no twelfth element lost, the first-published **12** was an addition
error. I also re-examined the one reading that would restore 12 — scoring the constraint at
`:52` ("Derive RIFF and data sizes from the generated duration") as a distinct element — and
**reached the same conclusion**: `:60` and `:67` already impose that derivation, so `:52` is
a restatement of scored work, not a distinct learner action. Adding an element to make a
published total come out is the defect the correction existed to remove. If the author rules
`:52` distinct, this lesson returns to 12 and the course to 54; that is the author's call.

`:59` remains the best-constructed element in the course: the learner builds a model of the
container before writing a byte, and a wrong sketch fails visibly at `:68`.

### `lessons/02-bytebeat-rhythm.md` — 15 (file unchanged; highest)

| file:line | Sentence | Score |
|---|---|---:|
| `:58a` | "Begin with a minimal expression based on `t` …" | +1 (practice) |
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

Sum: `1 + 0 + 2 + 2 + 2 + 2 + 2 + 0 + 0 + 0 + 2 + 2` = **15**. Twelve elements. `:58a` is
practice, not teaching: writing `t` applies the writer built in lesson 01 and makes no new
decision. The high figure is earned — `:59`–`:61` are a controlled one-variable-at-a-time
experiment loop, and `:62` forces the learner to compute expected sample values by hand
across whichever language they chose.

### `lessons/03-compose-and-export.md` — 8 (two elements rewritten at `2ce5345`; figure unchanged)

| file:line | Sentence | Score |
|---|---|---:|
| `:54` | "Decide what should change over the duration and derive a coarse time value." | +2 |
| `:55` | "Add one intentional section change or evolving control term." | +2 |
| `:56` | "Regenerate and listen from beginning to end." | 0 |
| `:57` | "Run tests and inspect the final WAV metadata and duration." | 0 |
| `:58` | "Ask the learner to explain the composition in terms of `t` and its subexpressions." | +2 |
| `:59-61` | "After the main-path completion conditions are met, make the authored stereo offer from the manifest. The mono course is finished by then, so a later two-channel `output.wav` does not disturb this lesson's completion conditions." | 0 (branch point) |
| `:62-65` | "After the main-path completion conditions are met, also offer a generated live-playback side lesson. …" | 0 (branch point) |
| `:69` | "`output.wav` is a valid mono 8-bit PCM WAV at 8,000 Hz with the intended duration." | 0 |
| `:70` | "It contains at least two recognisable sections or one deliberate evolving structure." | 0 |
| `:71` | "All deterministic sample and format tests pass." | 0 |
| `:72-73` | "The learner can explain how coarse time changes the output and identify which parts of the result are subjective musical choices." | +2 |
| `:74` | "The core project remains usable without third-party audio playback dependencies." | 0 |

Sum: `2 + 2 + 0 + 0 + 2 + 0 + 0 + 0 + 0 + 0 + 2 + 0` = **8**. Twelve elements.

The figure is unchanged from 2026-09-13 and so is its cause: two branch points and six
evidence conditions against four constructive elements, which is what a closing lesson does.
The `2ce5345` repair rewrote `:59` into `:59-61` and moved the live-playback bullet down, but
both were branch points at 0 before and after, so the repair is worth 0 points and is worth a
great deal anyway — see section 6.5.

### `lessons/stereo-bytebeat.md` *(optional)* — 10 (`:16` rewritten at `2ce5345`; not a scored element)

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

Sum: `2 + 2 + 2 + 0 + 0 + 2 + 0 + 0 + 0 + 0 + 2` = **10**. Eleven elements. The lesson's
`## Prerequisites` at `:16` changed from lesson 02 to lesson 03; `## Prerequisites` is not a
scored element, so the figure is unaffected. The change matters for section 6.5.

---

## 2b. Every delta from 2026-09-13, and its cause

The baseline is `docs/audits/2026-09-13/portable-bytebeat-wav.md` (total **48**, main path
**38**). That report carries a corrected arithmetic error in its own text, which I did not
inherit: I re-added every lesson from the files.

### Scored deltas

| Item | 2026-09-13 | 2026-09-15 | Cause |
|---|---:|---:|---|
| lesson 00 | 8 | **12** | **bundle changed and rubric changed**, two effects, +2 each — see below |
| lesson 01 | 10 | 10 | **no delta.** Re-added independently; my sum reproduces the baseline's corrected 10 |
| lesson 02 | 15 | 15 | no delta; file unchanged |
| lesson 03 | 8 | 8 | no delta in the figure; two elements' text and line numbers changed at `2ce5345`, both branch points at 0 before and after |
| lesson stereo | 10 | 10 | no delta in the figure; `:16` changed at `2ce5345`, and `## Prerequisites` is not scored |
| unserved objectives | 1 (−3) | 1 (−3) | no delta; `lessons/03:23` is still unserved |
| unserved anchors | 0 | 0 | no delta; all 7 served |
| `required_for` gates | 0 | 0 | no delta; the manifest declares none |
| **COURSE TOTAL** | **48** | **52** | **+4**, entirely from lesson 00 |
| **main path** | **38** | **42** | **+4**, the same +4 |

### Lesson 00's +4, decomposed

The baseline's lesson 00 table and mine are the same eleven-element shape with one element
replaced by two. The +4 is two independent +2s:

| | 2026-09-13 | 2026-09-15 | Cause |
|---|---|---|---|
| the language selection | folded into `:57`, counted 0 (the fork was scored at `:49`) | `:57-58`, **+2** | **bundle changed** — `c80d8e3` split the conjunction and gave the selection bullet its consequences. My ruling on the new text; the counter-argument is printed above |
| the project creation | `:57` project clause, **−2** (toil) | `:59-60`, **0** — not an element | **bundle changed** (`c80d8e3` moved it to the tutor and set `ownership_policy: on-request`) **and rubric changed** ("A step the tutor performs is not an element"). Both were needed: the rubric rule alone would not fire without the declaration, and the declaration alone would have been scored as assigned work |
| everything else in the lesson | 8 points across nine elements | 8 points across nine elements | unchanged, only renumbered (`c80d8e3` added three lines above them) |

`8 − (−2) + 2 = 12`. Every 2026-09-13 line number in lesson 00 from `:57` down has moved by
+3 or +4; I took all line numbers from the file.

### Deltas that are not scores

- **`tutorail-bundles#5` is fixed** — the baseline's proposal 1, its self-described highest
  value finding. Verified in section 6.5, not assumed.
- **The baseline's proposal 5 is fixed** — the stereo lesson's prerequisite now names lesson
  03. Same commit.
- **The baseline's proposal 7 is resolved by a different repair than it proposed.** It asked
  for five `supplies:` skeletons, one per track, and predicted lesson 00 at 10 and the course
  at 50. The author instead moved the work to the tutor, which the rubric blesses explicitly
  and which needs no shipped files. The outcome is 12 and 52 rather than 10 and 50, and the
  whole of that 2-point difference is my +2 on the selection bullet, which the proposal did
  not anticipate because the proposal did not rewrite the bullet. `supplies:` is still empty,
  and under the repair the author chose it is correctly empty.
- **The baseline's proposals 2, 3, 4 and 6 are all still open** and are carried forward
  unchanged in section 5.
- **The old report is not wrong anywhere I could find**, beyond the lesson 01 arithmetic it
  had already corrected in its own text. Its rulings were correct descriptions of the file as
  it stood on 2026-09-13; two commits have moved the file since.

---

## 3. Goal gaps

Every per-lesson learning objective (20 across 5 lessons), every `COURSE.md` coverage topic
(13) and every `DESIGN.md` anchor (7) was checked against **what the lessons make the learner
do**, never against `design_refs` citations and never against `topic_candidates` word
overlap.

**One gap, −3.**

- **`lessons/03-compose-and-export.md:23` — "Distinguish the authored course from
  environment-specific extensions" — −3.**
  How I decided: I looked for an element where the learner does something that depends on the
  distinction and where getting it wrong is visible. There is none, and the `2ce5345` repair
  did not add one. `:62-65` is the tutor narrating the boundary to the learner ("Explain that
  it is outside the 60–90 minute estimate"); `:59-61` and `:62-65` are branch points the
  rubric scores 0, and accepting or declining an offer is not exercising the distinction;
  `:74` ("The core project remains usable without third-party audio playback dependencies") is
  a property of the project that holds whether or not the learner understands why. The new
  sentence at `:60-61` ("The mono course is finished by then…") is addressed to the tutor about
  course structure and asks the learner nothing. The lesson's other three objectives are each
  exercised, by `:54`/`:55`, `:55`/`:70` and `:57`/`:71`. The author may reasonably argue this
  one back; the argument would be that `:72-73`'s "identify which parts of the result are
  subjective" carries it, which I reject for the same reason the baseline did — that sentence
  is about musical subjectivity, not about the authored/generated boundary.

**Checked and ruled served — the close calls, with reasoning:**

- **`#supported-tracks` (`DESIGN.md:3-7`) — served, and more directly than in 2026-09-13.**
  The anchor says the selected track "determines project layout, binary I/O APIs, integer
  conversion details, and test commands, but not the audio semantics". Lesson 00's new
  `:57-58` now says nearly the same thing to the learner, and `:49` fixes the closed set.
  Served by lessons doing what the anchor describes.
- **`#generated-live-playback-extension` (`DESIGN.md:34-42`) — served**, despite the gap
  above, and the two rulings do not conflict. The anchor asks the *course* to bound the
  extension; `lessons/03:49` ("Do not require live audio libraries or device APIs"), `:62-65`
  and `:74` do exactly that. The objective asks the *learner* to distinguish, and nothing makes
  them. Different tests, different answers. One clause of the anchor is still not carried into
  any lesson — section 6.1 and proposal 3.
- **`#stereo-layout` (`DESIGN.md:44-48`) — served, but only by the optional lesson**
  (`lessons/stereo-bytebeat.md:54-56`, `:63-64`). Tasks do exercise it, so no −3. That it is
  reachable only by accepting an offer is section 6.6's permanently-unscored question, and the
  `2ce5345` repair sharpens it: the offer now comes strictly after the main path ends.
- **`little-endian binary encoding` (`COURSE.md:58`) — served**, by `lessons/01:60` plus `:68`
  (a player recognising the file is only possible if the byte order is right). Served
  *implicitly*: no element names endianness as a thing to check, and `:63`'s focused check is
  on "header fields or total size". Served, thinly — proposal 6.
- **`integer overflow and masking` (`COURSE.md:60`) — served**, on the masking half without
  argument (`lessons/00:62`, `lessons/02:61`) and on the overflow half by `lessons/02:71` ("The
  learner can explain why only the low eight bits are written"). Worth naming that machine-word
  overflow — the reason `t*t` behaves differently in Python and Go — appears only as
  tutor-facing theory at `lessons/00:34-36` and is never something the learner is made to
  observe. Compound topic, one half strong, so not a −3.
- **`supported-language selection` (`COURSE.md:53`) — served** by `lessons/00:49` + `:57-58`.
  Note that serving and scoring remain independent in both directions here: `:49` serves the
  topic and scores 0.
- The remaining coverage topics — `discrete audio samples`, `sample rate`, `unsigned 8-bit
  PCM`, `WAV containers`, `Bytebeat expressions`, `bitwise shifts`, `audible pitch and
  rhythm`, `deterministic generation`, `basic artifact validation` — are each served by named
  progression or completion elements in lessons 00–03 and needed no judgement call.
  `stereo PCM` is served only by the optional lesson (section 6.6).
- The other four anchors — `#sample-model`, `#wav-contract`, `#expression-boundary`,
  `#composition-scope` — are each served by lessons doing what they describe (`lessons/00:62`
  + `lessons/01:51`; `lessons/01:52`, `:59-60`; `lessons/02:50-51`, `:71`; `lessons/03:46-47`,
  `:72-73`).
- All 16 objectives in lessons 00, 01, 02 and stereo are served; the breakdowns above carry
  the element for each.

**The portable-bundle trap, re-checked: no coverage topic is taught by only one language
track.** Every topic is stated in language-neutral terms and every element that could have
been track-specific is hedged to the chosen track — `lessons/00:62`, `lessons/01:22`,
`lessons/01:63`, `lessons/02:62`. All five tracks have a standard-library little-endian binary
writer, so `COURSE.md:58` is reachable from each. The two environment-dependent steps
(`lessons/01:61`, `:62`) vary by operating system, not by language, and both are hedged.
Nothing found. The `c80d8e3` repair does not change this: the tutor creating the skeleton
covers all five tracks and any sixth, since the tutor is not limited to what the bundle ships.

**Gaps listed: 1. Subtracted: −3. This agrees with section 1.**

---

## 4. The toil inventory

**Confirmed toil sites: none.**

This is a delta from 2026-09-13, which confirmed one: `lessons/00-language-and-waveform.md:57`,
the project skeleton, −2. That site no longer exists as an element. `c80d8e3` moved the
creation to the tutor and declared the hand-over in both required places, and the rubric is
explicit that such a step is not an element at all — "not toil, and not evidence at 0". The
charge is gone because the work changed hands, which is exactly what the row exists to
demand. Section 2's lesson 00 breakdown carries the two-guard check in full.

**`audit.py` reported 0 toil candidates** (`candidates: []` in `--json`). **The scanner is a
candidate generator over a fixed verb list, and its silence is evidence about the verb list,
not about the course.** This inventory comes from opening all five lessons and reading every
progression bullet, every constraint and every completion condition — 57 scored elements —
against the rubric's toil test. An empty candidate list is not a pass, and this empty
inventory is not derived from it.

One structural fact still shapes the reading: **this bundle ships no files at all.**
`supplies:` is empty and the bundle contains only `COURSE.md`, `DESIGN.md`, `tutorial.yaml`,
`STATE.template.md` and five lesson files. On 2026-09-13 that emptiness meant one shippable
result had been assigned to the learner instead. It no longer does. The one shippable result
— the project skeleton — is now produced by the tutor, which needs no `supplies:` entry and
covers tracks the bundle never enumerated.

**Candidates I examined and rejected, so the next reader does not re-litigate them:**

- `lessons/00-language-and-waveform.md:59-60` — "Offer to create the smallest conventional
  runnable project for that track…" **Rejected: not an element.** The tutor performs it and
  both guards hold (section 2). This is the site that was −2 on 2026-09-13.
- `lessons/01-write-a-tone.md:61` — "Inspect the file size and, where available, use an
  installed file-inspection tool." **Rejected: the bundle could not have supplied the
  result** — the tool is in the learner's environment, and the clause says "where available"
  precisely because it may not be. Scored 0.
- `lessons/01-write-a-tone.md:62` — "Play the completed file with an existing player chosen by
  the learner." **Rejected: the bundle could not have supplied the result** — an operating
  system's audio player is not shippable under any language. Scored 0.
- `lessons/01-write-a-tone.md:59-60` — "Sketch the three required WAV regions before encoding
  fields." / "Write the header and then the sample bytes." **This is the one place in the
  bundle where the bundle genuinely could have shipped the result** — a WAV writer is a small
  file and a `supplies:` entry could hand it over. It is nonetheless **not toil**, because it
  fails the first half of the test decisively: the learner decides the layout, a wrong header
  is instructive and visible at `:68`, and it serves three stated objectives (`:21`, `:22`,
  `:23`). Handing this over would delete the course. Named here because "could the bundle have
  shipped it?" answering *yes* is unusual and a later reader will otherwise ask.
- `lessons/02-bytebeat-rhythm.md:62` and `lessons/00:63` — adding tests with known expected
  sample values. Looks mechanical; **rejected**, because the expected values must be derived
  by the learner from the expression and the chosen language's integer semantics, which is the
  objective at `lessons/02:22`.
- `lessons/03-compose-and-export.md:62-65` — the four environment questions before generating
  the live-playback lesson. **Rejected: this is the tutor's work, not an assignment to the
  learner.**
- `lessons/stereo-bytebeat.md:56` — "Interleave them and update the header calculations."
  Recalculating `byte rate`, `block align` and the two sizes is arithmetic. **Rejected**: the
  learner must work out *which* fields channel count touches, `:63` makes a wrong answer
  visible, and it serves `:23` ("Recalculate format fields that depend on channel count").

**No element in this course is charged −2. Every candidate above is rejected and scores what
it actually is.**

---

## 5. Proposals

Each names a concrete action. All are refusable. Proposals 1, 5 and 7 of the 2026-09-13
report are discharged and are not repeated; the rest are carried forward, renumbered, with
the line numbers re-taken from the files.

**Proposal 1 — decide, in writing, whether `stereo PCM` may live only in an optional
lesson.** `COURSE.md:65` lists `stereo PCM` under "Topics this course must cover", and the
only lesson that teaches it is optional (`tutorial.yaml:18-24`). `DESIGN.md:44-48`
(`#stereo-layout`) is likewise served only there. This is the rubric's permanently-unscored
question, so it costs nothing; the author's answer changes what happens next. If the topic
must be met: promote the material to the main path, or fold a two-channel section into lesson
03. If the offer is the right home for it: say so in `COURSE.md` — e.g. mark the bullet
"*(taught in the optional stereo lesson)*" — so a learner who declines is not left thinking a
must-cover topic was skipped by accident. **The `2ce5345` repair makes this question
sharper, not softer**: the offer is now made strictly after the main path is finished, so the
learner who declines has demonstrably completed the course without ever meeting the topic.

**Proposal 2 — close the unserved objective at `lessons/03-compose-and-export.md:23`.**
Either:

- (a) give it a learner-facing element — add one completion condition after `:74`, e.g. "The
  learner can state which parts of the finished project would still work on another machine
  with no audio hardware, and why live playback is not part of the authored course." That
  converts a narrated boundary into something the learner constructs, and recovers the −3; or
- (b) drop the objective from `:23` and let `COURSE.md:67-73` ("Explicit extension boundary")
  carry the idea as course framing rather than as a per-lesson objective. Also recovers the
  −3, and is the honest option if the author's intent was always that the tutor explains the
  boundary.

**Proposal 3 — split `lessons/03-compose-and-export.md:54` into a decision and an action.**
This is the one closing-action failure in the course (section 6.4). The bullet reads "Decide
what should change over the duration and derive a coarse time value." It is the lesson's
first progression bullet, so it is the first thing a tutor closes a turn on, and it fuses a
design decision with the action that depends on it. Concretely: replace it with two bullets,
e.g.

```
- Design decision for the learner: what should change over the duration? Settle this
  before the next task.
- Derive a coarse time value from `t` that expresses the decision above.
```

That is the same repair shape the rubric records for
`portable-fixed-window-rate-limiter/lessons/00-contract-and-language.md:66`, and it costs the
lesson no teaching: `:54` keeps its +2 either way.

**Proposal 4 — carry the missing `DESIGN.md` clause into the lesson that must honour it.**
`DESIGN.md:41-42` requires the generated live-playback lesson to "preserve the working offline
WAV path, **state any external dependency before installation**, and count its time separately".
`lessons/03:62-65` reproduces the first and third and not the second. Add "state any external
dependency before installing it" to the instruction at `:64-65`, so a tutor generating the side
lesson from the lesson text alone still honours the design decision.

**Proposal 5 — make little-endian encoding something the learner checks, not only something
the file implies.** `lessons/01:22` states it as an objective and `:63` asks for "a focused
check for header fields or total size". Extend `:63` to name the byte order, e.g. "Add a
focused check that a multi-byte header field (sample rate or byte rate) is written
least-significant byte first." One sentence, and the objective stops depending on a player's
tolerance to prove it.

**Proposal 6 — decide whether objective `lessons/00:23` should still claim the project
half.** After `c80d8e3`, the *project* half of "Establish an idiomatic project and test loop
in the chosen language" is exercised by `:57-58` (which determines the layout) and by `:68`
(an evidence condition), and no longer by any element that builds it. The objective is not
unserved — three or four servers remain, so no −3 fires (section 2) — but the author may
prefer to narrow it to "Establish a test loop in the chosen language", which `:63` and
`:70-71` exercise directly. This is the rubric's "residual hole" note, raised rather than
scored.

**Proposal 7 — consider giving lesson 03's composition work more weight.** Not a defect: at 8
over twelve elements it is the course's joint-lowest lesson, and the cause is two branch
points and six evidence conditions, which is what a closing lesson does. It is above zero, so
the rubric does not require a what-is-this-for question. Raised anyway, because if the author
wants the composition to carry more, `:54-55` is where to add it — and proposal 3 already
touches `:54`.

**The one result this bundle could have shipped stays where it is.** The WAV writer
(`lessons/01:59-60`) is a small file and a `supplies:` entry could hand it over — and must
not. It fails the first half of the toil test decisively and is the teaching the course exists
for; section 4 records that reasoning in full.

---

## 6. The questions only a reader can answer

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

**None found.** All 16 `design_refs` entries across the five lessons resolve to an anchor
that speaks to something the lesson actually raises:

- `lessons/00:4` → `#supported-tracks` (which track, and what it fixes — `:49`, `:57-58`),
  `#sample-model` (why 0–255, `:62`), `#expression-boundary` (what `t` maps to, `:61`);
- `lessons/01:4` → `#sample-model`, `#wav-contract` (`:52`, `:59-60`);
- `lessons/02:4` → `#sample-model`, `#expression-boundary` (`:50-51`), `#wav-contract`
  (`:52`);
- `lessons/03:4` → `#wav-contract`, `#expression-boundary`, `#composition-scope` (`:46-47`),
  `#generated-live-playback-extension` (`:62-65`);
- `lessons/stereo-bytebeat.md:4` → all four, including `#stereo-layout` for `:54-56`.

**One partial, in the opposite direction** — the lesson drops one of the reference's
obligations rather than the reference failing the lesson. `lessons/03:4` cites
`#generated-live-playback-extension`, and the anchor carries a requirement (`DESIGN.md:41-42`,
"state any external dependency before installation") that the lesson never restates.
Proposal 4. Unchanged from 2026-09-13 and re-verified against both files.

The weakest citation remains `lessons/03:4` → `#wav-contract`: lesson 03 raises no new
container question beyond "do not break what lesson 01 built" (`:48`, `:50`). Near-vacuous,
not wrong.

`lessons/00:4` → `#supported-tracks` improved at `c80d8e3`: the anchor's own list of what the
track determines is now echoed to the learner at `:57-58`, where before the lesson only named
the five options.

### 6.2 A lesson that introduces a type or concept nothing later uses

**None found.** The closest candidate, examined and cleared: `lessons/01:43` introduces
**"square waves"**, and lesson 02 immediately discards the square wave (`lessons/02:10-11`,
"Replace the regular test tone with a compact Bytebeat expression"). The *artifact* is
discarded; the *concept* is not. Period-and-frequency reasoning from `lessons/01:29` is what
makes `lessons/02:59` ("Multiply `t` and compare the perceived pitch") legible, and it
resurfaces at `lessons/stereo-bytebeat.md:66`. Scaffolding used later, not a dead concept.

Also checked and cleared:

- `lessons/00:45` "selected-language integer semantics" → used at `lessons/02:62` and now
  named as a consequence of the choice at `:57-58`;
- `lessons/03:41` "subjective versus objective completion criteria" → used in that lesson's
  own `:72-73`;
- `lessons/stereo-bytebeat.md:39-41` "block alignment", "byte rate" → used in that lesson's
  own `:63` and `:66`. Terminal lesson, so "nothing later" is structural rather than a defect.

Newly checked because `c80d8e3` added it: the three consequences named at `:57-58` — "project
layout", "run and test commands", "integer semantics" — are all used later (`:68`, `:63`,
`lessons/02:62`). Nothing introduced and abandoned.

### 6.3 A symbol or term a lesson uses and no lesson introduces

**The row passes. No symbol in this bundle is bound only in `DESIGN.md`, and none is bound
nowhere.** I sorted the candidates by hand and did not repeat the script's buckets as a
verdict.

`audit.py` tabulated **one distinct symbol, `t`**, in five rows: one in
`lesson-prose-elsewhere` (lesson 00) and four in `other-lesson-prose` (lessons 01, 02, 03 and
stereo). Its `design-md-only` and `none` buckets are both empty. Taking each judgement in
turn:

- **Is `t` a symbol under this row? Yes.** It is a parameter of the concept being taught —
  the sample index, which is what a Bytebeat expression maps — exactly the `N`/`W` side of the
  author's 2026-09-13 boundary. Nobody brings `t` to this course from their chosen language.
  The script correctly declined to sort it, and I sort it in.
- **Is it introduced in a lesson, at or before its first use? Yes.** First use anywhere is
  `lessons/00-language-and-waveform.md:21`, "Relate sample index `t` to elapsed time" — a
  learning-objective bullet that itself binds the symbol by apposition ("sample index `t`").
  Six lines later, `## Theory` at `:27` defines it quantitatively for the learner: "At 8,000
  samples per second, sample `t` represents `t / 8000` seconds after the start", and `:28`
  adds "The program will calculate one integer for each `t`." Both are learner-facing
  expository prose, not tutor instruction. The script filed these as
  `lesson-prose-elsewhere` only because its window is the paragraph block around the first
  use and a `## Theory` heading starts a fresh block; the distance is six lines inside one
  lesson.
- **Is `## Concepts to teach` doing the work? No, and it does not need to.** `lessons/00:40`
  lists "sample index", and the rubric is right that appearing there is not itself a
  definition — it is an instruction to the tutor. The pass rests on `:21` and `:27`, not on
  `:40`. I checked this deliberately because it is the trap the row names.
- **The four `other-lesson-prose` rows do not fire.** The script's caveat for that bucket is
  "A learner who reaches this lesson without that one has met no definition." No learner can
  reach any of them without lesson 00, because the course is a strict prerequisite chain
  stated in the lesson files: `lessons/01:15` requires lesson 00; `lessons/02:15` requires
  lesson 01; `lessons/03:15` requires lesson 02; `lessons/stereo-bytebeat.md:16` requires
  lesson 03 (and that last link is stronger than it was yesterday — `2ce5345`). So the first
  uses at `lessons/01:29`, `lessons/02:20`, `lessons/03:28` and
  `lessons/stereo-bytebeat.md:54` all stand behind `lessons/00:27`.
- **`DESIGN.md:24` binds `t` too** ("A Bytebeat expression maps the non-negative integer
  sample index `t` to an integer"), under `#expression-boundary`. The script flags it
  `TUTOR-ONLY, does not introduce the symbol to a learner`, and that is correct. It is not
  needed here: the lessons carry the binding independently. Had they not, this would have been
  a **bound only in `DESIGN.md`** finding and the repair would have been to restate it in
  lesson 00.
- **Bound nowhere: none.**

Two terms I checked by hand beyond the script's candidate shape, because the script only
collects short backticked identifiers: `block alignment` and `byte rate` are used first at
`lessons/stereo-bytebeat.md:30` and defined in the same paragraph (`:28-30`), and listed at
`:39-41`. `RIFF` is used and defined in the same sentence at `lessons/01:31`. Nothing else in
the corpus is a course-invented term used before its binding.

### 6.4 Does the lesson equip the tutor to end a turn with one concrete action?

Answered for **every** lesson in the section 2 table. **Four pass, one fails.** I graded the
lesson **files**. No transcript exists for this bundle and none would have changed the
answer: an author can edit a lesson and cannot edit a tutor's behaviour from this repository.

**Condition 2 first, because it is the one an auditor skips.** The rubric's second failure
shape is an open question with no home — a section that invites a discussion the tutor then
raises where the action should be. **All five lessons carry an `## Optional deeper paths`
section and none of them fails this way**, which is worth stating rather than passing over.
The failing precedent (`portable-fixed-window-rate-limiter`) *invites* a discussion with no
gate. Each of these five gates the content on the learner asking **and** puts it outside the
required work:

- `lessons/00:81-82` "If asked … Do not require them before the learner has heard the
  generated output."
- `lessons/01:81-82` "If asked … Keep music theory and general-purpose WAV support outside
  the required work."
- `lessons/02:80-81` "If asked … Avoid turning exploration into a catalogue of unexplained
  formulas."
- `lessons/03:85-87` "… only if asked. Each can become a learner-requested generated side
  lesson; **none changes completion of the authored course**."
- `lessons/stereo-bytebeat.md:75-76` "If asked … Do not combine those changes into this
  lesson's required work."

A tutor reading any of these cannot conclude that raising one closes a turn.

**Per lesson:**

- **`lessons/00-language-and-waveform.md` — pass.** Condition 1: the first concrete learner
  action is named at `:61`, "Generate a short sequence from a deliberately simple function of
  `t`", with the artifact bounded at `:52` ("Generate enough values to inspect, but do not
  write a WAV file yet"). Condition 2: the lesson's one design decision — the language track —
  is marked as a decision *and* sequenced ahead of every action, by `:49` ("Ask the learner to
  choose … **before setup**") and again by `:57-58` standing as its own bullet ahead of the
  action bullets. This is the textbook shape the rubric asks for, and `c80d8e3` improved it:
  the old single bullet fused the decision with the creation.
- **`lessons/01-write-a-tone.md` — pass.** Condition 1: the artifact is named at `:50`
  ("Write the result to `output.wav`") and the first action at `:58`. Condition 2: no design
  decision is left standing in an action bullet — the container's parameters are fixed by
  `:51-54` before the progression begins. I examined `:60` ("Write the header and then the
  sample bytes"), which has the two-clause shape the rubric warns about, and cleared it: both
  halves are the same act in a stated order, "and then" tells the tutor which comes first, and
  neither half contains an unresolved choice. The failing precedent's bullet fused *prose*
  with *an API signature **or** a stub* — different kinds of work with a choice inside the
  second. This is not that.
- **`lessons/02-bytebeat-rhythm.md` — pass, and it is the strongest lesson on this row.**
  Condition 1: `:58` names the first action. Condition 2: `:54` states the rule explicitly —
  "Make changes one at a time so the learner can attribute audible effects" — which is the
  runner's one-actionable-task rule written into the lesson, and `:59`–`:61` are three
  single-action bullets in order.
- **`lessons/03-compose-and-export.md` — FAIL, condition 2.** The failing sentence is
  **`lessons/03-compose-and-export.md:54`: "Decide what should change over the duration and
  derive a coarse time value."** It is the lesson's **first** progression bullet, so it is the
  first thing a tutor can close a turn on, and it holds a design decision ("what should change
  over the duration") in the same bullet as the action that depends on it ("derive a coarse
  time value"). The tutor must split it before either half is a next step, and the lesson
  nowhere says to split it, marks the decision as a decision, or settles it earlier — `:47`
  ("Create at least two recognisably different sections or one deliberate evolving rule")
  restates the choice rather than settling it, and `:21` names it as an objective. This is the
  same shape the rubric records at
  `portable-fixed-window-rate-limiter/lessons/00-contract-and-language.md:66`. Condition 1 is
  satisfied — `:50` names `output.wav` and `:56-57` name concrete actions — but the row needs
  both. Repair: proposal 3. **The rubric does not object to the decision**; the lesson should
  make the learner choose. It objects to the decision sitting where the action should be.
- **`lessons/stereo-bytebeat.md` — pass.** Condition 1: `:54` is a single concrete design act
  ("Separate “sample at `t`” from “frame at `t`” in the design"), `:55`–`:57` are single
  actions, and the artifact is `output.wav` throughout. Condition 2: the channel-expression
  decision is stated as a constraint at `:49` ("Use two deterministic expressions with an
  intentional relationship") ahead of the progression, and the progression's refinement step
  (`:58b`) comes last, after the artifact exists.

**One delta worth naming.** Before `2ce5345`, `lessons/03:59` read "Before the first required
task, make the authored stereo offer from the manifest" — an open offer placed at exactly the
moment the lesson's first concrete action should be. That was a second condition-2 concern in
the same lesson, and the fix removed it. Lesson 03 still fails this row, on `:54` alone.

### 6.5 The completability invariant, and `tutorail-bundles#5`

> **Can a learner who declines every offer still finish this course?**

**Yes — and, new since 2026-09-13, so can a learner who accepts.**

**`tutorail-bundles#5` is genuinely fixed. Verified from the files, not from the commit
message.** The 2026-09-13 report's proposal 1 recorded the defect: the stereo offer was made
*before* lesson 03's first required task, the stereo lesson converts the writer to two
channels, and lesson 03 requires `output.wav` to be mono — so a learner who accepted the offer
where the lesson told the tutor to make it could not then satisfy lesson 03. The evidence that
it is repaired:

- **The offer moved.** `lessons/03-compose-and-export.md:59-61` now reads: "After the
  main-path completion conditions are met, make the authored stereo offer from the manifest.
  The mono course is finished by then, so a later two-channel `output.wav` does not disturb
  this lesson's completion conditions." The old text, "Before the first required task, make
  the authored stereo offer from the manifest", is gone from the file.
- **The prerequisite moved too, which was the second door.** `lessons/stereo-bytebeat.md:16`
  now reads "Lesson `03-compose-and-export` is complete and the mono WAV writer produces a
  valid, audible file." It said `02-bytebeat-rhythm` before. That line was the one remaining
  licence to start the stereo lesson before lesson 03's mono conditions were met, and it no
  longer grants it. This is also the 2026-09-13 report's proposal 5, discharged by the same
  commit.
- **No third door exists.** I grepped every mention of stereo, offers and two channels across
  `tutorial.yaml`, `COURSE.md`, `DESIGN.md` and all five lessons. Every remaining mention is
  either descriptive (`COURSE.md:44-45`, `DESIGN.md:44-48`, `lessons/03:79`, `:85`) or
  correctly gated. `tutorial.yaml:20` still reads `offer_at:
  [lessons/03-compose-and-export.md]`, which names the lesson and not the moment inside it, and
  was never the defect. `tutorial.yaml:21-24`'s `offer_because` is timing-neutral.
- **The ordering is now internally consistent in both directions.** Lesson 03's completion
  conditions (`:69-74`) demand mono; the offer comes after they are met; the stereo lesson's
  own prerequisite demands lesson 03 complete. Lesson 03 is the last lesson on the main path,
  so an accepting learner extends a finished mono course rather than interrupting one.

**What is deliberately *not* fixed, and does not need to be.** `tutorial.yaml:49` still
declares `output-wav: { kind: file-exists, path: output.wav }`, which a stereo file satisfies
as well as a mono one. That is why the validator stayed green through the original defect, and
it is still true today. It is now harmless, because nothing re-checks lesson 03's conditions
after the stereo lesson runs; the contradiction was in the ordering, and the ordering is what
was repaired. The commit message records that writing `output-stereo.wav` was considered and
rejected because `output.wav` is the course's single named artefact. I agree with that call:
the alternative would have contradicted `lessons/03:50` ("Keep the final output at
`output.wav`") and `COURSE.md:10-11`. **No proposal here.**

**The invariant itself, answered from the main-path lessons rather than the manifest:**

- **Does any main-path completion condition depend on something only an optional lesson
  builds or explains?** No. Lesson 03's conditions (`:69-74`) require mono 8-bit PCM at 8,000
  Hz, two sections or an evolving structure, passing tests, an explanation, and independence
  from playback dependencies. Every one is built by lessons 00–02 and 03 itself. Nothing
  requires frames, interleaving, block alignment or a second channel.
- **Does any main-path lesson's prose assume the learner took an offer?** No, and the course
  goes out of its way not to. `lessons/03:79-81` instructs the tutor to record whether the
  stereo and live-playback offers "were declined, deferred, or accepted", so declining is an
  explicitly anticipated path. `COURSE.md:10-12` puts live playback outside the time estimate,
  and `lessons/03:74` makes independence from playback dependencies a *condition*, not a
  caveat.
- **`required_for` gates on optional lessons: none.** I read `tutorial.yaml:18-24` directly
  rather than trusting `optional_lesson_count` — the block contains `offer_at` and
  `offer_because` only, with no `required_for`, no `anticipates` and no `repair_in`. The
  rubric's −3 row does not fire and its warning is therefore not printed.

**Prose optionality vs manifest optionality: they agree here.** The one lesson the manifest
makes optional (`lessons/stereo-bytebeat.md`) also declares `optional: true` in its own front
matter (`:6`), is titled and described as an extension, and is named as optional at
`COURSE.md:44-45`. No lesson sitting in `lessons:` calls itself optional in its prose. The
`## Optional deeper paths` sections at the foot of all five lessons are conditional discussion
topics ("If asked…"), not lessons, and the live-playback extension is generated on request and
is not a bundle lesson at all (`DESIGN.md:34-39`). Neither creates a disagreement. **The total
in section 1 therefore needs no restatement**; the main-path figure of 42 is given for
information, not as a correction.

### 6.6 A must-cover topic that only an optional lesson teaches

**Found: one, unchanged from 2026-09-13.** `COURSE.md:65` lists **`stereo PCM`** under "Topics
this course must cover". The only lesson teaching it is `lessons/stereo-bytebeat.md`, which
`tutorial.yaml:18-24` makes optional. `DESIGN.md:44-48` (`#stereo-layout`) is likewise served
only there.

Asked as the rubric requires, and **not scored** — the rubric settled in the negative on
scoring this row, and that decision stands:

> Is that acceptable for this course, given that a learner who declines every offer never
> meets `stereo PCM` at all, while `COURSE.md` tells them the course must cover it?

It may well be acceptable: the format is explicit that a topic an optional lesson teaches *is*
in the course, and listing it is what makes the tutor offer the authored lesson instead of
improvising a replacement. The author's answer drives proposal 1 either way. Note only that
`2ce5345` moved the offer to after the main path completes, so the declining learner's course
is now demonstrably finished before the topic is ever mentioned.

### 6.7 A lesson far outside the course's usual size

**None found.** The five lessons carry 11, 11, 12, 12 and 11 scored elements, run 82 / 82 / 81
/ 87 / 76 lines, and share an identical section structure. There is no candidate for splitting
and none for folding into a neighbour. Lesson 00 grew three lines at `c80d8e3` and lesson 03
two at `2ce5345`; neither moves the distribution.

The outliers are **scores**, not sizes. `lessons/03-compose-and-export.md` scores 8 against
12, 10, 15 and 10. It reaches 8 from the same twelve-element count as lesson 02, and the cause
is visible in its breakdown: two branch points and six evidence conditions against four
constructive elements. That is a defensible shape for a closing lesson that has to land the
artifact and make two offers, and it is above zero, so the rubric does not require a
what-is-this-for question. Raised anyway as proposal 7. **Lesson 00 is no longer an outlier**:
it scored 8 on 2026-09-13 only because one element was charged −2, and that element is gone.

### 6.8 Dynamic evidence

No dry-run harness was run against this bundle for this audit, so there is no stall to cite in
either direction. Nothing in this report rests on dynamic evidence. The `tutorail-bundles#5`
finding it inherits was found by reading, not by a harness, and it is verified above by
reading.

---

## Note on the audit brief

Assertions in the dispatch, checked against the files:

- **"Its old element was a CONJUNCTION … and it is now TWO bullets"** — correct.
  `c80d8e3` replaced "Select the language track and create its smallest conventional runnable
  project." with the two bullets now at `:57-58` and `:59-60`.
- **"The selection bullet gained consequences"** — correct, and quoted in full in section 2.
- **"So this is NOT a subtraction: the course loses a charge and may gain a positive"** —
  correct as a description of what the change makes possible. The judgement was still mine to
  make, and I made it in favour of +2, with the counter-argument and its cost (48 and 38)
  printed so the author can overrule me without re-deriving anything.
- **"On 2026-09-13 this bundle did NOT take the exception: objective `00:23` had four
  servers. Re-enumerate; the lesson has changed."** — correct and acted on. Re-enumerated in
  section 2: three servers remain without counting the selection bullet, four with it. The
  objective is not sole-served, so no −3, and the exception is moot rather than declined,
  because there is no longer a setup element for it to except.
- **"`audit.py` reports `t` for this bundle across several lessons — judge those rows, do not
  just repeat them."** — done in section 6.3. The row passes; the buckets are a correct
  tabulation and none of them is a finding, because the definition is in a lesson and the
  course is a strict prerequisite chain.
- **"The 2026-09-13 report … contains a corrected arithmetic error … Re-add everything
  yourself."** — done. I re-added all five lessons from the files. My lesson 01 sum is 10,
  independently of that report's corrected figure; I did not inherit either 10 or 12.
- **No instruction in the brief was found to be wrong.** The one place I depart from a
  reading the brief invited is that I scored the *selection* bullet rather than treating the
  whole of `c80d8e3` as removing a charge; the brief explicitly left that judgement open
  ("may gain a positive … Judge the selection bullet on what it now says").

Every element score sums to the lesson figure printed beside it, and the lesson figures sum to
55, from which the single course-level penalty of −3 gives **52**. No discrepancy was found
between the elements and the stated totals, and no element was adjusted to make a total come
out.
