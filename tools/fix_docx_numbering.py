from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import tempfile

from lxml import etree


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def qn(tag: str) -> str:
    return f"{{{W}}}{tag}"


def para_text(p):
    return "".join(p.xpath(".//w:t/text()", namespaces=NS)).strip()


def set_para_text(p, text: str):
    texts = p.xpath(".//w:t", namespaces=NS)
    if not texts:
        r = etree.SubElement(p, qn("r"))
        t = etree.SubElement(r, qn("t"))
        t.text = text
        return
    texts[0].text = text
    for t in texts[1:]:
        t.text = ""


def set_style(p, style: str):
    ppr = p.find(qn("pPr"))
    if ppr is None:
        ppr = etree.Element(qn("pPr"))
        p.insert(0, ppr)
    pstyle = ppr.find(qn("pStyle"))
    if pstyle is None:
        pstyle = etree.Element(qn("pStyle"))
        ppr.insert(0, pstyle)
    pstyle.set(qn("val"), style)


def remove_toc_bookmarks(p):
    for el in list(p.xpath(".//w:bookmarkStart[starts-with(@w:name, '_Toc')]", namespaces=NS)):
        bid = el.get(qn("id"))
        parent = el.getparent()
        parent.remove(el)
        for end in list(p.xpath(f".//w:bookmarkEnd[@w:id='{bid}']", namespaces=NS)):
            end.getparent().remove(end)


def add_toc_bookmark(p, name: str, bid: str):
    first_r = p.find(qn("r"))
    if first_r is None:
        first_r = etree.SubElement(p, qn("r"))
    start = etree.Element(qn("bookmarkStart"))
    start.set(qn("id"), bid)
    start.set(qn("name"), name)
    p.insert(p.index(first_r), start)
    end = etree.Element(qn("bookmarkEnd"))
    end.set(qn("id"), bid)
    p.insert(p.index(first_r) + 1, end)


def visible_text_nodes(p):
    return p.xpath(".//w:t", namespaces=NS)


def replace_visible_prefix(p, old: str, new: str):
    text = para_text(p)
    if not text.startswith(old):
        return False
    set_para_text(p, new + text[len(old):])
    return True


def main():
    src = Path("论文正式版.docx")
    backup = Path("论文正式版.docx.bak-numbering")
    if not backup.exists():
        shutil.copy2(src, backup)

    with ZipFile(src, "r") as zin:
        files = {name: zin.read(name) for name in zin.namelist()}

    doc = etree.fromstring(files["word/document.xml"])
    body = doc.find(".//w:body", namespaces=NS)
    paras = body.findall(qn("p"))

    # Locate the start of the detailed-design block that was accidentally kept
    # under chapter 4.
    database_para = next(p for p in paras if para_text(p) == "4.3  数据库设计")
    system_impl_para = next(p for p in paras if para_text(p) == "5  系统实现")

    # Insert the missing chapter heading before 5.1.
    detail_heading = deepcopy(system_impl_para)
    remove_toc_bookmarks(detail_heading)
    set_style(detail_heading, "1")
    set_para_text(detail_heading, "5  系统详细设计")
    add_toc_bookmark(detail_heading, "_Toc229484221", "1201")
    body.insert(body.index(database_para), detail_heading)

    # Fix body headings from chapter 5 onward.
    replacements = {
        "4  系统设计": "4  系统总体设计",
        "4.3  数据库设计": "5.1  数据库设计",
        "5  系统实现": "6  软件实现",
        "5.1  用户认证与权限控制实现": "6.1  用户认证与权限控制实现",
        "6.2  课程与知识点管理功能实现": "6.2  课程与知识点管理功能实现",
        "6.3  在线编程与代码运行功能实现": "6.3  在线编程与代码运行功能实现",
        "6.4  大模型辅助教学功能实现": "6.4  大模型辅助教学功能实现",
        "6.4.1  自由问答功能实现": "6.4.1  自由问答功能实现",
        "6.4.2  代码解释功能实现": "6.4.2  代码解释功能实现",
        "6.4.3  报错解析功能实现": "6.4.3  报错解析功能实现",
        "6.4.4  问题分解功能实现": "6.4.4  问题分解功能实现",
        "6.4.5  抽象建模功能实现": "6.4.5  抽象建模功能实现",
        "6.4.6  算法设计引导功能实现": "6.4.6  算法设计引导功能实现",
        "6.5  师生互动与消息功能实现": "6.5  师生互动与消息功能实现",
        "6.6  教学资源管理功能实现": "6.6  教学资源管理功能实现",
        "6.7  学习行为记录与事件追踪功能实现": "6.7  学习行为记录与事件追踪功能实现",
        "6.8  系统界面展示": "6.8  系统界面展示",
        "6.8.1  登录界面": "6.8.1  登录界面",
        "6.8.2  学生资源页仪表板": "6.8.2  学生资源页仪表板",
        "6.8.3  教师资源页仪表板": "6.8.3  教师资源页仪表板",
        "6.8.4  教师资源管理页面": "6.8.4  教师资源管理页面",
        "6  系统测试与调试": "7  系统测试与调试",
        "7  结论": "8  结论",
    }

    # Prefix fixes for chapter 7 subheadings and implementation subheadings.
    prefix_replacements = [
        ("5.1.1  ", "5.1.1  "),
        ("5.1.2  ", "5.1.2  "),
        ("7.1  ", "7.1  "),
        ("7.2  ", "7.2  "),
        ("7.3  ", "7.3  "),
        ("7.4  ", "7.4  "),
        ("7.5  ", "7.5  "),
        ("7.6  ", "7.6  "),
    ]

    for p in body.findall(qn("p")):
        text = para_text(p)
        if text in replacements:
            set_para_text(p, replacements[text])
        for old, new in prefix_replacements:
            replace_visible_prefix(p, old, new)

    # Re-add the missing TOC bookmark for the database section.
    add_toc_bookmark(database_para, "_Toc229484222", "1202")

    # Update the static TOC display text that Word shows before field refresh.
    toc_replacements = {
        "4  系统总体设计12": "4  系统总体设计12",
        "7  结论33": "8  结论33",
    }
    for p in body.findall(qn("p")):
        text = para_text(p)
        if text in toc_replacements:
            set_para_text(p, toc_replacements[text])

    files["word/document.xml"] = etree.tostring(
        doc, xml_declaration=True, encoding="UTF-8", standalone="yes"
    )

    tmp = Path(tempfile.mkstemp(suffix=".docx", dir="/private/tmp")[1])
    with ZipFile(tmp, "w", ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)
    shutil.move(tmp, src)
    print(f"fixed {src}; backup: {backup}")


if __name__ == "__main__":
    main()
