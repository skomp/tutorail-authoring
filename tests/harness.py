#!/usr/bin/env python3
"""Shared machinery for the tutorail-authoring test suites.

No pytest. Nothing is installed in this environment, so every suite is a
plain `python3 tests/test_*.py` runner and this module is what they share.

Three things here are load-bearing, and each exists because of a mistake this
project has already made once.

`tree_digest` - the atomicity proof. Every mutating operation must leave the
bundle BYTE-IDENTICAL when it fails. A test that only checked "the lesson
file is still absent" would pass against a half-edited tutorial.yaml, so the
check hashes every path, every mode bit and every byte.

`listing` - the case-insensitivity trap. THIS FILESYSTEM IS CASE-INSENSITIVE.
`Path("lessons/lesson.md").exists()` is True in a directory holding
`LESSON.md`, so a fixture built with a rename that only changes case is a
silent no-op that tests nothing. Every assertion about a filename goes
through os.listdir.

`no_runner_env` - the false-oracle guard. A test that shows a failure path
firing is worth nothing unless the same probe can be shown reporting the
opposite. Every negative case in this suite has a positive control beside it.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SCRIPTS = REPO / "skills" / "tutorail-authoring" / "scripts"
FIXTURES = HERE / "fixtures"

INDEX = SCRIPTS / "index.py"
LESSON = SCRIPTS / "lesson.py"
PROMOTE = SCRIPTS / "promote.py"
CATALOG = SCRIPTS / "catalog.py"
RUNNER = SCRIPTS / "runner.py"

sys.path.insert(0, str(SCRIPTS))


# --------------------------------------------------------------------------
# Assertions
# --------------------------------------------------------------------------

_failures: list[str] = []
_passed = 0
_notes: list[str] = []


def check(condition: bool, description: str) -> bool:
    global _passed
    if condition:
        _passed += 1
        return True
    _failures.append(description)
    print(f"    FAIL  {description}")
    return False


def check_in(needle: str, haystack: str, description: str) -> bool:
    if needle in haystack:
        return check(True, description)
    print(f"    ---- output did not contain {needle!r} ----")
    print("\n".join(f"    | {line}" for line in haystack.splitlines()[-40:]))
    return check(False, description)


def check_not_in(needle: str, haystack: str, description: str) -> bool:
    if needle not in haystack:
        return check(True, description)
    for line in haystack.splitlines():
        if needle in line:
            print(f"    ---- unexpected: {line.strip()!r}")
            break
    return check(False, description)


def note(text: str) -> None:
    _notes.append(text)


def report(title: str) -> int:
    print()
    if _notes:
        print("notes:")
        for text in _notes:
            print(f"  {text}")
        print()
    if _failures:
        print(f"FAILED - {title}: {len(_failures)} of {_passed + len(_failures)} assertions:")
        for text in _failures:
            print(f"  - {text}")
        return 1
    print(f"OK - {title}: {_passed} assertions passed.")
    return 0


def case(name: str):
    """Decorator-free case runner: `with case('x'):` prints and traps."""
    return _Case(name)


class _Case:
    def __init__(self, name: str) -> None:
        self.name = name

    def __enter__(self) -> "_Case":
        print(f"  {self.name}")
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None and not issubclass(exc_type, KeyboardInterrupt):
            _failures.append(f"{self.name}: raised {exc_type.__name__}: {exc}")
            print(f"    FAIL  raised {exc_type.__name__}: {exc}")
            traceback.print_exception(exc_type, exc, tb)
            return True
        return False


# --------------------------------------------------------------------------
# Filesystem
# --------------------------------------------------------------------------


def listing(directory: Path) -> list[str]:
    """os.listdir, sorted. NEVER use exists() to assert a filename.

    This filesystem is case-insensitive: `(d / "lesson.md").exists()` is True
    in a directory holding `LESSON.md`. A fixture or an assertion built on
    exists() therefore cannot tell the two apart, and the mistake has already
    been made once in this project.
    """
    return sorted(os.listdir(directory))


def has_exactly(directory: Path, name: str) -> bool:
    """True only when the directory holds an entry of exactly this name."""
    return name in listing(directory)


def has_miscased(directory: Path, name: str) -> str | None:
    """The differently-cased entry, when one is there. Proof a fixture bit."""
    for entry in listing(directory):
        if entry != name and entry.lower() == name.lower():
            return entry
    return None


def tree_digest(root: Path) -> str:
    """A hash over every relative path, mode bit and byte under `root`.

    This is the atomicity proof. A failed mutating operation must leave the
    bundle byte-identical, and "the new file is absent" is not that: a
    half-written tutorial.yaml or a renamed-but-not-rewritten lesson would
    pass a weaker check. Symlinks are hashed as their target text rather than
    followed.

    `.git` is excluded. A dirty-tree refusal runs `git status`, which
    refreshes the index's stat cache and so rewrites `.git/index` without
    changing one byte of the bundle. Including it made the refusal cases fail
    for a reason that had nothing to do with the property under test.
    """
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        digest.update(b"\0path\0")
        digest.update(rel.encode("utf-8"))
        if path.is_symlink():
            digest.update(b"\0link\0")
            digest.update(os.readlink(path).encode("utf-8"))
            continue
        if path.is_dir():
            digest.update(b"\0dir\0")
            continue
        stat = path.stat()
        digest.update(f"\0mode{stat.st_mode & 0o777}\0".encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


class Workspace:
    """A temp directory that cleans itself up."""

    def __init__(self, prefix: str = "tutorail-test-") -> None:
        self.root = Path(tempfile.mkdtemp(prefix=prefix))

    def __enter__(self) -> "Workspace":
        return self

    def __exit__(self, *exc) -> bool:
        shutil.rmtree(self.root, ignore_errors=True)
        return False

    def copy(self, fixture: str, name: str | None = None) -> Path:
        source = FIXTURES / fixture
        target = self.root / (name or fixture)
        shutil.copytree(source, target, symlinks=True)
        return target

    def path(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)


def git_init(directory: Path) -> None:
    """Make `directory` a git repository with one clean commit."""
    env = dict(os.environ)
    env.update(
        {
            "GIT_AUTHOR_NAME": "fixture",
            "GIT_AUTHOR_EMAIL": "fixture@invalid",
            "GIT_COMMITTER_NAME": "fixture",
            "GIT_COMMITTER_EMAIL": "fixture@invalid",
            "GIT_CONFIG_GLOBAL": str(directory / ".gitconfig-absent"),
            "GIT_CONFIG_SYSTEM": str(directory / ".gitconfig-absent"),
        }
    )
    for argv in (
        ["git", "init", "-q", "-b", "main"],
        ["git", "add", "-A"],
        ["git", "commit", "-q", "-m", "fixture"],
    ):
        done = subprocess.run(
            argv, cwd=str(directory), env=env, capture_output=True, text=True
        )
        if done.returncode != 0:  # pragma: no cover - a broken git install
            raise RuntimeError(f"{' '.join(argv)}: {done.stderr}")


# --------------------------------------------------------------------------
# Running the scripts
# --------------------------------------------------------------------------


@dataclass
class Run:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def output(self) -> str:
        return self.stdout + self.stderr


def run(script: Path, *args: str, env: dict[str, str] | None = None) -> Run:
    argv = [sys.executable, str(script), *[str(a) for a in args]]
    full = dict(os.environ)
    if env is not None:
        for key, value in env.items():
            if value is None:
                full.pop(key, None)
            else:
                full[key] = value
    done = subprocess.run(argv, capture_output=True, text=True, env=full)
    return Run(argv, done.returncode, done.stdout, done.stderr)


def no_runner_env(home: Path) -> dict[str, str]:
    """An environment in which the validator search must find nothing.

    HOME is redirected at an empty directory, so search locations 2, 3 and 4
    all resolve under it and miss, and TUTORAIL_VALIDATOR is removed so
    location 1 does not answer either. bundlelib uses os.path.expanduser,
    which reads HOME, so this genuinely exercises the same code path a
    machine without the runner would.
    """
    return {"HOME": str(home), "TUTORAIL_VALIDATOR": None}  # type: ignore[dict-item]


STUB_VALIDATOR = '''#!/usr/bin/env python3
"""A stand-in validator that always reports one finding.

It exists so the discard path of every mutating operation can be exercised
deterministically, without needing a bundle that is invalid for some other
reason. Its output is shaped like the real validator's so the finding parser
is exercised too.
"""
import sys

print("tutorAIl validator - mode: bundle")
print("target:      " + sys.argv[-1])
print("")
print("FAIL - 1 finding(s):")
print("  [check  9] DESIGN.md: the file is required and is missing")
sys.exit(1)
'''


def write_stub_validator(directory: Path) -> Path:
    path = directory / "stub_validate_bundle.py"
    path.write_text(STUB_VALIDATOR, encoding="utf-8")
    return path
