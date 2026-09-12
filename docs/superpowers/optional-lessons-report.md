# Optional lessons in the toolkit - implementation report

**Date:** 2026-09-12
**Spec:** `docs/superpowers/specs/2026-09-12-optional-lessons-in-the-toolkit.md` (approved)
**Issue:** skomp/tutorail-authoring#1

---

## 1. Status

All three pieces are implemented and committed. The full suite passes against the pinned
validator, with one suite red for a cause outside this change (section 7).

| Piece | Spec section | State |
|---|---|---|
| `lesson.py add --optional` | 3 | done |
| `promote.py --optional` | 4 | done |
| `renumber` tests, no code change | 5 | done |
| `bundlelib.add_optional_lesson` | 6 | done |

## 2. Suite counts

Measured with the whole runner scripts directory pinned:

```
mkdir -p /tmp/optpin && cp ~/.claude/plugins/marketplaces/tutorail/skills/tutorail/scripts/*.py /tmp/optpin/
TUTORAIL_VALIDATOR=/tmp/optpin/validate_bundle.py python3 tests/run_all.py
```

| Suite | Before | After |
|---|---|---|
| `test_lesson_add.py` | 149 | 254 |
| `test_lesson_renumber.py` | 92 | 111 |
| `test_promote.py` | 206 | 275 |
| every other suite | unchanged | unchanged |
| **total** | **1254** | **1447** |

No existing assertion was changed or removed.

## 3. What was built

### 3.1 `bundlelib`

`OPTIONAL_KEY`, `render_optional_entry`, `read_optional_lessons` and `add_optional_lesson`.
`add_optional_lesson` is the `add_supplies` sibling the spec asks for: it reuses
`emit_scalar` for every scalar, reuses `_top_level_block_end` for the block walk (the
function was named `_supplies_block_end`; it was already generic and is now named after the
shape), and it ends with the same round-trip guard - it parses its own output through
`load_yaml` and raises `ToolError` when the entry reads back differently from the entry it
was given. No second quoting rule was written.

It accepts the three starting shapes `add_supplies` accepts: a block mapping, a bare
`optional_lessons:` key, and the empty inline `optional_lessons: {}`. A non-empty inline
value raises `ManifestEditError`. A path already declared is refused before anything is
written, because the loader rejects a duplicate key.

`Bundle.optional`'s docstring carried the claim that "this toolkit does not author, edit or
renumber such a lesson". Two thirds of that is now false and the last third never was, so
the docstring carries an explicit correction note rather than a silent rewrite.

### 3.2 `lesson.py add --optional`

Shape as the spec specifies: `bl.find_validator()` first, then `load_bundle`,
`require_clean_tree`, the refusals, the printed plan, then one `bl.Staged` wrapping all
three writes and `stage.commit()`.

- the lesson file has **no number prefix**;
- its frontmatter carries `optional: true`, written with `set_frontmatter_field` into the
  same file write, so the frontmatter and the list can never be apart (check 20);
- the `optional_lessons` entry is written by `add_optional_lesson`;
- the `lessons` list is never touched and no renumber is advised.

`--offer-at`, `--anticipates` and `--required-for` are repeatable and write lists;
`--repair-in` writes a scalar. That matches the shapes the runner's check 18 reads.

`--offer-at`, `--repair-in` and `--required-for` accept either spelling an author has in
front of them - the manifest entry `lessons/03-x.md` or the bare lesson id `03-x` - and
resolve to the manifest entry.

### 3.3 The `--required-for` warning

Printed verbatim from `skills/course-quality/references/rubric.md`, five lines, stored as
`REQUIRED_FOR_WARNING` in `lesson.py` with a comment saying it must not be edited there
alone. `tests/test_lesson_add.py` case E21 asserts, for each of the five lines, that the
tool prints it **and** that the rubric carries it as a quoted `> ` line. A drift in either
file fails the suite - both directions are demonstrated in section 6.

### 3.4 `promote.py --optional`

`offer_at` is derived from the generated lesson's `after`, `offer_because` from its
`reason`. A folded block scalar (`reason: >`) is normalised to one line, and the normalised
value is printed, so the author confirms the exact text that will be written.

Confirmation is a second flag, `--confirm`, not a prompt: these commands are run by the
authoring skill, and a tty prompt would hang an agent. Without `--confirm` and without
`--check` the command prints both derived values and **refuses** (exit 2), writing nothing.
`--check` runs the whole thing on a staging copy, validates it and writes nothing.
`--confirm` applies it. `--confirm` without `--optional` is refused.

Promotion strips the five provenance fields, sets `id`, writes `optional: true`, adds the
entry, leaves the `lessons` list alone, advises no renumber, and does not touch the
learner's copy.

Four helpers were lifted out of `promote()` so both modes share one copy of steps 1, 2, 3, 5
and 6: `body_slug_of`, `refuse_slug_clash`, `check_steps_5_and_6`, `strip_provenance`. The
main-path path is otherwise unchanged and its 206 assertions still pass.

### 3.5 `renumber`

**No code change**, as the spec requires. Two cases were added, each with a control in the
same run, and the fixture they need is new: `tests/fixtures/optional-course`.

## 4. The new fixture

`tests/fixtures/optional-course` - three main-path lessons, one optional lesson, one
declared failure mode that the optional lesson anticipates (check 19 reports a declared mode
that nothing anticipates, so the two have to ship together). It validates clean against the
pinned validator before any test touches it.

It carries the prose reference the renumber case needs: `- \`01-shapes\`` inside the
optional lesson, and the identical line inside a main-path lesson as the control.

## 5. Atomicity

Every refusal test ends with a `tree_digest` comparison, not with "the new file is absent".
Two of them are mid-transaction failures by construction:

- a non-empty inline `optional_lessons:` makes the MANIFEST edit raise **after** the lesson
  file has already been written to the staging copy. The digest still matches and the staged
  file is not left behind;
- the stub validator refuses at `commit()`. The digest matches, the lesson file is absent,
  and the `optional_lessons` map is still empty.

Both have a positive control: the empty inline `optional_lessons: {}` is accepted and
rewritten in block form, and the same run under the real validator writes both halves.

## 6. Guards watched failing before they were believed

Each break was applied to the working tree, the suite was run, and the break was reverted.

| Break | Where | What failed |
|---|---|---|
| A' | `renumber_plan` iterates `bundle.listed + sorted(bundle.optional)` | ONLY the two new renumber cases. The optional lesson was renamed to `04-vertex-winding-detour.md` - exactly the corruption issue #1's first comment feared. Every pre-existing renumber case still passed, so the break is surgical and the new cases are what caught it. |
| B | `renumber`'s rewrite loop skips files in `bundle.optional` | The prose case's three content assertions, **and** case 1's byte-probe positive control ("the optional lesson's CONTENT did change"). That control exists precisely to stop "the file was not renamed" being confused with "the file was not visited", and it fired. |
| C | `add --optional` writes the lesson file but never the manifest entry | Every E-case. The runner's check 20 rejected the half-written bundle, the transaction discarded it, and the digest assertions confirmed byte-identity. This is the atomicity claim demonstrated end to end rather than asserted. |
| D | one word changed in `REQUIRED_FOR_WARNING` in `lesson.py` | E21's "the tool prints ..." assertion. |
| E | one word changed in `rubric.md` instead | E21's "and the rubric carries that line VERBATIM" assertion. Drift in either direction fails. |
| F | `promote --optional`'s confirmation gate made unconditional | C1's seven assertions, including the byte-identity of the bundle. |

Break A' is worth reading twice: the spec's central claim is that `renumber` is already
correct, and the test that locks that in is only worth something if it can fail. It can.

Section 5 of the spec says "a deliberately broken `renumber_plan`". Break A' is in
`renumber_plan`; break B had to go in `renumber`'s rewrite loop, because that loop, and not
the plan, is the code the prose case tests. Breaking only the plan would have failed the
prose case for the wrong reason (an empty plan rewrites nothing at all, so the control fails
with it).

## 7. One suite is red, for a cause outside this change

`test_yamlite_drift.py` fails: 4 of 49 assertions.

It compares the vendored `skills/tutorail-authoring/scripts/yamlite.py` against the runner's
own copy, and `run_all.py` deliberately UNSETS `$TUTORAIL_VALIDATOR` for it, so it always
measures the live runner checkout and cannot be pinned.

**The live runner checkout changed while this work was in progress.**
`~/.agents/skills/tutorail/scripts/yamlite.py` and `validate_bundle.py` both have an mtime
of 21:51 on 2026-09-12; the full suite passed twice earlier in the same session, including
once after every source change here was already in place. The diff against the plugin copy
is a docstring reword:

```
-  * validate_bundle.py - authoring-time, reads tutorial.yaml and catalogues;
+  * validate_bundle.py - reads tutorial.yaml and catalogues. An author runs it;
+                         the runner also runs it once, at materialization.
```

The vendored file in this repo is **unmodified** (`git status` is clean for it), and no file
of this change touches it.

The fix is to re-copy `yamlite.py` from the runner, which is what the vendored banner tells
the next reader to do. **It was deliberately not done here**, for three reasons: the file is
outside this change's ownership; the runner checkout is being edited right now, so copying
it would vendor a file mid-edit; and the plugin copy at version 0.4.0 still carries the old
text, so a re-copy would put this repo ahead of the published runner. It belongs to whoever
is editing the runner.

## 8. Disagreements and judgement calls

Nothing in the spec was found to be wrong. Four places where it was silent and a decision
had to be made:

1. **`--offer-at` takes a `lessons` ENTRY, not only a lesson id.** The spec writes
   `--offer-at <lesson-id>`, but check 18 resolves `offer_at` against the `lessons` list,
   whose entries are paths. Both spellings are accepted and resolved to the path, so the
   spec's spelling works and the manifest is correct.
2. **`--repair-in` and `--required-for` get the same pre-flight refusal as `--offer-at`.**
   The spec lists a refusal only for `--offer-at`. Check 18 requires all three to name a
   main-path lesson, so the other two would have failed inside the validator with a message
   in the validator's vocabulary. Refusing early costs nothing and says which flag is wrong.
   E22 shows `--repair-in` refusing, with the shared positive control.
3. **Confirmation in `promote --optional` is `--confirm`, not a prompt.** Reasoning in
   section 3.4. The unconfirmed run exits 2, because it is a refusal to write, and exit 0
   would read to an agent as "done".
4. **An undeclared `--anticipates` id is not refused before staging.** The toolkit has no
   command that declares a `failure_modes` entry, so the check would be a refusal with no
   remedy inside the toolkit. The validator refuses it at `commit()` instead, atomically,
   with its own precise message.

## 9. What this change does NOT close

- `skills/tutorail-authoring/SKILL.md` still documents `lesson.py add` and `promote.py`
  without the new modes: the command table at lines 117-121 needs two rows. That file was
  outside this change's file ownership and was deliberately left alone. It is the one
  follow-up and it is filed as an issue.
- `catalog.py`'s `scope` line still counts the main path only - out of scope by the spec,
  tracked as tutorail-authoring#2.
