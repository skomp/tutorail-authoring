#!/usr/bin/env python3
"""promote.py - the ten-step promotion procedure of bundle-format.md section 8.

Run it:  python3 tests/test_promote.py

Every refusal below is shown FIRING, and every refusal has a POSITIVE CONTROL
beside it: the same command against material that differs only in the one
thing the refusal is supposed to be about, succeeding. Without the control,
"it refused" is evidence of nothing - a refusal for an unrelated reason
(a typo'd path, a missing validator, a dirty tree) looks exactly the same
from the outside, and this project has already been bitten by a probe whose
negative result nobody had shown could ever turn positive.

Two invariants are asserted after EVERY promote in this file, success or
failure:

  * the learner's instance is BYTE-IDENTICAL afterwards. Step 9 is explicit
    that the learner's copy stays; a tool that moved rather than copied would
    take a file out of a live course and the learner would find out later.
  * on any failure the bundle is BYTE-IDENTICAL. "The new lesson is absent"
    is the weaker check, and a half-written tutorial.yaml passes it.

Both fixtures are copied per case. Neither is ever edited in place.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from harness import (  # noqa: E402
    PROMOTE,
    Workspace,
    case,
    check,
    check_in,
    check_not_in,
    git_init,
    has_exactly,
    listing,
    report,
    run,
    tree_digest,
    write_stub_validator,
)

import bundlelib as bl  # noqa: E402  (harness put the scripts dir on sys.path)

GEN = "lessons.generated"
LIFE = "lifetimes-and-borrows.md"
SIBLING = "sibling-resolution.md"

# The placement the fixture pins down: lifetimes-and-borrows carries
# `after: lessons/03-first-refactor.md`, which is index 3 of the manifest's
# 23-entry list, so it lands at position 4 and takes the name below. The
# bundle's existing 04- lesson moves to index 5 in the list and keeps its
# filename, which is why a renumber is advised and not done.
PROMOTED = "04-lifetimes-and-borrows.md"
PROMOTED_ID = "04-lifetimes-and-borrows"

# The second line of the `reason: >` block scalar in the fixture. Stripping a
# block scalar must take its continuation lines with it; a naive line-delete
# leaves this behind as stray YAML that either fails to parse or, worse,
# parses as a new key.
REASON_CONTINUATION = "nothing on the main path teaches lifetime elision."


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair(ws: Workspace, suffix: str = "") -> tuple[Path, Path]:
    """A fresh bundle and a fresh learner instance, both temp copies."""
    bundle = ws.copy("rust-automaton-db", f"bundle{suffix}")
    instance = ws.copy("instance-with-generated", f"instance{suffix}")
    return bundle, instance


def frontmatter_of(path: Path) -> tuple[str, dict]:
    text = path.read_text(encoding="utf-8")
    raw, _ = bl.split_frontmatter(text)
    assert raw is not None, f"{path} has no frontmatter"
    parsed = bl.load_yaml(raw, path.name)
    assert isinstance(parsed, dict)
    return raw, parsed


class Learner:
    """Snapshot of the learner's instance, so every case can prove it survived.

    Step 9 of the procedure is "say what happens to the learner's copy", and
    the answer is "nothing". This is how that is checked, after every single
    promote in the file rather than in one dedicated case, because a delete
    would most plausibly appear in some path nobody thought to look at.
    """

    def __init__(self, instance: Path, name: str = LIFE) -> None:
        self.instance = instance
        self.name = name
        self.digest = tree_digest(instance)
        self.file_sha = sha(instance / GEN / name)

    def still_there(self, label: str) -> None:
        check(
            has_exactly(self.instance / GEN, self.name),
            f"{label}: {self.name} is still listed in the instance's {GEN}/",
        )
        check(
            sha(self.instance / GEN / self.name) == self.file_sha,
            f"{label}: the learner's copy of {self.name} is byte-identical",
        )
        check(
            tree_digest(self.instance) == self.digest,
            f"{label}: the whole instance is byte-identical (nothing moved, "
            f"nothing rewritten)",
        )


def promote(instance: Path, given: str, bundle: Path, *flags: str, env=None):
    return run(PROMOTE, instance, given, bundle, *flags, env=env)


# --------------------------------------------------------------------------


def main() -> int:
    print("test_promote.py - bundle-format.md section 8, the ten-step procedure")
    print()

    # ------------------------------------------------------------------
    # A. The happy path
    # ------------------------------------------------------------------

    with case("A1  step 1: the promoted file is named from its 'after:' position"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)
            before = listing(bundle / "lessons")
            done = promote(instance, "lifetimes-and-borrows", bundle)
            check(done.returncode == 0, f"exit 0 (got {done.returncode})")
            after = listing(bundle / "lessons")
            # By directory listing, never .exists(): this filesystem is
            # case-insensitive, so exists() cannot tell 04-Lifetimes... apart
            # from 04-lifetimes... and the difference fails on Linux.
            check(
                has_exactly(bundle / "lessons", PROMOTED),
                f"lessons/ holds exactly {PROMOTED}",
            )
            check(
                set(after) - set(before) == {PROMOTED},
                f"exactly one file appeared, and it is {PROMOTED} "
                f"(new entries: {sorted(set(after) - set(before))})",
            )
            check(
                has_exactly(bundle / "lessons", "04-richer-typed-schemas.md"),
                "the bundle's existing 04- lesson keeps its filename "
                "(the list is the order; the prefix follows it)",
            )
            check_in(
                "run  lesson.py renumber",
                done.output,
                "the output says the prefixes are now out of sequence and names "
                "the command that fixes them",
            )
            learner.still_there("A1")

    with case("A2  step 2: id is set to the new slug, exactly"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)
            done = promote(instance, "lifetimes-and-borrows", bundle)
            check(done.returncode == 0, f"exit 0 (got {done.returncode})")
            _, fields = frontmatter_of(bundle / "lessons" / PROMOTED)
            # The value, not the shape: `id` must equal the slug the file was
            # renamed to, character for character. Section 6 requires it and
            # the validator enforces it, but a tool that wrote the old id back
            # would still produce a parseable lesson.
            check(
                fields.get("id") == PROMOTED_ID,
                f"id == {PROMOTED_ID!r} (got {fields.get('id')!r})",
            )
            source_id = frontmatter_of(instance / GEN / LIFE)[1].get("id")
            check(
                source_id == "lifetimes-and-borrows",
                f"positive control: the SOURCE still carries the un-numbered id "
                f"{source_id!r}, so the assertion above reads a rewritten value "
                f"rather than a coincidence",
            )
            check(
                fields.get("title") == "Lifetimes and borrows, the short version",
                "title is carried across unchanged",
            )
            learner.still_there("A2")

    with case("A3  step 3: all five provenance fields are gone, block scalar and all"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)

            # POSITIVE CONTROL FIRST, on the source file: it proves the probe
            # below can see a provenance field when one is there. An absence
            # assertion written against a parser that returns {} for every
            # input passes for the wrong reason.
            source_raw, source_fields = frontmatter_of(instance / GEN / LIFE)
            check(
                all(f in source_fields for f in bl.PROVENANCE_FIELDS),
                f"positive control: the source frontmatter parses and holds all "
                f"five provenance fields {bl.PROVENANCE_FIELDS}",
            )
            check_in(
                REASON_CONTINUATION,
                source_raw,
                "positive control: the source frontmatter carries the reason's "
                "second line, so the absence check below can fail",
            )

            done = promote(instance, "lifetimes-and-borrows", bundle)
            check(done.returncode == 0, f"exit 0 (got {done.returncode})")
            raw, fields = frontmatter_of(bundle / "lessons" / PROMOTED)
            for field in bl.PROVENANCE_FIELDS:
                check(
                    field not in fields,
                    f"{field!r} is absent from the promoted frontmatter "
                    f"(parsed keys: {sorted(fields)})",
                )
            # The block scalar's continuation lines must go with it. If one
            # were left behind the frontmatter would either not parse (caught
            # by frontmatter_of above) or would parse with junk in it.
            check_not_in(
                REASON_CONTINUATION,
                raw,
                "no orphan continuation line from the multi-line `reason: >` "
                "survives in the promoted frontmatter",
            )
            check(
                sorted(fields) == ["design_refs", "id", "title", "validators"],
                f"the promoted frontmatter holds exactly the four authoring "
                f"fields (got {sorted(fields)})",
            )
            check_in(
                "stripped generated, generated_at, kind, reason, after",
                done.output,
                "the output names all five stripped fields",
            )
            learner.still_there("A3")

    with case("A4  step 7: the manifest lists the new path at position 4"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)
            before_manifest, _ = bl.load_manifest(bundle)
            check(
                before_manifest["lessons"][4] == "lessons/04-richer-typed-schemas.md",
                "positive control: before the run, index 4 is the bundle's own "
                "04- lesson, so the assertion below records a change",
            )
            done = promote(instance, "lifetimes-and-borrows", bundle)
            check(done.returncode == 0, f"exit 0 (got {done.returncode})")
            manifest, _ = bl.load_manifest(bundle)
            lessons = manifest["lessons"]
            check(len(lessons) == 24, f"the list grew from 23 to 24 (got {len(lessons)})")
            check(
                lessons[3] == "lessons/03-first-refactor.md",
                f"index 3 is still lessons/03-first-refactor.md (got {lessons[3]!r})",
            )
            check(
                lessons[4] == f"lessons/{PROMOTED}",
                f"index 4 is lessons/{PROMOTED} (got {lessons[4]!r})",
            )
            check(
                lessons[5] == "lessons/04-richer-typed-schemas.md",
                f"the previously-index-4 lesson moved to index 5 "
                f"(got {lessons[5]!r})",
            )
            check(
                lessons.count(f"lessons/{PROMOTED}") == 1,
                "the new path is listed exactly once",
            )
            learner.still_there("A4")

    with case("A5  step 9: the learner's copy stays, and the output says why"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)
            done = promote(instance, "lifetimes-and-borrows", bundle)
            check(done.returncode == 0, f"exit 0 (got {done.returncode})")
            learner.still_there("A5")
            check_in(
                "the learner's copy is NOT touched",
                done.output,
                "the plan says the learner's copy is not touched",
            )
            check_in(
                f"{instance}/{GEN}/{LIFE} stays where it is.",
                done.output,
                "step 9 names the learner's file by path and says it stays",
            )
            check_in(
                "share a slug",
                done.output,
                "step 9 explains the duplicate-slug situation the copy creates",
            )
            check_in(
                "re-materialization",
                done.output,
                "step 9 says when the duplicate becomes visible: at "
                "re-materialization, when the learner takes a revision",
            )
            check_in(
                "the tutor deletes it then",
                done.output,
                "step 9 says who removes the draft, and when",
            )

    with case("A6  steps 4 and 8 are judgement and are NOT claimed as done"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)
            done = promote(instance, "lifetimes-and-borrows", bundle)
            check(done.returncode == 0, f"exit 0 (got {done.returncode})")
            # The plan block prints one line per MECHANICAL step it performed.
            # Reading the numbers back out is the value assertion: 4 and 8 must
            # not be in it, because claiming them is the failure this guards.
            claimed = re.findall(r"^  (\d+)  ", done.output, re.M)
            check(
                claimed == ["1", "2", "3", "5", "6", "7"],
                f"the plan claims exactly steps 1,2,3,5,6,7 as done "
                f"(got {claimed})",
            )
            check_in(
                "TWO STEPS OF THE PROCEDURE ARE NOT DONE",
                done.output,
                "the output states plainly that two steps were not done",
            )
            check_in(
                "this tool has not attempted either",
                done.output,
                "the output disclaims having attempted them",
            )
            check_in(
                "STEP 4 - rewrite it for a learner who has not started.",
                done.output,
                "step 4 is named as the author's, in words",
            )
            check_in(
                "STEP 8 - update COURSE.md",
                done.output,
                "step 8 is named as the author's, in words",
            )
            check_in(
                f"{bundle}/COURSE.md",
                done.output,
                "step 8 names the COURSE.md file by path",
            )
            check_in(
                "NOT exhaustive, and a clean scan proves",
                done.output,
                "the generalisation scan is labelled as a heuristic that proves "
                "nothing when it is clean",
            )
            learner.still_there("A6")

    with case("A7  step 10: the validator ran, passed, and passes again independently"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)
            done = promote(instance, "lifetimes-and-borrows", bundle)
            check(done.returncode == 0, f"exit 0 (got {done.returncode})")
            validator, how = bl.find_validator()
            check_in(
                str(validator),
                done.output,
                "the output names the validator it ran, by path",
            )
            check_in("PASS", done.output, "the output reports the validator as PASS")
            learner.still_there("A7")

            # Re-run the runner's validator myself. The tool reporting PASS is
            # the tool grading its own homework; this is an independent read.
            mine = subprocess.run(
                [sys.executable, str(validator), str(bundle)],
                capture_output=True,
                text=True,
            )
            check(
                mine.returncode == 0,
                f"an independent run of {validator.name} against the promoted "
                f"bundle exits 0 (got {mine.returncode}: "
                f"{mine.stdout.strip()[-200:]})",
            )
            # POSITIVE CONTROL for that probe. A validator invocation that
            # cannot fail proves nothing about the bundle; break a copy in a
            # way the validator must report, and show the same call fail.
            broken = ws.copy("rust-automaton-db", "broken")
            os.remove(broken / "DESIGN.md")
            control = subprocess.run(
                [sys.executable, str(validator), str(broken)],
                capture_output=True,
                text=True,
            )
            check(
                control.returncode != 0,
                f"positive control: the same validator call reports a bundle "
                f"with DESIGN.md removed as bad (got {control.returncode})",
            )

    with case("A8  --check prints the plan and writes nothing, to either side"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)
            bundle_before = tree_digest(bundle)
            done = promote(instance, "lifetimes-and-borrows", bundle, "--check")
            check(done.returncode == 0, f"exit 0 (got {done.returncode})")
            check_in(
                "--check: nothing was written",
                done.output,
                "--check says nothing was written",
            )
            check_in(
                f"-> {bundle}/lessons/{PROMOTED}",
                done.output,
                "--check still prints the plan, including the target path",
            )
            check_in("PASS", done.output, "--check still ran the validator")
            check(
                tree_digest(bundle) == bundle_before,
                "the bundle is byte-identical after --check",
            )
            check(
                not has_exactly(bundle / "lessons", PROMOTED),
                f"lessons/ does not hold {PROMOTED} after --check",
            )
            learner.still_there("A8")

            # POSITIVE CONTROL: the identical command WITHOUT --check does
            # change the same bundle. Otherwise "nothing changed" would also
            # be satisfied by a promote that silently did nothing at all.
            again = promote(instance, "lifetimes-and-borrows", bundle)
            check(again.returncode == 0, f"positive control exits 0 (got {again.returncode})")
            check(
                tree_digest(bundle) != bundle_before,
                "positive control: without --check the same command does change "
                "the bundle",
            )
            check(
                has_exactly(bundle / "lessons", PROMOTED),
                f"positive control: without --check, lessons/ holds {PROMOTED}",
            )
            learner.still_there("A8 control")

    # ------------------------------------------------------------------
    # B. The refusals. Each one firing, each one with a control.
    # ------------------------------------------------------------------

    with case("B1  step 5: a design_ref the BUNDLE's DESIGN.md has never had"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance, SIBLING)
            bundle_before = tree_digest(bundle)

            # The fixture's shape, asserted rather than assumed: the anchor is
            # in the instance's DESIGN.md and not in the bundle's. If that ever
            # stopped being true this case would "pass" while testing nothing.
            bundle_design = (bundle / "DESIGN.md").read_text(encoding="utf-8")
            instance_design = (instance / "DESIGN.md").read_text(encoding="utf-8")
            check(
                "{#client-sibling-resolution}" not in bundle_design,
                "fixture: the bundle's DESIGN.md has no client-sibling-resolution "
                "anchor",
            )
            check_in(
                "{#client-sibling-resolution}",
                instance_design,
                "fixture: the instance's DESIGN.md does have that anchor",
            )

            done = promote(instance, "sibling-resolution", bundle)
            check(done.returncode != 0, f"non-zero exit (got {done.returncode})")
            check_in(
                "step 5 of the promotion procedure fails",
                done.output,
                "the refusal names the step it belongs to",
            )
            check_in(
                "client-sibling-resolution",
                done.output,
                "the refusal names the unresolved anchor",
            )
            check_in(
                "DESIGN.md GREW during the course",
                done.output,
                "the refusal explains WHY: the instance's DESIGN.md grew while "
                "the course ran",
            )
            # The actionable half: the section text is printed so the author can
            # move it across without opening the learner's instance.
            check_in(
                "picks the highest write timestamp",
                done.output,
                "the refusal prints the section text from the INSTANCE's "
                "DESIGN.md, so the author can move it across",
            )
            check_in(
                "## Client-side sibling resolution {#client-sibling-resolution}",
                done.output,
                "the printed section includes its heading and anchor",
            )
            check_in(
                "Nothing was written",
                done.output,
                "the refusal says nothing was written",
            )
            check(
                tree_digest(bundle) == bundle_before,
                "the bundle is byte-identical after the refusal",
            )
            check(
                not has_exactly(bundle / "lessons", "04-sibling-resolution.md"),
                "no lesson file was left behind",
            )
            learner.still_there("B1")

            # POSITIVE CONTROL. Add the missing section to THIS bundle's
            # DESIGN.md and run the identical command. If it now succeeds, the
            # refusal was about the anchor and nothing else - a dirty tree, a
            # bad path or a missing validator would still refuse here.
            section = instance_design[instance_design.index("## Client-side sibling resolution") :]
            with (bundle / "DESIGN.md").open("a", encoding="utf-8") as handle:
                handle.write("\n" + section.rstrip() + "\n")
            control = promote(instance, "sibling-resolution", bundle)
            check(
                control.returncode == 0,
                f"positive control: with the anchor added to the bundle's "
                f"DESIGN.md the same promote succeeds (got {control.returncode}: "
                f"{control.output.strip()[:200]})",
            )
            check(
                has_exactly(bundle / "lessons", "04-sibling-resolution.md"),
                "positive control: the lesson is now in lessons/",
            )
            learner.still_there("B1 control")

    with case("B2  step 6: a validator name the manifest does not declare"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            # Written into the INSTANCE COPY, never into the fixture.
            lesson = instance / GEN / "clippy-detour.md"
            lesson.write_text(
                "---\n"
                "id: clippy-detour\n"
                "title: A clippy detour\n"
                "design_refs: [row-cell-model]\n"
                "validators: [cargo-clippy]\n"
                "generated: true\n"
                "generated_at: 2026-09-12\n"
                "kind: side-lesson\n"
                "reason: The learner asked what clippy is for.\n"
                "after: lessons/03-first-refactor.md\n"
                "---\n"
                "\n"
                "## Purpose\n"
                "\n"
                "Read what the linter says and decide which of it to act on.\n"
                "\n"
                "## Completion conditions\n"
                "\n"
                "The linter reports nothing the lesson has not explained.\n",
                encoding="utf-8",
            )
            learner = Learner(instance, "clippy-detour.md")
            declared = bl.load_bundle(bundle).declared_validators()
            check(
                "cargo-clippy" not in declared and "cargo-check" in declared,
                f"fixture: the manifest declares cargo-check and not cargo-clippy "
                f"(declares {sorted(declared)})",
            )
            bundle_before = tree_digest(bundle)

            done = promote(instance, "clippy-detour", bundle)
            check(done.returncode != 0, f"non-zero exit (got {done.returncode})")
            check_in(
                "step 6 of the promotion procedure fails",
                done.output,
                "the refusal names the step it belongs to",
            )
            check_in(
                "cargo-clippy",
                done.output,
                "the refusal names the undeclared validator",
            )
            check_in(
                "'validators' map",
                done.output,
                "the refusal points at the manifest's validators map",
            )
            check_in(
                f"{bundle}/tutorial.yaml",
                done.output,
                "the refusal names the manifest by path",
            )
            check(
                tree_digest(bundle) == bundle_before,
                "the bundle is byte-identical after the refusal",
            )
            learner.still_there("B2")

            # POSITIVE CONTROL: change the ONE field the refusal was about to a
            # declared name and run the identical command.
            lesson.write_text(
                lesson.read_text(encoding="utf-8").replace(
                    "validators: [cargo-clippy]", "validators: [cargo-check]"
                ),
                encoding="utf-8",
            )
            control_learner = Learner(instance, "clippy-detour.md")
            control = promote(instance, "clippy-detour", bundle)
            check(
                control.returncode == 0,
                f"positive control: with validators: [cargo-check] the same "
                f"promote succeeds (got {control.returncode}: "
                f"{control.output.strip()[:200]})",
            )
            check(
                has_exactly(bundle / "lessons", "04-clippy-detour.md"),
                "positive control: the lesson is now in lessons/",
            )
            control_learner.still_there("B2 control")

    with case("B3  a slug that already exists under a different number"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            lesson = instance / GEN / "first-refactor.md"
            lesson.write_text(
                "---\n"
                "id: first-refactor\n"
                "title: Another take on the first refactor\n"
                "design_refs: []\n"
                "validators: [manual]\n"
                "generated: true\n"
                "generated_at: 2026-09-12\n"
                "kind: side-lesson\n"
                "reason: The learner wanted a second pass over the same ground.\n"
                "after: lessons/10-storage-durability.md\n"
                "---\n"
                "\n"
                "## Purpose\n"
                "\n"
                "Revisit the refactor with the storage engine in view.\n"
                "\n"
                "## Completion conditions\n"
                "\n"
                "The seams named in the earlier lesson are still the seams.\n",
                encoding="utf-8",
            )
            learner = Learner(instance, "first-refactor.md")
            check(
                has_exactly(bundle / "lessons", "03-first-refactor.md"),
                "fixture: the bundle already holds 03-first-refactor.md",
            )
            bundle_before = tree_digest(bundle)
            done = promote(instance, "first-refactor", bundle)
            check(done.returncode != 0, f"non-zero exit (got {done.returncode})")
            check_in(
                "'03-first-refactor'",
                done.output,
                "the refusal names the lesson it would collide with",
            )
            check_in(
                "same lesson under a different number",
                done.output,
                "the refusal explains that the collision is by name, not number",
            )
            check(
                tree_digest(bundle) == bundle_before,
                "the bundle is byte-identical after the refusal",
            )
            check(
                not has_exactly(bundle / "lessons", "11-first-refactor.md"),
                "the second 11- copy was not written",
            )
            learner.still_there("B3")

            # POSITIVE CONTROL: rename the id so nothing collides. Same file,
            # same position, same bundle - only the name differs.
            lesson.write_text(
                lesson.read_text(encoding="utf-8").replace(
                    "id: first-refactor", "id: second-refactor"
                ),
                encoding="utf-8",
            )
            control_learner = Learner(instance, "first-refactor.md")
            control = promote(instance, "first-refactor", bundle)
            check(
                control.returncode == 0,
                f"positive control: with a non-colliding id the same promote "
                f"succeeds (got {control.returncode}: "
                f"{control.output.strip()[:200]})",
            )
            check(
                has_exactly(bundle / "lessons", "11-second-refactor.md"),
                "positive control: lessons/ holds 11-second-refactor.md",
            )
            control_learner.still_there("B3 control")

    with case("B4  a generated-lesson path that names nothing"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)
            bundle_before = tree_digest(bundle)
            done = promote(instance, "lifetymes", bundle)
            check(done.returncode != 0, f"non-zero exit (got {done.returncode})")
            check_in(
                "does not name a generated lesson",
                done.output,
                "the error says the argument named nothing",
            )
            check_in(
                "The instance holds:",
                done.output,
                "the error offers what the instance actually holds",
            )
            # The value, not the shape: the listing must be the real contents.
            for name in (LIFE, SIBLING):
                check_in(
                    f"{GEN}/{name}",
                    done.output,
                    f"the listing names {GEN}/{name}, which is really there",
                )
            check_in(
                "Tried: lifetymes, lessons.generated/lifetymes, "
                "lessons.generated/lifetymes.md",
                done.output,
                "the error says which three forms it tried",
            )
            check(
                tree_digest(bundle) == bundle_before,
                "the bundle is byte-identical after the refusal",
            )
            learner.still_there("B4")
            # POSITIVE CONTROL: the same resolver, given a name that IS there,
            # resolves it. Case B8 is that control, run against all three forms.

    with case("B5  a generated lesson with no frontmatter at all"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            bare = instance / GEN / "bare-draft.md"
            bare.write_text(
                "## Purpose\n\nSomething the tutor started and never framed.\n",
                encoding="utf-8",
            )
            learner = Learner(instance, "bare-draft.md")
            bundle_before = tree_digest(bundle)
            done = promote(instance, "bare-draft", bundle)
            check(done.returncode != 0, f"non-zero exit (got {done.returncode})")
            check_in(
                "has no YAML frontmatter, so it is not a lesson",
                done.output,
                "the refusal says what is wrong, in words",
            )
            check_in(
                "id, title and its five provenance fields",
                done.output,
                "the refusal says what a generated lesson must declare",
            )
            check(
                tree_digest(bundle) == bundle_before,
                "the bundle is byte-identical after the refusal",
            )
            learner.still_there("B5")

            # POSITIVE CONTROL: give the same file a frontmatter and nothing
            # else changes. This proves the refusal was about the frontmatter
            # and not about the file being new, or oddly named, or empty.
            bare.write_text(
                "---\n"
                "id: bare-draft\n"
                "title: A draft that now has a frontmatter\n"
                "design_refs: []\n"
                "validators: [manual]\n"
                "generated: true\n"
                "generated_at: 2026-09-12\n"
                "kind: side-lesson\n"
                "reason: The tutor framed it on the second pass.\n"
                "after: lessons/03-first-refactor.md\n"
                "---\n"
                "\n"
                "## Purpose\n"
                "\n"
                "Something the tutor started and then framed.\n"
                "\n"
                "## Completion conditions\n"
                "\n"
                "The draft reads as a lesson rather than as a note.\n",
                encoding="utf-8",
            )
            control_learner = Learner(instance, "bare-draft.md")
            control = promote(instance, "bare-draft", bundle)
            check(
                control.returncode == 0,
                f"positive control: with a frontmatter the same promote "
                f"succeeds (got {control.returncode}: "
                f"{control.output.strip()[:200]})",
            )
            check(
                has_exactly(bundle / "lessons", "04-bare-draft.md"),
                "positive control: the lesson is now in lessons/",
            )
            control_learner.still_there("B5 control")

    with case("B6  a dirty git working tree under the bundle"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            git_init(bundle)
            (bundle / "stray-note.txt").write_text("half an idea\n", encoding="utf-8")
            learner = Learner(instance)
            bundle_before = tree_digest(bundle)
            done = promote(instance, "lifetimes-and-borrows", bundle)
            check(done.returncode != 0, f"non-zero exit (got {done.returncode})")
            check_in(
                "uncommitted change(s)",
                done.output,
                "the refusal says the tree is dirty",
            )
            check_in(
                "?? stray-note.txt",
                done.output,
                "the refusal names the file that made it dirty",
            )
            check_in(
                "Pass --force to run anyway",
                done.output,
                "the refusal names the override",
            )
            check(
                tree_digest(bundle) == bundle_before,
                "the bundle is byte-identical after the refusal",
            )
            check(
                not has_exactly(bundle / "lessons", PROMOTED),
                f"lessons/ does not hold {PROMOTED} after the refusal",
            )
            learner.still_there("B6")

            # --force overrides, on the SAME dirty tree.
            forced = promote(instance, "lifetimes-and-borrows", bundle, "--force")
            check(
                forced.returncode == 0,
                f"--force runs anyway on the same dirty tree "
                f"(got {forced.returncode}: {forced.output.strip()[:200]})",
            )
            check(
                has_exactly(bundle / "lessons", PROMOTED),
                f"--force: lessons/ holds {PROMOTED}",
            )
            check_in(
                "--force was given, so the run continues",
                forced.output,
                "--force says so rather than passing silently",
            )
            learner.still_there("B6 force")

            # POSITIVE CONTROL: a CLEAN git tree, same fixtures, no --force.
            # This is what proves the refusal was about the dirt and not about
            # the bundle being a git repository at all.
            clean_bundle, clean_instance = pair(ws, "-clean")
            git_init(clean_bundle)
            clean_learner = Learner(clean_instance)
            control = promote(clean_instance, "lifetimes-and-borrows", clean_bundle)
            check(
                control.returncode == 0,
                f"positive control: a clean git tree promotes without --force "
                f"(got {control.returncode}: {control.output.strip()[:200]})",
            )
            check(
                has_exactly(clean_bundle / "lessons", PROMOTED),
                f"positive control: lessons/ holds {PROMOTED}",
            )
            clean_learner.still_there("B6 control")

    with case("B7  a validator that reports findings discards the whole promotion"):
        with Workspace() as ws:
            bundle, instance = pair(ws)
            learner = Learner(instance)
            stub = write_stub_validator(ws.root)
            bundle_before = tree_digest(bundle)
            done = promote(
                instance,
                "lifetimes-and-borrows",
                bundle,
                env={"TUTORAIL_VALIDATOR": str(stub)},
            )
            check(done.returncode != 0, f"non-zero exit (got {done.returncode})")
            check_in(
                "would leave the bundle invalid",
                done.output,
                "the message says the edit was rejected by the validator",
            )
            check_in(
                f"{bundle} is unchanged",
                done.output,
                "the message says the bundle is unchanged, and names it",
            )
            check_in(
                "[check  9] DESIGN.md: the file is required and is missing",
                done.output,
                "the finding the validator reported is quoted back",
            )
            check(
                tree_digest(bundle) == bundle_before,
                "the bundle is byte-identical: the staged copy was thrown away",
            )
            check(
                not has_exactly(bundle / "lessons", PROMOTED),
                f"lessons/ does not hold {PROMOTED}",
            )
            manifest, _ = bl.load_manifest(bundle)
            check(
                len(manifest["lessons"]) == 23
                and f"lessons/{PROMOTED}" not in manifest["lessons"],
                "tutorial.yaml was not half-edited either",
            )
            learner.still_there("B7")

            # POSITIVE CONTROL: the identical command with the REAL validator.
            # Without it, "it refused" is equally consistent with promote being
            # broken for this lesson, this bundle, or in general.
            control = promote(
                instance,
                "lifetimes-and-borrows",
                bundle,
                env={"TUTORAIL_VALIDATOR": None},
            )
            check(
                control.returncode == 0,
                f"positive control: the same command with the real validator "
                f"succeeds (got {control.returncode}: "
                f"{control.output.strip()[:200]})",
            )
            check(
                has_exactly(bundle / "lessons", PROMOTED),
                f"positive control: lessons/ holds {PROMOTED}",
            )
            learner.still_there("B7 control")

    with case("B8  bare slug, relative path and absolute path all name the same lesson"):
        with Workspace() as ws:
            forms = {
                "bare slug": lambda inst: "lifetimes-and-borrows",
                "relative path": lambda inst: f"{GEN}/{LIFE}",
                "absolute path": lambda inst: str(inst / GEN / LIFE),
            }
            digests: dict[str, str] = {}
            for index, (label, make) in enumerate(forms.items()):
                bundle, instance = pair(ws, f"-{index}")
                learner = Learner(instance)
                done = promote(instance, make(instance), bundle)
                check(
                    done.returncode == 0,
                    f"{label}: exit 0 (got {done.returncode}: "
                    f"{done.output.strip()[:200]})",
                )
                check(
                    has_exactly(bundle / "lessons", PROMOTED),
                    f"{label}: lessons/ holds {PROMOTED}",
                )
                _, fields = frontmatter_of(bundle / "lessons" / PROMOTED)
                check(
                    fields.get("id") == PROMOTED_ID,
                    f"{label}: id == {PROMOTED_ID!r} (got {fields.get('id')!r})",
                )
                digests[label] = tree_digest(bundle)
                learner.still_there(f"B8 {label}")
            # The strongest form of "the same result": the three bundles are
            # byte-identical to each other, not merely each plausible.
            check(
                len(set(digests.values())) == 1,
                f"all three forms leave byte-identical bundles (digests: "
                f"{ {k: v[:12] for k, v in digests.items()} })",
            )

    return report("test_promote.py")


if __name__ == "__main__":
    sys.exit(main())
