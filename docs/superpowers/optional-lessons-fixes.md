# Optional lessons — fix wave after the review of 67ef718

**Date:** 2026-09-12
**Reviewed commit:** 67ef718 (plus 565b888, which made `test_yamlite_drift.py` green)
**Spec:** `docs/superpowers/specs/2026-09-12-optional-lessons-in-the-toolkit.md` (approved)
**Implementation report:** `docs/superpowers/optional-lessons-report.md`
**Issues:** skomp/tutorail-authoring#1 (feature), #7 (SKILL.md)

---

## 1. Status

Every finding in the wave is addressed. Nothing in the review was found to be wrong, and
one finding is closed slightly differently from how it was written — see section 7.

| Finding | What it was | State |
|---|---|---|
| Important 3 | `SKILL.md` documents neither `--optional` mode | done; closes #7 |
| Important 1 | `index.py:70` points at the corrected docstring while restating the old claim | done |
| Important 2 | `README.md` lines 107 and 110 | done |
| Minor 4 | a list-shaped `optional_lessons` is misattributed to the tool | done, with a test |
| Minor 5 | `numbered_twins` is an untested oracle | done |
| Minor 6 | `--required-for` and dirty-tree have no test | done, both |
| Minor 7 | report section 7 is stale | done, as a correction note |
| Minor 8 | `TODO.md` is silent about #7 | done, see section 7 |
| Ruling A | the `--offer-at` input contract | in `SKILL.md` |
| Ruling B | the `--confirm` mechanism | in `SKILL.md` and in the spec |

## 2. Suite counts

Measured with the whole runner scripts directory pinned, as the dispatch requires:

```
mkdir -p /tmp/fixpin && cp ~/.claude/plugins/marketplaces/tutorail/skills/tutorail/scripts/*.py /tmp/fixpin/
TUTORAIL_VALIDATOR=/tmp/fixpin/validate_bundle.py python3 tests/run_all.py
```

| | Before this wave | After |
|---|---|---|
| suites | 11, all green | 11, all green |
| `test_lesson_add.py` | 254 | 290 |
| every other suite | unchanged | unchanged |
| **total assertions** | **1447** | **1483** |

No existing assertion was changed or removed. The floor of 1447 was measured first, on the
tree as it stood at 565b888, before anything here was edited.

## 3. Important 3 — the modes reach the calling agent

`skills/tutorail-authoring/SKILL.md` gained one table row per mode, and a three-bullet
block under the table for the contracts the table cannot show:

1. **`--offer-at`, `--repair-in` and `--required-for` name a MAIN-PATH lesson**, and accept
   either spelling — the `lessons` entry `lessons/03-first-refactor.md` or the bare id
   `03-first-refactor`. The runner's check 18 resolves these three fields against the
   `lessons` list, so a bare id naming an *optional* lesson is refused, correctly.
2. **`promote.py --optional` exits 2 until `--confirm` is passed**, printing the two derived
   values and writing nothing. The bullet says in as many words that the non-zero exit is
   the confirmation gate and not a failure, because an agent reads exit 0 as "done" and is
   equally likely to read exit 2 as "something to work around".
3. **`--required-for` prints the rubric's warning**, and the agent is told to put it in
   front of the author.

The second and third of those are the two rulings the dispatch asked to land in a normative
document. The `--confirm` mechanism also reached the spec, which previously said only
"requires confirmation" and left the mechanism to an implementation report.

The other two judgement calls the review ruled correct — the pre-flight refusals, and
leaving an undeclared `--anticipates` to the validator — were deliberately not documented.

`SKILL.md` and every `references/*.md` were swept for host-specific tool names, `${...}`
and `CLAUDE_PLUGIN_ROOT`, case-sensitively, with a planted control file carrying one hit of
each class. The control fired on all four classes; the real sweep is clean.

## 4. Important 1 and 2 — the superseded claim

The claim that this toolkit does not author or edit an optional lesson was corrected in
`Bundle.optional`'s docstring by 67ef718 and left standing in three other places.

**Sweep, run before declaring the fix done.** `grep` here is ugrep 7.8.4 and the dispatch
warns that `-E` with a digit class beside `\b` matches nothing with a clean exit 1, so
every sweep used `-P` and a planted positive control that was watched firing first.

Pattern 1, `(?i)(toolkit|tool)\s+does\s+not\s+(author|edit|renumber|create|touch|write)|does\s+not\s+author,\s*edit\s+or\s+renumber|inserted\s+in\s+the\s+list`, across the whole
repository:

| Hit | Verdict |
|---|---|
| `README.md:107` | changed — the row now says `lessons` list, and a second row documents `--optional` |
| `skills/tutorail-authoring/scripts/index.py:70` | changed — carries a dated correction note, and says index.py still only READS the field |
| `docs/superpowers/optional-lessons-report.md:58` | **left** — it is the implementer quoting the old docstring inside their own correction note. Rewriting a quotation would make the note incoherent. |

Pattern 2, `(?i)inserts?\s+into\s+.?lessons`, found a fourth instance the review did not
name:

| Hit | Verdict |
|---|---|
| `docs/superpowers/specs/2026-09-12-bundle-authoring-design.md:146` | changed — a dated correction note now sits directly under that table, pointing at the optional-lessons spec and at `SKILL.md` |

**Counts: 4 instances found, 3 changed, 1 deliberately left as a quotation.** Plus
`README.md:110`, which was an omission rather than a false claim (the `promote.py` row with
no optional mode) and was found by reading, not by the pattern: a second row was added.

## 5. Minor 4 — the misattributed failure

`Bundle.optional` accepts a LIST-shaped `optional_lessons` (`bundlelib.py:343`), so every
reading command in the toolkit copes with one and an author can really be holding it.
`read_optional_lessons` flattened that shape to `{}`, so neither the duplicate check nor the
inline check in `add_optional_lesson` saw it; the append produced unparseable YAML; and the
function's own round-trip guard then told the author

> This is a bug in `add_optional_lesson` itself, not in the caller's entry.

which is a true statement about the wrong thing, with no remedy in it. Reproduced directly
against `bundlelib` before anything was changed.

The fix separates the reader from the editor. `_optional_lessons_value` returns the raw
value with no shape filter; `read_optional_lessons` is now a two-line wrapper over it and
behaves exactly as before. `add_optional_lesson` refuses a non-mapping block value with
`ManifestEditError` carrying the same remedy the non-empty inline case gets — the block
mapping form, spelled out, and "Nothing was written."

The check sits **after** the inline-value scan, so an inline value keeps its own message.

## 6. Minor 5 and 6 — the three missing tests

All three are in `tests/test_lesson_add.py`.

- **`numbered_twins`** now has a positive control inside E18. A main-path add into the same
  `lessons/` directory writes `23-twin-probe.md`, the oracle is required to find it, and the
  `borrow-detour` assertion is then re-run over that same listing — so the empty answer is a
  fact about the optional lesson and not about the probe.
- **`--required-for`'s pre-flight refusal** is a new block in E22, on the `optional-course`
  fixture rather than `rust-automaton-db`. That is not cosmetic: check 18 refuses a gate
  that anticipates nothing, so on a bundle with no declared failure mode the control could
  never be accepted and the refusals would have been measured against an instrument that
  could not report a positive. Two refusals (an unknown lesson, a mis-cased one), a
  `check_not_in` asserting the refusal comes *before* the rubric warning, and one control
  that is accepted, prints the warning, and writes the resolved gate.
- **`--optional` against a dirty tree** is a new case, E23b: a clean-repo control first, then
  a tracked-file modification refused with the path named and no `optional_lessons` entry
  written, then `--force` overriding on the same still-dirty bundle and leaving the author's
  uncommitted edit alone. `--optional` takes its own branch through `add()`, which is why
  D15's main-path proof does not cover it.
- **The list-shaped manifest** from section 5 is a new block in E23, with the
  `optional-course` fixture rewritten into sequence form and the unmodified fixture as the
  control — the two bundles differ only in the shape of that one value.

Every refusal ends in the `refusal()` helper's `tree_digest` comparison.

### Guards watched failing before they were believed

Each break was applied to the working tree, the suite was run, and the break was reverted.

| Break | Where | What failed |
|---|---|---|
| G | the new non-mapping refusal in `add_optional_lesson` disabled | exactly 3 assertions, all new: the refusal's message needle, "use block form", **and** "the author is NOT told the tool is broken" — the `check_not_in` probe demonstrated firing, which is the whole point of adding it |
| H | `numbered_twins` returns `[]` unconditionally | exactly 1 assertion: the new control. Before this wave that break passed the entire suite. |
| I | `--required-for` skips `resolve_main_path` | 8 assertions: both new refusals, the "refusal before warning" probe, the mis-case hint, the new control, and E21 — which uses the bare-id spelling and so depends on the same resolver |
| J | `require_clean_tree` skipped when `args.optional` | exactly the 7 assertions of the new E23b, and nothing else |

Break H is the one worth reading twice. The oracle it breaks was asserted five times in the
suite and every one of those assertions still passed, because they all asserted `== []`.

## 7. Where this deviates from the dispatch

**Minor 8.** The dispatch asked for `tutorail-authoring#7` as a row in `TODO.md`'s dated
table. That table is explicitly a list of what is still OPEN, and this commit closes #7, so
a row would have been false from the moment it landed. Instead the table's lead-in now
names the optional-lesson work, and two short bullets under it record #7 as filed and closed
on 2026-09-12, and #1 as implemented and awaiting the owner's close. A reader who meets
either number elsewhere can now find out where it stands without guessing, which is what the
finding was for.

Nothing else departs from the dispatch, and no finding in it was found to be wrong.
