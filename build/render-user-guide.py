#!/usr/bin/env python3
"""Render the Markdown user guide with links, bookmarks and a paginated contents."""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from markdown_it import MarkdownIt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, NextPageTemplate, PageBreak, PageTemplate,
    Paragraph, Preformatted, Spacer, Table, TableStyle, KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
BLUE = colors.HexColor("#466887")
INK = colors.HexColor("#202a35")
MUTED = colors.HexColor("#627282")
PAPER = colors.HexColor("#f2f5f8")


def fonts():
    candidates = [
        (Path("/usr/share/fonts/truetype/dejavu"),
         ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans-Oblique.ttf", "DejaVuSans-BoldOblique.ttf"]),
        (Path("/System/Library/Fonts/Supplemental"),
         ["Arial.ttf", "Arial Bold.ttf", "Arial Italic.ttf", "Arial Bold Italic.ttf"]),
    ]
    for directory, names in candidates:
        if all((directory / name).exists() for name in names):
            for suffix, name in zip(["", "-Bold", "-Italic", "-BoldItalic"], names):
                pdfmetrics.registerFont(TTFont("Guide" + suffix, str(directory / name)))
            pdfmetrics.registerFontFamily("Guide", normal="Guide", bold="Guide-Bold",
                                         italic="Guide-Italic", boldItalic="Guide-BoldItalic")
            return
    raise SystemExit("Install fonts-dejavu-core, or provide the standard macOS Arial fonts.")


def slug(text):
    return re.sub(r"[^\w -]", "", text.lower()).replace(" ", "-")


def inline(token):
    result = []
    for part in token.children or []:
        if part.type == "text":
            result.append(html.escape(part.content))
        elif part.type == "code_inline":
            result.append('<font name="Courier" size="8.6">' + html.escape(part.content) + "</font>")
        elif part.type in {"strong_open", "strong_close", "em_open", "em_close"}:
            result.append({"strong_open": "<b>", "strong_close": "</b>",
                           "em_open": "<i>", "em_close": "</i>"}[part.type])
        elif part.type == "link_open":
            href = html.escape(part.attrGet("href") or "", quote=True)
            result.append(f'<a href="{href}" color="#466887">')
        elif part.type == "link_close":
            result.append("</a>")
        elif part.type in {"softbreak", "hardbreak"}:
            result.append("<br/>" if part.type == "hardbreak" else " ")
        else:
            raise ValueError(f"Unsupported inline token: {part.type}")
    return "".join(result)


class GuideDoc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if getattr(flowable, "section_key", None):
            key = flowable.section_key
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.section_title, key, level=0)
            self.notify("TOCEntry", (0, flowable.section_title, self.page, key))


def page_header(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFont("Guide-Bold", 9)
    canvas.setFillColor(BLUE)
    canvas.drawString(48, height - 31, "RILEX / USER GUIDE")
    canvas.setFont("Guide", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 48, height - 31, "0.1 / OCTOBER 2026")
    canvas.setStrokeColor(colors.HexColor("#d8e0e8"))
    canvas.line(48, height - 40, width - 48, height - 40)
    canvas.setFont("Guide", 8)
    canvas.drawString(48, 28, "Installation / keyboard workflows / maintenance")
    canvas.drawRightString(width - 48, 28, str(doc.page))
    canvas.restoreState()


def cover(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(INK)
    canvas.rect(0, 0, width, height, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor("#7699bc"))
    canvas.rect(48, height - 173, 58, 5, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Guide-Bold", 48)
    canvas.drawString(48, height - 240, "Rilex")
    canvas.setFont("Guide", 25)
    canvas.drawString(48, height - 285, "User Guide")
    canvas.setFont("Guide", 12)
    canvas.setFillColor(colors.HexColor("#c6d2df"))
    for n, line in enumerate(["Installation, keyboard workflows,", "customization, and maintenance"]):
        canvas.drawString(48, height - 336 - n * 20, line)
    canvas.setFont("Guide", 11)
    canvas.drawString(48, 164, "Rilex 0.1 / Debian 13 Trixie / x86-64")
    canvas.drawString(48, 143, "11 October 2026")
    canvas.setFont("Guide", 10)
    canvas.drawString(48, 88, "A Linux desktop built for people who prefer keyboards to mice.")
    canvas.restoreState()


def render(source, output):
    fonts()
    body = ParagraphStyle("GuideBody", fontName="Guide", fontSize=10,
                          leading=14.5, textColor=INK, spaceAfter=8)
    h2 = ParagraphStyle("GuideSection", parent=body, fontName="Guide-Bold",
                        fontSize=19, leading=25, spaceBefore=13, spaceAfter=12,
                        textColor=BLUE, keepWithNext=True)
    h3 = ParagraphStyle("GuideSubsection", parent=body, fontName="Guide-Bold",
                        fontSize=12, leading=17, spaceBefore=10, spaceAfter=6,
                        keepWithNext=True)
    cell = ParagraphStyle("GuideCell", parent=body, fontSize=8.7, leading=12,
                          spaceAfter=0)
    code = ParagraphStyle("GuideCode", fontName="Courier", fontSize=8,
                          leading=11, leftIndent=9, rightIndent=9,
                          borderPadding=9, backColor=PAPER, spaceBefore=3, spaceAfter=12)
    tokens = MarkdownIt("commonmark").enable("table").parse(source.read_text())
    story = [Spacer(1, 1), NextPageTemplate("body"), PageBreak()]
    width, height = A4
    usable = width - 96
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = GuideDoc(str(output), pagesize=A4, title="Rilex 0.1 User Guide",
                   author="Rilex Project", leftMargin=48, rightMargin=48,
                   topMargin=56, bottomMargin=48)
    frame = Frame(48, 48, usable, height - 104, leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate("cover", [frame], onPage=cover),
                          PageTemplate("body", [frame], onPage=page_header)])
    list_stack = []
    list_marker = None
    i = 0
    skip_contents = False
    while i < len(tokens):
        token = tokens[i]
        if token.type == "heading_open":
            label = tokens[i + 1].content
            if token.tag == "h1":
                story.append(Paragraph("About this guide", h2))
                i += 3
                continue
            if label == "Contents":
                story.append(PageBreak())
                story.append(Paragraph("Contents", h2))
                toc = TableOfContents()
                toc.levelStyles = [ParagraphStyle("GuideTOC", parent=body,
                                                  fontSize=10, leading=17, spaceBefore=3)]
                story.append(toc)
                story.append(PageBreak())
                skip_contents = True
                i += 3
                continue
            skip_contents = False
            heading = Paragraph(inline(tokens[i + 1]), h2 if token.tag == "h2" else h3)
            if token.tag == "h2":
                # Long chapters start cleanly; short chapters may share a page.
                if label.startswith(("8.", "12.", "16.", "18.")):
                    story.append(PageBreak())
                heading.section_key = slug(label)
                heading.section_title = label
            story.append(heading)
            i += 3
            continue
        if skip_contents:
            i += 1
            continue
        if token.type in {"bullet_list_open", "ordered_list_open"}:
            list_stack.append([token.type, int(token.attrGet("start") or 1)])
        elif token.type in {"bullet_list_close", "ordered_list_close"}:
            list_stack.pop()
        elif token.type == "list_item_open":
            kind, number = list_stack[-1]
            list_marker = "-" if kind == "bullet_list_open" else f"{number}."
            list_stack[-1][1] += 1
        elif token.type == "paragraph_open":
            para_style = body
            if list_stack:
                para_style = ParagraphStyle("GuideList", parent=body, leftIndent=18,
                                             bulletIndent=1, spaceAfter=5)
            if i + 3 < len(tokens) and tokens[i + 3].type == "fence":
                para_style = ParagraphStyle("BeforeCode", parent=para_style, keepWithNext=True)
            story.append(Paragraph(inline(tokens[i + 1]), para_style, bulletText=list_marker))
            list_marker = None
            i += 3
            continue
        elif token.type == "fence":
            text = token.content.rstrip()
            # Shrink only exceptionally long lines; never silently change commands.
            longest = max((pdfmetrics.stringWidth(line, "Courier", 8) for line in text.splitlines()), default=0)
            size = min(8, 8 * (usable - 24) / max(longest, 1))
            if size < 6.3:
                raise ValueError("Code line too long for legible output; wrap it in Markdown.")
            cs = ParagraphStyle("SizedCode", parent=code, fontSize=size, leading=size * 1.375)
            story.append(KeepTogether([Preformatted(text, cs)]))
        elif token.type == "table_open":
            rows = []
            row = []
            j = i + 1
            while tokens[j].type != "table_close":
                t = tokens[j]
                if t.type == "tr_open":
                    row = []
                elif t.type == "inline":
                    row.append(Paragraph(inline(t), cell))
                elif t.type == "tr_close":
                    rows.append(row)
                j += 1
            count = len(rows[0])
            fractions = {2: [0.43, 0.57], 3: [0.2, 0.4, 0.4],
                         4: [0.12, 0.24, 0.32, 0.32]}.get(count, [1 / count] * count)
            table = Table(rows, colWidths=[usable * f for f in fractions], repeatRows=1,
                          hAlign="LEFT", spaceBefore=4, spaceAfter=13)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce7f1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, colors.white]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#a5b7ca")),
            ]))
            story.append(table)
            i = j
        i += 1
    doc.multiBuild(story)
    print(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "docs/user-guide.md")
    parser.add_argument("--output", type=Path, default=ROOT / "output/pdf/rilex-0.1-user-guide.pdf")
    args = parser.parse_args()
    render(args.source, args.output)
