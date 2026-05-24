#!/usr/bin/env python3
"""
修复论文中的表格，保留并正确格式化
"""
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
import copy

def clone_table(source_table):
    """克隆一个表格"""
    # 创建一个新的表格元素
    new_tbl = copy.deepcopy(source_table._element)
    return new_tbl

def main():
    # 文档路径
    original_path = "/Users/tk/Documents/杭州电子科技大学/毕业设计/论文正式版.docx"
    rewrite_path = "/Users/tk/Documents/杭州电子科技大学/毕业设计/论文重写版.docx"
    
    # 打开文档
    original_doc = Document(original_path)
    rewrite_doc = Document(rewrite_path)
    
    # 获取原始文档的表格
    original_tables = original_doc.tables
    
    # 清除重写文档中的所有表格
    # 从后往前删除，避免索引变化
    for i in range(len(rewrite_doc.tables) - 1, -1, -1):
        tbl = rewrite_doc.tables[i]
        tbl._element.getparent().remove(tbl._element)
    
    # 将原始文档的表格复制到重写文档中
    for table in original_tables:
        new_tbl = clone_table(table)
        rewrite_doc.element.body.append(new_tbl)
    
    # 保存文档
    rewrite_doc.save(rewrite_path)
    print(f"已修复表格: {rewrite_path}")
    print(f"原始表格数量: {len(original_tables)}")
    print(f"修复后表格数量: {len(rewrite_doc.tables)}")

if __name__ == "__main__":
    main()
