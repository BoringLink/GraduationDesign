#!/usr/bin/env python3
"""
修复论文中图片的环绕方式为以上下型
"""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import zipfile
import os

def set_image_wrapping_above_bottom(paragraph):
    """设置段落中图片的环绕方式为以上下型"""
    # 找到段落中的所有图片
    for run in paragraph.runs:
        # 检查run中是否有图片
        if 'drawing' in run._element.xml:
            # 获取图片的XML元素
            drawing_element = run._element.find(qn('w:drawing'))
            if drawing_element is not None:
                # 查找或创建包装格式元素
                wrap_none = drawing_element.find(qn('w:wrapNone'))
                wrap_square = drawing_element.find(qn('w:wrapSquare'))
                wrap_tight = drawing_element.find(qn('w:wrapTight'))
                wrap_through = drawing_element.find(qn('w:wrapThrough'))
                wrap_top_and_bottom = drawing_element.find(qn('w:wrapTopAndBottom'))
                wrap_behind = drawing_element.find(qn('w:wrapBehind'))
                wrap_in_front = drawing_element.find(qn('w:wrapInFront'))
                
                # 如果没有找到以上下型环绕，则创建它
                if wrap_top_and_bottom is None:
                    # 删除其他环绕方式
                    for elem in [wrap_none, wrap_square, wrap_tight, wrap_through, wrap_behind, wrap_in_front]:
                        if elem is not None:
                            drawing_element.remove(elem)
                    
                    # 创建以上下型环绕元素
                    wrap_top_and_bottom = OxmlElement('w:wrapTopAndBottom')
                    wrap_top_and_bottom.set(qn('w:distT'), '0')
                    wrap_top_and_bottom.set(qn('w:distB'), '0')
                    wrap_top_and_bottom.set(qn('w:distL'), '0')
                    wrap_top_and_bottom.set(qn('w:distR'), '0')
                    drawing_element.append(wrap_top_and_bottom)

def main():
    # 文档路径
    doc_path = "/Users/tk/Documents/杭州电子科技大学/毕业设计/论文重写版.docx"
    
    # 打开文档
    doc = Document(doc_path)
    
    # 处理所有段落
    for paragraph in doc.paragraphs:
        set_image_wrapping_above_bottom(paragraph)
    
    # 处理表格中的段落
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    set_image_wrapping_above_bottom(paragraph)
    
    # 保存文档
    doc.save(doc_path)
    print(f"已更新图片环绕方式: {doc_path}")

if __name__ == "__main__":
    main()
