# Teaching the Toolkit About Optional Lessons — Design

**Date:** 2026-09-12
**Issue:** skomp/tutorail-authoring#1
**Status:** approved

---

## 1. What is actually missing

`optional_lessons` reached the bundle format after the toolkit was written. Three commands
were reported as not knowing about it. One of those reports was wrong, and correcting it is
most of this design's value.

| Command | State | This design |
|---|---|---|
| `index.py` | reads the field already | no change |
| `lesson.py add` | cannot create an optional lesson | a new `--optional` mode |
| `lesson.py renumber` | **already correct** | two tests, no code change |
| `promote.py` | cannot promote into the optional set | a new `--optional` mode |
| `catalog.py` | derives `scope` from the main path only | out of scope, issue #2 |

**`renumber` was reported as silently corrupting a course with optional lessons. It does
not.** `renumber_plan` iterates `bundle.listed`, the main-path `lessons` list, so a lesson
that list does not name is never renamed — its docstring already states that rule. Prose
references are rewritten through `bl.text_files(root)`, which walks every readable file in
the bundle, so a reference inside an optional lesson is rewritten like any other. The
original report counted references to `optional_lessons` in each file and drew a conclusion
from the count without reading the code. The count was real; the conclusion was not.

That leaves two features and one behaviour worth locking in.

## 2. The principle this follows

The toolkit writes bookkeeping. The interview supplies judgement. An `optional_lessons`
entry is both: the shape is bookkeeping, and `offer_at` and `offer_because` are judgement.

**The commands are run by the authoring skill, not typed by a person.** That single fact
decides the interface. A long argument list costs nothing when an agent composes it, and the
agent already holds the answers — it has just finished asking the author when this lesson
should be offered and why.

It also rules out a stub-with-placeholders design, which would otherwise be the obvious
match for how `add` writes a lesson body full of headings to fill in. **A placeholder is
safe for a human and dangerous for an agent.** A person editing a stub sees `TODO: say why`
and feels the itch. An agent that wrote it and moved on feels nothing, no check can see it,
and it ships. So nothing incomplete is ever written.

## 3. `lesson.py add --optional`

```
python3 scripts/lesson.py add <bundle> --id <slug> --title <text> --optional \
        --offer-at <lesson-id> --offer-because <text> \
        [--anticipates <failure-mode-id>] [--repair-in <lesson-id>] \
        [--required-for <lesson-id>] [--check] [--force]
```

**Required with `--optional`:** `--offer-at` and `--offer-because`. The command refuses
without them and says which is missing. `--position` and `--after` are refused in this mode:
an optional lesson has no position.

**Writes, as one atomic act:**

1. the lesson file at `lessons/<slug>.md` (or `lessons/<slug>/LESSON.md` with `--folder`),
   **with no number prefix**;
2. `optional: true` in that lesson's frontmatter;
3. the `optional_lessons` entry.

It never adds to the `lessons` list and never renumbers.

**Refusals, each with a positive control in the tests:** a missing `--offer-at` or
`--offer-because`; an `--offer-at` naming a lesson the bundle does not have; a `--id`
carrying a number prefix, because the format says an optional lesson has no position in the
main path's order; `--position` or `--after` combined with `--optional`; and every refusal
the non-optional `add` already makes.

**Atomicity is the sharpest edge.** Three writes must land together. A run that creates the
file and fails before the entry leaves a bundle the validator rejects, with the author's work
half-applied. `bl.Staged` exists for exactly this and must wrap all three, with a
`tree_digest` comparison in the tests proving a refused run leaves the bundle byte-identical.

### `--required-for` prints the rubric's warning

The owner settled on 2026-09-12 that `required_for` on an optional lesson **scores −3 and is
raised for review**: an author who writes it has declared something load-bearing and then
made it skippable, and that is usually wrong and sometimes correct.

The skill forbids hand-editing `tutorial.yaml`, so refusing a flag would leave no legitimate
way to set the field at all. The flag therefore exists, and using it prints the warning —
**quoting `skills/course-quality/references/rubric.md` verbatim rather than paraphrasing**,
so the two cannot drift.

This is the one place the toolkit carries an opinion instead of only bookkeeping. It earns
that because the command line is the only moment the warning reaches the author while they
are making the decision.

## 4. `promote.py --optional`

Promotion takes a lesson the tutor wrote for one learner and makes it part of the course.
Today it can only promote onto the main path, which needs a position.

With `--optional`, the offer metadata is **derived from the generated lesson's provenance and
confirmed by the author**:

| Field | Source |
|---|---|
| `offer_at` | the generated lesson's `after` |
| `offer_because` | the generated lesson's `reason` |

The derived values are printed and the command requires confirmation before writing,
matching the `--check`-then-apply discipline the rest of the toolkit uses.

**CORRECTION, 2026-09-12 — what "requires confirmation" turned out to mean.** This
sentence left the mechanism to the implementer, and a calling agent must not have to read
an implementation report to use the command. The mechanism is a second flag, `--confirm`,
not a prompt: these commands are run by the authoring skill, and a tty prompt would hang an
agent. Without `--confirm` and without `--check`, `promote.py --optional` prints both
derived values and **exits 2**, writing nothing — the non-zero exit is the confirmation
gate, not a failure, and it is non-zero precisely because exit 0 would read to an agent as
"done". `--confirm` is meaningless without `--optional` and is refused there. The same
contract is stated for callers in `skills/tutorail-authoring/SKILL.md`.

Deriving judgement from data is normally the wrong move. It is right here because the
provenance is the best evidence anyone will ever have about when the lesson is needed: a real
learner needed it at exactly that point, which is a stronger signal than an author's
recollection. Confirmation keeps the decision with the author.

Promotion strips the provenance fields, writes `optional: true`, adds the `optional_lessons`
entry, and does not renumber. The learner keeps their copy; promotion is a bundle-side act.

## 5. `renumber` — tests, not a fix

Two cases, each with a control that a main-path lesson in the same run behaves normally:

1. an optional lesson is **not** renamed by a renumber that renames main-path lessons;
2. a prose reference to a renamed main-path lesson, sitting **inside** an optional lesson
   file, **is** rewritten.

Both must be shown failing against a deliberately broken `renumber_plan` before they are
believed, or they prove nothing.

## 6. Reuse

Writing an `optional_lessons` entry is the same YAML block surgery as `supplies:`.
`bundlelib` gained `emit_scalar`, `render_supplies_item` and `add_supplies` earlier today,
including a round-trip guard that parses the written text back and raises when it does not
match. An `add_optional_lesson` sibling reuses `emit_scalar` and that guard.

Do not grow a second way to write YAML. `emit_scalar` already carries a measured quoting
rule — it was widened after a review found 2082 values in a 20455-value corpus that this
project's own reader accepted and a standards-compliant parser rejected.

## 7. Out of scope

- `catalog.py`'s `scope` line, which counts the main path only. Issue #2.
- Any change to `index.py`, which already handles the field.
- Any change to the runner or the bundle format. This is toolkit-only.
