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
its validator rather than shipping a second, weaker copy. Install that first:

```
/plugin marketplace add skomp/tutorAIl
/plugin install tutorail@tutorail
```

## Install

**Claude Code**

```
/plugin marketplace add skomp/tutorail-authoring
/plugin install tutorail-authoring@tutorail-authoring
```

**Codex**

```
git clone git@github.com:skomp/tutorail-authoring.git ~/src/tutorail-authoring
mkdir -p ~/.agents/skills
ln -s ~/src/tutorail-authoring/skills/tutorail-authoring ~/.agents/skills/tutorail-authoring
```

Not `codex plugin add` — see the runner's README for why that path does not work yet.

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

## The toolkit

The skill drives these rather than hand-editing YAML, because hand-editing is how `id` and
slug drift apart and how a `lessons` list stops matching the files beside it.

| Command | Does |
|---|---|
| `index.py <bundle>` | compact index: id, title, form, design refs, validators, purpose |
| `lesson.py add` | new lesson in either form, correct frontmatter, inserted in the list |
| `lesson.py renumber` | renumber files, ids, the list, and prose cross-references |
| `promote.py` | move a generated lesson from a learner instance into a bundle |
| `catalog.py` | generate a repository-level `catalog.yaml` from bundle manifests |

Every operation that changes a bundle:

- runs the validator afterwards and **fails loudly if it left the bundle invalid**
- supports `--check`, showing what it would do without doing it
- refuses on a dirty working tree unless forced, so `git diff` is a clean record
- leaves the bundle **unchanged** on failure, never half-edited

## Design

`docs/superpowers/specs/2026-09-12-bundle-authoring-design.md` records the architecture, why
the validator stays in the runner, and a hazard nothing currently catches: lessons reference
each other by id in prose, so renumbering can leave those references dangling.

## Licence

MIT.
