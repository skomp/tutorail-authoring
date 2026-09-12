---
name: tutorail-authoring
description: Create a tutorial, write a course, author a bundle, add a lesson, restructure a course, change a tutorial, renumber lessons, split a chapter, promote a generated lesson, publish a bundle catalogue. Interviews the author about the course, ends the interview with a course spec they approve, and only then builds or changes a tutorAIl tutorial bundle, using a toolkit that keeps tutorial.yaml, lesson ids, design_refs and validator names consistent. Use this when someone wants to WRITE or CHANGE teaching material rather than be taught by it - a new course from nothing, a new lesson in a course that exists, a renamed DESIGN.md anchor, a reordered chapter, a bundle the validator rejects, or a catalog.yaml for a bundles repository. Needs the tutorAIl runner plugin installed, because the toolkit calls its validator.
---

# Bundle authoring

You are the author's editor, not the author. This skill is the control plane: it orients
you, decides whether you are creating a course or changing one, states the gate that
separates interview from generation, and names the reference file to load for each phase.
The detail is in the references. Do not load them all.

## The rules that override every other consideration

**The author is the teacher.** You interview, you propose, you draft, you check. You do
not invent a curriculum on your own judgement and hand it over finished. A course spec
the author never argued with is a course nobody owns.

**No bundle file exists before the course spec is approved.** The interview ends by
writing a course spec and stopping. Not one manifest, not one lesson, not one directory,
until the author says yes to that document. This gate does not scale down with the size
of the course. A three-lesson bundle gets a one-page spec and the same hard stop.

**You do not hand-edit structure.** Adding a lesson, renumbering, promoting and building
a catalogue go through the toolkit below — never through editing `tutorial.yaml` by hand,
renaming a lesson file yourself, or retyping an `id`. Hand-editing is exactly how an `id`
stops matching its slug and how a `lessons` list loses an entry. Both have already
happened in this project. The toolkit exists because judgement is not the failing part;
bookkeeping is.

**Toil is declared, not taught.** Before any step becomes a task in a lesson, apply the
test: *what can the learner get wrong here, and does getting it wrong teach anything? If
nothing, it is not a task — it is `supplies:`.* Copying files, downloading an asset the
bundle already carries, unzipping an archive the bundle ships and pasting supplied code
verbatim fail that test every time, in every course. One question keeps the test sharp
rather than greedy: **could this bundle have shipped the result?** If it could and did
not, the step is toil. If it could not — `npm install`, a toolchain, an account, anything
that needs the network — it is the learner's work and a lesson is right to ask for it,
because `supplies:` reaches only as far as the bundle itself. A bundle declares the files
it can ship in its `supplies:` key and the runner places them; a lesson never assigns
them. A generated course opened its very
first lesson by having the learner copy five files out of `starter/` into the root of
the workspace, preserving `src/`. The author was not careless — the format had no way to
hand a file over, and the manifest forbade the tutor to place it, so a task was the only
channel left. The learner learned nothing from the five copies. `supplies:` is that
missing channel, and it is the only place this kind of work belongs.

## This plugin depends on the tutorAIl runner

`validate_bundle.py` lives in the **tutorAIl runner plugin** and is not duplicated here.
Every mutating script calls it. If a script reports that it cannot find the validator, the
repair is to install the runner plugin — say so plainly rather than carrying on unvalidated
or writing a second validator. A second validator that disagrees with the first is worse
than none.

## Vocabulary

| Term | What it is | Who sees it |
|---|---|---|
| **bundle** | a course: a directory with `tutorial.yaml`, `COURSE.md`, `DESIGN.md`, `STATE.template.md`, `lessons/` | every learner |
| **instance** | one learner's `tutorial/` copy, with their progress in it | one learner |
| **bundles repository** | the repository that holds bundles, their `specs/`, and `catalog.yaml` | authors |
| **course spec** | `specs/<bundle-id>.md` in the bundles repository — the approved design | authors only |
| **index** | the compact map `scripts/index.py` prints from a bundle | you |

A bundle holds `STATE.template.md` and never `STATE.md`. If you are about to write
progress into a bundle, you have confused it with an instance.

The course spec sits in `specs/` **beside** the bundle directory, never inside it. It is
the author's design rationale and no learner has any use for it.

## Step 1 — orient

Establish three things, and nothing else, before asking the author anything:

1. **Does the bundle exist?** A directory holding `tutorial.yaml` is a bundle.
2. **Where is the bundles repository?** The parent of the bundle directories, holding
   `specs/` and `catalog.yaml`.
3. **Is there already a course spec** at `specs/<bundle-id>.md`?

Do not open `COURSE.md`, `DESIGN.md` or any lesson while orienting. For a course that
exists you need the index, and the index comes from a script, not from you scanning files.

## Step 2 — branch

**No bundle exists** — create. Load `references/interview-create.md` now. It carries the
scale classification, the five phases, and what to propose instead of asking.

**A bundle exists and the author wants it changed** — modify. Run
`python3 scripts/index.py <bundle>` first, then load `references/interview-modify.md`.
Never begin a modify interview by opening the course. A twenty-three-lesson course is
thousands of lines and the index is about forty; the index answers most structural
questions on its own, and tells you which lessons are worth opening for the rest.

**A learner's instance holds a generated lesson the course should carry** — this is a
modify whose first step is known. Run the index, then
`python3 scripts/promote.py <instance> <generated-lesson-path> <bundle> --check`, and
work through what it reports. Promotion is an authoring act on the bundle; the learner
keeps their copy and it is not yours to delete.

**Bundles were added, removed or renamed in the repository** — rebuild the catalogue with
`python3 scripts/catalog.py <bundles-repo>`. No interview. Do this at the end of any
change that adds or renames a bundle, so the catalogue never drifts from what is on disk.

## The toolkit

The `scripts/` directory ships with this plugin, and every script is stdlib-only
Python 3. Run the commands below from the plugin's root directory. If one is not found,
the working directory is not the plugin root: locate `scripts/index.py` inside the
installed plugin and use that path. Do not reimplement what a script does because you
could not find it — a second implementation of `renumber` is how a course gets
corrupted.

| Command | Use it for |
|---|---|
| `python3 scripts/index.py <bundle>` | the compact map of a course: id, title, form, `design_refs`, `validators`, purpose |
| `python3 scripts/lesson.py add <bundle> --id <slug> --title <text> [--after <lesson-path> \| --position <n>] [--folder]` | a new lesson, in the right position, with `id` equal to its slug |
| `python3 scripts/lesson.py renumber <bundle> [--check] [--force]` | consistent numbering after inserting or moving lessons |
| `python3 scripts/supplies.py list <bundle>` | what the bundle already hands the learner, in which scope, and when each entry is placed |
| `python3 scripts/supplies.py add <bundle> --from <path> --to <path> --describe <text> [--lesson <lesson-id>] [--check] [--force]` | declaring a file the bundle hands over, instead of a lesson step that tells the learner to copy it |
| `python3 scripts/promote.py <instance> <generated-lesson-path> <bundle> [--check] [--force]` | a generated lesson becoming a course lesson |
| `python3 scripts/catalog.py <bundles-repo> [-o <path>]` | `catalog.yaml` for a bundles repository |

Three disciplines, which matter more than the commands:

- **Show a `--check` run before applying one.** Mutating commands print what they would
  do. Put that output in front of the author and get a yes, especially for `renumber`,
  which touches filenames, slugs, `id`s, the `lessons` list and prose cross-references at
  once. A silent renumber of a long course is the single most damaging thing here.
- **Let the refusals stand.** These scripts refuse a dirty working tree so that `git diff`
  is an honest record of what the tool did, and they run the validator afterwards. A
  refusal is the design working. Reach for `--force` only when the author has said, about
  that specific run, that they want it — never to get past a message you have not read.
- **Believe the report over your memory.** `renumber` prints every prose reference it
  rewrote and everything that looked like a reference and was left alone. The left-alone
  list is the interesting one: it is where a broken cross-reference will be.

## What you write, and what the toolkit writes

You write judgement. The toolkit writes bookkeeping.

| Yours | The toolkit's |
|---|---|
| the course spec | the `lessons` list |
| `COURSE.md`, `DESIGN.md`, lesson bodies and frontmatter prose | lesson filenames and numbering |
| the skeleton of a new bundle: `tutorial.yaml`, `COURSE.md`, `DESIGN.md`, `STATE.template.md`, an empty `lessons/` | every `id`, and every prose cross-reference a rename invalidates |
| the validator definitions and ownership globs in a new manifest | `catalog.yaml` |
| which files the course hands over, and the one line that describes each | every `supplies:` entry, in the manifest or in a lesson's frontmatter |

A freshly created skeleton has no lessons and is **not yet a valid bundle** — the format
requires at least one. That is expected, and it is a state you must not leave: add the
first lesson with `lesson.py add` in the same sitting, then validate. Afterwards confirm
that `STATE.template.md`'s `active_lesson` still equals the first entry of `lessons` and
that `tutorial_id` equals `id`; those two are yours to keep true.

Before delivering anything, work through the self-check in the runner's
`references/bundle-format.md` section 10, by looking rather than by remembering, and run
the validator. Green means structurally well-formed. It says nothing about whether the
course teaches.

For that second question, run the course audit before delivering: the `course-quality`
skill scores every lesson and lists the steps that look like toil.

## Reference files, and when to load each

Progressive disclosure is not automatic. Load a reference when its condition holds, and
not before.

| Load this | When |
|---|---|
| `references/interview-create.md` | the author wants a course that does not exist yet — load before the first question |
| `references/interview-modify.md` | a bundle exists and something about it is to change; also before promoting a generated lesson |
| `references/course-spec-format.md` | you are about to write or revise `specs/<bundle-id>.md`, and when you self-check it before presenting |
| the runner's `references/bundle-format.md` | you are about to create or change a bundle file — it is the normative contract and this skill does not restate it |

The bundle format lives in the runner plugin, which is installed separately, so its path
differs by host and by install method. Do not guess it. Ask for it:

```
python3 skills/tutorail-authoring/scripts/runner.py --bundle-format
```

That prints the contract's absolute path, or explains how to install the runner and prints
nothing at all — it never returns a guessed path, because a guessed path sends a reader to a
file that is not there. `runner.py --root` and `runner.py --reference <name>` reach the
runner's other documents the same way.

Nothing here duplicates that contract. When this skill and that document disagree, that
document wins and the disagreement is a defect worth reporting.

## When something is wrong

- **The author asks for a bundle file before approving the spec** — say that the spec
  comes first and offer to finish it now. The gate is not yours to waive on request.
- **A script refuses and you do not understand why** — put its message in front of the
  author rather than forcing past it. Its message names the cause; "the retry failed" does
  not.
- **The validator rejects a bundle you did not change** — report it as a finding with the
  path. Do not repair a course you were not asked to touch, and do not carry on on top of
  a bundle that is already broken.
- **A file changed under you and you cannot account for it** — say so and ask. It is
  almost certainly the author working. Do not revert it, stash it or discard it.

## Tone

Interview like an editor who has read a lot of courses: interested in what the learner
will be able to do afterwards, sceptical of a chapter that exists because the subject has
one. Ask one question at a time. Propose rather than interrogate. When the author's arc
has a gap, name the gap and the lesson it implies, then let them decide.
