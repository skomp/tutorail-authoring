# Course quality: `pico-ps2-usb-adapter`

**Date:** 2026-09-29
**Bundle:** `skomp/tutorail-bundles`, `pico-ps2-usb-adapter`, on branch
`worktree-pico-ps2-usb-adapter` (local; not pushed at the time of this audit)
**Auditor:** a Claude session, using the `course-quality` skill and the rubric at
`skills/course-quality/references/rubric.md`

This bundle was authored the same day it was audited. That is worth stating plainly: the
audit is of a course nobody has taught yet, so every finding is about the text and none of
it is about how a lesson actually went.

**The validator is green and says nothing about any of this.** `validate_bundle.py` returns
PASS on this bundle. That answers "is this a bundle?". This report answers "does it teach?".

---

## 1. The course and its total

| | |
|---|---|
| Bundle id | `pico-ps2-usb-adapter` |
| Title | Build a PS/2 to USB HID Keyboard Adapter on the Raspberry Pi Pico |
| Main-path lessons | 19 |
| Offered lessons | 7 |
| Declared supplies | 16 |
| Validators | 28 (17 `command`, 11 `manual`) |

**Total: 579**

```
  lessons 00-05                                139
  lessons 06-12                                155
  lessons 13-18                                161
  the seven offered lessons                    133
                                            ------
  sum of lessons                               588

  unserved objective  00 "where code and data live"   -3
  unserved objective  04 "what the CPU does on entry" -3
  unserved objective  11 "why control plus interrupt" -3
  required_for gates on optional lessons (none)        0
  unserved DESIGN.md anchors (none)                    0
                                            ------
  total                                        579
```

**This number is comparable against this course's own lessons and against nothing else.**
A lesson's figure tracks how finely its `## Suggested progression` enumerates clauses, so
it must not be set beside `rust-automaton-db`'s total or any other bundle's. The inventory
below is the point; the number is a summary of it.

---

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil | Closing action |
|---|---|---|---|---|
| 00 `first-code-and-a-window-in` | **11** | 5 of 6 | **1 site, −2** | pass |
| 01 `the-ps2-connector-and-what-is-safe` | 19 | 6 of 6 | none | pass |
| 02 `open-drain-and-pull-ups` | 21 | 7 of 7 | none | pass |
| 03 `see-the-protocol-before-you-decode-it` | 28 | 6 of 6 | none | pass |
| 04 `your-first-interrupt` | 27 | 4 of 6 | none | pass |
| 05 `a-state-machine-in-an-isr` | 33 | 7 of 7 | none | pass |
| 06 `handing-data-to-the-main-loop` | 23 | 7 of 7 | none | pass |
| 07 `what-a-pio-state-machine-is` | 22 | 7 of 7 | none | pass |
| 08 `ps2-receive-in-pio` | 28 | 7 of 7 | none | pass |
| 09 `talking-back-in-pio` | 24 | 7 of 7 | none | pass |
| 10 `scan-codes-to-key-events` | 20 | 7 of 7 | none | pass |
| 11 `descriptors-you-write-yourself` | **16** | 7 of 8 | none | pass |
| 12 `the-hid-report-descriptor` | 22 | 8 of 8 | none | pass |
| 13 `your-first-keystroke` | 21 | 7 of 7 | none | pass |
| 14 `events-to-state` | 32 | 8 of 8 | none | pass |
| 15 `the-lock-leds` | 19 | 8 of 8 | none | pass |
| 16 `when-it-goes-wrong` | 32 | 9 of 9 | none | pass |
| 17 `robustness-and-the-real-world` | 30 | 9 of 9 | none | pass |
| 18 `off-the-breadboard-and-done` | 27 | 10 of 10 | none | pass |
| `see-the-edges-on-a-scope` *(offered)* | 18 | 5 of 5 | none | pass |
| `watch-the-enumeration` *(offered)* | 19 | 5 of 5 | none | pass |
| `a-safety-catch` *(offered)* | 18 | 5 of 5 | none | pass † |
| `a-second-interface-for-debugging` *(offered)* | 20 | 6 of 6 | none | pass |
| `measure-your-latency` *(offered)* | 18 | 6 of 6 | none | pass |
| `nkro-without-a-driver` *(offered)* | 17 | 6 of 6 | none | pass |
| `remap-and-macros` *(offered)* | 23 | 5 of 5 | none | pass |

**No lesson scores at or below zero.** The lowest is lesson 00 at 11, and its figure is
depressed by the single toil charge in the whole course plus a high proportion of
unavoidable setup; see the breakdown below.

† **One overturned verdict, recorded so it can be argued with.** The scorer failed
`a-safety-catch` on `lessons/a-safety-catch.md:195-197`, a compound step bundling two
transition handlers and a verification. I overturned it to pass. The rubric's row asks
whether the lesson's **closing** action names a concrete first action and keeps a design
decision out of it. This lesson's closing action is step 17 at `:214-216` — "Remove the
runaway build, return to your real firmware, keep the gate" — which is concrete, and the
one design decision (gate polarity) is settled back at step 2, `:177-179`. The compound
bullet is mid-progression and cannot fail this row. It is recorded as a step-granularity
note in section 5 instead.

### Element breakdown — lesson 00, the only lesson whose figure needs explaining

| Element | Score | file:line |
|---|---|---|
| Install toolchain, CMake, SDK; set `PICO_SDK_PATH` | 0 | `00:210-212` |
| Confirm the environment with `toolchain-present` | 0 | `00:213-214` |
| Read supplied `README.md` and `pico_sdk_import.cmake` | 0 | `00:215-217` |
| **Write a minimal `CMakeLists.txt`** | **−2** | `00:218-219` |
| Write a `main` that toggles the LED | +2 | `00:220` |
| Flash via BOOTSEL, watch the drive dismount | 0 | `00:221-222` |
| Say what each of those two states was | +2 | `00:223-224` |
| Add a `printf` with no stdio route and observe silence | +2 | `00:225-227` |
| Enable UART stdio, explicitly disable USB | +2 | `00:228-229` |
| Flash the second Pico as `debugprobe` | 0 | `00:230-231` |
| Wire the console, checking pin numbers against documentation | 0 | `00:232-235` |
| Get `printf` onto the screen; suspect TX/RX swap | +1 | `00:236-238` |
| Record the port in `device.env` | 0 | `00:239-240` |
| Replace the scratch print with `alive: <n>` | +2 | `00:241-243` |
| Run `build-ok` and `firmware-alive` | 0 | `00:244` |
| Unplug the probe and watch the console go silent | +2 | `00:245-247` |
| Six completion conditions | 0 each | `00:251-261` |

Sum: **11**.

---

## 3. Goal gaps

**DESIGN.md anchors: zero gaps.** All nine are served, judged by what lessons *do* and not
by what they cite. Worth recording how the hardest one was decided:
`#deliberately-unresolved` appears in **no** lesson's `design_refs` at all and is served
anyway — lesson 18 puts two of its three choices to the learner (`18:348-350` module versus
discrete, `18:395-398` the vendor interface) and lesson 13 raises the third, the host you
are willing to have typed into (`13:21`). The other eight anchors are each cited and used
by between three and nine lessons.

**Unserved learning objectives: three, −3 each, −9 total.** Each was decided by reading the
lesson's `## Suggested progression` and `## Completion conditions` and looking for an
element that makes the learner do the thing. A topic taught only in `## Theory` is read and
not exercised, and that is what these three are.

| Objective | Where it is stated | Why it is unserved |
|---|---|---|
| "Describe where code and data live on this chip — external QSPI flash executed in place, internal SRAM — and why the first call into a function can be slower than the second." | `00` objectives, 3rd bullet | Taught at `00:107-111` in Theory. No progression step and no completion condition touches XIP, SRAM or first-call cost. The only exercise is the **optional** deeper path "Measure the XIP cache effect" at `00:280-281`, which a learner need never open. |
| "Explain what the CPU does when an interrupt fires — what the hardware stacks, where the vector comes from, and why a handler is not a thread." | `04` objectives, 1st bullet | Taught at `04:66-98`. The eight completion conditions at `04:311-328` cover edge counts, the `printf` prohibition, `volatile`, and handler-body discipline — none asks the learner to explain stacking, the vector table, or handler-versus-thread. |
| "Describe the USB bus model: one host, addresses, endpoints, and the four transfer types, and say why a keyboard uses control plus interrupt and neither of the other two." | `11` objectives, 1st bullet | Taught at `11:78-90`. Neither half is exercised: the ten completion conditions never mention transfer types, and no progression step asks the learner to justify the choice. |

**One flagged objective I am NOT charging**, recorded so the next auditor does not re-open
it. Lesson 04's third objective — "State the components of interrupt latency on this chip,
and give a number for your own handler's budget derived from your measured clock period" —
was reported as thinly exercised. It is half-served, and half-served is not unserved:
completion condition 5 at `04:315-317` requires the learner to "justify the `printf`
prohibition with the 86.8 µs-per-character figure set against their own measured bit time",
which is exactly a number derived from their measured clock period set against a budget.
The *components* of latency remain Theory-only. That is a tightening proposal in section 5,
not a −3.

---

## 4. The toil inventory

**One confirmed site in twenty-six lessons.**

> `lessons/00-first-code-and-a-window-in.md:218-219`
> "Write a minimal `CMakeLists.txt`: project, SDK initialisation, one executable, link the
> core SDK library, and produce the extra outputs including the `.uf2`."

Scored **−2**. The reasoning, because this one is contestable and the author has a real
counter-argument (section 5 puts it):

- **The shippability test.** This is a single-platform course — RP2040, pico-sdk, C, no
  language choice — so the bundle could ship exactly one file and be done. It already ships
  `pico_sdk_import.cmake`, which is comparably boilerplate.
- **The sole-server exception does not fire.** The nearest objective naming this work is
  "Configure a pico-sdk project so that `printf` reaches a specific physical route", and it
  has other servers: step 9 at `00:228-229` enables UART stdio and disables USB, and
  completion condition 5 at `00:255-256` requires the learner to point at both lines. So the
  skeleton is a part of a larger goal, not the goal, and the rubric's project-skeleton
  tiebreak applies: when the two tests disagree, shippability wins.

### Candidates examined and rejected

The scanner produced four candidates over 26 lessons. All four were opened; **three were
rejected, and the fourth is a different line in lesson 00 from the one charged.**

| Candidate | Verdict |
|---|---|
| `00:210-212` "Install the ARM cross-toolchain, CMake and the Pico SDK on your machine" | **Rejected — needs the network.** No `supplies` entry can install a toolchain. The lesson says so itself in the same sentence. The learner's setup, not toil. |
| `00:221-222` "Flash it: hold BOOTSEL while plugging the Pico in… copy the `.uf2`" | **Rejected — physical.** The `copy` verb fired on a hardware action. A bundle cannot ship "having flashed a chip". |
| `a-second-interface-for-debugging.md:206` "Install a HID tool and attempt to open your keyboard interface" | **Rejected — needs the network**, and the tool is platform-specific. The lesson's own prerequisites say "Installing it is your work and needs the network." |
| `watch-the-enumeration.md:180` "Install Wireshark and the capture back end — a kernel module you load on Linux" | **Rejected — needs the network**, and a kernel module cannot ship in any bundle. |

Beyond the scanner, three further candidates were examined by hand and rejected:

- **Hand-writing USB descriptor bytes** (`11`, `12`, `a-second-interface-for-debugging`,
  `nkro-without-a-driver`). Not toil, and it is the setup-is-the-subject exception:
  `COURSE.md:48-50` declares "You write every USB descriptor by hand. No generator, no
  copied header." The bookkeeping mistakes these steps invite — a wrong `wTotalLength`, a
  forced report ID — are the lessons' designed instructive failures. A wrong answer here
  teaches a great deal, which is the opposite of the toil test.
- **Transcribing the scan-code table** (`10`). Not toil, and this is the toil rule working
  as intended rather than being violated. Lesson 10 bounds the learner's own table to about
  ten entries (constraint `10:236-237`, step `10:278-281`, completion `10:303-304`) and the
  bundle ships the remaining hundred-odd as `include/ps2_set2_to_hid.h`, placed at lesson
  14. The lesson says out loud that the rest is not the learner's work.
- **Soldering, track cuts, continuity testing, the BIOS test** (`18`). Not toil. A bundle
  cannot ship a soldered, cased, hand-tested adapter. Each step was scored on whether it
  carries a decision or an instructive mistake, and they do.

**The scanner is a candidate generator and its silence proves nothing.** This inventory came
from opening all twenty-six lessons, not from the four lines the verb patterns caught.

---

## 5. Proposals

Every one of these is a proposal the author may refuse. Applying any of them goes back
through the `tutorail-authoring` skill and its toolkit.

### 5.1 The `CMakeLists.txt` charge, and the author's counter-argument

The spec already ruled on this, deliberately, and the ruling is in
`pico-ps2-usb-adapter/SPEC.md` under *Supplied files*:

> **Not supplied, and deliberately so:** `CMakeLists.txt` and every line of firmware. The
> CMake file is edited in nearly every lesson — adding the PIO program, adding TinyUSB,
> switching backends — so it is a thing the learner must be able to change, not a thing
> handed over.

**That argument is good and the score stands anyway**, which is the rubric working rather
than the rubric being wrong: a signal a reader can argue down to zero stops being
comparable. But the two positions are reconcilable, and the reconciliation is the proposal:

> Supply a **minimal** `CMakeLists.txt` — `cmake_minimum_required`, `project`,
> `pico_sdk_init`, one `add_executable` with an empty source list, `target_link_libraries`
> with `pico_stdlib`, and `pico_add_extra_outputs` — and keep every *decision* in lesson 00
> as the learner's. The stdio routing (`pico_enable_stdio_uart` / `pico_enable_stdio_usb`),
> which is the actual teaching in that lesson, is then an edit the learner makes to a file
> they own rather than boilerplate they retype first.

```
python3 scripts/supplies.py add pico-ps2-usb-adapter \
    --from supplies/CMakeLists.txt \
    --to CMakeLists.txt \
    --describe "A minimal CMake file that finds the SDK and builds one executable. Everything this course teaches about the build - the stdio route, the PIO header, TinyUSB, the backend switch - you add to it yourself." \
    --check
```

Prose to delete once declared: `00:218-219`, replaced by a sentence pointing at the supplied
file and naming what the learner must add to it. **Note the file does not exist yet** — it
must be written into `pico-ps2-usb-adapter/supplies/` before the command above will run.

If the author prefers the current arrangement, the right outcome is to record the decision
in the bundle and leave the −2 standing as a known, accepted cost.

### 5.2 The three unserved objectives

Each needs either an element or a rewritten objective. Both are acceptable outcomes;
leaving the gap named and unaddressed is not.

- **`00`, XIP and the memory map.** The exercise already exists at `00:280-281` as an
  optional deeper path. **Promote it to the main path** as one progression step and one
  completion condition, or narrow the objective to drop "why the first call into a function
  can be slower than the second". Promoting is the better answer: the measurement is short,
  and it is the only place in the course where the learner meets flash-versus-SRAM cost.
- **`04`, interrupt entry mechanics.** Add a completion condition in the shape the lesson
  already uses elsewhere — the learner can say what the hardware stacked, where the vector
  came from, and why a handler is not a thread. This is a one-bullet change and lesson 04
  already has the Theory behind it at `04:66-98`.
- **`11`, why control plus interrupt.** Add a completion condition requiring the learner to
  say why a keyboard uses control and interrupt transfers and neither bulk nor isochronous.
  Lesson 11 has the material at `11:78-90` and the lesson is otherwise the strongest in its
  chapter; it scores 16 mostly because this half of its first objective goes unexercised.

### 5.3 Lesson 18 is two lessons — the strongest structural finding

`lessons/18-off-the-breadboard-and-done/LESSON.md` is **473 lines**, the longest in the
course against a main-path range of 283–473, and its own `## Purpose` names the seam:

> `18:23-26` — "Two things stand between the breadboard and the object. **Construction**…
> And **acceptance**…"

Construction (transcribing the layout, cutting tracks, soldering, strain relief, staged
bring-up) and acceptance (the twelve-item test list, the firmware-setup test, the soak test)
exercise different skills and have separable objectives. The natural split is after step 11,
"Fit the enclosure", and neither half's completion conditions break across it.

**Proposal:** split it, with `scripts/lesson.py`, so the ids and the `lessons` list stay
consistent — never by renaming files by hand.

```
python3 scripts/lesson.py add pico-ps2-usb-adapter \
    --id does-it-pass --title "Does it pass?" \
    --after lessons/18-off-the-breadboard-and-done/LESSON.md --folder --check
```

Then move the acceptance half into the new lesson and run
`python3 scripts/lesson.py renumber pico-ps2-usb-adapter --check` before applying. **Show
the author the `--check` output before applying either** — a renumber touches filenames,
slugs, ids, the `lessons` list and prose cross-references at once, and this bundle has
cross-references into lesson 18 from at least `15:118` and `12:344`.

This is a judgement call and the author may reasonably keep one long capstone. Eighteen is
the last lesson, a learner who reaches it is committed, and a single "finish the object"
arc has its own logic.

### 5.4 The watchdog is built and never verified on the finished object

Lesson 17 makes the learner configure the hardware watchdog with a justified period
(objective at `17:64-65`, persisted at `17:403-404`). Lesson 18's twelve-item acceptance
list at `18:254-268` never wedges the soldered adapter to confirm it self-recovers. Lesson
18's own prerequisites hedge it at `18:46-47` — "*several* acceptance tests below are lesson
17's behaviours performed on the finished object" — so this is a stated limitation and not
an oversight, but the effect is that the course's last defence is never tested on the object
it defends.

**Proposal:** one more acceptance item in lesson 18 — trigger the deliberate wedge from
lesson 17 on the finished adapter and confirm it returns without a replug. It costs a
sentence and closes the course's only build-it-then-never-check-it loop.

### 5.5 Smaller items

- **`04`, the components of interrupt latency.** Half-served, not charged (section 3). Add
  the enumeration to a completion condition if the author wants it exercised rather than
  read.
- **`16:324-325` bundles three actions** into one closing bullet: "Guard or remove the
  injected fault and the wedge, confirm the adapter works normally, and keep the marker."
  Split into three. It does not fail the closing-action row, because the completion
  conditions that follow are individually actionable, but a tutor handing this over as one
  next step is handing over three.
- **`a-safety-catch:195-197`** bundles two transition handlers and a verification into one
  bullet. Split. See the overturn note in section 2.
- **`nkro-without-a-driver:189-190`** fuses "decide" with "implement" in one bullet. Minor;
  the decision space is narrow because the mechanism is already given.
- **`07`, `N` is reused** for two unrelated things — the immediate operand of `set x, N` at
  `07:123` and the autopush threshold at `07:166`. Both are locally clear. Renaming one
  costs nothing and removes a reread.

---

## 6. The questions only a reader can answer

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

**None found**, across all twenty-six lessons. Every citation was checked against the
anchor's content and the question the lesson actually raises. The clearest positive case is
`15:162`, which cites `#wire-format` to answer precisely why the *device* and not the host
clocks a host-to-device write.

One thing worth recording rather than scoring: `DESIGN.md`'s `#pin-assignment` carries a
dated self-correction from earlier the same day, admitting that its original justification
for the GP2/GP3 adjacency — an `in pins, 1` claim about PIO addressing — was wrong. Lessons
07 and 08 teach the correct semantics and no lesson repeats the withdrawn claim. The anchor
and the lessons agree.

### 6.2 A lesson that introduces a type or concept nothing later uses

Two, both offered to the author as questions rather than findings.

- **`side-set`**, introduced at `07:113-114` and `07:218-219` as "it exists, it steals bits
  from the delay field, and it drives a clock line for free". No task in lesson 07 builds
  with it, and lessons 08 and 09 both use `set pindirs` instead. The lesson hedges it as
  "at least as 'it exists'", so this reads as deliberate awareness-only. **Is that worth the
  learner's attention here, or should it move to an optional deeper path?**
- **Flash persistence with XIP disabled**, named in `remap-and-macros:154-155` and taught at
  `:113-116`. The lesson then endorses compile-time configuration as "the right default",
  and the only exercise is in *Optional deeper paths* at `:251-252`. A learner who follows
  the lesson's own recommendation never uses the mechanic it taught them. **Keep the theory,
  or drop it to a pointer?**

### 6.3 A symbol or term a lesson uses and no lesson introduces

**None found — neither "bound only in `DESIGN.md`" nor "bound nowhere".** This was checked
hardest on the seventeen console log keys the course invents, because they are exactly the
kind of course-specific parameter the row exists to catch, and because a binding that lived
only in `DESIGN.md` would reach the tutor and never the learner. Every one is introduced in
a **lesson**, at or before its first use in a task:

| Key | Introduced | Key | Introduced |
|---|---|---|---|
| `alive` | `00:169` | `key` | `10:177` |
| `edges` | `04:274` | `report` | `13:167` |
| `frame` | `05` constraints | `held` | `14:142` |
| `resync` | `05:207` | `leds` | `15:207` |
| `queue` | `06:275` | `usb` | `17:180-187` |
| `pio` | `07:244` | `ps2` | `17:180-187` |
| `backend` | `08:146` | `safety` | `a-safety-catch:117-122` |
| `cpu` | `08:176` | `latency` | `measure-your-latency:157-159` |
| `tx` | `09:163` | | |

The scanner's other candidates were sorted by hand against the author's 2026-09-13 boundary
— a parameter of the concept being taught is owed to the learner; an identifier of the
language or platform they already chose is not — and rejected: `R0`, `R3`, `LR` and `PC`
are ARM architectural register names glossed in place; `-O0` is a GCC flag; `C`, `R` and
`RC` are each defined in the sentence that introduces them at `02:179`; `bool`-class tokens
belong to C. Two late-but-present bindings were noted and are not findings: `up`/`down` at
`10:159` appear about eighteen lines before the formal `key: down/up` convention at
`10:177`, inside the same Theory section.

### 6.4 Does the lesson equip the tutor to end a turn with one concrete action?

**Answered for every lesson in the section 2 table. All twenty-six pass**, one of them by
overturn (see the † note). No lesson ends on an open question or on a bare list of
deliverables, and the design decisions the course deliberately leaves to the learner are
kept out of the closing actions — checked hardest in lesson 18, where
`#deliberately-unresolved` puts two of them: the module-versus-discrete choice is made at
step 2 (`18:348-350`) and the vendor-interface consequence is merely confirmed at step 17
(`18:395-398`), leaving step 18 (`18:399-403`) as a decision-free capstone.

Two lessons carry compound bullets that are worth splitting anyway (`16:324-325`,
`a-safety-catch:195-197`); neither is the closing action, so neither fails this row. They
are in section 5.5.

### 6.5 A lesson far outside the course's usual size

**In both directions, and both are patterns rather than outliers.**

- **Lesson 18 at 473 lines** is the one lesson I judge to really be two. Section 5.3 has the
  proposal. Lesson 17 at 425 lines was considered and rejected as a split candidate: its
  four behaviours are the four bullets of one anchor, `#failure-posture`.
- **Every offered lesson is shorter than the shortest main-path lesson** — 238 to 291 lines
  against a main-path floor of 283. This is almost certainly deliberate, and correct: the
  bundle format warns that a detour costing more than the lesson it interrupts is a detour
  nobody finishes. Recorded because the rubric asks about both directions, not as a defect.

### 6.6 A must-cover topic that only an optional lesson teaches

**None found.** Every one of the 55 topics in `COURSE.md`'s coverage list maps to at least
one main-path lesson by content, not merely by word overlap. The four worth naming, because
an offered lesson also covers them and a careless reading would call them optional-only:

| Topic | Main-path home | The offered lesson deepens, it does not carry |
|---|---|---|
| logic analyser use; sample rate and triggering | `03` | `see-the-edges-on-a-scope` adds an oscilloscope |
| protocol offload and how to measure it | `08`, its `cpu:` lines | `measure-your-latency` compares *against* those numbers |
| USB enumeration | `11` | `watch-the-enumeration` shows the packets |
| rollover | `14`, six-key with `ErrorRollOver` | `nkro-without-a-driver` goes beyond six |

**One question for the author anyway.** NKRO beyond six keys lives only in the offered
lesson. `COURSE.md:228` already scopes it out explicitly under "Where this course stops"
— "NKRO beyond the optional lesson" — and the *required* topic, rollover, is fully taught on
the main path. So my reading is that the author has already answered this deliberately. It
is asked here because the rubric requires it to be asked, and it is worth one line of
confirmation: **is it acceptable that a learner who declines every offer never meets NKRO?**

### 6.7 Can a learner who declines every offer still finish this course?

**Yes.** Asked out loud because `optional_lessons` is declared, and answered from the
main-path lessons rather than from the manifest.

All nineteen main-path lessons were searched for references to all seven offered lesson ids.
Every hit is either a forward-reference in an *Optional deeper paths* section or an explicit
conditional. No main-path completion condition depends on anything an offered lesson builds
or explains, and no main-path prose assumes an offer was taken. The two strongest pieces of
evidence:

- `18:236` — "The acceptance test must pass either way, and if it passes with the second
  interface present, then the second interface is genuinely harmless."
- `13:40` — "If the learner took the offered `a-safety-catch` lesson…, it is worth having
  armed." Conditional, and the lesson proceeds without it.

`15:118-120` deserves a specific mention because it is the one place the wording could have
gone wrong and did not: it tells the learner the `instance` argument matters "until the
offered `a-second-interface-for-debugging` lesson adds a second interface", which requires
the code to be written correctly whether or not the offer is ever taken.

**`required_for` gates: none.** `tutorial.yaml`'s `optional_lessons` block was read in full;
every entry carries `offer_at` and `offer_because` and nothing else. No `anticipates`, no
`repair_in`, and `failure_modes` is not declared anywhere. So the rubric's −3-per-gate charge
does not apply, and its warning about not deleting a justified gate has nothing to attach to
here.

**Prose optionality was checked too**, since a lesson its own text calls optional while
sitting in `lessons:` would be a required lesson banking points nobody earns. All seven
optional lessons are in `optional_lessons`, all seven declare `optional: true` in their
frontmatter, and no main-path lesson describes itself as optional. The manifest and the
prose agree.

---

## What this audit did not do

It did not change the bundle. Every finding above is a proposal.

It did not run the course. No learner has taken it, no tutor has taught it, and the
completion conditions are judged as written rather than as they will behave. The eleven
`manual` validators in particular are judged only on whether a human could act on them.

It did not verify the supplied check scripts against real hardware. There is no Raspberry Pi
Pico, no ARM toolchain and no Model M on the machine this audit ran on. The scripts were
exercised by their author against a pty and fixtures; that is recorded in the bundle's own
history and is not a finding of this report.
