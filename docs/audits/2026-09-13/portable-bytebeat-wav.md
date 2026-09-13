# Course quality audit: `portable-bytebeat-wav`

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
  lesson 00-language-and-waveform   12
  lesson 01-write-a-tone            12
  lesson 02-bytebeat-rhythm         15
  lesson 03-compose-and-export       8
  lesson stereo-bytebeat [optional] 10
  --------------------------------------
  sum of lessons                    57
  − unserved objectives (1 × −3)    −3   (03-compose-and-export objective 4)
  − unserved anchors    (0 × −3)     0
  − required_for gates  (0 × −3)     0
  --------------------------------------
  COURSE TOTAL                      54
```

**Main path only** (a learner who declines the stereo offer, which is the supported outcome):
12 + 12 + 15 + 8 = 47, − 3 = **44**. Prose and manifest agree about which lesson is optional
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
| `lessons/00-language-and-waveform.md` — Turn time into samples | **12** | 4 of 4 | none |
| `lessons/01-write-a-tone.md` — Put a tone in a WAV file | **12** | 4 of 4 | none |
| `lessons/02-bytebeat-rhythm.md` — Find rhythm in the bits | **15** | 4 of 4 | none |
| `lessons/03-compose-and-export.md` — Shape a tiny composition | **8** | 3 of 4 | none |
| `lessons/stereo-bytebeat.md` *(optional)* — Compose in two channels | **10** | 4 of 4 | none |

No lesson scores at or below zero. Full element breakdowns follow for all five, because two
figures (03 at 8, 02 at 15) are not obvious from the row.

### `lessons/00-language-and-waveform.md` — 12

| file:line | Sentence | Score |
|---|---|---:|
| `:49` | "Ask the learner to choose TypeScript, JavaScript, Python, Go, or Kotlin before setup." | 0 |
| `:57` | "Select the language track and create its smallest conventional runnable project." (project clause; the select clause is the branch at `:49`) | +2 |
| `:58` | "Generate a short sequence from a deliberately simple function of `t`." | +2 |
| `:59` | "Reduce every value to 0–255 using an idiom correct for the language." | +2 |
| `:60` | "Add a small deterministic test or inspectable assertion for several known samples." | +2 |
| `:61` | "Ask the learner to predict how changing the expression changes the sequence." | +2 |
| `:65` | "The project runs with the selected toolchain." | 0 |
| `:66` | "It produces a deterministic sequence of values, all in the range 0–255." | 0 |
| `:67-68` | "At least a few known indices are checked automatically or by clear executable evidence." | 0 |
| `:69` | "The learner can explain the relationship among `t`, sample rate, and elapsed time." | +2 |

Sum: 0+2+2+2+2+2+0+0+0+2 = **12**.

Two calls worth arguing with. `:49` is the course's language fork, and the rubric settles a
branch point at 0 even though it is the element that serves the `supported-language selection`
topic — **serving a topic and scoring points are different questions**. `:57`'s project clause
I scored +2 rather than 0 because `Establish an idiomatic project and test loop in the chosen
language` is a stated objective (`:23`) and the learner picks the layout and test runner; an
author who thinks "create a project" is setup rather than teaching would score it 0 and the
lesson would be 10.

### `lessons/01-write-a-tone.md` — 12

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

Sum: **12**. `:59` is the best-constructed element in the course — the learner builds a model
of the container before writing a byte, and a wrong sketch fails visibly at `:68`.

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

### `lessons/03-compose-and-export.md` — 8 (lowest)

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
  though `:49` scores 0. Serving and scoring are independent.
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

**Confirmed toil sites: none. The inventory is empty, and here is why that is a real finding
rather than an absence of looking.**

The scanner reported 0 candidates. **The scanner is a candidate generator over a fixed verb
list, and its silence is evidence about the verb list, not about the course.** This inventory
comes from opening all five lessons and reading every progression bullet, constraint and
completion condition — 56 scored elements — against the rubric's two-part toil test.

The structural reason the inventory is empty is worth stating: **this bundle ships no files at
all.** `supplies:` is empty, the bundle contains nothing but `COURSE.md`, `DESIGN.md`,
`tutorial.yaml`, `STATE.template.md` and five lesson files. There is no asset it withheld and
re-assigned to the learner, and the one deterministic, unambiguous piece of work in the course —
laying out the RIFF header bytes — is also the thing the course exists to teach.

**Candidates I examined and rejected, so the next reader does not re-litigate them:**

- `lessons/00-language-and-waveform.md:57` — "Select the language track and create its smallest
  conventional runnable project." **Rejected: the bundle could not have supplied the result.**
  A runnable project in the learner's chosen track needs a toolchain, and for Node tracks a
  package install; no `supplies:` entry can create either. The rubric's last clause is explicit
  that this is the learner's setup. Scored +2 on its own merits, not −2.
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

**Nothing in this course is charged −2.**

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

**No `supplies.py` proposal is possible or appropriate for this bundle.** The toil inventory is
empty, and the only result the bundle could have shipped (the WAV writer) is the teaching. There is
no `--from` path to write, and saying so plainly is the correct outcome here rather than inventing
a supplies entry.

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

The outlier is a **score**, not a size: `lessons/03-compose-and-export.md` scores 8 against 12, 12
and 15, from the same 12-element count as lesson 02. The cause is visible in its breakdown — two
branch points (`:59`, `:60-63`) and six evidence conditions, against four constructive elements.
That is a defensible shape for a closing lesson that has to land the artifact and make two offers,
and it is above zero, so the rubric does not require a what-is-this-for question. Raised anyway,
because if the author wants the composition work to carry more weight, `:54-55` is where to add it.

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
therefore needs no restatement**; the main-path-only figure of 44 is given there for information,
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
