"""Render native-deck diagram mirrors from the reviewed Neo4j visual design.

The Google Slides objects remain the editable delivery. These vector mirrors use
identical point coordinates, circular graph records and full relationship names.
"""

from __future__ import annotations

import json
import textwrap
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def render(element: dict) -> str:
    """Render one native scene primitive as editable SVG geometry/text."""
    kind = element["kind"]
    if kind == "line":
        arrow = ' marker-end="url(#arrow)"' if element["arrow"] else ""
        dash = ' stroke-dasharray="5 4"' if element.get("dash") else ""
        return (
            f'<line x1="{element["x1"]}" y1="{element["y1"]}" '
            f'x2="{element["x2"]}" y2="{element["y2"]}" '
            f'stroke="#{element["color"]}" stroke-width="{element["width"]}"'
            f'{arrow}{dash}/>'
        )
    x, y, width, height = (element[k] for k in ("x", "y", "w", "h"))
    fill = "none" if element.get("transparent") else "#" + element.get("fill", "ffffff")
    stroke = "#" + element["stroke"] if element.get("stroke") else "none"
    outline = f'fill="{fill}" stroke="{stroke}" stroke-width="{element.get("strokeWidth", 1)}"'
    if kind == "ELLIPSE":
        result = (
            f'<circle cx="{x + width / 2}" cy="{y + height / 2}" '
            f'r="{width / 2}" {outline}/>'
        )
    else:
        radius = 12 if kind == "ROUND_RECTANGLE" else 0
        result = (
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'rx="{radius}" {outline}/>'
        )
    if not element.get("text"):
        return result
    size = element["fontSize"]
    # Match the native textbox side insets; preserve intentional line breaks.
    columns = max(1, int((width - 14.4) / (size * 0.57)))
    lines = []
    for paragraph in element["text"].split("\n"):
        lines.extend(textwrap.wrap(paragraph, columns, break_long_words=False) or [""])
    line_height = size * 1.08
    top = y + height / 2 - (len(lines) - 1) * line_height / 2 + size * 0.34
    centered = element.get("align") == "CENTER"
    anchor = "middle" if centered else "start"
    tx = x + width / 2 if centered else x + 7.2
    weight = 700 if element.get("bold") else 400
    font = escape(element["font"])
    color = element["textColor"]
    for index, line in enumerate(lines):
        result += (
            f'<text x="{tx}" y="{top + index * line_height}" '
            f'text-anchor="{anchor}" font-family="{font}, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="#{color}">'
            f'{escape(line)}</text>'
        )
    return result


def main() -> None:
    """Write the full-slide illustrations and any graph-only detail views."""
    design = json.loads((ROOT.parent / "visual-design.json").read_text())
    for diagram in design["diagrams"]:
        x, y, width, height = diagram.get("view_box", [0, 0, 720, 405])
        background = diagram.get("background", "faf8f5")
        arrow_color = "ffffff" if background == "0a6190" else "0a6190"
        description = diagram.get("description")
        content = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width * 2}" height="{height * 2}" '
            f'viewBox="{x} {y} {width} {height}" role="img">'
            f'<title>{escape(diagram["title"])}</title>'
        )
        if description:
            content += f'<desc>{escape(description)}</desc>'
        content += (
            '<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
            'refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" '
            f'fill="#{arrow_color}"/></marker></defs>'
        )
        if "view_box" in diagram:
            content += (
                f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="#{background}"/>'
            )
        else:
            content += (
                f'<rect width="720" height="405" fill="#{background}"/>'
                '<rect width="5" height="405" fill="#4e9ca6"/>'
                '<text x="29" y="24" font-family="Public Sans, sans-serif" '
                'font-size="10" font-weight="700" fill="#0a6190">'
                f'{escape(diagram["section"])}</text>'
                '<text x="29" y="62" font-family="Syne, sans-serif" '
                f'font-size="26" fill="#004063">{escape(diagram["title"])}</text>'
            )
        content += "".join(render(element) for element in diagram["elements"])
        (ROOT / diagram["file"]).write_text(content + "</svg>\n")
    print(f"Rendered {len(design['diagrams'])} branded diagram mirrors")


if __name__ == "__main__":
    main()
