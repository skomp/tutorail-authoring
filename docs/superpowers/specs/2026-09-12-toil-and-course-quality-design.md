# Supplied Files and Course Quality — Design

**Date:** 2026-09-12
**Status:** approved
**Repositories:** `skomp/tutorAIl` (runner, the format) and `skomp/tutorail-authoring` (this one)

---

## 1. The problem, as observed

A generated bundle, `webgl-typescript-scene`, opens its first lesson with this task:

> Copy these five files from `tutorial/lessons/00-project-setup/starter/` to the root of
> `webgl-scene/`, preserving the `src/` directory.

The learner learns nothing by doing it. The tutor was right to assign it, because the
lesson told it to: `lessons/00-project-setup/LESSON.md` line 34 puts the copy in
**Constraints**, and `lessons/13-load-gltf-model/LESSON.md` line 40 does the same for a
glTF model.

The author had no alternative. The runner has no concept of author-supplied files.
`state-lifecycle.md` section 3 materializes `tutorial/` and nothing else, and says
plainly that creating a project skeleton is the learner's action. The bundle also sets
`ownership_policy: tutor-must-not-edit-learner-owned` with `learner_owned` covering
`package.json`, `tsconfig.json`, `index.html` and `src/**` — so the tutor is *forbidden*
to place those files itself. A task was the only channel left open.

This design opens the right channel, forbids the wrong one in the authoring skills, and
adds a skill that measures how much of a course is teaching and how much is toil.

## 2. Definitions

| Term | Meaning |
|---|---|
| **toil** | a step that is deterministic and unambiguous, where the learner makes no decision and a mistake teaches nothing. Copying files, installing dependencies, downloading assets, unzipping, pasting supplied code verbatim. |
| **supplies** | files the bundle gives the learner's workspace. The runner places them. They are never a task. |
| **teaching step** | a step where the learner decides or constructs something, a wrong answer is instructive, and it serves a stated objective. |

The test that separates them, and the sentence the authoring skills must carry:

> **What can the learner get wrong here, and does getting it wrong teach anything?**
> If nothing, it is not a task. It is `supplies:`.

## 3. Measured facts — do not re-derive

Verified on this machine, 2026-09-12, against `skomp/tutorAIl` at `1697874` and
`skomp/tutorail-bundles` at `76dcdce`. First measured at tutorAIl `0b1c422` and
**re-verified at `1697874`** after three commits landed there mid-session: every line
number below still holds, and the only change to `bundle-format.md` was wording.

| Fact | Where |
|---|---|
| The runner plugin resolves to `/Users/robert/.agents/skills/tutorail`, a **symlink** into `~/src/github.com/skomp/tutorAIl/skills/tutorail` | `scripts/runner.py --root` |
| `KNOWN_BUNDLE_FORMATS = (1,)`; the validator rejects an unknown `bundle_format` | `validate_bundle.py:143`, `:654` |
| The validator does **not** reject unknown manifest keys or unknown lesson frontmatter keys. Only `catalog.yaml` gets an unknown-key check (`:2478`) | `validate_bundle.py` |
| `optional_lessons` is the precedent for an additive key: "the key is additive to bundle_format 1" | `bundle-format.md:1197` |
| Checks are numbered 1–21 in `CHECKS` at `validate_bundle.py:77`; `BUNDLE_ONLY = {12, 13}`, `INSTANCE_ONLY = {11, 14, 15, 17, 21}` | `validate_bundle.py:77`–`:106` |
| `resolve_exact()` already refuses unsafe path components ("path component %r is not allowed") | `validate_bundle.py:447`, `:462` |
| Check 9 does not object to extra directories at the bundle root | `check_required_files`, `validate_bundle.py:713` |
| Check 6 requires every file in a lesson **folder** to be *named* by that folder's `LESSON.md`, matched as a delimited token, basename or folder-relative path | `names_file`/`check_material_reachable`, `validate_bundle.py:1081`, `:1115` |
| The webgl bundle's toil is exactly two sites: `lessons/00-project-setup/LESSON.md:34` and `lessons/13-load-gltf-model/LESSON.md:40` | grep over the bundle |
| This repo's test suites run the runner's live validator through the symlink, and have already gone red from a mid-edit runner | `tests/run_all.py` header |

## 4. The format: `supplies:`

Additive to `bundle_format: 1`. No version bump. An older validator ignores it; an older
runner does not place the files, which is the same failure the bundles have today, not a
new one.

### 4.1 Shape

A list of entries. Each entry is a mapping with exactly three fields:

| Field | Required | Meaning |
|---|---|---|
| `from` | yes | a path **relative to the bundle root**. A trailing `/` means "the contents of this directory, recursively". Without a trailing `/` it is one file. |
| `to` | yes | a path **relative to the workspace root**. `.` is the workspace root itself. |
| `describe` | yes, non-empty | one line, in the author's words, naming what these files are. This is the sentence the runner says to the learner. |

`from` is bundle-root-relative in **both** scopes. A lesson-scope entry for a foldered
lesson therefore reads `from: lessons/13-load-gltf-model/model/`, not `model/`. One rule,
no scope-dependent resolution, and the path is greppable from the bundle root.

### 4.2 Scope decides timing

| Declared in | Placed |
|---|---|
| `tutorial.yaml`, top level | immediately after materialization, before the first lesson opens |
| a lesson's frontmatter | when that lesson opens, before its first task |

One word, one meaning. Where it is declared is the only thing that decides when it lands.

### 4.3 Placement rules

1. **Never overwrite.** A target path that already exists is left exactly as it is.
2. **Silence when nothing was done.** If every target of an entry already exists, the
   entry is already applied. Say nothing about it. This is what makes re-opening a lesson
   idempotent with **no new state**: nothing is written to `STATE.md` and nothing is
   written to the instance's `instance:` block.
3. **Report what was placed, precisely — and what was left alone.** When some targets were
   missing, place those, name them, and name the ones that already existed and were
   skipped. Partial application is reported as partial. This is the sharpest edge in the
   feature: a lesson-scope entry can land on a `learner_owned` path, and a learner must
   never be left wondering whether their own file was replaced.
4. **Name it as setup.** The report says these files are setup, not a lesson, so the
   learner is not left wondering what they were supposed to have learned.
5. Placement never reaches inside `tutorial/`. The instance is not the workspace.

### 4.4 The ownership exemption, stated narrowly

Under `tutor-must-not-edit-learner-owned` the tutor **may create** a declared supplies
target that does not exist. It may **never modify** one that does. Undeclared paths get no
exemption of any kind.

That is the whole exemption. It is narrow because the policy is load-bearing: the reason
the learner trusts that their code is theirs is that the tutor cannot write it.

### 4.5 Bundles that predate this key

The runner needs a rule for today's bundles, because `webgl-typescript-scene` will not be
changed by this work. When a lesson's prose instructs the learner to copy, download or
unzip files that the bundle itself supplies, the runner **does it, reports it as setup
handled, and notes that the bundle should declare it in `supplies:`**. It does not assign
it as a task.

This is deliberately a runner-side behaviour rule and not a detector: it is applied by a
reader who has the lesson in front of it, at the moment it would otherwise write a task.
It is not a lexical scan, and nothing in the runner is allowed to turn it into one.

## 5. Validator changes (`validate_bundle.py`)

### 5.1 New check 22

`CHECKS[22] = "supplies entries are well-formed, and every 'from' exists"`

It runs in both modes. For every entry, in the manifest and in every lesson's
frontmatter:

- the entry is a mapping and has exactly the keys `from`, `to`, `describe`; an unknown key
  is a finding, because a misspelled `describe` would otherwise silently produce a
  supplies entry the runner cannot narrate;
- `from` resolves, exact-case, to a file or directory **inside the bundle**, via the
  existing `resolve_exact`; a trailing `/` requires a directory and its absence a file;
- `from` does not point inside `lessons.generated/`;
- `to` is relative, has no unsafe component, does not begin with `tutorial/`, and is not
  absolute;
- `describe` is a non-empty string;
- a lesson-scope entry lives in a lesson that the manifest lists (in `lessons` or
  `optional_lessons`).

Report `n/a` when no `supplies` key exists anywhere. That is the common case and it must
not look like a pass.

### 5.2 Check 6 must not fight check 6

**This is the defect this design would otherwise ship.** Check 6 requires every file in a
lesson folder to be named by that folder's `LESSON.md`. A lesson that supplies
`lessons/13-load-gltf-model/model/` names the *directory* in its frontmatter, not
`Duck.glb` and not the texture beside it. Check 6 as written fires on both.

So: **a file covered by a lesson-scope `supplies` entry whose `from` is that file or a
directory prefix of it counts as named.** The declaration is a stronger statement of
intent than prose is — it says what the file is and where it goes — and check 6's own
docstring concedes that prose naming proves only naming. Check 6's `ran` line must say how
many files were satisfied by a supplies declaration rather than by prose, so a reader can
see which mechanism cleared them.

### 5.3 What the validator must not claim

Check 22 proves the entries are well-formed and the sources exist. It says nothing about
whether the supplied files are the right files, and nothing about whether a lesson still
carries prose telling the learner to copy them by hand. Section 7's audit is where that
question is asked, and the check's `ran` line must not imply otherwise.

## 6. Runner document changes

| Document | Change |
|---|---|
| `references/bundle-format.md` | a new section defining `supplies:` (4.1–4.4 above), a paragraph in the ownership section stating the exemption, a row in the manifest-key table, and a self-check item in section 10 |
| `references/state-lifecycle.md` | section 3 gains step 8: place manifest-scope supplies, then report. The existing "creating a project skeleton is the learner's action" sentence is qualified — declared supplies are the runner's. |
| `references/runner-protocol.md` | at lesson open, place that lesson's supplies before the first task; the 4.5 rule for undeclared setup prose; and an explicit prohibition on writing a file-copying task |
| `SKILL.md` | one line in the teaching loop; no new load |
| `README.md` | a line under what a bundle can declare |
| `.claude-plugin/plugin.json` | `0.3.0` → `0.4.0` — the format is additive but the runner's behaviour is new |

## 7. The authoring rules (this repository)

| File | Change |
|---|---|
| `skills/tutorail-authoring/SKILL.md` | a new rule in "The rules that override every other consideration": **toil is declared, not taught**, with the section 2 test and the named examples. A line in the delivery self-check: run the course audit before delivering. A row in the "what you write / what the toolkit writes" table putting `supplies:` on the toolkit's side. |
| `references/interview-create.md` | during the interview, capture the workspace the course assumes and the assets each lesson hands over, and record them in the spec as supplies. A lesson proposal that is only setup is not a lesson. |
| `references/interview-modify.md` | the same test for any new or changed lesson, and a named repair for the reported symptom: "the tutor made me copy files" means that prose moves into `supplies:`. |
| `references/course-spec-format.md` | a **Supplied files** section in the spec; every lesson entry states the objective it serves and the instructive failure it contains. |

## 8. `scripts/supplies.py`

Hand-editing `tutorial.yaml` is already forbidden in this skill, so declaring supplies
needs a tool. It follows the conventions the existing scripts already establish — a
`--check` run that prints what it would do, a dirty-tree refusal overridable only with
`--force`, atomic writes, and the validator run afterwards.

```
python3 scripts/supplies.py list  <bundle>
python3 scripts/supplies.py add   <bundle> --from <path> --to <path> --describe <text>
                                  [--lesson <lesson-id>] [--check] [--force]
```

`--lesson` declares the entry in that lesson's frontmatter; without it the entry goes in
the manifest. `add` refuses when `from` does not exist in the bundle, when an identical
entry is already declared, and when `to` would escape the workspace — the same conditions
check 22 enforces, refused at the point of writing rather than discovered afterwards.

`list` prints every declared entry in both scopes with its scope and its timing, which is
what the audit and the author both need to read.

## 9. The `course-quality` skill

A second skill in this plugin. Triggers: evaluate the quality of a bundle, score a course,
does this tutorial teach, audit a course, find the toil in this course.

### 9.1 What the script does, and what it refuses to do

`scripts/audit.py <bundle>` emits the part a script can produce honestly:

- the lesson skeleton: id, title, objectives, `design_refs`, `validators`, form;
- the goal inventory from `COURSE.md` and the `DESIGN.md` anchors;
- the coverage matrix of anchors and stated objectives against the lessons that reference
  them;
- every declared supplies entry, with scope;
- **candidate** toil spans as `file:line` plus the matched phrase.

The candidate scan is a candidate generator. It never rules. The skill must state, in the
report and in its own instructions, that **an empty candidate list is not evidence that a
course has no toil** — the model reads the lessons.

`audit.py`'s own tests carry a **positive control and a negative control**: a fixture
holding webgl lesson 00's copy-constraint sentence must produce a candidate, and a fixture
holding ordinary prose must not. A scanner nobody has seen fire is not a scanner.

### 9.2 The rubric (`references/rubric.md`, printed in every report)

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing |
| **unserved objective** | −3 | a stated objective or `DESIGN.md` anchor that no task exercises — counted once per course, not per lesson |

A lesson's score is the sum of its elements. The course score is the sum of the lessons
minus the gap penalties. The numbers are a way to make a judgement legible and comparable
across a long course; the rubric is printed with the report so a reader can disagree with
the scoring rather than with a bare number.

### 9.3 The report

1. the course, its lesson count, and the total;
2. a table: lesson, score, objectives served, toil found;
3. the goal gaps — every stated objective and anchor no lesson exercises;
4. the toil inventory, each entry with `file:line` and the exact sentence;
5. proposals.

### 9.4 Proposals

Every proposal names a concrete action, not a sentiment:

- a toil span becomes `python3 scripts/supplies.py add <bundle> --from … --to … --describe …`
  plus the prose to delete;
- an unserved objective becomes a lesson proposal, or an argument that the objective
  should be dropped;
- a lesson scoring at or below zero becomes a question for the author about what it is for.

The skill **proposes**. Applying goes back through `tutorail-authoring` and its toolkit,
after the author says yes. The audit never edits a bundle.

## 10. Testing

**Runner repository** — `tests/test_validate_bundle.py`: a well-formed manifest-scope
entry passes; a well-formed lesson-scope entry passes; a missing `from` is a finding; a
`from` that is a file declared with a trailing `/` is a finding; `to: ../escape` is a
finding; `to: tutorial/x` is a finding; an empty `describe` is a finding; an unknown entry
key is a finding; a lesson-scope entry in an unlisted lesson is a finding; check 22 is
`n/a` when no bundle declares supplies; **and a folder file covered by a supplies entry
does not trigger check 6 while an uncovered sibling still does.** That last pair is the
regression test for section 5.2.

**This repository** — `tests/test_supplies.py` (add and list in both scopes, every
refusal, `--check` prints and writes nothing, dirty-tree refusal) and `tests/test_audit.py`
(skeleton extraction, coverage matrix, the positive and negative scan controls, supplies
parsing). Both registered in `tests/run_all.py`.

**Pin the validator.** `tests/run_all.py` already warns that this repository's suites run
the runner's live validator through a symlink into a checkout someone may be editing —
which is exactly what this work does. Every result quoted as verification here must come
from a run against a pinned copy:

```
git -C <tutorAIl> show HEAD:skills/tutorail/scripts/validate_bundle.py > <pinned>/validate_bundle.py
```

An unpinned red suite during this work proves nothing about the code under test.

## 11. Order of work

1. Runner: `bundle-format.md` section, validator check 22, check 6 interaction, tests.
2. Runner: `state-lifecycle.md` step 8, `runner-protocol.md` lesson-open rule and the
   prose fallback, `SKILL.md`, `README.md`, version bump.
3. This repository: `scripts/supplies.py` and its tests.
4. This repository: the anti-toil rules in `SKILL.md` and the three references.
5. This repository: the `course-quality` skill, `scripts/audit.py`, `references/rubric.md`,
   tests, and registration in the plugin manifest.
6. Run the audit against `webgl-typescript-scene` and present the report.

Step 1 is the contract every later step cites, so it lands first.

## 11b. Interaction with bundle revision

Supplied files are author-supplied content sitting in the learner's workspace, so they
drift when a bundle is revised, exactly as a lesson does. The runner's design spec records
the approved answer for that whole class: **detect and report, never auto-apply.** This
design implements no drift detection, and nothing here should be read as though it does.
Placement rule 1 — never overwrite — is what keeps the two compatible: a revised supply
lands only where nothing is present, so drift detection can be added later without having
to undo anything this feature did.

## 12. Out of scope, deliberately

- **`webgl-typescript-scene` is not changed.** The audit is run against it and the report
  is presented. Acting on the report is a separate decision. Section 4.5 is what keeps
  that bundle teachable in the meantime.
- **No detector in the runner.** Section 4.5 is a rule for a reader, not a regex. A lexical
  detector that decides whether the tutor may write to learner-owned paths would be a
  false oracle guarding an ownership policy, and a false negative silently reinstates the
  toil task.
- **No scoring inside the validator.** Structural validity and pedagogical quality are
  different questions with different answers, and a validator that mixed them would make a
  green bundle look like a good course.
