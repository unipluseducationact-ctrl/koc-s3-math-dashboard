#!/usr/bin/env python3
"""Fail the build when text files show signs of encoding corruption.

Twice now, UTF-8 content in the JM24 Law of Indices pages has been saved
through the CP950/Big5 code page. Characters that code page cannot represent
turn into "?", and when the lost character sat immediately before markup the
following "<" is swallowed too, so "\u2014</button>" reaches the browser as the
visible text "??/button>".

The rules below are deliberately narrow so they do not fire on legitimate
content: real Chinese text, the JavaScript "??" operator and "?" in query
strings all pass. Files that are already corrupted are listed in
tools/encoding-baseline.txt so this check can be enforced on everything else
without blocking deploys; remove entries as those files get repaired.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_FILE = Path(__file__).resolve().parent / "encoding-baseline.txt"

SCAN_DIRS = ("dashboard",)
SCAN_SUFFIXES = {".html", ".htm", ".css", ".js", ".json", ".svg", ".md"}
SKIP_PARTS = {".git", "node_modules"}

# "??" immediately followed by a closing tag: the signature of a character that
# was destroyed together with the "<" that followed it.
SWALLOWED_TAG = re.compile(r"\?\?/[A-Za-z][A-Za-z0-9]*>")

# Characters produced when common Latin punctuation is re-read as Big5.
# U+7E5A came from "\u00b7", U+79AE from "\u00a7", U+7E69 from a dash.
# These are all real Chinese characters, so they are only reported when they
# turn up in a line of otherwise-Latin text; that is the corruption signature
# ("JM24 <U+7E5A> Scientific Notation"). Lines of genuine Chinese are ignored.
BIG5_ARTEFACTS = {"\u7e5a": "\u00b7", "\u79ae": "\u00a7", "\u7e69": "\u2014"}

CJK_RANGES = ((0x3400, 0x9FFF), (0xF900, 0xFAFF), (0x20000, 0x2FA1F))


def is_cjk(ch: str) -> bool:
    cp = ord(ch)
    return any(low <= cp <= high for low, high in CJK_RANGES)


def is_private_use(ch: str) -> bool:
    return unicodedata.category(ch) == "Co"


def show(text: str) -> str:
    """Render ``text`` using only ASCII, so any console can print it."""
    return text.encode("unicode_escape").decode("ascii")


def check_text(text: str) -> list[str]:
    """Return a list of human-readable problems found in ``text``."""
    problems: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if "\ufffd" in line:
            problems.append(f"line {lineno}: U+FFFD replacement character")
        for ch in line:
            if is_private_use(ch):
                problems.append(
                    f"line {lineno}: private-use character U+{ord(ch):04X}"
                )
                break
        artefacts = {ch for ch in line if ch in BIG5_ARTEFACTS}
        if artefacts and not any(is_cjk(ch) and ch not in artefacts for ch in line):
            for artefact in sorted(artefacts):
                intended = BIG5_ARTEFACTS[artefact]
                problems.append(
                    f"line {lineno}: U+{ord(artefact):04X} "
                    f"({show(artefact)}) in Latin text - a Big5 misreading of "
                    f"U+{ord(intended):04X} ({show(intended)})"
                )
        swallowed = SWALLOWED_TAG.search(line)
        if swallowed:
            problems.append(
                f"line {lineno}: '{swallowed.group(0)}' - a lost character "
                "swallowed the '<' of a closing tag"
            )
    return problems


def load_baseline() -> set[str]:
    if not BASELINE_FILE.exists():
        return set()
    entries = set()
    for raw in BASELINE_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            entries.add(line)
    return entries


def iter_files():
    for top in SCAN_DIRS:
        for path in sorted((REPO_ROOT / top).rglob("*")):
            if path.suffix.lower() not in SCAN_SUFFIXES or not path.is_file():
                continue
            if SKIP_PARTS & set(path.parts):
                continue
            yield path


def main() -> int:
    baseline = load_baseline()
    failures: dict[str, list[str]] = {}
    seen_baselined: set[str] = set()

    for path in iter_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            problems = [f"not valid UTF-8: {exc}"]
        else:
            problems = check_text(text)
        if not problems:
            continue
        if rel in baseline:
            seen_baselined.add(rel)
            continue
        failures[rel] = problems

    if failures:
        print("Encoding corruption detected.\n")
        for rel, problems in sorted(failures.items()):
            print(f"{rel}")
            for problem in problems[:10]:
                print(f"    {problem}")
            if len(problems) > 10:
                print(f"    ... and {len(problems) - 10} more")
            print()
        print(
            "These files look like UTF-8 text that was saved through a non-UTF-8\n"
            "code page (CP950/Big5). Re-save them as UTF-8, restoring the lost\n"
            "characters. If a finding is a false positive, add the path to\n"
            "tools/encoding-baseline.txt with a comment explaining why."
        )
        return 1

    stale = sorted(baseline - seen_baselined)
    if stale:
        print(
            "These paths are listed in tools/encoding-baseline.txt but are now\n"
            "clean (or gone). Please remove them from the baseline:\n"
        )
        for rel in stale:
            print(f"    {rel}")
        return 1

    print("No encoding corruption found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
