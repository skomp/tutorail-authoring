# Course quality: `cpp-png-inspector`

**Run:** 2026-09-29. **Bundle:** `skomp/tutorail-bundles`, branch `worktree-cpp-png-inspector`
(unpushed at the time of the audit), at commit `3a5fa34`.
**Rubric:** `skills/course-quality/references/rubric.md`, repository source, as at 2026-09-29.

`validate_bundle.py` returns `PASS - every applicable check ran and found nothing`, exit 0.
That says the bundle is well formed. It says nothing about whether the course teaches, which
is what follows.

**Totals are comparable against this course's own lessons only.** A lesson's figure tracks
how finely its `## Suggested progression` enumerates clauses, and this course writes long
progressions. Do not set this total beside another bundle's.

---

## 1. The course and its total

| | |
|---|---|
| Bundle | `cpp-png-inspector` — C++ for C Programmers: Build a PNG Inspector |
| Main-path lessons | 13 |
| Optional lessons | 2 |
| Sum of the fifteen lessons | **377** |
| Unserved objectives | 2 × −3 = **−6** |
| `required_for` gates on optional lessons | 0 × −3 = **0** |
| **Course total** | **371** |

Arithmetic, visible:

```
  22  00-write-the-c-walker
  29  01-not-a-superset
  20  02-where-the-leaks-are
  30  03-a-class-that-cleans-up
  26  04-a-target-of-its-own
  34  05-the-rule-of-three
  45  06-moving-not-copying
  17  07-bounds-you-cannot-skip
  26  08-templates-eat-the-macros
  28  09-errors-without-errno
  33  10-chunks-without-switch
  21  11-the-finished-tool
  17  12-it-was-in-the-box
  17  reading-a-template-error          (optional)
  12  what-the-compiler-writes-for-you  (optional)
 ---
 377  sum of lessons
  -3  unserved objective: 04:33, the data-file path
  -3  unserved objective: 11:40, where the tool's scope ends
 ---
 371  course total
```

### Two decomposition rulings, stated so they can be reversed uniformly

Both change the total materially, and both were applied to every lesson.

**Articulation conditions.** This course's completion conditions are largely "the learner
can state / say / explain X". They sit between the rubric's teaching and evidence rows.
The ruling applied: **+2 when the condition requires an account of the learner's own code or
decision, or a causal or counterfactual argument; 0 when it is recall of a fact the lesson
already stated.** So `06:294` ("the rule of five, and that declaring a destructor in
`03-a-class-that-cleans-up` had already removed the implicit moves") scores 2, and `11:259`
("state the CRC's byte range exactly") scores 0.

**Multi-clause bullets are scored as one element.** Several bullets carry three to six acts
in one sentence — `00:264-265`, `01:229-233`, `07:231`, `11:218`. Each is scored once. The
alternative, scoring per clause, would raise the total substantially and is defensible; it
is not what was done. `01:229-233` alone is the difference between +2 and +6.

---

## 2. The per-lesson table

Closing action is the rubric's reader-answered row. It is not a score and is never added
into one. Every lesson is answered, with no blanks.

| Lesson | Score | Objectives served | Toil | Closing action |
|---|---|---|---|---|
| `00-write-the-c-walker` | 22 | O1–O5 all served | **1 site, −2** | pass |
| `01-not-a-superset` | 29 | O1–O6 all served | none | pass |
| `02-where-the-leaks-are` | 20 | O1–O5 all served | none | **fail** |
| `03-a-class-that-cleans-up` | 30 | O1–O6 all served; O5 has no completion condition | none | pass |
| `04-a-target-of-its-own` | 26 | O1–O5 served; **O6 unserved** | none | pass |
| `05-the-rule-of-three` | 34 | O1–O6 served, four of them only inside one branch | none | pass |
| `06-moving-not-copying` | 45 | O1–O7 all served | none | pass |
| `07-bounds-you-cannot-skip` | 17 | O1–O6 all served | none | pass |
| `08-templates-eat-the-macros` | 26 | O1–O5 all served | none | pass |
| `09-errors-without-errno` | 28 | O1–O6 all served | none | pass |
| `10-chunks-without-switch` | 33 | O1–O6 all served | none | pass |
| `11-the-finished-tool` | 21 | O1–O5 served; **O6 unserved** | none | pass |
| `12-it-was-in-the-box` | 17 | O1–O6 all served; O5 by one recall condition only | none | pass |
| `reading-a-template-error` (opt) | 17 | O1–O5 served; O4 weakly | none | pass |
| `what-the-compiler-writes-for-you` (opt) | 12 | O1–O6 served; O4 weakly | none | pass |

No lesson scores at or below zero.

### Element breakdown for the lessons whose figure is not obvious from the row

**`00-write-the-c-walker` — 22.** Progression 16, completion 6. The only toil site in the
course sits here and costs −2; without it the lesson scores 24. Teaching elements:
`:255-257` (work out the three output lines by hand before writing code), `:264-265`,
`:267`, `:271`, `:271-274` (predict 13, not 218103808), `:276-277`, `:277-278` (decide what
stops the loop), `:278-279`, and three completion articulations at `:297-298`, `:299-303`,
`:304-305`. Practice: `:265`, `:281`. Everything else is evidence at 0.

**`02-where-the-leaks-are` — 20.** Progression 14, completion 6. The lowest main-path
figure in the first chapter, and the reason is visible in the coverage row rather than the
score: it exercises exactly one `COURSE.md` must-cover topic. It earns its place
structurally — `DESIGN.md:30-31` makes it the evidence for five later lessons, and
`02:107-113` argues that a leak detector which has never fired is untrustworthy — but on
the must-cover ledger it is the thinnest lesson in the course.

**`07-bounds-you-cannot-skip` — 17.** Progression 15, completion 2. Low for a lesson
carrying six objectives and two distinct subjects. The cause is entirely the second
ruling above: five of its six completion conditions are validator readings at 0, and its
middle progression paragraph `:225-234` packs at least eight acts into ten lines, scored as
four elements. Scored per clause this lesson would roughly double. The density is the
finding, not the number.

**`11-the-finished-tool` — 21.** Progression 19, completion 2. Nine of its ten completion
conditions are observed behaviour or recall. The `crc32.hpp` hand-over is correct and costs
nothing — see section 4.

**`12-it-was-in-the-box` — 17.** Progression 11, completion 6. The arrival lesson is
mostly mechanical by design: `12:62` calls the replacements mechanical in its own voice,
and the teaching is concentrated in four elements — `:277` (sort each break into the three
categories), `:283` (the virtual-destructor experiment), `:287` (decide where the offset
lives), `:296` (write the sentence this lesson is for, once per replacement).

**`what-the-compiler-writes-for-you` — 12.** The lowest figure in the course, and
appropriate: it is a 218-line offered detour with five progression elements, all five of
them teaching. Nothing is wrong here.

---

## 3. Goal gaps

Two, at −3 each, −6 in total. Both were established by enumerating every element in the
lesson and finding none, not by reading the objective's wording.

**`lessons/04-a-target-of-its-own.md:33` — "Give a test the path to a data file without
depending on the directory it was run from."** Servers found: **zero**. The theory teaches
it at `04:155-163` and then excuses the learner from it in the same breath, at `04:161-163`:
"A test that only exercises the buffer with bytes it made up itself avoids the question
entirely, and is a perfectly good first test." The progression's only test instruction,
`04:240-244`, is exactly that excused test — "construct one, check that its length is what
you gave it and its bytes are what you put in" — with no data file and no path. No
completion condition at `:260-274` mentions a data path, `WORKING_DIRECTORY` or
`${CMAKE_CURRENT_SOURCE_DIR}`.

**`lessons/11-the-finished-tool/LESSON.md:40` — "Say where the tool's scope ends, and why
`IDAT` is walked past rather than decoded."** Servers found: **zero**. It is taught in prose
at `11:158-165`, named in `## Concepts to teach` at `11:181` and constrained at
`11:200-201`, but no progression step and no completion condition asks the learner to say it.
Grepping `11:210-266` for `scope`, `IDAT`, `decode` and `decompress` returns nothing.

### Judged and NOT charged, with the reasoning

**`DESIGN.md#json-output` — served.** The anchor's own text reads "**Deliberately
unresolved.** … no lesson depends on the answer." What it asks for is that the question be
raised and any decision recorded, and two lessons do exactly that: `11:292-294` invites the
learner to argue it, and `12:329` instructs that a proposed second output mode be recorded
against it. Charging a course for not resolving an anchor that declares itself unresolved
would be perverse.

**The other nine anchors — all served.** `#whole-file-in-memory`, `#the-allocation-counter`,
`#owning-and-borrowing`, `#errors-are-values`, `#byte-order-in-one-place`,
`#chunk-data-vs-chunk-handlers`, `#handwritten-then-replaced`, `#the-output-contract` and
`#idat-is-out-of-scope` are each honoured by what at least one lesson makes the learner do.
This was judged on lesson behaviour, not on `design_refs` — which in this bundle would give
badly wrong answers in both directions. See section 6.

**`COURSE.md:187` "exception safety, and what RAII has to do with it" — served, partly; not
charged.** The entry is conjunctive and one conjunct is exercised hard: the learner builds
the unwinding experiment at `09:235`, builds the control at `09:237`, and it is a completion
condition at `09:254`. The other conjunct — the three guarantees at `09:148-151` — is named
and then withdrawn in the lesson's own words: "Those names are worth having; the course does
not examine them further." A conjunctive topic with one conjunct exercised is not unserved.
It is raised as a proposal in section 5 instead.

**`reading-a-template-error:44` (bisect a wall down to one question) and
`what-the-compiler-writes-for-you:43` (use `= delete` deliberately) — served weakly; not
charged.** Each is served by a recall condition plus one oblique element — `RTE:198` adds a
`static_assert` and reintroduces case two to see what the error looks like afterwards, which
is bisection in miniature; `WCW:177-179` writes `= default` as shape 3. Both are raised as
questions in section 6 rather than scored.

---

## 4. The toil inventory

**One confirmed site in the whole course.**

`lessons/00-write-the-c-walker.md:259-260`, the exact sentence:

> "Build the skeleton first: `CMakeLists.txt`, a `src/` with a `main` that prints its
> argument and exits, then `cmake -S . -B build` and `cmake --build build`."

**−2.** This is the rubric's project-skeleton tiebreak. Both tests point the same way here,
so the tiebreak is not even needed:

- **Shippability.** The course is single-language, so one skeleton covers every learner it
  claims to support. The bundle already ships `supplies/gitignore`, so the channel exists
  and is in use. It could have shipped a `CMakeLists.txt` and did not.
- **The sole-server exception does not fire.** Objective `00:43-44` ("Write a minimal
  `CMakeLists.txt` for a C executable, and configure and build it out of source as two
  separate steps") has **six** servers, enumerated: `:259-260`, `:262`, `:292`, `:293`,
  `:297`, `:297-298`. The rubric's operational test asks whether the setup step is the only
  element serving the objective that names it. It is one of six, so the skeleton is a part
  of a larger goal and not the goal.
- **No decision is left in it.** `00:199` says "Your `CMakeLists.txt` needs three commands
  and is about eight lines long", and `:203-206` fixes the target name. Deterministic and
  unambiguous on the plain test too.
- **The tutor route is closed.** `tutorial.yaml:35-40` lists `CMakeLists.txt` under
  `learner_owned` with `ownership_policy: tutor-must-not-edit-learner-owned`, so guard 2 of
  the hand-over test fails: an unmodified runner assigns this to the learner.

The objective is conjunctive ("write … *and* configure and build …"), the shape the rubric
says is almost never sole-served. It is not sole-served here. Recorded so a reader can see
the check was made rather than assumed.

### Candidates examined and rejected

**All seventeen `audit.py` toil candidates are false positives**, and every one was opened.
Nine are prose about C++ copy semantics rather than assigned work: `05:95`, `05:131` (twice),
`05:205`, `05:207`, `06:47`, `06:172` (twice), `07:101`, `07:256`, `10:19`, `12:65`,
`what-the-compiler-writes-for-you:182` (twice). Two are real progression elements that the
`copy`/`move` pattern caught by coincidence — `05:243` ("construct a buffer, copy it, let
both go out of scope, and check the counter's allocations") and `03:35` ("Move the allocation
counter from `malloc`/`free` to `operator new`/`operator delete`") — and both are the
learner exercising a C++ mechanism, not copying a file. `12:239` is a topic list.

**Rejected because the bundle could not have supplied the result** — worth naming as such,
because it is a different rejection:

- Every "break your own code on purpose" step: `04:249`, `05:263`, `06:255`, `08:209`,
  `10:265`, `12:283`, `RTE:170-174`. The file being broken is the learner's own, written in
  an earlier lesson, and the bundle has never seen it. There is no `supplies:` entry to
  write.
- `01:214-215`, the C→C++17 edit to a `CMakeLists.txt` the learner wrote in lesson 00. Same
  reason.

**Rejected because the hand-over already happened, and what remains is teaching:**

`lessons/11-the-finished-tool/` supplies `crc32.hpp` to `src/crc32.hpp`, lesson-scoped,
declared in three places: the lesson's own `supplies:` block at `11:6-9`, the lesson text at
`11:99-103`, and constraint `11:195`. Writing a CRC32 "teaches bit manipulation, not C++",
and the bundle ships it. What remains for the learner is the byte range, and that is not
toil: `11:105-117` makes it a decision, and `11:119-127` records that a wrong answer produces
a characteristic misleading symptom — "*every* chunk in *every* file fails … It reads like a
broken CRC implementation and it is not." A mistake there teaches a great deal. Scored
**teaching, +2** at `11:227` and `11:229`. This is the supplies mechanism working exactly as
intended, and it is the best example of it in the catalogue.

**The scanner is a candidate generator, and its silence is evidence about the pattern rather
than about the course.** This inventory came from opening all fifteen lessons, not from the
candidate list. The one confirmed toil site, `00:259-260`, **was not flagged by the scanner
at all** — no pattern fired on "Build the skeleton first". That is the clearest possible
demonstration of why an empty candidate list is not a pass.

---

## 5. Proposals

Each is a concrete action. All are proposals the author may refuse; nothing in this report
has changed the bundle.

### P1 — Declare the project skeleton as a supply (the toil charge)

```
python3 scripts/supplies.py add <bundle> \
  --from supplies/skeleton/CMakeLists.txt \
  --to CMakeLists.txt \
  --describe "A three-command CMakeLists.txt for a C executable named pngdump. Configuring and building it, and knowing why the build directory is separate, is still yours" \
  --check
```

The file does not exist in the bundle yet, so the fix is two steps: add
`supplies/skeleton/CMakeLists.txt` with the eight lines `00:199-206` already specifies, then
declare it. Prose to delete from `00:259-260`: the clause "`CMakeLists.txt`, a `src/` with a
`main` that prints its argument and exits, then", leaving the sentence to begin at "Build the
skeleton first: `cmake -S . -B build` and `cmake --build build`."

**Do not remove the two-step configure-and-build act** — `:262`, `:292`, `:293`, `:297` and
`:297-298` all serve objective `00:43-44` and four of them survive this change, so the
objective keeps five servers and costs no −3. **The objective's first clause must be
reworded** in the same change, because "Write a minimal `CMakeLists.txt`" stops being true.
Suggested: "Read a minimal `CMakeLists.txt` for a C executable, and configure and build it
out of source as two separate steps."

A counter-argument the author may prefer: `COURSE.md:163` makes the CMake build a must-cover
topic and `00:179-206` teaches it at length, so an author could hold that the setup is the
subject here. The rubric forecloses that route explicitly — "an objective that merely names
the setup is not enough" — and the sole-server count is six. The charge stands, and the
author may still decide the eight lines are worth writing by hand. If so, record the reason;
this report will otherwise re-raise it next run.

### P2 — Lesson 04's data-path objective (−3)

Two acceptable outcomes; the author picks one.

**Either** give it a server. `04:157-161` already names the two mechanisms. One progression
sentence after `04:244` would do it: have the test read `assets/basic.png` through a path
passed by `add_test`, and add a completion condition that the suite passes when CTest is
invoked from a different working directory.

**Or** drop `04:33` from the objective list and let `04:155-163` stand as background. That is
a coherent choice — `04:161-163` already argues the made-up-bytes test is "a perfectly good
first test" — but the objective cannot stay while nothing serves it.

### P3 — Lesson 11's scope objective (−3)

`11:40` is the cheapest of the two to repair. The lesson already teaches it at `11:158-165`.
Add one completion condition alongside `11:263`:

> The learner can say where the tool's scope ends, and why `IDAT` is listed by offset and
> size and never decompressed.

That is one line, and it converts a taught-but-unexercised objective into a served one.

### P4 — The `read_u16` that the course requires and never asks for

`00:112-113` says: "Write yourself small helpers for a 32-bit and an 8-bit read". **Two.**
Lesson 08 requires three, in four places: `08:13` ("Look at `read_u32`, `read_u16` and
`read_u8`"), `08:46` (its instructive failure turns on getting "`read_u32` right and
`read_u16` subtly" wrong), `08:188` and completion condition `08:229` ("No
`read_u32`/`read_u16`/`read_u8` function or macro remains in the source"). `COURSE.md:29`
states the premise as "four functions that differ only by a type".

PNG chunk framing has no 16-bit field — length, type and CRC are four bytes each — so a
learner who follows `00:112-113` literally never writes `read_u16`, arrives at lesson 08 with
a weakened motivation, and meets a completion condition naming a function that does not
exist. Repair is one clause in `00:112-113`, plus reconciling `COURSE.md:29`'s "four" with
lesson 08's three.

### P5 — Two contradictions in lesson 11's machinery

**`src/crc32.hpp`: the lesson states the ownership wrongly. The manifest is correct.**

> **Correction, 2026-09-29, after this report was first published.** The paragraph here
> originally read that the file was "classed both ways", that the manifest forbids the tutor
> to touch a file the lesson calls the course's, and that "one of the two is wrong, and the
> manifest is what a runner reads." **That was wrong about the manifest**, and anyone who
> read the first version should discard the proposed repair. `bundle-format.md`, section
> "The ownership exemption", settles it: under
> `ownership_policy: tutor-must-not-edit-learner-owned` the tutor MAY **create** a declared
> supplies target that does not exist even where it falls under a `learner_owned` glob, and
> MAY **never modify** one that does. So `src/**` covering `src/crc32.hpp` is correct and
> intended, the supplies declaration grants exactly the create permission the course needs,
> and there is no manifest defect. The finding below is what remains of it.

`11:278` says "Note that `src/crc32.hpp` is supplied and not learner-owned". **That clause is
false.** `tutorial.yaml:36` lists `src/**` under `learner_owned:`, so the file *is*
learner-owned — correctly, per the exemption above. What is true is the course rule rather
than the manifest classification: the file is supplied, the learner must not edit it, and the
tutor may place it but never modify it.

`11:26-27` ("It is supplied and is not yours to edit") and `11:195-196` ("supplied and must
not be edited, replaced or reimplemented") are both addressed to the learner and are **true
as written**. Only `11:278` needs rewording, and the manifest must not change.

**Lesson 11 asserts the allocation balance and checks it with nothing.** Constraint
`11:204-205` requires "the allocation report still prints at exit and still balances", but
`11:5` declares `[build, tests, dumps-basic-png, reads-text-metadata, detects-bad-crc,
rejects-truncated]` and none of those six reads the report — `dump.sh` compares the chunk
listing, the `error:` line and the exit status, and `error-path.sh` is the only script that
reads `outstanding:`. Lesson 10 carries `no-leak-on-error-path` and lesson 12 now does too, so
lesson 11 is the one gap in the 10→11→12 chain, and it is the lesson that adds a new handler
class and a new error path. Lesson 12's prerequisite at `12:26-27` then assumes the balance
held. Adding `no-leak-on-error-path` to `11:5` closes it for one word, exactly as it did for
lesson 12.

### P6 — Lesson 07 requires a validator it does not declare

`07:5` is `[build, tests, rejects-truncated]`; completion condition `07:248-250` requires
`dumps-basic-png` and says so in its own text: "run it even though this lesson does not list
it, because a bounds check that rejects valid files is the commonest way to pass the
truncation check for the wrong reason." The reason is sound and the condition should stay.
A runner driving off `validators:` will not run it, so add `dumps-basic-png` to `07:5`.

### P7 — Three factual slips

- `00:13` — "This is the longest lesson in the course". It is 329 lines; `12-it-was-in-the-box.md`
  is 345 and `06-moving-not-copying.md` is 332. Either reword to "one of the longest" or drop
  the claim; a learner can check it.
- `07:181` — "says the file is good to byte 95 and broken after". Byte 95 does not exist:
  `truncated.png` is 95 bytes, so the last index is 94, which `07:51` states correctly ("The
  file stops at byte 94"). One word.
- `COURSE.md:151-159` — the Milestones table has five unlabelled rows, and `11:276` and
  `12:332` refer to "milestone M4" and "milestone M5". `M1`, `M2` and `M3` appear nowhere in
  the bundle. Either label the table's rows M1–M5 or drop the labels from the two lessons.

### P8 — The "exception safety" half of `COURSE.md:187`

Not charged, but worth closing. Either give the guarantees one task — the `noexcept` move
from lesson 06 is a nothrow-guarantee example sitting unused three lessons earlier, and
`09:146` already connects them — or narrow the coverage entry to what the course actually
does, which is the RAII half. As it stands `09:148-151` names three concepts and withdraws
them in the next sentence.

### P9 — `what-the-compiler-writes-for-you` cites an anchor nothing in it honours

`WCW:4` declares `design_refs: [owning-and-borrowing]`. That anchor decides that one type
owns bytes and everything else borrows through a non-owning view. The lesson is about the six
special member functions, and its progression never makes the learner borrow anything. The
anchor it does honour — `#the-allocation-counter`, the instrument at `WCW:183-185` and the
argument at `WCW:139-143` — is not cited. Swap them.

---

## 6. The questions only a reader can answer

### A `design_refs` entry that does not answer the question its lesson raises

**Four found**, and one systemic observation that matters more than any of them.

- **`what-the-compiler-writes-for-you:4`, `owning-and-borrowing`** — the clearest instance.
  See P9. A learner who follows it does not find out why their buffer has no move constructor.
- **`04-a-target-of-its-own:4`, `owning-and-borrowing`** — lesson 04 raises the target graph,
  usage requirements, the ODR and how CTest decides a test passed. The anchor answers none of
  them, and the lesson's own text cites a different anchor, `#handwritten-then-replaced`, at
  `04:215`. Aggravating: `DESIGN.md` has **no anchor at all** for the build, the target graph
  or the test harness, so there is nothing correct for lesson 04 to cite. The repair is
  probably a new anchor rather than a swapped citation.
- **`01-not-a-superset:4`, `whole-file-in-memory`** — the constraint at `01:196-199` forbids
  `std::vector` and cites this anchor. The question raised is "why am I forbidden
  `std::vector` now?", and the anchor answers a different one (why the tool buffers rather
  than streams). `#handwritten-then-replaced` answers it, at `DESIGN.md:114-132`, and is not
  cited here. Counter-reading: the sentence supplies its own answer inline, so the anchor is
  doing supporting rather than answering work.
- **`09-errors-without-errno:272`** — a mis-attribution in the persist section rather than in
  `design_refs`: "Note whether the unwinding test is in the suite, since it is the evidence
  for `#owning-and-borrowing`". The unwinding test demonstrates that a destructor runs during
  stack unwinding; `#owning-and-borrowing` is about owners and views and says nothing about
  exceptions. The evidence belongs to `#the-allocation-counter`.

**The systemic observation: `design_refs` is close to useless as a coverage index in this
bundle, in both directions.** Across the fifteen lessons, anchors honoured but not cited
outnumber anchors cited by a wide margin — lesson 11 honours five uncited anchors, lesson 12
five, lesson 06 three, lesson 07 three, lesson 04 three. `#chunk-data-vs-chunk-handlers` is
the strongest honour in lesson 11 (constraints `11:191-194` keep CRC validation out of the
handlers) and is cited nowhere in it. Anyone who scores the unserved-anchor row mechanically
off `design_refs` will get this course badly wrong. The rubric already rules that an anchor is
served by what lessons **do**; this bundle is the strongest evidence yet for that rule. It is
not a defect and costs nothing — but it is worth the author deciding whether `design_refs` is
meant to be complete, because right now it is not.

### A lesson that introduces a type or concept nothing later uses

**Found, in three tiers.**

Real, in the sense that a named objective or a full section is spent on something the course
abandons:

- **`01:142-148` and objective `01:32` — `auto`.** A full paragraph, a named learning
  objective, and one progression act at `01:233`. **Zero** uses in lessons 04–12. The only
  later hit is `09:123` "every **auto**matic object", a substring.
- **`01:89-95` — `enum class`.** Introduced in full with the int-conversion contrast. Zero
  later uses. The lesson concedes it at `:94-95`: "worth knowing exists even if your program
  has no use for one yet."
- **`04:104` — `target_compile_features`.** Introduced and contrasted with
  `CMAKE_CXX_STANDARD`, then never used or required. Related: `04:28`/`04:87` `INTERFACE`,
  one third of a named objective's keyword triple, never used — lesson 08 puts a template in a
  header, the one natural place for an interface library, and does not.
- **`04:149` — `assert` / `NDEBUG`.** `NDEBUG` appears nowhere else in the bundle.
- **`08:105-109` — `static_assert`.** Zero uses in lessons 09–12; the only later uses are in
  the **optional** `reading-a-template-error`. A learner who declines meets it once.
- **`09:148-151` — the three exception-safety guarantees.** See P8. The lesson admits it.
- **`02:73-76` — `realloc`**, with a decision the learner must "be able to defend". Zero
  later uses.
- **`12:82` — iterators, range-based `for`, the standard algorithms.** Named as reasons
  `std::vector` interoperates, in a course that has taught none of them. See the next row.
- **`WCW:116-123` — the Rule of Zero.** Introduced, named, applied once at `WCW:186`, and
  never again. Its payoff exists on the main path at `12:275-277`, which deletes the
  hand-written buffer — and lesson 12 never names the rule. Worth the author's eye: the
  optional lesson teaches the principle and the main path performs it without knowing.

Terminal by design, and not findings: lesson 03's `destroy()` anti-pattern (introduced to be
disproved, and disproved in the same lesson); `std::shared_ptr` at `12:197-209`, which
`COURSE.md:199` explicitly budgets at "one paragraph in lesson 12"; `std::expected` at
`12:149-152`, named because C++17 cannot provide it; `08:138` explicit instantiation,
explicitly set aside.

**None found** in lessons 00, 05, 06, 07, 10, 11 that survives scrutiny.

### A symbol or term a lesson uses and no lesson introduces

The two categories the rubric names, kept separate, plus two the rubric does not name and
which this bundle needs.

**Bound nowhere** — first use given:

| First use | Symbol |
|---|---|
| `00:103` | the strict aliasing rule — glossed by consequence, never stated |
| `01:110` | translation unit — reused at `02:61`, `02:144`, `RTE:74` |
| `02:60-61` | internal linkage — carries a real instruction the learner cannot act on |
| `03:165` | `std::cout` — never introduced; the course prints with `printf` throughout |
| `05:55` | **`Buffer`** — the identifier the course then uses as if bound, across lessons 05, 06, 07 and 09. Lesson 03 uses `Widget` for its illustrative class and `03:273` has the learner **name** the type themselves. No lesson ever says "we will write `Buffer` for whatever you called it." |
| `06:212` | `NRVO` — its only occurrence in the bundle; the mechanism is described at `06:66-69` and the name never attached |
| `08:62` | **`View`** — appears exactly once in the bundle, in the signature that defines lesson 08's subject. Lesson 07 creates the view and deliberately leaves naming to the learner (`07:263`). Same defect as `Buffer`, same one-sentence repair, and the repair belongs in lesson 07. |
| `08:130` | **mangled name** — `08:130` tells the learner that "recognising it on sight is worth as much as anything else in this lesson", and the lesson never shows one, never says what mangling is, and never says how to demangle. The only explanation is `RTE:87-91`, which is optional. The sharpest instance in the course. |
| `10:109` | `Chunk` — the identifier; the five fields are described eight lines earlier at `10:44`, and no lesson ever has the learner build a type by that name |
| `11:276`, `12:332` | `M4`, `M5` — see P7 |
| `12:82` | iterators, range-based `for`, the standard algorithms |
| `12:88` | `std::out_of_range` — lesson 09 teaches `throw`/`catch` and names no standard exception type |
| `12:77` | amortised constant time |
| `WCW:216` | triviality |

**Bound only in `DESIGN.md`** — the category the rubric singles out, because the runner loads
an anchor for the tutor and not for the learner:

- **`03:204` — "a view" (the non-owning view).** Bound at `DESIGN.md:53-58`, under
  `#owning-and-borrowing`, which **is** this lesson's `design_refs` entry — so the tutor has
  the definition and the learner does not. No lesson introduces the term until lesson 07.
  Repair is a move: restate the one-line meaning at `03:204`, or drop the parenthetical.

**Only one instance in the whole bundle**, which is a good result.

**Two categories the rubric does not name, raised for a ruling.** Both recur often enough
that scoring them either way changes the picture, and neither is covered by the existing
split.

1. **Bound in a supplied, learner-facing file.** `IHDR`, `IDAT`, `IEND`, `tEXt`, `CRC`,
   `gAMA`, `pHYs` and the chunk framing are all bound in `supplies/PNG-FORMAT.md`, which is
   placed in the learner's workspace before lesson 00 and which `00:29-30` and `11:27-28`
   direct the learner to read. That is not "introduced in a lesson", and it is nothing like a
   `DESIGN.md`-only binding — the learner can read it. **Recommendation: this should count as
   bound.** A course that ships a reference page and tells the learner to read it has
   introduced the terms in it. Without a ruling, every such term is a finding and the row
   becomes noise.
2. **Bound only in a main-path lesson's `## Optional deeper paths`.** `mangling` is explained
   only at `01:276`, inside a section the learner may never reach, and is then used
   load-bearingly at `08:130`. **Recommendation: this should NOT count as bound**, for the
   same reason `required_for` is scored — material the learner can decline is not material the
   course can rely on.

**A third case, which is the mirror of the completability invariant rather than an instance of
this row.** `what-the-compiler-writes-for-you` is offered at lesson 05 (`tutorial.yaml:135-136`)
and uses three terms bound only in later main-path lessons: `rvalue` (`WCW:95`, `WCW:184`;
bound `06:86-95`), `overload resolution` (`WCW:96`; bound `06:155`) and `static_assert`
(`WCW:129`, load-bearing at `WCW:181`; bound `08:105-110`). Declining the offer costs the
learner nothing; **accepting it at the point the manifest makes it costs three unbound terms.**
The completability invariant protects the decliner and nothing in the format protects the
accepter. `tutorial.yaml:137` and `WCW:33-34` both argue for the lesson-05 offer point on good
grounds, so the repair is to bind the three terms in the lesson's own `## Theory`, not to move
the offer.

### Does the lesson equip the tutor to end a turn with one concrete action?

Answered for every lesson in the section 2 table. **Fourteen pass; one fails.**

**`02-where-the-leaks-are` — FAIL.** Condition 1 passes: `02:175-176` names a written
artifact, `02:179-180` names code to write, `02:191` names a validator. Condition 2 fails.
The final paragraph of `## Suggested progression` is:

> `02:198-201` — "C's `atexit` registers a function to run when the program exits normally,
> which is one answer; a single exit point that all the error paths funnel to is another; and
> the answer the course is heading towards is that scope exit should be doing this work for
> you, which is next lesson."

A three-way design question, unresolved, sitting where the closing action belongs, with the
third option explicitly unavailable until the next lesson, and not marked as a decision. The
counter-reading: it is conditional, opening at `02:197-198` with "If placing the report on
every path turns out to be awkward", so on a clean run the tutor never reaches it. That
counter-reading is weak here, because the lesson's own `02:92-96` and `02:185-189` treat "the
report does not print on the failing path" as the *expected* outcome — `02:187-189` calls it
"the most instructive of the three". The tutor will reach that paragraph in most runs.

**`11-the-finished-tool` — PASS, against the reading first proposed.** `11:237` ("Decide what
each kind of problem does to the walk and to the exit status, and make the two consistent")
welds a decision to its dependent action in one bullet, and the lesson does not say to split
it. That is a real weakness and it is recorded. It does not fail the row: the rubric's second
condition is that the decision be kept **out of the closing action**, and `11:237` is
mid-progression — the closing action is `11:242-243`, a six-validator sweep with no decision
in it.

**Weaknesses recorded on lessons that pass.** Multi-action closing or near-closing sentences
at `05:261`, `08:213`, `09:241`, `10:274-278` and `12:275-277`, and the dense
eight-act paragraph at `07:225-234`. Lesson 07 is the closest of the fourteen to a fail, and
for a second reason: its one real design decision — which of the two out-of-range shapes to
adopt, set up properly at `07:90-95` — never appears in the progression as a decision. Its
only trace is the half-clause at `07:227-229`, "so the test names the behaviour you chose
rather than the one you assumed", which presumes a choice the progression never asks the
learner to make. Compare `05:246` and `06:262`, which both mark their decision in its own
sentence. A reader who graded condition 2 on any bullet rather than on the closing action
would fail lesson 07 and lesson 11 as well as lesson 02.

**One course-level property, reported once rather than fifteen times.** Every lesson ends with
an `## Optional deeper paths` section, several of which raise open questions —
`07:276-277`, `11:292-294`, `12:339`, `12:343-345` — and **no lesson anywhere in the bundle
states that the section does not close a turn.** Grepping all fifteen files plus `COURSE.md`
and `DESIGN.md` for that assurance returns nothing. This is the rubric's second closing-action
failure property, and it is this course's house style rather than any lesson's lapse. One
sentence in `COURSE.md`, or in the runner's contract, would settle it for all fifteen.

### A lesson far outside the course's usual size

**None.** Measured, in lines:

```
218  what-the-compiler-writes-for-you (opt)   298  03-a-class-that-cleans-up
231  reading-a-template-error (opt)           304  04-a-target-of-its-own
245  02-where-the-leaks-are                   318  05-the-rule-of-three
262  08-templates-eat-the-macros              326  10-chunks-without-switch
278  07-bounds-you-cannot-skip                329  00-write-the-c-walker
281  01-not-a-superset                        332  06-moving-not-copying
287  09-errors-without-errno                  345  12-it-was-in-the-box
294  11-the-finished-tool
```

Main path runs 245–345, a 100-line spread with no gaps and no outlier. The two optional
lessons are the two shortest, which is right for offered detours. `12-it-was-in-the-box` is
the largest at 345 and is structurally justified — it makes five distinct type replacements —
so it is not a split candidate. `02-where-the-leaks-are` is the shortest main-path lesson at
245; its thinness shows in the coverage ledger rather than in its length, and it is discussed
in section 2.

### A must-cover topic that only an optional lesson teaches

**One, and it is a genuine question rather than a defect.**

**`COURSE.md:182` "reading a template error message".** `COURSE.md:149` glosses it as "How to
read a two-hundred-line template error and find the one line that matters."

The main path covers the **link-time** kind, and covers it well: `08:116-140` explains it,
`08:209-214` walks the learner into it deliberately, and completion condition `08:238` grades
it. But a link error has no instantiation chain and, as `RTE:91-92` points out, no line number
at all. The skill the topic is named after — reading a wall of instantiation output, knowing
which end to start from, cutting it down — exists **only** in the optional
`reading-a-template-error`: `RTE:99-121` (including `RTE:109`, "**the first line of the output
is not the mistake in either compiler**"), `RTE:123-138`, `RTE:182-195`, and its completion
conditions at `RTE:210-213`. No main-path lesson makes the learner read an instantiation chain.

**Put to the author, as the rubric requires:** *a learner who declines the offer at lesson 08
meets the undefined-symbol failure, diagnoses it and repairs it — and never sees a
two-hundred-line instantiation error, never learns which end to read, and never learns to cut
one down. Is that acceptable for this course?*

Two facts bear on the answer. `08:248-250` shows the author already thinking about the
decliner at exactly this point: "Note whether the learner took `reading-a-template-error` …
since a learner who never saw it will need the explanation repeated when a class template
arrives in `09-errors-without-errno`." And `09:31` puts a **class** template in the learner's
hands, which is where the first real wall is most likely to arrive — after the offer has been
declined. This is a question and not a score, permanently.

**Two adjacent topics checked and found NOT at risk:**

- **`COURSE.md:175` `= delete` and `= default`** — fully main-path. `= delete` is taught at
  `05:165-192`, exercised at `05:255-259`, named in objective `05:33` and graded at `05:286`.
  `= default` is written by the learner at `10:155-159` (`virtual ~Handler() = default;`) and
  required by completion `10:287`. One caveat: `05:255` is the *else* branch of a learner
  choice, so a learner who chooses a deep copy exercises `= delete` only through theory and
  the completion condition.
- **`COURSE.md:174` the special member functions the compiler writes for you** — substantially
  main-path. Objective `05:26` has the learner predict what the generated copy does and confirm
  it with the counter; `06:175-182` teaches the suppression rule and `06:294` grades it;
  `09:109-113` makes the learner apply it to a new type. What lives **only** in the optional
  lesson is the *systematic* form: the enumeration of all six (`WCW:53-57`), the full
  suppression table (`WCW:71-80`), and the Rule of Zero by name. A declining learner meets five
  of the six by construction and never sees them enumerated. That is defensible — the course's
  method (`COURSE.md:23`, "No feature is introduced before you have been hurt by its absence")
  argues against a systematic enumeration on the main path, and this is exactly the material an
  offered detour should carry.

### `required_for` gates

**None.** `grep -rn "required_for"` over the bundle returns exactly one hit, in `SPEC.md:70`,
which is prose recording the deliberate absence: "No `required_for` gate: the tutor can …".
The `optional_lessons:` key is present at `tutorial.yaml:133` and was read directly rather
than inferred from `optional_lesson_count`.

**0 × −3 = 0**, and the rubric's warning paragraph is deliberately not printed, because there
is no gate to justify and none to mistakenly delete.

Worth saying positively rather than recording a zero: the design that makes a gate unnecessary
is visible and deliberate. `reading-a-template-error` declares `anticipates:
template-definition-in-a-cpp-file` and `repair_in: lessons/08-templates-eat-the-macros.md` —
the repair is on the **main path**, and `08:209-214` induces and repairs the failure for every
learner. The optional lesson is the deeper explanation of a failure the main path already
handles. That is exactly the shape a gate exists to avoid needing.

### The completability invariant

> **Can a learner who declines every offer still finish this course?**

**Yes.** Answered from the main-path lessons, checking the prose as well as the manifest.

**No main-path completion condition depends on anything only an optional lesson builds or
explains.** The three that come closest each have a main-path binding:

- `06:294` (the destructor removed the implicit moves) is taught on the main path at
  `06:175-182`, in that lesson's own theory. `WCW` is named at `06:181` as an extra, not as
  the source.
- `09:262` (which special member makes `Result<Buffer>` returnable) is bound at `09:105-113`.
- `08:238` (describe the link error) is both explained at `08:116-140` and performed at
  `08:209-214`.

Lessons 11 and 12 contain no reference of any kind to either optional lesson.

**No main-path prose assumes an offer was taken.** All five mentions are explicitly
conditional — `05:160` ("if you want the whole picture rather than the part you need today"),
`05:301`, `06:181` ("if you want it"), `08:254` — and one asserts the invariant outright:
`08:142`, "**It is optional and this lesson finishes without it.**"

**Both optional lessons assert it from their own side:** `RTE:27` ("nothing on the main path
depends on it") and `WCW:33` ("the course is completable without it").

**And the main path plans for the refusal**, which is the strongest evidence and the thing no
mechanical check could see. `08:248-250` instructs that `STATE.md` record whether the learner
took the offer and whether the failure actually happened, "since a learner who never saw it
will need the explanation repeated when a class template arrives in `09-errors-without-errno`."

**Prose optionality was checked too.** No lesson in `lessons:` calls itself optional in its own
text; the two optional lessons are in `optional_lessons:` where they belong, and
`tutorial.yaml:133` declares them. The manifest and the prose agree, so there is no second
total to report.

---

## Where this leaves the course

A 371 with one toil site in fifteen lessons, two unserved objectives, no `required_for` gates,
a completability invariant that holds and is planned for, and no lesson at or below zero. The
teaching machinery is in good order: predictions before evidence throughout, deliberate
breakage as a method, and completion conditions that mostly ask the learner to account for
their own code rather than recite.

The findings worth acting on first are not the score. They are **P4** (a function three
lessons require and one lesson never asks for), **P5** (a false ownership claim in one
lesson's prose, and an assertion nothing checks), and the `Buffer`/`View`/mangled-name group
in section 6 — three one-sentence repairs that between them remove the course's most likely
"the tutor used a word I have never seen" moments.
