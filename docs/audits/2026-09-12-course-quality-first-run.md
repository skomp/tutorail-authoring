# Task B6 — the `course-quality` skill run against the real courses

> ## CORRECTION, 2026-09-12 — the totals below are superseded
>
> **What changed.** Section 0 of this report says constraints "addressed to the **tutor**
> rather than the learner are not scored either", and section T5 records that exclusion as
> a gap for the owner to settle. It was settled, the other way:
> `skills/course-quality/references/rubric.md` now reads **"A tutor-addressed element
> scores `teaching`, +2, when the learner must decide or construct in response"**, and adds
> that the grammatical person the author wrote in does not change what the learner does.
>
> **Why the totals move.** This report scored those elements at `0` by exclusion. Under the
> settled rule they score `+2` wherever the learner must decide or construct. So **194 /
> 193 / 211 are not reproducible under the current rubric.** They are superseded, not wrong:
> the arithmetic as published was re-checked and is correct under the rubric in force when
> the run was made. Every lesson figure here is still the visible sum of its own elements.
>
> **Which figures the settled rule moves.** Two, both named in T5:
>
> - **`webgl 11`** — `11-secondary-demo-scene/LESSON.md:31`–`:34`, the whole "the tutor MUST
>   explicitly ask" block. T5 already says it is "load-bearing teaching content — it is what
>   makes the learner's choice a real choice", which is exactly the condition the settled
>   rule scores `+2`. The rubric's own statement of the rule cites this lesson.
> - **The regenerated `01-canvas-and-context/LESSON.md:42`–`:48`** bootstrap paragraph, in
>   audit 2. This one matters most, because **audit 2's whole comparison turns on it**: the
>   193-versus-194 gap is a one-point difference between two versions of the same course,
>   and this block is scored `0` in the candidate and has no counterpart in the catalogue
>   version. Re-score it `+2` and the direction of that comparison is no longer settled by
>   this report.
>
> `00-project-setup/LESSON.md:38` ("Read `starter/README.md` before giving the first task")
> is the control: it is tutor-addressed too, and the learner decides and constructs nothing
> in response, so the settled rule leaves it at `0`. The rule is not "score every sentence
> that addresses the tutor".
>
> **The totals are deliberately not recomputed here.** A re-score is a fresh audit run
> against the current rubric, with every element re-read and re-quoted; patching three
> numbers into a report whose method section describes the old rule would produce a document
> that disagrees with itself. Treat the per-element evidence below as sound and the three
> totals as belonging to the rubric of 2026-09-12 before this rule was settled.

First real run of `skills/course-quality/SKILL.md` and `skills/course-quality/references/rubric.md`.
Three audits, in this order:

| # | Course | Path | Total |
|---|---|---|---|
| 1 | `webgl-typescript-scene` (catalogue version) | `../tutorail-bundles/webgl-typescript-scene` | **194** |
| 2 | `webgl-typescript-scene` (regenerated candidate) | `…/scratchpad/wz/webgl-typescript-scene` | **193** |
| 3 | `durable-event-broker` | `../tutorail-bundles/durable-event-broker` | **211** (main path alone: **170**) |

**No bundle was changed.** Every finding below is a proposal. Applying one goes back
through the `tutorail-authoring` skill and its toolkit, after the owner says yes.
Section 8 reports what this exercise revealed about the tooling, which the plan says is
the most valuable thing this task produces. If you read one section, read that one.

---

## 0. How I scored, so you can argue with it

The rubric says a score with no `file:line` and no quoted sentence cannot be disagreed
with. That is only true if the *method* is also visible, so here it is.

An **element** is one of:

1. a clause of **`## Suggested progression`** that assigns the learner an action;
2. a clause of **`## Constraints`** that assigns work the progression does not already
   name (a constraint that merely qualifies a progression step is folded into it, never
   counted twice);
3. a clause of **`## Completion conditions`** that requires the learner to *construct an
   account* — "the learner can explain / trace / classify / name". The rest of the
   completion block is one element scoring `0` (evidence), because running validators and
   reading output is exactly what the `0` row describes.

`## Theory`, `## Concepts to teach` and `## On completion, persist` are **not** scored.
Theory and Concepts state what the tutor says; they assign the learner nothing. Persist
steps are state-keeping. Constraints addressed to the **tutor** rather than the learner
are not scored either — this matters in audit 2, and it is called out there.

Scores are the rubric's: `+2` teaching, `+1` practice, `0` evidence, `−2` toil,
`−3` per unserved objective or anchor, `−3` per `required_for` gate on an optional lesson.
Course-level penalties are counted separately and never folded into a lesson's figure.

**Which list is "stated objectives".** The skill's section 3 says "every stated learning
objective"; `audit.py` surfaces the `COURSE.md` coverage list. Those are two different
lists. I scored **both**: the coverage list at course level (it is the course's declared
boundary), and each lesson's own `## Learning objectives` against that lesson's elements.
Section 8 records this as an ambiguity in the skill.

---

# AUDIT 1 — `webgl-typescript-scene`, the catalogue version

## 1. The course and its total

- **Bundle id:** `webgl-typescript-scene`
- **Title:** Learn WebGL 2 by Building a 3D Scene
- **Lessons:** 19 on the main path
- **Optional lessons declared in the manifest:** **0** — see the note below, it matters
- **`supplies:` entries declared:** none

```
sum of the 19 lessons                                        194
unserved coverage topics            0 x -3                  -  0
unserved DESIGN.md anchors          0 x -3                  -  0
required_for gates on optional lessons  0 x -3              -  0
                                                            ----
TOTAL                                                        194
```

**The manifest declares no optional lessons, but the course has one.** `COURSE.md:138`
says "Lesson 14 is optional." The lesson's own title is "Optional — decode the packaged
GLB yourself" and `lessons/14-optional-minimal-gltf-loader/LESSON.md:41` says "The learner
may skip this lesson without implementing anything; record that choice and advance."
Yet `tutorial.yaml:27` lists it under `lessons:`, not `optional_lessons:`. Consequences:

- `audit.py` reports "0 optional" and the completability machinery never engages;
- the runner presents lesson 14 as a main-path lesson, so the *offer* the course intends
  is made only by the lesson's own prose, to whatever tutor happens to read it;
- the rubric therefore scores lesson 14's full **11 points** into the course total, even
  though a learner who skips it — which the course invites — collects **0** from it.

A learner who skips lesson 14 experiences a **183**-point course, not a 194-point one.
Both figures are real; the rubric as written reports only the second.

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil found |
|---|---:|---|---|
| `00-project-setup` | **−2** | 3 of 3, but none maps to a coverage topic | 1 site |
| `01-canvas-and-context` | 9 | 4 of 4 | — |
| `02-first-shader-program` | 11 | 4 of 4 | — |
| `03-vertex-data` | 10 | 4 of 4 | — |
| `04-uniforms-and-animation` | 7 | 4 of 4 | — |
| `05-transforms-and-perspective` | 8 | 4 of 4 | — |
| `06-depth-and-culling` | 7 | 4 of 4 | — |
| `07-indexed-meshes-and-vaos` | 12 | 4 of 4 | — |
| `08-textures` | 13 | 4 of 4 | — |
| `09-normals-and-lighting` | 9 | 4 of 4 | — |
| `10-camera-and-scene` | 11 | 5 of 5 | — |
| `11-secondary-demo-scene` | 11 | 4 of 4 | — |
| `12-scene-transition` | 12 | 4 of 4 | — |
| `13-load-gltf-model` | 7 | 5 of 5 (obj 5 **only** by the toil span — see below) | 1 site |
| `14-optional-minimal-gltf-loader` | 11 | 4 of 4 | — |
| `15-render-to-texture` | 11 | 4 of 4 | — |
| `16-bloom` | 15 | 4 of 4 | — |
| `17-depth-reconstruction-and-ssr` | **21** | 5 of 5 | — |
| `18-finish-the-scene` | 11 | 4 of 4 | — |
| **Sum** | **194** | | **2 sites** |

### Element breakdown

Every lesson is broken out, not only the ones at or below zero, because no figure above is
obvious from its row.

**`00-project-setup` = −2** — the only lesson in either course with a negative figure.

| Score | `file:line` | The sentence it scored |
|---:|---|---|
| **−2** | `lessons/00-project-setup/LESSON.md:34` | "Copy `starter/package.json`, `starter/package-lock.json`, `starter/tsconfig.json`, `starter/index.html` and `starter/src/main.ts` into their corresponding repository-root paths, preserving `src/`." |
| 0 | `:42` | "Install dependencies" — see section 8, finding T4: the rubric's toil test catches this and the rubric's remedy does not apply to it. |
| 0 | `:42` | "inspect each supplied file" — constructs nothing and applies nothing already taught; closest row is evidence. |
| 0 | `:42` | "type-check, build, start the development server, and verify both page output and the absence of console errors" |
| 0 | `:47` | "`npm run typecheck` and `npm run build` succeed. `npm run serve` exposes the page on its reported local URL, the page shows the starter heading, and the console has no error." |

Sum: −2 + 0 + 0 + 0 + 0 = **−2**.

Not scored: `:37` "Do not introduce a framework…" and `:38` "Read `starter/README.md`
before giving the first task" — both addressed to the tutor.

**`01-canvas-and-context` = 9.** `:41` "Acquire the context" +2 (obj 1). `:41` "choose an
unmistakable clear colour" +1. `:41` "resize the drawing buffer" +2 (obj 2; `:36`
"cap or explain the chosen device-pixel-ratio policy" folded in). `:42` "set the viewport"
+1. `:42` "clear" +1. `:42` "inspect the result at more than one browser-window size" 0.
`:47` "a missing context produces a useful error rather than a null dereference" +2 (obj 4).

**`02-first-shader-program` = 11.** `:36` "Generate three positions from `gl_VertexID`" +2.
`:41` "Write and compile each shader separately" +2. `:41` "link the program" +1. `:41`
"select it, issue one triangle draw" +1. `:36` "Check compile and link status and include
diagnostic logs in thrown errors" +1. `:42` "deliberately break a shader briefly to observe
the diagnostic path" +2. `:47` "the learner can explain the value written to `gl_Position`
and why the fragment shader needs a precision declaration" +2.

**`03-vertex-data` = 10.** `:41` "Upload positions" +2. `:41` "connect the position
attribute" +2 (`:36` byte-based stride and offset folded in). `:41` "add colour data and
pass it between shader stages" +2. `:42` "Change one layout parameter intentionally and
reason from the corrupted image" +2. `:47` "the learner can account for every
attribute-layout argument in bytes" +2.

**`04-uniforms-and-animation` = 7.** `:42` "Add a scalar uniform, make it affect the
shader" +2. `:42` "introduce the frame callback" +2. `:43` "verify that refreshing or
resizing does not create multiple loops" 0. `:38` "Handle a missing required uniform
location explicitly" +1. `:48` "The learner can classify current data as per-vertex,
per-draw or per-frame" +2.

**`05-transforms-and-perspective` = 8.** `:41` "Create a cube or other simple volume" +1.
`:41` "add model then view then projection transforms" +2. `:41` "predict the result of
changing each" +2. `:42` "update aspect ratio after canvas resize" +1. `:46` "The learner
can trace a sample vertex through the named spaces and explain near-plane clipping
qualitatively" +2.

**`06-depth-and-culling` = 7.** `:40` "Capture the incorrect overlap" +2 — the lesson's
best move, failure before fix. `:40` "enable depth testing" +1. `:40` "rotate through
several views" 0. `:40` "inspect mesh winding" +2. `:41` "then enable and toggle back-face
culling" +1. `:46` "The learner can name the colour and depth buffers cleared each frame"
+1 — recall, not construction, so practice rather than teaching.

**`07-indexed-meshes-and-vaos` = 12.** `:43` "Convert the procedural object to indices" +2.
`:43` "bind its element buffer in a VAO" +2. `:43` "define `MeshData`" +2. `:44` "write one
upload path and one draw path" +2. `:44` "ensure temporary resources can be deleted" +1.
`:38` "Validate array lengths and supported index types before upload" +1. `:50` "the
learner can explain what state the VAO does and does not capture" +2.

**`08-textures` = 13.** `:41` "Render UVs as colours" +2. `:41` "upload a labelled image"
+2. `:41` "bind it through a sampler" +1. `:41` "test orientation" +2 (`:36` "Make the
vertical orientation decision explicit"). `:42` "compare nearest and linear filtering" +2.
`:42` "enable a valid mipmap policy" +1. `:37` "Keep rendering valid while an image is
still loading" +1. `:47` "The learner can trace a texture sample from vertex attribute to
fragment colour" +2.

**`09-normals-and-lighting` = 9.** `:41` "Visualise normals as colour" +2. `:41` "add the
light vector and diffuse term" +2. `:41` "combine with texture colour" +1. `:42` "rotate
the model" 0. `:42` "test a non-uniform scale to expose incorrect normal transformation"
+2. `:47` "The learner can explain the spaces used by every vector in the dot product" +2.

**`10-camera-and-scene` = 11.** `:47` "Extract camera state" +2. `:47` "render a small
fixed set of instances" +1. `:47` "move placement into a divisor-backed instance attribute"
+2. `:48` "expand to a grid" +1. `:48` "derive vertical displacement from time and grid
position" +2. `:49` "add crest-dependent colour or brightness" +1. `:49` "orbit the camera"
+2. `:49` "verify resize behaviour" 0.

**`11-secondary-demo-scene` = 11.** `:54` "Present the sorted catalogue, ask for the
learner's selection and desired visual mood" +2 — the learner decides, which is the whole
point of the lesson. `:55` "agree a bounded definition of done" +2. `:55` "define the
minimal shared scene lifecycle" +2. `:56` "adapt the cube-wave scene to it without visual
changes" +1. `:56` "build the selected effect from its core mechanism outward" +2. `:57`
"verify independent resize, pause and disposal behaviour" 0. `:48` "For Level 3 or 4
choices, establish one diagnostic visualisation before the final look" +2.

**`12-scene-transition` = 12.** `:46` "Render each scene to its own target" +2. `:46`
"display each directly" +1. `:46` "implement crossfade with manual progress" +2. `:47` "add
time-based direction and easing" +2. `:47` "present `transition-menu.md`, ask for a choice"
+2. `:48` "implement and validate the selected transition at endpoints and intermediate
values" +2. `:42` "The transition owns its targets and resizes and disposes them
explicitly" +1.

**`13-load-gltf-model` = 7.**

| Score | `file:line` | The sentence it scored |
|---:|---|---|
| **−2** | `lessons/13-load-gltf-model/LESSON.md:40` | "Before starting, copy every file under `model/` to a repository-root `models/` directory: `Duck.glb`, `LICENSE.md`, `SCEA.txt` and `ATTRIBUTION.md`." |
| +2 | `:50` | "Fetch and parse `models/Duck.glb`" |
| +1 | `:50` | "inspect its scene and first mesh primitive" |
| +2 | `:50` | "adapt accessors to `MeshData`" |
| +1 | `:51` | "handle its base-colour texture" |
| +1 | `:51` | "upload through the established mesh path" |
| +1 | `:52` | "then place the duck as a normal scene object" |
| +1 | `:45` | "Reject missing required attributes with useful errors." |

Sum: −2 +2 +1 +2 +1 +1 +1 +1 = **7**.

**The objective the toil is carrying.** Objective 5 at `:24` is "Carry asset licence and
attribution into the repository". The **only** element that serves it is the toil span at
`:40`. If that span is replaced by a `supplies:` entry and the prose deleted without care,
objective 5 becomes an unserved objective and the lesson costs the course −3. The proposal
in section 5 handles this explicitly.

**`14-optional-minimal-gltf-loader` = 11.** `:48` "Choose or skip the path" **0** — the
rubric has no row for a branch point (section 8, finding T5). `:48` "parse and validate the
GLB envelope" +2. `:49` "decode JSON, locate the binary chunk" +1. `:49` "implement
accessor extraction" +2. `:49` "adapt the supported primitive" +2. `:50` "decode its
embedded image" +1. `:50` "compare with the library-backed result" 0. `:50` "switch
adapters only after equivalence" +1. `:43` "Implement only `supported-subset.md`, reject
everything else clearly" +2.

**`15-render-to-texture` = 11.** `:45` "Allocate attachments" +2. `:45` "check
completeness" +1. `:45` "render the scene off-screen" +1. `:45` "display its colour through
a full-screen triangle" +2. `:46` "expose the depth texture as a diagnostic view" +2. `:47`
"then integrate resize and cleanup" +2. `:53` "an incomplete configuration produces a
useful failure" +1. `:41` "Provide a direct-copy composition shader before adding effects"
is folded into the full-screen-triangle step — and is the scanner's negative control; see
section 4.

**`16-bloom` = 15** — the second-largest lesson. `:43` "Introduce emissive/bright scene
values" +1. `:43` "validate the HDR target" +1. `:43` "extract bright regions" +2. `:43`
"implement one blur direction" +2. `:44` "ping-pong the second direction for a small fixed
number of iterations" +2. `:45` "then additively compose and tune threshold/intensity" +2.
`:37` "check required capabilities" +1. `:38` "Let the learner view the bright pass, each
blur direction and final composition independently" +1. `:39` "Bloom must be toggleable"
+1. `:51` "the learner can explain why ordinary clamped colour prevents useful
thresholding" +2.

**`17-depth-reconstruction-and-ssr` = 21** — the outlier; see section 6, row C. `:50` "Add
and inspect the normal target" +2. `:50` "reconstruct and visualise linear/view-space
depth" +2. `:51` "reconstruct positions" +2. `:51` "verify them by camera motion" 0. `:51`
"derive the reflection ray" +2. `:52` "display projected ray steps" +2. `:52` "add
depth-crossing detection" +2. `:52` "refine the first hit locally" +1. `:53` "sample
reflected colour" +1. `:53` "then add edge, distance and grazing-angle fades" +2. `:44`
"Bound loop iterations for WebGL shader compilation and performance" +1. `:45` "Expose step
count, thickness and maximum distance as controlled parameters" +1. `:46` "SSR must be
toggleable" +1. `:60` "the learner can explain at least four failure modes inherent to SSR"
+2.

**`18-finish-the-scene` = 11.** `:45` "Choose a composition that makes reflections and
bloom readable" +2. `:45` "integrate asynchronous loading" +1. `:46` "tune camera and
lighting" +1. `:46` "tune effects without hiding their artefacts" +1. `:47` "test resize
and extreme camera positions" 0. `:47` "audit allocations/state transitions" +2. `:47`
"then perform deliberate geometry-pass and post-processing failure investigations" +2.
`:57` "The learner can explain the end-to-end pipeline and isolate failures by pass" +2.

## 3. Goal gaps

**Coverage topics: 0 unserved of 56.** I walked all 56 topics from `COURSE.md:70`–`:125`
against the lessons I had opened, not against `topic_candidates`. Every one is exercised by
at least one element. Three deserve their reasoning written down, because they are the ones
a later reader would re-litigate:

- **"GLSL types and precision"** (`COURSE.md:76`) — served by `02-first-shader-program.md:48`,
  "why the fragment shader needs a precision declaration". *Types* are implicit in writing
  GLSL at all; I accepted that. A stricter reader could call this half-served.
- **"mipmaps and power-of-two considerations"** (`:97`) — served by `08-textures.md:42`,
  "enable a valid mipmap policy". In WebGL 2 the power-of-two restriction is gone, so
  "valid mipmap policy" *is* the modern form of the consideration. Accepted.
- **"multiple render targets"** (`:115`) — `16-bloom.md:32` offers "multiple render targets
  **or** extraction passes", so bloom alone does not require MRT. But
  `17-depth-reconstruction-and-ssr.md:42` says "Add a view-space normal attachment with a
  defined encoding", which the scene pass cannot satisfy without a second colour
  attachment. Served by lesson 17, not by lesson 16.

**`DESIGN.md` anchors: 0 unserved of 16.** Fifteen of the sixteen appear in some lesson's
`design_refs`. The sixteenth, **`#unresolved-decisions`** (`DESIGN.md:116`), appears in no
`design_refs` entry — and is nevertheless served. Its text is "The concrete `MeshData`
TypeScript shape, camera input mapping, scene composition and final visual styling are
learner decisions made at the lessons that need them. Record those choices under new stable
anchors in the instance's `DESIGN.md`." That is precisely what
`07-indexed-meshes-and-vaos.md:54` ("Add a stable design anchor documenting the concrete
`MeshData` shape and resource ownership"), `10-camera-and-scene.md:60`,
`11-secondary-demo-scene/LESSON.md:68` and `18-finish-the-scene.md:61` instruct. **No −3.**

This one is worth flagging as a method warning: a mechanical proxy — "is the anchor named
in some `design_refs` list?" — would have charged −3 here and been wrong. See section 8,
finding T6.

**Lesson-level objectives: 0 unserved.** All 78 are exercised by an element of their own
lesson, with the caveat recorded at lesson 13 above (objective 5 is carried entirely by the
toil span).

**Arithmetic check:** 0 gaps listed, 0 × −3 = 0 subtracted in section 1. Agreed.

## 4. The toil inventory

**Confirmed toil — 2 sites, −4 total.**

1. `lessons/00-project-setup/LESSON.md:34`

   > Copy `starter/package.json`, `starter/package-lock.json`, `starter/tsconfig.json`,
   > `starter/index.html` and `starter/src/main.ts` into their corresponding repository-root
   > paths, preserving `src/`.

   The sentence spans physical lines 34–36; `audit.py`'s `text` field stops at the comma at
   the end of line 34. Deterministic, unambiguous, no decision, and a mistake teaches
   nothing about WebGL. This is the sentence that started the whole change.

2. `lessons/13-load-gltf-model/LESSON.md:40`

   > Before starting, copy every file under `model/` to a repository-root `models/`
   > directory: `Duck.glb`, `LICENSE.md`, `SCEA.txt` and `ATTRIBUTION.md`.

   Spans lines 40–41. Same judgement. Note that this one is doing double duty — see the
   objective-5 warning at lesson 13 above.

**Script candidates examined and rejected — 1.**

- `lessons/00-project-setup/LESSON.md:42` `[install]` — "Install dependencies, inspect each
  supplied file, type-check, build, start the development server, and verify both page
  output and the absence of console errors." I split it. "Install dependencies" is
  deterministic but **not removable by `supplies:`**: `node_modules` is not a bundle
  artefact and no `supplies:` entry can create it. Scored `0`, not `−2`. Everything after
  the first comma is the lesson. Section 8, finding T4, argues the rubric's toil row is
  worded in a way that catches this and should not.

**The scanner's negative control passed, and I checked why.**
`lessons/15-render-to-texture.md:41` reads "state for every pass. Provide a direct-copy
composition shader before adding effects." The `copy` pattern requires the verb in a lead
position (line start, bullet, after `.␣`, after `,␣`, after `must`/`should`/`then`). In
`direct-copy` the verb is preceded by a hyphen, so none of those apply. I confirmed this
against the live pattern with a positive control in the same call:

```
negative control fires: False
POSITIVE control fires: True      # "Copy `starter/package.json` into place."
```

**The scanner is a candidate generator, and this inventory came from the lessons.** All 19
lesson files were opened and read in full. The two confirmed sites happen to coincide with
two of the three candidates, which is a fact about this corpus and not a property of the
tool. An empty candidate list would not have been evidence of anything.

## 5. Proposals

**P1 — replace the lesson 00 toil with a manifest-level `supplies:` declaration.**
The five files are placed at materialisation, before any lesson opens, so they belong in
`tutorial.yaml` and take no `--lesson`. Five entries rather than one
`--from lessons/00-project-setup/starter/ --to .`, because that directory form would also
place `starter/README.md` into the learner's workspace root, where it is not listed in
`learner_owned` (`tutorial.yaml:35`) and where it does not belong — it is tutor-facing
material read at `00-project-setup/LESSON.md:38`.

```
python3 scripts/supplies.py add ../tutorail-bundles/webgl-typescript-scene \
  --from lessons/00-project-setup/starter/package.json \
  --to package.json \
  --describe "the npm manifest and its scripts for the graphics workspace" --check
python3 scripts/supplies.py add ../tutorail-bundles/webgl-typescript-scene \
  --from lessons/00-project-setup/starter/package-lock.json \
  --to package-lock.json \
  --describe "the pinned dependency lockfile" --check
python3 scripts/supplies.py add ../tutorail-bundles/webgl-typescript-scene \
  --from lessons/00-project-setup/starter/tsconfig.json \
  --to tsconfig.json \
  --describe "the strict TypeScript configuration used by npm run typecheck" --check
python3 scripts/supplies.py add ../tutorail-bundles/webgl-typescript-scene \
  --from lessons/00-project-setup/starter/index.html \
  --to index.html \
  --describe "the plain HTML page that hosts the canvas and the bundled entry point" --check
python3 scripts/supplies.py add ../tutorail-bundles/webgl-typescript-scene \
  --from lessons/00-project-setup/starter/src/main.ts \
  --to src/main.ts \
  --describe "the starter TypeScript entry point" --check
```

`--from` is bundle-relative; `--to` is workspace-relative. Run with `--check` first — this
is the `tutorail-authoring` toolkit's job, not this skill's, and the paths above are
relative to that skill's directory.

**Prose to delete once the entries exist:** `lessons/00-project-setup/LESSON.md:34`–`:36`
in full, the whole `Copy … preserving \`src/\`.` sentence. Keep `:37`–`:38` ("Do not
introduce a framework…" and "Read `starter/README.md` before giving the first task"): the
first is a real constraint and the second is what tells the tutor where the supplied
commands are documented. **Do not delete the prose without adding the entries** — the
learner would be left without the files.

**P2 — replace the lesson 13 toil with a lesson-scoped `supplies:` declaration, and
re-home objective 5.** These files belong to lesson 13 and should appear when it opens.

```
python3 scripts/supplies.py add ../tutorail-bundles/webgl-typescript-scene \
  --from lessons/13-load-gltf-model/model/ \
  --to models \
  --describe "Duck.glb and its licence and attribution files, which travel together" \
  --lesson 13-load-gltf-model --check
```

**Prose to delete:** `lessons/13-load-gltf-model/LESSON.md:40`–`:41`, up to and including
"`ATTRIBUTION.md`." **Keep** the rest of `:41`–`:42`: "Read `model/ATTRIBUTION.md` when
introducing the asset and retain all four files together."

**And this proposal has a condition.** Learning objective 5 (`:24`, "Carry asset licence
and attribution into the repository") is currently served by nothing except the sentence
being deleted. Either:

- (a) keep `:64` "Record the model attribution in the project documentation" and promote it
  from `## On completion, persist` into `## Suggested progression`, so an element serves the
  objective; or
- (b) reword objective 5 to what the lesson would then actually teach — that licence files
  travel with an asset and must not be separated from it — which `:42` and `:56` already
  assert.

Without one of these, applying P2 converts a −2 into a −3 and makes the course slightly
worse by the rubric. This is the single most important thing to get right when applying
these proposals.

**P3 — a question about `00-project-setup`, which scores −2.** The rubric requires this to
be a question, not a deletion proposal. The elements that produced the figure are in the
table above: one toil span at −2 and four elements at 0. After P1, its figure becomes **0**
— four evidence elements and nothing else, and no coverage topic in `COURSE.md:70`–`:125`
that it serves.

> What is lesson 00 for, once the files arrive on their own? It teaches no topic the course
> declares it must cover. Its three objectives are "Distinguish type checking, bundling and
> static serving", "Run a TypeScript entry point in a plain HTML page" and "Use the console
> and page as separate sources of evidence" — all real, none of them WebGL, and all of them
> discharged by running four commands. The regenerated candidate in audit 2 answers this by
> folding it into lesson 01. That is a reasonable answer. So is keeping it as a deliberate
> warm-up. It is your call, and the rubric cannot make it.

**P4 — move lesson 14 into `optional_lessons:`.** The course already treats it as optional
in three places (`COURSE.md:138`, the lesson title, `LESSON.md:41`). Declaring it in the
manifest would make the runner offer it, make `audit.py` report it, and bring the
completability invariant into scope for this course. It needs no `required_for` — the
lesson explicitly says the library path remains intact when skipped
(`14-optional-minimal-gltf-loader/LESSON.md:54`), and `15-render-to-texture.md:15` already
names both outcomes: "lesson `14-optional-minimal-gltf-loader` was completed or skipped."
That prerequisite line is exactly what a correctly declared optional lesson looks like.

## 6. The questions only a reader can answer

**Row A — a `design_refs` entry that does not answer the question its lesson raises.**
**One found.**

`lessons/06-depth-and-culling.md:4` declares `design_refs: [api-boundary, matrix-convention]`.
The lesson raises "Relate vertex winding to front and back faces" (`:20`) and "Diagnose
missing faces caused by inconsistent winding" (`:21`), and asks the learner at `:50` to
"Record the depth function, front-face convention and culling decision." A learner who
follows either anchor to find out **which winding is front** does not find out.
`#api-boundary` (`DESIGN.md:10`) says only that rendering uses `WebGL2RenderingContext`
directly. `#matrix-convention` (`DESIGN.md:16`) fixes handedness, column vectors,
`projection * view * model`, camera down −Z and radians — everything that *determines* the
front-face winding, and not the winding itself. Both references resolve, the validator is
green, and the question is unanswered.

*Considered and rejected:* `lessons/15-render-to-texture.md:4` → `#scene-boundary`
(`DESIGN.md:41`). The anchor is about scene objects and per-frame state ordering while the
lesson is about framebuffers; but the off-screen pass genuinely changes per-frame state
ordering, so the reference earns its place. Weak, not wrong.

**Row B — a lesson that introduces a type or concept nothing later uses.** **None found.**
The closest calls, both cleared:

- `03-vertex-data.md:21`, "Add per-vertex colour and observe interpolation". Per-vertex
  colour is superseded by textures at lesson 08 and by lighting at lesson 09, and nothing
  later uses a colour attribute. But the *varying* it introduces is used in every lesson
  from 08 onward for UVs and normals, and that is what the objective is for. Cleared.
- `08-textures.md:42`, "enable a valid mipmap policy". No later lesson revisits mipmaps, and
  the post-processing targets in 15–17 deliberately do not use them. It serves a declared
  coverage topic (`COURSE.md:97`) on its own, so it is not attention bought for nothing.
  Cleared, and it is the closest thing in the course to a hit.

**Row C — a lesson far outside the course's usual size.** **Two found, one in each
direction.**

- **`17-depth-reconstruction-and-ssr.md` is much larger.** 21 points against a course median
  of 11; 14 scored elements against a median of 7; ten clauses in one `## Suggested
  progression` sentence at `:50`–`:54`; five learning objectives, which only two other
  lessons reach; 69 lines. The rubric's guidance is that a much larger lesson is usually two,
  and the seam is visible in the lesson's own structure: `:50`–`:51` "Add and inspect the
  normal target, reconstruct and visualise linear/view-space depth, reconstruct positions,
  verify them by camera motion" is **depth reconstruction** and stands alone with its own
  diagnostic; `:51`–`:54` from "derive the reflection ray" onward is **SSR** and depends on
  it. Objectives 1–2 belong to the first, 3–5 to the second. A question, not a proposal:
  the lesson's title names both halves, which suggests you already saw this and decided
  against splitting.
- **`00-project-setup/LESSON.md` is much smaller**, and after P1 becomes four evidence
  elements. The rubric says a much smaller lesson is usually a paragraph of the lesson
  beside it. That is exactly what the regenerated candidate does. See audit 2.

**The completability invariant.**

> Can a learner who declines every offer still finish this course?

**Not applicable — no optional lessons are declared in `tutorial.yaml`.** I keyed this off
the presence of an `optional_lessons:` key in the manifest, not off
`optional_lesson_count`. The key is absent.

**But the answer is not as clean as the manifest makes it look.** The course describes
lesson 14 as optional in prose (`COURSE.md:138`, `LESSON.md:41`) while listing it under
`lessons:`. The invariant is formally out of scope and substantively in play. Answering it
anyway, from the lessons: **yes** — `15-render-to-texture.md:15` names both outcomes
explicitly ("was completed or skipped"), `13-load-gltf-model.md:68` says lesson 14 "is not
required for WebGL coverage or the final scene", and `18-finish-the-scene.md` requires only
"the packaged duck", not a particular loader. No main-path completion condition depends on
lesson 14, and no main-path prose assumes the learner took it. The course is completable by
a learner who skips it. P4 would make the manifest say so.

---

# AUDIT 2 — `webgl-typescript-scene`, the regenerated candidate

Unpacked at
`/private/tmp/claude-501/-Users-robert-src-github-com-skomp-tutorail-authoring/89d87f4d-f904-4106-9206-17ba8542c620/scratchpad/wz/webgl-typescript-scene`.
Read-only; nothing there was modified.

**What actually differs.** I diffed the trees rather than trusting the summary. The
difference is exactly four things:

1. `lessons/00-project-setup/` is gone; `lessons/01-canvas-and-context.md` became
   `lessons/01-canvas-and-context/LESSON.md` and absorbed the `starter/` directory.
2. `tutorial.yaml:35` — `ownership_policy: tutor-must-not-edit-learner-owned` →
   `ownership_policy: unrestricted`.
3. `COURSE.md` — the course map renumbers 1–18, and a new paragraph in Teaching philosophy
   describes the tutor bootstrap.
4. `STATE.template.md:3` — `active_lesson` repointed.

**Lessons 02 through 18 are byte-identical to the catalogue version.** So the entire score
difference lives in lesson 00/01 and the manifest, and every element breakdown in audit 1
for lessons 02–18 carries over unchanged.

## 1. The course and its total

- **Lessons:** 18 on the main path
- **Optional lessons declared:** 0 (same prose/manifest mismatch at lesson 14 as audit 1)
- **`supplies:` entries declared:** none

```
sum of the 18 lessons                                        196
unserved objective: "static serving"   1 x -3               -  3
unserved DESIGN.md anchors             0 x -3               -  0
required_for gates                     0 x -3               -  0
                                                            ----
TOTAL                                                        193
```

196 rather than 194 because the −2 toil span at `00-project-setup/LESSON.md:34` is gone and
the lesson that carried it is gone with it. The new lesson 01 scores 9, the same as the old
lesson 01.

## 2. The per-lesson table

Lessons 02–18 are unchanged; their rows and element breakdowns are in audit 1, section 2.
Only the first row is new.

| Lesson | Score | Objectives served | Toil found |
|---|---:|---|---|
| `01-canvas-and-context` (rewritten) | 9 | 4 of 5 — objective 5 partly unserved | — (the copy is now tutor work; see below) |
| `02-first-shader-program` … `18-finish-the-scene` | 187 | as audit 1 | 1 site (lesson 13, unchanged) |
| **Sum** | **196** | | **1 site** |

### Element breakdown — `01-canvas-and-context` = 9

| Score | `file:line` | The sentence it scored |
|---:|---|---|
| +2 | `lessons/01-canvas-and-context/LESSON.md:55` | "After tutor bootstrap succeeds, ask the learner to acquire the context." |
| +1 | `:55` | "Then choose an unmistakable clear colour" |
| +2 | `:56` | "resize the drawing buffer" |
| +1 | `:56` | "set the viewport" |
| +1 | `:56` | "clear" |
| 0 | `:56` | "inspect the result at more than one browser-window size" |
| +2 | `:63` | "a missing context produces a useful error rather than a null dereference" |

Sum: **9**.

**Not scored, and this is the interesting part.** `:42`–`:48`:

> Before presenting any learner task, the tutor MUST read `starter/README.md`; copy
> `starter/package.json`, `starter/package-lock.json`, `starter/tsconfig.json`,
> `starter/index.html` and `starter/src/main.ts` into their corresponding workspace-root
> paths; initialise Git if the workspace is not already a repository; run `npm install`;
> and verify the untouched starter with `npm run typecheck` and `npm run build`. This
> bootstrap is tutor work and is not offered as the first task.

Under the rubric this is **not toil**, because toil is work the bundle *assigns the
learner*, and this is explicitly assigned to the tutor ("This bootstrap is tutor work and
is not offered as the first task", `:46`). It costs the learner no attention. So the
regenerated version's lesson-00 toil score is correctly 0 rather than −2.

**That is also the whole problem.** The file copy did not go away. It was **re-assigned**,
and re-assigning it cost a manifest-level safety property — see section 5 below. A
`supplies:` entry would have removed it without either.

## 3. Goal gaps

**One unserved objective: −3.**

`lessons/01-canvas-and-context/LESSON.md:23` states:

> - Distinguish type checking, bundling and static serving when using the prepared workspace

**No element in the regenerated course exercises "static serving", and no completion
condition verifies it.** The tutor bootstrap at `:42`–`:46` runs `npm install`,
`npm run typecheck` and `npm run build` — not `npm run serve`. The progression at
`:55`–`:57` never mentions it. The completion conditions at `:61`–`:64` never mention it.

I verified this by grepping the whole regenerated bundle, with a positive control on the
same needle in the same call. `npm run serve` survives in exactly two places, neither of
them a lesson:

- `lessons/01-canvas-and-context/starter/README.md:10` — "`npm run serve` rebuilds, watches
  source files and serves the repository."
- `lessons/01-canvas-and-context/starter/package.json:8` — the script itself.

In the catalogue version the step was **required and verified**:
`00-project-setup/LESSON.md:43` "start the development server" and `:47` "`npm run serve`
exposes the page on its reported local URL, the page shows the starter heading, and the
console has no error."

**The mitigating fact, stated plainly so you can argue the −3 down if you want to.** The
tutor is instructed at `:42` to read `starter/README.md` before presenting any task, and
that README documents the command. So a tutor who follows the instruction will *discover*
the serve command. The step has degraded from required-and-verified to discoverable.

**Why I charged it anyway.** Every lesson from 01 onward declares the `browser-check`
validator, and lesson 01's own completion condition at `:62`–`:63` requires that "The canvas
clears to the chosen colour, remains sharp after resize". A learner cannot satisfy any of
that without a served page, and `DESIGN.md:7` states the project is served over a local HTTP
origin because "later asset requests cannot reliably use `file://`". The course now depends
on a step it never instructs and never checks. That is the shape the −3 row exists to name.

**Coverage topics: 0 unserved of 56.** The coverage list at `COURSE.md:72`–`:127` is
unchanged from the catalogue version, and no topic was served by the deleted lesson 00 —
lesson 00 served **none** of the 56. Its content lay entirely outside the boundary the
course declares for itself, which is the strongest argument in favour of folding it in.

**`DESIGN.md` anchors: 0 unserved of 16.** Unchanged, including `#unresolved-decisions`;
`#platform-toolchain` is still referenced, by the new `01-canvas-and-context`.

**Arithmetic check:** 1 gap listed, 1 × −3 = 3 subtracted in section 1. Agreed.

## 4. The toil inventory

**Confirmed toil — 1 site, −2 total.**

1. `lessons/13-load-gltf-model/LESSON.md:40` — identical to audit 1, item 2, byte for byte.

   > Before starting, copy every file under `model/` to a repository-root `models/`
   > directory: `Duck.glb`, `LICENSE.md`, `SCEA.txt` and `ATTRIBUTION.md`.

**Script candidates examined and rejected — none.** `audit.py` returned exactly one
candidate for this bundle, and it is the confirmed site. The `install` candidate from
audit 1 is gone because the sentence that carried it is gone. All 18 lesson files were
opened and read.

**Not toil under the rubric, but still an authored file copy:**
`lessons/01-canvas-and-context/LESSON.md:42`–`:46`, assigned to the tutor. The scanner did
not flag it. I checked why: the sentence begins "Before presenting any learner task, the
tutor MUST read `starter/README.md`; copy `starter/package.json`…" — `copy` sits after a
semicolon and a space, which is not one of the `_LEAD` alternatives (line start, bullet,
after `.␣`, after `,␣`, after `must`/`should`/`then`). See section 8, finding T2: the
scanner cannot see a copy instruction that has been moved from the learner to the tutor,
which is now a known way to write one.

## 5. Which version is the better course

**On the rubric, they are a tie that the rubric cannot break: 194 against 193.** One point
apart across nineteen and eighteen lessons. Taking that difference seriously would be
over-reading a method whose granularity is coarser than a point. **Report the numbers, and
report that they do not decide it.**

Here is what each change actually bought and cost, in rubric terms:

| Change | Effect on the score | Effect on the course |
|---|---:|---|
| Lesson 00 deleted, folded into 01 | **+2** (the toil span goes) | **Better.** Lesson 00 served none of the 56 declared coverage topics and scored −2, the worst figure in either course. Folding it in is exactly what the rubric's "much smaller lesson" row recommends. |
| Lesson 01 declares scaffolding tutor work | 0 | **Better, in intent.** `:11` "Repository scaffolding is tutor setup, not part of the learner's task" and `:46` "This bootstrap is tutor work" state the principle the whole `supplies:` change exists to enforce. |
| `npm run serve` dropped from every lesson | **−3** | **Worse.** A required, verified step became a line in a supplied README. |
| `ownership_policy` → `unrestricted` | **0** | **Worse, and this is the one that matters.** See below. |
| Lesson 13's copy instruction | unchanged, −2 in both | Neither. |

### The ownership change is the finding, and the rubric scored it zero

`tutorial.yaml:35` went from `tutor-must-not-edit-learner-owned` to `unrestricted`, across
the whole course, to buy the tutor permission to place five files once, before lesson 01.
`learner_owned` (`tutorial.yaml:34`) still lists `index.html, package.json,
package-lock.json, tsconfig.json, src/**, dist/**, models/**` — that is, every file the
learner writes for the next eighteen lessons. The policy that kept the tutor out of them is
gone.

The regenerated `COURSE.md:27`–`:29` notices this and tries to patch it in prose:

> Although the manifest permits the initial workspace writes, the tutor must not edit
> learner implementation files again unless explicitly asked.

**A machine-readable invariant was replaced by a sentence in a teaching-philosophy
paragraph.** The guarantee now holds only for as long as every tutor reads and honours that
sentence, for eighteen lessons, including the ones where the learner is stuck and the tutor
is tempted. That is a categorically weaker thing than what it replaced, it was paid for a
one-time five-file copy, and **the rubric charged nothing for it**, because it has no row
that can see a manifest.

`supplies:` exists precisely to avoid this trade. It places the files without assigning
them to anyone and without touching `ownership_policy`.

### Verdict

**Neither version is the better course as it stands. The regenerated one has the better
lesson structure and the worse manifest.**

- The regenerated version is **right about lesson 00**. Delete it, fold setup into lesson
  01, say out loud that scaffolding is tutor setup. Keep all of that.
- The regenerated version is **wrong about how it paid for it**. Do not adopt
  `ownership_policy: unrestricted`. The correct instrument is a manifest-level `supplies:`
  declaration — proposal P1 in audit 1, retargeted at `lessons/01-canvas-and-context/starter/`
  — which places the same five files with `ownership_policy` left at
  `tutor-must-not-edit-learner-owned`.
- The regenerated version **dropped a step it still depends on**. Restore `npm run serve`
  to the tutor bootstrap at `:45` and to the completion conditions at `:61`, or delete
  "static serving" from objective `:23`. The first is better: the course needs a served
  page from lesson 01 to the end.

**What to adopt:** the regenerated lesson structure, with `ownership_policy` restored, the
five-file copy in `:42`–`:46` replaced by a `supplies:` declaration, and `npm run serve`
put back. That course would score 196 with no goal gap and no toil in lesson 01, and it
would keep the ownership guarantee. Neither version in front of you is that course, and the
numbers alone would never have told you so.

## 6. The questions only a reader can answer

**Row A — a `design_refs` entry that does not answer the question its lesson raises.**
**One found, unchanged from audit 1:** `lessons/06-depth-and-culling.md:4` — neither
`#api-boundary` nor `#matrix-convention` states a front-face winding convention. See audit
1, section 6, row A, for the full reasoning. The rewritten lesson 01 keeps
`design_refs: [platform-toolchain, api-boundary]`, and `#platform-toolchain`
(`DESIGN.md:3`) does now have more work to do — it is the only anchor behind the tutor
bootstrap — but it answers what it is asked: npm, esbuild, `tsc --noEmit`, no framework.
Not a hit.

**Row B — a lesson that introduces a type or concept nothing later uses.** **None found.**
Same two cleared near-misses as audit 1 (`03-vertex-data.md:21` per-vertex colour,
`08-textures.md:42` mipmap policy). Folding lesson 00 in removed the one place where the
question was arguable, since lesson 00's tooling concepts are now stated as supporting the
graphics loop rather than as objectives in their own right
(`01-canvas-and-context/LESSON.md:31`–`:33`).

**Row C — a lesson far outside the course's usual size.** **One found.**
`17-depth-reconstruction-and-ssr.md` at 21 points and 14 elements, exactly as in audit 1;
the same split at the reconstruction/marching seam applies. The small-direction outlier is
**gone** — that was lesson 00, and folding it in is what the row recommends. The new lesson
01 at 9 points sits inside the normal band.

**The completability invariant.**

> Can a learner who declines every offer still finish this course?

**Not applicable — no optional lessons are declared in `tutorial.yaml`.** Keyed off the
absence of an `optional_lessons:` key, not off a count. Lesson 14 carries the same
prose-versus-manifest mismatch as the catalogue version and the same substantive answer:
yes, it is skippable, and `15-render-to-texture.md:15` says so. Proposal P4 applies here
unchanged.

---

# AUDIT 3 — `durable-event-broker`

The first real bundle using `optional_lessons`, and therefore the first time the
completability invariant is asked.

## 1. The course and its total

- **Bundle id:** `durable-event-broker`
- **Title:** Build a Durable Event Broker in Go
- **Lessons:** 15 on the main path, **3 optional** (`tutorial.yaml:29`–`:49`)
- **`supplies:` entries declared:** none
- **`required_for` gates on optional lessons:** **none** — see section 6

```
sum of the 15 main-path lessons                              170
sum of the 3 optional lessons                                 41
                                                            ----
sum of all 18 lessons                                        211
unserved coverage topics            0 x -3                  -  0
unserved DESIGN.md anchors          0 x -3                  -  0
required_for gates                  0 x -3                  -  0
                                                            ----
TOTAL                                                        211
```

The skill notes that the lesson rows cover main-path and optional lessons together while
`lesson_count` counts the main path only — 15 and 3 above a table of 18 rows, and the script
dropped nothing. **Both figures matter here**: 211 is what the rubric reports, and **170 is
what a learner who declines every offer receives.** Section 6 is where that gap is argued.

## 2. The per-lesson table

| Lesson | Score | Objectives served | Toil found |
|---|---:|---|---|
| `00-running-broker` | 9 | 3 of 3 | — |
| `01-offsets-and-replay` | 12 | 4 of 4 | — |
| `02-record-framing` | 12 | 4 of 4 | — |
| `03-recovery` | 10 | 4 of 4 | — |
| `04-durability-contract` | 11 | 4 of 4 | — |
| `05-partition-ownership` | 13 | 4 of 4 | — |
| `06-group-commit` | 10 | 4 of 4 | — |
| `07-segments` | 12 | 4 of 4 | — |
| `08-sparse-indexes` | 12 | 4 of 4 | — |
| `09-retention` | 11 | 4 of 4 | — |
| `10-topics-and-partitions` | 12 | 4 of 4 | — |
| `11-http-api` | 12 | 4 of 4 | — |
| `12-long-polling-and-overload` | 10 | 4 of 4 | — |
| `13-observability-and-load` | 10 | 4 of 4 | — |
| `14-asynchronous-follower` | 14 | 5 of 5 | — (2 candidates, both rejected) |
| **main-path subtotal** | **170** | | |
| `property-based-framing` *(optional)* | 15 | 4 of 4 | — |
| `tcp-transport` *(optional)* | 14 | 4 of 4 | — |
| `page-cache-experiments` *(optional)* | 12 | 4 of 4 | — |
| **Sum of all 18** | **211** | | **0 sites** |

### Element breakdown

**`00-running-broker` = 9.** `:53` "Create the module and a minimal broker executable" +1.
`:53` "Add a directly testable record and log implementation" +2. `:54` "Append several
opaque records, fetch them, and verify insertion order and copying behaviour" +2 — the
slice-aliasing point at `:32`–`:33` is the lesson's real content. `:55` "Keep the executable
on the same path by making it exercise the API" +1. `:49` "Do not add interfaces with only
one implementation unless a present test boundary needs one" +2. `:63` "No declared
production function or type is disconnected from the running path" +1. `:59` validators 0.

**`01-offsets-and-replay` = 12.** `:48` "Add broker-assigned metadata to stored records"
+1. `:48` "Extend append to return the assigned offset" +2. `:49` "then implement bounded
fetch" +2. `:49` "Test boundary cases before changing the executable" +2. `:50` "demonstrate
two independent replay positions" +2. `:41` "The first appended record uses a documented
initial offset" +1. `:44` "Do not expose slice indexes as the public offset contract" +2.

**`02-record-framing` = 12.** `:50` "Write the format down, including byte order and
checksum range" +2. `:50` "Implement encoding" +2. `:50` "then decoding with explicit
errors" +2. `:51` "Test empty keys and payloads, binary zero bytes, maximum accepted sizes,
truncation at several boundaries, version mismatch, and corruption" +2. `:43` "Define a
maximum frame size and reject larger declarations before allocation" +2. `:45` "Encoding
the same record produces the same bytes" +1. `:59` "The concrete frame decision is recorded
under `#record-framing` in the learner design" +1.

**`03-recovery` = 10.** `:50` "Open or create the log, append encoded frames" +2. `:50` "and
rebuild in-memory metadata on reopen" +2. `:51` "Create deterministic tests that cut a valid
file at several tail positions" +2. `:52` "and another that corrupts an interior frame" +2 —
the tail/interior distinction at `:28`–`:29` is the lesson. `:52` "Add a manual kill/restart
experiment after the tests" +1. `:59` "File descriptors close on success and error paths"
+1.

**`04-durability-contract` = 11.** `:49` "Instrument the existing append path, establish its
current acknowledgement point" +2. `:50` "then move the point behind explicit
synchronisation" +2. `:50` "Measure a repeatable sequence of durable appends and capture
latency and throughput" +2. `:51` "Discuss why different environments may produce different
numbers without invalidating the contract" +2. `:43` "Sync failures are returned to the
caller" +1. `:59` "The acknowledgement contract is written precisely and does not claim
replication" +2.

**`05-partition-ownership` = 13** — the highest main-path figure. `:52` "Identify all mutable
append state" +2. `:52` "then wrap append submissions in request values carrying a private
result path" +2. `:53` "Start and stop the owner explicitly" +2. `:53` "Add concurrent tests
for offset uniqueness and ordering" +1. `:54` "followed by cancellation and shutdown cases
under the race detector" +2. `:47` "One component owns channel closure; callers never close
the shared request channel" +2. `:63` "The learner can state the ownership invariant and why
a channel serves it" +2.

**`06-group-commit` = 10.** `:50` "Measure the existing owner" 0. `:50` "add a size-only
batch" +2. `:50` "then add a time bound so sparse traffic does not wait forever" +2. `:51`
"Test threshold edges, storage failures, cancellation, and shutdown" +2. `:52` "Repeat the
earlier workload and compare distributions rather than quoting one best run" +2. `:46`
"Empty timers or busy loops must not consume CPU while idle" +1. `:57` "A sync spy or
equivalent evidence proves one sync may cover several acknowledgements" +1.

**`07-segments` = 12.** `:49` "Introduce a segment type around the existing single-file
mechanics" +1. `:49` "then make a partition manage an ordered collection" +2. `:50` "Add
rollover with tiny deterministic limits" +2. `:50` "reopen tests" +1. `:51` "and
invalid-directory-layout tests" +2. `:42` "Existing closed segments are never reopened for
append" +2. `:44` "A batch is not split in a way that violates its durability
acknowledgement" +2 — a genuinely subtle constraint reaching back to lesson 06.

**`08-sparse-indexes` = 12.** `:49` "Measure or count frames scanned by the existing fetch"
+1. `:49` "Add periodic index entries" +2. `:49` "floor lookup" +2. `:50` "and forward scan"
+1. `:50` "Test exact hits, between-entry lookups, boundaries, missing indexes, and
corruption" +2. `:51` "Compare scan work at more than one interval" +2. `:45` "Index updates
must respect the append durability ordering documented by the learner" +2.

**`09-retention` = 11.** `:49` "Expose earliest available offset" +2. `:49` "implement size
retention" +2. `:49` "then age retention with a deterministic clock" +2. `:50` "Test
all-history-fits, several deletions, active-only history, restart, and fetches below, at,
and above the retained boundary" +2. `:41` "Never delete the active segment" +1. `:43` "Size
policy removes oldest eligible segments first" +1. `:45` "Index files are removed
consistently with their segments" +1.

**`10-topics-and-partitions` = 12.** `:51` "Wrap the existing partition behind broker
lookup" +2. `:51` "create a topic with a fixed count, and address appends explicitly first"
+1. `:52` "Add keyed selection" +2. `:52` "and then a documented unkeyed strategy" +2. `:53`
"Exercise independent owners under the race detector and restart the whole broker" +1. `:44`
"Topic and partition names are validated before they become filesystem paths" +2. `:46`
"Tests must not assert a global order across partitions" +2 — the conceptual heart of the
lesson lives in a constraint rather than in the progression.

**`11-http-api` = 12.** `:52` "Define the smallest external contract" +2. `:52` "implement
single append and bounded fetch" +1. `:53` "then batch append and metadata" +1. `:53` "Add
handler tests for success, malformed input, excessive bodies, unknown resources, expired
offsets, cancellation, and storage errors" +2. `:54` "Exercise the server with small
producer and consumer commands that use the HTTP API" +1. `:46` "Fetch can carry arbitrary
key and payload bytes safely" +2. `:47` "Storage packages do not import HTTP packages" +2.
`:44` "Request bodies have explicit limits" +1.

**`12-long-polling-and-overload` = 10.** `:51` "Add a wait-capable internal fetch operation"
+2. `:51` "then expose it through HTTP" +1. `:51` "Test data already present,
append-after-wait, timeout, client cancellation, shutdown, and several waiters" +2. `:53`
"Saturate a deliberately tiny append queue and confirm overload behaviour under the race
detector" +2. `:45` "Notification cannot be lost in a way that leaves available data waiting
indefinitely" +2 — the lost-wakeup problem, and the hardest idea in the lesson. `:47` "Slow
or disconnected clients do not create unbounded goroutines" +1.

**`13-observability-and-load` = 10.** `:51` "Add measurements around queueing, batching,
write, sync, fetch, segments, retention, and errors" +2. `:52` "Build a load command with
fixed-duration and fixed-count modes" +2. `:52` "then add a JSON log producer representing
several fictional services" +1. `:53` "Run below saturation, near saturation, and above
capacity" +1. `:54` "explain the change in metrics and errors" +2. `:43` "Instrumentation
must not parse application payloads" +1. `:46` "Results include environment and
configuration; they are not universal benchmarks" +1.

**`14-asynchronous-follower` = 14** — the highest main-path figure with lesson 05, and the
course's closing argument. `:54` "Reuse the internal fetch and append mechanics through a
replication-specific boundary that can preserve assigned metadata" +2. `:55` "Copy existing
history, follow new records" +2. `:55` "interrupt and restart the follower" +2. `:56` "and
expose lag" +1. `:56` "Finally delay replication, acknowledge new leader records, terminate
the leader, and inspect which records the follower lacks" +2 — a fault experiment whose
whole purpose is to make a wrong belief fail visibly. `:48` "The follower never accepts
producer traffic or promotes itself" +1. `:50` "The final documentation states that
acknowledged records may be absent from the follower" +2. `:66` "The learner explains why
this system has neither quorum durability nor safe failover" +2.

**`property-based-framing` *(optional)* = 15** — the largest figure in the course. `:56`
"State the properties in plain language" +2. `:56` "add the valid-record round trip" +2.
`:57` "then exercise the decoder with arbitrary and truncated bytes" +2. `:57` "Inspect any
reduced counterexample" +2. `:58` "repair the codec" +2. `:58` "and retain a deterministic
regression case before continuing generation" +2. `:47` "The learner chooses Go's built-in
fuzzing or a maintained property-testing library after comparing what the required
properties need" +2. `:50` "Arbitrary-byte decoding has a finite test resource budget" +1.

**`tcp-transport` *(optional)* = 14.** `:54` "Define a minimal append and fetch envelope"
+2. `:54` "implement exact framed I/O" +2. `:54` "and test using a connection that
deliberately fragments and combines writes" +2. `:55` "Add request identifiers if more than
one outstanding request is supported" +2. `:56` "Propagate disconnect and deadlines" +1.
`:57` "then exercise concurrent connections and shutdown under the race detector" +1. `:46`
"All broker actions call the same internal operations as HTTP" +2. `:48` "One malformed
connection cannot crash the broker" +1. `:49` "Connection and request concurrency are
bounded" +1.

**`page-cache-experiments` *(optional)* = 12.** `:52` "Diagram the layers a record crosses"
+2. `:52` "measure append and sync separately" +2. `:53` "and inspect the system calls on a
supported platform" +1. `:53` "Compare ordinary process termination and abrupt process kill"
+2. `:54` "then state what neither experiment can prove about sudden machine power loss" +2
— the best single element in the course, and worth noting that it teaches the limits of a
measurement rather than the measurement. `:47` "Results include operating system, filesystem
when known, storage context, and limitations" +1. `:61` "The written conclusion separates
observation, inference, and untested failure boundaries" +2.

## 3. Goal gaps

**Coverage topics: 0 unserved of 26 — with a serious caveat the rubric cannot express.**

All 26 topics from `COURSE.md:88`–`:114` are exercised by an element somewhere in the
bundle. But **three of them are exercised only inside optional lessons**:

| Topic | `COURSE.md` | Served only by |
|---|---|---|
| property-based record-framing tests | `:111` | `lessons/property-based-framing.md` *(optional)* |
| length-prefixed TCP protocols | `:112` | `lessons/tcp-transport.md` *(optional)* |
| operating-system page-cache behaviour | `:113` | `lessons/page-cache-experiments.md` *(optional)* — partially; see below |

The third is the mildest: `04-durability-contract.md:33` lists "Page cache" under Concepts
to teach and `:26`–`:27` explains that "Operating systems normally buffer writes", so the
main path does name the mechanism. The optional lesson deepens it into measurement. I count
it served on the main path, weakly. The first two are not served on the main path at all.
`02-record-framing.md:51` asks for hand-written truncation and corruption cases, which is
explicitly the thing property-based testing is contrasted against
(`property-based-framing.md:27`, "Example tests check cases the author selected");
`02-record-framing` builds a length-delimited *frame*, not a TCP *protocol*, and
`11-http-api.md:48` says "Do not add long polling until the next lesson" with no TCP on the
main path anywhere.

**This contradicts the course's own completability claim.** `COURSE.md:77` says:

> The course remains complete when every optional offer is declined.

and the coverage list is headed (`COURSE.md:87`) "Topics this course must cover". Both
cannot be true. A learner who declines every offer finishes the course and does not meet
three topics the course says it must cover.

**I did not charge −3 for these**, because the rubric's row is "a stated objective or
`DESIGN.md` anchor that **no task exercises**", and a task does exercise all three. Charging
would have been inventing a rule mid-audit. **Under the rubric as written, the total is
211.** If the row proposed in section 8 (finding T7) existed, two of these would charge −3
each and the total would be **205**. That second figure is *not* this report's score; it is
there so you can see what the missing row would cost.

**`DESIGN.md` anchors: 0 unserved of 15.** All fifteen — `acknowledgement-contract`,
`backpressure-contract`, `group-commit`, `observability-contract`, `offset-semantics`,
`partition-ownership`, `record-framing`, `record-model`, `recovery-policy`,
`replication-boundary`, `retention-semantics`, `segment-layout`, `sparse-index-contract`,
`topic-partition-model`, `transport-boundary` — appear in at least one lesson's
`design_refs`, and in every case the lesson exercises what the anchor describes. I checked
the set difference in both directions: no anchor is unreferenced, and no `design_refs` entry
names an anchor that does not exist. This is the tidiest anchor set of the three bundles.

**Lesson-level objectives: 0 unserved.** All 72 across the 18 lessons are exercised by an
element of their own lesson.

**Arithmetic check:** 0 gaps listed, 0 × −3 = 0 subtracted in section 1. Agreed.

## 4. The toil inventory

**Confirmed toil — none. Zero sites in eighteen lessons.**

That is a real finding and not an absence of evidence: all 18 lesson files were opened and
read in full, and the course hands the learner no files at all. Its `workspace_kind` is
`new-repository` and `00-running-broker.md:45` says "Begin from a fresh repository" — the
learner types `go mod init` and everything after it. There is nothing for `supplies:` to
declare. **No `supplies:` proposal applies to this bundle.**

**Script candidates examined and rejected — 2, both in the same lesson.**

1. `lessons/14-asynchronous-follower.md:30` `[copy]` — the candidate line is
   "copy is neither a quorum nor a failover protocol. Without authority and election rules,"
   The actual sentence, from `:29`–`:31`, is:

   > It can create another copy, but the leader acknowledges without waiting for it.
   > Therefore the copy is neither a quorum nor a failover protocol.

   Here "copy" is a **noun**, mid-sentence, in the middle of a Theory paragraph. It arrived
   at the start of a physical line only because the paragraph is hard-wrapped. **False
   positive**, and an instructive one — see section 8, finding T1.

2. `lessons/14-asynchronous-follower.md:55` `[copy]` — the candidate line is
   "can preserve assigned metadata. Copy existing history, follow new records, interrupt and"
   The sentence, from `:54`–`:57`, is:

   > Reuse the internal fetch and append mechanics through a replication-specific boundary
   > that can preserve assigned metadata. Copy existing history, follow new records,
   > interrupt and restart the follower, and expose lag.

   This *is* an imperative and the pattern is right to fire on it. It is not toil: "Copy
   existing history" means *implement replication catch-up*, which is the lesson's entire
   subject and objective 1 at `:20`. Scored +2, not −2. **True imperative, wrong semantics.**

**The scanner is a candidate generator, and this inventory came from the lessons.** Its two
candidates for this bundle produced zero findings. Had I trusted the scan in either
direction — treating its hits as toil, or its silence elsewhere as cleanliness — the result
would have been wrong both times.

## 5. Proposals

**P5 — reconcile `COURSE.md:77` with the coverage list.** The course states both "The
course remains complete when every optional offer is declined" (`:77`) and that its
must-cover topics include three things only optional lessons teach (`:111`–`:113`). Pick
one; the rubric cannot pick for you, and both are defensible:

- **(a) Move the three topics out of "Topics this course must cover" into a new section —
  "Topics the optional lessons cover".** Smallest change, honest, and it makes the
  completability claim at `:77` true as written. This is the one I would take.
- **(b) Bring the material onto the main path.** Expensive, and it argues against the
  design: `11-http-api.md:10`–`:12` deliberately chose HTTP "to keep the main path focused
  on broker behaviour rather than application protocol framing", and TCP framing is exactly
  the distraction that sentence names. Not recommended for `tcp-transport`. Arguable for
  `property-based-framing`, since `02-record-framing.md:44` already *requires* that "The
  decoder must never panic on arbitrary input" on the main path, and the optional lesson is
  the only place that property is tested rather than asserted.
- **(c) Do nothing and record the decision.** Acceptable, if `:77` is reworded so it claims
  completability rather than coverage.

**P6 — a question, not a proposal: should `property-based-framing` carry a
`required_for`?** It does not have one today, and section 6 rules that correct. Raising it
only because the course itself points at the tension: `02-record-framing.md:44` makes
"The decoder must never panic on arbitrary input" a **main-path constraint**, and `:58`
makes "No malformed input causes a panic or unbounded allocation" a **main-path completion
condition** — yet the only place that property is genuinely *exercised* is the optional
lesson. The main path asserts it from hand-written cases (`:51`). That is a deliberate and
defensible line, and the `anticipates` / `repair_in` wiring at `tutorial.yaml:36`–`:37` is
the right mechanism for it: the offer becomes a repair when the failure is actually
observed, rather than a gate before it is. **Do not add a `required_for` to improve
anything.** The question is only whether you are content that a main-path completion
condition is checked by examples the author chose.

**No lesson in this course scores at or below zero, so no "what is this lesson for"
question applies.** The lowest figure is 9 (`00-running-broker`), and its elements are in
section 2.

## 6. The questions only a reader can answer

**Row A — a `design_refs` entry that does not answer the question its lesson raises.**
**One found.**

`lessons/00-running-broker.md:4` declares `design_refs: [record-model]`, a single anchor.
The lesson raises three objectives (`:21`–`:23`):

- "Create a small Go module and executable without speculative package structure."
- "Represent an optional key and opaque payload without treating them as text or JSON."
- "Separate the executable entry point from a directly testable in-process broker API."

`#record-model` (`DESIGN.md`, "A record contains an optional opaque key and an opaque byte
payload…") answers the **middle** one, precisely and well. It says nothing about module or
package structure, and nothing about the entry-point/API separation — and **no other anchor
in the bundle does either.** The lesson leans hard on this: `:31`–`:33` "Introduce Go
packages only when both executable and tests need the code", `:49` "Do not add interfaces
with only one implementation…", `:63` "No declared production function or type is
disconnected from the running path". That is a real, opinionated, repeated design position
with no anchor behind it, so nothing later can cite it and the learner instance has nowhere
to record it.

A question, not a proposal: **should the bundle carry a `#project-layout` anchor?** Or is
package structure deliberately a learner decision, in which case the lesson's three
constraints on it are doing an anchor's job in a place nothing can reference?

*Considered and rejected:* `lessons/13-observability-and-load.md:4` → `#observability-contract`.
The lesson raises "Interpret latency distributions, queue depth, batch size, and sync time
together" (`:22`) and "Coordinated omission awareness" (`:35`), and the anchor lists which
measurements exist without saying how to read them. But an anchor's job is the contract,
not the interpretation, and it does answer what it is asked — including "replica lag",
which is what `14-asynchronous-follower.md:4` cites it for. Not a hit.

**Row B — a lesson that introduces a type or concept nothing later uses.** **None found.**
The closest call: `13-observability-and-load.md:52`, "then add a JSON log producer
representing several fictional services". Nothing in `14-asynchronous-follower` uses the
JSON workload again, so it is terminal. It is not attention bought for nothing —
`COURSE.md:12`–`:14` sets it up deliberately ("The project uses JSON application logs as one
visible workload, but JSON is not part of the broker's record model"), the coverage list
names "broker metrics and load testing" (`:107`), and the lesson's own point at `:28`–`:30`
is that the workload stays opaque to the broker. The concept it introduces is *that the
payload stays opaque under a realistic workload*, and demonstrating it once is the whole
demonstration. Cleared.

**Row C — a lesson far outside the course's usual size.** **None found**, and this is
worth saying positively: the main path runs from **9 to 14** points with a median of **12**,
across files of 66 to 73 lines, with four learning objectives in thirteen of the fifteen
(three in `00-running-broker`, five in `14-asynchronous-follower`). It is the most uniform of the three courses audited by a wide margin — compare
webgl's 21-point outlier against an 11-point median. The largest figure in the bundle is an
**optional** lesson, `property-based-framing` at 15, which is notable but not a defect: an
optional lesson that is substantial is doing its job, and the course offers it as a detour
rather than a footnote.

**The completability invariant, asked out loud.**

> **Can a learner who declines every offer still finish this course?**

**Yes — the course is completable. But it is not fully covered, and the course says
otherwise about itself.**

I answered this from the main-path lessons, checking both halves of the rubric's test.

*Does any main-path completion condition depend on something only an optional lesson builds
or explains?* **No.** I walked all fifteen main-path completion blocks. The one that comes
closest is `03-recovery.md:15`, whose prerequisite is "Complete `02-record-framing` **with a
bounded defensive decoder**" — and that decoder is a main-path deliverable of lesson 02
itself (`02-record-framing.md:44` "The decoder must never panic on arbitrary input", `:58`
"No malformed input causes a panic or unbounded allocation"), not something
`property-based-framing` supplies. The optional lesson *strengthens the evidence* for a
property the main path already requires. That is the correct relationship, and it is what
`anticipates` plus `repair_in` are for.

*Does any main-path lesson's prose assume the learner took an offer?* **No.** All three
references to optional lessons sit under `## Optional deeper paths` and are explicitly
conditional:

- `02-record-framing.md:69` — "The authored optional lesson `property-based-framing`
  exercises the decoder beyond hand-written cases **when the learner accepts it**."
- `04-durability-contract.md:69` — "The authored optional lesson `page-cache-experiments`
  explores the operating-system boundary further **when the learner accepts it**."
- `11-http-api.md:72` — "The authored optional lesson `tcp-transport` adds a framed TCP
  protocol against the same internal operations **when the learner accepts it**."

Three offers, three conditional mentions, zero assumptions. Structurally this course gets
the invariant right, and it is a good first example of the feature.

**The caveat, restated because it is the finding.** Completable is not covered. The
declining learner finishes the course with **170** of the 211 points and misses three of the
26 topics under a heading that reads "Topics this course must cover" (`COURSE.md:87`), while
`COURSE.md:77` tells them "The course remains complete when every optional offer is
declined." Both sentences are in the same file, eleven lines apart, and they disagree.
Proposal P5 reconciles them.

**`required_for` gates: none — checked in the manifest, not in the script's output.**
The skill is explicit that `required_for`, `anticipates` and `repair_in` are absent from
`audit.py`'s output and must be read from `tutorial.yaml` directly, keyed off the presence
of an `optional_lessons:` key rather than off a count. I did that. `tutorial.yaml:29`–`:49`
declares three optional lessons:

| Optional lesson | `offer_at` | `anticipates` | `repair_in` | `required_for` |
|---|---|---|---|---|
| `property-based-framing` | `02-record-framing` | `frame-decoder-breaks-on-arbitrary-input` | `02-record-framing` | **none** |
| `tcp-transport` | `11-http-api` | — | — | **none** |
| `page-cache-experiments` | `04-durability-contract` | — | — | **none** |

**Zero gates, so 0 × −3 = 0**, and the rubric's warning about deleting a justified gate has
nothing to attach to here. Recording it anyway so the next auditor does not have to
re-derive it, and because the warning is the thing that stops a later reader from "improving"
a score by removing a gate:

> This gate cost the course 3 points and may still be correct. If the lesson genuinely
> cannot be completed while its failure stands, the gate is doing its job — say so and keep
> it. Do not delete a gate to improve a score. A course that drops a justified gate lets a
> learner finish a lesson whose failure is still standing, which is worse than the toil this
> rubric hunts.

The one place a gate could plausibly have gone is `property-based-framing`, which is the
only optional lesson with a `repair_in`. It does not have one. Proposal P6 explains why
that is right and asks the one question it leaves open.

**Dynamic evidence.** No dry-run harness has walked any of these three courses, so this
report cites no stall as evidence. The rubric's warning applies in the other direction too
and is worth stating: if a dry run later finishes all three, that will mean nothing got
stuck, not that they teach.

---

# 7. The validator is not the question

Stated plainly, as the skill requires. This report says nothing about whether any of these
three bundles is structurally valid, and a green validator would not have changed a single
figure above. The `−2` at `00-project-setup/LESSON.md:34` is a perfectly well-formed
sentence in a perfectly well-formed lesson in a bundle that presumably validates. The
`ownership_policy: unrestricted` line in the regenerated candidate is a legal value of a
legal key. The contradiction between `COURSE.md:77` and `COURSE.md:87` in
`durable-event-broker` is two valid Markdown paragraphs. Structural validity and teaching
quality are different questions, which is why the two skills live apart.

---

# 8. What this run revealed about the tooling

The plan says findings about this work are more valuable than findings about the courses.
Here they are, unsoftened. Seven findings: two about the scanner, five about the rubric and
the skill.

## T1 — the toil scanner's imperative heuristic is evaluated on physical lines, and hard wrapping puts nouns in imperative position

`scan_toil` iterates `text.splitlines()` and `_LEAD` includes `^` as its first alternative.
Lesson prose in this corpus is hard-wrapped at roughly 95 columns with no regard for
sentence structure, so any paragraph can put an ordinary noun at the start of a line.

The live example is `durable-event-broker/lessons/14-asynchronous-follower.md:30`:

```
It can create another copy, but the leader acknowledges without waiting for it. Therefore the
copy is neither a quorum nor a failover protocol. Without authority and election rules,
```

`copy` here is a noun with a definite article in front of it, on the previous line. The
scanner sees `^copy\b` and fires. This is not a tuning problem — it is structural. The
heuristic asks "is this verb in an imperative position?", and the answer depends on the
sentence, while the input is a line.

**It also produces a false *negative* of the same origin**, which is worse. The skill already
warns that `text` is one physical line, not one sentence, and that both real toil sites are
hard-wrapped mid-clause. The scanner has the same blindness the reader was warned about.

**Suggested fix, offered as a proposal:** join physical lines into paragraphs before
scanning, keep a line-number map, and report the `file:line` of the line where the *match*
falls. That removes this class of false positive and lets the reported `text` be the
sentence the report actually needs to quote, which is what the skill asks the reader to go
and reconstruct by hand today. It is a change to `audit.py`, not to the pattern list.

## T2 — the scanner cannot see a copy instruction that has been re-assigned to the tutor, which is now a known way to write one

`webgl-typescript-scene` (regenerated) `lessons/01-canvas-and-context/LESSON.md:42`–`:46`
contains a five-file copy instruction. The scanner produced **zero** candidates for it. Two
independent reasons:

1. the verb sits after `; ` (semicolon-space), which is not one of `_LEAD`'s alternatives;
2. even had it fired, the rubric would score it 0, because the work is assigned to the tutor.

The second is arguably correct as scoring. But the combined effect is that **the pattern
that started this whole change — "the lesson tells someone to copy five files" — is now
invisible to the tool, in a bundle where it is still present.** The regenerated course is a
demonstration that authored file copies can be relocated out of the scanner's reach without
being removed. If the toil scanner is meant to help authors find places where `supplies:`
should be used, it needs to fire on a copy instruction regardless of who is told to do it,
and let the reader decide.

**Suggested fix:** add `;\s` to `_LEAD`, and make the report distinguish *scored toil*
(assigned to the learner) from *undeclared supplied files* (assigned to anyone). They are
different findings with the same remedy.

## T3 — `topic_candidates` reads only four fields, and has no stemming, so "no candidate lesson found" fired on a topic taught by name

`durable-event-broker`'s audit output contains exactly one topic with no candidate:

```
- checksums: no candidate lesson found (a possible gap - read the course before concluding that)
```

`02-record-framing` teaches checksums explicitly: `:36` "Checksums and their limits" under
Concepts to teach, `:42` "The frame carries offset, append timestamp, optional key, opaque
payload, version, and **checksum**", `:57` "**Corrupt checksum**, unsupported version,
impossible length, and truncated frame are distinguishable", and `#record-framing` in
`DESIGN.md` names the checksum directly. It is about as taught as a topic can be.

I probed the live matcher to find out why, with a positive control in the same call:

```
topic 'checksums' -> {'checksums'}
overlap: set()
'checksum' in lesson tokens: True
```

**Two independent causes, both in `_lesson_tokens`:**

1. **No stemming.** The topic says `checksums`; the lesson's learning objective (`:20`) says
   `checksum coverage`. Singular and plural are different tokens.
2. **The token source is four fields only** — `title`, `slug`, `design_refs` and
   `## Learning objectives`. `## Concepts to teach`, `## Theory`, `## Constraints` and
   `## Completion conditions` are never read. `Checksums` appears in three of the four
   fields the matcher does not read.

The skill already says topic matches are word overlap and not coverage, and it is right. But
this is the one line of the output that reads as a *finding* rather than as a candidate —
"no candidate lesson found" invites the reader to look — and the one time it fired in this
corpus, it was wrong. A reader who took it at face value would have charged this course −3
for a topic taught by name in four places.

**Suggested fix:** widen the token source to the whole lesson body, or at minimum add
`## Concepts to teach`; and add naive plural folding (strip a trailing `s` before
comparison). Either alone would have fixed this case. Both together would make the
"no candidate" line worth the attention it asks for.

## T4 — the rubric's toil test catches `npm install`, and the rubric's remedy cannot touch it

The `−2` row reads: "deterministic and unambiguous; no decision; a mistake teaches nothing."
`webgl-typescript-scene/lessons/00-project-setup/LESSON.md:42` begins "Install
dependencies", which satisfies every clause of that test literally.

But every proposal this skill can make for toil is a `supplies:` entry, and **no `supplies:`
entry can create `node_modules`.** It is not a bundle artefact. The remedy does not reach
the finding.

I scored it `0` and said so at the element. That is a judgement I am confident about and a
rule the rubric does not contain, which means the next auditor may score it `−2` and the two
reports will not be comparable — the exact failure the rubric exists to prevent.

**Suggested fix:** make the toil row's test say what it means. Something like: *deterministic
and unambiguous; no decision; a mistake teaches nothing; **and the bundle could hand the
result over instead of assigning it.*** The last clause is the one that does the work, it is
implicit in the whole design of `supplies:`, and adding it costs nothing.

## T5 — the rubric has no row for a branch point, and no row for an element addressed to the tutor

Two gaps of the same shape, both hit in audit 1 and audit 2.

**A branch point.** `14-optional-minimal-gltf-loader/LESSON.md:48` says "Choose or skip the
path." The learner decides — so it is not `+1` or `0` — but the decision serves no learning
objective and a wrong answer teaches nothing about glTF, so it is not `+2` either. I scored
it `0` by elimination and said so. A different auditor could defensibly score it `+2`.

**A tutor-addressed element.** `00-project-setup/LESSON.md:38` ("Read `starter/README.md`
before giving the first task"), `11-secondary-demo-scene/LESSON.md:31`–`:34` (the whole
"the tutor MUST explicitly ask" block), and the entire bootstrap paragraph in the
regenerated `01-canvas-and-context/LESSON.md:42`–`:48` are instructions to the tutor, not
tasks for the learner. I excluded them from scoring and wrote the rule into section 0. The
rubric does not contain that rule, and lesson 11's tutor block is load-bearing teaching
content — it is what makes the learner's choice a real choice. Excluding it is defensible
and it is also throwing away signal.

**Suggested fix:** state both rules in the rubric, whichever way you decide them. The cost
of leaving them unstated is that two auditors produce two different numbers for the same
lesson and neither is wrong.

## T6 — "unserved anchor" has an obvious mechanical proxy, and the proxy is wrong

The tempting implementation of the `−3` anchor row is: *is this anchor named in some
lesson's `design_refs`?* It is one line of code and `audit.py` already emits both lists.

It would have been wrong on the first course audited. `webgl-typescript-scene`'s
`#unresolved-decisions` (`DESIGN.md:116`) appears in **no** `design_refs` entry and is
**served**, because its content is "these are learner decisions, record them under new
anchors at the lessons that need them" — and four lessons instruct exactly that
(`07-indexed-meshes-and-vaos.md:54`, `10-camera-and-scene.md:60`,
`11-secondary-demo-scene/LESSON.md:68`, `18-finish-the-scene.md:61`). The proxy would have
charged −3 and moved the course from 194 to 191 for a defect that does not exist.

The skill is already right about this in principle — it says the score comes from reading —
but it does not warn about *this* proxy by name, the way it warns at length about the toil
scanner and about `topic_candidates`. A meta-anchor is not an exotic construct; it is a
natural thing for an author to write.

**Suggested fix:** one sentence in the skill's "What the script does not give you" section:
an anchor absent from every `design_refs` list is a candidate, not a gap, and an anchor
whose content is "decide this later" is served by the lessons that decide it.

## T7 — the rubric has no row for a declared topic served only by an optional lesson, and `durable-event-broker` is the case

This is the finding the third audit exists to produce, and it is the most consequential one
here.

`durable-event-broker` declares 26 topics under "Topics this course must cover"
(`COURSE.md:87`), and three of them are reachable only by accepting an offer. The course
also states that "The course remains complete when every optional offer is declined"
(`COURSE.md:77`). Under the rubric as written, this scores **exactly the same** as a course
whose main path covers all 26 — because the `−3` row asks whether *a task* exercises the
topic, and a task does.

So the rubric is blind to the single most interesting thing about the first course to use
the feature it was extended for. The completability invariant caught it, because I asked the
question in section 6 — but the invariant is about *finishing*, and finishing is not the
problem here. The course is completable. It is under-covered for a declining learner, and
those are different failures.

**Suggested fix:** add a scored row.

> **a must-cover topic served only by an optional lesson** — `−3` each. The course declared
> the topic mandatory and then made it skippable. This is the coverage analogue of
> `required_for`, and like `required_for` it may be correct — say so and keep it — but the
> cost is visible either way.

Applied to `durable-event-broker` that is −6 (TCP protocols and property-based tests;
page-cache behaviour is named on the main path at `04-durability-contract.md:33`), taking
211 to **205**. I did **not** apply it in section 1 of audit 3, because inventing a rubric
row mid-audit is exactly the "argue a signal down to zero" failure the rubric warns about,
run in reverse. The number in audit 3 is 211 under the rubric you have.

## T8 — the score tracks how finely a lesson enumerates its own steps

Not a defect exactly, but a property you should know about before comparing two numbers.

A lesson's figure is the sum of its elements, and elements are clauses of `## Suggested
progression`. So a lesson that writes "Add the index, test it, and measure it" scores three
elements and a lesson that writes "Add and validate a sparse index" scores one, for the same
work. `17-depth-reconstruction-and-ssr.md` scores 21 partly because it teaches more and
partly because `:50`–`:54` is a single sentence with ten clauses in it.

The consequence: **within a course, the scores are comparable only to the extent that the
lessons are written in one voice.** Both of these bundles are, strikingly so — which is why
the median figures are so tight (webgl 11, broker 12) and why `17` stands out as genuinely
large rather than merely verbose. Across courses written by different hands, the comparison
would be much weaker than the rubric's "legible and comparable across a long course" claim
suggests.

Worth a sentence in the rubric, so a reader does not compare a 194 against a number from a
course with a different house style and think it means something.

---

# 9. Summary of proposals

| # | Course | Proposal | Kind |
|---|---|---|---|
| P1 | webgl (either version) | Five manifest-level `supplies:` entries for the starter files; delete `00-project-setup/LESSON.md:34`–`:36` | Toil span |
| P2 | webgl (either version) | Lesson-scoped `supplies:` entry for `model/`; delete `13-load-gltf-model/LESSON.md:40`–`:41`; **and** re-home learning objective 5 first | Toil span, conditional |
| P3 | webgl (catalogue) | What is `00-project-setup` for, once it scores 0? | Question (lesson ≤ 0) |
| P4 | webgl (either version) | Move lesson 14 from `lessons:` to `optional_lessons:` | Structural |
| P5 | broker | Reconcile `COURSE.md:77` with the coverage list at `:111`–`:113` | Coverage |
| P6 | broker | Are you content that a main-path completion condition is checked only by chosen examples? | Question |
| — | regenerated webgl | Adopt the lesson structure; restore `ownership_policy`; use `supplies:`; restore `npm run serve` | Verdict, audit 2 §5 |
| T1–T8 | the tooling | Eight findings against `audit.py`, the rubric and the skill | Section 8 |

Nothing above has been applied. Applying any of it is the `tutorail-authoring` skill's work,
after you say yes.
