#!/usr/bin/env python3
"""catalog.py - the generated catalogue for a repository of bundles.

Run: python3 tests/test_catalog.py

catalog.py makes three claims that a reader cannot check by eye, and all three
are asserted here against values rather than shapes:

  * every `source.path` is RELATIVE, so the repository can serve its own
    bundles wherever it is checked out;
  * `scope` is DERIVED from the lesson count, not invented. Asserting the two
    fixtures' scope strings would not show that - a hardcoded lookup table
    would pass. So synthetic bundles are built at each of `catalog.SCOPE_BANDS`
    ceilings and one lesson past it, and the boundary is asserted from the
    module's own numbers rather than from numbers copied into this file;
  * the written catalogue passes the runner's own catalogue validator. The
    tool says so on stderr; this suite does not take its word for it and runs
    the validator again itself - and, because a validator probe that cannot
    fail proves nothing, runs the same probe against a catalogue known to be
    bad and confirms it reports the failure.

Note on streams: catalog.py writes its notes and its validator verdict to
STDERR and the catalogue itself to stdout only under `-o -`. `Run.output` is
used wherever both matter.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import (  # noqa: E402
    CATALOG,
    FIXTURES,
    Workspace,
    case,
    check,
    check_in,
    check_not_in,
    has_exactly,
    listing,
    report,
    run,
)

import bundlelib as bl  # noqa: E402  (harness puts SCRIPTS on sys.path)
import catalog  # noqa: E402  the module under test, imported for SCOPE_BANDS


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

STATE_TEMPLATE = """---
tutorial_id: {id}
active_lesson: lessons/00-a.md
status: not-started
updated: null
---

## Next task

Begin the first lesson.
"""

LESSON = """---
id: {slug}
title: Lesson {n}
design_refs: []
validators: [manual]
---

## Purpose

Lesson {n} of a synthetic bundle.
"""


def make_bundle(parent: Path, bundle_id: str, lesson_count: int) -> Path:
    """A minimal but real bundle: tutorial.yaml, STATE.template.md, lessons."""
    root = parent / bundle_id
    (root / "lessons").mkdir(parents=True)
    listed = []
    for n in range(lesson_count):
        slug = f"{n:02d}-a" if n == 0 else f"{n:02d}-lesson"
        (root / "lessons" / f"{slug}.md").write_text(LESSON.format(slug=slug, n=n), encoding="utf-8")
        listed.append(f"  - lessons/{slug}.md")
    lessons_block = "lessons: []" if not listed else "lessons:\n" + "\n".join(listed)
    (root / "tutorial.yaml").write_text(
        "bundle_format: 1\n"
        f"id: {bundle_id}\n"
        f"title: Synthetic {bundle_id}\n"
        "description: >\n"
        "  A synthetic bundle built so the scope derivation can be measured at a\n"
        "  known lesson count.\n"
        "subjects: [fixtures, testing]\n"
        "aliases: [synthetic]\n"
        "level: beginner\n"
        "style: [exercise-based]\n"
        "\n"
        f"{lessons_block}\n"
        "\n"
        "workspace_kind: none\n"
        "tutor_owned: [tutorial/STATE.md]\n"
        "learner_owned: []\n"
        "ownership_policy: tutor-must-not-edit-learner-owned\n"
        "\n"
        "validators:\n"
        "  manual: { kind: manual }\n"
        "\n"
        "one_task_at_a_time: true\n"
        "solution_code: on-request-only\n"
        "advance_on: validated-evidence-only\n",
        encoding="utf-8",
    )
    (root / "STATE.template.md").write_text(STATE_TEMPLATE.format(id=bundle_id), encoding="utf-8")
    (root / "DESIGN.md").write_text("# Design\n\n## Naming {#naming}\n\nNames are lowercase.\n", encoding="utf-8")
    (root / "COURSE.md").write_text("# Course\n\nA synthetic course.\n", encoding="utf-8")
    return root


def edit(path: Path, old: str, new: str) -> None:
    """Replace `old` once, and refuse to be a silent no-op."""
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise AssertionError(f"{path}: fixture text {old!r} not found; the edit would do nothing")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def entries(catalogue_text: str) -> dict[str, dict[str, str]]:
    """id -> {field: value} for every `tutorials:` entry, parsed positionally."""
    found: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for line in catalogue_text.splitlines():
        if line.startswith("  - id: "):
            current = {}
            found[line[len("  - id: ") :].strip()] = current
        elif current is not None and line.startswith("    ") and ": " in line:
            key, _, value = line.strip().partition(": ")
            current[key] = value.strip().strip('"')
        elif current is not None and line.startswith("      path: "):
            current["path"] = line[len("      path: ") :].strip()
    return found


def absolute_paths_in(text: str) -> list[str]:
    """Every line that names an absolute path. The probe for case 3.

    Kept as a function so it can be pointed at a known-POSITIVE input; a
    "found nothing" verdict from a scanner nobody tested is not evidence.
    """
    hits = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        _, _, value = stripped.partition(": ")
        if value.startswith("/") or "/Users/" in stripped or "/var/folders/" in stripped:
            hits.append(line)
    return hits


def repo_with_fixtures(ws: Workspace, name: str = "bundles") -> Path:
    repo = ws.path(name)
    repo.mkdir()
    ws_copy(repo, "rust-automaton-db")
    ws_copy(repo, "foldered-bundle")
    return repo


def ws_copy(into: Path, fixture: str, as_name: str | None = None) -> Path:
    target = into / (as_name or fixture)
    shutil.copytree(FIXTURES / fixture, target, symlinks=True)
    return target


# --------------------------------------------------------------------------
# Cases
# --------------------------------------------------------------------------


def case_writes_and_validates() -> None:
    with Workspace() as ws:
        repo = repo_with_fixtures(ws)
        done = run(CATALOG, repo)
        check(done.returncode == 0, f"exit 0 on a repo of two real bundles (got {done.returncode})")
        # listing(), never exists(): this filesystem is case-insensitive, so
        # exists() cannot tell catalog.yaml from CATALOG.YAML.
        check(
            has_exactly(repo, "catalog.yaml"),
            f"catalog.yaml is written into the repo under exactly that name (saw {listing(repo)})",
        )
        check_in("--catalog --portable", done.output, "catalog.py names the validator mode it ran")
        # The exact verdict line, not just the substring "PASS": catalog.py
        # prints ValidatorRun.summary() padded under the validator path, and
        # "FAIL - 1 finding(s)" would satisfy a looser needle in a file that
        # also mentions passing anywhere.
        check_in(
            "\n             PASS\n",
            done.output,
            "catalog.py reports the runner's catalogue validator verdict as PASS",
        )
        check_not_in("FAIL -", done.output, "no finding was reported against the catalogue it wrote")
        check_in("2 bundle(s)", done.output, "it reports both bundles were written")

        text = (repo / "catalog.yaml").read_text(encoding="utf-8")
        found = entries(text)
        check(
            sorted(found) == ["foldered-demo", "rust-automaton-db"],
            f"both bundle ids are catalogued (got {sorted(found)})",
        )
        check(text.startswith("# Catalogue of the bundles in this repository."), "the generated header is present")
        check_in("catalog_version: 1", text, "catalog_version is 1")


def case_independent_validator() -> None:
    """Re-run the runner's validator ourselves, and prove the probe can fail."""
    with Workspace() as ws:
        repo = repo_with_fixtures(ws)
        run(CATALOG, repo)
        validator, how = bl.find_validator()
        check(
            "validate_bundle.py" in validator.name,
            f"the validator was found by discovery, not a hardcoded path ({how}: {validator})",
        )

        good = run(validator, "--catalog", "--portable", repo / "catalog.yaml")
        check(
            good.returncode == 0,
            f"the produced catalogue validates independently (exit {good.returncode}; {good.output[-400:]!r})",
        )

        # POSITIVE CONTROL for the probe above. A validator invocation that
        # exited 0 for the wrong reason - wrong flags, wrong path, a stub -
        # would look exactly like a passing catalogue. Point it at a catalogue
        # that must fail and confirm it says so.
        bad = ws.path("bad-catalog.yaml")
        bad.write_text("catalog_version: 99\ntutorials: []\n", encoding="utf-8")
        bad_run = run(validator, "--catalog", "--portable", bad)
        check(
            bad_run.returncode != 0,
            f"control: the same validator invocation FAILS a known-bad catalogue (exit {bad_run.returncode})",
        )


def case_paths_are_relative() -> None:
    with Workspace() as ws:
        repo = repo_with_fixtures(ws)
        run(CATALOG, repo)
        text = (repo / "catalog.yaml").read_text(encoding="utf-8")

        check_in("      path: rust-automaton-db", text, "the AutomatonDB bundle is named by its relative path")
        check_in("      path: foldered-bundle", text, "the foldered bundle is named by its relative path")
        check_not_in(str(repo), text, "the catalogue never names the repository's own absolute location")

        hits = absolute_paths_in(text)
        check(not hits, f"no absolute path appears anywhere in the catalogue (found {hits})")

        # POSITIVE CONTROL for the scanner. Without it, "found nothing" could
        # equally mean the scanner is broken.
        planted = text.replace("      path: foldered-bundle", f"      path: {repo}/foldered-bundle")
        check(
            len(absolute_paths_in(planted)) == 1,
            "control: the same scanner reports exactly one hit when an absolute path is planted",
        )


def case_scope_is_derived() -> None:
    """Scope comes from the lesson count, and the bands are catalog.SCOPE_BANDS."""
    bands = catalog.SCOPE_BANDS
    check(len(bands) >= 2, f"catalog.SCOPE_BANDS defines at least two bands (got {len(bands)})")

    with Workspace() as ws:
        # The real fixtures first: the exact strings the design calls for.
        real = repo_with_fixtures(ws, "real")
        done = run(CATALOG, real, "-o", "-")
        check(done.returncode == 0, f"-o - on the real fixtures exits 0 (got {done.returncode})")
        found = entries(done.stdout)
        check(
            found.get("rust-automaton-db", {}).get("scope") == "23 lessons; months of work",
            f"the 23-lesson bundle reads '23 lessons; months of work' "
            f"(got {found.get('rust-automaton-db', {}).get('scope')!r})",
        )
        check(
            found.get("foldered-demo", {}).get("scope") == "2 lessons; a few hours",
            f"the 2-lesson bundle reads '2 lessons; a few hours' "
            f"(got {found.get('foldered-demo', {}).get('scope')!r})",
        )

        # Now prove the derivation by changing the input. The counts come from
        # SCOPE_BANDS itself, so this test moves with the module rather than
        # repeating its numbers; a band edited in catalog.py without editing
        # the phrasing here still gets checked at the right boundary.
        counts = {1}
        for ceiling, _ in bands[:-1]:
            counts.add(ceiling)
            counts.add(ceiling + 1)
        synthetic = ws.path("synthetic")
        synthetic.mkdir()
        for n in sorted(counts):
            make_bundle(synthetic, f"scope-{n:03d}", n)

        got = run(CATALOG, synthetic, "-o", "-")
        check(got.returncode == 0, f"the synthetic repo catalogues cleanly (got {got.returncode}; {got.stderr[-300:]!r})")
        scopes = {name: fields.get("scope") for name, fields in entries(got.stdout).items()}
        check(
            len(scopes) == len(counts),
            f"one entry per synthetic bundle ({len(counts)} expected, got {len(scopes)})",
        )

        # Singular, not "1 lessons;". A plural bug here is invisible in every
        # other count.
        check(
            scopes.get("scope-001") == f"1 lesson; {bands[0][1]}",
            f"1 lesson reads '1 lesson; {bands[0][1]}' - singular (got {scopes.get('scope-001')!r})",
        )

        for index, (ceiling, phrase) in enumerate(bands[:-1]):
            next_phrase = bands[index + 1][1]
            check(phrase != next_phrase, f"bands {index} and {index + 1} really are different phrases")
            check(
                scopes.get(f"scope-{ceiling:03d}") == f"{ceiling} lessons; {phrase}",
                f"{ceiling} lessons (the band ceiling) reads {phrase!r} "
                f"(got {scopes.get(f'scope-{ceiling:03d}')!r})",
            )
            check(
                scopes.get(f"scope-{ceiling + 1:03d}") == f"{ceiling + 1} lessons; {next_phrase}",
                f"{ceiling + 1} lessons (one past the ceiling) reads {next_phrase!r} "
                f"(got {scopes.get(f'scope-{ceiling + 1:03d}')!r})",
            )


def case_duplicate_id_fires() -> None:
    with Workspace() as ws:
        # POSITIVE CONTROL: two bundles with DISTINCT ids both appear, so the
        # skip below is caused by the id collision and not by the second copy
        # being unreachable for some other reason.
        ok_repo = ws.path("distinct")
        ok_repo.mkdir()
        ws_copy(ok_repo, "foldered-bundle", "aaa-first")
        second_ok = ws_copy(ok_repo, "foldered-bundle", "zzz-second")
        edit(second_ok / "tutorial.yaml", "id: foldered-demo", "id: foldered-demo-two")
        ok = run(CATALOG, ok_repo, "-o", "-")
        check(ok.returncode == 0, f"control: distinct ids exit 0 (got {ok.returncode})")
        check(
            sorted(entries(ok.stdout)) == ["foldered-demo", "foldered-demo-two"],
            f"control: with distinct ids BOTH bundles are catalogued (got {sorted(entries(ok.stdout))})",
        )
        check_not_in("skipped", ok.output, "control: nothing is skipped when the ids differ")

        repo = ws.path("collide")
        repo.mkdir()
        ws_copy(repo, "foldered-bundle", "aaa-first")
        ws_copy(repo, "foldered-bundle", "zzz-second")
        done = run(CATALOG, repo)
        check(done.returncode == 0, f"a duplicate id is a skip, not a hard failure (got {done.returncode})")
        check_in("skipped", done.output, "the duplicate is reported as skipped")
        check_in("zzz-second", done.output, "the note names the directory that was skipped")
        check_in("'foldered-demo' is already used by", done.output, "the note names the colliding id")
        check_in("precedence undecidable", done.output, "the note says why a duplicate id cannot be catalogued")
        # The skip notes read "skipped <directory>: ...", so the first copy's
        # name followed by a colon appears only if IT was the one dropped.
        check_not_in("aaa-first: ", done.output, "the first copy was kept, not skipped")

        text = (repo / "catalog.yaml").read_text(encoding="utf-8")
        check(
            text.count("  - id: foldered-demo") == 1,
            f"the written catalogue carries the id exactly once (got {text.count('  - id: foldered-demo')})",
        )


def case_no_bundle_at_all_fires() -> None:
    with Workspace() as ws:
        # POSITIVE CONTROL: the same invocation against a repo that DOES hold a
        # bundle exits 0, so exit 1 below is about emptiness, not about the
        # invocation being wrong.
        ok_repo = ws.path("has-one")
        ok_repo.mkdir()
        ws_copy(ok_repo, "foldered-bundle")
        ok = run(CATALOG, ok_repo)
        check(ok.returncode == 0, f"control: a repo holding one bundle exits 0 (got {ok.returncode})")

        empty = ws.path("empty")
        empty.mkdir()
        check(listing(empty) == [], f"the directory really is empty (got {listing(empty)})")
        done = run(CATALOG, empty)
        check(done.returncode == 1, f"an empty directory exits 1 (got {done.returncode})")
        check_in("no bundle was found under", done.output, "it says no bundle was found")
        check_in(
            "A bundle is a directory holding both tutorial.yaml and STATE.template.md.",
            done.output,
            "it says what a bundle is, so the operator can act on it",
        )
        check(
            not has_exactly(empty, "catalog.yaml"),
            f"nothing was written into the empty directory (saw {listing(empty)})",
        )


def case_instance_is_not_a_bundle_fires() -> None:
    """An instance carries STATE.md; a bundle carries STATE.template.md."""
    with Workspace() as ws:
        repo = ws.path("mixed")
        repo.mkdir()
        ws_copy(repo, "foldered-bundle")
        instance = ws_copy(repo, "instance-with-generated")
        # The fixture shares the AutomatonDB id, which would make "the id is
        # absent" unfalsifiable if the real bundle were also present. Give it
        # its own id so absence means something.
        edit(instance / "tutorial.yaml", "id: rust-automaton-db", "id: instance-not-a-bundle")
        check(
            "STATE.md" in listing(instance) and "STATE.template.md" not in listing(instance),
            f"the instance really has STATE.md and no STATE.template.md (saw {listing(instance)})",
        )

        done = run(CATALOG, repo)
        check(done.returncode == 0, f"the real bundle beside an instance still catalogues (got {done.returncode})")
        text = (repo / "catalog.yaml").read_text(encoding="utf-8")
        found = entries(text)
        check_not_in("instance-not-a-bundle", text, "the learner instance is NOT catalogued")
        check("foldered-demo" in found, f"the real bundle beside it still is (got {sorted(found)})")

        # POSITIVE CONTROL. The same directory, with STATE.template.md added,
        # IS catalogued - which shows the discriminator is that one file and
        # not something incidental about the instance fixture (its
        # lessons.generated/ directory, its name, its depth in the tree).
        (instance / "STATE.template.md").write_text(
            (instance / "STATE.md").read_text(encoding="utf-8"), encoding="utf-8"
        )
        promoted = run(CATALOG, repo)
        check(promoted.returncode == 0, f"control: exit 0 after adding STATE.template.md (got {promoted.returncode})")
        promoted_text = (repo / "catalog.yaml").read_text(encoding="utf-8")
        check_in(
            "instance-not-a-bundle",
            promoted_text,
            "control: the SAME directory IS catalogued once STATE.template.md is there",
        )


def case_empty_lessons_list_fires() -> None:
    with Workspace() as ws:
        repo = ws.path("repo")
        repo.mkdir()
        ws_copy(repo, "foldered-bundle")  # so the run has something to write
        make_bundle(repo, "no-lessons", 0)
        check(
            "lessons: []" in (repo / "no-lessons" / "tutorial.yaml").read_text(encoding="utf-8"),
            "the synthetic bundle really declares an empty lessons list",
        )

        done = run(CATALOG, repo)
        check(done.returncode == 0, f"one skipped bundle beside a good one still exits 0 (got {done.returncode})")
        check_in("skipped", done.output, "the empty-lessons bundle is skipped")
        check_in("no-lessons", done.output, "the note names the skipped bundle")
        check_in(
            "its lessons list is empty, so scope cannot be derived",
            done.output,
            "the note says scope cannot be derived from an empty lessons list",
        )
        text = (repo / "catalog.yaml").read_text(encoding="utf-8")
        check_not_in("  - id: no-lessons", text, "the empty-lessons bundle is not in the written catalogue")

        # POSITIVE CONTROL: the same bundle with ONE lesson is catalogued, so
        # the skip is about the empty list and not about the bundle being
        # synthetic, freshly made, or badly named.
        shutil.rmtree(repo / "no-lessons")
        make_bundle(repo, "no-lessons", 1)
        again = run(CATALOG, repo)
        check(again.returncode == 0, f"control: exit 0 with one lesson (got {again.returncode})")
        found = entries((repo / "catalog.yaml").read_text(encoding="utf-8"))
        check("no-lessons" in found, f"control: the same bundle with 1 lesson IS catalogued (got {sorted(found)})")
        check(
            found.get("no-lessons", {}).get("scope") == f"1 lesson; {catalog.SCOPE_BANDS[0][1]}",
            f"control: and its scope is derived from that one lesson "
            f"(got {found.get('no-lessons', {}).get('scope')!r})",
        )


def case_output_destinations() -> None:
    with Workspace() as ws:
        repo = ws.path("stdout-repo")
        repo.mkdir()
        ws_copy(repo, "foldered-bundle")

        before = listing(repo)
        done = run(CATALOG, repo, "-o", "-")
        check(done.returncode == 0, f"-o - exits 0 (got {done.returncode})")
        check_in("catalog_version: 1", done.stdout, "-o - writes the catalogue to stdout")
        check_in("      path: foldered-bundle", done.stdout, "the stdout catalogue carries the relative path")
        check_in("not written (-o -)", done.stderr, "-o - says on stderr that nothing was written")
        check(
            not has_exactly(repo, "catalog.yaml"),
            f"-o - leaves no catalog.yaml in the repo (saw {listing(repo)})",
        )
        check(listing(repo) == before, f"-o - changed nothing in the repo (before {before}, after {listing(repo)})")

        # POSITIVE CONTROL for that listing probe: the default run in the SAME
        # directory does produce catalog.yaml, so "not in listing" above is a
        # statement about -o - and not about a probe that never sees anything.
        default = run(CATALOG, repo)
        check(default.returncode == 0, f"control: the default run exits 0 (got {default.returncode})")
        check(
            has_exactly(repo, "catalog.yaml"),
            f"control: the same probe DOES see catalog.yaml after a default run (saw {listing(repo)})",
        )

        # -o <path>: written where told, and nowhere else.
        target_repo = ws.path("target-repo")
        target_repo.mkdir()
        ws_copy(target_repo, "foldered-bundle")
        named = run(CATALOG, target_repo, "-o", target_repo / "alt-catalog.yaml")
        check(named.returncode == 0, f"-o <path> exits 0 (got {named.returncode})")
        check(
            has_exactly(target_repo, "alt-catalog.yaml"),
            f"-o <path> writes to exactly the name given (saw {listing(target_repo)})",
        )
        check(
            not has_exactly(target_repo, "catalog.yaml"),
            f"-o <path> does not also write the default catalog.yaml (saw {listing(target_repo)})",
        )
        written = (target_repo / "alt-catalog.yaml").read_text(encoding="utf-8")
        check_in("catalog_version: 1", written, "the named file holds the catalogue")
        check(
            entries(written).get("foldered-demo", {}).get("path") == "foldered-bundle",
            "the named file's path stays relative to its own directory",
        )
        check_in("PASS", named.output, "-o <path> validates what it wrote")


def main() -> int:
    print(f"catalog.py  ({CATALOG})")
    print()
    with case("a repo of two real bundles: written, and the runner's validator passes"):
        case_writes_and_validates()
    with case("the produced catalogue validates under an independently found validator"):
        case_independent_validator()
    with case("every source.path is relative and no absolute path leaks"):
        case_paths_are_relative()
    with case("scope is derived from the lesson count, at catalog.SCOPE_BANDS' boundaries"):
        case_scope_is_derived()
    with case("FIRING: two bundles claiming one id"):
        case_duplicate_id_fires()
    with case("FIRING: a directory holding no bundle"):
        case_no_bundle_at_all_fires()
    with case("FIRING: a learner instance is not a bundle"):
        case_instance_is_not_a_bundle_fires()
    with case("FIRING: a bundle whose lessons list is empty"):
        case_empty_lessons_list_fires()
    with case("-o - and -o <path>"):
        case_output_destinations()
    return report("catalog.py")



# --------------------------------------------------------------------------
# tutorail-authoring#6 - a valid catalogue must not depend on how its path is spelled
# --------------------------------------------------------------------------

def _repo_with_one_bundle(ws: Workspace) -> Path:
    """A bundles repository holding one real bundle, ready for catalog.py."""
    repo = ws.path("repo")
    repo.mkdir()
    shutil.copytree(FIXTURES / "rust-automaton-db", repo / "rust-automaton-db")
    return repo


with case("catalog.py . succeeds from inside the repository (issue #6)"):
    with Workspace() as ws:
        repo = _repo_with_one_bundle(ws)
        out = run(CATALOG, ".", cwd=repo)
        check(out.returncode == 0, f"exit 0 with a bare '.' (got {out.returncode})")
        check_not_in("does not validate", out.output,
                     "it does not refuse to ship its own valid catalogue")

with case("POSITIVE CONTROL: the same repository passes when named absolutely"):
    with Workspace() as ws:
        repo = _repo_with_one_bundle(ws)
        out = run(CATALOG, str(repo))
        check(out.returncode == 0, "exit 0 with an absolute path")

with case("the two spellings produce byte-identical catalogues"):
    with Workspace() as ws:
        a = _repo_with_one_bundle(ws)
        run(CATALOG, ".", cwd=a)
        text_dot = (a / "catalog.yaml").read_text(encoding="utf-8")
    with Workspace() as ws:
        b = _repo_with_one_bundle(ws)
        run(CATALOG, str(b))
        text_abs = (b / "catalog.yaml").read_text(encoding="utf-8")
    check(text_dot == text_abs,
          "one file, one content, whichever spelling wrote it")

with case("NEGATIVE CONTROL: a bundle path that escapes still fails, both spellings"):
    # The fix must not turn a false alarm into a false negative. --portable exists
    # to catch a catalogue naming a bundle that will not travel with it.
    with Workspace() as ws:
        repo = _repo_with_one_bundle(ws)
        outside = ws.path("outside")
        outside.mkdir()
        shutil.copytree(FIXTURES / "rust-automaton-db", outside / "elsewhere")
        cat = repo / "catalog.yaml"
        run(CATALOG, ".", cwd=repo)
        text = cat.read_text(encoding="utf-8")
        planted = text.replace("path: rust-automaton-db",
                               "path: ../outside/elsewhere")
        # Guard the needle. A replacement that silently matches nothing leaves a VALID
        # catalogue behind, and the probe below then passes for the wrong reason.
        check(planted != text, "the escaping path was actually planted")
        cat.write_text(planted, encoding="utf-8")
        v = bl.find_validator()[0]
        for label, target in (("bare", "catalog.yaml"), ("absolute", str(cat))):
            probe = run(Path(v), "--catalog", target, "--portable",
                        cwd=repo if label == "bare" else None)
            check(probe.returncode != 0,
                  f"an escaping bundle path still fails when named {label}")
            check_in("leaves", probe.output,
                     f"and the finding still names the escape ({label})")

if __name__ == "__main__":
    sys.exit(main())
