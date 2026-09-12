# TODO

Deferred work for tutorail-authoring.

---

## Bundle quality checker — BEING BUILT ELSEWHERE, 2026-09-12

**Do not build this.** It exists as `skills/course-quality/`, with the design at
`docs/superpowers/specs/2026-09-12-toil-and-course-quality-design.md` section 9 and
`skills/course-quality/scripts/audit.py` producing the evidence the skill judges.

This entry originally said "build a checker". It is kept, rewritten, because the reasoning
below is what the tool has to keep being, and because a later session reading a stale
"build a checker" note would build a second one.

### Why it is separate from the validator

`validate_bundle.py` answers one question: can a runner execute this bundle? A pass means
"structurally well-formed", never "good course". Its checks must stay **binary**, because
the runner uses it as a gate at materialization.

Course quality is not binary, and **no quality finding may ever reject a bundle.** Two tools
disagreeing about whether a bundle is acceptable would be worse than either alone.

It is authoring-time only: it runs when someone writes a course, never when someone takes
one.

### Settled since this entry was written

- **A score is never reported alone.** A single number invites gaming and hides which signal
  fired, so the breakdown is mandatory: every element carries its own figure, its
  `file:line`, and the sentence it scored. A report that prints only the number is defective.
- **No signal ever becomes an error**, while the validator is the gate.
- **Both automatic and on request**: the authoring skill runs the audit before delivering,
  and the checker also stands alone when an author asks to evaluate a course.
- Already implemented there: the coverage-list signal, and the completion-conditions signal
  as a reader-answered row citing the dry-run harness as evidence rather than verdict.

### The `required_for` signal — settled 2026-09-12

**Both: it scores negatively AND it is raised for review.** Not either.

Robert ruled this directly when the course-quality session asked him. The -3 stands
unconditionally and is visible in the total; every instance is also raised as a question the
author answers.

The objection that argued against scoring survives, because it was a good objection — a
score alone teaches authors to delete a gate that is doing its job. It does not get to cancel
the instruction, so it becomes required text printed beside the score:

> This gate cost the course 3 points and may still be correct. If the lesson genuinely
> cannot be completed while its failure stands, the gate is doing its job — say so and keep
> it. Do not delete a gate to improve a score. A course that drops a justified gate lets a
> learner finish a lesson whose failure is still standing, which is worse than the toil this
> rubric hunts.

An author may record the gate as justified. The score stands anyway and the justification
stands beside it, because a rubric a reader can argue down to zero stops being comparable
across courses.

Recorded here second-hand, relayed by the session that asked. Correct it if that is not what
you meant.

### Signals not yet implemented

Candidates, not decisions. None is mechanically decidable, so each would be a
reader-answered row:

- a lesson that introduces a type or concept nothing later uses
- an optional lesson anticipating a failure mode no lesson repairs
- lessons far outside the course's usual size
