# tutorail-authoring

## Where work is tracked

This project tracks deferred work in `TODO.md`. Do not open GitHub issues for it.

Write every entry in ASD-STE100 Simplified Technical English. Keep identifiers, file paths
and command names verbatim.

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
