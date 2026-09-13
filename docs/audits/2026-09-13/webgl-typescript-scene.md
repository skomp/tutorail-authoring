# Course quality audit: `webgl-typescript-scene`

Audited 2026-09-13 against `tutorail-authoring:course-quality` 0.3.0 and its
`references/rubric.md`. Read-only: nothing in
`/Users/robert/src/github.com/skomp/tutorail-bundles` was created, edited, staged or deleted.
`git status --porcelain` was empty at the start and at the end of the audit.

**Re-checked 2026-09-13 against the author's ruling "A project skeleton is toil"**, added to
`references/rubric.md` after this report was written. **No score changed**; one piece of reasoning
did. Section 4 shows the check element by element.

**This bundle is the rubric's own worked example, and it has changed since the rubric was
written.** The rubric describes lesson 14 as prose-optional while sitting in `lessons:`, and
publishes totals of 194 / 183 for that state. Commit `49af681` repaired it. Those two figures
describe a bundle that no longer exists and are **not** carried into this report. Every figure
below was derived from the files as they stand today.

**The validator's verdict is not an input to this report.** Structural validity and teaching
quality are different questions; "the bundle loads" is never an answer to anything here.

---

## The rubric, printed in full

### Scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises (course-level, counted once per gap) |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised |

### The two elements the rubric settles rather than leaving to the auditor

- **A branch point — where the lesson offers the learner a choice of paths — scores
  `evidence`, 0.** The teaching is in whichever branch the learner takes, scored on its own.
- **A tutor-addressed element scores `teaching`, +2, when the learner must decide or construct
  in response.** Score by what the learner does, at whatever grammatical person the author
  wrote it in.

### Rows a reader answers, and a script never scores

- a `design_refs` entry that does not answer the question its lesson raises;
- a lesson that introduces a type or concept nothing later uses;
- a lesson far outside the course's usual size, in either direction;
- a must-cover topic that only an optional lesson teaches — **a question, permanently, not a
  score.**

### The invariant no structural check can reach

> A course carrying optional lessons must be completable by a learner who declines every offer.

All of these are answered in section 6.

### My scoring protocol, stated so it can be argued with

The rubric's totals are comparable inside one course's house style, not between courses. This
course's house style is: `## Constraints` states rules, `## Suggested progression` enumerates
clauses, `## Completion conditions` enumerates conditions. I scored:

- every clause of `## Suggested progression`;
- every distinct clause of `## Completion conditions`;
- every clause of `## Constraints`, `## Theory` or `## Prerequisites` that assigns the learner
  something to do **and is not restated in the progression** (restatements are scored once, at
  the place the doing happens, so no instruction is counted twice);
- **not** `## On completion, persist` — those lines are the tutor writing `STATE.md`/`DESIGN.md`,
  not the learner doing anything. This follows the author's own precedent in `49af681`, which
  removed an objective precisely because its only service was a persist line;
- **not** `## Optional deeper paths` — explicitly beyond the required path;
- **not** bare prohibitions ("Do not introduce a framework") where no separate act is assigned.

One further ruling, applied throughout: **writing renderer code is never toil.** The toil row is
conjunctive — deterministic, no decision, a mistake teaches nothing, **and** the bundle could have
handed the result over. Renderer code fails the first three clauses: the learner decides and
constructs, and a wrong answer is instructive on screen. So it scores +2 or +1 on the teaching
row's own test, and the toil row is out before its last clause is reached.

Stated that way deliberately. An earlier draft of this report rested the same conclusion on "the
bundle cannot ship the renderer", and the author's ruling of 2026-09-13 shows why that ground is
unsafe: asked in its full form — *could the bundle have shipped one set of files for each language
the course supports?* — the shippability question would answer **yes, a bundle can ship TypeScript
source**. What excludes renderer code from the toil row is what the learner does with it, not the
format's reach. The figures are unchanged either way; the argument is now the one that survives the
ruling. Toil in this bundle is confined to moving files the bundle already contains.

---

## 1. The course and its total

| | |
|---|---|
| Bundle id | `webgl-typescript-scene` |
| Title | Learn WebGL 2 by Building a 3D Scene |
| Main-path lessons | 18 |
| Optional lessons | 1 (`lessons/minimal-gltf-loader/LESSON.md`) |
| Scored lesson rows | 19 |
| `supplies:` entries declared | 0 |
| Coverage list | present, 55 topics |
| `DESIGN.md` anchors | 16 |

### Arithmetic

Main-path lesson sum, in course order:

```
  -1  00-project-setup
+ 10  01-canvas-and-context
+ 14  02-first-shader-program
+ 13  03-vertex-data
+  9  04-uniforms-and-animation
+ 13  05-transforms-and-perspective
+ 11  06-depth-and-culling
+ 13  07-indexed-meshes-and-vaos
+ 15  08-textures
+ 10  09-normals-and-lighting
+ 15  10-camera-and-scene
+ 15  11-secondary-demo-scene
+ 18  12-scene-transition
+ 12  13-load-gltf-model
+ 15  15-render-to-texture
+ 17  16-bloom
+ 28  17-depth-reconstruction-and-ssr
+ 16  18-finish-the-scene
-------------------------------------
= 243  main-path lesson sum
```

Course-level penalties, each named:

```
  243  main-path lesson sum
-   0  unserved objectives      (0 gaps x -3)
-   0  unserved DESIGN.md anchors (0 gaps x -3)
-   0  required_for gates on optional lessons (0 gates x -3)
-------------------------------------
= 243  COURSE TOTAL, main path only
```

Adding the optional lesson's own figure:

```
  243  main path
+  17  minimal-gltf-loader (optional)
-------------------------------------
= 260  total across all 19 scored rows
```

**243 is the number that matters**, because it is what a learner who declines every offer
earns, and section 6 confirms that such a learner can finish the course. 260 is what a learner
who accepts the offer earns. Neither figure may be set beside another course's total.

Two toil spans cost this course 4 points and are recoverable in full (section 4). No course-level
penalty fired; the goal-gap inventory in section 3 is genuinely empty, and the arithmetic above
agrees with it: 0 gaps listed, 0 subtracted.

---

## 2. The per-lesson table

Mean main-path lesson: **13.5**.

| Lesson | Score | Objectives served | Toil found |
|---|---:|---|---|
| `lessons/00-project-setup/LESSON.md` | **−1** | 3 of 3 | **yes** — `:34` starter copy (−2) |
| `lessons/01-canvas-and-context.md` | 10 | 4 of 4 | none |
| `lessons/02-first-shader-program.md` | 14 | 4 of 4 | none |
| `lessons/03-vertex-data.md` | 13 | 4 of 4 | none |
| `lessons/04-uniforms-and-animation.md` | 9 | 4 of 4 | none |
| `lessons/05-transforms-and-perspective.md` | 13 | 4 of 4 | none |
| `lessons/06-depth-and-culling.md` | 11 | 4 of 4 | none |
| `lessons/07-indexed-meshes-and-vaos.md` | 13 | 4 of 4 | none |
| `lessons/08-textures.md` | 15 | 4 of 4 (obj. 4 partial: wrapping) | none |
| `lessons/09-normals-and-lighting.md` | 10 | 4 of 4 | none |
| `lessons/10-camera-and-scene.md` | 15 | 5 of 5 | none |
| `lessons/11-secondary-demo-scene/LESSON.md` | 15 | 4 of 4 | none |
| `lessons/12-scene-transition/LESSON.md` | 18 | 4 of 4 | none |
| `lessons/13-load-gltf-model/LESSON.md` | 12 | 4 of 4 | **yes** — `:39` model copy (−2) |
| `lessons/15-render-to-texture.md` | 15 | 4 of 4 | none |
| `lessons/16-bloom.md` | 17 | 4 of 4 | none |
| `lessons/17-depth-reconstruction-and-ssr.md` | **28** | 5 of 5 | none |
| `lessons/18-finish-the-scene.md` | 16 | 4 of 4 | none |
| `lessons/minimal-gltf-loader/LESSON.md` *(optional)* | 17 | 4 of 4 | none |

### Element breakdowns

Given in full for every lesson at or below zero (rule), for the two outliers by size, and for
every lesson whose figure is not obvious from its row. `L` = line number in that lesson file.

#### `00-project-setup` — **−1** (mandatory: scores at or below zero)

| L | Element (quoted) | Score |
|---|---|---:|
| 34–36 | "Copy `starter/package.json`, `starter/package-lock.json`, `starter/tsconfig.json`, `starter/index.html` and `starter/src/main.ts` into their corresponding repository-root paths, preserving `src/`." | **−2** toil |
| 37–38 | "Read `starter/README.md` before giving the first task" | 0 — tutor prep; the learner does nothing |
| 42 | "Install dependencies" | 0 — learner setup; no bundle can ship `node_modules`, and the 2026-09-13 ruling names `npm install` as expressly unaffected |
| 42 | "inspect each supplied file" | +1 — applies the TypeScript/npm prerequisite; serves "Distinguish type checking, bundling and static serving" |
| 42 | "type-check" | 0 evidence |
| 42 | "build" | 0 evidence |
| 42–43 | "start the development server" | 0 evidence |
| 43 | "verify both page output and the absence of console errors" | 0 evidence |
| 47 | "`npm run typecheck` and `npm run build` succeed." | 0 evidence |
| 47–48 | "`npm run serve` exposes the page on its reported local URL" | 0 evidence |
| 48 | "the page shows the starter heading" | 0 evidence |
| 48 | "the console has no error" | 0 evidence |

Sum: −2 +1 = **−1**. The lesson is almost entirely evidence, which is what a setup lesson is,
plus one span of toil which is not. Removing the toil (section 5) lifts it to +1 without
changing a single thing the learner learns. Its three stated objectives are all served — this
is a low score, not an unserved-objective finding. It goes to the author as a question in
section 5, not as a deletion proposal.

#### `17-depth-reconstruction-and-ssr` — **28** (outlier: 2.1x the mean)

| L | Element (quoted) | Score |
|---|---|---:|
| 42 | "Perform reconstruction and ray comparisons in one documented coordinate space." | +2 |
| 42–43 | "Add a view-space normal attachment with a defined encoding." | +2 |
| 43–44 | "Bound loop iterations for WebGL shader compilation and performance." | +2 |
| 44–45 | "Expose step count, thickness and maximum distance as controlled parameters." | +2 |
| 45–46 | "SSR must be toggleable and must fade rather than smear invalid/off-screen hits." | +2 |
| 50 | "Add and inspect the normal target" | +1 practice (the constraint above already scored the decision) |
| 50 | "reconstruct and visualise linear/view-space depth" | +2 |
| 50 | "reconstruct positions" | +2 |
| 51 | "verify them by camera motion" | 0 evidence |
| 51 | "derive the reflection ray" | +2 |
| 51 | "display projected ray steps" | +2 |
| 52 | "add depth-crossing detection" | +2 |
| 52 | "refine the first hit locally" | +2 |
| 52 | "sample reflected colour" | +1 practice |
| 52–53 | "then add edge, distance and grazing-angle fades" | +2 |
| 57 | "The reconstruction diagnostic remains spatially coherent under camera movement and resize." | 0 evidence |
| 57–58 | "A reflective procedural surface shows plausible reflections of visible scene content." | 0 evidence |
| 58–59 | "Off-screen and missing hits fade safely" | 0 evidence |
| 59 | "bounded marching cannot hang the shader" | 0 evidence |
| 59–60 | "SSR can be disabled without changing the base scene" | 0 evidence |
| 60 | "the learner can explain at least four failure modes inherent to SSR." | +2 |

Sum: **28**. Raised as an oversize lesson in section 6.

#### `12-scene-transition` — 18 (highest main-path lesson after 17)

| L | Element (quoted) | Score |
|---|---|---:|
| 30–31 | "Before selecting the characteristic transition, read `transition-menu.md` and ask the learner which style fits their two scenes." | +2 — tutor-addressed, learner decides (rubric's settled ruling) |
| 40–41 | "At progress zero the output must equal the first scene; at one it must equal the second." | +2 |
| 41 | "Neither scene may manipulate the other's internal resources." | +1 |
| 41–42 | "The transition owns its targets and resizes and disposes them explicitly." | +2 |
| 42 | "Keep a crossfade mode after the selected transition works." | +1 |
| 46 | "Render each scene to its own target" | +2 |
| 46 | "display each directly" | +1 |
| 46 | "implement crossfade with manual progress" | +2 |
| 47 | "add time-based direction and easing" | +2 |
| 48 | "then implement and validate the selected transition at endpoints and intermediate values" | +2 |
| 52 | "Each scene and render target can be displayed independently." | 0 evidence |
| 52–53 | "Crossfade and one learner-selected transition work in both directions, preserve exact endpoints, respond correctly after resize and do not leak resources." | 0 evidence |
| 54 | "Scene update/freeze behaviour during transitions is documented." | +1 — a policy the learner must choose (`DESIGN.md#scene-transition` leaves it open) |

"present `transition-menu.md`, ask for a choice" (L47–48) is the same instruction as L30–31 and
is scored once, at L30–31.

Sum: **18**.

#### `15-render-to-texture` — 15 (figure not obvious: several steps are repeats of lesson 12)

| L | Element (quoted) | Score |
|---|---|---:|
| 38–39 | "Build on the two-scene render-target work without replacing its transition boundary." | +1 |
| 39 | "Preserve the existing scene shaders." | +1 |
| 39 | "Use one scene colour texture and one sampleable depth texture." | +2 — the depth texture is new here |
| 40 | "Never sample an attachment while writing to it." | +2 |
| 40–41 | "Restore or explicitly set framebuffer and viewport state for every pass." | +2 |
| 45 | "Allocate attachments" | +1 practice — lesson 12 already allocated colour targets |
| 45 | "check completeness" | +1 practice — lesson 12 lists framebuffer completeness in its own Concepts |
| 45 | "render the scene off-screen" | +1 practice |
| 45–46 | "display its colour through a full-screen triangle" | +1 practice — lesson 12 already composed scene textures in a full-screen pass |
| 46 | "expose the depth texture as a diagnostic view" | +2 — new |
| 47 | "then integrate resize and cleanup" | +1 practice — lesson 12 already required the transition to "resize and dispose [targets] explicitly" |
| 51–53 | four completion conditions, all output checks | 0 each |

Sum: **15**. The scoring makes a real structural fact visible: **lesson 12 teaches framebuffers,
completeness and full-screen triangles before lesson 15 does.** Three of lesson 15's four stated
objectives were already exercised in lesson 12; only the sampleable depth texture and the
diagnostic views are new. This is raised in section 5 as a question, not a defect — the author
may well want the generalisation pass.

#### `13-load-gltf-model` — 12 (figure depressed by one toil span)

| L | Element (quoted) | Score |
|---|---|---:|
| 39–40 | "Before starting, copy every file under `model/` to a repository-root `models/` directory: `Duck.glb`, `LICENSE.md`, `SCEA.txt` and `ATTRIBUTION.md`." | **−2** toil |
| 40–41 | "Read `model/ATTRIBUTION.md` when introducing the asset and retain all four files together." | 0 |
| 43 | "Use `@gltf-transform/core` only for asset parsing and traversal, never for rendering." | +1 |
| 43–44 | "Support the packaged model first." | 0 — sequencing |
| 44 | "Reject missing required attributes with useful errors." | +2 |
| 44–45 | "Do not expose library types to the renderer or attempt complete glTF feature support." | +1 |
| 49 | "Fetch and parse `models/Duck.glb`" | +2 |
| 49 | "inspect its scene and first mesh primitive" | +2 |
| 50 | "adapt accessors to `MeshData`" | +2 |
| 50 | "handle its base-colour texture" | +2 |
| 50 | "upload through the established mesh path" | +1 practice |
| 51 | "then place the duck as a normal scene object" | +1 practice |
| 55–58 | five completion conditions, all output/validator checks | 0 each |

Sum: **12**. Removing the toil span lifts it to 14.

#### `minimal-gltf-loader` (optional) — 17 (contains the rubric's branch-point example)

| L | Element (quoted) | Score |
|---|---|---:|
| 32–33 | "For the exact supported subset and the cases that must be rejected, read `supported-subset.md` before proposing implementation tasks." | 0 — tutor prep |
| 42 | "The learner may skip this lesson without implementing anything; record that choice and advance." | 0 — the offer |
| 43–44 | "If taken, keep the library adapter available until the new decoder produces equivalent visible output." | +2 |
| 44 | "Implement only `supported-subset.md`, reject everything else clearly" | +2 |
| 44–45 | "and return the same `MeshData` boundary." | +1 |
| **49** | **"Choose or skip the path."** | **0 — branch point**, per the rubric's settled ruling. The rubric cites this element at `webgl 14/LESSON.md:48`; after `49af681` it lives at `lessons/minimal-gltf-loader/LESSON.md:49`. Same sentence, new address. |
| 49–50 | "If chosen, parse and validate the GLB envelope" | +2 |
| 50 | "decode JSON" | +1 |
| 50 | "locate the binary chunk" | +1 |
| 50 | "implement accessor extraction" | +2 |
| 51 | "adapt the supported primitive" | +2 |
| 51 | "decode its embedded image" | +2 |
| 51 | "compare with the library-backed result" | 0 evidence |
| 51 | "and switch adapters only after equivalence" | +1 |
| 55 | "Either the learner explicitly chooses to skip and the working library path remains intact, or:" | 0 — branch |
| 56–57 | "type checking and build pass"; "the minimal loader renders the same packaged duck"; "malformed or unsupported input fails explicitly" | 0 each |
| 57 | "and its documentation does not claim general glTF support." | +1 — the learner must write an honest scope statement |

Sum: **17**.

#### `11-secondary-demo-scene` — 15 (contains the rubric's tutor-addressed example)

| L | Element (quoted) | Score |
|---|---|---:|
| 31–32 | "Before asking the learner to choose, read `effect-menu.md`. Present the effects grouped and sorted by its difficulty levels, including the technique and scope note." | 0 — tutor prep |
| **32–33** | **"The tutor MUST explicitly ask which effect the learner wants to build. Do not silently choose for them."** | **+2 teaching** — the rubric's own named example. Tutor-addressed; the learner must decide. |
| 33–34 | "They may propose another effect; assess it against the same scale before accepting or narrowing it." | +1 |
| 44–45 | "Preserve the first scene unchanged." | +1 |
| 45–46 | "Both scenes must implement the lifecycle in `#demo-scene-contract`, own their GPU resources and render correctly when invoked independently." | +2 |
| 48 | "For Level 3 or 4 choices, establish one diagnostic visualisation before the final look." | +2 |
| 48–50 | "For "Technokartoffeln", the tutor may and should use that name alongside "3D metaballs" for fun..." | 0 — tone instruction; the learner does nothing |
| 54 | "ask for the learner's selection and desired visual mood" | +1 (the effect choice itself is scored once, at L32–33) |
| 55 | "agree a bounded definition of done" | +2 |
| 55–56 | "adapt the cube-wave scene to it without visual changes" | +2 |
| 56 | "build the selected effect from its core mechanism outward" | +2 |
| 56–57 | "then verify independent resize, pause and disposal behaviour" | 0 evidence |
| 61–64 | five completion conditions, all output/record checks | 0 each |

Sum: **15**. Note that this figure **understates** the lesson: `effect-menu.md` authors twelve
effects, each with a technique, a completion target, a scope warning and an enhancement, plus a
four-level assessment scale for learner proposals. Those 97 lines are real teaching that the
lesson's own progression cannot show, because the learner meets exactly one of them. The same is
true of `12-scene-transition`'s `transition-menu.md`. The ruler used here counts clauses in the
lesson, so an authored catalogue is invisible to it. Said plainly so nobody reads 15 as thin.

#### `04-uniforms-and-animation` — 9 (lowest main-path figure after 00)

| L | Element (quoted) | Score |
|---|---|---:|
| 37–38 | "Handle a missing required uniform location explicitly." | +2 |
| 42 | "Add a scalar uniform" | +2 |
| 42 | "make it affect the shader" | +1 practice |
| 42 | "introduce the frame callback" | +2 |
| 42–43 | "verify that refreshing or resizing does not create multiple loops" | 0 evidence |
| 47–48 | "The animation is time-based, continues smoothly at varying refresh rates, and draws from one intentional loop." | 0 evidence |
| 48 | "Build and type check pass." | 0 evidence |
| 48–49 | "The learner can classify current data as per-vertex, per-draw or per-frame." | +2 |

Sum: **9**. All four objectives are served; the lesson is simply short. Not flagged as an
outlier — it sits inside the course's spread.

#### Remaining lessons — summary of the sums

Scored on the same protocol; every element carries a `file:line` in my working notes and can be
reproduced from the lesson text. The recurring shapes are:

- `01` (10): context acquisition +2, clear-colour choice +2, drawing-buffer resize +2, viewport
  +1, clear +1, multi-size inspection 0, three completion checks 0, and `:47–48` "a missing
  context produces a useful error rather than a null dereference" +2.
- `02` (14): `:36` "Generate three positions from `gl_VertexID`" +2, `:36–37` "Check compile and
  link status and include diagnostic logs in thrown errors." +2, `:37` "Delete failed
  shader/program objects." +1, write/compile shaders +2, link +1, select +1, draw +1, `:41–42`
  "then deliberately break a shader briefly to observe the diagnostic path" +2, two evidence
  conditions 0, `:47–48` "the learner can explain the value written to `gl_Position` and why the
  fragment shader needs a precision declaration." +2.
- `03` (13): `:36–37` "Make byte-based stride and offset calculations explicit." +2, `:37` "Keep
  the vertex format simple enough to inspect manually." +1, upload positions +2, connect
  attribute +2, add colour/varying +2, `:42` "Change one layout parameter intentionally and
  reason from the corrupted image." +2, two evidence 0, explain-in-bytes +2.
- `05` (13), `06` (11), `07` (13), `08` (15), `09` (10), `10` (15), `16` (17), `18` (16) follow
  the same pattern: 5–8 constructing steps at +2, 1–3 practice steps at +1, all output-checking
  completion conditions at 0, and one "the learner can explain…" condition at +2.

A consistent and deliberate ruling across the whole course: **"the learner can explain X"
completion conditions score +2**, not 0. They are the course's real assessment — they require
the learner to construct an account, and a wrong account is instructive. Fourteen of the
nineteen lessons carry one. Scoring them as evidence would have cost the course 28 points and
would have misdescribed what this course does.

---

## 3. Goal gaps

**None. Zero unserved learning objectives, zero unserved `DESIGN.md` anchors, zero unserved
coverage-list topics. Course-level gap penalty: 0 x −3 = 0.** This agrees with the arithmetic
in section 1.

That is an unusual finding and I want it checkable, so here is how each class was decided.

### The 16 `DESIGN.md` anchors — decided by what lessons make the learner DO, never by `design_refs`

| Anchor | Served by (what the learner does) |
|---|---|
| `#platform-toolchain` | `00`: copies, type-checks, builds and serves the plain HTML/esbuild/`tsc` shell |
| `#api-boundary` | `01`–`03`: raw `WebGL2RenderingContext` calls throughout; `02:36–37` requires helpers that expose diagnostics rather than conceal them |
| `#matrix-convention` | `05:41` composes model→view→projection in the stated order; `05:46–47` "trace a sample vertex through the named spaces"; `17:42` "one documented coordinate space" |
| `#shader-convention` | `02`: GLSL ES 3.00 with `in`/`out`, compile/link status checked immediately, failure stops construction; `03`: explicit attribute layout |
| `#mesh-boundary` | `07:43` "define `MeshData`"; `13:50` "adapt accessors to `MeshData`" |
| `#resource-ownership` | `02:37`, `07:44`, `12:41–42`, `15:47`, `16:50` — five lessons delete or recreate what they own |
| `#scene-boundary` | `10:46` "Extract camera state"; `10` sets frame-wide then per-object state |
| `#first-demo-scene` | `10`: one instanced cube mesh, sine-wave displacement from time and grid position, bright crests, orbit camera |
| `#demo-scene-contract` | `11:45–46` both scenes implement the shared lifecycle; `11:55` defines its concrete form |
| `#scene-transition` | `12`: both scenes to separate targets, full-screen composition, exact endpoints, documented freeze policy |
| `#lighting-model` | `09`: ambient + one directional Lambertian term, computed in world space, no specular/PBR |
| `#texture-convention` | `08:36–37` "Make the vertical orientation decision explicit"; `08:41` "test orientation" |
| `#asset-loading-paths` | `13` (required library path) and `minimal-gltf-loader` (optional direct path), both returning the same `MeshData` |
| `#post-processing-pipeline` | `15`, `16`, `17`, `18` — off-screen pass, bloom, depth-reconstructing SSR, every pass toggleable and independently viewable |
| `#packaged-model` | `13:39–40` copies the four files; `13:63` records attribution; `18:41` "Retain model attribution and licences." **Caveat below.** |
| `#unresolved-decisions` | `07:54`, `10:60–61`, `11:68–70`, `12:58–59`, `16:55`, `17:64–65` — six lessons record learner decisions under new stable anchors. **Cited by no `design_refs` entry at all**, and served all the same. This is the rubric's own warning about the citation proxy, reproduced exactly in this course. |

**Caveat on `#packaged-model`.** Today the anchor's principal service is the copy instruction at
`13:39–40`, which section 4 scores as toil. If the author accepts the supplies proposal, that
instruction disappears and the anchor is left served by `13:63` (a persist line, which I do not
score) and `18:41` ("Retain model attribution and licences"). The anchor would still be served,
but thinly, and by a retention obligation rather than an act. The author already reasoned along
exactly this line in `49af681` when removing the licence objective. Flagged so the decision is
made deliberately rather than discovered later; a one-clause addition to `18`'s progression
("check the licence files are still beside the model and cited in the project README") restores
it cheaply.

### The 55 coverage-list topics

Every one is exercised by a main-path lesson. The four I had to work hardest to confirm, because
word overlap would have misled:

- **"primitive assembly"** — no lesson uses the phrase in a task. Served by `02:41` "issue one
  triangle draw" (mode and vertex count with no buffer) and decisively by `07:43` "Convert the
  procedural object to indices", which is exactly the vertex-record-versus-topology distinction.
- **"homogeneous coordinates"** — served by `05:46–47` "trace a sample vertex through the named
  spaces" plus `05`'s stated objective on the role of `w`; `02`'s optional path deepens it but
  the required path already covers it.
- **"multiple render targets"** — appears in a task nowhere, and in `16:32` only as an
  alternative ("multiple render targets or extraction passes"). Served by `17:15–16` "The
  off-screen pass must provide depth and a world- or view-space normal texture; add the normal
  attachment before reflection marching" and `17:42–43` "Add a view-space normal attachment with
  a defined encoding": adding a second colour attachment to the existing scene framebuffer *is*
  MRT. No lesson names `gl.drawBuffers`. Served, but by inference — see the proposal in section 5.
- **"WebGL state"** — served by `01` (state-machine model), `06` (depth and cull state),
  `15:40–41` ("Restore or explicitly set framebuffer and viewport state for every pass") and
  `18:47` ("audit allocations/state transitions").

### Two partial topics — listed, **not** penalised, and I want the reasoning argued with

The rubric penalises a stated item "that no task exercises". These two are exercised in part, so
levying −3 would be over-reading; leaving them unlisted would be under-reporting.

- **`COURSE.md:95` "texture filtering and wrapping"** and **`08:21` "Explain wrapping, filtering,
  mipmaps and image orientation".** Filtering is exercised (`08:42` "compare nearest and linear
  filtering"), mipmaps are (`08:42` "enable a valid mipmap policy"), orientation is (`08:41`
  "test orientation"). **Wrapping is exercised nowhere.** It appears only in the objective and in
  `08:32` Concepts. No progression step and no completion condition touches `TEXTURE_WRAP_S/T`.
- **`COURSE.md:96` "mipmaps and power-of-two considerations".** Mipmaps are exercised;
  "power-of-two considerations" appear in no lesson at all — unsurprising, since WebGL 2 lifted
  the NPOT mipmap restriction that made the phrase matter in WebGL 1.

A stricter reader could levy −3 each, taking the course to 237 main-path / 254 overall. I did
not, and section 5 proposes repairs that close both for good. The choice is visible so the
author can overrule it.

### Every per-lesson objective is served

I walked all 73 stated `learning_objectives` across the 19 lessons against that lesson's own
tasks. All are served except the wrapping fragment noted above. The objective `49af681` removed
("Carry asset licence and attribution into the repository") left **no dangling references**: no
lesson, `COURSE.md` or `DESIGN.md` line names an objective that no longer exists. The licence
*work* correctly remains as a constraint (`13:39–41`), a completion condition (`13:55`), a
validator (`has-model`), and two obligations in lesson 18 (`18:41`, `18:56`). Removing the
objective while keeping the work was the right shape and it was done cleanly.

---

## 4. The toil inventory

**Two confirmed toil spans, −2 each, −4 in total. Both are the same defect: the bundle ships
nine files for the learner's workspace and declares no `supplies:` entry for any of them.**

### Checked against the ruling of 2026-09-13 — no score moves

`references/rubric.md` now rules that **a project skeleton is toil** where the two tests disagree,
and asks the shippability question in full: *could the bundle have shipped one set of files for
each language the course supports?* Re-checked here:

- **This course's skeleton is finding 1 below**, and it was already toil. The learner copies a
  shipped `starter/` set at `00:34–36`; the five files sit in the bundle, so the plain
  shippability test already answered yes and the tiebreak never has to fire. −2 before the ruling,
  −2 after it.
- **No lesson asks the learner to create a skeleton with a toolchain command.** Searching
  `COURSE.md` and all nineteen lessons for `init`, `scaffold` and `skeleton` returns no such
  instruction: the skeleton arrives in this course as files to move, never as `npm init`. There is
  no second, unscored skeleton site.
- **The exception does not apply to `00`.** Its three objectives are "Distinguish type checking,
  bundling and static serving", "Run a TypeScript entry point in a plain HTML page" and "Use the
  console and page as separate sources of evidence"; `#platform-toolchain` describes the target
  platform and the tools, not the act of assembling the project. No objective and no anchor makes
  placing the files the subject, so it stays toil — which is also what P1 proposes to remove.
- **`npm install` at `00:42` stays the learner's work**, named in the ruling as unaffected.

**Section 1 is unchanged: 243 main-path, 260 across all 19 scored rows.** What the ruling did
change here is an *argument*, not a figure — see the protocol note in the rubric section above and
the renderer-code entry under "Additional sites" below.

### Confirmed

**1. `lessons/00-project-setup/LESSON.md:34` (sentence spans lines 34–36)** — the exact sentence:

> "Copy `starter/package.json`, `starter/package-lock.json`, `starter/tsconfig.json`,
> `starter/index.html` and `starter/src/main.ts` into their corresponding repository-root paths,
> preserving `src/`."

Deterministic, unambiguous, no decision, and a mistake teaches nothing — a mistyped destination
produces a build error about a missing file, which is not a lesson about type checking, bundling
or static serving. And the bundle **could** have handed the result over: all five files exist at
`lessons/00-project-setup/starter/`, inside `lessons/`, so a lesson-scoped `supplies:` entry
places them when the lesson opens. **−2.**

**2. `lessons/13-load-gltf-model/LESSON.md:39` (sentence spans lines 39–40)** — the exact
sentence:

> "Before starting, copy every file under `model/` to a repository-root `models/` directory:
> `Duck.glb`, `LICENSE.md`, `SCEA.txt` and `ATTRIBUTION.md`."

Same test, same answer. The four files exist at `lessons/13-load-gltf-model/model/`, inside
`lessons/`, and the `has-model` validator already checks the destination. Copying a binary and
three text files teaches nothing about GLB containers, accessors or adapter boundaries — which
is what the lesson is for. **−2.**

The following clause of that same sentence, "Read `model/ATTRIBUTION.md` when introducing the
asset and retain all four files together" (L40–41), is **not** toil: it is a licence obligation,
it survives the supplies entry, and it must stay in the lesson.

### Examined and rejected — recorded so the next reader does not re-litigate them

- **`lessons/00-project-setup/LESSON.md:42`** — the `install` verb fired. The line still reads
  exactly as the rubric records it:

  > "Install dependencies, inspect each supplied file, type-check, build, start the development
  > server, and verify both page output and the absence of console errors."
  > *(physical line 42 ends at "development"; the sentence continues on line 43)*

  **Rejected, on the rubric's stated ground: no bundle can ship `node_modules`**, which the
  2026-09-13 skeleton ruling restates and preserves by name. There is no
  `supplies:` entry to write, because the result has to come off a package registry. This is the
  learner's setup and it is scored as what it actually is — evidence, 0 — not as toil. The rest
  of the sentence is the lesson itself. I am not reopening this.

- **`lessons/13-load-gltf-model/LESSON.md:39`** — the same line as confirmed finding 2, reported
  by the scanner as one physical line ending in a colon. Opened, split, and the first clause
  confirmed as toil; the trailing licence-reading clause rejected.

### Additional sites I checked and found clean

The scanner is a candidate generator over a fixed verb list, and **an empty candidate list is
not a pass**, so I read all nineteen lessons looking for toil it has no pattern for. What I
considered and rejected:

- Every `npm run typecheck` / `npm run build` / `npm run serve` instruction — evidence, 0.
- `13:40–41` "retain all four files together" — a licence obligation, not toil.
- `15:45` "Allocate attachments", `16:42` "validate the HDR target" and similar — renderer code.
  Each is a decision the learner makes and a mistake that shows on screen, so the toil row is
  already out at its first three clauses and its shippability clause is never reached.
  `COURSE.md:24` ("The learner writes the renderer") and `#api-boundary` make that the subject of
  the course. **Not** rejected on the ground that the bundle could not ship the files — it could,
  and per the 2026-09-13 ruling that would not have saved them.
- `11:31–32` and `12:30–31`, the instructions to read `effect-menu.md` and
  `transition-menu.md` — the tutor reads them; no file is moved and no learner act is assigned.

**The toil surface of this bundle is exactly its two shipped file sets**, because `starter/` and
`model/` are the only bundle files ever destined for the learner's workspace. **This inventory
came from reading the lessons, not from the scanner**, and the scanner's three candidates
happened to overlap it in two places.

---

## 5. Proposals

Each names a concrete action. All are proposals; applying any of them is the
`tutorail-authoring` skill's job, not this one's. Nothing in the bundle was changed here.

### P1 — Declare the starter files as supplies and delete the copy instruction (closes toil 1, +2)

```
cd /Users/robert/.claude/plugins/cache/tutorail-authoring/tutorail-authoring/0.3.0/skills/tutorail-authoring
python3 scripts/supplies.py add /Users/robert/src/github.com/skomp/tutorail-bundles/webgl-typescript-scene \
  --from lessons/00-project-setup/starter \
  --to . \
  --describe "Plain HTML + TypeScript + esbuild starter shell: package.json, package-lock.json, tsconfig.json, index.html and src/main.ts" \
  --lesson 00-project-setup \
  --check
```

`--from` is bundle-relative and sits inside `lessons/`, as a `--lesson`-scoped entry requires.
`--to .` is the learner's workspace root. Then:

- **delete** `lessons/00-project-setup/LESSON.md:34–36` (the whole Copy sentence);
- **keep** L37 "Do not introduce a framework…" and L37–38 "Read `starter/README.md`…";
- **rewrite** `lessons/00-project-setup/starter/README.md:3–4`, which currently repeats the copy
  instruction ("Copy `package.json`, `package-lock.json`, `tsconfig.json`, `index.html` and
  `src/main.ts` to their corresponding paths at the root of a new repository.") and would
  otherwise contradict the supplies entry. Replace with a sentence saying the files are placed
  for the learner and what each one does — which is what the lesson wants the learner to inspect.
- **Note:** a directory-scoped entry also places `starter/README.md` at the workspace root, which
  today's instruction deliberately excludes. Either move `README.md` up to
  `lessons/00-project-setup/STARTER-NOTES.md` (and update L37–38's path), or replace the single
  entry above with five per-file entries. The move is cleaner and keeps the notes where the tutor
  reads them.

Effect: lesson `00` goes from **−1 to +1** and the learner loses nothing.

### P2 — Declare the model files as supplies and delete the copy instruction (closes toil 2, +2)

```
cd /Users/robert/.claude/plugins/cache/tutorail-authoring/tutorail-authoring/0.3.0/skills/tutorail-authoring
python3 scripts/supplies.py add /Users/robert/src/github.com/skomp/tutorail-bundles/webgl-typescript-scene \
  --from lessons/13-load-gltf-model/model \
  --to models \
  --describe "Khronos glTF Sample Assets Duck GLB with its SCEA licence, Khronos metadata licence and attribution" \
  --lesson 13-load-gltf-model \
  --check
```

Then **delete** the first sentence at `lessons/13-load-gltf-model/LESSON.md:39–40` and **keep**
the licence clause, rewritten to stand alone, e.g. "Read `models/ATTRIBUTION.md` when introducing
the asset; the model, `LICENSE.md`, `SCEA.txt` and `ATTRIBUTION.md` must stay together." The
`has-model` validator (`models/Duck.glb`) and the completion condition at `13:55` are unaffected.

Effect: lesson `13` goes from **12 to 14**.

Together P1 and P2 take the course from **243 to 247** main-path (260 to 264 overall) with no
change to what the learner learns. They are the whole of the recoverable loss in this course.

### P3 — Restore `#packaged-model`'s service after P2

P2 removes the anchor's principal act. Add one clause to `lessons/18-finish-the-scene.md:45–48`,
e.g. "confirm the licence and attribution files are still beside the model and cited in the
project documentation", so the anchor is served by something the learner does rather than by a
persist line. Cheap, and it keeps a licence obligation visible at the end of the course where it
belongs.

### P4 — Close the wrapping gap in lesson 08 (one clause)

Add to `lessons/08-textures.md:41–42`, after "test orientation": "set `TEXTURE_WRAP_S`/`_T` and
compare `REPEAT` with `CLAMP_TO_EDGE` on UVs deliberately pushed outside 0–1". That is a genuine
decision with an instructive wrong answer, it serves the existing objective at `08:21` verbatim,
it serves `COURSE.md:95` in full, and it adds +2. Optionally mirror it in the completion
conditions at `08:46`.

### P5 — Decide "power-of-two considerations" one way or the other

Two acceptable outcomes, and I argue for the second:

1. Add a clause to lesson 08 exercising NPOT behaviour; or
2. **Drop "power-of-two considerations" from `COURSE.md:96`**, leaving "mipmaps". WebGL 2 removed
   the NPOT mipmap and wrapping restrictions, so the phrase describes a WebGL 1 constraint that
   the course's own stated target (`DESIGN.md#platform-toolchain`: "a modern desktop browser with
   WebGL 2") does not face. The course boundary section already declines things that belong to
   other courses; this belongs with them.

### P6 — Name `gl.drawBuffers` where MRT is actually required

`COURSE.md:114` promises "multiple render targets". The learner does it at `17:42–43` without the
lesson ever saying so, and `16:32` offers "multiple render targets **or** extraction passes",
which reads as permission to avoid it. Add the API to `lessons/17-depth-reconstruction-and-ssr.md`
Concepts (L36–38) and one clause to its Constraints at L42–43: "write colour and normal from one
pass with `gl.drawBuffers`". Closes the inference and makes a must-cover topic unmissable.

### P7 — Fix the one residual reference from `49af681`

`COURSE.md:137` reads:

> "`minimal-gltf-loader` is an optional lesson, offered while you are in lesson 14."

The manifest offers it at `lessons/13-load-gltf-model/LESSON.md`, and the commit message for
`49af681` itself says "offered while the learner is in lesson 13". The sentence is right by
`COURSE.md`'s own 1-based chapter map (chapter 14 *is* the glTF lesson) and wrong by every lesson
id and prerequisite line in the bundle, which use the 0-based file numbering. Replace the bare
number: "offered while you are in the glTF model lesson (`13-load-gltf-model`, chapter 14 above)".

Related and worth a decision, though not a defect on its own: since `49af681` the two numbering
schemes no longer differ by a constant. Chapters 1–14 map to files `00`–`13` (offset +1), while
chapters 15–18 map to files `15`–`18` (offset 0); the missing `14` absorbs the difference. Any
future bare chapter number in prose is a trap. Either renumber the post-14 files to close the
gap, or state the mapping once in `COURSE.md` and never write a bare lesson number again. P7
alone is enough to remove the live ambiguity.

### P8 — A question for the author about lesson `00` (score at or below zero)

The rubric requires this to be a question, not a deletion proposal. Lesson `00` scores **−1**.
Its elements are one toil span and eleven evidence steps:

> `:34–36` "Copy `starter/package.json` … preserving `src/`." (−2)
> `:42` "Install dependencies, inspect each supplied file, type-check, build, start the
> development server, and verify both page output and the absence of console errors."
> (0, +1, 0, 0, 0, 0)
> `:47–48` four completion conditions, all output checks (0 each)

P1 lifts it to +1, which is an honest figure for a setup lesson: it establishes the feedback loop
the rest of the course runs on, and the rubric has no row that rewards that. **What is this
lesson for beyond the feedback loop, and does it want more teaching in it** — for example, making
the learner predict which of `tsc` and `esbuild` catches which of two deliberately planted errors,
which would serve its first objective with a decision instead of an inspection? You know whether
that is worth the minute it costs. I am not proposing to delete anything.

### P9 — A question about lessons 12 and 15

Lesson `12` teaches framebuffers, completeness and full-screen triangles; lesson `15` states all
three again as objectives (`15:20–23`), and only its sampleable depth texture and diagnostic views
are new. Was the overlap intended as a generalisation pass, or did render-to-texture arrive early
in lesson 12 because the transition needed it? If the former, `15:20–23` could say so ("you built
these ad hoc in lesson 12; here they become the pipeline"), which would stop a learner wondering
whether they missed something. If the latter, some of lesson 15's framebuffer material may want to
move forward into lesson 12. Your call — the rubric cannot see the intent.

### P10 — A question about splitting lesson 17

See section 6. Lesson `17` scores 28 against a mean of 13.5 and carries twenty scored elements:
depth linearisation, inverse projection, a normal G-buffer, reflection-ray derivation, bounded
marching, hit refinement and five artefact mitigations. The natural seam is at `17:51`, between
"verify them by camera motion" and "derive the reflection ray": everything before it is depth
reconstruction (a complete, separately valuable skill with its own diagnostic), everything after
is SSR. Splitting would also let the reflective procedural surface that `17:57–58` requires get an
explicit construction step, which no progression clause currently assigns.

---

## 6. The questions only a reader can answer

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

**Two instances found.**

- **`lessons/06-depth-and-culling.md:4`** — `design_refs: [api-boundary, matrix-convention]`. The
  lesson raises the winding question directly: `:21` "Relate vertex winding to front and back
  faces", `:40` "inspect mesh winding", `:45–46` "no required face disappears under the chosen
  culling state". A learner following `#matrix-convention` finds handedness, column vectors and
  the camera's −Z axis, and **no statement of which winding is front-facing** — and no other
  anchor in `DESIGN.md` states one either. `#api-boundary` says nothing about depth or cull state.
  The lesson then tells the learner to decide it themselves (`:50` "Record the … front-face
  convention"). That may be deliberate, but `#unresolved-decisions` at `DESIGN.md:116–119` does
  not list the front-face convention among the decisions it defers, so the learner is deciding
  something the design document neither answers nor admits to leaving open. **Question: should
  `#matrix-convention` state the front-face winding, or should `#unresolved-decisions` name it?**

- **`lessons/01-canvas-and-context.md:4`** — `design_refs: [platform-toolchain, api-boundary]`.
  The lesson demands a policy at `:36–37` ("Centralise drawing-buffer resize logic and cap or
  explain the chosen device-pixel-ratio policy") and checks it at `:47–48` ("its backing
  dimensions match the documented policy"). Neither cited anchor mentions drawing-buffer sizing
  or device-pixel ratio, and `#unresolved-decisions` does not list it either. Same shape as
  above, same question.

Both are cheap to fix and neither is a scored finding.

### 6.2 A lesson that introduces a type or concept nothing later uses

**None found.** Three candidates examined and all three rejected as deliberate scaffolding, each
of which the course itself flags as temporary:

- `02:36` "Generate three positions from `gl_VertexID`; **GPU buffers arrive next lesson.**"
  Discarded in lesson 03 — by announcement.
- `03:51` "Record the **chosen temporary vertex layout**". The per-vertex colour attribute is
  superseded by texture and lighting in lessons 08–09; the *concept* it teaches (varying
  interpolation) is used for the rest of the course.
- `07:37–38` "Define `MeshData` with positions, normals, UVs and optional indices **even if some
  attributes are temporarily unused.**" Normals are used in 09, UVs in 08 — one and two lessons
  later respectively.

Every type introduced in this course is consumed later, usually within two lessons. This is one
of the course's genuine strengths and it should be said as plainly as the findings are.

### 6.3 A lesson far outside the course's usual size

**Two, in opposite directions.** Mean main-path lesson: 13.5; the middle of the distribution runs
9–18.

- **`lessons/17-depth-reconstruction-and-ssr.md` — 28, twenty scored elements, 2.1x the mean.**
  Far the largest. It carries two teachable subjects: recovering view-space position from a depth
  buffer, and screen-space reflection. Its own title names both. Proposal P10 gives the seam. A
  learner who stalls anywhere in this lesson has no smaller unit to fall back to, which is the
  practical cost of an oversize lesson.
- **`lessons/00-project-setup/LESSON.md` — −1, and structurally unlike every other lesson**
  (eleven of twelve elements are evidence). It is small because it is setup, not because it is
  incomplete; all three of its objectives are served. P8 asks the author about it rather than
  proposing a change.

No other lesson is outside 9–18.

### 6.4 A must-cover topic that only an optional lesson teaches

**None found — and I checked rather than assumed.** `minimal-gltf-loader` teaches GLB headers,
JSON/BIN chunks, buffer views, accessors, component types, byte stride and image buffer views.
**Not one of those appears in `COURSE.md:69–124`.** The two adjacent topics that *are* in the
coverage list, "asynchronous asset loading" (`COURSE.md:110`) and "glTF model integration"
(`COURSE.md:111`), are both taught on the main path by `13-load-gltf-model`.

So the question the rubric insists on asking — *is it acceptable that a learner who declines
every offer never meets this material?* — has the easiest possible answer here: **yes, because
the course never promised it.** The optional lesson is pure enrichment, sitting exactly where the
bundle format says such a lesson should. `COURSE.md:132–133` even states the boundary explicitly:
"The optional loader lesson supports only the packaged model's documented subset and must say so
clearly." Nothing is at risk, and no author judgement is needed.

### 6.5 The completability invariant, asked out loud

> **Can a learner who declines every offer still finish this course?**

**Yes. Verified against the lessons, not only against the manifest.**

- **Does any main-path completion condition depend on something only the optional lesson builds
  or explains?** No. I read all eighteen main-path `## Completion conditions` blocks. The only
  asset-loading condition downstream of the offer is `13:55–58`, which is satisfied by the
  library-backed adapter the same lesson builds. Lessons `15`, `16`, `17` and `18` never mention
  GLB decoding; they consume `MeshData`, which exists either way.
- **Does any main-path lesson's prose assume the learner took the offer?** No. There are exactly
  two main-path mentions of the optional lesson, and both handle the decline case explicitly:
  - `lessons/13-load-gltf-model/LESSON.md:67–68` — "The optional lesson `minimal-gltf-loader`
    replaces the parsing-library adapter with one you write. The tutor offers it here; **it is
    not required for WebGL coverage or the final scene.**" (offer, not assumption)
  - `lessons/15-render-to-texture.md:15–16` — "Lesson `13-load-gltf-model` is complete. The
    optional lesson `minimal-gltf-loader` **was taken or declined; either way a working
    `MeshData` adapter exists.**" (both branches named, and the post-condition stated)
- **Does the manifest gate anything?** No. `grep -rn -E "required_for|anticipates|repair_in"`
  over the whole bundle returns nothing. The `optional_lessons` block at `tutorial.yaml:29–36`
  carries only `offer_at` and `offer_because`. **No `required_for` gate exists, so the −3 row
  does not fire and its warning is not printed** — there is no gate to warn about. I checked this
  by opening `tutorial.yaml` rather than by trusting `optional_lesson_count`, as the skill
  requires.

**The invariant holds.**

### 6.6 Prose optionality versus the manifest — the rubric's own worked defect, re-checked

The rubric records this bundle as the case where a lesson's prose called it optional while the
manifest required it. **That defect is repaired, and the repair holds.** Verified in the current
files:

| Check | Result |
|---|---|
| Is the lesson in `optional_lessons:`? | Yes — `tutorial.yaml:29–35`, keyed `lessons/minimal-gltf-loader/LESSON.md`, with `offer_at: [lessons/13-load-gltf-model/LESSON.md]` and an `offer_because` |
| Is it absent from `lessons:`? | Yes — `tutorial.yaml:13–27` lists 18 main-path lessons and does not include it |
| Does the lesson declare itself optional? | Yes — `minimal-gltf-loader/LESSON.md:4` `optional: true` |
| Does its prose agree? | Yes — `:11` "Optionally look below the parsing library", `:12` "not a prerequisite for later WebGL concepts", `:42` "The learner may skip this lesson without implementing anything", `:55` "Either the learner explicitly chooses to skip and the working library path remains intact, or:" |
| Does `COURSE.md` agree? | Yes — `:135–141`, in its own "Optional path" section, out of the numbered map |
| Do its neighbours agree? | Yes — `13:67–68` and `15:15–16`, both quoted above |
| Leftover `14-optional-minimal-gltf-loader` references? | None. `grep -rn "14-optional"` returns nothing |
| Does the tooling now see it? | Yes — `audit.py` reports "18 lesson(s), 1 optional" over 19 rows |

**Prose and manifest agree everywhere.** The course is scored as the manifest has it, and the two
totals a reader needs are both given in section 1: **243** for a learner who declines,
**260** for one who accepts. The rubric's published 194 / 183 describe the pre-repair bundle and
are superseded.

One residual from the repair, not an optionality defect: the bare "lesson 14" at `COURSE.md:137`,
addressed in P7.

---

## Verdict

A strong course. It teaches by making the learner decide and construct at almost every step, it
breaks things deliberately and reasons from the wreckage, it demands an explanation at the end of
fourteen of nineteen lessons, it serves all 55 of its declared topics and all 16 of its design
anchors, and it introduces nothing it does not later use. The completability invariant holds and
no gate is hiding in the manifest.

Its entire recoverable loss is 4 points across two file-copy instructions, caused by one omission:
**the bundle declares no `supplies:` entries at all** while shipping nine files destined for the
learner's workspace. P1 and P2 close that. P4 and P5 close the only two topics that are exercised
in part rather than in full. Everything else in section 5 is a question for the author, which is
where it belongs.
