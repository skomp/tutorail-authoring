# TODO

Deferred work for tutorail-authoring.

---

## Bundle quality checker — 2026-09-12

Build a checker that **scores** a bundle, separate from the runner's validator, which
**rejects** one.

### Why it is separate

`validate_bundle.py` answers one question: can a runner execute this bundle? It says so
itself on every run — a pass means "structurally well-formed", never "good course". Its
checks must stay binary, because the runner uses it as a gate at materialization.

Course quality is not binary. A bundle can be perfectly valid and still teach badly. Those
findings must not reject a bundle, so they need their own tool and their own vocabulary.

It belongs here rather than in the runner: it runs when someone writes a course, never when
someone takes one.

### The first signal, which motivated this

**`required_for` on an optional lesson scores negatively.** An author who writes it has
declared something load-bearing and then made it skippable. The format permits it and the
runner copes — it teaches the repair inline when a learner who declined meets the gate — but
the course is usually better with that material on the main path.

### Other signals worth considering

These are candidates, not decisions:

- a lesson whose completion conditions cannot be met by what earlier lessons built
- a `design_refs` entry that does not answer the question its lesson raises
- a lesson that introduces a type or concept nothing later uses
- a course with no coverage list, which loses the gap-versus-difficulty test
- an optional lesson that anticipates a failure mode no lesson repairs
- lessons far outside the course's usual size

The first three are the same defects the dry-run harness finds by walking a course. A static
checker finds a subset cheaply. It does not replace the harness.

### Open questions

1. What a score means. A single number invites gaming and hides which signal fired. A list
   of findings with severities may be all that is needed, and "score" may be the wrong word.
2. Whether any signal ever becomes an error. It must not, while the validator is the gate —
   two tools disagreeing about whether a bundle is acceptable is worse than either alone.
3. Whether the authoring skill runs it automatically after generating a bundle, or only when
   asked.
