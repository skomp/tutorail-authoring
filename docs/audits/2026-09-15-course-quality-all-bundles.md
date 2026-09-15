# Course-quality audit, 2026-09-15 — every bundle in `skomp/tutorail-bundles`

This audit supersedes `2026-09-13-course-quality-all-bundles.md`. It is a fresh run and not
a patch: the 2026-09-13 reports were amended twice in one day, and a third amendment would
have been harder to read than a clean audit of a settled catalogue.

## Provenance

A green validator line is a claim about a machine on a day unless it records **which copy of
the validator** and **which YAML reader** produced it. Ten `validate_bundle.py` copies exist
on the machine that ran this.

```
bundles     skomp/tutorail-bundles @ 221c164 (== origin/main, tree clean)
rubric      skomp/tutorail-authoring @ 86c2bc7, plugin 0.4.0
validator   pinned copy of the WHOLE scripts directory from the source checkout
            skomp/tutorAIl @ 717c575
yaml reader restricted built-in, ALWAYS — tutorAIl#29 decided at 7419722.
            PyYAML 6.0.3 was importable and was deliberately not used.
verdicts    all five bundles: PASS - every applicable check ran and found nothing. exit 0
```

The whole scripts directory is pinned because `validate_bundle.py` imports `yamlite` and
`catalogs` from beside itself. A single-file pin produces a validator that cannot run and
fails in a way that reads as product defects.

## The totals

The rubric says a lesson's figure tracks how finely its `## Suggested progression` enumerates
clauses. **Every total below is comparable only against its own course's lessons**, and
against that course's own figure on 2026-09-13.

| Course | Lesson sum | Penalties | Total | On 2026-09-13 | Declining every offer |
|---|---|---|---|---|---|
| `durable-event-broker` | 131 | none | **131** | 128 | 111 |
| `portable-bytebeat-wav` | 55 | −3 (1 unserved objective) | **52** | 48 | 42 |
| `portable-fixed-window-rate-limiter` | 34 | none | **34** | 32 | 26 |
| `rust-automaton-db` | 370 | −15 (5 unserved topics) | **355** | 355 | 355 |
| `webgl-typescript-scene` | 264 | none | **264** | 260 | 247 |

| Report | |
|---|---|
| `durable-event-broker` | [`2026-09-15/durable-event-broker.md`](2026-09-15/durable-event-broker.md) |
| `portable-bytebeat-wav` | [`2026-09-15/portable-bytebeat-wav.md`](2026-09-15/portable-bytebeat-wav.md) |
| `portable-fixed-window-rate-limiter` | [`2026-09-15/portable-fixed-window-rate-limiter.md`](2026-09-15/portable-fixed-window-rate-limiter.md) |
| `rust-automaton-db` | [`2026-09-15/rust-automaton-db.md`](2026-09-15/rust-automaton-db.md) |
| `webgl-typescript-scene` | [`2026-09-15/webgl-typescript-scene.md`](2026-09-15/webgl-typescript-scene.md) |

**Every figure rose or held.** No course scores lower than it did two days ago. Four rose
because defects were repaired between the audits; `rust-automaton-db` held.

## Confirmed toil across 69 scored lessons: one site

On 2026-09-13 there were six. Five are gone.

| Bundle | Sites | What happened |
|---|---|---|
| `portable-fixed-window-rate-limiter` | 0 | the setup step moved to the tutor (`a67de21`) |
| `portable-bytebeat-wav` | 0 | the same, `c80d8e3` |
| `durable-event-broker` | 0 | the skeleton is now a declared `supplies` entry (`dc3ba72`) |
| `webgl-typescript-scene` | 0 | both copy instructions became declared `supplies` entries (`b969892`, `221c164`) |
| `rust-automaton-db` | **1** | `22-hardening-performance.md:63`, "Build CI and reproducible clusters." Unrelated to the skeleton ruling |

The one remaining site is the only toil finding in the catalogue that the project-skeleton
ruling of 2026-09-13 never touched.

## What the ruling did, and what it did not do

The ruling said a project skeleton is toil, with an exception where the setup is the only
element serving the objective that names it, and a following rule that **a step the tutor
performs is not an element**.

Three courses took the hand-over route and one took the supply route:

- `portable-fixed-window-rate-limiter` and `portable-bytebeat-wav` declare
  `ownership_policy: on-request` and let the tutor create the project. In both, the step
  **stops being an element** rather than stopping being toil.
- `durable-event-broker` and `rust-automaton-db` ship the file. The broker's step became
  practice at +1; the Rust step kept `evidence, 0`.
- `webgl-typescript-scene` never needed the tiebreak: its skeleton always shipped, and its
  defect was assigning the copying anyway.

**The exception still fires exactly once in five.** `rust-automaton-db` remains the only
course whose setup objective is sole-served, and the reason is sharper than it was: the
bundle ships `Cargo.toml` and **not** `src/main.rs`, so half of `cargo new --bin` is still
the learner's act. The objective `00:24` was **not** rewritten. It is not stranded, because
the step at `00:79` was rewritten instead.

## Two rows answered for the first time

`tutorail-authoring#13` and `#14` added two reader-answered rows. This is their first run.

### The closing-action row: 7 of 69 lessons fail

| Bundle | Failing lessons |
|---|---|
| `portable-fixed-window-rate-limiter` | `00:66`, and `00:83-86` |
| `portable-bytebeat-wav` | `03:54` |
| `durable-event-broker` | `11:52` |
| `rust-automaton-db` | `01:79-80`, `04:93`, `19:58` |
| `webgl-typescript-scene` | `18:45` |

**The row reproduced the field report it was written from, without being pointed at it.**
`tutorail-authoring#13` records a learner saying "there is no call to action in this step"
in the rate limiter's lesson 00, and names the bullet "Define the public contract in prose
and then as an API signature or stub". The auditor, working from the rubric, failed that
same bullet.

One repair was also caught: `durable-event-broker`'s `00:53` passes now and would have
failed before. Supplying `go.mod` split a two-action bullet as a side effect.

### The undefined-symbol row: five symbols, in three bundles

| Symbol | Bundle | First use | Bucket |
|---|---|---|---|
| `base offset` | `durable-event-broker` | `07-segments.md:19` | bound nowhere |
| `metadata seam` | `durable-event-broker` | `09-retention.md:44` | bound nowhere (weaker) |
| `CAS` | `rust-automaton-db` | `21:22` | bound only in `DESIGN.md` |
| `WAL` | `rust-automaton-db` | `10:18` | bound nowhere |
| `FST` | `rust-automaton-db` | `08:54` | bound nowhere |
| `thickness` | `webgl-typescript-scene` | `17:45` | bound nowhere |

`w` in `webgl-typescript-scene` is **clean**, bound at `02:25-26` in the same sentence as its
first use. That was the defect that justified the row, and its repair is the row's negative
test.

**The script found none of the six above.** Its candidate rule is a 1-2 character identifier
token, and every one of these is a word or an acronym. Two limits are now measured rather
than suspected:

1. `audit.py` returned **nothing-to-check** for `durable-event-broker` — 0 candidates over 18
   lessons. The auditor did not read that as a pass. Enumerating all 26 backticked spans
   showed none holds a short token, so the blindness is that bundle's house style. Answering
   the row by hand is what found `base offset`.
2. A symbol named in `## Concepts to teach` is **not** thereby introduced. `thickness` and
   `base offset` both appear in a Concepts bullet and are defined nowhere.

The `nothing-to-check` status is what made the first of those visible. A scanner that
reported "clean" would have hidden it.

## A tooling defect this audit had to work around

`tutorail-authoring#10` is not latent. Running `audit.py --json` against `rust-automaton-db`
returns `coverage_list.topics: []` and states that the author "never filled it in".

`COURSE.md:225-271` holds **45** topics inside a ```` ```text ```` fence.

An auditor who trusted the script would have reported no coverage list, suppressed the
**−15** for five unserved topics, and published **370** for that course instead of 355. The
figure above is correct only because the auditor read `COURSE.md` by hand.

The 2026-09-13 report said the fence holds 46 topics. It holds 45. No figure moves.

## Findings raised that are nobody's open issue yet

- **`rust-automaton-db` declares validators that nothing invokes, in 14 of its 23 lessons.**
  The `cargo-run` case recorded on 2026-09-13 as the quirk that made `00:79` sole-served is
  the bundle's habit and not a slip.
- **`durable-event-broker`'s supplied `go.mod:3` asserts `go 1.22`**, and `COURSE.md:139-144`
  names no minimum Go version. That directive used to be the learner's choice. This is new,
  and the supplies commit introduced it.
- **`durable-event-broker`'s objective `00:21` was not reworded** when the skeleton was
  supplied, which the last audit proposed. It survives only because the objective is a
  three-conjunct conjunction and two conjuncts keep their own servers.

## Still open in `skomp/tutorail-bundles`

`#3`, `#4`, `#7`, `#8` and `#9`. None changes a lesson. `#5`, `#6` and `#11` were closed by
the fixes this audit measures, and each was verified from the files rather than from its
commit message.
