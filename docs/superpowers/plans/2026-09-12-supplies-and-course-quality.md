# Supplied Files and Course Quality — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give a bundle a way to declare the files it hands the learner, so no lesson ever
assigns a file copy as a task, and add a skill that scores how much of a course teaches and
how much of it is toil.

**Architecture:** An additive `supplies:` key at `bundle_format: 1`, declared in
`tutorial.yaml` (placed after materialization) or in a lesson's frontmatter (placed when
that lesson opens). The runner places the files and reports them; it never assigns them.
The authoring skills forbid authored toil and route it into `supplies:` through a new
`supplies.py`. A second skill, `course-quality`, audits a bundle against its declared
coverage list and scores every lesson.

**Tech Stack:** Python 3, stdlib only, no pytest in either repository. YAML is read by the
project's own restricted loader `yamlite.py` and written as text.

**Spec:** `docs/superpowers/specs/2026-09-12-toil-and-course-quality-design.md`

---

## Global Constraints

- **Two repositories.** Part A is `~/src/github.com/skomp/tutorAIl` (the runner). Part B is
  `~/src/github.com/skomp/tutorail-authoring` (this one). Part A lands first: it is the
  contract Part B cites.
- **Part A happens in a git WORKTREE, branched from `origin/main` at `1697874`.** A live
  session works in that checkout, and `~/.agents/skills/tutorail` is a **symlink into its
  working tree** — anything written there changes what a running session loads, mid-edit.
  Everything is pushed, so branching from the remote loses nothing. The branch is handed
  back for that session to review and merge; do not merge it yourself.
  ```bash
  git -C ~/src/github.com/skomp/tutorAIl fetch origin
  git -C ~/src/github.com/skomp/tutorAIl worktree add -b supplies ../tutorAIl-supplies origin/main
  ```
  That session is concurrently committing to `docs/superpowers/specs/2026-09-11-tutorial-runner-design.md`
  and `TODO.md` on main. Those two paths are **theirs**; every path this plan names is
  ours. Expect to rebase before handing the branch over.
- **Part B happens on `main` in this checkout.** It was confirmed clean and unowned by the
  other session working nearby.
- **No host-specific tool name may appear in any `SKILL.md` or `references/*.md`.** Not
  `Read`, `Bash`, `Task`, `Grep`, `Edit`, `Write`, `apply_patch`, `AskUserQuestion`; no
  `${...}`; no `CLAUDE_PLUGIN_ROOT`. Sentence-initial English trips this constantly — "Read
  the file" is a violation, "Open the file" is not. It has already bitten three agents in
  the runner repository. It is enforced by convention, not by a test, so verify with a
  **case-sensitive** grep whose positive control you have watched fire:
  ```bash
  grep -rnE '\b(Read|Bash|Task|Grep|Edit|Write|apply_patch|AskUserQuestion)\b' <the files you touched>
  printf 'Read the file\n' | grep -nE '\b(Read|Bash)\b'   # positive control: must print
  ```
- **Stdlib only, Python 3.** No dependency may be added to either repository. No pytest:
  every suite is a plain `python3 tests/test_x.py` runner.
- **Never `git add -A` or `git commit -a`.** Stage the explicit paths named in the task.
  Other sessions have been committing in both repositories today.
- **If a file changes under you and you cannot account for the change, stop and report
  it.** Do not revert it, stash it, `git checkout` it or stage it. Quote the diff in your
  report and carry on with the rest of the task if you can. An unexplained edit is far more
  likely to be the owner working than corruption, and it is never yours to discard.
- **Every code block in this plan is a PROPOSAL, not a requirement.** The measurements in
  the table below were taken; the code was not run. Be sceptical. If a block is wrong,
  report the defect rather than implementing something you believe is incorrect — and if
  you conclude one of this plan's claims is wrong, say so with evidence rather than
  silently working around it.
- **Every refusal gets a positive control.** Both suites already insist on this: a probe
  that has never been shown reporting the opposite has not been tested. A new check that
  cannot be shown firing is not done.
- **Pin the validator when a result has to mean something.** This repository's suites run
  the runner's live validator through `~/.agents/skills/tutorail`, which is a **symlink**
  into the tutorAIl checkout that Part A edits. Export `TUTORAIL_VALIDATOR` at a pinned
  copy for any run quoted as verification:
  ```bash
  git -C ~/src/github.com/skomp/tutorAIl show HEAD:skills/tutorail/scripts/validate_bundle.py > /tmp/pin/validate_bundle.py
  TUTORAIL_VALIDATOR=/tmp/pin/validate_bundle.py python3 tests/run_all.py
  ```
- **Tickets and issue text use ASD-STE100 Simplified Technical English.** Code comments,
  commit messages and reference documents keep their normal voice.
- **Commit message trailer**, on every commit in both repositories:
  ```
  Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01C2TnyNEjDWaDuDuKdp2XaW
  ```

## Already measured — do not re-derive

Taken on this machine 2026-09-12, tutorAIl at `1697874`, tutorail-authoring at `310e37f`,
tutorail-bundles at `76dcdce` or later.

| Fact | Evidence |
|---|---|
| `yamlite.load_yaml` **does** parse a block sequence of mappings, and a double-quoted scalar containing `:` | ran against `/Users/robert/.agents/skills/tutorail/scripts/yamlite.py`; `supplies` came back as a `list` of `dict` with `describe` = `Duck.glb: the sample model` |
| The validator rejects neither unknown manifest keys nor unknown lesson frontmatter keys. Only `catalog.yaml` gets an unknown-key check | `validate_bundle.py:2478` is the only one |
| `CHECKS` runs 1–21; `BUNDLE_ONLY = {12, 13}`, `INSTANCE_ONLY = {11, 14, 15, 17, 21}`. **22 is free** | `validate_bundle.py:77`–`:106` |
| `tests/test_validate_bundle.py` ends in a **meta-test that fails when any check in `CHECKS` has no fixture that makes it fire**. Adding check 22 without a mutator turns the suite red | `tests/test_validate_bundle.py:2470` |
| Its case table is `CASES: list[Case]`, entries `Case(name, check_number, baseline, mode, mutator, expected_substring)`, baselines `"automaton"` and `"cli"` | `tests/test_validate_bundle.py:1388`, `:1404` |
| `resolve_exact(base, rel)` already refuses unsafe path components, returning `(None, "path component %r is not allowed")` | `validate_bundle.py:447`, `:462` |
| Check 6 (`check_material_reachable`) walks every file in a lesson **folder** and requires `names_file(LESSON.md text, folder-relative path)`; it matches the folder-relative path or the bare basename as a delimited token | `validate_bundle.py:1081`, `:1115` |
| Lesson body sections are normative: Purpose, Prerequisites, Learning objectives, Theory, Concepts to teach, Constraints, Suggested progression, Completion conditions, On completion persist, Optional deeper paths | `bundle-format.md:609`–`:662` |
| `COURSE.md` SHOULD carry a **coverage list**: a heading naming what it is, then one topic per line. It is the only part of `COURSE.md` the tutor reads mechanically, and topics are named as a learner would ask, not as lessons are titled | `bundle-format.md:390`–`:445` |
| A lesson in `lessons/` is listed in `lessons` **or** in `optional_lessons` — "exactly once in `lessons`" is no longer true | `bundle-format.md` sections 2, 6, 12, 13, from tutorAIl `9dbbcd4` |
| `failure_modes` is a second additive key: stable id → `summary`, `signals` | `bundle-format.md:304` |
| `bundlelib` gives Part B: `find_validator()`, `load_bundle(root)`, `require_clean_tree(root, force)`, `Staged(root, check_only=)` with `stage.root` and `stage.commit() -> ValidatorRun`, `read_text`, `atomic_write_text`, `split_frontmatter`, `frontmatter_span`, `set_frontmatter_field` (**scalars only**), `replace_lessons_list`, `ToolError`, `run_main` | `skills/tutorail-authoring/scripts/bundlelib.py` |
| The authoring harness gives: `Workspace`, `case`, `check`, `check_in`, `check_not_in`, `run(script, *args)` → `.output`, `tree_digest`, `listing`, `has_exactly`, `git_init`, `write_stub_validator`, `no_runner_env`, `report` | `tests/harness.py` |
| `TUTORAIL_VALIDATOR` is the env var the validator search consults first | `tests/harness.py:no_runner_env` |
| The webgl bundle's toil is exactly two sites | `lessons/00-project-setup/LESSON.md:34`, `lessons/13-load-gltf-model/LESSON.md:40` |
| **The negative control for the toil scanner already exists in the corpus**: `webgl-typescript-scene/lessons/15-render-to-texture.md:41` reads "Provide a direct-copy composition shader before adding effects." A scanner that fires on the word `copy` fires here, and it must not | grep over the bundle |
| `durable-event-broker` in `tutorail-bundles` is the first real bundle using `optional_lessons` | reported by a peer session, 2026-09-12 |
| **Runner suite baseline at `1697874`: `tests/test_validate_bundle.py` = 252 assertions, `tests/test_catalogs.py` = 158. Both green.** Check 22 and the check 6 fix must leave both green | measured by the session working in that repository, 2026-09-12 |
| The runner has **three** manifests to keep in step, all at `0.3.0`: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`. `claude plugin validate .` checks their consistency | same source |
| **An install compares the manifest VERSION, not the content.** `claude plugin update` reported `0.1.0` as "already at the latest version" while the installed copy was missing a whole feature. A `supplies:` that ships without a bump reaches no installed copy | same source, observed today |
| This repository has **two** manifests, both at `0.1.0`: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`. There is no `.codex-plugin` here | `grep -rn '"version"' .claude-plugin/*.json` |

---

# Part A — the runner (`~/src/github.com/skomp/tutorAIl`)

### Task A1: check 22 — `supplies` entries are well-formed

**Files:**
- Modify: `skills/tutorail/scripts/validate_bundle.py` (`CHECKS` at `:77`, new functions, wiring in `validate()` at `:2250`)
- Test: `tests/test_validate_bundle.py` (mutators beside the others, entries in `CASES`)

**Interfaces:**
- Consumes: `resolve_exact`, `as_list`, `_is_text`, `Lesson`, `Report`, `load_yaml`, `split_frontmatter`
- Produces, relied on by A2 and Part B:
  - `collect_supplies(root: Path, manifest: Any, lessons: list[Lesson]) -> list[tuple[str, dict]]`
    — `(where, entry)` pairs, `where` being `"tutorial.yaml"` or the lesson's `rel`. It
    returns only entries that are mappings; malformed ones are reported by the caller.
  - `supplies_covers(entries: list[dict], bundle_rel: str) -> bool` — True when any entry's
    `from` equals `bundle_rel` or is a directory prefix of it, matched on path boundaries.
  - `CHECKS[22] = "supplies entries are well-formed, and every 'from' exists"`

- [ ] **Step 1: Write the failing tests**

Add the mutators beside the existing ones, and the cases to `CASES`. The baseline
`"automaton"` has no `supplies` key, so each mutator installs one and then breaks exactly
one thing — that is what makes the message attributable.

```python
def m_supplies_from_missing(root: Path) -> None:
    append(root / "tutorial.yaml", """
supplies:
  - from: supplies/workspace/
    to: .
    describe: the workspace this course assumes
""")


def m_supplies_from_is_a_file_declared_as_a_directory(root: Path) -> None:
    (root / "supplies").mkdir()
    (root / "supplies" / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
    append(root / "tutorial.yaml", """
supplies:
  - from: supplies/Cargo.toml/
    to: Cargo.toml
    describe: the manifest this course assumes
""")


def m_supplies_to_escapes_the_workspace(root: Path) -> None:
    (root / "supplies").mkdir()
    (root / "supplies" / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
    append(root / "tutorial.yaml", """
supplies:
  - from: supplies/Cargo.toml
    to: ../Cargo.toml
    describe: the manifest this course assumes
""")


def m_supplies_to_is_inside_the_instance(root: Path) -> None:
    (root / "supplies").mkdir()
    (root / "supplies" / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
    append(root / "tutorial.yaml", """
supplies:
  - from: supplies/Cargo.toml
    to: tutorial/Cargo.toml
    describe: the manifest this course assumes
""")


def m_supplies_describe_is_empty(root: Path) -> None:
    (root / "supplies").mkdir()
    (root / "supplies" / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
    append(root / "tutorial.yaml", """
supplies:
  - from: supplies/Cargo.toml
    to: Cargo.toml
    describe: ""
""")


def m_supplies_unknown_entry_key(root: Path) -> None:
    (root / "supplies").mkdir()
    (root / "supplies" / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
    append(root / "tutorial.yaml", """
supplies:
  - from: supplies/Cargo.toml
    to: Cargo.toml
    description: the manifest this course assumes
""")


def m_supplies_in_an_unlisted_lesson(root: Path) -> None:
    (root / "supplies").mkdir()
    (root / "supplies" / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
    (root / "lessons" / "99-orphan.md").write_text(
        "---\n"
        "id: 99-orphan\n"
        "title: Orphan\n"
        "supplies:\n"
        "  - from: supplies/Cargo.toml\n"
        "    to: Cargo.toml\n"
        "    describe: the manifest this course assumes\n"
        "---\n\n## Purpose\n\nNothing.\n",
        encoding="utf-8",
    )
```

```python
    # ---- check 22
    Case("22: a supplies 'from' does not exist in the bundle", 22, "automaton",
         "bundle", m_supplies_from_missing, "'supplies/workspace/' does not resolve"),
    Case("22: a file is declared with a trailing slash", 22, "automaton", "bundle",
         m_supplies_from_is_a_file_declared_as_a_directory,
         "trailing '/' means a directory"),
    Case("22: a supplies 'to' escapes the workspace", 22, "automaton", "bundle",
         m_supplies_to_escapes_the_workspace, "path component '..' is not allowed"),
    Case("22: a supplies 'to' points inside the instance", 22, "automaton", "bundle",
         m_supplies_to_is_inside_the_instance, "'tutorial/' is the instance"),
    Case("22: describe is empty", 22, "automaton", "bundle",
         m_supplies_describe_is_empty, "'describe' must be a non-empty"),
    Case("22: an entry carries an unknown key", 22, "automaton", "bundle",
         m_supplies_unknown_entry_key, "unknown key 'description'"),
    Case("22: a lesson that is not listed declares supplies", 22, "automaton",
         "bundle", m_supplies_in_an_unlisted_lesson, "is not listed"),
```

- [ ] **Step 2: Run them and watch every one fail**

```bash
cd ~/src/github.com/skomp/tutorAIl && python3 tests/test_validate_bundle.py
```

Expected: the seven new cases fail because check 22 does not exist, **and** the meta-test
now reports check 22 as having no fixture — read both, because the meta-test failing on its
own would mean the cases are not wired to the number.

- [ ] **Step 3: Implement check 22**

Proposal. `SUPPLIES_KEYS = ("from", "to", "describe")`.

```python
def collect_supplies(root, manifest, lessons):
    """Every declared supplies entry, as (where, entry). Malformed lists are skipped."""
    out = []
    if isinstance(manifest, dict):
        entries = as_list(manifest.get("supplies"))
        if entries:
            out.extend(("tutorial.yaml", e) for e in entries)
    for lesson in lessons:
        text = read_text(lesson.path)
        if text is None:
            continue
        fm_text, _ = split_frontmatter(text)
        if fm_text is None:
            continue
        try:
            fm = load_yaml(fm_text, lesson.rel + " frontmatter")
        except YamlError:
            continue
        if not isinstance(fm, dict):
            continue
        entries = as_list(fm.get("supplies"))
        if entries:
            out.extend((lesson.rel, e) for e in entries)
    return out
```

`check_supplies(root, manifest, lessons, listed_rels, report)` then walks those pairs and
reports, per entry: a non-mapping entry; an unknown key; a missing `from`, `to` or
`describe`; a `describe` that is not a non-empty string; a `from` that does not resolve
through `resolve_exact` against the bundle root; a trailing-`/` mismatch with what is on
disk; a `from` under `lessons.generated/`; a `to` that is absolute, contains a component
`resolve_exact` refuses, or begins with `tutorial/`; and a lesson-scope entry whose lesson
is in neither `lessons` nor `optional_lessons`. When `collect_supplies` returns nothing,
`report.na(22, "no bundle declares supplies")`.

Wire it into `validate()` beside the other check calls, and add the `CHECKS[22]` line.

**`to` is validated as a path, not resolved on disk.** The workspace does not exist at
validation time. Reuse `resolve_exact`'s component rule by splitting `to` yourself; do not
call `resolve_exact` against the bundle root for a `to`, which would be meaningless.

- [ ] **Step 4: Run the tests and watch them pass**

```bash
cd ~/src/github.com/skomp/tutorAIl && python3 tests/test_validate_bundle.py
```

Expected: PASS, including the meta-test.

- [ ] **Step 5: Prove the check passes a good bundle too**

Add one positive control: a fixture copy with a well-formed manifest-scope entry **and** a
well-formed lesson-scope entry reports no check-22 finding. Without it, every one of the
seven cases above is consistent with a check that always fires.

- [ ] **Step 6: Commit**

```bash
cd ~/src/github.com/skomp/tutorAIl
git add skills/tutorail/scripts/validate_bundle.py tests/test_validate_bundle.py
git commit -m "Add check 22: supplies entries are well-formed"
```

---

### Task A2: check 6 must not fire on supplied material

**Files:**
- Modify: `skills/tutorail/scripts/validate_bundle.py:1115` (`check_material_reachable`)
- Test: `tests/test_validate_bundle.py`

**Interfaces:**
- Consumes: `collect_supplies`, `supplies_covers` from A1
- Produces: nothing new

This is the defect the design would otherwise ship. A lesson that supplies
`lessons/13-load-gltf-model/model/` names the **directory** in its frontmatter. Check 6
walks the files and demands each be named. `Duck.glb` is not named, so check 6 fires on a
bundle that is correct.

- [ ] **Step 1: Write the failing test — and its negative half in the same fixture**

The fixture is a foldered lesson with two material files: one covered by a supplies entry,
one not. The covered one must produce no finding; the uncovered one must still produce
one. A test that only asserts the first would pass against a check 6 that had been
disabled altogether.

```python
def m_supplied_material_and_an_uncovered_sibling(root: Path) -> None:
    """Check 6 must ignore the supplied file and still catch the other one."""
    folder = root / "lessons" / "01-subcommands"        # baseline "cli" is foldered
    (folder / "model").mkdir()
    (folder / "model" / "Duck.glb").write_bytes(b"glTF\x02\x00\x00\x00")
    (folder / "stray.txt").write_text("never named\n", encoding="utf-8")
    lesson = folder / "LESSON.md"
    edit(lesson, "id: 01-subcommands", (
        "id: 01-subcommands\n"
        "supplies:\n"
        "  - from: lessons/01-subcommands/model/\n"
        "    to: models/\n"
        "    describe: the sample model this lesson loads"
    ))
```

```python
    Case("6: a material file no LESSON.md names", 6, "cli", "bundle",
         m_supplied_material_and_an_uncovered_sibling, "'stray.txt' is never named"),
```

and a separate assertion, in the same run, that the output does **not** contain
`Duck.glb` — use the suite's negative-assertion idiom rather than only checking the
positive.

- [ ] **Step 2: Run it and watch it fail on the wrong file**

Expected before the fix: findings for **both** `stray.txt` and `model/Duck.glb`. Read the
output; the failure must be the `Duck.glb` finding, not a missing `stray.txt` one.

- [ ] **Step 3: Implement the exemption**

Proposal, inside `check_material_reachable`, before the `names_file` call:

```python
        if supplies_covers(supplies_entries, f"{lesson.rel_folder}/{rel_in_folder}"):
            supplied += 1
            continue
```

where `supplies_entries` is every entry `collect_supplies` returned, from any scope — a
file declared anywhere in the bundle is declared. `supplies_covers` matches on path
boundaries: `from` equal to the path, or `from.rstrip("/") + "/"` a prefix of it. A
`from` of `model` must not cover `model2/x.bin`.

Then say so in the `ran` line, because a reader has to be able to tell which mechanism
cleared a file:

```python
    report.ran(6, f"{checked} material files in {len(foldered)} lesson folders "
                  f"({supplied} cleared by a supplies declaration); names only, not intent")
```

- [ ] **Step 4: Run the tests and watch them pass**

```bash
cd ~/src/github.com/skomp/tutorAIl && python3 tests/test_validate_bundle.py
```

Expected: PASS. The `stray.txt` finding is still there; `Duck.glb` is gone.

- [ ] **Step 5: Commit**

```bash
git add skills/tutorail/scripts/validate_bundle.py tests/test_validate_bundle.py
git commit -m "Stop check 6 firing on material a lesson supplies"
```

---

### Task A3: the format contract

**Files:**
- Modify: `skills/tutorail/references/bundle-format.md` — a new section after section 2's
  `failure_modes` subsection, a row in the field reference at `:129`, a paragraph in the
  ownership material, and an item in section 10's self-check at `:918`

**Interfaces:**
- Consumes: the shape A1 validates. The document and the validator must agree exactly;
  where they differ, the document is normative and the validator has the defect.
- Produces: the contract Part B cites.

- [ ] **Step 1: Write the section**

It must state, in this order and without inventing anything beyond it:

1. What `supplies:` is for, in one sentence — the files the bundle hands the learner's
   workspace, so that no lesson ever assigns a copy as a task.
2. The three fields, `from` (bundle-root-relative in **both** scopes, trailing `/` meaning
   the contents of a directory), `to` (workspace-root-relative, never inside `tutorial/`),
   `describe` (required, non-empty, one line, the sentence the runner says to the learner).
3. Scope decides timing: manifest → right after materialization; lesson frontmatter → when
   that lesson opens, before its first task.
4. The four placement rules: never overwrite; silence when every target already exists;
   report exactly what was placed when some were missing; name it as setup, not a lesson.
5. The ownership exemption, stated as narrowly as the spec states it: under
   `tutor-must-not-edit-learner-owned` the tutor **may create** a declared supplies target
   that does not exist and may **never modify** one that does; undeclared paths get no
   exemption.
6. That the key is additive to `bundle_format: 1`, and that an older runner ignores it —
   which is the same failure those bundles have today, not a new one.
7. That a file covered by a supplies entry satisfies section 6's material-naming rule,
   because the declaration says more than a prose mention does.
8. **What happens when a target exists and differs.** It is left exactly as it is and
   **named in the report** — the runner says which files it placed and which it left
   alone, so a learner is never left guessing whether their own file was replaced. This is
   the sharpest edge in the feature: a lesson-scope entry can land on a `learner_owned`
   path, and silently overwriting a learner's work would be the worst outcome this format
   can produce. Say so in the document, not only in the rules table.

A note for the reader, and for whoever implements bundle-revision drift later: supplied
files are author-supplied content sitting in the learner's workspace, so they drift when a
bundle is revised, exactly like a lesson does. The decision recorded in the runner's
design spec is **detect and report, never auto-apply**. This plan implements no drift
detection; it must not be written as though it does.

- [ ] **Step 2: Add the self-check item to section 10**

One line, in the voice of the items already there: every `supplies` entry names a file that
exists, lands outside `tutorial/`, and carries a `describe` a learner would understand.

- [ ] **Step 3: Check the document against the validator, by looking**

Read A1's implemented conditions and this section side by side. Any disagreement is a
defect in one of them — fix it now and say which one was wrong. Do not leave the two to be
reconciled later by a reader who trusts whichever they open first.

- [ ] **Step 4: Commit**

```bash
git add skills/tutorail/references/bundle-format.md
git commit -m "Define supplies: the files a bundle hands the learner"
```

---

### Task A4: the runner's behaviour

**Files:**
- Modify: `skills/tutorail/references/state-lifecycle.md` (section 3, `:101`–`:160`)
- Modify: `skills/tutorail/references/runner-protocol.md`
- Modify: `skills/tutorail/SKILL.md`, `README.md`, `.claude-plugin/plugin.json`,
  `.codex-plugin/plugin.json`

- [ ] **Step 1: `state-lifecycle.md` section 3 gains step 8**

After step 7 ("report what was created"), place manifest-scope supplies and report them.
Then qualify the existing sentence at `:157`, which currently reads that creating a project
skeleton is the learner's action: declared supplies are the runner's, and nothing else
changes.

- [ ] **Step 2: `runner-protocol.md` gains the lesson-open rule and the prose fallback**

Two paragraphs:

- when a lesson opens, place that lesson's supplies before writing its first task, under
  the same four placement rules;
- **the rule for bundles that predate the key.** When a lesson's prose instructs the
  learner to copy, download or unzip files the bundle itself carries, do it, report it as
  setup handled, and note that the bundle should declare it in `supplies:`. Never write it
  as a task.

State plainly that this is a judgement a reader makes with the lesson in front of it, and
that it must not become a lexical detector. A regex deciding when the tutor may write to
learner-owned paths would be a false oracle guarding an ownership policy, and its false
negatives silently reinstate the toil task.

- [ ] **Step 3: `SKILL.md` and `README.md`**

One line each. `SKILL.md` names the new step in the teaching loop; `README.md` adds
`supplies` to what a bundle can declare. No new reference load.

- [ ] **Step 4: Version bump**

`0.3.0` → `0.4.0` in **all three** manifests: `.claude-plugin/plugin.json`,
`.claude-plugin/marketplace.json` and `.codex-plugin/plugin.json`. The format is additive;
the runner's behaviour is new.

This is not bookkeeping. An install compares the version, not the content: today
`claude plugin update` reported `0.1.0` as "already at the latest version" while the
installed copy was missing an entire feature. A `supplies:` that ships without a bump
reaches nobody.

```bash
grep -rn "0\.3\.0" . --include=*.json --include=*.md | grep -v '^./.git'
claude plugin validate .
```

Report how many instances you found and how many you changed. A version that lives in three
places and is changed in two is the failure this step exists to avoid.

- [ ] **Step 5: Run the full runner suite**

```bash
cd ~/src/github.com/skomp/tutorAIl && python3 tests/test_validate_bundle.py && python3 tests/test_catalogs.py
```

Expected: both PASS, at **252 and 158 assertions** — the baseline measured at `1697874`.
A lower count means a case stopped running, which a green line will not tell you.

- [ ] **Step 6: Commit**

```bash
git add skills/tutorail/references/state-lifecycle.md skills/tutorail/references/runner-protocol.md \
        skills/tutorail/SKILL.md README.md \
        .claude-plugin/plugin.json .claude-plugin/marketplace.json .codex-plugin/plugin.json
git commit -m "Place declared supplies instead of assigning them"
```

---

# Part B — authoring and quality (`~/src/github.com/skomp/tutorail-authoring`)

### Task B1: bundlelib writes a supplies entry

**Files:**
- Modify: `skills/tutorail-authoring/scripts/bundlelib.py`
- Test: `tests/test_supplies.py` (new; the unit half)

**Interfaces:**
- Consumes: `frontmatter_span`, `split_frontmatter`, `ToolError`, `load_yaml`
- Produces, relied on by B2:
  - `emit_scalar(value: str) -> str` — a single-line YAML scalar `yamlite` reads back as
    `value`
  - `render_supplies_item(entry: dict) -> list[str]` — the block-sequence item lines for
    one entry, two-space indented, keys in the order `from`, `to`, `describe`
  - `add_supplies(text: str, entry: dict, *, frontmatter: bool) -> str` — the text with the
    entry appended to its `supplies:` block, creating the block when absent. Raises
    `ToolError` when the result does not read back as expected.

`set_frontmatter_field` writes scalars only and cannot be used here. Model
`add_supplies` on `replace_lessons_list` at `bundlelib.py:714`, which already does this
class of surgery on the manifest text.

- [ ] **Step 1: Write the failing tests**

```python
def test_emit_scalar_round_trips_the_hard_cases() -> None:
    for value in [
        "npm workspace",
        "Duck.glb: the sample model",              # a colon
        "the #1 thing this lesson needs",          # a hash
        "  leading and trailing  ",                # whitespace that YAML would eat
        'she said "copy it"',                      # quotes
        "a - b",                                   # a dash
        "{not a flow mapping}",                    # a brace
    ]:
        doc = f"describe: {bl.emit_scalar(value)}\n"
        back = load_yaml(doc, "probe")
        check(back["describe"] == value, f"emit_scalar round-trips {value!r}")


def test_add_supplies_creates_the_block_then_appends_to_it() -> None:
    text = "bundle_format: 1\nid: x\n"
    entry = {"from": "supplies/workspace/", "to": ".", "describe": "the workspace"}
    once = bl.add_supplies(text, entry, frontmatter=False)
    twice = bl.add_supplies(once, {"from": "m/", "to": "models/",
                                   "describe": "the model"}, frontmatter=False)
    parsed = load_yaml(twice, "probe")
    check(len(parsed["supplies"]) == 2, "two entries after two adds")
    check(parsed["supplies"][0] == entry, "the first entry survived the second add")
    check(parsed["id"] == "x", "the rest of the manifest is untouched")


def test_add_supplies_in_frontmatter_leaves_the_body_alone() -> None:
    text = "---\nid: 00-x\ntitle: X\n---\n\n## Purpose\n\nTeach something.\n"
    out = bl.add_supplies(text, {"from": "lessons/00-x/model/", "to": "models/",
                                 "describe": "the model"}, frontmatter=True)
    fm, body = bl.split_frontmatter(out)
    check(load_yaml(fm, "probe")["supplies"][0]["to"] == "models/", "entry is in the frontmatter")
    check(body.strip().startswith("## Purpose"), "the body is unchanged")
```

- [ ] **Step 2: Run and watch them fail**

```bash
cd ~/src/github.com/skomp/tutorail-authoring && python3 tests/test_supplies.py
```

Expected: `AttributeError: module 'bundlelib' has no attribute 'emit_scalar'`.

- [ ] **Step 3: Implement**

Proposal for the one part that is easy to get subtly wrong:

```python
_PLAIN_SCALAR_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9 ._/-]*\Z")


def emit_scalar(value: str) -> str:
    """A single-line YAML scalar that yamlite reads back as `value`.

    Conservative on purpose: anything that is not obviously plain is quoted.
    A wrong answer here writes a manifest that parses into something the
    author did not type, which is the quiet kind of corruption.
    """
    if _PLAIN_SCALAR_RE.match(value) and value == value.strip():
        return value
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
```

`add_supplies` ends by parsing its own output and comparing the appended entry to the
`entry` it was given, raising `ToolError` when they differ. That round-trip is the only
honest proof that the emitter and the loader agree, and it costs one parse.

- [ ] **Step 4: Run and watch them pass**

- [ ] **Step 5: Commit**

```bash
git add skills/tutorail-authoring/scripts/bundlelib.py tests/test_supplies.py
git commit -m "Teach bundlelib to write a supplies entry"
```

---

### Task B2: `supplies.py list` and `supplies.py add`

**Files:**
- Create: `skills/tutorail-authoring/scripts/supplies.py`
- Modify: `tests/test_supplies.py`, `tests/harness.py` (add `SUPPLIES = SCRIPTS / "supplies.py"`)
- Modify: `tests/run_all.py` (register the suite)

**Interfaces:**
- Consumes: B1's `add_supplies`; `bl.find_validator`, `bl.load_bundle`,
  `bl.require_clean_tree`, `bl.Staged`, `bl.run_main`
- Produces: the CLI the authoring skill and the quality skill both name:

```
python3 scripts/supplies.py list <bundle>
python3 scripts/supplies.py add  <bundle> --from <path> --to <path> --describe <text>
                                 [--lesson <lesson-id>] [--check] [--force]
```

Follow `lesson.py add` exactly: `bl.find_validator()` **first**, before reading the bundle
and before the dirty-tree check, so a machine with no runner cannot reach a clean-looking
exit; then `load_bundle`, `require_clean_tree`, the refusals, the printed plan, then
`with bl.Staged(root, check_only=args.check) as stage:` and `stage.commit()`.

- [ ] **Step 1: Write the failing tests**

Every refusal, each with the positive control that differs only in the thing under test,
and each followed by a `tree_digest` comparison rather than "the file is absent":

```python
with case("add refuses a --from that is not in the bundle"):
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db")
        git_init(bundle)
        before = tree_digest(bundle)
        out = run(SUPPLIES, "add", bundle, "--from", "supplies/nope/",
                  "--to", ".", "--describe", "the workspace")
        check(out.returncode != 0, "it refused")
        check_in("does not exist in the bundle", out.output, "and said why")
        check(tree_digest(bundle) == before, "the bundle is byte-identical")

with case("positive control: the same add succeeds once the file exists"):
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db")
        (bundle / "supplies").mkdir()
        (bundle / "supplies" / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
        git_init(bundle)
        before = tree_digest(bundle)
        out = run(SUPPLIES, "add", bundle, "--from", "supplies/Cargo.toml",
                  "--to", "Cargo.toml", "--describe", "the manifest this course assumes")
        check(out.returncode == 0, "it succeeded")
        check(tree_digest(bundle) != before, "and the digest oracle can tell")
```

The refusals to cover: `--from` missing from the bundle; `--to` escaping the workspace
(`../x`); `--to` starting `tutorial/`; an empty `--describe`; an identical entry already
declared; `--lesson` naming a lesson that does not exist; a dirty working tree (with
`--force` as its positive control); and `--check` printing the plan while leaving the
digest unchanged.

`list` gets one test: with one manifest-scope and one lesson-scope entry declared, the
output names both, says which scope each is in, and says when each is placed.

- [ ] **Step 2: Run and watch every one fail**

- [ ] **Step 3: Implement `supplies.py`**

Refuse before staging, with a message that names the cause the way the other scripts do.
`--lesson` takes a lesson **id** and is resolved through `bundle.by_rel` / the lesson
slugs — not a path, because an id is what the author has in front of them and what
`index.py` prints.

The `add` plan printed before writing, in the shape `lesson.py add` uses:

```
add: supplies entry (manifest scope, placed after materialization)
     from     supplies/workspace/
     to       .
     describe the workspace this course assumes
```

- [ ] **Step 4: Run and watch them pass, against a PINNED validator**

Pin at **Part A's worktree**, not at the runner's `main` — main does not have check 22
until the branch is merged, and `~/.agents/skills/tutorail` resolves to main through a
symlink.

```bash
mkdir -p /tmp/pin
cp ~/src/github.com/skomp/tutorAIl-supplies/skills/tutorail/scripts/validate_bundle.py /tmp/pin/validate_bundle.py
cd ~/src/github.com/skomp/tutorail-authoring
TUTORAIL_VALIDATOR=/tmp/pin/validate_bundle.py python3 tests/test_supplies.py
```

Expected: PASS. Say in your report which validator you pinned and at which commit. A run
whose validator you cannot name is a run that proves nothing.

- [ ] **Step 5: Commit**

```bash
git add skills/tutorail-authoring/scripts/supplies.py tests/test_supplies.py tests/harness.py tests/run_all.py
git commit -m "Add supplies.py: declare the files a bundle hands the learner"
```

---

### Task B3: the anti-toil rules

**Files:**
- Modify: `skills/tutorail-authoring/SKILL.md`
- Modify: `skills/tutorail-authoring/references/interview-create.md`
- Modify: `skills/tutorail-authoring/references/interview-modify.md`
- Modify: `skills/tutorail-authoring/references/course-spec-format.md`

No tests: these are instructions to a reader. The verification is Step 5.

- [ ] **Step 1: `SKILL.md` — the rule**

A fourth entry in "The rules that override every other consideration", in the voice of the
three already there. It must carry:

- the name: **toil is declared, not taught**;
- the test, verbatim: *what can the learner get wrong here, and does getting it wrong teach
  anything? If nothing, it is not a task — it is `supplies:`*;
- the named examples: copying files, installing dependencies, downloading assets,
  unzipping, pasting supplied code verbatim;
- the evidence, because a rule with a scar attached is followed and an abstract one is not:
  a generated course opened its first lesson by having the learner copy five files out of
  `starter/`, and the author had no other channel.

- [ ] **Step 2: `SKILL.md` — two table rows and one self-check line**

Add `supplies:` to the toolkit's column in "What you write, and what the toolkit writes",
add `supplies.py` to the toolkit command table, and add one line to the delivery
self-check: run the course audit (`course-quality`) before delivering, because the
validator being green says nothing about whether the course teaches.

- [ ] **Step 3: `interview-create.md`**

Two additions. During the interview, ask what the learner's workspace must already contain
and what each lesson hands over, and record both in the spec as supplies. When a proposed
lesson turns out to be only setup, it is not a lesson: say so and fold it into `supplies:`.

- [ ] **Step 4: `interview-modify.md` and `course-spec-format.md`**

`interview-modify.md`: the same test for every new or changed lesson, and a named repair
for the symptom an author actually reports — "the tutor made me copy files" means that
prose moves into `supplies:` with `supplies.py add`.

`course-spec-format.md`: a **Supplied files** section in the spec, and every lesson entry
states the objective it serves and the instructive failure it contains. Update the format's
own self-check list to match, or the section will be written once and never again.

- [ ] **Step 5: Verify by grepping, not by remembering**

```bash
cd ~/src/github.com/skomp/tutorail-authoring
grep -rn "supplies" skills/tutorail-authoring/SKILL.md skills/tutorail-authoring/references/
grep -rn "starter/" skills/tutorail-authoring/
```

Every one of the four files must appear in the first result. Report the count.

- [ ] **Step 6: Commit**

```bash
git add skills/tutorail-authoring/SKILL.md skills/tutorail-authoring/references/
git commit -m "Forbid authored toil: declare it, do not teach it"
```

---

### Task B4: `audit.py` — the evidence a script can honestly produce

**Files:**
- Create: `skills/course-quality/scripts/audit.py`
- Create: `tests/test_audit.py`
- Create: `tests/fixtures/toil-course/` (a small bundle carrying both controls)
- Modify: `tests/harness.py` — **a new base constant, not a fifth sibling.** `SCRIPTS`
  points at `skills/tutorail-authoring/scripts`; `audit.py` belongs to the course-quality
  skill, so it needs its own base, and a second session's `dryrun.py` will hang off the
  same one:

  ```python
  QUALITY_SCRIPTS = REPO / "skills" / "course-quality" / "scripts"

  AUDIT = QUALITY_SCRIPTS / "audit.py"
  ```

- `tests/run_all.py` needs **no edit**: it discovers suites with
  `sorted(HERE.glob("test_*.py"))` at line 72. Add the suite to `NEEDS_CLEAN_SEARCH`
  (line 67) only if it manipulates `TUTORAIL_VALIDATOR`, which this one does not.

**Interfaces:**
- Consumes: `bl.load_bundle`, `bl.Lesson`, `bl._ANCHOR_RE`, `yamlite.load_yaml`
- Produces, relied on by the skill in B5:

```
python3 scripts/audit.py <bundle> [--json]
```

Default output is a Markdown skeleton for a reader to fill in. `--json` is the same data as
a JSON object, and is what the tests read. Both carry, per bundle:

- `course`: id, title, lesson count, optional-lesson count;
- `coverage_list`: the topics from `COURSE.md`'s coverage list, verbatim, with the heading
  they were found under — and an explicit `null` when the course declares none, which is
  a finding in itself and must not look like an empty list;
- `anchors`: every `{#anchor}` in `DESIGN.md`;
- `lessons`: for each, `rel`, `id`, `title`, `optional`, `form`, `design_refs`,
  `validators`, and the bullets under `## Learning objectives`;
- `supplies`: every declared entry with its scope;
- `candidates`: possible toil, each with `rel`, `line`, `text` and the `pattern` name that
  matched.

- [ ] **Step 1: Build the fixture carrying both controls**

`tests/fixtures/toil-course/` is a minimal valid bundle with a coverage list under the
heading `## Topics this course must cover`, holding exactly three topics in this order:
`shader compilation`, `depth testing`, `texture sampling`. One of the three is taught by no
lesson, so the gap case has something to find.

`tests/fixtures/toil-course-no-coverage/` is the same bundle with that section deleted. It
exists so the coverage-list parser can be shown reporting absence, which is the one thing
a parser that returns an empty list on every input would also appear to do.

One lesson's Constraints section carries the real sentence from the corpus:

> Copy `starter/package.json`, `starter/tsconfig.json` and `starter/src/main.ts` into
> their corresponding repository-root paths, preserving `src/`.

and another lesson's Theory carries the real negative control, also from the corpus:

> Provide a direct-copy composition shader before adding effects.

Both sentences contain the word "copy". Only the first is an instruction to the learner.

- [ ] **Step 2: Write the failing tests**

```python
with case("the scanner fires on a real copy-the-starter constraint"):
    data = audit_json(FIXTURES / "toil-course")
    hits = [c for c in data["candidates"] if "starter/package.json" in c["text"]]
    check(len(hits) == 1, "the copy-the-starter sentence is a candidate")
    check(hits[0]["pattern"] == "copy", "and it says which pattern matched")

with case("NEGATIVE CONTROL: it does not fire on 'a direct-copy composition shader'"):
    data = audit_json(FIXTURES / "toil-course")
    hits = [c for c in data["candidates"] if "composition shader" in c["text"]]
    check(not hits, "prose that merely contains 'copy' is not a candidate")

with case("the coverage list comes back verbatim, under its own heading"):
    data = audit_json(FIXTURES / "toil-course")
    check(data["coverage_list"]["heading"] == "Topics this course must cover",
          "the heading the topics were found under is reported")
    check(data["coverage_list"]["topics"] == ["shader compilation", "depth testing",
                                              "texture sampling"],
          "every topic is reported verbatim, in order")

with case("NEGATIVE CONTROL: a course with no coverage list reports null, not empty"):
    # `toil-course-no-coverage` is the same fixture with the section deleted.
    # Without this case the assertion above is consistent with a parser that
    # cannot tell an absent section from an empty one, which is the
    # distinction the whole field exists to make.
    data = audit_json(FIXTURES / "toil-course-no-coverage")
    check(data["coverage_list"] is None, "absent is null")
    check(data["coverage_list"] != [], "absent is not an empty list")

with case("an optional lesson is inventoried, not reported as unreachable"):
    data = audit_json(FIXTURES / "toil-course")
    optional = [l for l in data["lessons"] if l["optional"]]
    check(len(optional) == 1, "the optional lesson is listed")
```

The fixture therefore needs one optional lesson, declared in `optional_lessons` with
`optional: true` in its frontmatter. **A lesson in `lessons/` is listed in `lessons` OR in
`optional_lessons`** — code that cross-references only the ordered list reports every
optional lesson as unreachable.

- [ ] **Step 3: Run and watch them fail**

**Run `audit.py` as a SUBPROCESS, the way every other suite here runs its script — the
`audit_json` helper shells out to `--json` and parses stdout. Do not import it as a
module.** `harness.py:49` already does `sys.path.insert(0, str(SCRIPTS))` for the authoring
scripts; a second insert for a second script directory puts two of them on one path, and
any module name they share then resolves by insert order. Nothing needs the import, so
nothing should take that risk.

- [ ] **Step 4: Implement `audit.py`**

The scan is the part with a sharp edge. It must require an imperative construction, not a
keyword: the verb at the start of a line, of a bullet, or of a sentence, or following
`must`, `should` or `then`. `direct-copy` fails that test because the verb is hyphenated
into a noun phrase mid-sentence. Proposal:

```python
TOIL_VERBS = {
    "copy": r"copy|copies",
    "download": r"download",
    "install": r"install",
    "unzip": r"unzip|extract",
    "paste": r"paste",
    "move": r"move",
    "rename": r"rename",
    "clone": r"clone",
    "create-directory": r"(?:create|make) (?:the |a )?(?:directory|folder)",
}
_LEAD = r"(?:^|^[-*]\s+|(?<=[.!?]\s)|(?<=,\s)|(?<=\bmust\s)|(?<=\bshould\s)|(?<=\bthen\s))"
```

matched case-insensitively, per line, with the verb required to be a whole word.

**The comma alternative is load-bearing and was added after testing the pattern against the
corpus.** Without it the scanner misses the real toil at
`lessons/13-load-gltf-model/LESSON.md:40`, which reads "Before starting, copy every file
under `model/` ..." — an introductory clause, so the verb is neither at the start of the
line nor after a full stop. A pattern that catches lesson 00 and misses lesson 13 would
have looked like it worked.

Favour recall over precision here, deliberately: the output is a candidate list a reader
adjudicates, so a false positive costs one glance and a false negative hides the thing the
skill exists to find. The negative control must still pass — `direct-copy` stays unmatched
because the verb is hyphenated into a noun phrase, not because of where it sits.

**This scanner is a candidate generator and nothing more.** Print that sentence in the
report header, and say in the same breath that an empty candidate list is not evidence that
a course has no toil.

Topic-to-lesson matching is the same kind of problem and gets the same treatment: emit a
`topic_candidates` map built from token overlap, labelled as candidates. The script must
not claim a topic is covered.

- [ ] **Step 5: Run and watch them pass**

```bash
cd ~/src/github.com/skomp/tutorail-authoring && python3 tests/test_audit.py
```

- [ ] **Step 6: Run it against the two real bundles and read the output yourself**

```bash
python3 skills/course-quality/scripts/audit.py ../tutorail-bundles/webgl-typescript-scene
python3 skills/course-quality/scripts/audit.py ../tutorail-bundles/durable-event-broker
```

The first must produce a candidate at `lessons/00-project-setup/LESSON.md:34` and one at
`lessons/13-load-gltf-model/LESSON.md:40`, and must **not** produce one at
`lessons/15-render-to-texture.md:41`. The second exercises `optional_lessons` against a
real bundle. Report every candidate either produced, including ones you think are wrong —
a scanner's false positives are a finding about the scanner.

- [ ] **Step 7: Commit**

```bash
git add skills/course-quality/scripts/audit.py tests/test_audit.py \
        tests/fixtures/toil-course tests/fixtures/toil-course-no-coverage \
        tests/harness.py tests/run_all.py
git commit -m "Add audit.py: the evidence a course-quality review starts from"
```

---

### Task B5: the `course-quality` skill

**Files:**
- Create: `skills/course-quality/SKILL.md`
- Create: `skills/course-quality/references/rubric.md`
- Modify: `.claude-plugin/plugin.json` (version), `README.md`

**Interfaces:**
- Consumes: `audit.py` from B4, `supplies.py` from B2, `index.py`
- Produces: the skill the author invokes as "evaluate the quality of the webgl bundle"

- [ ] **Step 1: `references/rubric.md`**

The five-row table from the spec, each row with its test, plus three paragraphs the numbers
need to survive contact with a reader:

- what a score is for — making a judgement legible and comparable across a long course, not
  replacing it;
- that the rubric is printed with every report so a reader can argue with the scoring
  rather than with a bare number;
- **the invariant no structural check can reach**: a course carrying optional lessons must
  be completable by a learner who declines every offer. `bundle-format.md` section 13
  states it as an authoring obligation for exactly that reason, and it belongs in this
  rubric as a course-level question the auditor asks by reading.

- [ ] **Step 2: `SKILL.md`**

Frontmatter `name: course-quality`, and a description carrying the phrases an author
actually types: evaluate the quality of a bundle, score a course, does this tutorial teach,
audit a course, find the toil in a course, review a tutorial against its learning goals.

The body: orient, run `audit.py`, **read the lessons** — the script's candidates are
candidates and its topic matches are candidates — score against the rubric, then report in
the five sections the spec names (course and total; the per-lesson table; goal gaps; the
toil inventory with `file:line` and the exact sentence; proposals).

Write it host-neutrally: no tool name from any host, and watch the sentence-initial
capitals in particular. "Open each lesson" and "Work through the lessons" are fine; the
capitalised tool names listed in the global constraints are not.

Three rules the skill must state about itself:

- **it proposes and never edits.** Applying a proposal goes back through
  `tutorail-authoring` and its toolkit, after the author says yes;
- **an empty candidate list is not a pass.** The script cannot see toil it has no pattern
  for. The score comes from reading;
- **a green validator is not a good course.** Structural validity and teaching quality are
  different questions, which is why this skill exists separately from the validator.

Every proposal names a concrete action: a toil span becomes a `supplies.py add` command
plus the prose to delete; an unserved topic becomes a lesson proposal or an argument for
dropping the topic; a lesson scoring at or below zero becomes a question for the author
about what it is for.

- [ ] **Step 3: Register and bump**

Add the skill to `.claude-plugin/plugin.json` if that manifest enumerates skills — **look,
do not assume**; `marketplace.json` may be where the enumeration lives. This repository has
**two** manifests and both are at `0.1.0`: bump both to `0.2.0` and keep them equal. Add the
skill to `README.md` beside the authoring one.

```bash
grep -rn '"version"' .claude-plugin/*.json
```

- [ ] **Step 4: Verify the skill loads**

```bash
cd ~/src/github.com/skomp/tutorail-authoring && python3 tests/run_all.py
```

plus: read `skills/course-quality/SKILL.md` back in full and check the commands it names
exist, with the flags it gives them. A skill that names a flag the script does not have is
the same defect class as a stale schema in a plan.

- [ ] **Step 5: Commit**

```bash
git add skills/course-quality .claude-plugin/plugin.json README.md
git commit -m "Add the course-quality skill"
```

---

### Task B6: run it on the real courses and report

**Files:** none changed in `tutorail-bundles`. **The webgl bundle is not edited by this
plan.**

- [ ] **Step 1: Audit `webgl-typescript-scene` and score it against the rubric**

Follow the skill exactly as written, including reading the lessons rather than trusting the
scan. Produce the full five-section report.

- [ ] **Step 2: Audit `durable-event-broker` the same way**

It is the first real bundle with optional lessons, so it is where the "completable by a
learner who declines every offer" question gets asked for the first time.

- [ ] **Step 3: Report to the author**

Both reports, the proposals, and — separately — anything the exercise revealed about the
tooling itself. A false positive from the scanner, a rubric row that did not fit, or a
lesson the rubric scored in a way you disagree with are findings about this work, not about
the courses, and they are the most valuable thing this task produces.

- [ ] **Step 4: Update `TODO.md` and commit the tracking**

Record what the reports found and what was deliberately not acted on, so a later session
does not have to re-derive it. Note the `catalog.py` `scope` gap a peer session filed in
tutorAIl's `TODO.md` against this repository: the catalogue's `scope` line counts only the
main path, so a course with optional lessons gives no signal that they exist. It is not
part of this plan and it should not be lost.

---

## Self-review

**Spec coverage.** Section 4 → A1, A3. Section 4.3 → A4. Section 4.4 → A3, A4. Section 4.5
→ A4. Section 5.1 → A1. Section 5.2 → A2. Section 5.3 → A1 step 5, B5 step 2. Section 6 →
A3, A4. Section 7 → B3. Section 8 → B1, B2. Section 9 → B4, B5. Section 10 → the test steps
of A1, A2, B1, B2, B4. Section 11 → task order. Section 12 → B6, which changes no bundle.

**Type consistency.** `collect_supplies` and `supplies_covers` are defined in A1 and used
in A2 under those names. `emit_scalar`, `render_supplies_item` and `add_supplies` are
defined in B1 and used in B2 under those names. `audit.py`'s `--json` keys are named in
B4's Interfaces block and used in B4's tests.

**Known weakness, stated rather than hidden.** The scanner's pattern list is a guess. It has
one real positive and one real negative control from the corpus, which is enough to prove it
runs, and not enough to prove it is complete. That is why the skill scores by reading and
the scanner only proposes.
