# The course-quality rubric

Print this table with every report. A reader who can see the rubric argues with the
scoring; a reader given only a number argues with the number, or worse, believes it.

## What a score is for

A score makes a judgement **legible and comparable across a long course**. It does not
replace the judgement. Nothing in this file is computed by a script: `audit.py` gathers
evidence and refuses to rule, and every figure below comes from someone who opened the
lessons and decided.

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
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing |
| **unserved objective** | −3 | a stated objective or `DESIGN.md` anchor that no task exercises — counted once per course, not per lesson |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised — see below (course-level) |

A lesson's score is the sum of its own elements. The course score is the sum of the
lessons minus the two course-level gap penalties. The gap penalties are counted
separately and shown separately; they are never folded into a lesson's figure.

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
at risk.

## Dynamic evidence is evidence, not a verdict

A dry-run harness that walks a course can report that a lesson **stalled**. Cite a stall
as **evidence, never as a verdict**, and say in the report which it is.

A stall cannot distinguish an unsatisfiable completion condition from a learner having a
bad day. The two look identical from outside: the lesson did not complete. One is a
defect in the course and one is a Tuesday. The ruling stays with whoever reads the lesson
and the transcript, and the report says what the harness observed, not what it concluded.

The same applies in the other direction: a course every dry run finished is not thereby a
course that teaches. It is a course nothing got stuck in.
