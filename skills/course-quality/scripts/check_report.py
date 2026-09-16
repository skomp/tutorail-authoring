#!/usr/bin/env python3
"""Re-add a finished course-quality report against itself.

This script reads the REPORT. It does not read the bundle and it computes no
score of its own, so it does not conflict with the rule that ``audit.py``
computes no score: it only checks that a human-written document agrees with
the numbers in its own tables.

It compares three things:

1. each lesson figure against the sum of that lesson's element rows;
2. the course total against the sum of the lesson figures and the
   course-level penalties;
3. each stated count of a category ("17 of 36 elements are `teaching`")
   against the number of rows in that category.

It reports each mismatch with the file, the line and both figures. It
corrects nothing.

Exit codes
----------
0  every report was read, and every figure that could be checked agreed
1  at least one mismatch
2  at least one report could not be read at all (no element table found, or
   no course-total block found). A report the parser is blind to never
   comes back clean.

Usage
-----
    python3 check_report.py docs/audits/2026-09-13/*.md
    python3 check_report.py --verbose report.md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# text helpers
# --------------------------------------------------------------------------

#: The reports are hand-written and use typographic characters freely.
_NUMERIC_TRANSLATIONS = {
    ord("−"): "-",   # minus sign
    ord("×"): "x",   # multiplication sign
    ord(" "): " ",   # no-break space
}

_PARENS = re.compile(r"\([^()]*\)")
_NUMBER = re.compile(r"[+-]?\d+")
_DASH = re.compile(r"\s[—–-]\s")
_FENCE = re.compile(r"^\s*(`{3,})\s*[A-Za-z0-9_+-]*\s*$")
_CELL_SPLIT = re.compile(r"(?<!\\)\|")

#: A score cell starts with a signed integer, optionally followed by a
#: repetition count ("0 x 5" means five elements each scoring 0).
_SCORE_CELL = re.compile(r"^\s*\**\s*([+-]?\d+)\s*\**\s*(?:[x*]\s*(\d+))?")

#: A first cell that names a line or a line span in a lesson file. The cell
#: has to carry a colon-and-line-number, or be nothing but a line number or a
#: line range - otherwise a file name such as `00-contract-and-language.md`
#: reads as the line number 00.
_LINE_REF = re.compile(
    r"^[\s`*]*(?:"
    r":\d"                          # :58, :67-68, :98-:99
    r"|[A-Za-z0-9_./-]+\.md:\d"     # 00-running-broker.md:53
    r"|\d+:\d"                      # 00:79
    r"|\d+[a-z]?(?:\s*[-\u2013\u2014]\s*\d+[a-z]?)?[\s`*,.]*$"   # 42, 34-36
    r")"
)

CATEGORIES = ("teaching", "practice", "evidence", "toil")

#: The rubric's scored rows. Used only when a table has no Element column.
SCORE_TO_CATEGORY = {2: "teaching", 1: "practice", 0: "evidence", -2: "toil"}

#: "16 of 36 scored elements are `teaching`". The category word has to be
#: bound to the count by an "elements/rows ... are" phrase, otherwise
#: sentences such as '"69 of 69" - ... scoring it toil says ...' match.
_CATEGORY_STATEMENT = re.compile(
    r"(\d+)\s+of\s+(\d+)\s+(?:[A-Za-z-]+\s+){0,3}(?:elements?|rows?)\s+"
    r"(?:are|is|were|was)\s+[`*\"']*(" + "|".join(CATEGORIES) + r")\b",
    re.IGNORECASE,
)


def numeric(text: str) -> str:
    """Normalise the characters that carry arithmetic meaning."""
    return text.translate(_NUMERIC_TRANSLATIONS)


def plain(text: str) -> str:
    """Drop the Markdown emphasis and code markers, keep the words."""
    return text.replace("**", "").replace("`", "").replace("*", "").strip()


def strip_parens(text: str) -> str:
    """Remove parenthesised asides, which carry commentary and not figures."""
    previous = None
    while previous != text:
        previous = text
        text = _PARENS.sub(" ", text)
    return text


def lesson_slug(text: str) -> str | None:
    """Reduce a lesson reference to a key two sections of a report share.

    ``lessons/01-write-a-tone.md``, ``01-write-a-tone.md`` and
    ``lesson 01-write-a-tone`` all reduce to ``01-write-a-tone``;
    ``lessons/00-project-setup/LESSON.md`` reduces to ``00-project-setup``,
    because the file name carries nothing.
    """
    text = plain(strip_parens(text)).lstrip("#").strip()
    match = re.search(r"([A-Za-z0-9_./-]+\.md)", text)
    if match:
        parts = [p for p in match.group(1)[: -len(".md")].split("/") if p]
        if not parts:
            return None
        slug = parts[-1]
        if slug.lower() in ("lesson", "readme") and len(parts) > 1:
            slug = parts[-2]
        return slug.lower()
    match = re.match(r"^\s*(\d{1,2}[\w-]*)", text)
    if match:
        return match.group(1).lower()
    match = re.match(r"^\s*lessons?\s+([A-Za-z0-9][\w-]*)", text, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    parts = _DASH.split(text)
    if len(parts) >= 2 and re.fullmatch(r"[A-Za-z][\w-]*", parts[0].strip()):
        return parts[0].strip().lower()
    return None


def figure_in(text: str) -> int | None:
    """Pull the one figure a report line asserts, ignoring its commentary.

    ``= 260  total across all 19 scored rows`` asserts 260, not 19.
    ``0 x -3 =  0`` asserts 0.  ``- unserved objectives  -3`` asserts -3.
    """
    text = numeric(strip_parens(plain(text)))
    if "=" in text:
        tail = text.rsplit("=", 1)[1]
        match = _NUMBER.search(tail)
        return int(match.group()) if match else None
    head = re.match(r"^\s*([+-]?\d+)\b", text)
    if head:
        return int(head.group(1))
    numbers = _NUMBER.findall(text)
    return int(numbers[-1]) if numbers else None


# --------------------------------------------------------------------------
# findings
# --------------------------------------------------------------------------


@dataclass
class Finding:
    path: str
    line: int
    kind: str
    message: str
    #: MISMATCH fails the run. BLIND means the parser could not read the
    #: report at all. NOTE is neither: it records what was not covered.
    severity: str = "MISMATCH"

    def render(self) -> str:
        return f"{self.severity} {self.path}:{self.line} [{self.kind}] {self.message}"


# --------------------------------------------------------------------------
# table model
# --------------------------------------------------------------------------


@dataclass
class Row:
    line: int
    cells: list[str]


@dataclass
class Table:
    start: int
    header: list[str]
    rows: list[Row] = field(default_factory=list)

    @property
    def end(self) -> int:
        return self.rows[-1].line if self.rows else self.start + 1


@dataclass
class Element:
    line: int
    value: int
    count: int
    category: str | None


@dataclass
class LessonBlock:
    heading_line: int
    heading_text: str
    slug: str | None
    table: Table
    elements: list[Element] = field(default_factory=list)
    unreadable: list[int] = field(default_factory=list)
    excluded: list[int] = field(default_factory=list)
    #: (line, label, figure) for every figure this block states about itself.
    stated: list[tuple[int, str, int]] = field(default_factory=list)

    @property
    def computed(self) -> int:
        return sum(e.value * e.count for e in self.elements)

    @property
    def element_count(self) -> int:
        return sum(e.count for e in self.elements)


def split_cells(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.replace("\\|", "|").strip() for c in _CELL_SPLIT.split(body)]


def is_delimiter(line: str) -> bool:
    return bool(re.match(r"^\s*\|[\s:|-]+\|\s*$", line)) and "-" in line


def find_tables(lines: list[str], in_fence: list[bool]) -> list[Table]:
    tables: list[Table] = []
    i = 0
    while i < len(lines) - 1:
        if (
            not in_fence[i]
            and lines[i].lstrip().startswith("|")
            and is_delimiter(lines[i + 1])
        ):
            table = Table(start=i + 1, header=split_cells(lines[i]))
            j = i + 2
            while j < len(lines) and not in_fence[j] and lines[j].lstrip().startswith("|"):
                table.rows.append(Row(line=j + 1, cells=split_cells(lines[j])))
                j += 1
            tables.append(table)
            i = j
        else:
            i += 1
    return tables


def fence_map(lines: list[str]) -> list[bool]:
    """Mark the lines inside a fenced code block.

    A fence line is backticks plus an optional info string and nothing else.
    A line that merely *starts* with backticks - an inline code span that
    quotes a fence, which one report does - is not a fence.
    """
    inside = False
    marks = []
    for line in lines:
        if _FENCE.match(line):
            inside = not inside
            marks.append(True)
        else:
            marks.append(inside)
    return marks


#: A score cell that says, in so many words, that the row is not scored.
_NOT_SCORED = re.compile(
    r"^(?:[-\u2012-\u2015\u2212]+|n/?a|none|not scored|unscored|"
    r"not an element.*)$",
    re.IGNORECASE,
)


def parse_score_cell(cell: str) -> tuple[int, int] | None:
    match = _SCORE_CELL.match(numeric(cell))
    if not match:
        return None
    return int(match.group(1)), int(match.group(2) or 1)


def is_not_scored(cell: str) -> bool:
    """A row the report deliberately excludes carries no figure to re-add.

    This is different from a cell the parser cannot read: the report says
    so itself, so the row is excluded rather than counted as a blind spot.
    """
    return bool(_NOT_SCORED.match(plain(cell).strip()))


def is_element_table(table: Table) -> bool:
    """An element table scores lesson elements, one row per element.

    Its last column is the score, its first column is not a lesson, and its
    first column names a line or a line span. The last two tests are what
    keep the rubric table, the per-lesson summary tables and the
    unserved-objective gap table out.
    """
    if not table.header or plain(table.header[-1]).lower() != "score":
        return False
    if "lesson" in plain(table.header[0]).lower():
        return False
    data = [r for r in table.rows if not is_sum_row(table, r)]
    if not data:
        return False
    refs = sum(1 for r in data if r.cells and _LINE_REF.match(numeric(r.cells[0])))
    return refs * 2 >= len(data)


def is_sum_row(table: Table, row: Row) -> bool:
    """A row that states the table's own total rather than an element."""
    if not row.cells:
        return False
    if plain(row.cells[0]):
        return False
    return any(plain(c).lower() in ("sum", "total") for c in row.cells[:-1])


def category_column(table: Table) -> int | None:
    for index, cell in enumerate(table.header[:-1]):
        if plain(cell).lower() in ("element", "kind", "category"):
            return index
    return None


# --------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------


@dataclass
class Report:
    path: str
    lines: list[str]
    blocks: list[LessonBlock] = field(default_factory=list)
    #: (line, slug, figure, optional) for the per-lesson summary table.
    summary_rows: list[tuple[int, str, int, bool]] = field(default_factory=list)
    total_blocks: int = 0
    findings: list[Finding] = field(default_factory=list)

    def add(self, line: int, kind: str, message: str, severity: str = "MISMATCH") -> None:
        self.findings.append(Finding(self.path, line, kind, message, severity))


def heading_figure(text: str) -> int | None:
    body = strip_parens(text.lstrip("#").strip())
    parts = _DASH.split(body)
    if len(parts) < 2:
        return None
    match = _NUMBER.search(numeric(plain(parts[-1])))
    return int(match.group()) if match else None


_SUM_LINE = re.compile(r"\bsum\b", re.IGNORECASE)
_EXPRESSION_LINE = re.compile(r"^[\s`*(]*[+-]?\d[\d\s+*/()x.-]*=\s*\**\s*[+-]?\d+")


def trailing_sum(lines: list[str], after: int, limit: int = 6) -> tuple[int, int] | None:
    """Find the ``Sum: ... = 12`` line that follows an element table."""
    for offset in range(after, min(after + limit, len(lines))):
        raw = lines[offset]
        if raw.lstrip().startswith("|") or raw.startswith("#"):
            break
        text = numeric(strip_parens(raw))
        if _SUM_LINE.search(text) or _EXPRESSION_LINE.match(text):
            figure = sum_figure(text)
            if figure is not None:
                return offset + 1, figure
    return None


def sum_figure(text: str) -> int | None:
    """Read the figure a ``Sum:`` line asserts.

    ``Sum: 2+2+2+0 = **10**. `:59` is the best element`` asserts 10 and not
    59, so the figure is taken from the right of the last ``=``, and from
    immediately after the word ``Sum`` when the line carries no ``=``.
    """
    if "=" in text:
        match = _NUMBER.search(plain(text.rsplit("=", 1)[1]))
        return int(match.group()) if match else None
    marker = _SUM_LINE.search(text)
    if not marker:
        return None
    match = _NUMBER.search(plain(text[marker.end():]))
    return int(match.group()) if match else None


def collect_lesson_blocks(report: Report, tables: list[Table]) -> None:
    lines = report.lines
    for table in tables:
        if not is_element_table(table):
            continue
        heading_line, heading_text = 0, ""
        for index in range(table.start - 2, -1, -1):
            if lines[index].startswith("#"):
                heading_line, heading_text = index + 1, lines[index].rstrip()
                break
        block = LessonBlock(
            heading_line=heading_line,
            heading_text=heading_text,
            slug=lesson_slug(heading_text) if heading_text else None,
            table=table,
        )
        cat_index = category_column(table)
        for row in table.rows:
            if is_sum_row(table, row):
                figure = figure_in(row.cells[-1])
                if figure is not None:
                    block.stated.append((row.line, "the table's own sum row", figure))
                continue
            if not row.cells or len(row.cells) < 2:
                continue
            parsed = parse_score_cell(row.cells[-1])
            if parsed is None:
                if is_not_scored(row.cells[-1]):
                    block.excluded.append(row.line)
                else:
                    block.unreadable.append(row.line)
                continue
            value, count = parsed
            category = None
            if cat_index is not None and cat_index < len(row.cells):
                text = plain(row.cells[cat_index]).lower()
                for name in CATEGORIES:
                    if re.search(r"\b" + name + r"\b", text):
                        category = name
                        break
            if category is None:
                category = SCORE_TO_CATEGORY.get(value)
            block.elements.append(Element(row.line, value, count, category))

        figure = heading_figure(heading_text) if heading_text else None
        if figure is not None:
            block.stated.append((block.heading_line, "the lesson heading", figure))
        found = trailing_sum(lines, table.end)
        if found:
            block.stated.append((found[0], "the sum line under the table", found[1]))
        report.blocks.append(block)


def collect_summary_rows(report: Report, tables: list[Table]) -> None:
    """Read the per-lesson summary table, which lists every lesson and its figure.

    Only the first such table is read. A report may carry a second table
    keyed on the lesson - a lesson-size table, for one - and adding its rows
    to the first table's would double every figure.
    """
    for table in tables:
        header = [plain(c).lower() for c in table.header]
        if not header or "lesson" not in header[0]:
            continue
        try:
            score_index = header.index("score")
        except ValueError:
            continue
        if report.summary_rows:
            return
        for row in table.rows:
            if len(row.cells) <= score_index:
                continue
            figure = figure_in(row.cells[score_index])
            slug = lesson_slug(row.cells[0])
            if figure is not None and slug:
                optional = "optional" in row.cells[0].lower()
                report.summary_rows.append((row.line, slug, figure, optional))


# --------------------------------------------------------------------------
# the three checks
# --------------------------------------------------------------------------


def check_lesson_sums(report: Report) -> None:
    """Check 1: each lesson figure against the sum of its element rows."""
    for block in report.blocks:
        name = block.slug or f"the lesson at line {block.heading_line}"
        for line, label, figure in block.stated:
            if figure != block.computed:
                report.add(
                    line,
                    "lesson-sum",
                    f"lesson {name}: {label} states {figure}, its "
                    f"{block.element_count} element row(s) sum to {block.computed}",
                )
        for line in block.unreadable:
            report.add(
                line,
                "unreadable-row",
                f"lesson {name}: the score cell of this row carries no figure, "
                f"so the lesson sum below it is incomplete",
                severity="BLIND",
            )

    by_slug: dict[str, LessonBlock] = {}
    for block in report.blocks:
        if block.slug and block.slug not in by_slug:
            by_slug[block.slug] = block
    for line, slug, figure, _optional in report.summary_rows:
        block = by_slug.get(slug)
        if block is None:
            continue
        if figure != block.computed:
            report.add(
                line,
                "lesson-sum",
                f"lesson {slug}: the per-lesson summary table states {figure}, "
                f"its {block.element_count} element row(s) sum to {block.computed}",
            )


def check_course_total(report: Report) -> None:
    """Check 2: the course total against the lesson figures and penalties."""
    lines = report.lines
    index = 0
    while index < len(lines):
        if not _FENCE.match(lines[index]):
            index += 1
            continue
        index += 1
        body: list[tuple[int, str]] = []
        while index < len(lines) and not _FENCE.match(lines[index]):
            body.append((index + 1, lines[index]))
            index += 1
        index += 1
        _check_arithmetic_block(report, body)


def _classify(text: str) -> str:
    low = numeric(strip_parens(plain(text))).lower()
    if re.search(r"(sum of (the )?(\d+ )?lessons?|lessons? sum|lesson subtotal)", low):
        return "subtotal"
    if re.search(r"\btotals?\b", low):
        return "total"
    if re.search(r"(unserved|required_for|gates?\b|penalt)", low):
        return "penalty"
    if re.match(r"^\s*lesson\b", low):
        return "lesson"
    return "other"


def _check_arithmetic_block(report: Report, body: list[tuple[int, str]]) -> None:
    entries: list[tuple[int, str, int]] = []
    for line, text in body:
        if not _NUMBER.search(numeric(text)):
            continue
        figure = figure_in(text)
        if figure is None:
            continue
        entries.append((line, _classify(text), figure))
    totals = [e for e in entries if e[1] == "total"]
    if not totals:
        return
    report.total_blocks += 1

    subtotals = [e for e in entries if e[1] == "subtotal"]
    penalties = [e for e in entries if e[1] == "penalty"]
    lessons = [e for e in entries if e[1] == "lesson"]
    others = [e for e in entries if e[1] == "other"]

    if subtotals and report.summary_rows:
        all_rows = sum(e[2] for e in report.summary_rows)
        main_rows = sum(e[2] for e in report.summary_rows if not e[3])
        for line, _, figure in subtotals:
            if figure not in (all_rows, main_rows):
                report.add(
                    line,
                    "lesson-subtotal",
                    f"the block states a lesson sum of {figure}; the "
                    f"{len(report.summary_rows)} row(s) of the per-lesson summary "
                    f"table sum to {all_rows} "
                    f"({main_rows} excluding the rows marked optional)",
                )

    if subtotals and lessons:
        stated = sum(e[2] for e in lessons)
        for line, _, figure in subtotals:
            if figure != stated:
                report.add(
                    line,
                    "lesson-subtotal",
                    f"the block states a lesson sum of {figure}; the "
                    f"{len(lessons)} lesson line(s) above it sum to {stated}",
                )

    base = subtotals if subtotals else lessons
    parts = base + penalties + others
    expected = sum(e[2] for e in parts)
    for line, _, figure in totals:
        if figure != expected:
            report.add(
                line,
                "course-total",
                f"the block states a total of {figure}; the "
                f"{len(parts)} figure(s) above it sum to {expected}",
            )

    # Cross-check the block's own lesson lines against the element tables.
    by_slug = {b.slug: b for b in report.blocks if b.slug}
    for line, _, figure in lessons:
        slug = lesson_slug(report.lines[line - 1])
        block = by_slug.get(slug) if slug else None
        if block is None:
            continue
        if figure != block.computed:
            report.add(
                line,
                "lesson-sum",
                f"lesson {slug}: the course arithmetic states {figure}, its "
                f"{block.element_count} element row(s) sum to {block.computed}",
            )


def check_category_counts(report: Report) -> int:
    """Check 3: each stated category count against the rows in that category."""
    counts: dict[str, int] = {name: 0 for name in CATEGORIES}
    total = 0
    for block in report.blocks:
        for element in block.elements:
            total += element.count
            if element.category in counts:
                counts[element.category] += element.count

    checked = 0
    inside = fence_map(report.lines)
    for index, raw in enumerate(report.lines):
        if inside[index]:
            continue
        for match in _CATEGORY_STATEMENT.finditer(raw):
            checked += 1
            stated_in_category = int(match.group(1))
            stated_total = int(match.group(2))
            category = match.group(3).lower()
            if stated_total != total:
                report.add(
                    index + 1,
                    "category-count",
                    f"the report states {stated_total} scored element(s) in total; "
                    f"its element tables hold {total}",
                )
            if stated_in_category != counts.get(category, 0):
                report.add(
                    index + 1,
                    "category-count",
                    f"the report states {stated_in_category} `{category}` element(s); "
                    f"its element tables hold {counts.get(category, 0)}",
                )
    return checked


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------


def check_file(path: str, verbose: bool = False) -> tuple[list[Finding], list[str]]:
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    report = Report(path=path, lines=lines)
    marks = fence_map(lines)
    tables = find_tables(lines, marks)
    collect_lesson_blocks(report, tables)
    collect_summary_rows(report, tables)

    check_lesson_sums(report)
    check_course_total(report)
    categories_checked = check_category_counts(report)

    element_rows = sum(len(b.elements) for b in report.blocks)
    elements = sum(b.element_count for b in report.blocks)
    unreadable = sum(len(b.unreadable) for b in report.blocks)
    excluded = sum(len(b.excluded) for b in report.blocks)
    reconciled = sum(1 for b in report.blocks if b.stated)
    slugs = {b.slug for b in report.blocks if b.slug}
    without_table = [s for _, s, _, _ in report.summary_rows if s not in slugs]

    if not report.blocks:
        report.add(
            1,
            "no-element-tables",
            "no element table was found in this file, so nothing was re-added. "
            "This is not a clean result: the parser is blind here",
            severity="BLIND",
        )
    if report.total_blocks == 0:
        report.add(
            1,
            "no-course-total",
            "no course-arithmetic block with a total was found, so the course "
            "total was not re-added. This is not a clean result",
            severity="BLIND",
        )

    lines_out = [
        f"{path}",
        f"  read: {len(report.blocks)} element table(s), {element_rows} row(s) "
        f"covering {elements} element(s), {excluded} row(s) the report itself "
        f"marks unscored, {unreadable} unreadable row(s)",
        f"  reconciled: {reconciled} lesson(s) with a stated figure and a table; "
        f"{len(set(without_table))} lesson(s) stated in the summary table with no "
        f"element table",
        f"  course-total block(s): {report.total_blocks}; "
        f"per-lesson summary row(s): {len(report.summary_rows)}; "
        f"category statement(s) checked: {categories_checked}",
    ]
    if without_table and verbose:
        lines_out.append(
            "  not re-added (no element table): "
            + ", ".join(sorted(set(without_table)))
        )
    if verbose:
        for block in report.blocks:
            stated = ", ".join(f"{label} {figure}" for _, label, figure in block.stated)
            lines_out.append(
                f"  lesson {block.slug or '?'} (line {block.heading_line}): "
                f"rows sum to {block.computed} over {block.element_count} element(s)"
                + (f"; stated as {stated}" if stated else "; no stated figure")
            )
    return report.findings, lines_out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Re-add a finished course-quality report against its own tables. "
            "Reads the report only; reads no bundle and computes no score."
        )
    )
    parser.add_argument("reports", nargs="+", help="report files to check")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print every lesson the parser read and every figure it found",
    )
    args = parser.parse_args(argv)

    mismatches: list[Finding] = []
    blind: list[Finding] = []
    for path in args.reports:
        try:
            findings, summary = check_file(path, verbose=args.verbose)
        except OSError as error:
            print(f"BLIND {path}:1 [unreadable-file] {error}")
            blind.append(Finding(path, 1, "unreadable-file", str(error), "BLIND"))
            continue
        for line in summary:
            print(line)
        for finding in findings:
            print("  " + finding.render())
            (blind if finding.severity == "BLIND" else mismatches).append(finding)
        if not findings:
            print("  OK - the tables were found and they add up")
        print()

    print(
        f"{len(args.reports)} report(s); {len(mismatches)} mismatch(es); "
        f"{len(blind)} blind spot(s)"
    )
    if mismatches:
        print(f"FAIL - {len(mismatches)} mismatch(es)")
        return 1
    if blind:
        print(
            "BLIND - no mismatch found, but the parser could not read part of "
            "the input. This is not a clean result."
        )
        return 2
    print("OK - every report was read and every figure that was checked agrees")
    return 0


if __name__ == "__main__":
    sys.exit(main())
