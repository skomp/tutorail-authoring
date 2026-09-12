---
name: course-quality
description: Evaluate the quality of a bundle, score a course, does this tutorial teach, audit a course, find the toil in a course, review a tutorial against its learning goals. Scores a tutorAIl bundle lesson by lesson against a teaching rubric - what teaches, what is practice, what is only evidence, and what is toil the bundle should hand over instead of assigning - and reports the objectives and DESIGN.md anchors no lesson exercises. Use this when someone asks how good a course is, whether a tutorial actually teaches, where its busywork is, or whether it covers what it claims. It proposes and never changes a bundle; applying a proposal goes back through the tutorail-authoring skill and its toolkit.
---

# Course quality

You are auditing a course for what it **teaches**, which is a different question from
whether it is well formed. A bundle can be structurally perfect and teach almost nothing.

The verdict is yours, from the lessons. A script gathers the evidence and refuses to rule,
because the parts of this that a script can decide are not the parts that matter.

## Three rules about this skill itself

**It proposes and never changes a bundle.** Every finding leaves this skill as a proposal
the author can accept or reject. Applying one goes back through the `tutorail-authoring`
skill and its toolkit, after the author says yes. An audit that quietly repaired the thing
it was measuring would have destroyed the measurement and the author's ownership of the
course in one move.

**An empty candidate list is not a pass.** The toil scanner in `audit.py` is a candidate
generator over a fixed list of verbs. It cannot see toil it has no pattern for, and it
fires on prose that is not toil at all. Its silence is evidence about the pattern, not
about the course. The score comes from opening the lessons.

**A green validator is not a good course.** Structural validity and teaching quality are
different questions. The validator answers "is this a bundle?"; this skill answers "does
this teach?". That is why the two live apart, and it is why "the validator passes" is
never an answer to anything in this report.

## Orient

1. Establish which bundle is under audit and confirm the path with the author.
2. Collect the evidence: `python3 scripts/audit.py <bundle>`.
3. Open the lessons — all of them. This is the part that produces the score.
4. Load `references/rubric.md` before scoring anything, and print it in the report — the
   scored table **and** the rows it does not score.
5. Report in the five sections below. Propose. Stop.

Do not change a file at any point in that sequence.

## The evidence script

`scripts/audit.py` ships with this skill, in this skill's own `scripts/` directory, and
the paths below are relative to it. It is stdlib-only Python 3, and it reaches across to
the `tutorail-authoring` skill's `scripts/bundlelib.py` for bundle loading, so both skills
must be installed — they ship in one plugin, so they are. If the command is not found,
the working directory is somewhere else: locate `audit.py` inside the installed plugin and
use that path. Do not reimplement what it does because you could not find it.

| Command | Gives you |
|---|---|
| `python3 scripts/audit.py <bundle>` | a Markdown evidence skeleton: course id and lesson counts, the `COURSE.md` coverage list with candidate lesson matches per topic, the lesson list, candidate toil sites as `file:line` with the whole line, every declared `supplies:` entry with its scope, and the `DESIGN.md` anchor names |
| `python3 scripts/audit.py <bundle> --json` | the same data as one JSON object — `course`, `coverage_list`, `anchors`, `lessons`, `supplies`, `candidates`, `topic_candidates`, `notes` |

Those are the only two forms. There is no `--score` and no `--fix`; the script computes no
score and changes nothing.

What each `lessons` entry carries: `rel`, `id`, `title`, `optional`, `form`, `design_refs`,
`validators`, `learning_objectives`. Each `candidates` entry carries `rel`, `line`, `text`
and `pattern` (which verb fired).

`text` is **one physical line, not one sentence.** Lesson prose is hard-wrapped, and both
of the real toil sites in the corpus are: `00-project-setup/LESSON.md:34` ends in a comma,
mid-clause. The report asks for the exact sentence, so open the lesson and take the
sentence — the `text` field tells you where it starts, not where it ends.

### What the script does not give you, and you must fetch yourself

- **`required_for`, `anticipates` and `repair_in` are not in its output.** The `−3` row of
  the rubric needs them, so open `tutorial.yaml` and work through its `optional_lessons`
  block yourself. Key that off **the presence of an `optional_lessons:` key in the
  manifest**, never off `optional_lesson_count`: that count is of optional lessons found
  **on disk**, so an `optional_lessons` entry naming a file that does not exist counts
  zero. Trusting the count there would tell you not to look at precisely the manifest most
  likely to be wrong, and the `required_for` row could never fire.
- **`--json` reports `optional` per lesson, and nothing about why.** A lesson being
  optional is not a finding. An optional lesson carrying a gate is.
- **The lesson rows do not sum to `lesson_count`.** `lesson_count` counts the main path
  only; the rows cover main-path and optional lessons together, each flagged. On
  `durable-event-broker` the header reads "15 lesson(s), 3 optional" above a table of 18
  rows. The script dropped nothing. The toil scan covers all 18.
- **The coverage list may be absent.** The script returns `coverage_list: null` and says so
  in prose, and that absence is itself a finding: the course has declared no boundary.

### Both candidate lists are candidates

The script says this about itself in its own output, and the report must repeat it.

- **Toil candidates contain false positives, and the `pattern` field says only which verb
  fired.** A candidate is a line where one of a fixed set of verbs sat in an imperative
  position. Whether the learner learns anything from that line is not a thing the pattern
  can see. On `webgl-typescript-scene`, `lessons/00-project-setup/LESSON.md:42` reads
  "Install dependencies, inspect each supplied file, type-check, build, start the
  development server" — one clause of that is toil and the rest is the lesson. Quote the
  sentence, split it if it needs splitting, and decide. Never carry a candidate into the
  report as a finding without having opened the line.
- **Topic matches are word overlap, not coverage.** A topic with candidate lessons may
  still go untaught, and a topic with no candidate may be taught throughout under
  different words. The list is a place to look, not an answer.

## Scoring

The rubric is in `references/rubric.md`. Load it, apply it per element, and print it in
the report so the author can argue with the scoring rather than with a number.

**The rubric is more than its scored table.** It also carries three rows a reader answers
and a scored table cannot reach, and one course-level invariant no structural check can
reach. Those are not optional reading and they are not footnotes: section 6 of the report
is where each of them is answered in writing.

Work lesson by lesson, and within a lesson, element by element: each task, each step, each
completion condition. Give every element its own score, its `file:line` and the sentence
it scored. A lesson's figure is the visible sum of its own elements.

The course-level penalties are counted and shown separately, never folded into a lesson's
figure. **An unserved objective or anchor costs −3 each**, not −3 for the fact of having
gaps: a course owing twelve topics is not the same course as one owing one, and a rubric
for comparing courses must not score them alike. A `required_for` gate on an optional
lesson costs −3 per gate.

**Never report the total alone.** A report that prints the number without the inventory
underneath it is defective; the rubric explains why at length.

## The report

Six sections, in this order. The first five are the ones the design spec names. The sixth
exists because the two obligations that only a reader can discharge belong to none of the
other five, and an obligation with no home in the template is an obligation nobody
performs.

**1. The course and its total.** Bundle id, title, lesson count, optional lesson count,
and the total with its arithmetic visible: the sum of the lessons, then each course-level
gap penalty subtracted by name.

**2. The per-lesson table.** One row per lesson: lesson, score, objectives served, toil
found. Below the table, the element breakdown for any lesson whose figure is not obvious
from its row — and for every lesson scoring at or below zero, without exception.

**3. Goal gaps.** Every stated learning objective and every `DESIGN.md` anchor that no
lesson exercises, listed one per line with its −3. State how you decided each one, because
`topic_candidates` does not decide it. The penalty is per gap, so this list and the
arithmetic in section 1 must agree: *n* gaps listed, −3*n* subtracted.

**4. The toil inventory.** Every confirmed site with its `file:line` and **the exact
sentence**, quoted. Separately and briefly: which script candidates you examined and
rejected, so the next reader does not re-litigate them. Then state plainly that the
scanner is a candidate generator and that this inventory came from the lessons.

**5. Proposals.** See below.

**6. The questions only a reader can answer.** Every one of them answered in writing.
Silence is not an answer here, and neither is "nothing found" with nothing underneath it.
None of these is scored; all of them change what the author does next.

- **Each of the rubric's three reader-answered rows**, answered explicitly, with a
  `file:line` for every instance found and an explicit "none found" where none was:
  - a `design_refs` entry that does not answer the question its lesson raises;
  - a lesson that introduces a type or concept nothing later uses;
  - a lesson far outside the course's usual size, in either direction.
- **The completability invariant, asked out loud**, for any course that declares
  `optional_lessons`:

  > Can a learner who declines every offer still finish this course?

  Answer it from the main-path lessons: does any main-path completion condition depend on
  something only an optional lesson builds or explains, and does any main-path lesson's
  prose assume the learner took an offer? `bundle-format.md` section 13 states this as an
  authoring obligation precisely because **no mechanical check can reach it** — a
  validator walking the main path sees nothing wrong, and a runner too old to know about
  `optional_lessons` never makes the offer at all. A rubric a person reads is the only
  place it is ever asked.

  For a course with no optional lessons, "not applicable — no optional lessons declared"
  is a complete and acceptable written answer. Leaving the question out is not.

A proposal in section 5 may answer one of these, in which case say so and cite it. What is
not allowed is a report with five tidy sections that never asked.

Where a dry-run harness has walked the course and reports a stalled lesson, cite the stall
as evidence and label it as evidence. It cannot distinguish an unsatisfiable completion
condition from a learner having a bad day, and the ruling stays with whoever reads it.

## Proposals

Every proposal names a **concrete action**, not a sentiment. "Lesson 04 could be tighter"
is not a proposal.

**A toil span** becomes the command that declares the files plus the prose to delete:

```
python3 scripts/supplies.py add <bundle> --from <bundle-relative-path> --to <workspace-relative-path> --describe <text> [--lesson <lesson-id>] --check
```

The two paths have **different roots**. `--from` is relative to the bundle root — where the
files live in the course. `--to` is relative to the learner's workspace root, and `.` is
that root itself. Quoting a workspace path as `--from` is the easiest way to get this
wrong.

`supplies.py` belongs to the `tutorail-authoring` toolkit, not to this skill, so that
path is relative to **that** skill's directory and running it is that skill's job. Quote
the command with `--check` so the author sees the plan before anything changes, and name the
lines of prose that come out of the lesson once the files are declared. A toil span
removed without the supplies entry leaves the learner without the files.

**An unserved objective** becomes either a lesson proposal — where it sits, what it
teaches, which anchor it cites — or an argued case that the objective should be dropped
from `COURSE.md`. Both are acceptable outcomes. Leaving the gap named and unaddressed is
not.

**A lesson scoring at or below zero** becomes a question for the author about what it is
for. Not a deletion proposal: a lesson that scores badly may be load-bearing for a reason
the rubric cannot see, and the author knows what it is. Ask, quote the elements that
produced the figure, and let them answer.

**A `required_for` gate on an optional lesson** becomes the rubric's warning, printed
beside the score, and a question. The gate may well be correct. The score stands anyway.

## When something is wrong

- **The author asks you to apply a proposal** — that is the `tutorail-authoring` skill's
  work, not this one's. Hand the proposal over; do not change the bundle here.
- **`audit.py` fails to load the bundle** — put its message in front of the author. A
  bundle the loader rejects is usually a bundle the validator also rejects, and repairing
  it is a separate job with a separate skill.
- **The validator is green and the course is bad** — that is the expected case, and it is
  what this skill is for. Say both plainly in the report.
- **A file changes under you and you cannot account for it** — say so and ask. It is
  almost certainly the author working. Do not revert it, stash it or discard it.

## Tone

Score the course, not the author. Every finding carries a `file:line` and a sentence so
the author can check it, and every one of them is a proposal they may refuse. A number
nobody can argue with is a number nobody should believe.
