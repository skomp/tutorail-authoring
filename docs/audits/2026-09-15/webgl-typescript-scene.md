# Course quality audit: `webgl-typescript-scene`

Audited 2026-09-15 against `tutorail-authoring:course-quality` and its `references/rubric.md`.
Read-only: nothing in `/Users/robert/src/github.com/skomp/tutorail-bundles` was created, edited,
staged or deleted. `git status --porcelain` in that repository was empty at the start and at the
end of this audit.

## Provenance

```
Audit provenance, 2026-09-15 — identical for all five bundles

bundles     skomp/tutorail-bundles @ 221c164 (== origin/main, tree clean)
rubric      skomp/tutorail-authoring @ 86c2bc7, plugin 0.4.0
            skills/course-quality/references/rubric.md
validator   pinned copy of the WHOLE scripts directory from the source checkout
            skomp/tutorAIl @ 717c575  ->  /private/tmp/claude-501/-Users-robert-src-github-com-skomp-tutorail-authoring/19f2342f-a334-4dd6-9b45-348b60a85a2d/scratchpad/pin/validate_bundle.py
            (10 validate_bundle.py copies exist on this machine; this is the source one)
yaml reader restricted built-in, ALWAYS — tutorAIl#29 decided at 7419722,
            "Parse YAML with the restricted reader always, never PyYAML".
            PyYAML 6.0.3 is importable here and is deliberately not used.
verdicts    all five bundles: PASS - every applicable check ran and found nothing. exit 0
```

**The validator's verdict is not an input to this report.** Structural validity and teaching
quality are different questions; "the bundle loads" is never an answer to anything here. The
provenance block is printed because a green line that does not record *which* copy of the
validator and *which* YAML reader produced it is a claim about a machine on a day, not a result.

## What changed since the 2026-09-13 audit

Two fixes landed in this bundle, both from `tutorail-bundles#6`:

- **`b969892`** — lesson `00-project-setup`: the five-file copy instruction is deleted and the
  starter set is declared as a lesson-scope `supplies` entry.
- **`221c164`** — lesson `13-load-gltf-model`: the four-file copy instruction is deleted and the
  model set is declared as a lesson-scope `supplies` entry.

A third commit, **`d11644a`** (`tutorail-bundles#11`), bound the symbol `w` in lesson 02.

On 2026-09-13 this bundle carried the catalogue's last two confirmed toil sites. **Both charges
come off. The confirmed-toil count for this bundle is now 0.**

---

## The rubric, printed in full

### The scored rows

| Element | Score | Test |
|---|---|---|
| **teaching** | +2 | the learner decides or constructs; a wrong answer is instructive; it serves a stated objective |
| **practice** | +1 | applies something already taught; no new decision, but the repetition is the point |
| **evidence** | 0 | run a validator, read output, report what happened |
| **toil** | −2 | deterministic and unambiguous; no decision; a mistake teaches nothing — **and the bundle could have handed the result over instead of assigning it** |
| **unserved objective** | −3 **each** | a stated objective or `DESIGN.md` anchor that no task exercises. Course-level, counted once PER UNSERVED OBJECTIVE |
| **`required_for` on an optional lesson** | −3 | the author declared something load-bearing and then made it skippable. Scored **and** raised |

Load-bearing clauses of the toil row, applied below:

- **The last clause governs.** Setup that needs the network, a toolchain or an account is the
  learner's work and is not toil: no `supplies:` entry can create `node_modules`. The question is
  never "is this boring?" but "**could this bundle have shipped the result?**"
- **A project skeleton is toil** where the two tests disagree (ruled 2026-09-13). This bundle's
  skeleton always shipped as `starter/` files, so the plain shippability test already answered
  yes and the tiebreak never fired here — before or after the fix.
- **The exception** — setup that is itself the subject — fires only when the setup step is the
  **only** element serving an objective that names it. It does not fire in this course; see §4.
- **A step the tutor performs is not an element.** Not applicable here: this bundle hands the
  work to *supplied files*, not to the tutor.

### The two elements the rubric settles rather than leaving to the auditor

- **A branch point scores `evidence`, 0.** The rubric's own example is this bundle's
  "Choose or skip the path.", cited there as `webgl 14/LESSON.md:48` and living today at
  `lessons/minimal-gltf-loader/LESSON.md:49`. Same sentence, new address.
- **A tutor-addressed element scores `teaching`, +2, when the learner must decide or construct
  in response.** The rubric's example is this bundle's `11:32-33` "the tutor MUST explicitly ask".

### Rows a reader answers, and a script never scores — six of them

1. a `design_refs` entry that does not answer the question its lesson raises;
2. a lesson that introduces a type or concept nothing later uses;
3. **a symbol or term a lesson uses and no lesson introduces** — report the `file:line` of the
   **first use**, and keep "bound only in `DESIGN.md`" separate from "bound nowhere". A binding
   in a `DESIGN.md` anchor is loaded for the **tutor**, never for the learner, so it does not
   introduce the symbol. Appearing in `## Concepts to teach` is **not** a definition either;
4. **a lesson that does not equip the tutor to end a turn with one concrete action** — passes
   only when **both** hold: the lesson names the first concrete action (a file, a command or an
   artifact, not only the outcome), **and** the lesson keeps a design decision the learner must
   make out of the closing action. Grade the lesson **file**, never a transcript;
5. a lesson far outside the course's usual size, in either direction;
6. a must-cover topic that only an optional lesson teaches — **a question, permanently, not a
   score.**

Rows 3 and 4 are new since the 2026-09-13 audit of this bundle, which answered four.

### The invariant no structural check can reach

> A course carrying optional lessons must be completable by a learner who declines every offer.

All six rows and the invariant are answered in §6.

### None of this rejects a bundle

Every finding here is a proposal the author may refuse. `validate_bundle.py` is where a finding
stops a course from starting, and no teaching judgement belongs there. Nothing in this audit
touched the validator or the bundle.

---

## My scoring protocol, stated so it can be argued with

The rubric is explicit that a lesson's figure tracks how finely its `## Suggested progression`
enumerates clauses, so totals are comparable **inside this course** and never against another
course's. This course's house style is: `## Constraints` states rules, `## Suggested progression`
is one hard-wrapped sentence of comma-separated clauses, `## Completion conditions` enumerates
conditions. I scored:

- **P-a** every distinct clause of `## Suggested progression`;
- **P-b** every distinct condition of `## Completion conditions`. A single
  "the learner can explain / name / classify / account for / trace …" condition is **one**
  element at **+2**, however many objects it names;
- **P-c** every clause of `## Constraints`, `## Theory` or `## Prerequisites` that assigns the
  learner an act **and is not restated in the progression** — restatements are scored once, at
  the place the doing happens, so no instruction is counted twice;
- **P-d** never `## On completion, persist` (those lines are the tutor writing
  `STATE.md`/`DESIGN.md`) and never `## Optional deeper paths` (explicitly beyond the required
  path);
- **P-e** never a bare prohibition that assigns no separate act ("Do not introduce a framework");
- **P-f** the rubric's two settled elements: a branch point is 0; a tutor-addressed element is
  scored by what the **learner** does.

Within P-a, the shape rule I applied uniformly: **determine / derive / decide / construct = +2;
apply something already taught = +1; observe, verify or read output = 0.** "Inspect X" is +2 where
X must be judged (`06:41` "inspect mesh winding") and 0 where only the result is looked at
(`01:42` "inspect the result at more than one browser-window size").

**Writing renderer code is never toil in this course.** The toil row is conjunctive and renderer
code fails its first three clauses: the learner decides and constructs, and a wrong answer is
instructive on screen. The row is out before its shippability clause is reached — which matters,
because a bundle *can* ship TypeScript source, so resting the conclusion on shippability would
not survive the 2026-09-13 ruling.

---

## 1. The course and its total

| | |
|---|---|
| Bundle id | `webgl-typescript-scene` |
| Title | Learn WebGL 2 by Building a 3D Scene |
| Main-path lessons | 18 |
| Optional lessons | 1 (`lessons/minimal-gltf-loader/LESSON.md`) |
| Scored lesson rows | 19 |
| `supplies:` entries declared | **2**, both lesson-scope (was 0 on 2026-09-13) |
| Coverage list | present, 55 topics |
| `DESIGN.md` anchors | 16 |
| Confirmed toil sites | **0** (was 2) |

### Arithmetic

Main-path lesson sum, in course order:

```
+  1  00-project-setup
+ 11  01-canvas-and-context
+ 14  02-first-shader-program
+ 13  03-vertex-data
+  9  04-uniforms-and-animation
+ 12  05-transforms-and-perspective
+  9  06-depth-and-culling
+ 13  07-indexed-meshes-and-vaos
+ 15  08-textures
+ 10  09-normals-and-lighting
+ 15  10-camera-and-scene
+ 15  11-secondary-demo-scene
+ 18  12-scene-transition
+ 14  13-load-gltf-model
+ 15  15-render-to-texture
+ 18  16-bloom
+ 28  17-depth-reconstruction-and-ssr
+ 17  18-finish-the-scene
-------------------------------------
= 247  main-path lesson sum
```

Course-level penalties, each named:

```
  247  main-path lesson sum
-   0  unserved objectives                        (0 gaps x -3)
-   0  unserved DESIGN.md anchors                 (0 gaps x -3)
-   0  required_for gates on optional lessons     (0 gates x -3)
-------------------------------------
= 247  COURSE TOTAL, main path only
```

Adding the optional lesson's own figure:

```
  247  main path
+  17  minimal-gltf-loader (optional)
-------------------------------------
= 264  total across all 19 scored rows
```

**247 is the number that matters**, because it is what a learner who declines every offer earns,
and §6.7 confirms such a learner can finish the course. 264 is what a learner who accepts earns.
Neither figure may be set beside another course's total.

**There is no recoverable toil left in this course.** The two spans that cost it 4 points on
2026-09-13 are gone, and the goal-gap inventory in §3 is genuinely empty: 0 gaps listed,
0 subtracted, and §1's arithmetic agrees.

---

## 2. The per-lesson table

Mean main-path lesson: **13.7**. Middle of the distribution: 9–18.

| Lesson | Score | Objectives served | Toil found | Closing action |
|---|---:|---|---|---|
| `lessons/00-project-setup/LESSON.md` | **1** | 3 of 3 | none | pass |
| `lessons/01-canvas-and-context.md` | 11 | 4 of 4 | none | pass |
| `lessons/02-first-shader-program.md` | 14 | 4 of 4 | none | pass |
| `lessons/03-vertex-data.md` | 13 | 4 of 4 | none | pass |
| `lessons/04-uniforms-and-animation.md` | 9 | 4 of 4 | none | pass |
| `lessons/05-transforms-and-perspective.md` | 12 | 4 of 4 | none | pass |
| `lessons/06-depth-and-culling.md` | 9 | 4 of 4 | none | pass |
| `lessons/07-indexed-meshes-and-vaos.md` | 13 | 4 of 4 | none | pass |
| `lessons/08-textures.md` | 15 | 4 of 4 (obj. 4 partial: wrapping) | none | pass |
| `lessons/09-normals-and-lighting.md` | 10 | 4 of 4 | none | pass |
| `lessons/10-camera-and-scene.md` | 15 | 5 of 5 | none | pass |
| `lessons/11-secondary-demo-scene/LESSON.md` | 15 | 4 of 4 | none | pass |
| `lessons/12-scene-transition/LESSON.md` | 18 | 4 of 4 | none | pass |
| `lessons/13-load-gltf-model/LESSON.md` | 14 | 4 of 4 | none | pass |
| `lessons/15-render-to-texture.md` | 15 | 4 of 4 | none | pass |
| `lessons/16-bloom.md` | 18 | 4 of 4 | none | pass |
| `lessons/17-depth-reconstruction-and-ssr.md` | **28** | 5 of 5 | none | pass |
| `lessons/18-finish-the-scene.md` | 17 | 4 of 4 | none | **fail** — `:45` |
| `lessons/minimal-gltf-loader/LESSON.md` *(optional)* | 17 | 4 of 4 | none | pass |

The closing-action column is not a score and is never added into one. The single `fail` is carried
into §6.4 with its `file:line` and its failing sentence.

### Element breakdowns

Given for every lesson, so the table above can be re-added by a reader. `L` = line number in that
lesson file, taken from the lesson, never from the old report or from an issue.

#### `00-project-setup` — **+1** (was −1; mandatory breakdown: it is the course's lowest figure)

| L | Element (quoted) | Score |
|---|---|---:|
| 38–39 | "Read `starter/README.md` before giving the first task; it defines the supplied commands and layout." | 0 — tutor prep; the learner does nothing |
| 43 | "Install dependencies" | 0 — learner setup. No bundle can ship `node_modules`; the 2026-09-13 ruling names `npm install` as expressly unaffected |
| 43 | "inspect each supplied file" | +1 — applies the TypeScript/npm prerequisite; serves "Distinguish type checking, bundling and static serving" |
| 43 | "type-check" | 0 evidence |
| 43 | "build" | 0 evidence |
| 43–44 | "start the development server" | 0 evidence |
| 44 | "verify both page output and the absence of console errors" | 0 evidence |
| 48 | "`npm run typecheck` and `npm run build` succeed." | 0 evidence |
| 48–49 | "`npm run serve` exposes the page on its reported local URL" | 0 evidence |
| 49 | "the page shows the starter heading" | 0 evidence |
| 49 | "the console has no error" | 0 evidence |

Sum: **+1** over **eleven** elements.

**The shape of this change, not just its sign.** On 2026-09-13 this lesson had **twelve**
elements summing −1, of which one was the copy span at `:34–36` scored −2. `b969892` **deleted
that element**; nothing was re-scored. So the figure moves −1 → +1, a +2 delta, and it arrives by
one element ceasing to exist rather than by any element changing value.

I checked the tempting alternative and rejected it: **`00:43` "inspect each supplied file" stays
+1 and is not upgraded.** The files now arrive rather than being placed by the learner, but the
act is unchanged — the learner reads `package.json`, `tsconfig.json`, `index.html` and
`src/main.ts` and tells the three tools apart. That is applying the stated prerequisite, not
deciding or constructing. The word "supplied" was already in the sentence before the fix; the fix
made it literally true.

**`00:43` was never toil and still is not.** The `install` pattern fires on the whole physical
line, and the rubric names this exact line as its worked false positive. `npm install` cannot be
supplied, and the four clauses after it are the lesson.

#### `01-canvas-and-context` — 11

| L | Element (quoted) | Score |
|---|---|---:|
| 36–37 | "cap or explain the chosen device-pixel-ratio policy" | +2 — a policy the learner decides; `:47` then checks conformance |
| 41 | "Acquire the context" | +2 |
| 41 | "choose an unmistakable clear colour" | +2 — a wrong choice hides whether the clear happened |
| 41 | "resize the drawing buffer" | +1 practice |
| 41–42 | "set the viewport" | +1 practice |
| 42 | "clear" | +1 practice |
| 42 | "inspect the result at more than one browser-window size" | 0 evidence |
| 46 | "Type checking and build succeed." | 0 |
| 46–47 | "The canvas clears to the chosen colour, remains sharp after resize" | 0 |
| 47 | "its backing dimensions match the documented policy" | 0 |
| 47–48 | "a missing context produces a useful error rather than a null dereference" | +2 |

Sum: **11**. "Use `WebGL2RenderingContext` directly" (`:36`) and "Do not create shaders yet"
(`:37`) are prohibitions assigning no separate act (P-e).

#### `02-first-shader-program` — 14

| L | Element (quoted) | Score |
|---|---|---:|
| 37 | "Generate three positions from `gl_VertexID`; GPU buffers arrive next lesson." | +2 |
| 37–38 | "Check compile and link status and include diagnostic logs in thrown errors." | +2 |
| 38 | "Delete failed shader/program objects." | +1 |
| 42 | "Write and compile each shader separately" | +2 |
| 42 | "link the program" | +1 |
| 42 | "select it" | +1 |
| 42 | "issue one triangle draw" | +1 |
| 42–43 | "then deliberately break a shader briefly to observe the diagnostic path" | +2 |
| 47 | "The build succeeds and one triangle appears at predicted clip-space positions." | 0 |
| 47–48 | "Restoring a deliberate shader error restores the image" | 0 |
| 48–49 | "the learner can explain the value written to `gl_Position` and why the fragment shader needs a precision declaration." | +2 |

Sum: **14**.

#### `03-vertex-data` — 13

| L | Element (quoted) | Score |
|---|---|---:|
| 36–37 | "Make byte-based stride and offset calculations explicit." | +2 |
| 37 | "Keep the vertex format simple enough to inspect manually." | +1 |
| 41 | "Upload positions" | +2 |
| 41 | "connect the position attribute" | +2 |
| 41–42 | "then add colour data and pass it between shader stages" | +2 |
| 42 | "Change one layout parameter intentionally and reason from the corrupted image." | +2 |
| 46 | "The buffered triangle renders with an interpolated colour gradient." | 0 |
| 46 | "Build and type check pass" | 0 |
| 47 | "the learner can account for every attribute-layout argument in bytes" | +2 |

Sum: **13**. "Use at least position and colour attributes" (`:36`) is restated by the progression
and scored there (P-c).

#### `04-uniforms-and-animation` — 9

| L | Element (quoted) | Score |
|---|---|---:|
| 37–38 | "Handle a missing required uniform location explicitly." | +2 |
| 42 | "Add a scalar uniform" | +2 |
| 42 | "make it affect the shader" | +1 practice |
| 42 | "introduce the frame callback" | +2 |
| 42–43 | "verify that refreshing or resizing does not create multiple loops" | 0 evidence |
| 47–48 | "The animation is time-based, continues smoothly at varying refresh rates, and draws from one intentional loop." | 0 |
| 48 | "Build and type check pass." | 0 |
| 48–49 | "The learner can classify current data as per-vertex, per-draw or per-frame." | +2 |

Sum: **9**.

#### `05-transforms-and-perspective` — 12

| L | Element (quoted) | Score |
|---|---|---:|
| 36–37 | "Send matrices through uniforms" | +1 practice — uniforms taught in `04` |
| 37 | "preserve the convention in `DESIGN.md`" | +2 — honouring `#matrix-convention` is a real act with an instructive failure |
| 37 | "Render 3D geometry even though occlusion is not correct yet." | 0 — sequencing |
| 41 | "Create a cube or other simple volume" | +2 |
| 41 | "add model then view then projection transforms" | +2 |
| 41–42 | "predict the result of changing each" | +2 |
| 42 | "update aspect ratio after canvas resize" | +1 practice |
| 46 | "A rotating 3D object is visible with plausible perspective and correct aspect ratio." | 0 |
| 46–47 | "The learner can trace a sample vertex through the named spaces and explain near-plane clipping qualitatively." | +2 |

Sum: **12**. See §7 for why this is 1 below the old report's 13.

#### `06-depth-and-culling` — 9

| L | Element (quoted) | Score |
|---|---|---:|
| 35 | "Clear depth on every frame." | +1 practice |
| 40 | "Capture the incorrect overlap" | +2 — the learner must construct the failure before the fix |
| 40 | "enable depth testing" | +1 |
| 40–41 | "rotate through several views" | 0 evidence |
| 41 | "inspect mesh winding" | +2 — the winding must be determined, not merely looked at |
| 41 | "then enable and toggle back-face culling" | +1 |
| 45–46 | "Faces occlude correctly from multiple angles and no required face disappears under the chosen culling state." | 0 |
| 46 | "The learner can name the colour and depth buffers cleared each frame." | +2 |

Sum: **9**. `:35–36` "Enable culling only after triangle winding is known to be consistent" is the
ordering the progression already performs ("inspect mesh winding, then enable … culling"), so
under P-c it is scored once, at the progression. See §7.

#### `07-indexed-meshes-and-vaos` — 13

| L | Element (quoted) | Score |
|---|---|---:|
| 38–39 | "Validate array lengths and supported index types before upload." | +2 |
| 43 | "Convert the procedural object to indices" | +2 |
| 43 | "bind its element buffer in a VAO" | +2 |
| 43 | "define `MeshData`" | +2 — `DESIGN.md:33` defers the concrete shape to exactly here |
| 43–44 | "write one upload path and one draw path" | +2 |
| 44 | "then ensure temporary resources can be deleted" | +1 |
| 48 | "The procedural object renders through an indexed VAO-backed mesh." | 0 |
| 48–49 | "Its CPU and GPU forms have distinct types or clearly distinct responsibilities" | 0 |
| 49 | "invalid attribute lengths are rejected" | 0 |
| 49–50 | "the learner can explain what state the VAO does and does not capture" | +2 |

Sum: **13**.

#### `08-textures` — 15

| L | Element (quoted) | Score |
|---|---|---:|
| 36 | "Use a tiny generated or packaged learning texture before the model asset." | +1 |
| 36–37 | "Make the vertical orientation decision explicit." | +2 |
| 37 | "Keep rendering valid while an image is still loading." | +2 |
| 41 | "Render UVs as colours" | +2 |
| 41 | "upload a labelled image" | +1 |
| 41 | "bind it through a sampler" | +1 |
| 41 | "test orientation" | 0 evidence |
| 42 | "then compare nearest and linear filtering" | +2 |
| 42 | "and enable a valid mipmap policy" | +2 |
| 46 | "The textured object has predictable orientation" | 0 |
| 46 | "remains renderable during load" | 0 |
| 46–47 | "shows an observable filtering difference under scale" | 0 |
| 47–48 | "The learner can trace a texture sample from vertex attribute to fragment colour." | +2 |

Sum: **15**. **No element exercises texture wrapping** — see §3 and §6.2.

#### `09-normals-and-lighting` — 10

| L | Element (quoted) | Score |
|---|---|---:|
| 36 | "Calculate required lighting in world space." | +1 — the space is mandated by `#lighting-model`, so this is compliance, not a choice |
| 41 | "Visualise normals as colour" | +2 |
| 41 | "add the light vector and diffuse term" | +2 |
| 41 | "combine with texture colour" | +1 practice |
| 42 | "rotate the model" | 0 evidence |
| 42 | "then test a non-uniform scale to expose incorrect normal transformation" | +2 |
| 46–47 | "Illumination changes predictably as object or light rotates" | 0 |
| 47 | "back-facing surfaces receive only ambient light" | 0 |
| 47 | "non-uniform scale does not visibly corrupt the lighting" | 0 |
| 47–48 | "The learner can explain the spaces used by every vector in the dot product." | +2 |

Sum: **10**.

#### `10-camera-and-scene` — 15

| L | Element (quoted) | Score |
|---|---|---:|
| 40–41 | "Store only stable per-instance data in its buffer; calculate time-varying wave displacement in the shader." | +2 — a real partition decision |
| 43 | "Keep lighting and texture behaviour from the preceding lessons visible." | +1 |
| 47 | "Extract camera state" | +2 |
| 47 | "render a small fixed set of instances" | +1 |
| 47–48 | "move placement into a divisor-backed instance attribute" | +2 |
| 48 | "expand to a grid" | +1 |
| 48 | "derive vertical displacement from time and grid position" | +2 |
| 48–49 | "add crest-dependent colour or brightness" | +2 |
| 49 | "orbit the camera" | +2 — carries the `:41–42` automatic/interactive/both choice |
| 49 | "and verify resize behaviour" | 0 |
| 53–56 | seven completion conditions, all output checks | 0 each |

Sum: **15**.

#### `11-secondary-demo-scene` — 15 (the rubric's tutor-addressed example)

| L | Element (quoted) | Score |
|---|---|---:|
| 31–32 | "Before asking the learner to choose, read `effect-menu.md`. Present the effects grouped and sorted by its difficulty levels…" | 0 — tutor prep |
| **32–33** | **"The tutor MUST explicitly ask which effect the learner wants to build. Do not silently choose for them."** | **+2 teaching** — the rubric's own named example; tutor-addressed, learner decides |
| 33–34 | "They may propose another effect; assess it against the same scale before accepting or narrowing it." | +1 |
| 44–45 | "Preserve the first scene unchanged." | +1 |
| 45–46 | "Both scenes must implement the lifecycle in `#demo-scene-contract`, own their GPU resources and render correctly when invoked independently." | +2 |
| 48 | "For Level 3 or 4 choices, establish one diagnostic visualisation before the final look." | +2 |
| 48–50 | "For “Technokartoffeln”, the tutor may and should use that name alongside “3D metaballs” for fun…" | 0 — tone; the learner does nothing |
| 54 | "Present the sorted catalogue" | 0 |
| 54 | "ask for the learner's selection and desired visual mood" | +1 — the effect choice itself is scored once, at `:32–33` |
| 54–55 | "agree a bounded definition of done" | +2 |
| 55–56 | "adapt the cube-wave scene to it without visual changes" | +2 |
| 56 | "build the selected effect from its core mechanism outward" | +2 |
| 56–57 | "then verify independent resize, pause and disposal behaviour" | 0 |
| 61–64 | six completion conditions, all record/output checks | 0 each |

Sum: **15**. `:55` "define the minimal shared scene lifecycle" is the progression's realisation of
the `:45–46` constraint and is scored once, there.

**This figure understates the lesson.** `effect-menu.md` authors twelve effects, each with a
technique, a completion target, a scope warning and an enhancement, plus a four-level assessment
scale for learner proposals. The ruler counts clauses in the lesson, so an authored catalogue the
learner meets one entry of is invisible to it. The same is true of `12`'s `transition-menu.md`.

#### `12-scene-transition` — 18

| L | Element (quoted) | Score |
|---|---|---:|
| 30–31 | "Before selecting the characteristic transition, read `transition-menu.md` and ask the learner which style fits their two scenes." | +2 — tutor-addressed, learner decides |
| 40–41 | "At progress zero the output must equal the first scene; at one it must equal the second." | +2 |
| 41 | "Neither scene may manipulate the other's internal resources." | +1 |
| 41–42 | "The transition owns its targets and resizes and disposes them explicitly." | +2 |
| 42 | "Keep a crossfade mode after the selected transition works." | +1 |
| 46 | "Render each scene to its own target" | +2 |
| 46 | "display each directly" | +1 |
| 46 | "implement crossfade with manual progress" | +2 |
| 47 | "add time-based direction and easing" | +2 |
| 47–48 | "then implement and validate the selected transition at endpoints and intermediate values" | +2 |
| 52 | "Each scene and render target can be displayed independently." | 0 |
| 52–54 | "Crossfade and one learner-selected transition work in both directions, preserve exact endpoints, respond correctly after resize and do not leak resources." | 0 |
| 54 | "Scene update/freeze behaviour during transitions is documented." | +1 — `#scene-transition` leaves the freeze policy to the learner |

Sum: **18**. `:47` "present `transition-menu.md`, ask for a choice" is the same instruction as
`:30–31` and is scored once, at `:30–31`.

#### `13-load-gltf-model` — **14** (was 12; the second fix)

| L | Element (quoted) | Score |
|---|---|---:|
| 43–44 | "Read `models/ATTRIBUTION.md` when introducing the asset, and retain all four supplied files together." | 0 — tutor-addressed reading plus a retention obligation; no learner construction. **Deliberately kept, and it is what keeps `#packaged-model` served** |
| 46 | "Use `@gltf-transform/core` only for asset parsing and traversal, never for rendering." | +1 |
| 46–47 | "Support the packaged model first." | 0 — sequencing |
| 47 | "Reject missing required attributes with useful errors." | +2 |
| 47–48 | "Do not expose library types to the renderer or attempt complete glTF feature support." | +1 |
| 52 | "Fetch and parse `models/Duck.glb`" | +2 |
| 52 | "inspect its scene and first mesh primitive" | +2 |
| 52–53 | "adapt accessors to `MeshData`" | +2 |
| 53 | "handle its base-colour texture" | +2 |
| 53 | "upload through the established mesh path" | +1 practice |
| 53–54 | "then place the duck as a normal scene object" | +1 practice |
| 58–61 | five completion conditions, all output/validator checks | 0 each |

Sum: **14** over **sixteen** elements. On 2026-09-13 there were seventeen, summing 12, of which
one was the copy span at `:39–40` scored −2. `221c164` deleted that element. Nothing was
re-scored; the delta is +2 and it is the deletion. The old report predicted exactly this figure.

#### `15-render-to-texture` — 15

| L | Element (quoted) | Score |
|---|---|---:|
| 38 | "Build on the two-scene render-target work without replacing its transition boundary." | +1 |
| 39 | "Preserve the existing scene shaders." | +1 |
| 39 | "Use one scene colour texture and one sampleable depth texture." | +2 — the depth texture is new here |
| 40 | "Never sample an attachment while writing to it." | +2 |
| 40–41 | "Restore or explicitly set framebuffer and viewport state for every pass." | +2 |
| 45 | "Allocate attachments" | +1 practice — `12` already allocated colour targets |
| 45 | "check completeness" | +1 practice — `12:35` lists framebuffer completeness in its own Concepts |
| 45 | "render the scene off-screen" | +1 practice |
| 45–46 | "display its colour through a full-screen triangle" | +1 practice — `12` already composed scene textures in a full-screen pass |
| 46 | "expose the depth texture as a diagnostic view" | +2 — new |
| 46–47 | "then integrate resize and cleanup" | +1 practice — `12:41–42` already required explicit resize and disposal |
| 51–53 | four completion conditions, all output checks | 0 each |

Sum: **15**. `:41` "Provide a direct-copy composition shader before adding effects" is restated by
`:45–46` and scored there. The scoring makes a real structural fact visible: **lesson `12` teaches
framebuffers, completeness and full-screen triangles before lesson `15` does.** Raised in §5 as a
question, not a defect.

#### `16-bloom` — 18

| L | Element (quoted) | Score |
|---|---|---:|
| 37 | "Use an explicitly supported floating-point colour format and check required capabilities." | +2 |
| 38 | "Keep blur targets at a documented resolution." | +1 |
| 38–39 | "Let the learner view the bright pass, each blur direction and final composition independently." | +2 |
| 39 | "Bloom must be toggleable." | +1 |
| 43 | "Introduce emissive/bright scene values" | +2 |
| 43–44 | "extract bright regions" | +2 |
| 44 | "implement one blur direction" | +2 |
| 44–45 | "ping-pong the second direction for a small fixed number of iterations" | +2 |
| 45 | "then additively compose and tune threshold/intensity" | +2 |
| 49 | "Only intended bright surfaces seed bloom" | 0 |
| 49–50 | "diagnostic pass views show the expected intermediate images" | 0 |
| 50 | "toggling bloom preserves the base scene" | 0 |
| 50–51 | "resize and repeated frames do not leak resources" | 0 |
| 51 | "the learner can explain why ordinary clamped colour prevents useful thresholding" | +2 |

Sum: **18**. `:43` "validate the HDR target" is the same act as the `:37` constraint and is scored
once, at `:37`. See §7 for the +1 against the old report.

#### `17-depth-reconstruction-and-ssr` — **28** (outlier: 2.0x the mean)

| L | Element (quoted) | Score |
|---|---|---:|
| 42 | "Perform reconstruction and ray comparisons in one documented coordinate space." | +2 |
| 42–43 | "Add a view-space normal attachment with a defined encoding." | +2 — the encoding is the decision |
| 44 | "Bound loop iterations for WebGL shader compilation and performance." | +2 |
| 44–45 | "Expose step count, thickness and maximum distance as controlled parameters." | +2 |
| 45–46 | "SSR must be toggleable and must fade rather than smear invalid/off-screen hits." | +2 |
| 50 | "Add and inspect the normal target" | +1 practice — the decision is already scored at `:42–43` |
| 50 | "reconstruct and visualise linear/view-space depth" | +2 |
| 50–51 | "reconstruct positions" | +2 |
| 51 | "verify them by camera motion" | 0 evidence |
| 51 | "derive the reflection ray" | +2 |
| 51 | "display projected ray steps" | +2 |
| 52 | "add depth-crossing detection" | +2 |
| 52 | "refine the first hit locally" | +2 |
| 52 | "sample reflected colour" | +1 practice |
| 52–53 | "then add edge, distance and grazing-angle fades" | +2 |
| 57 | "The reconstruction diagnostic remains spatially coherent under camera movement and resize." | 0 |
| 57–58 | "A reflective procedural surface shows plausible reflections of visible scene content." | 0 |
| 58–59 | "Off-screen and missing hits fade safely" | 0 |
| 59 | "bounded marching cannot hang the shader" | 0 |
| 59–60 | "SSR can be disabled without changing the base scene" | 0 |
| 60 | "the learner can explain at least four failure modes inherent to SSR." | +2 |

Sum: **28**. `:43–44` "Begin with a reconstruction diagnostic that visualises position or linear
depth" is restated by `:50` and scored there. Raised as an oversize lesson in §6.5.

#### `18-finish-the-scene` — 17

| L | Element (quoted) | Score |
|---|---|---:|
| 37–38 | "The final demo must retain both independently renderable scenes and their transition." | +1 |
| 38–40 | "The lit 3D scene must include the packaged duck and at least one reflective procedural mesh, a controllable camera, perspective, depth testing, textured surfaces, ambient plus directional lighting, bloom and SSR." | +2 |
| 40–41 | "Bloom and SSR must be independently toggleable and expose diagnostic intermediate views." | +1 |
| 41 | "Retain model attribution and licences." | +1 — a real act, and one of the servers of `#packaged-model` |
| 45 | "Choose a composition that makes reflections and bloom readable" | +2 — **and the closing-action failure; see §6.4** |
| 45 | "integrate asynchronous loading" | +1 |
| 46 | "tune camera and lighting" | +1 |
| 46 | "tune effects without hiding their artefacts" | +2 |
| 46–47 | "test resize and extreme camera positions" | 0 |
| 47 | "audit allocations/state transitions" | +2 |
| 47–48 | "then perform deliberate geometry-pass and post-processing failure investigations" | +2 |
| 52–57 | ten completion conditions, all output/state checks | 0 each |
| 57 | "The learner can explain the end-to-end pipeline and isolate failures by pass." | +2 |

Sum: **17**.

#### `minimal-gltf-loader` (optional) — 17 (contains the rubric's branch-point example)

| L | Element (quoted) | Score |
|---|---|---:|
| 32–33 | "For the exact supported subset and the cases that must be rejected, read `supported-subset.md` before proposing implementation tasks." | 0 — tutor prep |
| 42 | "The learner may skip this lesson without implementing anything; record that choice and advance." | 0 — the offer |
| 43–44 | "If taken, keep the library adapter available until the new decoder produces equivalent visible output." | +2 |
| 44 | "Implement only `supported-subset.md`, reject everything else clearly" | +2 |
| 44–45 | "and return the same `MeshData` boundary." | +1 |
| **49** | **"Choose or skip the path."** | **0 — branch point**, per the rubric's settled ruling. The rubric cites this element at `webgl 14/LESSON.md:48`; it lives today at `lessons/minimal-gltf-loader/LESSON.md:49` |
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

---

## 3. Goal gaps

**None. Zero unserved learning objectives, zero unserved `DESIGN.md` anchors, zero unserved
coverage-list topics. Course-level gap penalty: 0 x −3 = 0.** This agrees with §1's arithmetic:
0 gaps listed, 0 subtracted.

That is an unusual finding, so here is how each class was decided.

### The 16 `DESIGN.md` anchors — decided by what lessons make the learner DO, never by `design_refs`

| Anchor | Served by (what the learner does) |
|---|---|
| `#platform-toolchain` | `00:43` inspects each supplied file, type-checks, builds and serves the plain HTML/esbuild/`tsc` shell; `00:38` refuses a framework. **Changed since 2026-09-13** — "copies" has dropped out of this list and the anchor is unaffected, because it describes the *platform*, not the act of assembling it |
| `#api-boundary` | `01:36` "Use `WebGL2RenderingContext` directly"; `02:37–38` requires helpers that expose diagnostics rather than conceal them; `03`, `07` throughout |
| `#matrix-convention` | `05:37` "preserve the convention in `DESIGN.md`"; `05:46–47` "trace a sample vertex through the named spaces"; `17:42` "one documented coordinate space" |
| `#shader-convention` | `02` GLSL ES 3.00 with `in`/`out`, compile/link status checked immediately, failure stops construction (`:37–38`); `03:36–37` explicit attribute layout |
| `#mesh-boundary` | `07:43` "define `MeshData`"; `13:52–53` "adapt accessors to `MeshData`"; `minimal-gltf-loader:44–45` returns the same boundary |
| `#resource-ownership` | `02:38`, `07:44`, `12:41–42`, `15:46–47`, `16:50–51` — five lessons delete or recreate what they own |
| `#scene-boundary` | `10:47` "Extract camera state"; `10:40–43` sets frame-wide then per-object state |
| `#first-demo-scene` | `10` entire: one instanced cube mesh, sine-wave displacement from time and grid position, bright crests, orbit camera |
| `#demo-scene-contract` | `11:45–46` both scenes implement the shared lifecycle; `11:55` defines its concrete form |
| `#scene-transition` | `12` entire: both scenes to separate targets, full-screen composition, exact endpoints, documented freeze policy at `:54` |
| `#lighting-model` | `09:36` ambient + one directional Lambertian term computed in world space; `09:37` excludes specular/PBR |
| `#texture-convention` | `08:36–37` "Make the vertical orientation decision explicit"; `08:41` "test orientation" |
| `#asset-loading-paths` | `13` (required library path) and `minimal-gltf-loader` (optional direct path), both returning the same `MeshData` |
| `#post-processing-pipeline` | `15`, `16`, `17`, `18` — off-screen pass, bloom, depth-reconstructing SSR, every pass toggleable and independently viewable |
| **`#packaged-model`** | **Still served after the copy instruction was removed — see the dedicated check below** |
| `#unresolved-decisions` | `07:54`, `10:60–61`, `11:68–70`, `12:58–59`, `16:55`, `17:64–65` — six lessons record learner decisions under new stable anchors. **Cited by no `design_refs` entry at all**, and served all the same. This is the rubric's own warning about the citation proxy, reproduced exactly in this course |

### `#packaged-model` after the fix — the check this run existed to make

`DESIGN.md:109–114` says the course packages the Khronos "Duck" GLB, states the SCEA and CC BY 4.0
terms, and requires that "The original licence and attribution material travels with the model
lesson and must be copied into the learner workspace with the asset."

On 2026-09-13 the anchor's principal service was the copy instruction at `13:39–40`, and the old
report flagged — correctly — that removing it would leave the anchor thin. **It did not.** The
anchor is served today by five things, four of which are acts:

1. `lessons/13-load-gltf-model/LESSON.md:6–9` — the lesson-scope `supplies` entry places
   `Duck.glb`, `LICENSE.md`, `SCEA.txt` and `ATTRIBUTION.md` into `models/` when the lesson opens.
   This is the bundle *performing* what the anchor requires rather than assigning it.
2. `13:43–44` — "Read `models/ATTRIBUTION.md` when introducing the asset, and retain all four
   supplied files together." The retention obligation is a standing act on the learner, and the
   author strengthened the wording to "all four **supplied** files" in `221c164`.
3. `13:58` — the completion condition "The model and all licence files exist under `models/`."
4. `18:41` — "Retain model attribution and licences." (+1 in §2), and `18:56–57` "licence files
   remain with the model."
5. `13:66` — the persist line "Record the model attribution in the project documentation."
   (not scored as an element, per P-d, but it is a real obligation.)

**Verdict: `#packaged-model` is served. The course does not pay −3.** This is also the case the
rubric's own consistency clause anticipates: *a bundle cannot be charged −2 for assigning a step
and −3 for supplying it.* The old report's proposal P3 — add a clause to lesson 18 restoring the
anchor's service — is **no longer needed**, because `18:41` and `18:56–57` were already there and
`13:43–44` survived the edit on purpose.

### The two `supplies` entries would actually place their files

Checked rather than assumed, because a lesson-scope entry whose `from` is outside that lesson's
own folder produces files that are not there when the lesson opens:

| Entry | `from` | Inside its own lesson folder? | `to` | Validator it satisfies |
|---|---|---|---|---|
| `00-project-setup` (`LESSON.md:6–9`) | `lessons/00-project-setup/starter/` | yes | `.` | `has-index` (`index.html`), `has-entrypoint` (`src/main.ts`) |
| `13-load-gltf-model` (`LESSON.md:6–9`) | `lessons/13-load-gltf-model/model/` | yes | `models` | `has-model` (`models/Duck.glb`) |

Both `from` paths sit under `lessons/<that lesson's folder>/`, both lesson keys match the `id` in
the same frontmatter, and materialization copies `lessons/` into the instance, so the runner
places each set when its lesson opens. The starter directory on disk holds exactly
`index.html`, `package.json`, `package-lock.json`, `tsconfig.json`, `README.md` and `src/main.ts`;
the model directory holds exactly the four named files.

**One consequence worth the author's attention, raised in §5 as Q3:** `to: .` also places
`starter/README.md` at the workspace root as `README.md`. Its text was correctly rewritten in
`b969892` — `starter/README.md:3` now reads "These files are placed in your repository when this
lesson opens. You do not copy them." — so it no longer contradicts the lesson. But `README.md` is
in neither `learner_owned` (`tutorial.yaml:42`) nor `tutor_owned` (`:41`), so a file arrives in the
workspace that the ownership policy does not cover.

### The 55 coverage-list topics

Every one is exercised by a main-path lesson. The four that word overlap would have got wrong:

- **"primitive assembly"** (`COURSE.md:79`) — no lesson uses the phrase in a task. Served by
  `02:42` "issue one triangle draw" (mode and vertex count with no buffer) and decisively by
  `07:43` "Convert the procedural object to indices", which is exactly the
  vertex-record-versus-topology distinction.
- **"homogeneous coordinates"** (`:87`) — served by `02:25–26` (the `w` binding), `05:20`'s
  objective on the role of `w`, and `05:46–47` "trace a sample vertex through the named spaces".
- **"multiple render targets"** (`:114`) — appears in a task nowhere, and in `16:32` only as an
  alternative ("multiple render targets or extraction passes"). Served by `17:15–16` "The
  off-screen pass must provide depth and a world- or view-space normal texture" and `17:42–43`
  "Add a view-space normal attachment with a defined encoding": adding a second colour attachment
  to the existing scene framebuffer *is* MRT. No lesson names `gl.drawBuffers`. Served, but by
  inference — see §5, Q5.
- **"WebGL state"** (`:81`) — served by `01` (state-machine model), `06` (depth and cull state),
  `15:40–41` and `18:47`.

### Two partial topics — listed, **not** penalised, and the reasoning is open to argument

The rubric penalises a stated item "that no task exercises". These two are exercised in part, so
levying −3 would be over-reading and leaving them unlisted would be under-reporting. Unchanged
from 2026-09-13; neither fix touched lesson 08.

- **`COURSE.md:95` "texture filtering and wrapping"** and **`08:21` "Explain wrapping, filtering,
  mipmaps and image orientation".** Filtering is exercised (`08:42` "compare nearest and linear
  filtering"), mipmaps are (`08:42` "enable a valid mipmap policy"), orientation is (`08:41`
  "test orientation"). **Wrapping is exercised nowhere.** It appears only in the objective at
  `08:21` and in Concepts at `08:32`. No progression clause and no completion condition touches
  `TEXTURE_WRAP_S`/`_T`.
- **`COURSE.md:96` "mipmaps and power-of-two considerations".** Mipmaps are exercised;
  "power-of-two considerations" appear in no lesson at all — unsurprising, since WebGL 2 lifted the
  NPOT mipmap restriction that made the phrase matter in WebGL 1.

A stricter reader could levy −3 each, taking the course to 241 main-path / 258 overall. I did not.
The choice is visible so the author can overrule it, and §5 proposes repairs that close both.

### Every per-lesson objective is served

I walked all 73 stated `learning_objectives` across the 19 lessons against that lesson's own tasks.
All are served except the wrapping fragment above. Two checks specific to this run:

- **Lesson 00's three objectives survive the deletion of the copy instruction.**
  "Distinguish type checking, bundling and static serving" — `00:43` inspect/type-check/build/serve
  plus Theory `:28–30`. "Run a TypeScript entry point in a plain HTML page" — `:43–44` build and
  serve, `:49` "the page shows the starter heading". "Use the console and page as separate sources
  of evidence" — `:44` and `:49`. **None of the three was served by the copy**, which is why the
  toil exception never applied to this lesson and why removing the step strands nothing.
- **Lesson 13's four objectives survive too**, and none of them names licences or attribution —
  that objective was removed in `49af681` before this run, leaving the licence *work* as a
  constraint, a completion condition, a validator and two obligations in lesson 18. So removing the
  copy instruction cost no objective either.

---

## 4. The toil inventory

### **Zero confirmed toil sites. The count was 2 on 2026-09-13 — the catalogue's last two — and both are closed.**

Both were the same defect and both had the same repair: the bundle shipped nine files destined for
the learner's workspace and declared no `supplies:` entry for any of them. `tutorail-bundles#6`
declared both sets and deleted both instructions.

### Closed since 2026-09-13

**1. `lessons/00-project-setup/LESSON.md:34` (sentence spanned lines 34–36)** — the sentence that
was scored −2 read:

> "Copy `starter/package.json`, `starter/package-lock.json`, `starter/tsconfig.json`,
> `starter/index.html` and `starter/src/main.ts` into their corresponding repository-root paths,
> preserving `src/`."

**Gone in `b969892`.** In its place, `LESSON.md:6–9` declares the whole `starter/` directory to
`.` at lesson scope. Verified by reading the file: the current `## Constraints` block at `:38–39`
contains no copy instruction, and `grep -rniP '\b(copy|copies|scaffold|skeleton|npm init|git init|duplicate)\b'`
over `COURSE.md`, `DESIGN.md` and every lesson returns no assignment of a copy to the learner —
only `15:41` "direct-copy composition shader", `18:62` and `00:53` "Do not copy … into state or
design notes", `starter/README.md:3` "You do not copy them", and the SCEA licence text.

**2. `lessons/13-load-gltf-model/LESSON.md:39` (sentence spanned lines 39–40)** — the sentence that
was scored −2 read:

> "Before starting, copy every file under `model/` to a repository-root `models/` directory:
> `Duck.glb`, `LICENSE.md`, `SCEA.txt` and `ATTRIBUTION.md`."

**Gone in `221c164`.** In its place, `LESSON.md:6–9` declares `model/` to `models` at lesson scope.
The following clause was deliberately kept and is now a sentence in its own right at `:43–44`:

> "Read `models/ATTRIBUTION.md` when introducing the asset, and retain all four supplied files
> together."

That clause is not toil — it is a licence obligation — and it is load-bearing for
`#packaged-model`, as §3 sets out.

### Examined and rejected — recorded so the next reader does not re-litigate them

- **`lessons/00-project-setup/LESSON.md:43`**, the scanner's only candidate this run. The `install`
  pattern fired. The physical line ends mid-clause at "development"; the sentence is:

  > "Install dependencies, inspect each supplied file, type-check, build, start the development
  > server, and verify both page output and the absence of console errors."

  **Rejected, on the rubric's stated ground: no bundle can ship `node_modules`.** There is no
  `supplies:` entry to write, because the result comes off a package registry. This is the
  learner's setup and it is scored as what it actually is — `install` 0, `inspect` +1, the rest
  evidence at 0. The rubric names this exact line as its worked false positive and names
  `npm install` as expressly unaffected by the 2026-09-13 skeleton ruling. **Not reopening it.**

- **The project skeleton, re-checked against the 2026-09-13 ruling.** The ruling is that where the
  shippability test and the toolchain test disagree, a project skeleton is toil. **They never
  disagreed here**: this course's skeleton always sat in the bundle as `starter/` files, so the
  plain shippability test answered yes on its own and the tiebreak never fired. The ruling's own
  table records that. What changed on 2026-09-13→15 is that the bundle now *supplies* the files
  instead of assigning the move, so there is no step left to charge.

- **The toil exception does not apply to lesson 00**, checked in its full operational form. The
  exception fires only when the setup step is the **only** element serving an objective that names
  the setup. Lesson 00's three objectives (`:22–24`) are "Distinguish type checking, bundling and
  static serving", "Run a TypeScript entry point in a plain HTML page" and "Use the console and
  page as separate sources of evidence" — **none names creating or assembling the project** — and
  `#platform-toolchain` describes the target platform and tools, not the act. So the −2 was correct
  on 2026-09-13 and the removal is the right repair rather than an exception being claimed.

- **No step in this course is handed to the tutor**, so the "a step the tutor performs is not an
  element" route is not in play. `tutorial.yaml:43` sets
  `ownership_policy: tutor-must-not-edit-learner-owned`, not `on-request`, and no lesson has the
  tutor generate anything for the learner. The work here moved to *supplied files*, which is the
  other legitimate route and the one this bundle could take because its file set is closed.

- **Renderer code is not toil.** `15:45` "Allocate attachments", `16:43` "validate the HDR target"
  and every sibling: each is a decision the learner makes and a mistake that shows on screen, so
  the toil row is already out at its first three clauses and its shippability clause is never
  reached. `COURSE.md:24` ("The learner writes the renderer") and `#api-boundary` make this the
  subject of the course. **Not** rejected on the ground that the bundle could not ship the files —
  it could, and per the 2026-09-13 ruling that would not have saved them.

- **`11:31–32` and `12:30–31`**, the instructions to read `effect-menu.md` and
  `transition-menu.md` — the tutor reads them; no file is moved and no learner act is assigned.

- Every `npm run typecheck` / `npm run build` / `npm run serve` instruction — evidence, 0.

**The scanner is a candidate generator over a fixed verb list, and an empty candidate list is not a
pass.** This inventory came from reading all nineteen lessons, `COURSE.md` and `DESIGN.md`, not
from the scanner, which produced exactly one candidate this run and it was the known false
positive. The toil surface of this bundle was always its two shipped file sets, because `starter/`
and `model/` are the only bundle files ever destined for the learner's workspace — and both are
now declared.

---

## 5. Proposals

Each names a concrete action. All are proposals; applying any of them is the `tutorail-authoring`
skill's job, not this one's. Nothing in the bundle was changed here.

**The 2026-09-13 report's P1, P2 and P3 are closed and are not repeated.** P1 and P2 were applied
as `b969892` and `221c164`. P3 (restore `#packaged-model`'s service after P2) proved unnecessary:
`13:43–44`, `13:58`, `18:41` and `18:56–57` already serve it, as §3 shows. The numbering below is
fresh for this run; the old number is given where one exists.

### P1 — Give lesson 18 a closing action the tutor can actually use (was not in the old report)

`lessons/18-finish-the-scene.md:45` opens the progression with a decision:

> "Choose a composition that makes reflections and bloom readable, …"

This is the only closing-action failure in the course (§6.4). Two repairs, either of which works:

- **Mark the decision and give it its own place**, the way `11:32–33` and `12:30–31` already do in
  this bundle. Move the composition choice into `## Constraints` as an explicit decision the tutor
  raises and settles ("Before the first task, agree with the learner which two or three subjects
  the final composition foregrounds"), and start the progression with an action —
  "Place the duck and the reflective mesh in the agreed composition" names an artifact.
- **Or** name the concrete first artifact inside the existing clause: "Choose a composition …, and
  write it down as a short shot list in the instance design before changing any code."

Lesson `18` is the last lesson in the course, so a turn that ends in an open question here is the
last thing the learner experiences.

### P2 — Close the wrapping gap in lesson 08 (old P4)

Add to `lessons/08-textures.md:41–42`, after "test orientation": "set `TEXTURE_WRAP_S`/`_T` and
compare `REPEAT` with `CLAMP_TO_EDGE` on UVs deliberately pushed outside 0–1". It is a genuine
decision with an instructive wrong answer, it serves the existing objective at `08:21` verbatim,
it serves `COURSE.md:95` in full, and it adds +2. Optionally mirror it in the completion
conditions at `08:46`. **Unchanged and still open** — neither fix touched lesson 08.

### P3 — Decide "power-of-two considerations" one way or the other (old P5)

Two acceptable outcomes, and I argue for the second:

1. Add a clause to lesson 08 exercising NPOT behaviour; or
2. **Drop "power-of-two considerations" from `COURSE.md:96`**, leaving "mipmaps". WebGL 2 removed
   the NPOT mipmap and wrapping restrictions, so the phrase describes a WebGL 1 constraint that the
   course's own stated target (`DESIGN.md:5`, "a modern desktop browser with WebGL 2") does not
   face. `COURSE.md:126–133` already declines things that belong to other courses; this belongs
   with them.

### P4 — Name `gl.drawBuffers` where MRT is actually required (old P6)

`COURSE.md:114` promises "multiple render targets". The learner does it at `17:42–43` without the
lesson ever saying so, and `16:32` offers "multiple render targets **or** extraction passes", which
reads as permission to avoid it. Add the API to `lessons/17-depth-reconstruction-and-ssr.md`
Concepts (`:36–38`) and one clause to its Constraints at `:42–43`: "write colour and normal from
one pass with `gl.drawBuffers`". Closes the inference and makes a must-cover topic unmissable.

### P5 — Fix the residual "lesson 14" reference (old P7, still open)

`COURSE.md:137` still reads:

> "`minimal-gltf-loader` is an optional lesson, offered while you are in lesson 14."

`tutorial.yaml:34` offers it at `lessons/13-load-gltf-model/LESSON.md`. The sentence is right by
`COURSE.md`'s own 1-based chapter map (chapter 14 *is* the glTF lesson at `:48`) and wrong by every
lesson id and prerequisite line in the bundle, which use the 0-based file numbering. Replace the
bare number: "offered while you are in the glTF model lesson (`13-load-gltf-model`, chapter 14
above)".

Related, and still true: the two numbering schemes no longer differ by a constant. Chapters 1–14
map to files `00`–`13` (offset +1); chapters 15–18 map to files `15`–`18` (offset 0); the missing
`14` absorbs the difference. Any future bare chapter number in prose is a trap. Either renumber the
post-14 files, or state the mapping once in `COURSE.md` and never write a bare lesson number again.

### P6 — Define "thickness" where lesson 17 first asks the learner to expose it (new)

`lessons/17-depth-reconstruction-and-ssr.md:44–45` reads "Expose step count, thickness and maximum
distance as controlled parameters", and no lesson says what thickness *is* in a screen-space
reflection. `17:37` lists "thickness bias" in `## Concepts to teach` and `DESIGN.md:106` names it
in a list of policies; neither is a binding sentence, and a `DESIGN.md` anchor is loaded for the
tutor, not for the learner. Add one clause to `17`'s `## Theory` at `:28–32`, e.g. "a hit is
accepted when the marched sample lies within a *thickness* — an assumed depth extent for the
surface behind each pixel, because a depth buffer records only a front surface". See §6.3.

### P7 — Decide where `starter/README.md` lives once it is supplied (new)

`lessons/00-project-setup/LESSON.md:6–9` supplies the whole `starter/` directory to `.`, so
`starter/README.md` lands in the learner's workspace root as `README.md`. Its text was correctly
rewritten and no longer contradicts the lesson. Two loose ends:

- `README.md` appears in neither `learner_owned` (`tutorial.yaml:42`) nor `tutor_owned` (`:41`),
  so the ownership policy at `:43` does not say who may edit it.
- `00:38–39` tells the tutor to read `starter/README.md` — the bundle path — while the learner now
  has the same file at the workspace root under a different name.

Either add `README.md` to `learner_owned`, or move the notes to
`lessons/00-project-setup/STARTER-NOTES.md` (outside `starter/`, so they are not supplied) and
update `00:38–39`. Neither is a scored finding; both are cheap.

### Q1 — A question for the author about lesson `00`

Lesson `00` is now **+1** and is the course's smallest figure, over eleven elements of which ten
are setup or evidence. That is an honest figure for a setup lesson: it establishes the feedback
loop the rest of the course runs on, and the rubric has no row that rewards that.

**What is this lesson for beyond the feedback loop, and does it want more teaching in it?** For
example, making the learner predict which of `tsc` and `esbuild` catches which of two deliberately
planted errors would serve its first objective with a decision instead of an inspection, and would
make "inspect each supplied file" +2 rather than +1. You know whether that is worth the minute it
costs. **This is a question, not a deletion proposal** — the rubric requires that for any lesson at
or below zero, and lesson 00 has only just left that band.

### Q2 — A question about lessons 12 and 15 (old P9)

Lesson `12` teaches framebuffers, completeness and full-screen triangles (`12:35`); lesson `15`
states all three again as objectives (`15:20–23`), and only its sampleable depth texture and
diagnostic views are new — which is why seven of its eleven scored elements are +1 practice. Was
the overlap intended as a generalisation pass, or did render-to-texture arrive early in lesson 12
because the transition needed it? If the former, `15:20–23` could say so ("you built these ad hoc
in lesson 12; here they become the pipeline"). If the latter, some of lesson 15's framebuffer
material may want to move forward into lesson 12. The rubric cannot see the intent.

### Q3 — A question about splitting lesson 17 (old P10)

Lesson `17` scores 28 against a mean of 13.7 and carries twenty-one scored elements: depth
linearisation, inverse projection, a normal G-buffer, reflection-ray derivation, bounded marching,
hit refinement and five artefact mitigations. The natural seam is at `17:51`, between "verify them
by camera motion" and "derive the reflection ray": everything before it is depth reconstruction — a
complete, separately valuable skill with its own diagnostic — and everything after is SSR.
Splitting would also let the reflective procedural surface that `17:57–58` requires get an explicit
construction step, which no progression clause currently assigns.

### Q4 — Two `design_refs` that do not answer their lesson's question

See §6.1. Both are cheap to fix and neither is scored.

---

## 6. The questions only a reader can answer

All six rows, answered in writing, plus the completability invariant. None is scored; all of them
change what the author does next.

### 6.1 A `design_refs` entry that does not answer the question its lesson raises

**Two instances found, both unchanged since 2026-09-13 — neither fix touched lesson 01 or 06.**

- **`lessons/06-depth-and-culling.md:4`** — `design_refs: [api-boundary, matrix-convention]`. The
  lesson raises the winding question directly: `:20` "Relate vertex winding to front and back
  faces", `:41` "inspect mesh winding", `:45–46` "no required face disappears under the chosen
  culling state". A learner following `#matrix-convention` (`DESIGN.md:16–20`) finds handedness,
  column vectors and the camera's −Z axis, and **no statement of which winding is front-facing** —
  and no other anchor states one either. `#api-boundary` says nothing about depth or cull state.
  The lesson then has the learner decide it (`:50` "Record the depth function, front-face
  convention and culling decision"), but `#unresolved-decisions` (`DESIGN.md:116–119`) lists only
  the `MeshData` shape, camera input mapping, scene composition and final visual styling — not the
  front-face convention. So the learner is deciding something the design document neither answers
  nor admits to leaving open. **Question: should `#matrix-convention` state the front-face winding,
  or should `#unresolved-decisions` name it?**

- **`lessons/01-canvas-and-context.md:4`** — `design_refs: [platform-toolchain, api-boundary]`. The
  lesson demands a policy at `:36–37` ("Centralise drawing-buffer resize logic and cap or explain
  the chosen device-pixel-ratio policy") and checks conformance at `:47` ("its backing dimensions
  match the documented policy"). Neither cited anchor mentions drawing-buffer sizing or
  device-pixel ratio, and `#unresolved-decisions` does not list it either. Same shape, same
  question.

**Considered and rejected:** `lessons/15-render-to-texture.md:4` cites `#post-processing-pipeline`
while `15:57` persists "attachment formats". The anchor does not state formats — but unlike the two
above, lesson 15 never checks the learner's work against a "documented policy" that no document
states, and `16:37` settles the one format choice that matters. Not a finding.

### 6.2 A lesson that introduces a type or concept nothing later uses

**One instance found**, and three candidates examined and rejected.

- **Found: texture wrapping.** `lessons/08-textures.md:21` states the objective "Explain wrapping,
  filtering, mipmaps and image orientation" and `08:32` lists "wrapping" in `## Concepts to teach`.
  **No task, no completion condition and no later lesson touches it** — `TEXTURE_WRAP_S`/`_T`
  appear nowhere in the bundle. It costs the learner attention in the Concepts list and buys the
  course nothing. Either something should exercise it (P2) or it should go. This is the same
  material as the partial coverage topic in §3, reported here because the row asks a different
  question about it: §3 asks whether `COURSE.md:95` is served, this row asks whether the concept
  earns its place in lesson 08.

- **Rejected — `02:37` "Generate three positions from `gl_VertexID`; GPU buffers arrive next
  lesson."** Discarded in lesson 03, by announcement, in the same sentence.
- **Rejected — `03:51` "Record the chosen temporary vertex layout".** The per-vertex colour
  attribute is superseded by texture (08) and lighting (09); the *concept* it teaches (varying
  interpolation) is used for the rest of the course.
- **Rejected — `07:37–38` "Define `MeshData` with positions, normals, UVs and optional indices
  even if some attributes are temporarily unused."** UVs are used one lesson later (08), normals
  two (09).

Every other type this course introduces is consumed later, usually within two lessons. That is a
genuine strength and it should be said as plainly as the finding is.

### 6.3 A symbol or term a lesson uses and no lesson introduces

#### `w` — **the row comes back CLEAN. This is the negative test for the detector, and it passes.**

`tutorail-bundles#11` (`d11644a`) is verified as a real fix, not a relabelling:

- **The binding sentence exists, in a lesson, in prose the learner meets.**
  `lessons/02-first-shader-program.md:25–26`:

  > "Each vertex invocation emits a homogeneous clip-space position `(x, y, z, w)`, whose fourth
  > component `w` is the homogeneous scale factor."

  It is a copula binding in `## Theory`, in the **same sentence as the first use** — not one
  paragraph later, not in another lesson, not in `DESIGN.md`.
- **The first use is `lessons/02-first-shader-program.md:25`**, written `(x, y, z, w)`. The two
  later uses, `lessons/05-transforms-and-perspective.md:20` and
  `lessons/17-depth-reconstruction-and-ssr.md:29`, are both downstream of lesson 02 on the main
  path, so every learner has met the definition before reaching them.
- **`## Concepts to teach` is not what makes it pass.** `02:32` names "the homogeneous `w`
  component", and that alone would **not** satisfy this row — a Concepts bullet instructs the
  tutor to introduce a term; it does not introduce it. The pass rests entirely on `:25–26`.
- **`w` is a symbol under the rubric's boundary**, and I sorted it by hand rather than by shape: it
  is a parameter of the concept being taught — part of what a homogeneous coordinate *is* — not an
  identifier of the language the learner already chose. Nobody brings `w`.
- **The scanner agrees in both directions.** `audit.py` files `w` under `concepts` because a
  Concepts bullet mentions it, and the bucket name is not the verdict; its own evidence line
  records `definition in window: lessons/02-first-shader-program.md:26 [copula]`. The three
  buckets that would be findings — `design-md-only`, `other-lesson-prose` and `none` — are **all
  empty**, over 19 lessons scanned, 19 declaring `## Concepts to teach`, `DESIGN.md` present and
  readable. That is "checked and clean", not "nothing was checked".

**Bound only in `DESIGN.md`: none. Bound nowhere: one, below.**

#### `thickness` — bound nowhere. First use in an instruction: `lessons/17-depth-reconstruction-and-ssr.md:45`

The scanner cannot see this one: its candidate rule collects 1–2 character identifier tokens inside
backticked spans, and `thickness` is an unbacticked word. The reader's sort found it.

- **First appearance:** `lessons/17-depth-reconstruction-and-ssr.md:37`, in `## Concepts to teach`
  ("thickness bias").
- **First use in an instruction to the learner:** `lessons/17-depth-reconstruction-and-ssr.md:45`
  — "Expose step count, thickness and maximum distance as controlled parameters."
- **Where it is bound:** nowhere. `17`'s `## Theory` (`:28–32`) explains depth reconstruction and
  ray marching and never mentions it. `DESIGN.md:106` names it in a list — "requires explicit
  policies for thickness, step size, maximum distance and edge fading" — which is not a definition,
  and would not pass this row even if it were, because an anchor is loaded for the tutor.
- **It is a symbol under the rubric's boundary**, in the same category as `N` and `W`: a parameter
  of the concept being taught. A learner who has just built a depth buffer has no way to guess that
  "thickness" means an assumed depth extent for the surface behind each pixel, and "step count" and
  "maximum distance" beside it are self-explaining, which makes the odd one out easy to miss.
- **Repair:** a decision, then a sentence — P6. It is milder than the `w` defect was: the learner
  meets it in a parameter list rather than in an equation, and the tutor is told to teach it.

#### The class I considered and declined to fire on, recorded so it is not re-litigated

Many terms in this course appear in `## Concepts to teach` with no binding sentence in `## Theory`
("ping-pong rendering" at `16:33`, "texture feedback hazards" at `15:34`, "vertex deduplication
trade-offs" at `07:32`). Firing on that whole class would make the row meaningless: a
Concepts-to-teach bullet is an instruction to the tutor to introduce the term, and the row exists
for the symbol the learner **meets in use** with no definition anywhere. `thickness` is reported
because the lesson **uses** it in a constraint the learner must satisfy, not merely lists it.
`ping-pong` is not, because `16:44–45` "ping-pong the second direction for a small fixed number of
iterations" tells the learner what the technique *does* at the point of use.

The sort in this section is the reader's, candidate by candidate, and the rubric says plainly that
no rule of shape does it. A future `DESIGN.md` convention marking a conceptual parameter apart from
a type would make it mechanical; that is a bundle-format question owned by `skomp/tutorAIl` and it
is not settled here.

### 6.4 Does the lesson equip the tutor to end a turn with one concrete action?

Answered for **every** lesson in the §2 table. **Eighteen pass, one fails.** Graded from the lesson
files; no transcript was used, and none would be admissible as a verdict here.

#### The one failure

**`lessons/18-finish-the-scene.md:45`** — the failing sentence, which opens `## Suggested
progression`:

> "Choose a composition that makes reflections and bloom readable, integrate asynchronous loading,
> tune camera and lighting, …"

It fails **both** conditions:

- **Condition 1 — name the first concrete action.** "Choose a composition" names no file, no
  command and no artifact. It names an outcome the learner must reach by deciding.
- **Condition 2 — keep the decision out of the action.** This is the condition an auditor skips,
  and it is the one that bites here. The lesson is right to make the learner choose a composition;
  the objection is that the decision is left standing **where the action should be**, unmarked as a
  decision, with nothing settling it first. A tutor following the lesson in order must open the
  final lesson of the course with a question.

The contrast inside this same bundle is instructive: `11:32–33` and `12:30–31` both put a genuine
learner choice into `## Theory`, mark it explicitly as a decision the tutor must raise, and leave
their progressions to open with actions. Lesson 18 is the one lesson that does not. P1 proposes
either repair.

#### Why the other eighteen pass

- **Condition 1 holds throughout.** Every other progression opens with an act on a named thing:
  `00:43` "Install dependencies" (a command, spelled out at `starter/README.md:5`), `01:41`
  "Acquire the context", `02:42` "Write and compile each shader separately", `03:41` "Upload
  positions", `04:42` "Add a scalar uniform", `05:41` "Create a cube or other simple volume",
  `06:40` "Capture the incorrect overlap", `07:43` "Convert the procedural object to indices",
  `08:41` "Render UVs as colours", `09:41` "Visualise normals as colour", `10:47` "Extract camera
  state", `11:54` "Present the sorted catalogue", `12:46` "Render each scene to its own target",
  `13:52` "Fetch and parse `models/Duck.glb`", `15:45` "Allocate attachments", `16:43` "Introduce
  emissive/bright scene values", `17:50` "Add and inspect the normal target",
  `minimal-gltf-loader:49–50` "If chosen, parse and validate the GLB envelope".
- **The house style helps condition 1.** This course writes its progression as one sentence of
  comma-separated clauses in strict order, so the tutor takes clause 1 and stops. There is no
  instance in this bundle of the rubric's first failure shape — a single bullet carrying two
  actions the tutor must split before either can be a next step.
- **Condition 2 holds for the two big learner choices**, which are the ones most at risk:
  `11:32–33` ("The tutor MUST explicitly ask which effect the learner wants to build") and
  `12:30–31` are both placed in `## Theory`, before the progression, and marked as decisions.
- **`13-load-gltf-model` improved with the fix, as a side effect worth recording.** Before
  `221c164` the lesson's first assigned act was the copy instruction at `:39`; today it is
  `:52` "Fetch and parse `models/Duck.glb`", a named artifact that is already on disk when the
  lesson opens. The closing-action row would have passed either way, but the first turn is now an
  act of the subject rather than file management.
- **`minimal-gltf-loader:49` "Choose or skip the path" passes**, although it is a branch. The
  decision is explicitly marked as the offer at `:42` and again at `:55`, and the lesson names the
  action that follows a "yes" in the same sentence. A marked, settled decision is exactly what
  condition 2 asks for.
- **`## Optional deeper paths` does not fail any lesson here.** The rubric's second worked failure
  was an optional-paths section that invited an open design question about the main artifact and
  never said it does not close a turn. This course's nineteen optional-paths sections are
  uniformly subordinate and mostly concrete ("After the required version works, add one
  enhancement listed for the chosen effect", `11:74–75`; "Visualise orthographic projection and
  compare it without changing the main scene", `05:55`; "do not implement it on the main course
  path", `minimal-gltf-loader:67–68`). The two discussion-shaped ones — `04:57` "discuss when
  on-demand rendering is preferable" and `08:56` "Discuss colour space at a conceptual level
  without building a full colour-management pipeline" — are both bounded by an explicit scope
  limit in the same sentence, and neither concerns a decision the main path leaves open. **No
  lesson is failed on this ground**, and the ruling is recorded here so the next auditor does not
  have to re-derive it.

### 6.5 A lesson far outside the course's usual size

**Two, in opposite directions.** Mean main-path lesson: 13.7; the middle of the distribution runs
9–18.

- **`lessons/17-depth-reconstruction-and-ssr.md` — 28, twenty-one scored elements, 2.0x the
  mean.** Far the largest, and unchanged since 2026-09-13. It carries two teachable subjects —
  recovering view-space position from a depth buffer, and screen-space reflection — and its own
  title names both. Q3 gives the seam. A learner who stalls anywhere in this lesson has no smaller
  unit to fall back to, which is the practical cost.
- **`lessons/00-project-setup/LESSON.md` — +1, and structurally unlike every other lesson** (ten
  of eleven elements are setup or evidence). It is small because it is setup, not because it is
  incomplete; all three of its objectives are served. **This is the one outlier the fix improved:
  on 2026-09-13 it was the only lesson in the catalogue with a negative figure.** Q1 asks the
  author about it rather than proposing a change.

No other lesson is outside 9–18.

### 6.6 A must-cover topic that only an optional lesson teaches

**None found — and I checked rather than assumed.** `minimal-gltf-loader` teaches GLB headers,
JSON/BIN chunks, buffer views, accessors, component types, byte offsets, byte stride, index arrays
and image buffer views (`:20–23`, `:37–38`). **Not one of those appears in `COURSE.md:69–124`.**
The two adjacent topics that *are* in the coverage list — "asynchronous asset loading"
(`COURSE.md:110`) and "glTF model integration" (`:111`) — are both taught on the main path by
`13-load-gltf-model`.

So the question the rubric insists on asking — *is it acceptable that a learner who declines every
offer never meets this material?* — has the easiest possible answer here: **yes, because the course
never promised it.** The optional lesson is pure enrichment, sitting exactly where the bundle format
says such a lesson should. `COURSE.md:132–133` states the boundary explicitly: "The optional loader
lesson supports only the packaged model's documented subset and must say so clearly." No author
judgement is needed.

This row stays a question and is not a score. The rubric records why, and it is recorded here so
the next auditor does not re-open it: a scored row would push authors toward dropping the topic
from the coverage list, producing the outcome the format calls worse — a tutor improvising material
an author had already written.

### 6.7 The completability invariant, asked out loud

> **Can a learner who declines every offer still finish this course?**

**Yes. Verified against the lessons, not only against the manifest.**

- **Does any main-path completion condition depend on something only the optional lesson builds or
  explains?** No. I read all eighteen main-path `## Completion conditions` blocks. The only
  asset-loading condition downstream of the offer is `13:58–61`, satisfied by the library-backed
  adapter the same lesson builds. Lessons `15`, `16`, `17` and `18` never mention GLB decoding;
  they consume `MeshData`, which exists either way.
- **Does any main-path lesson's prose assume the learner took the offer?** No. There are exactly
  two main-path mentions, and both handle the decline case explicitly:
  - `lessons/13-load-gltf-model/LESSON.md:70–71` — "The optional lesson `minimal-gltf-loader`
    replaces the parsing-library adapter with one you write. The tutor offers it here; **it is not
    required for WebGL coverage or the final scene.**"
  - `lessons/15-render-to-texture.md:15–16` — "The optional lesson `minimal-gltf-loader` **was
    taken or declined; either way a working `MeshData` adapter exists.**"
- **Does the fix put anything behind the offer?** **No, and this was worth checking.** Both new
  `supplies` entries are scoped to **main-path** lessons — `00-project-setup` and
  `13-load-gltf-model` — so a learner who declines every offer still receives all nine files. Had
  either set been attached to `minimal-gltf-loader`, the invariant would have broken silently.
- **Does the manifest gate anything?** No. `grep -rnP 'required_for|anticipates|repair_in'` over
  the whole bundle returns nothing (exit 1, against a positive control that found
  `tutorial.yaml:32 optional_lessons:`). The `optional_lessons` block at `tutorial.yaml:32–38`
  carries only `offer_at` and `offer_because`. **No `required_for` gate exists, so the −3 row does
  not fire and its warning is not printed — there is no gate to warn about.** I checked by opening
  `tutorial.yaml`, not by trusting `optional_lesson_count`, as the skill requires.

**The invariant holds.**

### 6.8 Prose optionality versus the manifest — re-checked, because the rubric's worked example is this bundle

**Prose and manifest agree everywhere. The repair made in `49af681` still holds.**

| Check | Result |
|---|---|
| Is the lesson in `optional_lessons:`? | Yes — `tutorial.yaml:32–38`, keyed `lessons/minimal-gltf-loader/LESSON.md`, with `offer_at: [lessons/13-load-gltf-model/LESSON.md]` and an `offer_because` |
| Is it absent from `lessons:`? | Yes — `tutorial.yaml:12–30` lists 18 main-path lessons and does not include it |
| Does the lesson declare itself optional? | Yes — `minimal-gltf-loader/LESSON.md:4` `optional: true` |
| Does its prose agree? | Yes — `:11`, `:12` "not a prerequisite for later WebGL concepts", `:42`, `:55` |
| Does `COURSE.md` agree? | Yes — `:135–141`, its own "Optional path" section, outside the numbered map |
| Do its neighbours agree? | Yes — `13:70–71` and `15:15–16` |
| Does the tooling see it? | Yes — `audit.py` reports "18 lesson(s), 1 optional" over 19 rows |

The course is scored as the manifest has it, and both totals a reader needs are in §1: **247** for a
learner who declines, **264** for one who accepts. The rubric's published 194 / 183 describe the
pre-repair bundle and are superseded; so are the 2026-09-13 figures of 243 / 260, by this report.

One residual from that repair is still open: the bare "lesson 14" at `COURSE.md:137`, P5.

---

## 7. Every delta from the 2026-09-13 report, and its cause

The baseline is `docs/audits/2026-09-13/webgl-typescript-scene.md` — total **260**, main path
**243**. I re-added every lesson's elements from the lesson files rather than carrying its figures
forward, so the table below separates deltas the bundle caused from deltas my ruler caused.

### Score deltas

| Lesson | 2026-09-13 | 2026-09-15 | Δ | Cause |
|---|---:|---:|---:|---|
| `00-project-setup` | −1 | **+1** | **+2** | **bundle changed** — `b969892` deleted the `:34–36` copy element |
| `01-canvas-and-context` | 10 | 11 | +1 | ruler (see below) |
| `02-first-shader-program` | 14 | 14 | 0 | — |
| `03-vertex-data` | 13 | 13 | 0 | — |
| `04-uniforms-and-animation` | 9 | 9 | 0 | — |
| `05-transforms-and-perspective` | 13 | 12 | −1 | ruler |
| `06-depth-and-culling` | 11 | 9 | −2 | ruler |
| `07-indexed-meshes-and-vaos` | 13 | 13 | 0 | — |
| `08-textures` | 15 | 15 | 0 | — |
| `09-normals-and-lighting` | 10 | 10 | 0 | — |
| `10-camera-and-scene` | 15 | 15 | 0 | — |
| `11-secondary-demo-scene` | 15 | 15 | 0 | — |
| `12-scene-transition` | 18 | 18 | 0 | — |
| `13-load-gltf-model` | 12 | **14** | **+2** | **bundle changed** — `221c164` deleted the `:39–40` copy element |
| `15-render-to-texture` | 15 | 15 | 0 | — |
| `16-bloom` | 17 | 18 | +1 | ruler |
| `17-depth-reconstruction-and-ssr` | 28 | 28 | 0 | — |
| `18-finish-the-scene` | 16 | 17 | +1 | ruler |
| `minimal-gltf-loader` *(optional)* | 17 | 17 | 0 | — |

```
bundle-caused delta   +2 (lesson 00) +2 (lesson 13)          = +4
ruler-caused delta    +1 -1 -2 +1 +1                         =  0
-------------------------------------------------------------------
main path             243 + 4 + 0                            = 247
all 19 rows           260 + 4 + 0                            = 264
```

**The ruler-caused deltas net to exactly zero**, which is a coincidence worth naming rather than
hiding: five individual lessons moved and the sum did not. The course total therefore changed by
exactly the amount the two fixes are worth, and it would be wrong to read that as confirmation that
my element lists match the old report's. They do not, on five lessons.

### The five ruler deltas, each explained

The old report published full element tables for `00`, `04`, `11`, `12`, `13`, `15`, `17` and
`minimal-gltf-loader` and only prose summaries for the rest. My figures match every published table
and differ on four of the summarised lessons plus lesson 18. The rubric says why this is expected:
a lesson's figure tracks how finely its progression is enumerated, and two readers enumerating the
same prose sentence can land one clause apart. **Cause in every case below: neither the bundle nor
the rubric — my clause split against an unpublished one.**

- **`01` +1.** I scored the device-pixel-ratio *policy* at `:36–37` as its own +2 element and
  "resize the drawing buffer" at `:41` as +1 practice. The old summary folded them, scoring the
  resize +2 and the policy not at all.
- **`05` −1.** I split `:36–37` into "Send matrices through uniforms" (+1) and "preserve the
  convention in `DESIGN.md`" (+2), and scored `:37` "Render 3D geometry even though occlusion is
  not correct yet" as sequencing at 0. The old summary reached 13 from "5–8 constructing steps at
  +2, 1–3 practice steps at +1"; my list has four constructing steps plus the explain condition.
- **`06` −2.** I scored the constraint at `:35–36` ("Enable culling only after triangle winding is
  known to be consistent") as **restated** by the progression's own order and therefore counted
  once, at `:41`. The old summary reached 11, which requires counting it separately. Mine is the
  stricter reading of P-c; a reader who thinks the constraint assigns an act the progression does
  not should add +2 and read this lesson as 11.
- **`16` +1.** I scored `:39` "Bloom must be toggleable" as its own +1 element; it is a real
  requirement on the artifact that the progression never restates. The old summary did not have it.
- **`18` +1.** I scored `:41` "Retain model attribution and licences" as +1. The old report cited
  that very line in its anchor table as a server of `#packaged-model` but did not score it as an
  element. Scoring it is the consistent choice, especially now that it carries more of the anchor.

None of these five is caused by the bundle. **Both bundle-caused deltas are exactly the two toil
elements ceasing to exist, and the old report predicted both figures** (+1 for lesson 00 under its
P1, 14 for lesson 13 under its P2).

### Deltas that are not scores

| What | 2026-09-13 | 2026-09-15 | Cause |
|---|---|---|---|
| Confirmed toil sites | **2** | **0** | bundle changed |
| `supplies:` entries declared | 0 | 2, both lesson-scope | bundle changed |
| Reader-answered rows | 4 | **6** | rubric changed |
| Symbol row | not asked | asked; **clean for `w`**, one `bound nowhere` (`thickness`) | rubric changed, and `d11644a` fixed `w` |
| Closing-action row | not asked | asked for all 19; **18 pass, `18:45` fails** | rubric changed |
| §6.2 (concept nothing uses) | "none found" | one instance: texture wrapping, `08:21` / `08:32` | my judgement, not the bundle. The old report carried the same evidence in its §3 as a partial coverage topic and did not also raise it here |
| Old P1 (declare `starter/`) | proposed | **applied** as `b969892` | bundle changed |
| Old P2 (declare `model/`) | proposed | **applied** as `221c164` | bundle changed |
| Old P3 (restore `#packaged-model`) | proposed, on the prediction that P2 would thin the anchor | **withdrawn as unnecessary** — the anchor is served by `13:43–44`, `13:58`, `18:41` and `18:56–57` | bundle changed; the old report's caveat was a reasonable forecast and the author's edit answered it by keeping the attribution clause |
| `#platform-toolchain`'s server list | "`00`: **copies**, type-checks, builds and serves…" | "`00:43` **inspects each supplied file**, type-checks, builds and serves…" | bundle changed. The anchor is still served: it describes the platform, not the act of assembling it |
| Old P4–P10 | open | P4→P2, P5→P3, P6→P4, P7→P5, P9→Q2, P10→Q3, all still open and unchanged; P8 restated as Q1 with lesson 00 now at +1 | neither |
| Lesson 00's standing | the catalogue's only negative lesson figure | +1, still the smallest | bundle changed |

### Two dated statements in the rubric, noted so a later reader does not take them as current

The rubric says so about itself; these are the two that concern this bundle.

- **`references/rubric.md:111`** — the worked table's webgl row reads "**toil** on the plain test;
  its skeleton ships as `starter/` files, so the tiebreak never fires". The reasoning is still
  exactly right and the **ruling is now spent**: the `starter/` files are no longer merely shipped,
  they are *declared*, so there is no step left to score. Read the row as the worked reasoning it
  is presented as, not as a description of this bundle today.
- **`references/rubric.md:504–517`**, the prose-optionality section, describes lesson 14 of this
  bundle sitting in `lessons:` while three places of prose called it optional, and publishes totals
  of 194 / 183. That defect was repaired in `49af681`, before the 2026-09-13 audit; §6.8 verifies
  the repair still holds. Those totals describe a bundle that no longer exists.

---

## Verdict

**A strong course, and now a clean one.** It teaches by making the learner decide and construct at
almost every step, it breaks things deliberately and reasons from the wreckage (`02:42–43`,
`03:42`, `09:42`, `18:47–48`), it demands an explanation at the end of fourteen of nineteen
lessons, it serves all 55 of its declared topics and all 16 of its design anchors, and — with one
exception — it introduces nothing it does not later use. The completability invariant holds, no
gate is hiding in the manifest, and both supplied file sets sit on the main path where a learner
who declines every offer still receives them.

**`tutorail-bundles#6` closed the last confirmed toil in this bundle, and with it the catalogue's
last two sites.** The course's entire recoverable loss on 2026-09-13 was 4 points across two
file-copy instructions caused by one omission — the bundle declared no `supplies:` entries at all
while shipping nine files destined for the learner's workspace. That omission is gone. **There is
no toil left here to propose a fix for**, and every remaining proposal in §5 is either a one-clause
coverage repair (P2, P3, P4), a wording fix (P5, P7), a missing definition (P6), one closing-action
repair (P1), or a question only the author can answer (Q1–Q4).

**`tutorail-bundles#11` holds up under the detector that found it.** `w` is bound in a lesson, in
prose the learner meets, in the same sentence as its first use, and all three finding buckets of
the symbol scan come back empty. The one term this run adds — `thickness` at `17:45` — is milder
and is the reader's find, not the scanner's.

The two places the course still asks the learner to decide something its design document neither
answers nor admits to deferring (`01:36–37`, `06:50`) are unchanged and remain the most interesting
thing left in this bundle, because they are the kind of gap no validator and no scanner will ever
raise.
