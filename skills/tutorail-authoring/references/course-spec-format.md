# The course spec

**Status:** normative. Load this when you are about to write or revise
`specs/<bundle-id>.md`, and when you self-check it before presenting.

A course spec is the artifact the author approves **before any bundle file exists**. It is
the whole reason the interview ends where it does: revising one document beats revising
twenty lesson files, and an arc that is wrong is only cheap to fix while it is still a
list.

---

## 1. Where it lives, and why it is not in the bundle

```
tutorail-bundles/
├── catalog.yaml
├── specs/
│   └── rust-automaton-db.md        the course spec
└── rust-automaton-db/              the bundle
    ├── tutorial.yaml
    └── ...
```

**In the repository that holds the bundle, at `specs/<bundle-id>.md`, outside the bundle
directory.** Two reasons, and both matter:

- **With the course, not with the tooling.** The spec describes one course. It belongs
  beside that course, so a fork of the bundles repository carries it and an author who
  never installs this plugin can still read the design.
- **Outside the bundle.** A bundle is shipped to learners, who have no use for the
  author's design rationale and every reason not to read ahead. A spec inside the bundle
  is also one more file the validator has to have an opinion about.

The file name is the bundle `id`, which is stable for the life of the course. One spec per
bundle, revised in place, not one per change.

---

## 2. What it must contain

Scale the sections to the course; do not scale away the arc or the gate.

### Always

**Identity.** Bundle `id`, title, one-sentence description, and the scale classification
the interview announced. The scale is worth recording: the next author needs to know a
short course was deliberately short, not unfinished.

**The learner.** Who this is for, what they already know, what they can do at the end that
they cannot do now. The end state in one sentence, in the learner's terms.

**The arc.** The ordered lesson list — the spine of the document. Each entry carries:

| Column | Content |
|---|---|
| position | its place in the order |
| slug | the lesson `id`, which is also its filename stem |
| purpose | one line: what pressure this lesson answers |
| completion | one line: the checkable condition for leaving it |
| `design_refs` | the `DESIGN.md` anchors it needs, by name |
| validators | by name |

A table is enough and reads better than prose. The completion and `design_refs` columns
are not decoration: the self-check in section 4 is run against them, and an arc without
them cannot be checked at all.

**Teaching stance.** `workspace_kind`, `ownership_policy`, `solution_code`, `advance_on`,
`one_task_at_a_time`, and the validator definitions — the actual map, not a description of
it, because this is what the manifest is generated from.

**Durable decisions.** One entry per `DESIGN.md` section: the anchor name, what the
decision is, and what would break if a later lesson contradicted it. Mark the deliberately
unresolved ones as unresolved; they are useful context and often where a later lesson does
its teaching.

**The proposed fields.** `subjects`, `aliases`, `level`, `style`, and the defaults, shown
as one block. This is the block the author objects to instead of answering nine questions,
so it must actually appear rather than being held in your head.

### For a standard or long course

**The chapter map**, if chapters group the lessons — this becomes `COURSE.md`'s map.

**The coverage list.** Topics the course owes a learner, named the way a learner would ask
about them, never as lesson titles. Include what the course deliberately does **not**
cover; that half is read mechanically by a tutor deciding whether a stuck learner has hit a
hole or the intended difficulty of an exercise.

### For a long course

**Milestones.** The points where the learner has something that works.

**Depth decision.** Which chapters get lesson files now and which stay a map in
`COURSE.md`. Record the cost that was accepted: every learner's tutor drafts an unwritten
chapter separately, differently.

### Never

- Anything about a learner's progress. No "completed", no "current", no status markers.
  You are designing a course that has no learner in it yet.
- Anyone's source code.
- Lesson bodies. The spec carries purpose and completion conditions; the teaching goes in
  the lesson.
- A conversational script. The tutor generates the conversation from objectives.

---

## 3. Shape

```markdown
# <Course title>

**Bundle id:** `<bundle-id>`
**Scale:** short | standard | long
**Status:** draft, pending author approval
**Date:** <date>

## The learner
Who this is for, what they already know, what they can do at the end.

## The arc
| # | slug | purpose | completion | design_refs | validators |
|---|---|---|---|---|---|

## Chapters and milestones
(standard and long courses)

## Teaching stance
workspace_kind, ownership_policy, solution_code, advance_on, one_task_at_a_time,
and the validators map as it will appear in tutorial.yaml.

## Durable decisions
### <anchor-name>
What the decision is. What breaks if a lesson contradicts it. Resolved or open.

## Coverage
What the course owes. What it deliberately leaves out.

## Proposed manifest fields
subjects, aliases, level, style, and the defaults — as one block to object to.

## Open questions
Anything the author has not decided. Empty is a fine answer; a "TBD" in a
section above is not.
```

The status line changes to `approved` when the author approves it, with the date. That is
how a later session, and a later author, can tell whether the gate was passed.

---

## 4. Self-check before presenting

Run this on the draft and fix what it finds. It is checkable rather than a feeling, and
the middle items catch statically a subset of what a full walk of the course would find
hours later. It is a first filter, not a proof — say so when you present.

- [ ] Every field the format requires has an answer or a defensible default. Walk the
      field table in the runner's `references/bundle-format.md` section 2.
- [ ] Every lesson's completion condition depends only on what **earlier** lessons built.
      Take the arc in order and check each row against the union of the rows above it.
- [ ] Every `design_refs` entry in the arc names a section that exists in *Durable
      decisions*.
- [ ] Every validator named in the arc is defined in *Teaching stance*.
- [ ] No lesson introduces a type or concept that nothing later uses.
- [ ] Every slug is unique, lowercase, and in the form a filename can take.
- [ ] The coverage list names topics, not lessons, and says what is out of scope.
- [ ] No placeholder survives: no "TBD", no purpose line that restates the title.
- [ ] No section contradicts another — most often the arc against the chapter map.
- [ ] Nothing in the document records progress, and no source code appears in it.

---

## 5. The spec after approval

**It is not a throwaway.** It is the reviewable record of the course's design, and the
modify interview revises it.

- A **structural** change revises the spec first, and the author approves the revision
  before any bundle file moves.
- A **local** change updates the affected rows afterwards, in the same sitting.
- A **cosmetic** change usually touches nothing here.

A spec that no longer describes the bundle is worse than no spec, because the next author
believes it. When you cannot reconcile the two, say which one you trust and why, rather
than quietly editing the document to match the files or the files to match the document.
