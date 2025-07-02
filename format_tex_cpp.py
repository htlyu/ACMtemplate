#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键式格式化LaTeX文件中的C++代码块
专门用于格式化Algorithm-template.tex中的minted C++代码
"""

import re
import os
import sys
import argparse

def format_cpp_code(code_block):
    """专门格式化C++代码"""
    lines = code_block.split('\n')
    formatted_lines = []
    
    cpp_rules = [
        # 移除行尾空格
        (r'\s+$', ''),
        # { 前加空格
        (r'(\w)\{', r'\1 {'),
        # 逗号后加空格
        (r',(\S)', r', \1'),
        # 运算符前后加空格
        (r'(\w)([\+\-\*/%]|==|!=|<=|>=|&&|\|\||<<|>>)(\w)', r'\1 \2 \3'),
        (r'(\w)(=)([^=])', r'\1 \2 \3'),
        (r'([^=<>!])(=)(\w)', r'\1\2 \3'),
        # if/for/while后加空格
        (r'\b(if|for|while|switch)\(', r'\1 ('),
        # else前后加空格
        (r'}else', r'} else'),
        (r'else{', r'else {'),
        # 括号内侧空格处理
        (r'\(\s+', '('),
        (r'\s+\)', ')'),
        # 分号后空格
        (r';(\S)', r'; \1'),
    ]
    
    for line in lines:
        # 保持原始缩进
        indent_match = re.match(r'^(\s*)', line)
        indent = indent_match.group(1) if indent_match else ''
        content = line.strip()
        
        if not content:
            formatted_lines.append('')
            continue
        
        # 应用C++格式化规则
        for pattern, replacement in cpp_rules:
            content = re.sub(pattern, replacement, content)
        
        formatted_lines.append(indent + content)
    
    return '\n'.join(formatted_lines)

def format_latex_cpp_blocks(content):
    """格式化LaTeX文件中的C++代码块"""
    def format_minted_block(match):
        language = match.group(1)
        code_content = match.group(2)
        
        # 只格式化C++相关的代码块
        if language.lower() in ['cpp', 'c++', 'cc', 'cxx', 'c']:
            formatted_code = format_cpp_code(code_content)
            return f'\\begin{{minted}}{{{language}}}\n{formatted_code}\n\\end{{minted}}'
        else:
            # 其他语言不处理
            return match.group(0)
    
    # 处理minted代码块
    pattern = r'\\begin\{minted\}\{([^}]+)\}\n(.*?)\n\\end\{minted\}'
    result = re.sub(pattern, format_minted_block, content, flags=re.DOTALL)
    
    return result

def main():
    parser = argparse.ArgumentParser(description='一键式格式化LaTeX文件中的C++代码块')
    parser.add_argument('file', nargs='?', default='Algorithm-template.tex', 
                       help='要格式化的LaTeX文件 (默认: Algorithm-template.tex)')
    parser.add_argument('--backup', action='store_true', 
                       help='创建备份文件')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"错误: 文件 {args.file} 不存在")
        sys.exit(1)
    
    try:
        # 读取文件
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"正在格式化 {args.file} 中的C++代码块...")
        
        # 创建备份
        if args.backup:
            backup_file = args.file + '.backup'
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已创建备份文件: {backup_file}")
        
        # 格式化C++代码块
        formatted_content = format_latex_cpp_blocks(content)
        
        # 写入格式化后的内容
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        print(f"✅ 格式化完成: {args.file}")
        print("所有C++代码块已按统一风格格式化")
        
    except Exception as e:
        print(f"❌ 格式化失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()