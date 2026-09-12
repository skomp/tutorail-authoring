#!/usr/bin/env python3
"""Shared machinery for the tutorail-authoring toolkit.

Stdlib only. Python 3.11.

Three things live here that every script needs, and one that only the
mutating scripts need.

Shared by everything:
  * lesson discovery, the restricted YAML reader, exact-case path resolution
    and frontmatter splitting - all taken from the runner's
    validate_bundle.py rather than reinvented (see the provenance notes on
    each function);
  * surgical edits to tutorial.yaml, which rewrite the bytes the edit
    touches and leave comments, ordering and quoting alone. Round-tripping a
    manifest through a YAML emitter would reformat a file the author wrote
    by hand;
  * the lesson-id token rewriter, which is the one piece with no upstream
    equivalent, because the validator never rewrites anything.

Needed only by the mutating scripts (lesson.py, promote.py):
  * Staged, the transaction that gives every mutating operation the property
    the design demands: the bundle is either better or byte-identical,
    never half-edited. The mutation happens on a copy, the runner's
    validator runs against the copy, and only a clean validator run swaps
    the copy into place.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

try:
    from yamlite import YAML_READER, YamlError, load_yaml
except ImportError:  # pragma: no cover - only when sys.path lacks this dir
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from yamlite import YAML_READER, YamlError, load_yaml

__all__ = [
    "YAML_READER",
    "YamlError",
    "load_yaml",
    "ToolError",
    "Lesson",
    "Bundle",
    "list_dir",
    "resolve_exact",
    "read_text",
    "split_frontmatter",
    "split_number_prefix",
    "discover_lessons",
    "load_manifest",
    "find_validator",
    "run_validator",
    "git_dirty_paths",
    "require_clean_tree",
    "Staged",
    "ManifestEditError",
    "replace_lessons_list",
    "Rewrite",
    "rewrite_tokens",
    "LOOKALIKE_RE",
    "set_frontmatter_field",
    "strip_frontmatter_fields",
    "reconcile_state_template",
    "find_runner_root",
    "find_runner_reference",
    "atomic_write_text",
]


class ToolError(Exception):
    """Anything the operator needs to read and act on. main() prints it."""


class ManifestEditError(ToolError):
    """tutorial.yaml is shaped in a way the surgical editor will not guess at."""


# --------------------------------------------------------------------------
# Filesystem helpers
#
# list_dir, resolve_exact, read_text and split_frontmatter are copied from
# the runner's validate_bundle.py. They exist there for a reason that applies
# here unchanged: this filesystem is case-insensitive, so Path.exists() will
# happily resolve `lessons/03-First-Refactor.md`, which then fails on Linux.
# Comparing against os.listdir() entries is the only way to see it.
# --------------------------------------------------------------------------


def list_dir(path: Path) -> list[str]:
    try:
        return sorted(os.listdir(path))
    except (FileNotFoundError, NotADirectoryError, PermissionError):
        return []


def resolve_exact(base: Path, rel: str) -> tuple[Path | None, str]:
    """Resolve `rel` under `base`, matching every component's case exactly.

    Copied from validate_bundle.resolve_exact. Returns (path, "") on success,
    or (None, reason).
    """
    if "\\" in rel:
        return None, "path uses a backslash; use '/' in bundle paths"
    parts = rel.split("/")
    current = base
    for part in parts:
        if part in ("", ".", ".."):
            return None, f"path component {part!r} is not allowed"
        entries = list_dir(current)
        if not entries and not current.is_dir():
            return None, f"{current.name or current} is not a directory"
        if part not in entries:
            near = [e for e in entries if e.lower() == part.lower()]
            if near:
                return None, (
                    f"the directory entry is named {near[0]!r}, not {part!r}; "
                    f"the case differs, which resolves on macOS or Windows and "
                    f"fails on Linux"
                )
            return None, "no such file"
        current = current / part
    return current, ""


def read_text(path: Path) -> str | None:
    """Read UTF-8 text, or None for a missing file or binary material."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


_FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(?P<fm>.*?)\n---[ \t]*(?:\n|\Z)", re.DOTALL)
_ANCHOR_RE = re.compile(r"\{#([A-Za-z0-9][A-Za-z0-9._-]*)\}")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter text or None, body). From validate_bundle."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    return match.group("fm"), text[match.end() :]


def frontmatter_span(text: str) -> tuple[int, int] | None:
    """Return the (start, end) character offsets of the frontmatter body."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    return match.start("fm"), match.end("fm")


def atomic_write_text(path: Path, text: str) -> None:
    """Write `text` to `path` via a temp file in the same directory.

    A half-written file is never observable under `path`, which matters for
    catalog.py: it writes into a repository the user may be reading.
    """
    handle, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tutorail-", suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


# --------------------------------------------------------------------------
# Lesson discovery
#
# Adapted from validate_bundle.discover_lessons. The shape of the walk is
# identical - a lesson is a top-level .md file, or a folder holding an
# exact-case LESSON.md - because a toolkit that discovered lessons
# differently from the validator would edit files the validator does not
# know about. The only change is that problems come back as a list of
# strings instead of Report findings, since this module has no Report.
# --------------------------------------------------------------------------

GENERATED_DIR = "lessons.generated"
PROVENANCE_FIELDS = ("generated", "generated_at", "kind", "reason", "after")

_NUM_PREFIX_RE = re.compile(r"^(\d+)-(.+)$")


def split_number_prefix(slug: str) -> tuple[str | None, str]:
    """`03-first-refactor` -> ('03', 'first-refactor'). No prefix -> (None, slug)."""
    match = _NUM_PREFIX_RE.match(slug)
    if not match:
        return None, slug
    return match.group(1), match.group(2)


@dataclass
class Lesson:
    rel: str  # path relative to the bundle root, e.g. lessons/00-x.md
    slug: str
    path: Path
    folder: Path | None  # the lesson folder, for foldered lessons

    @property
    def is_folder(self) -> bool:
        return self.folder is not None

    @property
    def form(self) -> str:
        return "folder" if self.folder is not None else "file"


def discover_lessons(
    root: Path, subdir: str = "lessons"
) -> tuple[list[Lesson], list[str]]:
    """Walk `subdir` and return (lessons, problems).

    `problems` carries the same two findings validate_bundle reports from its
    walk: a folder whose body is mis-cased, and a folder with no body at all.
    """
    lessons_dir = root / subdir
    problems: list[str] = []
    if not lessons_dir.is_dir():
        return [], [f"{subdir}/ is not a directory"]
    found: list[Lesson] = []
    for name in list_dir(lessons_dir):
        if name.startswith("."):
            continue
        child = lessons_dir / name
        if child.is_file():
            if name.endswith(".md"):
                found.append(Lesson(f"{subdir}/{name}", name[:-3], child, None))
            continue
        if child.is_dir():
            entries = list_dir(child)
            if "LESSON.md" in entries:
                found.append(
                    Lesson(
                        f"{subdir}/{name}/LESSON.md", name, child / "LESSON.md", child
                    )
                )
                continue
            miscased = [e for e in entries if e.lower() == "lesson.md"]
            if miscased:
                problems.append(
                    f"{subdir}/{name}/{miscased[0]}: a lesson folder's body must be "
                    f"named exactly 'LESSON.md'"
                )
            else:
                problems.append(
                    f"{subdir}/{name}/: a folder directly under {subdir}/ has no "
                    f"LESSON.md, so it is not a lesson"
                )
    return found, problems


# --------------------------------------------------------------------------
# The bundle as the toolkit sees it
# --------------------------------------------------------------------------


@dataclass
class Bundle:
    root: Path
    manifest: dict
    manifest_text: str
    lessons: list[Lesson]  # on disk, sorted by name
    listed: list[str]  # the manifest's lessons list, in order
    problems: list[str]

    @property
    def by_rel(self) -> dict[str, Lesson]:
        return {lesson.rel: lesson for lesson in self.lessons}

    @property
    def ordered(self) -> list[Lesson]:
        """The lessons in manifest order. Unlisted lessons are appended."""
        index = self.by_rel
        out = [index[rel] for rel in self.listed if rel in index]
        seen = {lesson.rel for lesson in out}
        out.extend(lesson for lesson in self.lessons if lesson.rel not in seen)
        return out

    @property
    def number_width(self) -> int:
        """How many digits a lesson's filename prefix gets.

        The widest prefix already in use, but never fewer than the number of
        digits the highest index needs, and never fewer than two. Without the
        middle term a course that grew past 99 lessons would keep producing
        two-digit prefixes, and `100-x` would sort before `11-x`.
        """
        widths = [
            len(prefix)
            for prefix, _ in (split_number_prefix(lesson.slug) for lesson in self.lessons)
            if prefix is not None
        ]
        needed = len(str(max(len(self.listed) - 1, 0)))
        return max(max(widths, default=2), needed, 2)

    @property
    def optional(self) -> set[str]:
        """Lesson paths named by a top-level `optional_lessons:` mapping.

        DEFENSIVE ONLY, and deliberately shallow. The runner is growing a
        format extension in which an authored lesson may sit off the main
        path: it is listed under `optional_lessons` instead of `lessons`, and
        is offered to the learner rather than sequenced. This toolkit does
        not author, edit or renumber such a lesson - that is a moving target
        in a repository this project does not own, and half-implementing it
        would be worse than not implementing it.

        What this property buys is that the toolkit does not CRY WOLF about
        one. Without it, index.py reports every optional lesson as UNLISTED
        and exits 1 on a bundle the runner considers valid, which is the
        "validator that gets ignored" failure the runner's own check 5
        comments warn about.

        An absent key gives an empty set, so nothing changes for a bundle
        that has none.
        """
        raw = self.manifest.get("optional_lessons")
        if isinstance(raw, dict):
            return {str(key) for key in raw}
        if isinstance(raw, list):
            return {str(item) for item in raw if isinstance(item, str)}
        return set()

    def design_anchors(self) -> set[str]:
        text = read_text(self.root / "DESIGN.md")
        return set(_ANCHOR_RE.findall(text)) if text is not None else set()

    def declared_validators(self) -> set[str]:
        raw = self.manifest.get("validators")
        return {str(k) for k in raw} if isinstance(raw, dict) else set()


def load_manifest(root: Path) -> tuple[dict, str]:
    """Read and parse tutorial.yaml. Raises ToolError with a usable message."""
    path = root / "tutorial.yaml"
    if "tutorial.yaml" not in list_dir(root):
        near = [e for e in list_dir(root) if e.lower() == "tutorial.yaml"]
        if near:
            raise ToolError(
                f"{root}: the manifest is named {near[0]!r}, not 'tutorial.yaml'. "
                f"The case must match exactly; this filesystem hides the difference."
            )
        raise ToolError(f"{root}: there is no tutorial.yaml, so this is not a bundle.")
    text = read_text(path)
    if text is None:
        raise ToolError(f"{path}: could not be read as UTF-8 text.")
    try:
        parsed = load_yaml(text, "tutorial.yaml")
    except YamlError as exc:
        raise ToolError(f"{path}: does not parse: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ToolError(
            f"{path}: the manifest must be a mapping of field to value, not "
            f"{type(parsed).__name__}."
        )
    return parsed, text


def load_bundle(root: Path, *, subdir: str = "lessons") -> Bundle:
    root = Path(root)
    if not root.is_dir():
        raise ToolError(f"{root}: not a directory.")
    manifest, manifest_text = load_manifest(root)
    lessons, problems = discover_lessons(root, subdir)
    raw_listed = manifest.get("lessons")
    listed = [x for x in raw_listed if isinstance(x, str)] if isinstance(raw_listed, list) else []
    return Bundle(root, manifest, manifest_text, lessons, listed, problems)


# --------------------------------------------------------------------------
# Validator discovery
#
# Measured on the machine this toolkit was written on: locations 2 and 4 both
# exist, location 3 does not. The order below is the pinned one.
#
# There is deliberately no "skip validation if the validator is missing"
# branch. Skipping would turn the design's central safety guarantee - the
# bundle is never left broken and reported as done - into a claim nothing
# checks, which is the false-oracle failure this project has already been
# bitten by.
# --------------------------------------------------------------------------

VALIDATOR_NAME = "validate_bundle.py"

INSTALL_HINT = """The tutorAIl runner is not installed, so neither its validator nor
its references can be found. No file was changed.

Looked for, in order:
  1. $TUTORAIL_VALIDATOR
  2. ~/.agents/skills/tutorail/scripts/validate_bundle.py
  3. ~/.claude/skills/tutorail/scripts/validate_bundle.py
  4. the newest ~/.claude/plugins/**/tutorail/**/scripts/validate_bundle.py

Install the runner plugin (skomp/tutorAIl), or point $TUTORAIL_VALIDATOR at a
checkout's skills/tutorail/scripts/validate_bundle.py.

Running without it is not offered. The toolkit's one safety guarantee is that a
mutating operation never leaves a bundle broken, and that guarantee is the
validator; a run that skipped it would report success it had not checked."""


def _plugin_candidates(home: Path) -> list[Path]:
    base = home / ".claude" / "plugins"
    if not base.is_dir():
        return []
    try:
        found = [
            path
            for path in base.glob(f"**/tutorail/**/scripts/{VALIDATOR_NAME}")
            if path.is_file()
        ]
    except OSError:  # pragma: no cover - unreadable tree
        return []
    return sorted(found, key=lambda p: (p.stat().st_mtime, str(p)), reverse=True)


def find_validator(env: dict[str, str] | None = None) -> tuple[Path, str]:
    """Return (path, how it was found). Raises ToolError when there is none."""
    env = os.environ if env is None else env
    override = env.get("TUTORAIL_VALIDATOR")
    if override:
        path = Path(os.path.expanduser(override))
        if path.is_file():
            return path, "$TUTORAIL_VALIDATOR"
        raise ToolError(
            f"$TUTORAIL_VALIDATOR is set to {override!r}, which is not a file. "
            f"Point it at a validate_bundle.py, or unset it to search the "
            f"installed plugins.\n\n{INSTALL_HINT}"
        )
    home = Path(os.path.expanduser("~"))
    for rel, label in (
        (Path(".agents") / "skills" / "tutorail" / "scripts" / VALIDATOR_NAME, "~/.agents"),
        (Path(".claude") / "skills" / "tutorail" / "scripts" / VALIDATOR_NAME, "~/.claude/skills"),
    ):
        candidate = home / rel
        if candidate.is_file():
            return candidate, label
    plugins = _plugin_candidates(home)
    if plugins:
        return plugins[0], "~/.claude/plugins (newest)"
    raise ToolError(INSTALL_HINT)


def find_runner_root(env: dict[str, str] | None = None) -> tuple[Path, str]:
    """Return (the runner's skill directory, how it was found).

    The runner's skill directory is the parent of the directory holding
    validate_bundle.py - `<root>/scripts/validate_bundle.py` - so this is the
    SAME search as find_validator, deliberately: the skill needs to read the
    runner's references/bundle-format.md, which is the normative contract, and
    a second search written in prose would drift from this one.

    A guessed path is never returned. If the directory two levels up from the
    validator is not a directory, that is reported as an error rather than
    printed, because a reader sent to a path that is not there is worse off
    than a reader told the runner is missing.
    """
    validator, how = find_validator(env)
    root = validator.parent.parent
    if not root.is_dir():
        raise ToolError(
            f"the validator was found at {validator}, but its skill directory "
            f"{root} is not a directory, so the runner's references cannot be "
            f"located.\n\n{INSTALL_HINT}"
        )
    return root, how


def find_runner_reference(name: str, env: dict[str, str] | None = None) -> tuple[Path, str]:
    """Return (path to `references/<name>` in the runner, how it was found)."""
    root, how = find_runner_root(env)
    path = root / "references" / name
    if name not in list_dir(root / "references"):
        near = [e for e in list_dir(root / "references") if e.lower() == name.lower()]
        detail = f" The directory holds {near[0]!r}." if near else ""
        raise ToolError(
            f"{path} does not exist, so the runner's {name} cannot be read.{detail}\n"
            f"The runner was found at {root} ({how}); it may be an older version "
            f"than this toolkit expects.\n\n{INSTALL_HINT}"
        )
    return path, how


_FINDING_RE = re.compile(r"^\s*\[check\s+(\d+)\]\s*(.*)$")


@dataclass
class ValidatorRun:
    validator: Path
    how: str
    returncode: int
    stdout: str
    stderr: str

    @property
    def clean(self) -> bool:
        return self.returncode == 0

    @property
    def findings(self) -> list[str]:
        out = []
        for line in self.stdout.splitlines():
            match = _FINDING_RE.match(line)
            if match:
                out.append(line.strip())
        return out

    def summary(self) -> str:
        if self.returncode == 0:
            return "PASS"
        if self.returncode == 1:
            return f"FAIL - {len(self.findings)} finding(s)"
        if self.returncode == 3:
            return "INDETERMINATE - a check could not run"
        return f"ERROR - the validator exited {self.returncode}"


def run_validator(target: Path, *, mode: str = "bundle") -> ValidatorRun:
    """Run the runner's validator against `target`. Never swallows a failure."""
    validator, how = find_validator()
    argv = [sys.executable, str(validator)]
    if mode == "instance":
        argv.append("--instance")
    elif mode == "catalog":
        # --portable as well: a catalogue this toolkit generates ships inside
        # a bundles repository, where every bundle must travel with it.
        argv.extend(["--catalog", "--portable"])
    argv.append(str(target))
    completed = subprocess.run(argv, capture_output=True, text=True)
    return ValidatorRun(
        validator, how, completed.returncode, completed.stdout, completed.stderr
    )


# --------------------------------------------------------------------------
# Git working tree
# --------------------------------------------------------------------------


def git_dirty_paths(target: Path) -> tuple[bool, list[str]]:
    """Return (target is inside a git repo, dirty entries touching it).

    Scoped to `target` rather than the whole repository, so a course author
    editing an unrelated bundle in the same repo is not blocked. Untracked
    files count: a stray file inside the bundle is exactly the thing that
    makes `git diff` stop being a clean record of what the tool did.
    """
    try:
        probe = subprocess.run(
            ["git", "-C", str(target), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
        )
    except (OSError, FileNotFoundError):
        return False, []
    if probe.returncode != 0:
        return False, []
    status = subprocess.run(
        ["git", "-C", str(target), "status", "--porcelain", "--", "."],
        capture_output=True,
        text=True,
    )
    if status.returncode != 0:
        return True, []
    return True, [line for line in status.stdout.splitlines() if line.strip()]


def require_clean_tree(target: Path, force: bool, out=sys.stdout) -> None:
    in_repo, dirty = git_dirty_paths(target)
    if not in_repo:
        print(
            f"note: {target} is not inside a git repository, so there is no working "
            f"tree to check. `git diff` will not be a record of this change.",
            file=out,
        )
        return
    if not dirty:
        return
    if force:
        print(
            f"note: the working tree under {target} has {len(dirty)} uncommitted "
            f"change(s); --force was given, so the run continues. `git diff` will "
            f"now mix them with this tool's edit.",
            file=out,
        )
        return
    listing = "\n".join(f"    {line}" for line in dirty[:20])
    more = f"\n    ... and {len(dirty) - 20} more" if len(dirty) > 20 else ""
    raise ToolError(
        f"the working tree under {target} has {len(dirty)} uncommitted change(s):\n"
        f"{listing}{more}\n\n"
        f"Commit or stash them first, so `git diff` afterwards is a clean record of "
        f"exactly what this tool did. Pass --force to run anyway."
    )


# --------------------------------------------------------------------------
# The transaction
# --------------------------------------------------------------------------


class Staged:
    """Mutate a copy; swap it in only after the validator passes.

    The guarantee, which tests/test_atomicity.py proves by hashing every file
    before and after a deliberately failing run: on any failure the bundle is
    byte-identical to what it was.

        with Staged(bundle) as stage:
            ...edit stage.root...
            stage.commit()          # validates, then swaps

    Anything that raises before commit() - including the validator reporting
    findings - discards the staging copy and leaves the original alone.

    The swap is two renames inside one temporary directory on the same
    filesystem. The window between them is the only moment the bundle path
    does not exist, and a failure there is rolled back explicitly.
    """

    def __init__(self, bundle: Path, *, check_only: bool = False, mode: str = "bundle"):
        self.bundle = Path(bundle).resolve()
        self.check_only = check_only
        self.mode = mode
        self.tmpbase: Path | None = None
        self.root: Path | None = None
        self.committed = False
        self.validator_run: ValidatorRun | None = None

    def __enter__(self) -> "Staged":
        # find_validator() runs BEFORE any copying. A missing runner must stop
        # the operation at the start, not after it has done work it will throw
        # away - and the message must be the install hint, not a stack trace.
        find_validator()
        parent = self.bundle.parent
        self.tmpbase = Path(tempfile.mkdtemp(dir=str(parent), prefix=".tutorail-stage-"))
        self.root = self.tmpbase / self.bundle.name
        shutil.copytree(self.bundle, self.root, symlinks=True)
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self._cleanup()
        return False

    def _cleanup(self) -> None:
        if self.tmpbase is not None and self.tmpbase.exists():
            shutil.rmtree(self.tmpbase, ignore_errors=True)
        self.tmpbase = None
        self.root = None

    def validate(self) -> ValidatorRun:
        assert self.root is not None
        self.validator_run = run_validator(self.root, mode=self.mode)
        return self.validator_run

    def commit(self) -> ValidatorRun:
        """Validate the staged copy, then swap it in. Raises on any failure."""
        assert self.root is not None and self.tmpbase is not None
        run = self.validate()
        if not run.clean:
            detail = "\n".join(f"    {line}" for line in run.findings[:25])
            extra = "\n" + detail if detail else ""
            raise ToolError(
                f"the validator says this edit would leave the bundle invalid "
                f"({run.summary()}). Nothing was written; {self.bundle} is "
                f"unchanged.{extra}\n\n"
                f"If the bundle was already invalid before this operation, fix the "
                f"existing findings first: "
                f"python3 {run.validator} {self.bundle}"
            )
        if self.check_only:
            self.committed = False
            return run
        backup = self.tmpbase / "__replaced__"
        os.rename(self.bundle, backup)
        try:
            os.rename(self.root, self.bundle)
        except OSError:
            os.rename(backup, self.bundle)
            raise
        self.committed = True
        self.root = None
        return run


# --------------------------------------------------------------------------
# Surgical edits to tutorial.yaml
#
# The manifest is a file a person wrote, with comments and a chosen layout.
# Re-emitting it from the parse tree would reformat all of it to record a
# one-line change, which buries the edit in `git diff` - the very thing the
# dirty-tree refusal exists to keep readable.
# --------------------------------------------------------------------------

_LESSONS_KEY_RE = re.compile(r"^(?P<indent>[ \t]*)lessons[ \t]*:(?P<rest>.*)$")
_SEQ_ITEM_RE = re.compile(r"^(?P<indent>[ \t]+)-[ \t]+(?P<value>.*?)[ \t]*$")


def replace_lessons_list(manifest_text: str, entries: list[str]) -> str:
    """Return `manifest_text` with the `lessons:` block sequence replaced.

    Three starting shapes are accepted:

        lessons:                a block sequence, with or without items
          - lessons/00-x.md
        lessons:                the key with nothing under it
        lessons: []             an empty flow sequence

    The last two are what a freshly scaffolded bundle carries, and
    `lesson.py add` is the only way to give such a bundle its first lesson -
    so refusing them would leave a new course impossible to start. An empty
    flow sequence is rewritten in block form, which loses no formatting
    because an empty list has none.

    A NON-empty flow sequence (`lessons: [a, b]`) raises ManifestEditError
    rather than being reformatted into a shape the author did not choose.
    """
    lines = manifest_text.split("\n")
    start = None
    empty_flow = False
    for index, line in enumerate(lines):
        match = _LESSONS_KEY_RE.match(line)
        if match and match.group("indent") == "":
            start = index
            rest = _strip_trailing_comment(match.group("rest")).strip()
            if rest == "[]":
                empty_flow = True
            elif rest:
                raise ManifestEditError(
                    f"tutorial.yaml line {index + 1}: the lessons list is written "
                    f"inline ({rest[:40]!r}). This toolkit edits the block form:\n"
                    f"    lessons:\n"
                    f"      - lessons/00-first.md\n"
                    f"Rewrite the list in block form and run the command again."
                )
            break
    if start is None:
        raise ManifestEditError(
            "tutorial.yaml has no top-level 'lessons:' key, so there is no lesson "
            "order to edit."
        )

    end = start + 1
    item_indent = ""
    while end < len(lines):
        line = lines[end]
        if line.strip() == "" or line.lstrip().startswith("#"):
            # A blank line or comment inside the block belongs to the block
            # only while more items follow it; look ahead before consuming.
            lookahead = end + 1
            while lookahead < len(lines) and (
                lines[lookahead].strip() == "" or lines[lookahead].lstrip().startswith("#")
            ):
                lookahead += 1
            if lookahead < len(lines) and _SEQ_ITEM_RE.match(lines[lookahead]):
                end = lookahead
                continue
            break
        item = _SEQ_ITEM_RE.match(line)
        if not item:
            break
        if not item_indent:
            item_indent = item.group("indent")
        end += 1

    head = list(lines[: start + 1])
    if empty_flow:
        comment = _trailing_comment(lines[start])
        head[-1] = "lessons:" + (f"  {comment}" if comment else "")
    replacement = [f"{item_indent or '  '}- {entry}" for entry in entries]
    return "\n".join(head + replacement + lines[end:])


def _strip_trailing_comment(text: str) -> str:
    index = text.find("#")
    while index != -1:
        if index == 0 or text[index - 1] in " \t":
            return text[:index]
        index = text.find("#", index + 1)
    return text


def _trailing_comment(text: str) -> str:
    index = text.find("#")
    while index != -1:
        if index == 0 or text[index - 1] in " \t":
            return text[index:].strip()
        index = text.find("#", index + 1)
    return ""


def read_lessons_list(manifest_text: str) -> list[str]:
    """The lessons list as the surgical editor sees it, for round-trip checks."""
    lines = manifest_text.split("\n")
    out: list[str] = []
    inside = False
    for line in lines:
        match = _LESSONS_KEY_RE.match(line)
        if match and match.group("indent") == "":
            inside = True
            continue
        if inside:
            if line.strip() == "" or line.lstrip().startswith("#"):
                continue
            item = _SEQ_ITEM_RE.match(line)
            if not item:
                break
            out.append(item.group("value"))
    return out


# --------------------------------------------------------------------------
# Frontmatter edits
# --------------------------------------------------------------------------


def set_frontmatter_field(text: str, key: str, value: str) -> tuple[str, bool]:
    """Set `key` in the frontmatter. Returns (text, changed)."""
    span = frontmatter_span(text)
    if span is None:
        return text, False
    start, end = span
    block = text[start:end]
    pattern = re.compile(rf"^([ \t]*){re.escape(key)}([ \t]*:[ \t]*)(.*)$", re.MULTILINE)
    match = pattern.search(block)
    if match:
        if match.group(3).strip() == value:
            return text, False
        new_block = block[: match.start()] + f"{match.group(1)}{key}: {value}" + block[match.end() :]
    else:
        new_block = block + f"\n{key}: {value}"
    return text[:start] + new_block + text[end:], True


def reconcile_state_template(root: Path, first_lesson: str) -> list[str]:
    """Keep STATE.template.md consistent with the manifest. Returns what changed.

    bundle-format.md section 5 requires two equalities, and the runner's
    validator enforces both as check 12:

        tutorial_id   == tutorial.yaml's id
        active_lesson == the first entry of lessons

    Any operation that changes which lesson is first - `add --position 0`,
    `add --after` naming nothing before it, a `renumber` that renames
    lessons[0] - breaks the second one. Leaving that to the author defeats
    the point of the toolkit, and it would surface as a post-validation
    failure whose message talks about a state file the author never touched.

    So both are reconciled here, by every mutating operation, and what
    changed is reported rather than done silently.
    """
    path = root / "STATE.template.md"
    text = read_text(path)
    if text is None:
        return []
    manifest, _ = load_manifest(root)
    changes: list[str] = []
    before, _ = split_frontmatter(text)
    previous = {}
    if before is not None:
        try:
            parsed = load_yaml(before, "STATE.template.md frontmatter")
            previous = parsed if isinstance(parsed, dict) else {}
        except YamlError:
            previous = {}

    if first_lesson and previous.get("active_lesson") != first_lesson:
        text, changed = set_frontmatter_field(text, "active_lesson", first_lesson)
        if changed:
            changes.append(
                f"active_lesson {previous.get('active_lesson')!r} -> {first_lesson!r}"
            )
    bundle_id = manifest.get("id")
    if isinstance(bundle_id, str) and previous.get("tutorial_id") != bundle_id:
        text, changed = set_frontmatter_field(text, "tutorial_id", bundle_id)
        if changed:
            changes.append(
                f"tutorial_id {previous.get('tutorial_id')!r} -> {bundle_id!r}"
            )
    if changes:
        path.write_text(text, encoding="utf-8")
    return changes


def strip_frontmatter_fields(text: str, keys: Iterable[str]) -> tuple[str, list[str]]:
    """Remove `keys` from the frontmatter, with any indented continuation.

    Returns (text, the keys actually removed). A field written as a block
    scalar (`reason: >` and an indented paragraph) loses its continuation
    lines too, which a naive line-delete would leave behind as stray YAML.
    """
    span = frontmatter_span(text)
    if span is None:
        return text, []
    start, end = span
    block = text[start:end]
    lines = block.split("\n")
    wanted = set(keys)
    removed: list[str] = []
    out: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"^([ \t]*)([A-Za-z0-9_.-]+)[ \t]*:", line)
        if match and match.group(2) in wanted and match.group(1) == "":
            removed.append(match.group(2))
            index += 1
            while index < len(lines):
                nxt = lines[index]
                if nxt.strip() == "":
                    # A blank line inside a removed block scalar goes with it,
                    # but a blank line before the next key does not.
                    look = index
                    while look < len(lines) and lines[look].strip() == "":
                        look += 1
                    if look < len(lines) and lines[look][:1] in (" ", "\t"):
                        index = look
                        continue
                    break
                if nxt[:1] in (" ", "\t"):
                    index += 1
                    continue
                break
            continue
        out.append(line)
        index += 1
    return text[:start] + "\n".join(out) + text[end:], removed


# --------------------------------------------------------------------------
# The lesson-id token rewriter
#
# Spec section 9 is normative and the whole of this section implements it:
#
#   rewrite only exact whole-token matches of ids it is itself renaming,
#   never a substring, never an id it does not own; report every rewrite;
#   report anything that looks like a reference but does not match an id
#   being renamed, and leave it alone.
#
# The delimiter classes come from validate_bundle.names_file, which solves
# the same problem for material filenames: a plain substring search matches
# `02-typed-keys` inside `02-typed-keys-table-hierarchy`, and matches
# `03-first-refactor` inside `lessons/03-first-refactor.md.bak`.
#
# Two token kinds are rewritten, and reported separately:
#
#   id    a bare lesson id in prose - `Prerequisites: 02-typed-keys-...`
#   path  a full lesson path - `lessons/02-typed-keys-....md`, which is what
#         tutorial.yaml, STATE.template.md's active_lesson and any prose that
#         names a file use.
#
# The path kind is an extension beyond the letter of section 9, which speaks
# only of ids. It is included because a rename breaks a prose path exactly as
# it breaks a prose id, the rewriter owns both sides of the mapping, and
# leaving paths alone would mean reporting the manifest's own entries as
# dangling references. It is reported under its own label so the two are
# never confused in the output.
# --------------------------------------------------------------------------

# Not preceded by a path or word character, and not continuing into one.
#
# The trailing `(?!\.[A-Za-z0-9])` is the half that is easy to leave out and
# expensive to leave out: without it, `lessons/03-first-refactor.md` matches
# inside `lessons/03-first-refactor.md.bak`, and a renumber silently renames
# a reference to a file it is not moving. validate_bundle.names_file carries
# the same guard, for the same reason, and a test plants that exact token.
_LEFT = r"(?<![A-Za-z0-9_./\\-])"
_RIGHT = r"(?![A-Za-z0-9_-])(?!\.[A-Za-z0-9])"

# A token shaped like a lesson id: digits, a hyphen, then lowercase words.
LOOKALIKE_RE = re.compile(_LEFT + r"\d{1,3}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*" + _RIGHT)


@dataclass
class Rewrite:
    where: str  # file:line, relative to the bundle root
    kind: str  # "id" or "path"
    old: str
    new: str
    line: str


@dataclass
class LeftAlone:
    where: str
    token: str
    line: str
    reason: str


def rewrite_tokens(
    text: str, mapping: dict[str, str], kind: str, where: str
) -> tuple[str, list[Rewrite]]:
    """Rewrite every exact whole-token occurrence of a key in `mapping`.

    One pass with a single alternation, so 03 -> 04 and 04 -> 05 in the same
    renumber cannot cascade: each character of the input is consumed once.
    Longest-first alternation so `02-typed-keys-table-hierarchy` is preferred
    over a shorter id that happens to be its prefix.
    """
    changed = {old: new for old, new in mapping.items() if old != new}
    if not changed:
        return text, []
    alternation = "|".join(
        re.escape(old) for old in sorted(changed, key=len, reverse=True)
    )
    pattern = re.compile(_LEFT + f"(?:{alternation})" + _RIGHT)
    rewrites: list[Rewrite] = []
    out_lines: list[str] = []
    for number, line in enumerate(text.split("\n"), 1):
        hits: list[str] = []

        def substitute(match: re.Match[str]) -> str:
            hits.append(match.group(0))
            return changed[match.group(0)]

        new_line = pattern.sub(substitute, line)
        for old in hits:
            rewrites.append(
                Rewrite(f"{where}:{number}", kind, old, changed[old], new_line.strip())
            )
        out_lines.append(new_line)
    return "\n".join(out_lines), rewrites


def find_left_alone(
    text: str, where: str, known_ids: set[str], renamed: set[str]
) -> list[LeftAlone]:
    """Report tokens shaped like a lesson id that were not rewritten.

    Two classes, because they need different attention:
      * `resolves` - the token names a lesson that exists and is not being
        renamed. Correct as it stands; counted, not listed individually.
      * `unknown` - the token names no lesson at all. This is the dangerous
        one: either a reference that was already dangling, or prose the
        rewriter deliberately did not touch.
    """
    out: list[LeftAlone] = []
    for number, line in enumerate(text.split("\n"), 1):
        for match in LOOKALIKE_RE.finditer(line):
            token = match.group(0)
            if token in renamed:
                continue
            reason = "resolves" if token in known_ids else "unknown"
            out.append(LeftAlone(f"{where}:{number}", token, line.strip(), reason))
    return out


# --------------------------------------------------------------------------
# Text files a rewrite pass should visit
# --------------------------------------------------------------------------

SKIP_NAMES = {".DS_Store"}


def text_files(root: Path) -> list[Path]:
    """Every UTF-8 readable file in the bundle, in a stable order.

    Binary material - the 120KB Duck.glb in webgl-typescript-scene is the
    real case - reads as None and is skipped, never rewritten.
    """
    out: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        if path.name in SKIP_NAMES:
            continue
        out.append(path)
    return out


PURPOSE_SOURCE_LINES = 3


def purpose_line(path: Path) -> str:
    """The opening sentence of the lesson's `## Purpose` section, or "".

    index.py is specified to read frontmatter only, with this as the single
    exception, and only for one line of purpose. The file is STREAMED and the
    read stops as soon as that line is complete - no lesson body is loaded.

    "One line" is one line of OUTPUT. Lesson prose is hard-wrapped, so the
    first source line is usually half a sentence: 00-foundations opens
    "Build the smallest useful in-memory key/value store while establishing
    the Rust", which stops mid-clause. Up to PURPOSE_SOURCE_LINES wrapped
    source lines are joined, and the reader still stops at the first blank
    line or the next heading, whichever comes first.
    """
    try:
        with path.open("r", encoding="utf-8") as stream:
            in_purpose = False
            parts: list[str] = []
            for line in stream:
                stripped = line.strip()
                if in_purpose:
                    if stripped.startswith("#"):
                        break
                    if not stripped:
                        if parts:
                            break
                        continue
                    parts.append(stripped)
                    if len(parts) >= PURPOSE_SOURCE_LINES:
                        break
                    continue
                if re.match(r"^#{1,6}[ \t]+Purpose[ \t]*$", stripped, re.IGNORECASE):
                    in_purpose = True
            return " ".join(parts)
    except (OSError, UnicodeDecodeError):
        return ""


def clip(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    return text[: width - 1].rstrip() + "…"


def fail(message: str, code: int = 2) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def run_main(entry: Callable[[list[str] | None], int], argv: list[str] | None = None) -> int:
    try:
        return entry(argv)
    except ToolError as exc:
        return fail(str(exc))
    except KeyboardInterrupt:  # pragma: no cover
        return fail("interrupted", 130)
