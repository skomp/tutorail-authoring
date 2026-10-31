#!/usr/bin/env python3
"""Declare where a learner's defect report goes.

Usage:
    report.py propose <bundles-repo>
    report.py set <bundle> --url <url> [--prefill github|gitlab|none]
                           [--check] [--force]

`report:` is an optional top-level key of tutorial.yaml (Belay 0.12,
bundle-format.md, "Defect reports"). When the runner finds a defect in a
course, the tutor drafts a report and the learner sends it to this place:

    report:
      url: https://github.com/<owner>/<repo>/issues/new   # https:// or mailto:
      prefill: github                                      # github | gitlab | none

A bundle without `report` is complete, and nothing warns: the runner falls
back to the catalogue entry's `report`, then to the catalogue repository's
issue page. The shape is the runner's validator's to check (check 34). This
tool refuses the inputs it can explain first, so that an author never sees a
raw check-34 finding for a value this tool could have named.

`propose` reads `git -C <bundles-repo> remote get-url origin` and maps a
github.com or gitlab.com remote to that repository's new-issue page with the
matching `prefill`. It prints the exact lines `set` would write, and it
writes nothing. Any other host gets no proposal: the author gives a URL or
declines. A host that only resembles github.com (`github.com.evil.example`,
`gist.github.com`) is another host.

`set` writes the block. It obeys the three safety properties every mutating
script in this toolkit obeys:

  * the runner's validator runs against the edited bundle, and a run that is
    not clean is discarded. One exception, as in supplies.py add: a bundle
    that was ALREADY invalid is repaired when the edit removes at least one
    finding and adds none - replacing a malformed `report` is that case;
  * --check does the whole operation on a staging copy, validates it, prints
    what it would do, and throws the copy away;
  * a dirty git working tree under the bundle refuses the run unless --force.

An existing top-level `report:` block is replaced where it stands, and the
output names the old value. Without one, the block is appended after the
last top-level key. No other key moves, and comments outside the replaced
block are kept. `prefill` is written only when it is given.

Exit codes:
    0  done (propose: a value was proposed; set: written, or --check
       validated it; a repair that leaves the bundle invalid is also 0 - read
       the report)
    1  propose only: no value can be proposed (no git repository, no
       `origin`, or a host this tool does not know). Nothing is wrong.
    2  usage, I/O, a refused run, or a validator failure
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

try:
    import bundlelib as bl
except ImportError:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import bundlelib as bl

import supplies  # the validator report every repair-capable command prints


REPORT_KEY = "report"
PREFILLS = ("github", "gitlab", "none")
SCHEMES = ("https://", "mailto:")

# A path segment of a GitHub or GitLab repository: both hosts restrict owner,
# group and repository names to these characters. Anything else (a space, a
# '?', a '%') is not a remote this tool should turn into a link.
_SEGMENT_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

# `git@host:owner/repo.git` - git's scp-like syntax. No '://' and a ':'
# before any '/'.
_SCP_RE = re.compile(r"^(?:[^@/:]+@)?(?P<host>[^@/:]+):(?P<path>.+)$")


# --------------------------------------------------------------------------
# propose
# --------------------------------------------------------------------------


def _host_and_path(remote: str) -> tuple[str, str] | None:
    """The host (lower case) and the path of a git remote URL, or None."""
    if "://" in remote:
        try:
            parts = urlsplit(remote)
            host = parts.hostname
            parts.port  # raises ValueError on a malformed port
        except ValueError:
            return None
        if parts.scheme not in ("https", "ssh") or not host:
            return None
        if parts.query or parts.fragment:
            return None
        return host.lower(), parts.path
    match = _SCP_RE.match(remote)
    if match is None:
        return None
    return match.group("host").lower(), match.group("path")


def propose_report(remote_url: str) -> dict | None:
    """The `report` value for a repository's remote, or None.

    github.com gives `https://github.com/<owner>/<repo>/issues/new` with
    prefill `github`. gitlab.com gives
    `https://gitlab.com/<group>/<subgroup...>/<repo>/-/issues/new` with
    prefill `gitlab`; GitLab subgroups are kept. Every other host gives None,
    and so does a host that only resembles one of the two: the comparison is
    on the whole host name. Only a final `.git` is stripped, and the case of
    every path segment is kept as given.
    """
    found = _host_and_path(remote_url.strip())
    if found is None:
        return None
    host, path = found
    path = path.strip("/")
    if path.endswith(".git"):
        path = path[: -len(".git")]
    segments = path.split("/")
    if not all(_SEGMENT_RE.match(s) and s not in (".", "..") for s in segments):
        return None
    if host == "github.com" and len(segments) == 2:
        return {"url": f"https://github.com/{path}/issues/new", "prefill": "github"}
    if host == "gitlab.com" and len(segments) >= 2:
        return {"url": f"https://gitlab.com/{path}/-/issues/new", "prefill": "gitlab"}
    return None


def render_block(value: dict) -> list[str]:
    """The lines of a top-level `report:` block. Scalars go through emit_scalar."""
    lines = [f"{REPORT_KEY}:", f"  url: {bl.emit_scalar(value['url'])}"]
    if "prefill" in value:
        lines.append(f"  prefill: {bl.emit_scalar(value['prefill'])}")
    return lines


def propose(args: argparse.Namespace) -> int:
    repo = Path(args.repo)
    if not repo.is_dir():
        raise bl.ToolError(f"{repo} is not a directory.")
    cannot = (
        "cannot propose a report value: {why}. Ask the author for a URL "
        "(https:// or mailto:), or let them decline."
    )
    try:
        done = subprocess.run(
            ["git", "-C", str(repo), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
        )
    except OSError:
        print(cannot.format(why="git could not be run"))
        return 1
    if done.returncode != 0:
        inside = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
        )
        why = (
            f"{repo} has no git remote named origin"
            if inside.returncode == 0
            else f"{repo} is not inside a git repository"
        )
        print(cannot.format(why=why))
        return 1
    remote = done.stdout.strip()
    value = propose_report(remote)
    if value is None:
        print(cannot.format(why=f"origin is {remote}, which is not a github.com or gitlab.com repository"))
        return 1
    print("\n".join(render_block(value)))
    return 0


# --------------------------------------------------------------------------
# set
# --------------------------------------------------------------------------


def _refuse_url(url: str, prefill: str | None) -> None:
    """Refuse, with a message naming the option, what check 34 would reject."""
    if not url.strip():
        raise bl.ToolError("--url must not be blank; it is the link a learner opens.")
    if not url.startswith(SCHEMES):
        raise bl.ToolError(
            f"--url {url!r} must start 'https://' or 'mailto:'. A learner opens "
            f"this link, so plain http and every other scheme are refused."
        )
    if url in SCHEMES:
        raise bl.ToolError(f"--url {url!r} is only a scheme; give the whole address.")
    if any(ch.isspace() for ch in url):
        raise bl.ToolError(f"--url {url!r} contains whitespace, which a link cannot.")
    if url.startswith("mailto:") and prefill in ("github", "gitlab"):
        raise bl.ToolError(
            f"--prefill {prefill} cannot go with a mailto: url. A mailto: link "
            f"always carries the subject and the body, so leave --prefill out "
            f"or give 'none'."
        )
    bl.refuse_unwritable("--url", url)
    if prefill is not None:
        bl.refuse_unwritable("--prefill", prefill)


_REPORT_KEY_RE = re.compile(rf"^{REPORT_KEY}[ \t]*:")


def set_report(text: str, value: dict) -> tuple[str, bool]:
    """`text` with its top-level `report:` block set to `value`.

    Returns (new text, whether a block was replaced). An existing block is
    replaced where it stands, so no key moves; without one, the block is
    appended after the last line. The result is parsed back, and a ToolError
    is raised unless `report` reads back as `value` and every other key reads
    back unchanged.
    """
    before = bl.load_yaml(text, "tutorial.yaml")
    lines = text.split("\n")
    block = render_block(value)
    key_index = next((i for i, line in enumerate(lines) if _REPORT_KEY_RE.match(line)), None)
    if key_index is not None:
        end = bl._top_level_block_end(lines, key_index)
        new_lines = lines[:key_index] + block + lines[end:]
        replaced = True
    else:
        body = text.rstrip("\n")
        new_lines = (body.split("\n") + [""] if body else []) + block + [""]
        replaced = False
    new_text = "\n".join(new_lines)
    try:
        after = bl.load_yaml(new_text, "tutorial.yaml (post-edit)")
    except bl.YamlError as exc:
        raise bl.ToolError(
            f"setting report produced text that does not parse: {exc}. Nothing was written."
        ) from exc
    if not isinstance(after, dict) or after.get(REPORT_KEY) != value:
        got = after.get(REPORT_KEY) if isinstance(after, dict) else after
        raise bl.ToolError(
            f"the written report block reads back as {got!r}, not {value!r}. "
            f"Nothing was written."
        )
    rest_before = {k: v for k, v in before.items() if k != REPORT_KEY}
    rest_after = {k: v for k, v in after.items() if k != REPORT_KEY}
    if rest_before != rest_after:
        raise bl.ToolError(
            "setting report would change another key of tutorial.yaml. "
            "Nothing was written."
        )
    return new_text, replaced


def set_cmd(args: argparse.Namespace) -> int:
    # The runner is a hard prerequisite: establish it before anything else.
    bl.find_validator()
    root = Path(args.bundle)
    bundle = bl.load_bundle(root)

    url = args.url
    _refuse_url(url, args.prefill)
    value = {"url": url}
    if args.prefill is not None:
        value["prefill"] = args.prefill

    had = REPORT_KEY in bundle.manifest
    old = bundle.manifest.get(REPORT_KEY)
    if had and old == value:
        raise bl.ToolError(
            f"--url: tutorial.yaml already declares exactly this report: "
            f"{value!r}. Nothing to set."
        )

    # After every refusal that writes nothing: its "not inside a git
    # repository" note is output, and a refusal must be the first line.
    bl.require_clean_tree(root, args.force)

    print(f"{'replace' if had else 'add'}: report block in tutorial.yaml")
    print(f"     url      {url}")
    if "prefill" in value:
        print(f"     prefill  {value['prefill']}")
    if had:
        print(f"     replaces the existing report, which was {old!r}")

    with bl.Staged(root, check_only=args.check, allow_repair=True) as stage:
        manifest_path = stage.root / "tutorial.yaml"
        text = bl.read_text(manifest_path)
        assert text is not None
        new_text, _ = set_report(text, value)
        manifest_path.write_text(new_text, encoding="utf-8")
        run = stage.commit()
        repair = stage.repair

    supplies._report_validator(run, args.check, repair)
    return 0


# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="report.py",
        description="Declare where a learner's defect report goes.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_propose = sub.add_parser(
        "propose", help="print the report block for a repository's origin; write nothing"
    )
    p_propose.add_argument("repo", help="a directory inside the bundles repository")

    p_set = sub.add_parser("set", help="write the report block into tutorial.yaml")
    p_set.add_argument("bundle", help="the bundle directory")
    p_set.add_argument("--url", required=True, help="https:// or mailto: address")
    p_set.add_argument(
        "--prefill",
        choices=PREFILLS,
        help="how the runner fills in the title and body; written only when given",
    )
    p_set.add_argument(
        "--check",
        action="store_true",
        help="do the whole operation on a copy, validate it, print the plan, "
        "and change nothing",
    )
    p_set.add_argument(
        "--force",
        action="store_true",
        help="run even though the working tree under the bundle is dirty",
    )

    args = parser.parse_args(argv)
    if args.command == "propose":
        return propose(args)
    return set_cmd(args)


if __name__ == "__main__":
    sys.exit(bl.run_main(main))
