# TODO

Deferred work for tutorail-authoring is tracked in **GitHub issues**, not in this file.

- https://github.com/skomp/tutorail-authoring/issues

Open issues, 2026-09-13:

| Issue | What |
|---|---|
| tutorail-authoring#3 | Add three reader-answered signals to the course-quality rubric |
| tutorail-authoring#4 | Two documents claim more than the code enforces |
| tutorail-authoring#5 | Build the dry-run harness that tests a course before a learner pays for it |
| tutorail-authoring#9 | README does not say how to install for Codex |
| tutorail-authoring#10 | `audit.py` does not read a coverage list that a course writes in a code fence |
| tutorail-authoring#11 | The toil rubric does not settle whether a project skeleton is toil |
| tutorail-bundles#3 | Create the initial workspace setup for the language that the learner selects |
| tutorail-bundles#4 | Show a banner when a tutorial loads for the first time |
| tutorail-bundles#5 | `portable-bytebeat-wav`: the stereo offer blocks the completion of lesson 03 |
| tutorail-bundles#6 | `webgl-typescript-scene`: declare the starter files and the model as supplies |
| tutorail-bundles#7 | `rust-automaton-db`: five topics in the coverage list have no task |
| tutorail-bundles#8 | `durable-event-broker`: make the timestamp, the ownership rule and the read path load-bearing |
| tutorail-bundles#9 | `portable-fixed-window-rate-limiter`: add a retention anchor, and decide where concurrency safety belongs |

All issues in `skomp/tutorAIl` are closed. `tutorail-authoring#1`, `#2`, `#6`, `#7` and `#8`
are also closed.

`tutorail-authoring#11` and `tutorail-bundles#3` are the same problem from two sides. The
learner changed `ownership_policy` because no bundle supplies a project skeleton. The rubric
does not say if a skeleton is toil, and no check finds the missing `supplies` entry. Decide
the rubric question first, because the bundle work depends on the ruling.

Where the rows come from:

- `tutorail-bundles#3` and `#4` come from a learner run on the morning of 2026-09-13. They
  are field reports, not audit findings.
- `tutorail-bundles#5` to `#9` come from the audit of 2026-09-13, one issue for each bundle.
- `tutorail-authoring#10` is the tooling defect that the same audit found.

The audits are at `docs/audits/2026-09-12-course-quality-first-run.md` and
`docs/audits/2026-09-13-course-quality-all-bundles.md`. The index of the second audit gives
the same split at lines 144-155.

## Do not build a second bundle quality checker

It exists as `skills/course-quality/`. The design is at
`docs/superpowers/specs/2026-09-12-toil-and-course-quality-design.md` section 9.
`skills/course-quality/scripts/audit.py` gathers the evidence and computes no score,
because the parts a script can decide are not the parts that matter.

The validator answers one question: can a runner execute this bundle? Its checks stay
binary, because the runner gates on them at materialization. Course quality is not binary,
and no quality finding may ever reject a bundle.
