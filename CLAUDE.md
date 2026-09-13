# tutorail-authoring

## Where work is tracked

This project tracks deferred work in **GitHub issues**, and in no other place. Label every
issue Claude creates with `created-by-claude`.

Do not add a `TODO.md`. One existed until 2026-09-13 and held a table of the open issues.
The table was a copy, and a copy goes stale: on 2026-09-13 it listed five issues that were
closed and omitted six that were open. Read the issues with `gh issue list`.

Issues that belong to a sibling repository stay in that repository. Use the qualified form
`tutorail-bundles#3`, never a bare number.

Write every entry in ASD-STE100 Simplified Technical English. Keep identifiers, file paths
and command names verbatim.

## Do not build a second bundle quality checker

It exists as `skills/course-quality/`. The design is at
`docs/superpowers/specs/2026-09-12-toil-and-course-quality-design.md` section 9.
`skills/course-quality/scripts/audit.py` gathers the evidence and computes no score, because
the parts a script can decide are not the parts that matter.

**The validator and the rubric answer different questions, and only one of them gates.**
The validator answers "can a runner execute this bundle?" Its checks stay binary, because
the runner gates on them at materialization. Course quality is not binary, and **no quality
finding may ever reject a bundle.** A rubric row is a judgement a reader makes, and a
judgement must not stop a learner from starting a course.

So: do not add a course-quality check to `validate_bundle.py`, and do not let a rubric row
grow a hard gate. Issues that add rubric rows say this in their own words; keep saying it.

This rule lived in `TODO.md` until 2026-09-13 and was lost for one commit when that file was
removed. It is operating guidance, not tracked work, so it belongs here.

## The validator comes from the runner plugin

`validate_bundle.py` lives in the tutorAIl runner plugin. Every mutating script calls it.

**Pin the whole scripts directory when a test result must be attributable.** The file imports
`yamlite` and `catalogs` from beside itself, so a single-file pin produces a validator that
cannot run, and it fails in a way that reads as product defects. The tell is
`FAIL - 0 finding(s)`: a validator that fails while reporting nothing did not run.

```bash
mkdir -p /tmp/pin && cp <runner>/skills/tutorail/scripts/*.py /tmp/pin/
TUTORAIL_VALIDATOR=/tmp/pin/validate_bundle.py python3 tests/run_all.py
```

## grep on this machine is ugrep

`grep -E` is ugrep 7.8.4. A digit class mixed with `\b` makes the whole pattern match
nothing, silently, with a clean exit 1. Use `-P` for those patterns, and plant a positive
control before you believe any zero.
