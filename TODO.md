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

### One signal still open — needs Robert

**`required_for` on an optional lesson.** Robert asked for it to score **negatively**: an
author who writes it has declared something load-bearing and then made it skippable.

The session building the gate objected that scoring it down unconditionally would teach
authors to **delete a gate that is doing its job**, and implemented it as *raise for review*
instead.

Both are defensible and they are not the same thing. Unresolved; Robert's call.

### Signals not yet implemented

Candidates, not decisions. None is mechanically decidable, so each would be a
reader-answered row:

- a lesson that introduces a type or concept nothing later uses
- an optional lesson anticipating a failure mode no lesson repairs
- lessons far outside the course's usual size
