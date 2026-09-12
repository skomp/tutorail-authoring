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

---

## Correct the material-naming rule in the runner design spec — owed 2026-09-12

This entry is a handover. The file is in the `skomp/tutorAIl-supplies` repository, on the
`supplies` branch. Another session owns that file. Do not edit it without that session.

**File:** `docs/superpowers/specs/2026-09-11-tutorial-runner-design.md`

### What is wrong

The spec states the material-naming rule without a qualification. The `supplies:` key adds
one. The branch therefore ships a design spec that contradicts the contract it describes.

Two places carry the unqualified rule.

1. Line 205 to line 207. The text says "material loads only when `LESSON.md` names it". It
   then says "Two consequences the validator enforces rather than leaves to judgement". The
   validator no longer enforces the first consequence in every case.
2. Line 833. The table row says "lesson-folder material not named by `LESSON.md`" is not
   loaded.

### The correction to make

Add the exemption to both places. The authority is
`skills/tutorail/references/bundle-format.md`, section 2, **Supplied material and section
6**.

- A file that a `supplies` entry covers is exempt from the naming rule.
- Any scope clears the file. The manifest clears it, and so does any lesson. The owning
  lesson does not have to be the one that declares it.
- `validate_bundle.py` check 6 applies the exemption. The check reports how many files a
  supplies declaration cleared.
- Every other file in a lesson folder still needs a name in the body.

At line 207, change "Two consequences the validator enforces rather than leaves to
judgement" to say that the validator enforces both consequences **for a file that no
`supplies` entry covers**.

At line 833, add "and not covered by a `supplies` entry" to the table row.

### Why this session did not make the change

The reviewer ruled that this file belongs to another session. This session corrected the
same claim in `docs/superpowers/specs/2026-09-12-toil-and-course-quality-design.md`, which
is in this repository. That correction carries a note at the top of the file.

---

## The catalogue scope line ignores optional lessons — 2026-09-12

`scripts/catalog.py` derives the `scope` line from the length of the `lessons` list. A course
that also ships optional lessons gives no signal that they exist. A reader of `catalog.yaml`
sees "15 lessons" for a course that carries three more.

To derive the count from the main path alone is correct. A learner can decline every offer.
The gap is that the catalogue says nothing about the optional lessons.

Change `scripts/catalog.py` and `catalogue-format.md` together. The runner does not change.

Reported by the session that regenerated `tutorail-bundles/catalog.yaml`.

---

## Course findings from the first audit — 2026-09-12

The first run of `skills/course-quality/` audited three courses. The full report is at
`docs/audits/2026-09-12-course-quality-first-run.md`.

The findings below are about the courses in `tutorail-bundles`, not about this repository.
No course was changed. The author decides what to act on.

- `webgl-typescript-scene` calls lesson 14 optional in three places of prose. The lesson sits
  in `lessons:`. The manifest has no `optional_lessons` key. A learner who skips the lesson
  earns 183 points, not the 194 the report shows. The two totals come from the rubric of
  2026-09-12. The correction note at the top of that report supersedes them. The gap of 11
  points stays the same.
- `webgl-typescript-scene` lesson 13 states the objective "Carry asset licence and attribution
  into the repository". Only the copy instruction serves that objective. Move the instruction
  into `supplies:` and the objective loses its only step.
- `durable-event-broker` `COURSE.md` line 77 says the course is complete when a learner
  declines every offer. Line 87 lists three topics that only optional lessons teach. The two
  statements disagree.

---

## Finish the supplies and course-quality work — 2026-09-12

Ten tasks are complete and reviewed. A final whole-branch review and one fix wave are done.
Only the steps below remain. A fresh session can do them without the original transcript.

### Step 1. Read the last re-review

A scoped re-review of the fix wave was running when the session ended. Its package is at
`.superpowers/sdd/2026-09-12-supplies-and-course-quality/rereview-final.md`. If the directory
is gone, re-create the package from the commit ranges below.

### Step 2. Push this repository

Robert asked for the plugin installs to be updated when the quality checker is done.

1. Run `python3 tests/run_all.py` with the whole runner scripts directory pinned. Expect 10
   suites.
2. Push `main`.
3. Run `claude plugin update tutorail-authoring@tutorail-authoring`, then restart.
4. **Verify by content, not by version.** Confirm the updated copy holds
   `skills/course-quality/SKILL.md` and `skills/course-quality/scripts/audit.py`. An install
   compares the version number, so a green "updated" line is not evidence.

### Step 3. Hand over the runner branch

Branch `supplies` in the worktree `../tutorAIl-supplies` holds 13 commits. It is rebased onto
`origin/main` and both suites are green: `test_validate_bundle.py` 310, `test_catalogs.py` 158.

**Do not merge it.** Merging is Robert's action. Tell him it is ready.

Send ONE line to the session named `runner` when it lands on main. Say also that this branch
does not correct the "deliberately shallow, one level at most" sentence in `bundle-format.md`,
which is stale because `optional_lessons` nests to three levels. That session will correct it
in its own change.

### Step 4. Hand over two items that belong to the runner repository

1. `docs/superpowers/specs/2026-09-11-tutorial-runner-design.md` states the material-naming
   rule with no exception, and says the validator enforces it. Check 6 now clears a file that
   a `supplies` entry covers. The exact correction is in the entry above this one.
2. `tests/test_validate_bundle.py` has a weak `run_case`. It checks that the expected message
   appears in ANY finding of that check number. A case can pass while the wrong file produces
   the finding. This is why one check-6 test passed against unfixed code.

### Step 5. Close the plan

Delete `.superpowers/sdd/2026-09-12-supplies-and-course-quality/` only after steps 1 to 4.
It holds the ledger and every review package.
