# TODO

Deferred work for tutorail-authoring is tracked in **GitHub issues**, not in this file.

- https://github.com/skomp/tutorail-authoring/issues

Open issues from the supplies and course-quality work, 2026-09-12:

| Issue | What |
|---|---|
| tutorail-authoring#2 | The catalogue scope line ignores the optional lessons |
| tutorail-authoring#3 | Add three reader-answered signals to the course-quality rubric |
| tutorail-authoring#4 | Two documents claim more than the code enforces |
| tutorAIl#11 | The runner design spec states the material-naming rule with no exception |
| tutorAIl#12 | `run_case` can pass when the wrong file produces the finding |
| tutorAIl#13 | Two claims in `bundle-format.md` are now wrong |
| tutorail-bundles#1 | Three findings from the first course-quality audit |

The audit that produced several of these is at
`docs/audits/2026-09-12-course-quality-first-run.md`.

## Do not build a second bundle quality checker

It exists as `skills/course-quality/`. The design is at
`docs/superpowers/specs/2026-09-12-toil-and-course-quality-design.md` section 9.
`skills/course-quality/scripts/audit.py` gathers the evidence and computes no score,
because the parts a script can decide are not the parts that matter.

The validator answers one question: can a runner execute this bundle? Its checks stay
binary, because the runner gates on them at materialization. Course quality is not binary,
and no quality finding may ever reject a bundle.
