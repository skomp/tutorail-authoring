# The modify interview

**Status:** normative. Load this when a bundle exists and something about it is to change,
and before promoting a generated lesson.

Modifying is not a smaller version of creating. It has a different first move, a different
first question, and one job that create does not have at all: **surfacing knock-on
effects**. Renaming a `DESIGN.md` anchor is one edit and four broken lessons. The author
cannot see the four. The index can.

---

## 1. Start from the index, never from the course

Before the first question:

```
python3 scripts/index.py <bundle>
```

The index is generated mechanically from the manifest and lesson frontmatter — id, title,
form, `design_refs`, `validators`, and a one-line purpose per lesson. A twenty-three-lesson
course is roughly 2,700 lines; its index is roughly 40. Loading the course to discuss
restructuring one chapter spends the entire context budget before the conversation starts.

**What the index answers on its own:**

| Question | How |
|---|---|
| which lessons cite a given `DESIGN.md` anchor | their `design_refs` |
| which lessons use a given validator | their `validators` |
| what order the lessons are in, and what is first | the list order |
| whether a lesson is a single file or a folder | its form |
| roughly what each lesson is for | its purpose line |

**What it does not answer**, and what you therefore open specific lessons for:

- prose prerequisites — a lesson naming an earlier lesson's id in its *Prerequisites*
  section. The index does not carry lesson bodies and the validator does not check these.
- completion conditions, constraints, and anything else in a lesson body.
- whether the material in a lesson folder is still referenced by its `LESSON.md`.

Open only the lessons the interview shows you will touch, plus the ones the knock-on
tables below name. If you find yourself opening a fifth lesson to answer one question,
stop and ask the author instead.

---

## 2. Ask what is wrong, not what the author wants

Authors arrive with a fix, not a complaint: *"split lesson 07"*, *"rename the
`key-ordering` anchor"*. The fix is a hypothesis about a problem you have not heard yet,
and it is frequently the wrong repair for the right complaint. So the first question is
some form of:

> "What goes wrong for a learner at that point?"

*"Split lesson 07"* often turns out to be *"learners get lost in 07"*, and the repair is
as often a missing prerequisite in 06, or completion conditions nobody can check, as it is
a split. *"Rename the anchor"* is sometimes *"the design decision changed"*, which is a
`DESIGN.md` rewrite plus every lesson that depended on the old decision — a much larger
change than a rename.

Two follow-ups earn their place:

- **Is there evidence?** Generated lessons in real instances are the best signal the format
  produces. Several learners taking the same detour after the same lesson is a missing
  lesson, with the files as proof. One learner once is evidence of nothing.
- **Which learners is this for?** A change that helps the learner the course was written
  for is different from one that quietly widens its audience — which is a scale change,
  not a fix.

---

## 3. Classify the change, and say so out loud

Same ratchet as the create interview, one-way, heavier when in doubt.

| Class | What it is | Process |
|---|---|---|
| **Cosmetic** | a typo, a clearer sentence, a better example inside one lesson. No structure moves. | State what you will change, change it, show the diff. No spec round. |
| **Local** | one lesson added, split, retired or reordered; a validator added; a `DESIGN.md` section extended. The arc is unchanged. | State the change **and its knock-on effects**, get a yes, apply with the toolkit, validate. Record the change in the course spec afterwards. |
| **Structural** | the arc changes: milestones move, chapters are resequenced, the end state or the audience changes, a design decision is reversed. | Run the relevant phases of the create interview, revise `specs/<bundle-id>.md`, and **stop for approval before touching a bundle file.** The gate is the same gate. |

A change that turns out to be structural mid-way upgrades. Say so and go back to the spec;
do not finish it as a local change because you have started.

---

## 4. The knock-on tables

This is the part the author cannot do without you. For the change in front of you, the
index answers the middle column; the right column is what you must raise **before**
applying anything.

### Structure

| Change | Ask the index | Raise with the author |
|---|---|---|
| **Add a lesson** | what is at that position now; which validators exist; which anchors exist | Does any later lesson's prerequisites now sit after it? Does it need a new anchor, or does it cite one that exists? Does the new topic belong in the coverage list? |
| **Reorder or move a lesson** | the current order; the `design_refs` of everything between old and new position | Does the moved lesson's completion now depend on something that comes after it? Do the lessons it passes still have their prerequisites met? |
| **Split a lesson** | its `design_refs` and `validators` | Which half keeps which anchors, and which keeps the prose prerequisites other lessons name? A split changes one id into two, so every lesson naming the old id in prose needs a decision. |
| **Retire a lesson** | which anchors and validators only it used; where it sits | Which later lessons name it as a prerequisite in prose? Which anchors are now cited by nothing — remove them, or leave them as context? Does the coverage list still hold? |
| **Renumber** | nothing; `renumber --check` reports it all | Show the `--check` output. It names every prose reference it would rewrite **and everything that looked like a reference and will be left alone** — that second list is where a break will be. |

### Design and validators

| Change | Ask the index | Raise with the author |
|---|---|---|
| **Rename a `DESIGN.md` anchor** | **every lesson whose `design_refs` cite it** | Anchors are stable once published, and the format has no aliasing: every citing lesson changes in the same commit or the bundle is broken. Name the lessons — "05, 07, 09 and 11" — and let the author decide whether the rename is worth it. |
| **Change what a decision says** | the same list | This is usually structural, not local. Every lesson taught against the old decision may now teach something wrong, and the validator cannot see that. |
| **Add or remove a decision** | which lessons might need it | A section nothing cites is harmless; a lesson citing a section that does not exist is invalid. |
| **Rename or remove a validator** | every lesson naming it | A lesson referencing an undeclared validator is invalid. All of them change together. |

### The pattern

The three questions behind every row: **who cites this, what breaks if it moves, and what
does the validator not check?** That last one is where the damage lives. `design_refs` and
validator names are checked; prose prerequisites, completion-condition ordering and
coverage-list accuracy are not. Those are yours.

---

## 5. Apply the change with the toolkit

Never by hand. The rules from the control plane, restated because this is where they are
broken:

1. **Run with `--check` first** and show the author the output. For `renumber` this is not
   optional courtesy; it is the only review the change gets.
2. **Let a refusal stand.** A dirty working tree is refused so that `git diff` is a true
   record of the tool's work. Commit or stash the author's own changes — do not `--force`
   past them, and never discard them.
3. **The validator runs after every mutating operation.** A run that leaves the bundle
   invalid fails loudly, and a failed run leaves the bundle unchanged rather than
   half-edited. If you are looking at a half-edited bundle, that is a defect in the
   toolkit and worth reporting, not working around.
4. **Check every rewrite the tool reports**, particularly `renumber`'s left-alone list.

Common sequences:

- **Adding a lesson**:
  `python3 scripts/lesson.py add <bundle> --id <slug> --title <text> --after <lesson-path>`,
  then `python3 scripts/lesson.py renumber <bundle> --check` if the numbering is now
  uneven, then fill the body, then validate.
- **Splitting a lesson**: add the second lesson with `lesson.py add`, move the prose
  yourself, then fix the prose prerequisites in the lessons the index named.
- **Retiring a lesson**: remove it from the course, then
  `python3 scripts/lesson.py renumber <bundle> --check`, then repair the prose references
  the report leaves alone.

---

## 6. Promoting a generated lesson

A tutor writes lessons into a learner's `tutorial/lessons.generated/` during a course.
Promotion is a bundle-side authoring act with a script:

```
python3 scripts/promote.py <instance> <generated-lesson-path> <bundle> --check
```

What to hold in mind while working through what it reports:

- **The learner keeps their copy.** Promotion copies; it never moves or deletes. That
  learner keeps working from their own file, and the duplicate is reported and resolved
  the next time they materialize a revision.
- **The provenance frontmatter goes.** `generated`, `generated_at`, `kind`, `reason` and
  `after` all describe one learner's run. All five, every time.
- **`id` becomes the new slug.** Generated lessons carry no number prefix, so the rename
  always changes the slug, and this is the easiest step to forget.
- **`design_refs` are re-checked against the bundle's `DESIGN.md`, not the instance's.**
  The instance's `DESIGN.md` grew during the course. A promoted lesson may cite an anchor
  the tutor appended and your bundle has never had. For each: add the section, or drop the
  reference.
- **The lesson is rewritten for a learner who has not started.** It was written against one
  learner's code and it names their types, their file, their error message. Generalise all
  of it. Nothing about their progress survives.
- **`COURSE.md` may owe an update** if the course now covers a chapter its map did not
  mention.

Ask first whether it should be promoted at all. One side lesson, once, is usually one
learner's background rather than a hole in the course. The same `after:` from several
learners is the signal worth acting on, and the repair may be to fix the lesson before the
detour rather than to add one after it.

---

## 7. Close the change out

- **Update the course spec.** `specs/<bundle-id>.md` is the reviewable record of the
  course's design. A local change adds a line to it; a structural change revised it before
  any file moved. A spec that no longer describes the bundle is worse than no spec, because
  the next author believes it.
- **Update `COURSE.md`** when the chapter map or coverage list moved.
- **Validate**, and work the runner's `bundle-format.md` section 10 self-check by looking.
- **Rebuild the catalogue** with `python3 scripts/catalog.py <bundles-repo>` if a bundle
  was added or renamed, or if the lesson count crossed the boundary the catalogue derives
  scope from.
- **Say what a learner mid-course gets**, because the answer is nothing: revising a bundle
  while an instance is live has no reconciliation story. The change reaches the learners who
  come after. Authors regularly assume otherwise.
