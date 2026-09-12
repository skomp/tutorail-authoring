#!/usr/bin/env python3
"""Promote a generated lesson out of a learner's instance into a bundle.

Usage:
    promote.py <instance> <generated-lesson-path> <bundle> [--check] [--force]
    promote.py <instance> <generated-lesson-path> <bundle> --optional
               [--confirm] [--check] [--force]

`--optional` promotes into `optional_lessons` instead of onto the main path.
The lesson then has no position, so step 7 becomes "no position", the file
keeps a slug with no number prefix, and nothing is renumbered. The offer
metadata is DERIVED - `offer_at` from the lesson's `after:`, `offer_because`
from its `reason:` - printed, and written only when `--confirm` says the
author has read and agreed with both. Without `--confirm` (and without
`--check`) the run prints the two values and refuses, writing nothing.

`<instance>` is the materialized tutorial directory - the one holding
STATE.md, tutorial.yaml and lessons.generated/. `<generated-lesson-path>` may
be given relative to it (`lessons.generated/lifetimes.md`), as an absolute
path, or as the bare slug.

This implements the ten-step procedure in bundle-format.md section 8. Six of
the ten steps are mechanical and are done here. Two are judgement and are
NOT done here; they are printed as required manual steps, because a tool that
claimed to have generalised one learner's prose would be writing the course.
One - "say what happens to the learner's copy" - is an explanation, printed.
The last is re-running the validator, which every mutating operation in this
toolkit does anyway.

    1  copy into lessons/ under this course's numbering      done here
    2  set id to the new slug                                done here
    3  strip the five provenance fields                      done here
    4  rewrite it for a learner who has not started          YOURS
    5  re-check design_refs against the BUNDLE's DESIGN.md   done here
    6  check every validators name is declared               done here
    7  add the path to lessons, at the right position        done here
    8  update COURSE.md                                      YOURS
    9  say what happens to the learner's copy                explained
    10 re-run the self-check and the validator               validator here

Step 5 is the one authoring alone never needs and the easiest to skip: the
instance's DESIGN.md GREW during the course, so a generated lesson can name
an anchor the tutor appended, which the bundle's DESIGN.md has never had.
When that happens this refuses, and prints the section from the instance's
DESIGN.md so it can be moved across.

The learner's copy is never deleted. Promotion is a bundle-side act.

Exit codes:
    0  promoted (or, with --check, the plan validates and nothing was written)
    2  usage, I/O, a refused run, an unresolved design_ref, or a validator
       failure
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import bundlelib as bl
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import bundlelib as bl


# --------------------------------------------------------------------------
# Locating the generated lesson
# --------------------------------------------------------------------------


def resolve_generated(instance: Path, given: str) -> tuple[Path, str]:
    """Return (path, rel) for the generated lesson. Raises with a usable list."""
    generated_dir = instance / bl.GENERATED_DIR
    candidates: list[str] = []
    if bl.GENERATED_DIR in bl.list_dir(instance):
        candidates = [
            name
            for name in bl.list_dir(generated_dir)
            if name.endswith(".md") and not name.startswith(".")
        ]

    given = given.strip()
    tries: list[str] = []
    absolute = Path(given)
    if absolute.is_absolute():
        if absolute.is_file():
            try:
                return absolute, absolute.relative_to(instance).as_posix()
            except ValueError:
                return absolute, absolute.name
        tries.append(str(absolute))
    else:
        for rel in (
            given,
            f"{bl.GENERATED_DIR}/{given}",
            f"{bl.GENERATED_DIR}/{given}.md",
        ):
            resolved, _ = bl.resolve_exact(instance, rel)
            if resolved is not None and resolved.is_file():
                return resolved, rel
            tries.append(rel)

    listing = (
        "\n".join(f"    {bl.GENERATED_DIR}/{name}" for name in candidates)
        if candidates
        else f"    (the instance has no {bl.GENERATED_DIR}/ directory, or it is empty)"
    )
    raise bl.ToolError(
        f"{given!r} does not name a generated lesson in {instance}.\n"
        f"Tried: {', '.join(tries)}\n"
        f"The instance holds:\n{listing}"
    )


def read_lesson(path: Path) -> tuple[dict, str]:
    text = bl.read_text(path)
    if text is None:
        raise bl.ToolError(f"{path}: could not be read as UTF-8 text.")
    raw, _ = bl.split_frontmatter(text)
    if raw is None:
        raise bl.ToolError(
            f"{path}: has no YAML frontmatter, so it is not a lesson. A generated "
            f"lesson declares id, title and its five provenance fields."
        )
    try:
        parsed = bl.load_yaml(raw, path.name + " frontmatter")
    except bl.YamlError as exc:
        raise bl.ToolError(f"{path}: the frontmatter does not parse: {exc}") from exc
    if not isinstance(parsed, dict):
        raise bl.ToolError(f"{path}: the frontmatter is not a mapping.")
    return parsed, text


# --------------------------------------------------------------------------
# Step 5: design_refs against the BUNDLE's DESIGN.md
# --------------------------------------------------------------------------

_SECTION_RE = re.compile(r"^(#{1,6})[ \t]+(?P<title>.*?)\{#(?P<anchor>[^}]+)\}[ \t]*$")


def design_section(design_text: str, anchor: str) -> str:
    """Return the DESIGN.md section that carries `anchor`, heading included."""
    lines = design_text.split("\n")
    start = None
    level = 0
    for index, line in enumerate(lines):
        match = _SECTION_RE.match(line)
        if match and match.group("anchor") == anchor:
            start = index
            level = len(match.group(1))
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start + 1, len(lines)):
        heading = re.match(r"^(#{1,6})[ \t]", lines[index])
        if heading and len(heading.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end]).rstrip()


def check_design_refs(
    refs: list[str], bundle: bl.Bundle, instance: Path, source_rel: str
) -> None:
    anchors = bundle.design_anchors()
    missing = [ref for ref in refs if ref not in anchors]
    if not missing:
        return
    instance_design = bl.read_text(instance / "DESIGN.md") or ""
    blocks = []
    for anchor in missing:
        section = design_section(instance_design, anchor)
        if section:
            blocks.append(
                f"  --- {anchor}: the instance's DESIGN.md has this section ---\n"
                + "\n".join(f"  {line}" for line in section.split("\n"))
            )
        else:
            blocks.append(
                f"  --- {anchor}: the instance's DESIGN.md has no such anchor "
                f"either; the reference was already dangling ---"
            )
    raise bl.ToolError(
        f"step 5 of the promotion procedure fails: {source_rel} names "
        f"{len(missing)} design_ref(s) that {bundle.root}/DESIGN.md does not "
        f"have: {', '.join(missing)}.\n"
        f"\n"
        f"This is the step authoring alone never needs. The instance's DESIGN.md "
        f"GREW during the course - the tutor appended decisions the learner made - "
        f"so a generated lesson can reference an anchor your bundle has never had.\n"
        f"\n"
        f"For each one: add the section to the bundle's DESIGN.md, or remove the "
        f"reference from the lesson. Nothing was written.\n"
        f"\n" + "\n\n".join(blocks)
    )


# --------------------------------------------------------------------------
# Step 4: the part this tool must not claim to have done
# --------------------------------------------------------------------------

_LEARNER_TELLS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("addresses the learner directly", re.compile(r"\byour\b|\byou\b|\byou're\b", re.I)),
    ("names a workspace file", re.compile(r"\b(?:src|tests|models|dist)/[\w./-]+")),
    ("quotes a compiler or runtime message", re.compile(r"\b(?:error\[?E?\d+\]?|panicked at|warning:)")),
    ("embeds code", re.compile(r"^```", re.M)),
)


def survey_for_generalisation(body: str) -> list[tuple[str, int, str]]:
    """Heuristic, deliberately not exhaustive. Returns (label, count, sample)."""
    out = []
    for label, pattern in _LEARNER_TELLS:
        hits = list(pattern.finditer(body))
        if hits:
            line = body[: hits[0].start()].count("\n") + 1
            out.append((label, len(hits), f"line {line}: {hits[0].group(0)!r}"))
    return out


# --------------------------------------------------------------------------


def body_slug_of(frontmatter: dict, source: Path, source_rel: str) -> str:
    """Steps 1 and 2's input: the lesson's slug with any number prefix off."""
    _, body_slug = bl.split_number_prefix(str(frontmatter.get("id", "")).strip())
    if not body_slug:
        body_slug = bl.split_number_prefix(source.stem)[1]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", body_slug):
        raise bl.ToolError(
            f"{source_rel}: neither its id ({frontmatter.get('id')!r}) nor its "
            f"filename gives a usable slug of lowercase words. Rename it first."
        )
    return body_slug


def refuse_slug_clash(
    bundle: bl.Bundle, bundle_root: Path, slug: str, body_slug: str, rel: str
) -> None:
    if slug in {lesson.slug for lesson in bundle.lessons}:
        raise bl.ToolError(f"{bundle_root}/{rel} already exists; nothing was written.")
    clash = [
        lesson.slug
        for lesson in bundle.lessons
        if bl.split_number_prefix(lesson.slug)[1] == body_slug
    ]
    if clash:
        raise bl.ToolError(
            f"the bundle already has {clash[0]!r}, which is the same lesson under "
            f"a different number. Promoting would give the course two lessons with "
            f"one name. Nothing was written."
        )


def check_steps_5_and_6(
    frontmatter: dict,
    bundle: bl.Bundle,
    bundle_root: Path,
    instance: Path,
    source_rel: str,
) -> tuple[list[str], list[str]]:
    """Steps 5 and 6, run before anything is copied. Returns (refs, validators)."""
    refs = frontmatter.get("design_refs")
    ref_names = [str(r).lstrip("#") for r in refs] if isinstance(refs, list) else []
    check_design_refs(ref_names, bundle, instance, source_rel)

    validators = frontmatter.get("validators")
    validator_names = [str(v) for v in validators] if isinstance(validators, list) else []
    undeclared = [v for v in validator_names if v not in bundle.declared_validators()]
    if undeclared:
        raise bl.ToolError(
            f"step 6 of the promotion procedure fails: {source_rel} names "
            f"validator(s) {', '.join(undeclared)}, which {bundle_root}/"
            f"tutorial.yaml does not declare. Declare them in the manifest's "
            f"'validators' map, or remove them from the lesson. Nothing was written."
        )
    return ref_names, validator_names


def strip_provenance(source_text: str, frontmatter: dict, source_rel: str, slug: str) -> tuple[str, list[str]]:
    """Step 3, plus step 2's id rewrite. Returns (text, fields removed)."""
    text, removed = bl.strip_frontmatter_fields(source_text, bl.PROVENANCE_FIELDS)
    text, _ = bl.set_frontmatter_field(text, "id", slug)
    left_behind = [
        field for field in bl.PROVENANCE_FIELDS if field in frontmatter and field not in removed
    ]
    if left_behind:
        raise bl.ToolError(
            f"the provenance field(s) {', '.join(left_behind)} could not be removed "
            f"from the frontmatter of {source_rel}. Every one of the five describes "
            f"one learner's run, so a promotion that left one behind would put "
            f"progress into a bundle. Nothing was written."
        )
    return text, removed


# --------------------------------------------------------------------------
# --optional: promotion into the offered set
#
# The offer metadata is DERIVED from the lesson's own provenance and then
# confirmed by the author:
#
#     offer_at      <- the generated lesson's `after`
#     offer_because <- the generated lesson's `reason`
#
# Deriving judgement from data is normally the wrong move. It is right here
# because the provenance is the best evidence anyone will ever have about
# when this lesson is needed: a real learner needed it at exactly that point,
# which is a stronger signal than an author's recollection. Confirmation is
# what keeps the decision with the author, so the run REFUSES to write until
# it is given --confirm, and prints both derived values first. That is the
# same check-then-apply discipline as --check, with the plan reduced to the
# two fields a person has to agree with.
# --------------------------------------------------------------------------


def derive_offer(frontmatter: dict, bundle: bl.Bundle, source_rel: str) -> dict:
    after = frontmatter.get("after")
    if not isinstance(after, str) or not after.strip():
        raise bl.ToolError(
            f"{source_rel} carries no usable 'after:' field, so there is "
            f"nothing to derive 'offer_at' from. An optional lesson must say "
            f"where the tutor offers it, and this promotion takes that from "
            f"the point the learner needed the lesson. Nothing was written."
        )
    after = after.strip()
    if after not in bundle.listed:
        raise bl.ToolError(
            f"{source_rel} names 'after: {after}', which is not an entry in "
            f"this bundle's lessons list, so it cannot be an offer point. "
            f"Every offer point is a place on the main path. Nothing was "
            f"written."
        )
    reason = frontmatter.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        raise bl.ToolError(
            f"{source_rel} carries no usable 'reason:' field, so there is "
            f"nothing to derive 'offer_because' from. The tutor says that "
            f"sentence to the learner when it raises the offer, and nothing "
            f"incomplete is written. Nothing was written."
        )
    # A folded block scalar (`reason: >`) arrives with its newlines folded to
    # spaces and a trailing one; the entry is a single-line scalar, so the
    # whitespace is normalised and the result is PRINTED for confirmation
    # rather than written unseen.
    return {"offer_at": [after], "offer_because": " ".join(reason.split())}


def promote_optional(
    args: argparse.Namespace,
    instance: Path,
    bundle_root: Path,
    bundle: bl.Bundle,
    source: Path,
    source_rel: str,
    frontmatter: dict,
    source_text: str,
) -> int:
    entry = derive_offer(frontmatter, bundle, source_rel)
    slug = body_slug_of(frontmatter, source, source_rel)
    rel = f"lessons/{slug}.md"
    refuse_slug_clash(bundle, bundle_root, slug, slug, rel)
    ref_names, validator_names = check_steps_5_and_6(
        frontmatter, bundle, bundle_root, instance, source_rel
    )
    stripped_text, removed = strip_provenance(source_text, frontmatter, source_rel, slug)
    stripped_text, changed = bl.set_frontmatter_field(stripped_text, "optional", "true")
    if not changed:
        raise bl.ToolError(
            f"{source_rel}: 'optional: true' could not be written into the "
            f"frontmatter, so the lesson file and the optional_lessons list "
            f"would disagree (the runner's check 20). Nothing was written."
        )

    print(f"promote: {instance}/{source_rel}")
    print(f"      -> {bundle_root}/{rel}   OPTIONAL - offered, not sequenced")
    print()
    print(f"  1  copy               kind={frontmatter.get('kind')!r}; the learner's copy is NOT touched")
    print(f"  2  id                 {frontmatter.get('id')!r} -> {slug!r}")
    print(
        f"  3  provenance          stripped "
        f"{', '.join(removed) if removed else '(none were present)'}"
    )
    print(f"  5  design_refs        {len(ref_names)} ref(s), all resolve in the bundle's DESIGN.md")
    print(f"  6  validators         {len(validator_names)} name(s), all declared in tutorial.yaml")
    print(f"  7  position           none. An optional lesson is offered, not sequenced:")
    print(f"                        it joins optional_lessons, not lessons, and no")
    print(f"                        renumber is needed or performed.")
    print()
    print("  THE OFFER METADATA IS DERIVED FROM THIS LEARNER'S RUN. Read both")
    print("  values and agree with them before they become part of the course:")
    print()
    print(f"      offer_at       {entry['offer_at'][0]}")
    print(f"                     (from the lesson's 'after:', where the learner needed it)")
    print(f"      offer_because  {entry['offer_because']}")
    print(f"                     (from the lesson's 'reason:', why the tutor wrote it)")

    if not args.confirm and not args.check:
        raise bl.ToolError(
            "nothing was written, because --optional writes judgement the author "
            "must agree with first. Read the two derived values above.\n"
            "  * to see the whole plan validated on a copy:  add --check\n"
            "  * to apply it:                                add --confirm\n"
            "If either value is wrong, fix the generated lesson's 'after:' or "
            "'reason:' and run this again."
        )

    with bl.Staged(bundle_root, check_only=args.check) as stage:
        target = stage.root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(stripped_text, encoding="utf-8")
        manifest_path = stage.root / "tutorial.yaml"
        manifest_text = bl.read_text(manifest_path)
        assert manifest_text is not None
        manifest_path.write_text(
            bl.add_optional_lesson(manifest_text, rel, entry), encoding="utf-8"
        )
        # The lessons list did not move, so this can only REPAIR a template
        # that was already out of step.
        changes = bl.reconcile_state_template(
            stage.root, bundle.listed[0] if bundle.listed else ""
        )
        run = stage.commit()

    if changes:
        print()
        print("STATE.template.md brought back in step with tutorial.yaml:")
        for change in changes:
            print(f"    {change}")

    print()
    print(f"validator: {run.validator}  ({run.how})")
    print(f"           {run.summary()}")

    _, promoted_body = bl.split_frontmatter(stripped_text)
    report_manual_steps(promoted_body, bundle_root, rel, instance, source_rel, args.check)
    return 0


def promote(args: argparse.Namespace) -> int:
    # The runner is a hard prerequisite, so establish it BEFORE anything else
    # - before reading the bundle, before the dirty-tree check, and before any
    # early return. `renumber` used to reach its "Nothing to do" exit without
    # ever looking, so on a machine with no runner installed it reported a
    # clean outcome it had not been able to check. Nothing here mutates, so
    # that was not unsafe; it was misleading, which is how a false oracle
    # starts.
    bl.find_validator()
    instance = Path(args.instance)
    bundle_root = Path(args.bundle)
    if not instance.is_dir():
        raise bl.ToolError(f"{instance}: not a directory.")

    if args.confirm and not args.optional:
        raise bl.ToolError(
            "--confirm is only meaningful with --optional, which is the one "
            "mode that derives judgement - offer_at and offer_because - and "
            "needs the author to agree with it before writing."
        )

    source, source_rel = resolve_generated(instance, args.generated)
    frontmatter, source_text = read_lesson(source)
    bundle = bl.load_bundle(bundle_root)
    bl.require_clean_tree(bundle_root, args.force)

    if args.optional:
        return promote_optional(
            args, instance, bundle_root, bundle, source, source_rel,
            frontmatter, source_text,
        )

    # -- step 7's input: where does it go?
    after = frontmatter.get("after")
    kind = frontmatter.get("kind")
    if isinstance(after, str) and after in bundle.listed:
        position = bundle.listed.index(after) + 1
        placement = f"after {after!r} (its 'after:' field)"
    elif isinstance(after, str) and after:
        position = len(bundle.listed)
        placement = (
            f"appended: its 'after:' names {after!r}, which is not in this "
            f"bundle's lessons list"
        )
    else:
        position = len(bundle.listed)
        placement = "appended: it carries no usable 'after:' field"

    # -- step 1 and 2: the new slug
    body_slug = body_slug_of(frontmatter, source, source_rel)
    # The width the bundle will need AFTER this lesson joins it, so a later
    # renumber computes the same width and has nothing to repad.
    width = max(bundle.number_width, len(str(len(bundle.listed))))
    slug = f"{position:0{width}d}-{body_slug}"
    rel = f"lessons/{slug}.md"

    refuse_slug_clash(bundle, bundle_root, slug, body_slug, rel)

    # -- steps 5 and 6, before anything is copied
    ref_names, validator_names = check_steps_5_and_6(
        frontmatter, bundle, bundle_root, instance, source_rel
    )

    # -- step 3
    stripped_text, removed = strip_provenance(
        source_text, frontmatter, source_rel, slug
    )

    new_listed = list(bundle.listed)
    new_listed.insert(position, rel)

    print(f"promote: {instance}/{source_rel}")
    print(f"      -> {bundle_root}/{rel}")
    print()
    print(f"  1  copy               kind={kind!r}; the learner's copy is NOT touched")
    print(f"  2  id                 {frontmatter.get('id')!r} -> {slug!r}")
    print(
        f"  3  provenance          stripped "
        f"{', '.join(removed) if removed else '(none were present)'}"
    )
    print(f"  5  design_refs        {len(ref_names)} ref(s), all resolve in the bundle's DESIGN.md")
    print(f"  6  validators         {len(validator_names)} name(s), all declared in tutorial.yaml")
    print(f"  7  position           {position} of {len(new_listed)}; {placement}")
    if position != len(bundle.listed):
        print(
            f"                      this leaves the filename prefixes out of "
            f"sequence; run  lesson.py renumber {bundle_root}"
        )

    with bl.Staged(bundle_root, check_only=args.check) as stage:
        target = stage.root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(stripped_text, encoding="utf-8")
        manifest_path = stage.root / "tutorial.yaml"
        manifest_text = bl.read_text(manifest_path)
        assert manifest_text is not None
        manifest_path.write_text(
            bl.replace_lessons_list(manifest_text, new_listed), encoding="utf-8"
        )
        changes = bl.reconcile_state_template(stage.root, new_listed[0])
        run = stage.commit()

    if changes:
        print()
        print("STATE.template.md brought back in step with tutorial.yaml:")
        for change in changes:
            print(f"    {change}")

    print()
    print(f"validator: {run.validator}  ({run.how})")
    print(f"           {run.summary()}")

    _, promoted_body = bl.split_frontmatter(stripped_text)
    report_manual_steps(promoted_body, bundle_root, rel, instance, source_rel, args.check)
    return 0


def report_manual_steps(
    body: str,
    bundle_root: Path,
    rel: str,
    instance: Path,
    source_rel: str,
    check_only: bool,
) -> None:
    print()
    if check_only:
        print("--check: nothing was written. The plan above validates.")
    else:
        print(f"written: {bundle_root}/{rel}")
    print()
    print("=" * 72)
    print("TWO STEPS OF THE PROCEDURE ARE NOT DONE. They are judgement, not")
    print("mechanics, and this tool has not attempted either.")
    print("=" * 72)
    print()
    print("  STEP 4 - rewrite it for a learner who has not started.")
    print("      The lesson was written against ONE learner's code. It will name")
    print("      their types, their files and their error messages. Generalise")
    print("      them. Section 0 of bundle-format.md is the test.")
    survey = survey_for_generalisation(body)
    if survey:
        print()
        print("      A heuristic scan - NOT exhaustive, and a clean scan proves")
        print("      nothing - found these to look at first:")
        for label, count, sample in survey:
            print(f"        {count:>3}x  {label}  ({sample})")
    else:
        print()
        print("      The heuristic scan found none of its tells. That is weak")
        print("      evidence: it looks for second person, workspace paths, quoted")
        print("      compiler output and code fences, and one learner's lesson can")
        print("      carry none of those and still be theirs. Read it.")
    print()
    print("  STEP 8 - update COURSE.md if the course now covers a chapter its map")
    print("      did not mention.")
    print(f"      {bundle_root}/COURSE.md")
    print()
    print("  STEP 9 - the learner's copy. It was NOT deleted and must not be:")
    print(f"      {instance}/{source_rel} stays where it is.")
    print("      The promoted lesson and that draft now share a slug. That becomes")
    print("      visible only when that learner takes a revision of the bundle: at")
    print("      re-materialization the draft is reported as a duplicate of an")
    print("      authored lesson, and the tutor deletes it then. Until then the")
    print("      learner keeps working from their copy and nothing breaks.")
    print()
    print("  STEP 10 - the validator above covers the structural half. The rest of")
    print("      the section 10 self-check is yours, in particular: no learner's")
    print("      source code anywhere, and no progress marker in free prose, which")
    print("      the validator deliberately does not report.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="promote.py",
        description="Promote a generated lesson from an instance into a bundle.",
    )
    parser.add_argument("instance", help="the materialized tutorial directory")
    parser.add_argument(
        "generated", help="the generated lesson, relative to the instance or absolute"
    )
    parser.add_argument("bundle", help="the bundle directory to promote into")
    parser.add_argument(
        "--check",
        action="store_true",
        help="do the whole operation on a copy, validate it, print the plan, "
        "and change nothing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="run even though the working tree under the bundle is dirty",
    )
    parser.add_argument(
        "--optional",
        action="store_true",
        help="promote into optional_lessons instead of onto the main path. "
        "offer_at and offer_because are derived from the lesson's 'after:' "
        "and 'reason:', printed, and written only with --confirm",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="with --optional: the derived offer metadata has been read and "
        "agreed. Without it, --optional prints and writes nothing",
    )
    return promote(parser.parse_args(argv))


if __name__ == "__main__":
    sys.exit(bl.run_main(main))
