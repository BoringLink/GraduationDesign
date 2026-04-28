#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path("/Users/tk/Documents/杭州电子科技大学/毕业设计")
THESIS_DIR = ROOT / "latex" / "thesis"
TEMPLATE_DIR = THESIS_DIR / "template"
SOURCE_DOCX = TEMPLATE_DIR / "hdu-template.docx"
OUTPUT_DOCX = TEMPLATE_DIR / "毕业论文模板-规范样式.docx"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

ET.register_namespace("w", NS["w"])
ET.register_namespace("r", NS["r"])


def w_tag(tag: str) -> str:
    return f"{{{NS['w']}}}{tag}"


def attr(name: str, value: str) -> tuple[str, str]:
    return w_tag(name), value


def child(
    parent: ET.Element, tag: str, attrs: dict[str, str] | None = None
) -> ET.Element:
    element = ET.SubElement(parent, w_tag(tag))
    if attrs:
        for key, value in attrs.items():
            element.set(w_tag(key), value)
    return element


def clear(element: ET.Element) -> None:
    for item in list(element):
        element.remove(item)
    element.attrib.clear()


def r_pr(font_east: str, font_latin: str, size: int, bold: bool = False) -> ET.Element:
    rpr = ET.Element(w_tag("rPr"))
    child(
        rpr,
        "rFonts",
        {
            "ascii": font_latin,
            "hAnsi": font_latin,
            "eastAsia": font_east,
            "cs": font_latin,
        },
    )
    if bold:
        child(rpr, "b")
        child(rpr, "bCs")
    child(rpr, "kern", {"val": "2"})
    child(rpr, "sz", {"val": str(size)})
    child(rpr, "szCs", {"val": str(size)})
    child(rpr, "lang", {"val": "en-US", "eastAsia": "zh-CN"})
    return rpr


def spacing(
    before: int | None = None,
    after: int | None = None,
    line: int | None = None,
    line_rule: str | None = None,
) -> ET.Element:
    element = ET.Element(w_tag("spacing"))
    if before is not None:
        element.set(w_tag("before"), str(before))
    if after is not None:
        element.set(w_tag("after"), str(after))
    if line is not None:
        element.set(w_tag("line"), str(line))
    if line_rule is not None:
        element.set(w_tag("lineRule"), line_rule)
    return element


def make_ppr(
    justify: str = "both",
    before: int | None = None,
    after: int | None = None,
    line: int | None = 400,
    line_rule: str | None = "exact",
    outline: int | None = None,
    keep_next: bool = False,
    keep_lines: bool = False,
    page_break_before: bool = False,
    first_line_chars: int | None = None,
    left_chars: int | None = None,
    hanging_chars: int | None = None,
) -> ET.Element:
    ppr = ET.Element(w_tag("pPr"))
    if keep_next:
        child(ppr, "keepNext")
    if keep_lines:
        child(ppr, "keepLines")
    if page_break_before:
        child(ppr, "pageBreakBefore")
    ppr.append(spacing(before=before, after=after, line=line, line_rule=line_rule))
    child(ppr, "jc", {"val": justify})
    if (
        first_line_chars is not None
        or left_chars is not None
        or hanging_chars is not None
    ):
        ind = child(ppr, "ind")
        if first_line_chars is not None:
            ind.set(w_tag("firstLineChars"), str(first_line_chars))
            ind.set(w_tag("firstLine"), "420")
        if left_chars is not None:
            ind.set(w_tag("leftChars"), str(left_chars))
            ind.set(w_tag("left"), str(left_chars * 2))
        if hanging_chars is not None:
            ind.set(w_tag("hangingChars"), str(hanging_chars))
            ind.set(w_tag("hanging"), "420")
    if outline is not None:
        child(ppr, "outlineLvl", {"val": str(outline)})
    return ppr


def upsert_style(
    styles_root: ET.Element,
    style_id: str,
    name: str,
    style_type: str = "paragraph",
    based_on: str | None = None,
    next_style: str | None = None,
    ppr: ET.Element | None = None,
    rpr: ET.Element | None = None,
    qformat: bool = True,
    custom: bool = True,
    default: bool = False,
) -> ET.Element:
    style = styles_root.find(f"w:style[@w:styleId='{style_id}']", NS)
    if style is None:
        style = ET.SubElement(styles_root, w_tag("style"))
    clear(style)
    style.set(w_tag("type"), style_type)
    style.set(w_tag("styleId"), style_id)
    if custom:
        style.set(w_tag("customStyle"), "1")
    if default:
        style.set(w_tag("default"), "1")
    child(style, "name", {"val": name})
    if based_on:
        child(style, "basedOn", {"val": based_on})
    if next_style:
        child(style, "next", {"val": next_style})
    if qformat:
        child(style, "qFormat")
    if ppr is not None:
        style.append(ppr)
    if rpr is not None:
        style.append(rpr)
    return style


def patch_styles(styles_xml: Path) -> None:
    tree = ET.parse(styles_xml)
    root = tree.getroot()

    doc_defaults = root.find("w:docDefaults", NS)
    if doc_defaults is None:
        doc_defaults = ET.Element(w_tag("docDefaults"))
        root.insert(0, doc_defaults)
    rpr_default = doc_defaults.find("w:rPrDefault", NS)
    if rpr_default is None:
        rpr_default = child(doc_defaults, "rPrDefault")
    clear(rpr_default)
    rpr_default.append(r_pr("宋体", "Times New Roman", 24))

    upsert_style(
        root,
        "a",
        "Normal",
        custom=False,
        default=True,
        ppr=make_ppr(justify="both", first_line_chars=200),
        rpr=r_pr("宋体", "Times New Roman", 24),
    )
    upsert_style(
        root,
        "1",
        "heading 1",
        custom=False,
        based_on="a",
        next_style="a",
        ppr=make_ppr(
            "center",
            before=480,
            after=480,
            line=None,
            line_rule=None,
            outline=0,
            keep_next=True,
            keep_lines=True,
            page_break_before=True,
        ),
        rpr=r_pr("黑体", "Times New Roman", 32, bold=True),
    )
    upsert_style(
        root,
        "2",
        "heading 2",
        custom=False,
        based_on="a",
        next_style="a",
        ppr=make_ppr("left", outline=1, keep_next=True, keep_lines=True),
        rpr=r_pr("黑体", "Times New Roman", 28, bold=True),
    )
    upsert_style(
        root,
        "3",
        "heading 3",
        custom=False,
        based_on="a",
        next_style="a",
        ppr=make_ppr("left", outline=2, keep_next=True, keep_lines=True),
        rpr=r_pr("黑体", "Times New Roman", 24, bold=True),
    )

    upsert_style(
        root,
        "HDUAbstractTitle",
        "HDU 摘要标题",
        based_on="1",
        ppr=make_ppr("center", before=480, after=480, line=None, line_rule=None),
        rpr=r_pr("黑体", "Times New Roman", 32, bold=True),
    )
    upsert_style(
        root,
        "HDUAbstractText",
        "HDU 中文摘要正文",
        based_on="a",
        ppr=make_ppr("both"),
        rpr=r_pr("宋体", "Times New Roman", 24),
    )
    upsert_style(
        root,
        "HDUAbstractTitleEn",
        "HDU ABSTRACT 标题",
        based_on="HDUAbstractTitle",
        ppr=make_ppr("center", before=480, after=480, line=None, line_rule=None),
        rpr=r_pr("Times New Roman", "Times New Roman", 32, bold=True),
    )
    upsert_style(
        root,
        "HDUAbstractTextEn",
        "HDU 英文摘要正文",
        based_on="a",
        ppr=make_ppr("both"),
        rpr=r_pr("Times New Roman", "Times New Roman", 24),
    )
    upsert_style(
        root,
        "HDUKeywords",
        "HDU 关键词段落",
        based_on="a",
        ppr=make_ppr("left"),
        rpr=r_pr("宋体", "Times New Roman", 24),
    )
    upsert_style(
        root,
        "HDUTocTitle",
        "HDU 目录标题",
        based_on="HDUAbstractTitle",
        ppr=make_ppr("center", before=480, after=480, line=None, line_rule=None),
        rpr=r_pr("黑体", "Times New Roman", 32, bold=True),
    )
    upsert_style(
        root,
        "HDUReferenceTitle",
        "HDU 参考文献标题",
        based_on="HDUAbstractTitle",
        ppr=make_ppr("center", before=480, after=480, line=None, line_rule=None),
        rpr=r_pr("黑体", "Times New Roman", 32, bold=True),
    )
    upsert_style(
        root,
        "HDUReferenceItem",
        "HDU 参考文献条目",
        based_on="a",
        ppr=make_ppr("both", first_line_chars=None, hanging_chars=200),
        rpr=r_pr("宋体", "Times New Roman", 21),
    )
    upsert_style(
        root,
        "HDUFigureCaption",
        "HDU 图题",
        based_on="a",
        ppr=make_ppr("center", first_line_chars=None),
        rpr=r_pr("宋体", "Times New Roman", 21),
    )
    upsert_style(
        root,
        "HDUTableCaption",
        "HDU 表题",
        based_on="HDUFigureCaption",
        ppr=make_ppr("center", first_line_chars=None),
        rpr=r_pr("宋体", "Times New Roman", 21),
    )
    upsert_style(
        root,
        "HDUEquation",
        "HDU 公式",
        based_on="a",
        ppr=make_ppr("center", first_line_chars=None),
        rpr=r_pr("宋体", "Times New Roman", 21),
    )
    upsert_style(
        root,
        "HDUTableText",
        "HDU 表格文字",
        based_on="a",
        ppr=make_ppr("center", first_line_chars=None),
        rpr=r_pr("宋体", "Times New Roman", 21),
    )

    upsert_style(
        root,
        "aa",
        "Body Text",
        custom=False,
        based_on="a",
        ppr=make_ppr("both", first_line_chars=200),
        rpr=r_pr("宋体", "Times New Roman", 24),
    )
    upsert_style(
        root,
        "21",
        "Body Text Indent 2",
        custom=False,
        based_on="a",
        ppr=make_ppr("both", first_line_chars=200),
        rpr=r_pr("宋体", "Times New Roman", 24),
    )
    upsert_style(
        root,
        "Caption",
        "caption",
        custom=False,
        based_on="a",
        ppr=make_ppr("center", first_line_chars=None),
        rpr=r_pr("宋体", "Times New Roman", 21),
    )
    upsert_style(
        root,
        "10",
        "目录 1",
        custom=False,
        based_on="a",
        ppr=make_ppr("left", first_line_chars=None),
        rpr=r_pr("宋体", "Times New Roman", 24),
    )
    upsert_style(
        root,
        "22",
        "目录 2",
        custom=False,
        based_on="a",
        ppr=make_ppr("left", first_line_chars=None, left_chars=200),
        rpr=r_pr("宋体", "Times New Roman", 24),
    )
    upsert_style(
        root,
        "TOC3",
        "目录 3",
        custom=False,
        based_on="a",
        ppr=make_ppr("left", first_line_chars=None, left_chars=400),
        rpr=r_pr("宋体", "Times New Roman", 24),
    )
    upsert_style(
        root,
        "a4",
        "header",
        custom=False,
        based_on="a",
        ppr=make_ppr("center", line=None, line_rule=None, first_line_chars=None),
        rpr=r_pr("宋体", "Times New Roman", 21),
    )
    upsert_style(
        root,
        "ab",
        "footer",
        custom=False,
        based_on="a",
        ppr=make_ppr("center", line=None, line_rule=None, first_line_chars=None),
        rpr=r_pr("宋体", "Times New Roman", 21),
    )
    upsert_style(
        root,
        "a6",
        "page number",
        "character",
        custom=False,
        rpr=r_pr("Times New Roman", "Times New Roman", 21),
    )
    upsert_style(
        root,
        "HDUKeywordLabelCn",
        "HDU 关键词标签",
        "character",
        rpr=r_pr("黑体", "Times New Roman", 24, bold=True),
    )
    upsert_style(
        root,
        "HDUKeywordLabelEn",
        "HDU Key words 标签",
        "character",
        rpr=r_pr("Times New Roman", "Times New Roman", 24, bold=True),
    )
    upsert_style(
        root,
        "HDUKeywordText",
        "HDU 关键词文本",
        "character",
        rpr=r_pr("宋体", "Times New Roman", 24),
    )

    tree.write(styles_xml, encoding="utf-8", xml_declaration=True)


def patch_sections(document_xml: Path) -> None:
    tree = ET.parse(document_xml)
    root = tree.getroot()
    for pg_mar in root.findall(".//w:pgMar", NS):
        pg_mar.set(w_tag("header"), "1134")
        pg_mar.set(w_tag("footer"), "567")
    tree.write(document_xml, encoding="utf-8", xml_declaration=True)


def patch_headers(tmp_dir: Path) -> None:
    header_text = "杭州电子科技大学继续教育学院本科毕业设计（论文）"
    for header_xml in (tmp_dir / "word").glob("header*.xml"):
        tree = ET.parse(header_xml)
        root = tree.getroot()
        paragraphs = root.findall(".//w:p", NS)
        if not paragraphs:
            continue
        p = paragraphs[0]
        for item in list(p):
            p.remove(item)
        ppr = child(p, "pPr")
        child(ppr, "pStyle", {"val": "a4"})
        child(ppr, "jc", {"val": "center"})
        run = child(p, "r")
        run.append(r_pr("宋体", "Times New Roman", 21))
        t = child(run, "t")
        t.text = header_text
        tree.write(header_xml, encoding="utf-8", xml_declaration=True)


def set_paragraph_style(paragraph: ET.Element, style_id: str) -> None:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        ppr = ET.Element(w_tag("pPr"))
        paragraph.insert(0, ppr)
    pstyle = ppr.find("w:pStyle", NS)
    if pstyle is None:
        pstyle = ET.Element(w_tag("pStyle"))
        ppr.insert(0, pstyle)
    pstyle.set(w_tag("val"), style_id)


def patch_template_paragraph_styles(document_xml: Path) -> None:
    tree = ET.parse(document_xml)
    root = tree.getroot()
    for paragraph in root.findall(".//w:p", NS):
        text = "".join(t.text or "" for t in paragraph.findall(".//w:t", NS)).strip()
        if text == "摘    要":
            set_paragraph_style(paragraph, "HDUAbstractTitle")
        elif text == "ABSTRACT":
            set_paragraph_style(paragraph, "HDUAbstractTitleEn")
        elif text == "目    录":
            set_paragraph_style(paragraph, "HDUTocTitle")
        elif text == "参考文献":
            set_paragraph_style(paragraph, "HDUReferenceTitle")
        elif text.startswith("关键词"):
            set_paragraph_style(paragraph, "HDUKeywords")
        elif text.startswith("Key words"):
            set_paragraph_style(paragraph, "HDUKeywords")
    tree.write(document_xml, encoding="utf-8", xml_declaration=True)


def patch_cover_table_layout(document_xml: Path) -> None:
    tree = ET.parse(document_xml)
    root = tree.getroot()
    tables = root.findall(".//w:tbl", NS)
    if not tables:
        tree.write(document_xml, encoding="utf-8", xml_declaration=True)
        return
    old_table = tables[0]
    rows = [
        ("题    目", "XXX(楷体小三号字)"),
        ("站点名称", "XXX(楷体小三号字)"),
        ("专    业", "XXX(楷体小三号字)"),
        ("班    级", "XXX(楷体小三号字)"),
        ("学    号", "XXX(楷体小三号字)"),
        ("学生姓名", "XXX(楷体小三号字)"),
        ("指导教师", "XXX(楷体小三号字)"),
        ("完成日期", "20××年5月"),
    ]

    paragraphs: list[ET.Element] = []
    for label, value in rows:
        p = ET.Element(w_tag("p"))
        p_pr = child(p, "pPr")
        child(p_pr, "jc", {"val": "center"})
        p_pr.append(spacing(before=90, after=90))
        run = child(p, "r")
        run.append(r_pr("楷体", "Times New Roman", 30))
        t = child(run, "t")
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = f"{label}：{value}"
        paragraphs.append(p)

    parent = None
    for candidate in root.iter():
        if old_table in list(candidate):
            parent = candidate
            break
    if parent is None:
        raise RuntimeError("failed to locate cover table parent")
    index = list(parent).index(old_table)
    for offset, paragraph in enumerate(paragraphs):
        parent.insert(index + offset, paragraph)
    parent.remove(old_table)
    tree.write(document_xml, encoding="utf-8", xml_declaration=True)


def build_template() -> None:
    if not SOURCE_DOCX.exists():
        raise FileNotFoundError(SOURCE_DOCX)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        with zipfile.ZipFile(SOURCE_DOCX) as zf:
            zf.extractall(tmp_dir)
        patch_styles(tmp_dir / "word" / "styles.xml")
        document_xml = tmp_dir / "word" / "document.xml"
        patch_sections(document_xml)
        patch_template_paragraph_styles(document_xml)
        patch_cover_table_layout(document_xml)
        patch_headers(tmp_dir)
        OUTPUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(OUTPUT_DOCX, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(tmp_dir.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(tmp_dir).as_posix())
    print(f"Built: {OUTPUT_DOCX}")


if __name__ == "__main__":
    build_template()
