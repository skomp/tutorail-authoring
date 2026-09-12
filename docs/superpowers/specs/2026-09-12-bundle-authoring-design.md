# Bundle Authoring and Maintenance — Design

**Date:** 2026-09-12
**Status:** Approved design, pending implementation plan
**Repository:** `skomp/tutorail-authoring`

---

## 1. Purpose

Give a course author a skill that interviews them until it knows enough to build or change
a tutorial bundle correctly, over a small toolkit that performs the mechanical edits.

Two problems this solves.

**Authoring by hand gets the mechanics wrong.** A bundle has invariants a person does not
hold in their head: `id` equals the lesson slug, the `lessons` list is the authoritative
order, `design_refs` must resolve, provenance fields must be stripped on promotion. Every
one of those has already been got wrong once during this project, by a model and by me.

**A wrong course arc is discovered too late.** Writing twenty lesson files and then finding
the sequence is wrong is expensive. An interview that ends in an approved spec makes the
arc reviewable before any lesson exists.

---

## 2. Relationship to the other repositories

| Repository | Holds | This project |
|---|---|---|
| `tutorAIl` | the runner plugin, the bundle format contract, `validate_bundle.py` | **depends on it** |
| `tutorail-bundles` | the bundles, and their course specs | **writes into it** |
| `tutorail-authoring` | this: the authoring skill and its toolkit | — |

**The dependency on the runner is real and stated.** `validate_bundle.py` stays in
`tutorAIl` and this project invokes it. It is not duplicated here.

That decision was reconsidered and confirmed. The validator looks like authoring-only
tooling, and the first instinct was to move it here — but the runner has a legitimate use
that was designed and never wired up: the protocol forbids improvising around a broken
bundle and requires reporting it, and the moment to catch a broken bundle is
**materialization**, before a learner starts, not at lesson 7 when a `design_ref` dangles.
A second, weaker validator here would be the false-oracle pattern this project has already
been bitten by twice.

Consequence: an author needs both plugins installed. Anyone authoring a tutorial almost
certainly runs tutorials, so the cost is near zero, and the README states it plainly.

---

## 3. One skill, two entry paths

Not two skills. Claude Code skill directories are flat, so two skills cannot share a
`references/` folder without cross-directory paths neither host documents. Create and
modify share the format knowledge, the index, the validator call and the house style. One
skill branching on *does this bundle already exist* is the same shape as the runner
branching on *is there an active instance*.

The `description` carries both trigger sets: create a tutorial, write a course, author a
bundle, add a lesson, restructure a course, change a tutorial.

Splitting later is cheap. Un-duplicating two reference trees is not.

---

## 4. The course spec artifact

The interview ends by writing a course spec the author reviews and approves. Only then are
bundle files generated. This mirrors brainstorming exactly, for the same reason: revising
one document beats revising twenty lesson files.

**Location: `specs/<bundle-id>.md` in the repository that holds the bundle** — for the
current work, `tutorail-bundles`. With the course, not with the tooling, and **outside** the
bundle directory so it is not shipped to learners who have no use for the author's design
rationale.

---

## 5. The interview

### It classifies scale first

A three-lesson introduction and a twenty-three-lesson course need different interviews. The
first question establishes which, and a short course is never asked about milestone
structure or a coverage list it does not need. This is brainstorming's three-path ratchet
applied to courses.

### Five phases

| Phase | Extracts | Feeds |
|---|---|---|
| Subject and learner | what they build, what they already know | `title`, `description`, `subjects`, `level`, prerequisites |
| The arc | end state, first task, milestones between | `COURSE.md` chapter map, `lessons` order |
| Teaching stance | who writes the code, whether it builds software, how work is checked | `workspace_kind`, `ownership_policy`, `validators`, `solution_code` |
| Durable decisions | what later lessons depend on, what is deliberately unresolved | `DESIGN.md` and its anchors |
| Coverage | topics the course must reach even if the project does not naturally get there | the coverage list |

### It never asks what it can propose

`aliases`, `style`, `bundle_format` and the validator names are suggested from the answers
and confirmed, not interrogated. Forty questions where six would do is how an interview
becomes something an author avoids.

### The confidence gate is checkable, not a feeling

Before presenting the draft spec, the skill self-checks it:

- every field the format requires has an answer or a defensible default
- every lesson's completion conditions depend only on what **earlier** lessons built
- every `DESIGN.md` anchor a lesson will need exists in the design decisions
- no lesson introduces a type or concept that nothing later uses

The middle two are significant beyond tidiness: **they are the same defects the dry-run
harness would find, caught at authoring time for free.** The harness finds them by walking
a course for hours. The spec self-review finds a subset by reading one document. It is a
cheap first filter, not a replacement.

### Modify runs the same machinery from the other end

It starts from the generated index, asks what is wrong rather than what the author wants,
and its distinguishing job is surfacing knock-on effects: *renaming the `key-ordering`
anchor affects lessons 05, 07, 09 and 11*. That question is unanswerable without the index.

---

## 6. Context strategy for modify

AutomatonDB is 23 lessons and roughly 2,700 lines. An interview about restructuring one
chapter must not begin by loading the course.

`index.py` generates a compact index mechanically from the manifest and lesson frontmatter:
id, title, form, `design_refs`, `validators`, one-line purpose. Roughly 40 lines for a
23-lesson course. The skill loads the index, interviews the author, then opens only the
lessons it will actually touch.

This is the same progressive-disclosure trick the runner already proves works, and it
reuses the validator's lesson discovery rather than reimplementing it.

---

## 7. The toolkit

| Script | Contract |
|---|---|
| `index.py` | Bundle → compact index. Reads frontmatter only, never lesson bodies. |
| `lesson.py add` | Creates single-file or foldered form; frontmatter `id` equals slug; inserts into `lessons` at the requested position. |
| `lesson.py renumber` | Renames files and folders to consistent numbering; rewrites `id`s, the `lessons` list, and prose cross-references (see §9). |
| `promote.py` | The ten-step instance-to-bundle procedure, including re-checking `design_refs` against the **bundle's** `DESIGN.md`. Does not delete the learner's copy. |
| `catalog.py` | Scans a bundles repository, reads each manifest, emits `catalog.yaml` with relative paths. Derives `scope` from the lesson count. |

`catalog.py` earns its place immediately: the multi-catalogue work expects a bundles
repository to ship a `catalog.yaml` listing its bundles by relative path, and maintaining
that by hand beside twenty bundles is the drift this toolkit exists to prevent.

Stdlib only. These run at authoring time on a developer machine, but there is no reason to
add dependencies the runner does not have.

---

## 8. Safety properties for mutating operations

These scripts differ from the validator in the way that drives their design: **they mutate
bundles.** The validator is read-only and its worst failure is a wrong verdict.
`renumber` can silently corrupt a 23-lesson course.

Every mutating operation therefore:

1. **runs the validator afterwards and fails loudly if it left the bundle invalid.** The
   bundle is either better or untouched, never broken and reported as done.
2. **supports `--check`**, printing what it would do without doing it.
3. **refuses to run on a dirty working tree** unless forced, so `git diff` is always a
   clean record of what the tool did.

A failed operation must leave the bundle unchanged rather than half-edited. This is a
tested property, not an intention.

---

## 9. Known hazard: prose cross-references

Lesson files reference other lessons **by id, in prose**. AutomatonDB's lesson 03 lists
`Prerequisites: 02-typed-keys-table-hierarchy`.

Renumbering rewrites filenames, slugs, `id`s and the manifest, and leaves those prose
references pointing at ids that no longer exist. **The validator would not catch it:**
`design_refs` and `validators` are checked, a prerequisite named in prose is not.

**`renumber` rewrites them.** Refusing instead was considered and rejected: nearly every
lesson lists prerequisites, so a renumber that refuses whenever prose references exist would
refuse almost always and be useless.

It rewrites only **exact whole-token matches of ids it is itself renaming**, never a
substring and never an id it does not own, and it **reports every rewrite** so the change is
reviewable in `git diff` rather than silent. Anything that looks like a reference but does
not match an id being renamed is reported and left alone.

There is a case for the validator learning to check that prerequisite ids resolve, which
would make this class of breakage catchable rather than merely handled. That is a change to
`tutorAIl`, recorded here as a candidate rather than assumed.

---

## 10. Testing standard

The standard already set by this project:

- a fixture per operation, and **every failure shown firing**; a check that can only be
  shown passing is a false oracle
- for mutating operations, a proof that a failed run leaves the bundle unchanged
- fixtures must not depend on platform-specific filesystem behaviour. A fixture that
  renamed `LESSON.md` to `lesson.md` silently tested nothing on a case-insensitive
  filesystem, and that mistake has already been made once here.

---

## 11. Packaging

A plugin, the same shape as the runner: `.claude-plugin/` for Claude Code, and a Codex
marketplace manifest once the runner's Codex distribution problem is solved. Until then the
Codex install is a symlink into `~/.agents/skills/`, as the runner's is.

---

## 12. Non-goals

Not a course-content generator that writes lessons unattended. The interview produces a
spec the author approves; the author remains the teacher.

Not a replacement for the dry-run harness. The spec self-review catches a subset of
sequencing defects statically. Only walking the course finds the rest.

Not a bundle registry, a publishing pipeline, or a marketplace.

---

## 13. Open decisions

1. **Format migration** (`bundle_format` 1 → 2) is out of scope until a version 2 exists.
   The toolkit should not grow a migration framework speculatively.
2. **Whether the validator gains a prerequisite-id check** (§9). A change to `tutorAIl`.
3. ~~**Whether `scaffold` is a script at all.**~~ **Settled 2026-09-12: no.** The skill
   writes the four root files and the empty `lessons/` directory itself, because that
   content is judgement, and `lesson.py add` creates every lesson, because that is
   bookkeeping. `add` was made to work on a bundle that has no lessons yet, which is what
   makes the bootstrap possible.
