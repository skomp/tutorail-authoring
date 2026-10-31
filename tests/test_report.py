#!/usr/bin/env python3
"""report.py - where a learner's defect report goes (belay-authoring#40).

Run: python3 tests/test_report.py

Belay 0.12 lets a bundle declare a top-level `report` mapping: a `url` that
starts `https://` or `mailto:`, and an optional `prefill` of `github`,
`gitlab` or `none`. The runner's validator owns the shape (check 34). This
suite covers the two things report.py adds on top:

  * `propose_report` maps a git remote to a proposed value. The done-when
    of the issue is that the tests cover the proposed value for a GitHub
    repository and for a GitLab repository, so every case asserts the exact
    url string and the exact prefill, never only that something printed. A
    host that only resembles github.com must give None, so each positive
    case has a lookalike beside it.
  * `set` writes the block into tutorial.yaml through bl.Staged. Every
    refusal is compared with `tree_digest`, and every refusal has a positive
    control that differs only in the thing under test.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness as h  # noqa: E402
from harness import Workspace, case, check, check_in, check_not_in, report  # noqa: E402

import bundlelib as bl  # noqa: E402  (harness put the scripts dir on sys.path)
import report as rp  # noqa: E402  the module under test, for propose_report


GH = "https://github.com/skomp/belay-bundles/issues/new"


# --------------------------------------------------------------------------
# propose_report - the pure function
# --------------------------------------------------------------------------


def unit_github_forms() -> None:
    want = {"url": GH, "prefill": "github"}
    for remote in (
        "git@github.com:skomp/belay-bundles.git",
        "git@github.com:skomp/belay-bundles",
        "ssh://git@github.com/skomp/belay-bundles.git",
        "ssh://git@github.com:22/skomp/belay-bundles.git",
        "https://github.com/skomp/belay-bundles",
        "https://github.com/skomp/belay-bundles.git",
        "https://github.com/skomp/belay-bundles/",
        "https://github.com/skomp/belay-bundles.git/",
        "https://someone@github.com/skomp/belay-bundles.git",
        "https://GitHub.com/skomp/belay-bundles.git",
    ):
        got = rp.propose_report(remote)
        check(got == want, f"{remote!r} -> {want!r} (got {got!r})")


def unit_case_is_kept_and_only_a_final_git_is_stripped() -> None:
    got = rp.propose_report("git@github.com:skomp/tutorAIl.git")
    check(got == {"url": "https://github.com/skomp/tutorAIl/issues/new", "prefill": "github"},
          f"the case of owner and repo is kept exactly (got {got!r})")
    got = rp.propose_report("https://github.com/o/r.git.git")
    check(got is not None and got["url"] == "https://github.com/o/r.git/issues/new",
          f"only the final .git is stripped (got {got!r})")
    got = rp.propose_report("https://github.com/o/my.gitops")
    check(got is not None and got["url"] == "https://github.com/o/my.gitops/issues/new",
          f"a repo name that only contains '.git' keeps it (got {got!r})")


def unit_gitlab_forms_and_subgroups() -> None:
    for remote, path in (
        ("git@gitlab.com:group/repo.git", "group/repo"),
        ("ssh://git@gitlab.com/group/repo.git", "group/repo"),
        ("https://gitlab.com/group/repo", "group/repo"),
        ("https://gitlab.com/group/repo.git/", "group/repo"),
        ("https://user@gitlab.com/group/repo.git", "group/repo"),
        ("git@gitlab.com:group/sub/repo.git", "group/sub/repo"),
        ("https://gitlab.com/Group/Sub/Deeper/Repo.git", "Group/Sub/Deeper/Repo"),
    ):
        want = {"url": f"https://gitlab.com/{path}/-/issues/new", "prefill": "gitlab"}
        got = rp.propose_report(remote)
        check(got == want, f"{remote!r} -> {want!r} (got {got!r})")


def unit_lookalikes_and_short_paths_give_none() -> None:
    # POSITIVE CONTROL first, so a None below is not a function that always
    # answers None.
    check(rp.propose_report("https://github.com/o/r") is not None,
          "control: a real github.com remote is proposed")
    check(rp.propose_report("https://gitlab.com/o/r") is not None,
          "control: a real gitlab.com remote is proposed")
    for remote in (
        "https://github.com.evil.example/o/r.git",
        "git@github.com.evil.example:o/r.git",
        "https://notgithub.com/o/r.git",
        "https://gist.github.com/o/r.git",
        "https://gitlab.com.evil.example/o/r.git",
        "https://mygitlab.com/o/r.git",
        "https://gitlab.example.org/o/r.git",
        "https://bitbucket.org/o/r.git",
        "https://github.com/o",
        "https://github.com/o/",
        "https://github.com/",
        "git@github.com:o.git",
        "https://gitlab.com/o",
        "https://github.com/o/r/tree/main",
        "https://github.com/o/r with space",
        "file:///srv/git/r.git",
        "/srv/git/r.git",
        "../r.git",
        "",
    ):
        got = rp.propose_report(remote)
        check(got is None, f"{remote!r} -> None (got {got!r})")


# --------------------------------------------------------------------------
# propose - the CLI, against real git repositories
# --------------------------------------------------------------------------


def _git_env(directory: Path) -> dict[str, str]:
    """Keep the developer's own git config (an insteadOf rewrite, say) out."""
    return {
        "GIT_CONFIG_GLOBAL": str(directory / ".gitconfig-absent"),
        "GIT_CONFIG_SYSTEM": str(directory / ".gitconfig-absent"),
    }


def _repo(ws: Workspace, origin: str | None) -> Path:
    repo = ws.path("bundles")
    repo.mkdir()
    env = dict(os.environ)
    env.update(_git_env(repo))
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, env=env, check=True)
    if origin is not None:
        subprocess.run(["git", "remote", "add", "origin", origin], cwd=repo, env=env, check=True)
    return repo


def cli_propose_github_and_gitlab() -> None:
    for origin, url, prefill in (
        ("git@github.com:skomp/belay-bundles.git", GH, "github"),
        ("https://gitlab.com/grp/sub/course.git",
         "https://gitlab.com/grp/sub/course/-/issues/new", "gitlab"),
    ):
        with Workspace() as ws:
            repo = _repo(ws, origin)
            before = h.tree_digest(repo)
            done = h.run(h.REPORT, "propose", repo, env=_git_env(repo))
            check(done.returncode == 0, f"{origin}: exit 0 (got {done.returncode}: {done.output!r})")
            want = f"report:\n  url: {url}\n  prefill: {prefill}\n"
            check(done.stdout == want, f"{origin}: prints exactly {want!r} (got {done.stdout!r})")
            parsed = bl.load_yaml(done.stdout, "propose output")
            check(parsed == {"report": {"url": url, "prefill": prefill}},
                  f"{origin}: the printed block parses to the proposed value (got {parsed!r})")
            check(h.tree_digest(repo) == before, f"{origin}: propose wrote nothing")


def cli_propose_cannot() -> None:
    cases = (
        ("no origin", lambda ws: _repo(ws, None)),
        ("unknown host", lambda ws: _repo(ws, "git@git.example.org:o/r.git")),
        ("not a git repository", lambda ws: (ws.path("plain").mkdir(), ws.path("plain"))[1]),
    )
    for label, make in cases:
        with Workspace() as ws:
            repo = make(ws)
            before = h.tree_digest(repo)
            done = h.run(h.REPORT, "propose", repo, env=_git_env(repo))
            check(done.returncode == 1, f"{label}: exit 1 (got {done.returncode}: {done.output!r})")
            lines = done.output.strip().splitlines()
            check(len(lines) == 1, f"{label}: one plain line (got {lines!r})")
            check_in("cannot propose", done.output, f"{label}: says it cannot propose a value")
            check_in("decline", done.output, f"{label}: says the author can give a URL or decline")
            check_not_in("report:", done.stdout, f"{label}: prints no block")
            check(h.tree_digest(repo) == before, f"{label}: propose wrote nothing")
    # A path that does not exist is a usage error, not "no proposal".
    with Workspace() as ws:
        done = h.run(h.REPORT, "propose", ws.path("absent"))
        check(done.returncode == 2, f"a missing directory: exit 2 (got {done.returncode})")


# --------------------------------------------------------------------------
# set
# --------------------------------------------------------------------------


def set_cmd(bundle: Path, *args: str) -> h.Run:
    return h.run(h.REPORT, "set", bundle, *args)


def _validates(bundle: Path) -> h.Run:
    validator = bl.find_validator()[0]
    return h.run(validator, bundle)


def _bundle(ws: Workspace) -> Path:
    bundle = ws.copy("rust-automaton-db")
    h.git_init(bundle)
    return bundle


def _commit(bundle: Path) -> None:
    env = dict(os.environ)
    env.update(_git_env(bundle))
    env.update({"GIT_AUTHOR_NAME": "f", "GIT_AUTHOR_EMAIL": "f@invalid",
                "GIT_COMMITTER_NAME": "f", "GIT_COMMITTER_EMAIL": "f@invalid"})
    for argv in (["git", "add", "-A"], ["git", "commit", "-q", "-m", "t"]):
        subprocess.run(argv, cwd=bundle, env=env, check=True, capture_output=True)


def cli_set_writes_a_valid_block() -> None:
    for args, want in (
        (("--url", GH, "--prefill", "github"), {"url": GH, "prefill": "github"}),
        (("--url", "https://gitlab.com/g/s/r/-/issues/new", "--prefill", "gitlab"),
         {"url": "https://gitlab.com/g/s/r/-/issues/new", "prefill": "gitlab"}),
        (("--url", "mailto:author@example.org"), {"url": "mailto:author@example.org"}),
        (("--url", "mailto:author@example.org", "--prefill", "none"),
         {"url": "mailto:author@example.org", "prefill": "none"}),
    ):
        with Workspace() as ws:
            bundle = _bundle(ws)
            original = (bundle / "tutorial.yaml").read_text(encoding="utf-8")
            before_manifest = bl.load_yaml(original, "before")
            done = set_cmd(bundle, *args)
            check(done.returncode == 0, f"{args}: exit 0 ({done.output[-400:]!r})")
            text = (bundle / "tutorial.yaml").read_text(encoding="utf-8")
            parsed = bl.load_yaml(text, "after")
            check(parsed.get("report") == want, f"{args}: reads back as {want!r} (got {parsed.get('report')!r})")
            rest = {k: v for k, v in parsed.items() if k != "report"}
            check(rest == before_manifest, f"{args}: every other key reads back unchanged")
            check(text.startswith(original.rstrip("\n")), f"{args}: the original bytes come first, unchanged")
            check(list(parsed)[-1] == "report", f"{args}: the block is after the existing keys")
            if "prefill" not in want:
                check_not_in("prefill", text, f"{args}: prefill is written only when given")
            v = _validates(bundle)
            check(v.returncode == 0, f"{args}: the validator accepts the bundle ({v.output[-300:]!r})")
            check(re.search(r"^\s*\[34\] ran\s.*\(declared\)$", v.output, re.M) is not None,
                  f"{args}: check 34 ran on the declared block and passed it")


def cli_set_keeps_comments_and_replaces() -> None:
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db")
        manifest = bundle / "tutorial.yaml"
        text = manifest.read_text(encoding="utf-8")
        old_block = (
            "# where reports go\n"
            "report:\n"
            "  url: https://github.com/old/place/issues/new\n"
            "  prefill: github\n"
            "\n"
        )
        # Put an existing block in the MIDDLE, so replacing it must not move
        # the keys after it.
        anchor = "workspace_kind: existing-or-new-repository\n"
        check(anchor in text, "fixture: the anchor line is present")
        manifest.write_text(text.replace(anchor, old_block + anchor, 1), encoding="utf-8")
        h.git_init(bundle)
        before = bl.load_yaml(manifest.read_text(encoding="utf-8"), "before")
        check(before["report"]["url"] == "https://github.com/old/place/issues/new",
              "fixture: the old block reads back")
        done = set_cmd(bundle, "--url", GH, "--prefill", "github")
        check(done.returncode == 0, f"replace: exit 0 ({done.output[-400:]!r})")
        check_in("replac", done.output, "replace: says it replaced a block")
        check_in("https://github.com/old/place/issues/new", done.output, "replace: names the old value")
        after_text = manifest.read_text(encoding="utf-8")
        after = bl.load_yaml(after_text, "after")
        check(after["report"] == {"url": GH, "prefill": "github"}, f"replace: new value (got {after['report']!r})")
        check(list(after) == list(before), f"replace: key order is unchanged ({list(after)})")
        check({k: v for k, v in after.items() if k != "report"}
              == {k: v for k, v in before.items() if k != "report"}, "replace: other keys unchanged")
        check_in("# where reports go\nreport:\n", after_text, "replace: the comment above the block is kept")
        check(after_text.count("report:") == 1, "replace: exactly one report: key")
        check_not_in("old/place", after_text, "replace: the old url is gone")

        # The same value again is refused first, and writes nothing.
        _commit(bundle)
        before_digest = h.tree_digest(bundle)
        h.check_refused_first("the same value again", set_cmd(bundle, "--url", GH, "--prefill", "github"),
                              "already declares", bundle, before_digest)

        # Replace with a block that has no prefill: the old prefill must go.
        done = set_cmd(bundle, "--url", "mailto:a@example.org")
        check(done.returncode == 0, f"replace to mailto: exit 0 ({done.output[-400:]!r})")
        after = bl.load_yaml(manifest.read_text(encoding="utf-8"), "after2")
        check(after["report"] == {"url": "mailto:a@example.org"},
              f"replace to mailto: the old prefill is gone (got {after['report']!r})")
        v = _validates(bundle)
        check(v.returncode == 0, f"replace: the validator accepts the bundle ({v.output[-300:]!r})")


def cli_set_repairs_a_malformed_block() -> None:
    """A block check 34 rejects is a finding that `set` removes."""
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db")
        manifest = bundle / "tutorial.yaml"
        manifest.write_text(manifest.read_text(encoding="utf-8")
                            + "report:\n  url: http://example.org\n  prefil: github\n", encoding="utf-8")
        h.git_init(bundle)
        v = _validates(bundle)
        check(v.returncode != 0 and "[check 34]" in v.output,
              f"fixture: check 34 rejects the planted block ({v.output[-300:]!r})")
        done = set_cmd(bundle, "--url", GH, "--prefill", "github")
        check(done.returncode == 0, f"repair: exit 0 ({done.output[-400:]!r})")
        v = _validates(bundle)
        check(v.returncode == 0, f"repair: the bundle now validates ({v.output[-300:]!r})")


def cli_set_check_writes_nothing() -> None:
    with Workspace() as ws:
        bundle = _bundle(ws)
        before = h.tree_digest(bundle)
        done = set_cmd(bundle, "--url", GH, "--prefill", "github", "--check")
        check(done.returncode == 0, f"--check: exit 0 ({done.output[-400:]!r})")
        check_in("nothing was written", done.output, "--check: says nothing was written")
        check_in(GH, done.output, "--check: the plan names the url")
        check(h.tree_digest(bundle) == before, "--check: the bundle is byte-identical")
        # POSITIVE CONTROL: the same call without --check moves the digest.
        done = set_cmd(bundle, "--url", GH, "--prefill", "github")
        check(done.returncode == 0, "--check control: the same set without --check succeeds")
        check(h.tree_digest(bundle) != before, "--check control: the digest does change")


def cli_set_dirty_tree() -> None:
    with Workspace() as ws:
        bundle = _bundle(ws)
        lesson = bundle / "lessons" / "00-foundations.md"
        lesson.write_text(lesson.read_text(encoding="utf-8") + "\nAn uncommitted edit.\n", encoding="utf-8")
        before = h.tree_digest(bundle)
        done = set_cmd(bundle, "--url", GH, "--prefill", "github")
        check(done.returncode == 2, f"dirty: exit 2 (got {done.returncode})")
        check_in("uncommitted change(s)", done.output, "dirty: says why")
        check_in("--force", done.output, "dirty: names --force")
        check(h.tree_digest(bundle) == before, "dirty: the bundle is byte-identical")
        # POSITIVE CONTROL: --force on the same dirty bundle writes.
        done = set_cmd(bundle, "--url", GH, "--prefill", "github", "--force")
        check(done.returncode == 0, f"dirty control: --force runs (got {done.returncode}: {done.output[-300:]!r})")
        check("An uncommitted edit." in lesson.read_text(encoding="utf-8"), "dirty control: the edit is left alone")
        check(bl.load_manifest(bundle)[0].get("report") == {"url": GH, "prefill": "github"},
              "dirty control: the block was written")


def cli_set_refusals() -> None:
    refusals = (
        ("plain http", ("--url", "http://github.com/o/r/issues/new"), "--url"),
        ("javascript scheme", ("--url", "javascript:alert(1)"), "--url"),
        ("no scheme", ("--url", "github.com/o/r/issues/new"), "--url"),
        ("bare https://", ("--url", "https://"), "--url"),
        ("bare mailto:", ("--url", "mailto:"), "--url"),
        ("blank", ("--url", ""), "--url"),
        ("only spaces", ("--url", "   "), "--url"),
        ("whitespace inside", ("--url", "https://example.org/a b"), "--url"),
        ("mailto with github", ("--url", "mailto:a@example.org", "--prefill", "github"), "--prefill"),
        ("mailto with gitlab", ("--url", "mailto:a@example.org", "--prefill", "gitlab"), "--prefill"),
        ("unwritable", ("--url", "https://example.org/a\x07b"), "--url"),
    )
    with Workspace() as ws:
        bundle = _bundle(ws)
        for label, args, option in refusals:
            before = h.tree_digest(bundle)
            h.check_refused_first(label, set_cmd(bundle, *args), option, bundle, before)
        # Outside git, require_clean_tree prints a note; the refusal must still
        # come first.
    with Workspace() as ws:
        bundle = ws.copy("rust-automaton-db")
        before = h.tree_digest(bundle)
        h.check_refused_first("outside git, plain http",
                              set_cmd(bundle, "--url", "http://x.example/"), "--url", bundle, before)
        # POSITIVE CONTROL outside git: the note is printed, and it writes.
        ok = set_cmd(bundle, "--url", GH)
        check(ok.returncode == 0, f"outside-git control: exit 0 ({ok.output[-300:]!r})")
        check_in("not inside a git repository", ok.output, "outside-git control: the note is printed")
    # An unknown --prefill is argparse's refusal: exit 2, nothing written.
    with Workspace() as ws:
        bundle = _bundle(ws)
        before = h.tree_digest(bundle)
        done = set_cmd(bundle, "--url", GH, "--prefill", "bitbucket")
        check(done.returncode == 2, f"unknown prefill: exit 2 (got {done.returncode})")
        check(h.tree_digest(bundle) == before, "unknown prefill: the bundle is byte-identical")
        # POSITIVE CONTROLS, one per refused shape, each differing only in the
        # thing under test.
        for label, args in (
            ("https instead of http", ("--url", "https://github.com/o/r/issues/new")),
            ("mailto with none", ("--url", "mailto:a@example.org", "--prefill", "none")),
            ("mailto without prefill", ("--url", "mailto:a@example.org")),
            ("https with gitlab", ("--url", "https://gitlab.com/g/r/-/issues/new", "--prefill", "gitlab")),
        ):
            before = h.tree_digest(bundle)
            done = set_cmd(bundle, *args, "--check")
            check(done.returncode == 0, f"control {label}: accepted ({done.output[-300:]!r})")
            check(h.tree_digest(bundle) == before, f"control {label}: --check wrote nothing")


def main() -> int:
    print(f"report.py  ({h.REPORT})")
    print()
    with case("propose_report: every github.com remote form gives the issues/new page, prefill github"):
        unit_github_forms()
    with case("propose_report: owner and repo case is kept; only a final .git is stripped"):
        unit_case_is_kept_and_only_a_final_git_is_stripped()
    with case("propose_report: gitlab.com gives /-/issues/new with prefill gitlab, subgroups kept"):
        unit_gitlab_forms_and_subgroups()
    with case("NEGATIVE: a lookalike host, another host or a short path gives None"):
        unit_lookalikes_and_short_paths_give_none()
    with case("propose: prints the exact block for a GitHub and a GitLab origin, writes nothing"):
        cli_propose_github_and_gitlab()
    with case("propose: no origin, unknown host, no repository -> exit 1, one line, nothing written"):
        cli_propose_cannot()
    with case("set: writes a block the validator accepts and yamlite reads back"):
        cli_set_writes_a_valid_block()
    with case("set: replaces an existing block in place, keeps comments and key order"):
        cli_set_keeps_comments_and_replaces()
    with case("set: replacing a block check 34 rejects repairs the bundle"):
        cli_set_repairs_a_malformed_block()
    with case("set --check: prints the plan and writes nothing"):
        cli_set_check_writes_nothing()
    with case("set: a dirty tree is refused unless --force"):
        cli_set_dirty_tree()
    with case("set: each refused url or prefill, with positive controls"):
        cli_set_refusals()
    return report("report.py")


if __name__ == "__main__":
    sys.exit(main())
