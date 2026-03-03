#!/usr/bin/env python

"""
MusicXML to PDF Renderer
========================
Converts MusicXML files to PDF with western staff notation using
Verovio (MusicXML → SVG per page) and svglib/reportlab (SVG → PDF).

Three pre-processing steps are applied to verovio's SVG before svglib:

  1. Flatten nested <svg>. Verovio wraps all score content in an inner
     <svg viewBox="0 0 21000 3520"> so its large internal coordinate
     space maps correctly to pixels. svglib ignores nested-SVG viewBox
     transforms, so coordinates like translate(90, 1806) are treated as
     raw pixels and land off-screen. Promoting the viewBox to the outer
     <svg> fixes the coordinate mapping.

  2. Inline <use xlink:href="#id"> elements. Verovio stores SMuFL music
     font glyphs in <defs> and references them via <use>, which svglib
     cannot resolve. Each <use> is replaced with a deep copy of the
     referenced content.

  3. Fix malformed 5-digit hex colours (#00000 → #000000) emitted by
     verovio that svglib cannot parse.

Dependencies (all pip-installable, no external applications required):
    pip install verovio svglib reportlab lxml
"""

import copy
import os
import tempfile
from pathlib import Path
from typing import Optional

import lxml.etree as ET
import verovio
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

# A4 in verovio units (tenths of a millimetre: 210mm → 2100, 297mm → 2970)
_A4_VRV_W = 2100
_A4_VRV_H = 2970

_SVG_NS     = 'http://www.w3.org/2000/svg'
_XLINK_NS   = 'http://www.w3.org/1999/xlink'
_SVG_TAG    = f'{{{_SVG_NS}}}svg'
_USE_TAG    = f'{{{_SVG_NS}}}use'
_TITLE_TAG  = f'{{{_SVG_NS}}}title'
_TEXT_TAG   = f'{{{_SVG_NS}}}text'
_XLINK_HREF = f'{{{_XLINK_NS}}}href'
_TSPAN_TAG  = f'{{{_SVG_NS}}}tspan'


def _flatten_nested_svg(root: ET.Element) -> ET.Element:
    """
    Verovio wraps score content in an inner <svg> with a viewBox.
    svglib doesn't apply viewBox scaling on nested SVGs, so we promote
    the inner SVG's viewBox to the outer element and inline its children.
    """
    inner_svg = None
    inner_idx = None
    for i, child in enumerate(root):
        if child.tag == _SVG_TAG:
            inner_svg = child
            inner_idx = i
            break

    if inner_svg is None:
        return root

    # Promote viewBox so svglib scales coordinates correctly
    viewBox = inner_svg.get('viewBox')
    if viewBox:
        root.set('viewBox', viewBox)

    # Copy text/style attributes used by score content
    for attr in ('color', 'font-family', 'font-size'):
        val = inner_svg.get(attr)
        if val:
            root.set(attr, val)

    # Replace the inner <svg> node with its children in-place
    root.remove(inner_svg)
    for j, child in enumerate(inner_svg):
        root.insert(inner_idx + j, child)

    return root


def _inline_use_elements(root: ET.Element) -> ET.Element:
    """
    Replace every <use xlink:href="#id"> with an inline <g> containing
    a deep copy of the referenced <defs> content. Iterates up to 5 times
    to handle any nested <use> references.
    """
    id_map: dict = {}
    for elem in root.iter():
        eid = elem.get('id')
        if eid:
            id_map[eid] = elem

    for _ in range(5):
        changed = False
        for parent in root.iter():
            for i, child in list(enumerate(parent)):
                if child.tag != _USE_TAG:
                    continue
                href = child.get(_XLINK_HREF) or child.get('href', '')
                if not href.startswith('#'):
                    continue
                ref_elem = id_map.get(href[1:])
                if ref_elem is None:
                    continue

                g = ET.Element(f'{{{_SVG_NS}}}g')
                parts = []
                x = child.get('x', '0') or '0'
                y = child.get('y', '0') or '0'
                if x != '0' or y != '0':
                    parts.append(f'translate({x},{y})')
                tf = child.get('transform', '')
                if tf:
                    parts.append(tf)
                if parts:
                    g.set('transform', ' '.join(parts))

                for ref_child in ref_elem:
                    g.append(copy.deepcopy(ref_child))

                parent.remove(child)
                parent.insert(i, g)
                changed = True

        if not changed:
            break

    return root


def _fix_title_rendering(root: ET.Element) -> ET.Element:
    """
    Three svglib quirks with how verovio marks up its title text:

    1. <title class="labelAttr">title</title> — SVG <title> elements are
       tooltips/accessibility labels, not visible text. svglib incorrectly
       renders them as visible characters, producing the spurious word
       "title" in the PDF. Strip them entirely.

    2. The enclosing <text font-size="0px"> — verovio sets 0px on the outer
       element and relies on child <tspan> overrides for the real size.
       svglib doesn't propagate tspan overrides, so it renders the text
       invisibly. Remove the 0px attribute so the tspan size is used.

    3. text-anchor="middle" and x/y position are set on the first child
       <tspan>, not on the outer <text>. svglib only honours text-anchor on
       <text>, so we promote those attributes up to the outer element.
    """
    for parent in root.iter():
        for child in list(parent):
            if child.tag == _TITLE_TAG:
                parent.remove(child)

    for elem in root.iter(_TEXT_TAG):
        if elem.get('font-size') == '0px':
            del elem.attrib['font-size']

        # Promote centering attrs from the first tspan so svglib centres it
        for child in elem:
            if child.tag == _TSPAN_TAG and child.get('text-anchor') == 'middle':
                elem.set('text-anchor', 'middle')
                for attr in ('x', 'y'):
                    val = child.get(attr)
                    if val is not None:
                        elem.set(attr, val)
                break

    return root


def _preprocess_svg(svg_str: str) -> bytes:
    """Apply all SVG pre-processing steps before passing to svglib."""
    # Fix malformed 5-digit hex colours
    svg_str = svg_str.replace('#00000', '#000000')

    root = ET.fromstring(svg_str.encode('utf-8'))
    root = _flatten_nested_svg(root)
    root = _inline_use_elements(root)
    root = _fix_title_rendering(root)

    return ET.tostring(root, encoding='unicode').encode('utf-8')


def convert_to_pdf(
    musicxml_path: str,
    output_path: Optional[str] = None,
    scale: int = 40,
) -> str:
    """
    Convert a MusicXML file to a PDF with western staff notation.

    Args:
        musicxml_path: Path to the input .musicxml file.
        output_path:   Output PDF path. Defaults to the same folder as the
                       input file with a .pdf extension.
        scale:         Verovio render scale as a percentage (default 40).
                       Raise to enlarge note heads; lower to fit more
                       measures per line.

    Returns:
        Absolute path to the generated PDF file.

    Raises:
        FileNotFoundError: If the input file does not exist.
        RuntimeError:      If Verovio fails to load the file.
    """
    musicxml_path = Path(musicxml_path)
    if not musicxml_path.exists():
        raise FileNotFoundError(f"Input file not found: {musicxml_path}")

    if output_path is None:
        output_path = musicxml_path.with_suffix('.pdf')
    else:
        output_path = Path(output_path)

    tk = verovio.toolkit()
    tk.setOptions({
        "pageWidth":  _A4_VRV_W,
        "pageHeight": _A4_VRV_H,
        "scale": scale,
        "adjustPageHeight": 1,
    })

    if not tk.loadFile(str(musicxml_path)):
        raise RuntimeError(f"Verovio could not load: {musicxml_path}")

    page_count = tk.getPageCount()
    page_w_pt, page_h_pt = A4
    pdf = canvas.Canvas(str(output_path), pagesize=A4)

    temp_files = []
    try:
        for page_num in range(1, page_count + 1):
            svg_str = tk.renderToSVG(page_num)
            svg_processed = _preprocess_svg(svg_str)

            with tempfile.NamedTemporaryFile(
                suffix='.svg', mode='wb', delete=False
            ) as tmp:
                tmp.write(svg_processed)
                temp_svg = tmp.name
            temp_files.append(temp_svg)

            drawing = svg2rlg(temp_svg)
            if not drawing or drawing.width == 0 or drawing.height == 0:
                continue

            sf = min(page_w_pt / drawing.width, page_h_pt / drawing.height)
            drawing.width  *= sf
            drawing.height *= sf
            drawing.transform = (sf, 0, 0, sf, 0, 0)

            y_pos = page_h_pt - drawing.height
            renderPDF.draw(drawing, pdf, 0, y_pos)
            pdf.showPage()

    finally:
        for f in temp_files:
            try:
                os.unlink(f)
            except FileNotFoundError:
                pass

    pdf.save()
    return str(output_path.resolve())


# ---------------------------------------------------------------------------
# Convenience CLI when run directly
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    fp = input("MusicXML file path: ").strip()
    out = convert_to_pdf(fp)
    print(f"Written to: {out}")
