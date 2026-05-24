#!/usr/bin/env python3
"""
验证输出文件：段落长度、格式、图片位置
"""
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
import zipfile
import os

def main():
    # 文档路径
    doc_path = "/Users/tk/Documents/杭州电子科技大学/毕业设计/论文重写版.docx"
    
    # 打开文档
    doc = docx.Document(doc_path)
    
    print("=== 论文重写版.docx 验证报告 ===")
    print(f"文件路径: {doc_path}")
    print(f"文件大小: {os.path.getsize(doc_path) / 1024 / 1024:.2f} MB")
    print()
    
    # 1. 段落统计
    print("1. 段落统计:")
    total_paragraphs = len(doc.paragraphs)
    print(f"   总段落数: {total_paragraphs}")
    
    # 按样式统计段落
    style_counts = {}
    normal_body_count = 0
    short_normal_body_count = 0
    short_normal_body_lengths = []
    
    for p in doc.paragraphs:
        if p.style and p.style.name:
            style_name = p.style.name
            style_counts[style_name] = style_counts.get(style_name, 0) + 1
            
            # 只统计Normal和Body Text样式的段落
            if style_name in ['Normal', 'Body Text']:
                normal_body_count += 1
                text_length = len(p.text.strip())
                if text_length < 150:
                    short_normal_body_count += 1
                    short_normal_body_lengths.append(text_length)
    
    print(f"   Normal+Body Text段落数: {normal_body_count}")
    print(f"   短Normal+Body Text段落数 (<150字符): {short_normal_body_count}")
    if short_normal_body_lengths:
        print(f"   短段落长度范围: {min(short_normal_body_lengths)} - {max(short_normal_body_lengths)}")
        print(f"   平均短段落长度: {sum(short_normal_body_lengths)/len(short_normal_body_lengths):.1f}")
    
    print("   样式分布:")
    for style, count in sorted(style_counts.items()):
        print(f"     {style}: {count}")
    print()
    
    # 2. 表格统计
    print("2. 表格统计:")
    total_tables = len(doc.tables)
    print(f"   总表格数: {total_tables}")
    for i, table in enumerate(doc.tables):
        print(f"   表格 {i+1}: {len(table.rows)} 行 x {len(table.columns)} 列")
    print()
    
    # 3. 图片统计
    print("3. 图片统计:")
    try:
        image_count = 0
        with zipfile.ZipFile(doc_path, 'r') as docx_zip:
            file_list = docx_zip.namelist()
            image_files = [f for f in file_list if f.startswith('word/media/') and 
                          any(f.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.emf', '.wmf'])]
            image_count = len(image_files)
            print(f"   图片数量: {image_count}")
            if image_files:
                print("   图片列表:")
                for img in sorted(image_files):
                    print(f"     {img}")
    except Exception as e:
        print(f"   图片统计错误: {e}")
    print()
    
    # 4. 页面设置验证（基于模板）
    print("4. 页面设置验证:")
    try:
        section = doc.sections[0]
        print(f"   页面宽度: {section.page_width}")
        print(f"   页面高度: {section.page_height}")
        print(f"   左边距: {section.left_margin}")
        print(f"   右边距: {section.right_margin}")
        print(f"   上边距: {section.top_margin}")
        print(f"   下边距: {section.bottom_margin}")
        print(f"   页眉距离: {section.header_distance}")
        print(f"   页脚距离: {section.footer_distance}")
    except Exception as e:
        print(f"   页面设置验证错误: {e}")
    print()
    
    # 5. 与原始论文对比
    print("5. 与原始论文对比:")
    original_path = "/Users/tk/Documents/杭州电子科技大学/毕业设计/论文正式版.docx"
    if os.path.exists(original_path):
        try:
            original_doc = docx.Document(original_path)
            print(f"   原始论文总段落数: {len(original_doc.paragraphs)}")
            print(f"   重写论文总段落数: {len(doc.paragraphs)}")
            print(f"   原始论文总表格数: {len(original_doc.tables)}")
            print(f"   重写论文总表格数: {len(doc.tables)}")
            
            # 原始论文图片数量
            original_image_count = 0
            with zipfile.ZipFile(original_path, 'r') as docx_zip:
                file_list = docx_zip.namelist()
                original_image_files = [f for f in file_list if f.startswith('word/media/') and 
                                      any(f.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.emf', '.wmf'])]
                original_image_count = len(original_image_files)
            print(f"   原始论文图片数量: {original_image_count}")
            print(f"   重写论文图片数量: {image_count}")
        except Exception as e:
            print(f"   对比验证错误: {e}")
    else:
        print(f"   原始论文文件不存在: {original_path}")
    print()
    
    print("=== 验证完成 ===")

if __name__ == "__main__":
    main()
