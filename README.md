# tutorail-authoring

Interview-driven authoring and maintenance for [tutorAIl](https://github.com/skomp/tutorAIl)
tutorial bundles.

You describe the course you want to teach. The skill asks until it knows enough, writes a
course spec for you to approve, and only then generates bundle files — because revising one
document beats revising twenty lesson files.

```
"I want to build a course on WebGL."
        │
        ▼
  interview — subject, arc, teaching stance, design decisions, coverage
        │
        ▼
  specs/webgl-typescript-scene.md      ← you review and approve
        │
        ▼
  tutorial.yaml, COURSE.md, DESIGN.md, STATE.template.md, lessons/
        │
        ▼
  validated before you are told it is done
```

## Requires the runner

This plugin **depends on the tutorAIl runner being installed**, because the toolkit invokes
its validator rather than shipping a second, weaker copy. Install that first, by the route
that matches your host:

```
/plugin marketplace add skomp/tutorAIl
/plugin install tutorail@tutorail
```

On Codex, install the runner the way its own README describes — a symlink into
`~/.agents/skills/tutorail`. The toolkit searches `~/.agents/skills/tutorail/scripts/` before
it searches the Claude Code plugin directories, so that install is what makes the validator
findable there. `$TUTORAIL_VALIDATOR` overrides the search on either host.

## Install

**Claude Code**

```
/plugin marketplace add skomp/tutorail-authoring
/plugin install tutorail-authoring@tutorail-authoring
```

Update it with both commands:

```
claude plugin marketplace update tutorail-authoring
claude plugin update tutorail-authoring@tutorail-authoring
```

The second alone compares manifest **versions**, not commits, and will report that you are
already current while new work sits unreachable behind the old version number. So a change
pushed here is invisible to an install that already holds the version until
`.claude-plugin/plugin.json` is bumped and pushed too. That is not hypothetical: on
2026-09-15 work committed in this repository was unreachable from Claude Code until the
plugin was bumped to 0.4.0 and pushed, while Codex had been running it all along.

**Codex — to use the plugin**

Codex follows symlinks in `~/.agents/skills/`, its documented user skills scope. Clone
somewhere you do not work in:

```
git clone git@github.com:skomp/tutorail-authoring.git ~/.local/share/tutorail-authoring
mkdir -p ~/.agents/skills
ln -s ~/.local/share/tutorail-authoring/skills/tutorail-authoring ~/.agents/skills/tutorail-authoring
ln -s ~/.local/share/tutorail-authoring/skills/course-quality ~/.agents/skills/course-quality
```

Update it with `git -C ~/.local/share/tutorail-authoring pull`.

Both symlinks. This plugin ships two skills, and this install path never reads a manifest,
so a missing symlink is a missing skill with nothing to warn you.

Not `codex plugin add` — see the runner's README, under *Installing on Codex*, for why that
path does not work yet. It fails silently on both plugins, for the same reasons.

**Codex — to develop the plugin**

Point the same two symlinks at the checkout you work in:

```
ln -s <your checkout>/skills/tutorail-authoring ~/.agents/skills/tutorail-authoring
ln -s <your checkout>/skills/course-quality ~/.agents/skills/course-quality
```

**The two hosts do not run the same copy, and that is what the choice above is between.**
Claude Code installs a published version from the marketplace: it changes only when you
update it, and it never contains uncommitted work. Codex follows the symlink into a
checkout, so it runs whatever is checked out there — including a half-finished edit
mid-save. That is the right arrangement while developing this plugin and the wrong one for
someone who only wants to use it.

## Use

Create a course:

```
I want to build a tutorial on WebGL.
Write me a course about Rust ownership.
```

Change one:

```
Add a lesson on lifetimes after lesson 03.
Restructure chapter 14 of the AutomatonDB course.
Split lesson 07 in two.
```

Modify starts from a generated index rather than by reading the whole course, so it costs
about forty lines of context for a twenty-three-lesson bundle, and it can answer the
question that matters: *what else does this change break?*

## Audit one

```
Evaluate the quality of the webgl bundle.
Does this tutorial actually teach?
Find the toil in this course.
```

The second skill in this plugin, `course-quality`, scores a bundle lesson by lesson against
a teaching rubric — what teaches, what is practice, what is only evidence, and what is toil
the bundle should hand over instead of assigning — and reports the objectives and
`DESIGN.md` anchors no lesson exercises. Its own script, `skills/course-quality/scripts/audit.py`,
gathers the evidence and computes no score, because the parts a script can decide are not
the parts that matter. The audit **proposes and never changes a bundle**; applying a
proposal comes back through the authoring skill and the toolkit below.

A green validator is not a good course. Structural validity and teaching quality are
different questions, which is why they are two skills.

## The toolkit

The authoring skill drives these rather than hand-editing YAML, because hand-editing is how `id` and
slug drift apart and how a `lessons` list stops matching the files beside it.

| Command | Does |
|---|---|
| `index.py <bundle>` | compact index: id, title, form, design refs, validators, purpose |
| `lesson.py add` | new lesson in either form, correct frontmatter, inserted in the `lessons` list |
| `lesson.py add --optional` | a lesson the tutor **offers** instead of sequencing: written under `optional_lessons`, never into the `lessons` list, with no number prefix and no renumber |
| `lesson.py renumber` | renumber files, ids, the list, and prose cross-references |
| `supplies.py` | declare the files a bundle hands the learner, instead of a lesson step that assigns a copy |
| `promote.py` | move a generated lesson from a learner instance into a bundle |
| `promote.py --optional` | move a generated lesson into `optional_lessons` instead; `offer_at` and `offer_because` are derived from the lesson's provenance, printed, and written only once `--confirm` is passed |
| `catalog.py` | generate a repository-level `catalog.yaml` from bundle manifests |

Every operation that changes a bundle:

- runs the validator afterwards and **fails loudly if it left the bundle invalid**
- supports `--check`, showing what it would do without doing it
- refuses on a dirty working tree unless forced, so `git diff` is a clean record
- leaves the bundle **unchanged** on failure, never half-edited

## Tests

```
python3 tests/run_all.py            every suite
python3 tests/run_all.py renumber   only suites whose name matches
```

Stdlib only — no pytest, no install. Each suite is also a plain runner on its own.

**Pin the validator when a result has to be attributable.** The suites run the runner's
`validate_bundle.py`, and on a developer machine the search leads to a checkout somebody may
be editing. Copy the whole scripts directory — `validate_bundle.py` imports `yamlite` and
`catalogs` from beside itself, so a single-file pin produces a validator that cannot run, and
it fails in a way that reads as product defects:

```
mkdir -p /tmp/pin && cp <tutorAIl>/skills/tutorail/scripts/*.py /tmp/pin/
TUTORAIL_VALIDATOR=/tmp/pin/validate_bundle.py python3 tests/run_all.py
```

Every suite prints the validator it used, so the pin is visible rather than assumed.

### CI

`.github/workflows/tests.yml` runs the whole suite on `ubuntu-latest` and `macos-latest` for
every push and pull request. The Linux job is the one that earns it: `ubuntu-latest` has a
case-sensitive filesystem, and an assertion that encodes the developer's filesystem reads as
correct on every macOS machine (tutorail-authoring#17).

The workflow checks out `skomp/tutorAIl` **at a commit sha**, not at `main`, so that a red
suite always means a defect in this repository and never an upstream change. The cost is that
somebody must bump the pin by hand. **The sha lives in one place — the `ref:` in that
workflow — and the file's own header comment holds the bump procedure and the reasoning.**

## Design

`docs/superpowers/specs/2026-09-12-bundle-authoring-design.md` records the architecture, why
the validator stays in the runner, and a hazard nothing currently catches: lessons reference
each other by id in prose, so renumbering can leave those references dangling.

## Licence

MIT.
