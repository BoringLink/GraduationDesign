#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path("/Users/tk/Documents/杭州电子科技大学/毕业设计")
THESIS_DIR = ROOT / "latex" / "thesis"
BUILD_DIR = THESIS_DIR / "build"
TEMPLATE_DOC = ROOT / "理工类专业毕业论文模板（更新）.doc"
FORMATTED_TEMPLATE_DOCX = THESIS_DIR / "template" / "毕业论文模板-规范样式.docx"
CLEAN_TEMPLATE_DOCX = THESIS_DIR / "template" / "hdu-template.docx"
TEMPLATE_DOCX = BUILD_DIR / "template" / "hdu-template.docx"
CONTENT_DOCX = BUILD_DIR / "main-content.docx"
OUTPUT_DOCX = BUILD_DIR / "main.docx"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}

ET.register_namespace("w", NS["w"])
ET.register_namespace("r", NS["r"])


def parse_metadata() -> dict[str, str]:
    text = (THESIS_DIR / "metadata.tex").read_text(encoding="utf-8")
    values: dict[str, str] = {}
    for name, value in re.findall(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}", text):
        values[name] = value.strip()
    return values


def template_docx() -> Path | None:
    if FORMATTED_TEMPLATE_DOCX.exists():
        return FORMATTED_TEMPLATE_DOCX
    if CLEAN_TEMPLATE_DOCX.exists():
        return CLEAN_TEMPLATE_DOCX
    return None


def ensure_template_docx() -> None:
    TEMPLATE_DOCX.parent.mkdir(parents=True, exist_ok=True)
    source_docx = template_docx()
    if source_docx is not None:
        shutil.copy2(source_docx, TEMPLATE_DOCX)
        return
    subprocess.run(
        [
            "/usr/bin/textutil",
            "-convert",
            "docx",
            str(TEMPLATE_DOC),
            "-output",
            str(TEMPLATE_DOCX),
        ],
        check=True,
    )


def build_content_docx() -> None:
    resource_path = ":".join(
        [
            str(THESIS_DIR),
            str(THESIS_DIR / "chapters"),
            str(THESIS_DIR / "figures"),
            str(ROOT / "CodingPlatformBak" / "output" / "playwright" / "recapture"),
        ]
    )
    subprocess.run(
        [
            "pandoc",
            "--from=latex",
            "--to=docx",
            "--standalone",
            "--reference-doc",
            str(template_docx() or TEMPLATE_DOCX),
            "--resource-path",
            resource_path,
            "-o",
            str(CONTENT_DOCX),
            str(THESIS_DIR / "chapters" / "body.tex"),
            str(THESIS_DIR / "chapters" / "backmatter.tex"),
        ],
        check=True,
    )


def w_tag(tag: str) -> str:
    return f"{{{NS['w']}}}{tag}"


def r_tag(tag: str) -> str:
    return f"{{{NS['r']}}}{tag}"


def replace_paragraph_text(paragraph: ET.Element, text: str) -> None:
    runs = paragraph.findall("w:r", NS)
    if not runs:
        run = ET.SubElement(paragraph, w_tag("r"))
        text_node = ET.SubElement(run, w_tag("t"))
        text_node.text = text
        return
    first_run = runs[0]
    for extra in runs[1:]:
        paragraph.remove(extra)
    text_nodes = first_run.findall("w:t", NS)
    if not text_nodes:
        text_node = ET.SubElement(first_run, w_tag("t"))
    else:
        text_node = text_nodes[0]
        for extra in text_nodes[1:]:
            first_run.remove(extra)
    text_node.text = text


def clean_latex_text(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = text.replace(r"\&", "&")
    text = text.replace("``", "“").replace("''", "”")
    text = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:label|addcontentsline)\{[^{}]*\}(?:\{[^{}]*\})*", "", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", "", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_abstract_tex() -> dict[str, list[str] | str]:
    lines = (
        (THESIS_DIR / "chapters" / "abstract.tex")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    state: str | None = None
    result: dict[str, list[str] | str] = {
        "cn_paragraphs": [],
        "en_paragraphs": [],
        "cn_keywords": "",
        "en_keywords": "",
    }
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        if state not in {"cn", "en"} or not buffer:
            buffer = []
            return
        text = clean_latex_text(" ".join(buffer))
        if text:
            key = "cn_paragraphs" if state == "cn" else "en_paragraphs"
            items = result[key]
            assert isinstance(items, list)
            items.append(text)
        buffer = []

    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("%"):
            flush()
            continue
        if r"\chapter*{摘要}" in line:
            flush()
            state = "cn"
            continue
        if r"\chapter*{ABSTRACT}" in line:
            flush()
            state = "en"
            continue
        if r"\textbf{关键词}" in line:
            flush()
            result["cn_keywords"] = (
                clean_latex_text(line).replace("关键词：", "", 1).strip()
            )
            continue
        if r"\textbf{Key words}" in line:
            flush()
            result["en_keywords"] = (
                clean_latex_text(line).replace("Key words:", "", 1).strip()
            )
            continue
        if state in {"cn", "en"}:
            buffer.append(line)
    flush()
    return result


def replace_paragraph_placeholder(
    paragraph: ET.Element, placeholder: str, value: str
) -> None:
    for text_node in paragraph.findall(".//w:t", NS):
        if text_node.text and placeholder in text_node.text:
            text_node.text = text_node.text.replace(placeholder, value, 1)
            return
    replace_paragraph_text(paragraph, value)


def find_paragraph_by_pattern(paragraphs: list[ET.Element], pattern: str) -> ET.Element:
    regex = re.compile(pattern)
    for paragraph in paragraphs:
        text = "".join(t.text or "" for t in paragraph.findall(".//w:t", NS)).strip()
        if regex.search(text):
            return paragraph
    raise KeyError(pattern)


def make_toc_paragraph() -> ET.Element:
    p = ET.Element(w_tag("p"))
    p_pr = ET.SubElement(p, w_tag("pPr"))
    ET.SubElement(p_pr, w_tag("jc"), {w_tag("val"): "center"})

    r_begin = ET.SubElement(p, w_tag("r"))
    ET.SubElement(r_begin, w_tag("fldChar"), {w_tag("fldCharType"): "begin"})

    r_instr = ET.SubElement(p, w_tag("r"))
    instr = ET.SubElement(
        r_instr,
        w_tag("instrText"),
        {"{http://www.w3.org/XML/1998/namespace}space": "preserve"},
    )
    instr.text = ' TOC \\\\o "1-3" \\\\h \\\\z \\\\u '

    r_sep = ET.SubElement(p, w_tag("r"))
    ET.SubElement(r_sep, w_tag("fldChar"), {w_tag("fldCharType"): "separate"})

    r_hint = ET.SubElement(p, w_tag("r"))
    t = ET.SubElement(r_hint, w_tag("t"))
    t.text = "目录将在 Word 中打开后自动更新"

    r_end = ET.SubElement(p, w_tag("r"))
    ET.SubElement(r_end, w_tag("fldChar"), {w_tag("fldCharType"): "end"})
    return p


def make_page_break_paragraph() -> ET.Element:
    p = ET.Element(w_tag("p"))
    r = ET.SubElement(p, w_tag("r"))
    ET.SubElement(r, w_tag("br"), {w_tag("type"): "page"})
    return p


def make_text_paragraph(text: str, style_id: str) -> ET.Element:
    p = ET.Element(w_tag("p"))
    p_pr = ET.SubElement(p, w_tag("pPr"))
    ET.SubElement(p_pr, w_tag("pStyle"), {w_tag("val"): style_id})
    r = ET.SubElement(p, w_tag("r"))
    t = ET.SubElement(r, w_tag("t"))
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t.text = text
    return p


def set_update_fields(settings_path: Path) -> None:
    if settings_path.exists():
        tree = ET.parse(settings_path)
        root = tree.getroot()
    else:
        root = ET.Element(w_tag("settings"))
        tree = ET.ElementTree(root)
    if root.find("w:updateFields", NS) is None:
        root.append(ET.Element(w_tag("updateFields"), {w_tag("val"): "true"}))
    tree.write(settings_path, encoding="utf-8", xml_declaration=True)


def set_paragraph_style(paragraph: ET.Element, style_id: str) -> None:
    p_pr = paragraph.find("w:pPr", NS)
    if p_pr is None:
        p_pr = ET.Element(w_tag("pPr"))
        paragraph.insert(0, p_pr)
    p_style = p_pr.find("w:pStyle", NS)
    if p_style is None:
        p_style = ET.Element(w_tag("pStyle"))
        p_pr.insert(0, p_style)
    p_style.set(w_tag("val"), style_id)


def normalize_content_docx_styles() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        with zipfile.ZipFile(CONTENT_DOCX) as zf:
            zf.extractall(tmp_dir)

        document_xml = tmp_dir / "word" / "document.xml"
        tree = ET.parse(document_xml)
        root = tree.getroot()
        in_references = False
        for paragraph in root.findall(".//w:p", NS):
            text = "".join(
                t.text or "" for t in paragraph.findall(".//w:t", NS)
            ).strip()
            p_style = paragraph.find("w:pPr/w:pStyle", NS)
            style_id = p_style.get(w_tag("val")) if p_style is not None else ""
            if not text:
                continue
            if text == "摘要":
                set_paragraph_style(paragraph, "HDUAbstractTitle")
            elif text == "ABSTRACT":
                set_paragraph_style(paragraph, "HDUAbstractTitleEn")
            elif text.startswith("关键词"):
                set_paragraph_style(paragraph, "HDUKeywords")
            elif text.startswith("Key words"):
                set_paragraph_style(paragraph, "HDUKeywords")
            elif text == "参考文献":
                in_references = True
                set_paragraph_style(paragraph, "HDUReferenceTitle")
            elif in_references and re.match(r"^\[\d+\]", text):
                set_paragraph_style(paragraph, "HDUReferenceItem")
            elif re.match(r"^图\s*\d+[-.]\d+", text):
                set_paragraph_style(paragraph, "HDUFigureCaption")
            elif re.match(r"^表\s*\d+[-.]\d+", text):
                set_paragraph_style(paragraph, "HDUTableCaption")
            elif style_id == "Heading4":
                set_paragraph_style(paragraph, "3")
            elif style_id == "FirstParagraph":
                set_paragraph_style(paragraph, "aa")
            elif style_id == "":
                set_paragraph_style(paragraph, "aa")
        tree.write(document_xml, encoding="utf-8", xml_declaration=True)

        with zipfile.ZipFile(CONTENT_DOCX, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(tmp_dir.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(tmp_dir).as_posix())


def merge_content_types(target_path: Path, source_path: Path) -> None:
    ct_ns = {"ct": "http://schemas.openxmlformats.org/package/2006/content-types"}
    ET.register_namespace("", ct_ns["ct"])
    target_tree = ET.parse(target_path)
    source_tree = ET.parse(source_path)
    target_root = target_tree.getroot()
    source_root = source_tree.getroot()

    existing_defaults = {
        item.attrib["Extension"]
        for item in target_root.findall("ct:Default", ct_ns)
        if "Extension" in item.attrib
    }
    for item in source_root.findall("ct:Default", ct_ns):
        extension = item.attrib.get("Extension")
        if extension and extension not in existing_defaults:
            target_root.append(item)
            existing_defaults.add(extension)

    existing_overrides = {
        item.attrib["PartName"]
        for item in target_root.findall("ct:Override", ct_ns)
        if "PartName" in item.attrib
    }
    for item in source_root.findall("ct:Override", ct_ns):
        part_name = item.attrib.get("PartName")
        if (
            part_name
            and part_name.startswith("/word/media/")
            and part_name not in existing_overrides
        ):
            target_root.append(item)
            existing_overrides.add(part_name)

    target_tree.write(target_path, encoding="utf-8", xml_declaration=True)


def merge_content_docx_parts(tmp_dir: Path, content_dir: Path) -> list[ET.Element]:
    target_word = tmp_dir / "word"
    content_word = content_dir / "word"

    for name in ["styles.xml", "numbering.xml", "fontTable.xml"]:
        source = content_word / name
        if source.exists():
            shutil.copy2(source, target_word / name)

    source_media = content_word / "media"
    if source_media.exists():
        target_media = target_word / "media"
        target_media.mkdir(exist_ok=True)
        for source in source_media.iterdir():
            if source.is_file():
                shutil.copy2(source, target_media / source.name)

    target_rels = target_word / "_rels" / "document.xml.rels"
    source_rels = content_word / "_rels" / "document.xml.rels"
    if source_rels.exists():
        target_tree = ET.parse(target_rels)
        source_tree = ET.parse(source_rels)
        target_root = target_tree.getroot()
        existing_ids = {
            item.attrib.get("Id") for item in target_root.findall("pr:Relationship", NS)
        }
        for rel in source_tree.getroot().findall("pr:Relationship", NS):
            rel_type = rel.attrib.get("Type", "")
            if not (rel_type.endswith("/image") or rel_type.endswith("/hyperlink")):
                continue
            rel_id = rel.attrib.get("Id")
            if rel_id and rel_id not in existing_ids:
                target_root.append(rel)
                existing_ids.add(rel_id)
        target_tree.write(target_rels, encoding="utf-8", xml_declaration=True)

    merge_content_types(
        tmp_dir / "[Content_Types].xml", content_dir / "[Content_Types].xml"
    )

    content_tree = ET.parse(content_word / "document.xml")
    content_body = content_tree.getroot().find("w:body", NS)
    if content_body is None:
        raise RuntimeError("content document.xml missing body")
    return [child for child in list(content_body) if child.tag != w_tag("sectPr")]


def patch_template(metadata: dict[str, str]) -> None:
    abstract = parse_abstract_tex()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        with zipfile.ZipFile(TEMPLATE_DOCX) as zf:
            zf.extractall(tmp_dir)
        content_dir = tmp_dir / "_content"
        with zipfile.ZipFile(CONTENT_DOCX) as zf:
            zf.extractall(content_dir)
        content_children = merge_content_docx_parts(tmp_dir, content_dir)

        document_xml = tmp_dir / "word" / "document.xml"
        settings_xml = tmp_dir / "word" / "settings.xml"

        tree = ET.parse(document_xml)
        root = tree.getroot()
        body = root.find("w:body", NS)
        if body is None:
            raise RuntimeError("template document.xml missing body")

        paragraphs = root.findall(".//w:p", NS)
        text_to_para: dict[str, ET.Element] = {}
        for p in paragraphs:
            text = "".join(t.text or "" for t in p.findall(".//w:t", NS)).strip()
            if text:
                text_to_para.setdefault(text, p)

        year_match = re.search(r"\d{4}", metadata["ThesisDate"])
        if year_match is None:
            raise RuntimeError(
                f"failed to extract year from ThesisDate: {metadata['ThesisDate']}"
            )

        replacements = {
            "XXX(楷体小三号字)": [
                metadata["ThesisTitleCn"],
                metadata["ThesisSite"],
                metadata["ThesisMajor"],
                metadata["ThesisClass"],
                metadata["ThesisStudentId"],
                metadata["ThesisAuthor"],
                metadata["ThesisAdvisor"],
            ],
            "20××年5月": [metadata["ThesisDate"]],
            "（20××届）": [f"（{year_match.group(0)}届）"],
        }

        placeholder_paras = []
        for p in paragraphs:
            text = "".join(t.text or "" for t in p.findall(".//w:t", NS)).strip()
            if "XXX(楷体小三号字)" in text:
                placeholder_paras.append(p)
        if len(placeholder_paras) < 7:
            raise RuntimeError("template placeholders not found as expected")
        for para, value in zip(
            placeholder_paras[:7], replacements["XXX(楷体小三号字)"], strict=True
        ):
            replace_paragraph_placeholder(para, "XXX(楷体小三号字)", value)

        replace_paragraph_placeholder(
            find_paragraph_by_pattern(paragraphs, r"20[×xX＊*]{2}年5月"),
            "20××年5月",
            replacements["20××年5月"][0],
        )
        replace_paragraph_text(
            find_paragraph_by_pattern(paragraphs, r"（(?:20[×xX＊*]{2}|\d{4})届）"),
            replacements["（20××届）"][0],
        )

        commitment = text_to_para[
            "我谨在此承诺：本人所写的毕业论文《XXXXXXXX》均系本人独立完成，没有抄袭行为，凡涉及其他作者的观点和材料，均作了注释，若有不实，后果由本人承担。"
        ]
        replace_paragraph_text(
            commitment,
            f"我谨在此承诺：本人所写的毕业论文《{metadata['ThesisTitleCn']}》均系本人独立完成，没有抄袭行为，凡涉及其他作者的观点和材料，均作了注释，若有不实，后果由本人承担。",
        )

        children = list(body)
        cn_title = text_to_para["摘    要"]
        cn_keywords = text_to_para["关键词："]
        en_title = text_to_para["ABSTRACT"]
        en_keywords = text_to_para["Key words："]
        cn_title_index = children.index(cn_title)
        cn_keywords_index = children.index(cn_keywords)
        en_title_index = children.index(en_title)
        en_keywords_index = children.index(en_keywords)

        for child in children[cn_title_index + 1 : cn_keywords_index]:
            if child in body:
                body.remove(child)
        for child in children[en_title_index + 1 : en_keywords_index]:
            if child in body:
                body.remove(child)

        insert_at = list(body).index(cn_title) + 1
        for offset, text in enumerate(abstract["cn_paragraphs"]):
            body.insert(
                insert_at + offset, make_text_paragraph(str(text), "HDUAbstractText")
            )
        replace_paragraph_text(cn_keywords, f"关键词：{abstract['cn_keywords']}")
        set_paragraph_style(cn_keywords, "HDUKeywords")

        insert_at = list(body).index(en_title) + 1
        for offset, text in enumerate(abstract["en_paragraphs"]):
            body.insert(
                insert_at + offset, make_text_paragraph(str(text), "HDUAbstractTextEn")
            )
        replace_paragraph_text(en_keywords, f"Key words: {abstract['en_keywords']}")
        set_paragraph_style(en_keywords, "HDUKeywords")

        toc_heading = text_to_para["目    录"]
        children = list(body)
        toc_index = children.index(toc_heading)
        sect_pr = body.find("w:sectPr", NS)
        if sect_pr is not None:
            body.remove(sect_pr)
        for child in children[toc_index + 1 :]:
            if child in body:
                body.remove(child)

        body.insert(toc_index + 1, make_toc_paragraph())
        body.insert(toc_index + 2, make_page_break_paragraph())
        insert_at = toc_index + 3
        for offset, child in enumerate(content_children):
            body.insert(insert_at + offset, child)
        if sect_pr is not None:
            body.append(sect_pr)

        tree.write(document_xml, encoding="utf-8", xml_declaration=True)
        set_update_fields(settings_xml)

        with zipfile.ZipFile(OUTPUT_DOCX, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(tmp_dir.rglob("*")):
                if path.is_file() and "_content" not in path.parts:
                    zf.write(path, path.relative_to(tmp_dir).as_posix())


def main() -> None:
    metadata = parse_metadata()
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    ensure_template_docx()
    build_content_docx()
    normalize_content_docx_styles()
    patch_template(metadata)
    print(f"Built template-aligned DOCX: {OUTPUT_DOCX}")


if __name__ == "__main__":
    main()
