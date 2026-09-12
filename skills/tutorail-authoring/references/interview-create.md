# The create interview

**Status:** normative. Load this before the first question when the author wants a course
that does not exist yet.

The interview has one output: an approved course spec at `specs/<bundle-id>.md` in the
bundles repository. No bundle file is created before the author approves it.

It has one failure mode worth naming up front: **asking too much.** Forty questions where
six would do is how an interview becomes the thing an author routes around, and an author
who routes around it hand-writes a manifest, which is the defect this whole project
exists to prevent. Everything below is shaped by that.

---

## 1. Classify the scale first, and say so out loud

The first thing you establish is how big the course is, because a three-lesson
introduction and a twenty-three-lesson project course need different interviews. Announce
the classification so the author can overrule it:

> "That sounds like a short course — four or five lessons in one sitting. I will keep the
> interview to the essentials and skip milestone structure. Say so if you are thinking
> bigger."

| Scale | Roughly | What the interview does |
|---|---|---|
| **Short** | 1 to 5 lessons, one sitting | Phases 1, 2 and 3. Phase 4 reduced to "is there any decision later lessons must not contradict". Phase 5 skipped. No milestones, no coverage list, `DESIGN.md` may be one anchor. |
| **Standard** | roughly 6 to 12 lessons, several sittings | All five phases. Chapters, no milestone ceremony. A coverage list is recommended and cheap. |
| **Long** | more than about 12 lessons, a project course | All five phases in full. Milestones, a coverage list, and an explicit decision about which chapters get lesson files now. |

**The ratchet is one-way.** Complexity discovered mid-interview upgrades the scale: stop,
say so, and ask the questions the larger scale needs. Nothing downgrades. When you are
between two, take the heavier one.

### What a short course is spared

Never ask a short course about milestone structure, a coverage list, `aliases` beyond the
obvious, optional paths, or which chapters get files. A four-lesson course answers those
by existing. Asking anyway is how the interview earns its reputation.

### The long-course question a short course never gets

For a long course, ask once, near the end: **which chapters need lesson files now, and
which stay a map in `COURSE.md` for now?** The format permits a chapter with no lesson
file, and it has a real cost at teaching time — every learner's tutor drafts that chapter
separately, differently. An author who knows the cost usually writes two more lessons and
maps the rest. Put the answer in the spec.

---

## 2. The five phases

Ask **one question per message**. Prefer a question with options over an open one.
Each phase ends in something concrete, and every concrete thing feeds named bundle fields.

| Phase | Ends with | Feeds |
|---|---|---|
| 1. Subject and learner | one sentence on what the learner builds, one on what they already know | `title`, `description`, `subjects`, `level`, prerequisites |
| 2. The arc | the end state, the first task, and the ordered steps between | the `COURSE.md` chapter map, the `lessons` order |
| 3. Teaching stance | who writes the code, whether software gets built, how work is checked, what the course hands over | `workspace_kind`, `ownership_policy`, `validators`, `solution_code`, `supplies` |
| 4. Durable decisions | the decisions later lessons depend on, and the ones left open | `DESIGN.md` and its anchors |
| 5. Coverage | topics the course owes a learner even if the project never forces them | the `COURSE.md` coverage list |

### Phase 1 — subject and learner

Two things, and they are usually two questions.

- **What does the learner build, and what can they do at the end that they cannot do
  now?** Push for the second half. "Learn Rust" is a subject; "has a working
  command-line tool and can explain where its errors come from" is an end state, and it
  is what phase 2 works backwards from.
- **What do you assume they already know?** This sets `level` and the prerequisites, and
  it is the answer that most often changes the arc. A course for someone who has never
  used the language needs a different lesson 00 from one for someone changing languages.

Propose `title`, `id`, `subjects` and `level` from these answers. Do not ask for them.

### Phase 2 — the arc

This is the phase worth spending questions on. A wrong arc is discovered after twenty
lesson files exist, which is the expensive way to find out.

- **Start from the end state** phase 1 produced and ask what the learner must be able to
  do immediately before it. Then again. Working backwards surfaces prerequisites that
  working forwards hides.
- **Ask for the first task separately.** The first lesson is the one that decides whether
  a learner continues, and authors under-specify it more than any other.
- **For a long course, ask where the milestones are** — the points where the learner has
  something that works. Chapters between milestones are the `COURSE.md` map.

You end with an ordered list of lessons, each with a one-line purpose and a one-line
completion condition. That list is the spine of the spec, and the thing the self-check in
section 4 is run against.

**A step that is only setup is not a lesson.** Test every entry the author proposes: what
can the learner get wrong here, and does getting it wrong teach anything? A "project
setup" lesson whose whole content is a scaffold arriving on disk fails that test — nothing
in it can be got wrong in an instructive way. Say so, in as many words, and fold it into
`supplies:` rather than accepting it into the arc:

> "Lesson 00 as you have it is a handover, not a lesson — the learner cannot get any of
> it wrong in a way that teaches them something. I will declare those files as supplies,
> so they are in place before lesson 01, and the course starts where the teaching starts.
> Is anything in that setup worth a learner's attention on its own?"

Sometimes the answer is yes and a real lesson survives — a learner who must understand the
build configuration because lesson 09 changes it is being taught, not set up. Then the
lesson keeps the part that can be got wrong, and the files still arrive through
`supplies:`. First lessons attract this defect more than any other position, so the arc's
first entry is worth the extra minute.

### Phase 3 — teaching stance

Four questions at most, and two of them usually answer themselves.

- **Does the course build software?** `existing-or-new-repository`, `new-repository`, or
  `none`. If nothing is built, `workspace_kind: none` and `learner_owned` is empty.
- **How is the learner's work checked?** The answer names a toolchain, and the toolchain
  names the validators. Turn it into a proposed `validators` map and show it:
  `cargo-check`, `cargo-test`, `pytest`, `has-lib` as a `file-exists`. Confirm, do not
  interrogate. A course where a human judges the work gets one `manual` validator and
  that is correct, not a gap.
- **May the tutor ever write the learner's code?** The default,
  `tutor-must-not-edit-learner-owned` with `solution_code: on-request-only`, is right for
  nearly every course. Propose it as a default and only explore if the author hesitates.
- **What must the learner's workspace already contain before lesson 1, and what does each
  later lesson hand over?** A scaffolded project, a config file the course never teaches, a
  sample asset, a fixture dataset. Ask it plainly, because an author who is not asked
  writes the handover into lesson 1 as a task. Every answer belongs in the spec's *Supplied
  files* section, and none of them is a lesson.

**What `supplies:` is, exactly**, because the narrowness is the whole point. An entry names
a path inside the bundle, a path in the learner's workspace, and one line describing what
the file is for. An entry in `tutorial.yaml` is placed once, right after materialization;
an entry in a lesson's frontmatter is placed when that lesson opens, which is what you want
for an asset a learner should not meet early. The runner places the files, never overwrites
one that is already there, names anything it left alone, and reports the lot as setup
rather than as work the learner did. Under `tutor-must-not-edit-learner-owned` the tutor may
**create** a declared target that does not exist, and may **never modify** one that does; a
path nobody declared gets no exemption at all. That is what lets the default ownership
policy stay on. A course that answers one bootstrap by setting `ownership_policy:
unrestricted` has traded the guarantee that the tutor will not write the learner's code for
a handful of file copies, and that is the trade `supplies:` exists to avoid.

### Phase 4 — durable decisions

The question that actually gets an answer is not "what are your design decisions". It is:

> **"What does a lesson in the middle of this course have to already be true about the
> design, that a learner could otherwise get wrong in lesson 2 and pay for in lesson 9?"**

Each answer becomes a `DESIGN.md` section with a stable anchor. Name the anchors now,
in the spec, because phase 2's lesson list has to cite them and the self-check checks
that the citations resolve.

Ask also what is **deliberately unresolved**. The format wants those recorded and marked
as such; they are often where a later lesson does its teaching.

A short course may have exactly one anchor, or none if the course builds nothing. That is
a legitimate answer. Do not manufacture design decisions to fill a section.

### Phase 5 — coverage

Skip for a short course. For the others, one question:

> "Which topics does this course owe a learner, even if the project never naturally forces
> them?"

Record them as topics named the way a learner would ask — `lifetimes`, `error design`,
`interior mutability` — never as lesson titles, which duplicates the chapter map and then
drifts from it. This list is read mechanically by a tutor deciding whether a stuck learner
has hit a hole in the course or the intended difficulty of an exercise, so it is worth the
one question it costs. It is also where the course says what it will **not** teach.

---

## 3. Never ask what you can propose

Everything in this table is derived from the phase answers, shown once as a proposal, and
confirmed in passing. None of it is a question.

| Field | Where it comes from |
|---|---|
| `bundle_format` | always `1`. Never mentioned. |
| `id` | the title, slugified. Confirm once, because it is permanent. |
| `aliases` | the words the author used for the subject while answering phase 1 |
| `style` | phase 3: `project-driven`, `exercise-based`, `interactive`, `long-form` |
| `subjects`, `level` | phase 1 |
| `validators` | phase 3's toolchain |
| `workspace_kind`, `tutor_owned`, `learner_owned` | phase 3, plus the language's conventional layout |
| `ownership_policy`, `one_task_at_a_time`, `solution_code`, `advance_on` | the defaults, confirmed as one group |
| lesson numbering and file naming | the toolkit's, never discussed |

Show the whole group once, in the spec, as a block the author can object to. One
objection is cheaper than nine questions.

---

## 4. Self-check the spec before presenting it

Run this on the draft, silently, and fix what it finds. It is cheap, it is checkable
rather than a feeling, and the middle two items catch the same defects a full walk of the
course would find hours later.

- [ ] **Every required field has an answer or a defensible default.** Walk the field table
      in the runner's `references/bundle-format.md` section 2, not your memory of it.
- [ ] **Every lesson's completion conditions depend only on what earlier lessons built.**
      Take each lesson in `lessons` order, and check its conditions against the union of
      what lessons before it produced. A condition that needs something from later is an
      ordering defect, and it is the most common one.
- [ ] **Every `DESIGN.md` anchor a lesson cites exists** in the phase 4 decisions. A
      citation with no section is a dangling `design_ref` waiting to happen.
- [ ] **No lesson introduces a type or concept that nothing later uses.** Either something
      later needs it, or the lesson is teaching for its own sake and should go.
- [ ] **Every validator a lesson names is in the proposed `validators` map.**
- [ ] **Every lesson contains something the learner can get wrong instructively**, and the
      spec says what it is. A lesson that fails this is toil: it moves to *Supplied files*
      and leaves the arc. No lesson asks the learner to copy, download, unzip, install or
      paste anything.
- [ ] **Every file the course hands the learner is in *Supplied files***, with its
      destination and the line that describes it. A course that supplies nothing says so
      explicitly; an absent section and a deliberate "none" are different claims.
- [ ] **No placeholder survives.** No "TBD", no lesson whose purpose line is its title.
- [ ] **Nothing in the spec describes a learner's progress.** You are designing a course,
      and the course has no learner in it yet.

This is a first filter, not a proof. Only walking the course finds the rest. Say so when
you present the spec, rather than implying the arc has been verified.

---

## 5. The gate

Save the spec to `specs/<bundle-id>.md` in the bundles repository — see
`course-spec-format.md` for what it contains — and **stop**.

> "The course spec is at `specs/<bundle-id>.md`. Have a look and tell me what to change.
> I will not create any bundle file until you say it is right."

Wait for an explicit yes. Presenting the spec and starting to generate in the same breath
is skipping the gate. If the author asks for changes, make them, re-run the self-check,
and present again.

The gate does not scale down. A four-lesson course gets a one-page spec and the same stop.

---

## 6. After approval: the generation order

Order matters, because the format's invariants are easier to keep than to repair.

1. **Create the skeleton by hand**, in a new bundle directory: `tutorial.yaml` with
   `lessons: []`, `COURSE.md` from the chapter map and coverage list, `DESIGN.md` with one
   anchored section per phase 4 decision, `STATE.template.md` describing a learner who has
   not started, and an empty `lessons/`. These are judgement, not bookkeeping, and no
   script writes them.
2. **Add every lesson with the toolkit**, in spec order:
   `python3 scripts/lesson.py add <bundle> --id <slug> --title <text> --position <n>`, with
   `--folder` for a lesson that ships material. This is what keeps `id` equal to the slug
   and the `lessons` list complete. Never create a lesson file yourself.
3. **Put the supplied files in the bundle and declare every one of them.** The files the
   course hands over go inside the bundle first — by convention `supplies/` at the bundle
   root for a manifest-scope entry, and the lesson's own folder for a lesson-scope one,
   which is also where the format's material checks expect them. Then declare each with
   `python3 scripts/supplies.py add <bundle> --from <path> --to <path> --describe <text>`,
   adding `--lesson <lesson-id>` when the files arrive with a lesson rather than at the
   start. Do this before you fill any lesson body, because a body written while the
   handover is still undeclared is a body that assigns it.
4. **Fill each lesson body** — purpose, prerequisites, objectives, theory, concepts,
   constraints, suggested progression, completion conditions, what to persist. Give it
   objectives, never dialogue; the tutor generates the conversation.
5. **Set `design_refs` and `validators`** in each lesson's frontmatter from the spec.
6. **Confirm the two links by hand**: `STATE.template.md`'s `tutorial_id` equals
   `tutorial.yaml`'s `id`, and its `active_lesson` equals the first entry of `lessons`.
7. **Validate**, and work through the runner's `bundle-format.md` section 10 self-check by
   looking at the files.
8. **Rebuild the catalogue**: `python3 scripts/catalog.py <bundles-repo>`, because a new
   bundle that no catalogue lists is a bundle no learner can find.

A skeleton with no lessons is not a valid bundle — the format requires at least one. Do
not stop between steps 1 and 2, and do not be surprised when a validator run in that gap
reports it.

### Depth

Author the lessons a learner will reach soon, in full. A long course may legitimately keep
its later chapters as a map in `COURSE.md` with no lesson file — that was decided in
section 1 and recorded in the spec. Prefer a small number of good lessons to a large
number of thin ones.
