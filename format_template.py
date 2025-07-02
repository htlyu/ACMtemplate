#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX ACM模板格式化脚本
用于统一LaTeX模板的格式，便于添加新模板时保持一致性
作者: Assistant
"""

import re
import argparse
import sys
import os

class LatexTemplateFormatter:
    def __init__(self):
        # 数学符号统一规则
        self.math_symbol_rules = [
            (r'\\le(?!qslant)', r'\\leqslant'),      # \le -> \leqslant
            (r'\\leq(?!slant)', r'\\leqslant'),      # \leq -> \leqslant  
            (r'\\ge(?!qslant)', r'\\geqslant'),      # \ge -> \geqslant
            (r'\\geq(?!slant)', r'\\geqslant'),      # \geq -> \geqslant
            (r'\\ne(?!q)', r'\\neq'),                # \ne -> \neq
            (r'\\wedge(?!q)', r'\\land'),            # \wedge -> \land
        ]
        
        # 代码块格式化规则
        self.code_formatting_rules = [
            # 统一缩进为4空格
            (r'^(\s*)([^\s])', lambda m: '    ' * (len(m.group(1)) // 4) + m.group(2)),
            # 移除行尾空格
            (r'\s+$', ''),
        ]
    
    def format_math_symbols(self, content: str) -> str:
        """统一数学符号格式"""
        result = content
        for pattern, replacement in self.math_symbol_rules:
            result = re.sub(pattern, replacement, result)
        return result
    
    def format_cpp_code(self, code_block: str) -> str:
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
            # 运算符前后加空格 (更精确的匹配)
            (r'(\w)([\+\-\*/%]|==|!=|<=|>=|&&|\|\||<<|>>)(\w)', r'\1 \2 \3'),
            (r'(\w)(=)([^=])', r'\1 \2 \3'),
            (r'([^=<>!])(=)(\w)', r'\1\2 \3'),
            # if/for/while后加空格
            (r'\b(if|for|while|switch)\(', r'\1 ('),
            # else前后加空格
            (r'}else', r'} else'),
            (r'else{', r'else {'),
            # 括号内侧不要空格
            (r'\(\s+', '('),
            (r'\s+\)', ')'),
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
                if callable(replacement):
                    content = re.sub(pattern, replacement, content)
                else:
                    content = re.sub(pattern, replacement, content)
            
            formatted_lines.append(indent + content)
        
        return '\n'.join(formatted_lines)
    
    def format_code_block(self, code_block: str, language: str = '') -> str:
        """格式化代码块内容"""
        # 如果是C++代码，使用专门的格式化
        if language.lower() in ['cpp', 'c++', 'cc', 'cxx']:
            return self.format_cpp_code(code_block)
        
        # 其他语言使用通用格式化
        lines = code_block.split('\n')
        formatted_lines = []
        
        for line in lines:
            # 应用代码格式化规则
            for pattern, replacement in self.code_formatting_rules:
                if callable(replacement):
                    line = re.sub(pattern, replacement, line)
                else:
                    line = re.sub(pattern, replacement, line)
            formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def extract_and_format_code_blocks(self, content: str) -> str:
        """提取并格式化所有代码块"""
        def format_minted_block(match):
            language = match.group(1)
            code_content = match.group(2)
            formatted_code = self.format_code_block(code_content, language)
            return f'\\begin{{minted}}{{{language}}}\n{formatted_code}\n\\end{{minted}}'
        
        # 处理minted代码块
        pattern = r'\\begin\{minted\}\{([^}]+)\}\n(.*?)\n\\end\{minted\}'
        result = re.sub(pattern, format_minted_block, content, flags=re.DOTALL)
        
        return result
    
    def add_complexity_comments(self, content: str, time_complexity: str = None, space_complexity: str = None) -> str:
        """为代码块添加复杂度注释"""
        if not time_complexity and not space_complexity:
            return content
        
        comments = []
        if time_complexity:
            comments.append(f"% 时间复杂度：{time_complexity}")
        if space_complexity:
            comments.append(f"% 空间复杂度：{space_complexity}")
        
        comment_block = '\n'.join(comments)
        
        # 在每个subsection或subsubsection后添加复杂度注释
        def add_comment(match):
            section_line = match.group(0)
            return f"{section_line}\n\n{comment_block}"
        
        pattern = r'\\(sub)*subsection\{[^}]+\}'
        result = re.sub(pattern, add_comment, content)
        
        return result
    
    def format_section_structure(self, content: str) -> str:
        """格式化章节结构"""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # 确保章节标题前后有适当的空行
            if re.match(r'\\(sub)*section\{', line.strip()):
                if formatted_lines and formatted_lines[-1].strip():
                    formatted_lines.append('')  # 添加空行
                formatted_lines.append(line)
                formatted_lines.append('')  # 章节后添加空行
            else:
                formatted_lines.append(line)
        
        # 移除多余的连续空行
        result_lines = []
        prev_empty = False
        for line in formatted_lines:
            if line.strip() == '':
                if not prev_empty:
                    result_lines.append(line)
                prev_empty = True
            else:
                result_lines.append(line)
                prev_empty = False
        
        return '\n'.join(result_lines)
    
    def create_template_snippet(self, title: str, code: str, time_complexity: str = None, 
                              space_complexity: str = None, language: str = "cpp") -> str:
        """创建标准的模板片段"""
        snippet_parts = []
        
        # 添加标题
        snippet_parts.append(f"\\subsubsection{{{title}}}")
        snippet_parts.append("")
        
        # 添加复杂度注释
        if time_complexity:
            snippet_parts.append(f"% 时间复杂度：{time_complexity}")
        if space_complexity:
            snippet_parts.append(f"% 空间复杂度：{space_complexity}")
        if time_complexity or space_complexity:
            snippet_parts.append("")
        
        # 添加代码块
        formatted_code = self.format_code_block(code, language)
        snippet_parts.append(f"\\begin{{minted}}{{{language}}}")
        snippet_parts.append(formatted_code)
        snippet_parts.append("\\end{minted}")
        snippet_parts.append("")
        
        return '\n'.join(snippet_parts)
    
    def format_file(self, filepath: str, output_filepath: str = None) -> None:
        """格式化整个LaTeX文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"正在格式化文件: {filepath}")
            
            # 应用各种格式化规则
            content = self.format_math_symbols(content)
            content = self.extract_and_format_code_blocks(content)
            content = self.format_section_structure(content)
            
            # 确定输出文件路径
            if output_filepath is None:
                # 创建备份
                backup_path = filepath + '.backup'
                if not os.path.exists(backup_path):
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        with open(filepath, 'r', encoding='utf-8') as original:
                            f.write(original.read())
                    print(f"已创建备份文件: {backup_path}")
                output_filepath = filepath
            
            # 写入格式化后的内容
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"格式化完成: {output_filepath}")
            
        except Exception as e:
            print(f"格式化文件时出错: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='LaTeX ACM模板格式化工具')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 格式化文件命令
    format_parser = subparsers.add_parser('format', help='格式化LaTeX文件')
    format_parser.add_argument('input_file', help='输入的LaTeX文件路径')
    format_parser.add_argument('-o', '--output', help='输出文件路径（默认覆盖原文件）')
    
    # 创建模板片段命令
    snippet_parser = subparsers.add_parser('snippet', help='创建标准模板片段')
    snippet_parser.add_argument('title', help='模板标题')
    snippet_parser.add_argument('code_file', help='包含代码的文件路径')
    snippet_parser.add_argument('-t', '--time', help='时间复杂度')
    snippet_parser.add_argument('-s', '--space', help='空间复杂度')
    snippet_parser.add_argument('-l', '--language', default='cpp', help='代码语言（默认cpp）')
    snippet_parser.add_argument('-o', '--output', help='输出文件路径')
    
    # 数学符号统一命令
    math_parser = subparsers.add_parser('math', help='统一数学符号')
    math_parser.add_argument('input_file', help='输入的LaTeX文件路径')
    math_parser.add_argument('-o', '--output', help='输出文件路径（默认覆盖原文件）')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    formatter = LatexTemplateFormatter()
    
    if args.command == 'format':
        formatter.format_file(args.input_file, args.output)
    
    elif args.command == 'snippet':
        try:
            with open(args.code_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            snippet = formatter.create_template_snippet(
                args.title, code_content, args.time, args.space, args.language
            )
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(snippet)
                print(f"模板片段已保存到: {args.output}")
            else:
                print(snippet)
        
        except Exception as e:
            print(f"创建模板片段时出错: {e}")
            sys.exit(1)
    
    elif args.command == 'math':
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = formatter.format_math_symbols(content)
            
            output_file = args.output or args.input_file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"数学符号统一完成: {output_file}")
        
        except Exception as e:
            print(f"统一数学符号时出错: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()