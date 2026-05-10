from __future__ import annotations

import textwrap

from growth_goaled.logging_utils import log_step
from growth_goaled.models import CompanyProfile, DiagnosticOutput
from growth_goaled.scoring import calculate_pillar_scores


def build_export_text(company: CompanyProfile, diagnostic: DiagnosticOutput) -> str:
    log_step("STEP 8 | Building export source text")
    scores = diagnostic.raw_scores or calculate_pillar_scores(company)
    roadmap = "\n".join(
        f"- {item['window']}: {item['focus']} | {item['actions']} | Metric: {item['success_metric']}"
        for item in diagnostic.roadmap
    )
    insights = "\n".join(f"- {insight}" for insight in diagnostic.key_insights)
    fixes = "\n".join(
        f"{idx}. {fix}" for idx, fix in enumerate(diagnostic.ranked_fix_order, start=1)
    )
    rhythm = "\n".join(f"- {item}" for item in diagnostic.weekly_rhythm)

    return f"""# Growth Goaled Snapshot

Company: {company.company_summary}

## Scores
- Sales Efficiency: {scores.sales_efficiency}/100
- Funnel Efficiency: {scores.funnel_efficiency}/100
- Founder Dependency: {scores.founder_dependency}/100

## Executive Summary
{diagnostic.executive_summary}

## Key Insights
{insights}

## Ranked Fix Order
{fixes}

## 90-Day Roadmap
{roadmap}

## Weekly Rhythm
{rhythm}

## Board Narrative
{diagnostic.board_narrative}
"""


def build_export_pdf(company: CompanyProfile, diagnostic: DiagnosticOutput) -> bytes:
    """Build a simple dependency-free PDF for the MVP download."""
    log_step("STEP 8 | Building PDF export")
    source_text = build_export_text(company, diagnostic)
    lines = _wrap_export_lines(source_text)
    pages = _paginate_lines(lines, lines_per_page=48)

    objects: list[str] = []
    catalog_id = _add_object(objects, "<< /Type /Catalog /Pages 2 0 R >>")
    page_ids: list[int] = []

    # Reserve object 2 for the Pages tree after we know all page ids.
    objects.append("")

    font_id = _add_object(objects, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    bold_font_id = _add_object(
        objects, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
    )

    for page_lines in pages:
        content_id = _add_object(objects, _content_stream(page_lines))
        page_id = _add_object(
            objects,
            (
                "<< /Type /Page /Parent 2 0 R "
                "/MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 {font_id} 0 R /F2 {bold_font_id} 0 R >> >> "
                f"/Contents {content_id} 0 R >>"
            ),
        )
        page_ids.append(page_id)

    objects[1] = (
        f"2 0 obj\n<< /Type /Pages /Kids [{' '.join(f'{page_id} 0 R' for page_id in page_ids)}] "
        f"/Count {len(page_ids)} >>\nendobj\n"
    )

    return _serialize_pdf(objects, catalog_id)


def _wrap_export_lines(text: str) -> list[tuple[str, bool]]:
    lines: list[tuple[str, bool]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            lines.append(("", False))
            continue

        is_heading = line.startswith("#")
        clean_line = line.lstrip("#").strip() if is_heading else line
        width = 68 if is_heading else 86
        wrapped = textwrap.wrap(clean_line, width=width) or [""]
        for wrapped_line in wrapped:
            lines.append((wrapped_line, is_heading))

    return lines


def _paginate_lines(
    lines: list[tuple[str, bool]],
    lines_per_page: int,
) -> list[list[tuple[str, bool]]]:
    return [lines[index : index + lines_per_page] for index in range(0, len(lines), lines_per_page)]


def _content_stream(lines: list[tuple[str, bool]]) -> str:
    commands = ["BT", "50 748 Td", "14 TL"]
    first_line = True

    for text, is_heading in lines:
        if not first_line:
            commands.append("T*")
        first_line = False

        if is_heading:
            commands.append("/F2 13 Tf")
        else:
            commands.append("/F1 10 Tf")
        commands.append(f"({_escape_pdf_text(text)}) Tj")

    commands.append("ET")
    stream = "\n".join(commands)
    byte_length = len(stream.encode("latin-1", errors="replace"))
    return f"<< /Length {byte_length} >>\nstream\n{stream}\nendstream"


def _escape_pdf_text(text: str) -> str:
    clean = text.encode("latin-1", errors="replace").decode("latin-1")
    return clean.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _add_object(objects: list[str], body: str) -> int:
    object_id = len(objects) + 1
    objects.append(f"{object_id} 0 obj\n{body}\nendobj\n")
    return object_id


def _serialize_pdf(objects: list[str], catalog_id: int) -> bytes:
    pdf = "%PDF-1.4\n%\xE2\xE3\xCF\xD3\n"
    offsets = [0]

    for obj in objects:
        offsets.append(len(pdf.encode("latin-1", errors="replace")))
        pdf += obj

    xref_offset = len(pdf.encode("latin-1", errors="replace"))
    pdf += f"xref\n0 {len(objects) + 1}\n"
    pdf += "0000000000 65535 f \n"
    for offset in offsets[1:]:
        pdf += f"{offset:010d} 00000 n \n"
    pdf += (
        "trailer\n"
        f"<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
        "startxref\n"
        f"{xref_offset}\n"
        "%%EOF\n"
    )
    return pdf.encode("latin-1", errors="replace")
