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
from typing import List, Tuple

def format_cpp_code(code_block):
    """专门格式化C++代码"""
    lines = code_block.split('\n')
    formatted_lines = []
    
    cpp_rules = [
        # 移除行尾空格
        (r'\s+$', ''),
        
        # ============ 模板格式化规则 (最后应用) ============
        
        # ============ 常规格式化规则 ============
        # { 前加空格
        (r'(\w)\{', r'\1 {'),
        # 逗号后加空格 (但不影响模板参数)
        (r',(\S)', r', \1'),
        # 逻辑运算符前后加空格 (优先处理)
        (r'([)\w\]])(&&|\|\|)([(\w\[])', r'\1 \2 \3'),
        # 比较运算符前后加空格 (避免影响模板)
        (r'([)\w\]])(==|!=|<=|>=)([(\w\[])', r'\1 \2 \3'),
        (r'([)\w\]])\s*(<|>)\s*([(\w\[])', r'\1 \2 \3'),
        # 赋值运算符前后加空格
        (r'([)\w\]])\s*(=)\s*([^=])', r'\1 \2 \3'),
        # 算术运算符前后加空格
        (r'([)\w\]])\s*([\+\-\*/%])\s*([(\w\[])', r'\1 \2 \3'),
        # 位运算符前后加空格 (避免影响模板的>>)
        (r'([)\w\]])\s*(<<)\s*([(\w\[])', r'\1 \2 \3'),
        # if/for/while后加空格
        (r'\b(if|for|while|switch)\(', r'\1 ('),
        # else前后加空格
        (r'}else', r'} else'),
        (r'else{', r'else {'),
        # 关键字前后空格（变量声明等）
        (r'>(\w)', r'> \1'),
        # 括号内侧空格处理
        (r'\(\s+', '('),
        (r'\s+\)', ')'),
        # 分号后空格
        (r';(\S)', r'; \1'),
        # 移除多余空格
        (r'  +', ' '),
        
        # ============ 模板格式化规则 (最后应用以避免被其他规则影响) ============
        # 修复模板角括号间的空格问题 - 简单模板
        (r'(\w+)\s*<\s*([^<>,]+)\s*>', r'\1<\2>'),
        # 修复模板角括号间的空格问题 - 带逗号的模板（先处理逗号空格）
        # 修复嵌套模板的空格问题
        (r'(\w+)\s*<\s*(\w+)\s*<\s*([^<>]+)\s*>\s*>', r'\1<\2<\3>>'),
        # 修复三重嵌套模板
        (r'(\w+)\s*<\s*(\w+)\s*<\s*(\w+)\s*<\s*([^<>]+)\s*>\s*>\s*>', r'\1<\2<\3<\4>>>'),
        # 修复priority_queue等复杂模板
        (r'priority_queue\s*<\s*([^,<>]+)\s*,\s*vector\s*<\s*([^<>]+)\s*>\s*,\s*greater\s*<\s*([^<>]+)\s*>\s*>', r'priority_queue<\1, vector<\2>, greater<\3>>'),
        # 修复std::vector<bool>等标准库模板
        (r'std\s*::\s*vector\s*<\s*([^<>]+)\s*>', r'std::vector<\1>'),
        (r'std\s*::\s*(\w+)\s*<\s*([^<>]+)\s*>', r'std::\1<\2>'),
        # 修复template声明
        (r'template\s*<\s*([^<>]+)\s*>', r'template<\1>'),
        # 修复numeric_limits等
        (r'numeric_limits\s*<\s*([^<>]+)\s*>', r'numeric_limits<\1>'),
        # 最终清理模板空格
        (r'<\s+', '<'),
        (r'\s+>', '>'),
        (r'>\s+>', '>>'),
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

def validate_template_formatting(content: str) -> List[Tuple[int, str]]:
    """验证模板格式化是否正确"""
    lines = content.split('\n')
    issues = []
    
    # 检查常见的模板格式化问题
    template_patterns = [
        (r'\w\s+<\s+\w', '模板角括号内有多余空格'),
        (r'>\s+>', '模板结束符间有空格'),
        (r'vector\s*<\s*\w+\s*>', 'vector模板格式不正确'),
        (r'priority_queue\s*<[^>]+>\s*>', 'priority_queue模板格式不正确'),
        (r'template\s*<\s*[^>]+\s*>', 'template声明格式不正确'),
        (r'numeric_limits\s*<\s*\w+\s*>', 'numeric_limits模板格式不正确'),
    ]
    
    for line_num, line in enumerate(lines, 1):
        for pattern, description in template_patterns:
            if re.search(pattern, line):
                issues.append((line_num, f"{description}: {line.strip()}"))
    
    return issues

def test_formatting_rules():
    """测试格式化规则的正确性"""
    test_cases = [
        # 模板格式化测试
        ("vector < int > v;", "vector<int> v;"),
        ("priority_queue < int, vector < int >, greater < int >> pq;", "priority_queue<int, vector<int>, greater<int>> pq;"),
        ("template < typename T >", "template<typename T>"),
        ("numeric_limits < T >::max()", "numeric_limits<T>::max()"),
        ("map < string, int > mp;", "map<string, int> mp;"),
        ("array < int, 2 > arr;", "array<int, 2> arr;"),
        # 常规格式化测试
        ("if(condition)", "if (condition)"),
        ("for(int i=0;i<n;i++)", "for (int i = 0; i < n; i++)"),
        ("a+b*c", "a + b * c"),
        ("vector<int>v(n,0);", "vector<int> v(n, 0);"),
    ]
    
    print("🧪 测试格式化规则...")
    failed_tests = []
    
    for input_code, expected in test_cases:
        result = format_cpp_code(input_code).strip()
        if result != expected:
            failed_tests.append((input_code, expected, result))
    
    if failed_tests:
        print("❌ 以下测试用例失败:")
        for input_code, expected, result in failed_tests:
            print(f"  输入: {input_code}")
            print(f"  期望: {expected}")
            print(f"  实际: {result}")
            print()
        return False
    else:
        print("✅ 所有测试用例通过!")
        return True

def main():
    parser = argparse.ArgumentParser(description='一键式格式化LaTeX文件中的C++代码块')
    parser.add_argument('file', nargs='?', default='Algorithm-template.tex', 
                       help='要格式化的LaTeX文件 (默认: Algorithm-template.tex)')
    parser.add_argument('--backup', action='store_true', 
                       help='创建备份文件')
    parser.add_argument('--test', action='store_true',
                       help='运行格式化规则测试')
    parser.add_argument('--validate', action='store_true',
                       help='验证文件中的模板格式化问题')
    parser.add_argument('--dry-run', action='store_true',
                       help='只预览更改，不实际修改文件')
    
    args = parser.parse_args()
    
    # 运行测试
    if args.test:
        success = test_formatting_rules()
        sys.exit(0 if success else 1)
    
    if not os.path.exists(args.file):
        print(f"错误: 文件 {args.file} 不存在")
        sys.exit(1)
    
    try:
        # 读取文件
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证模式
        if args.validate:
            print(f"🔍 验证 {args.file} 中的模板格式化问题...")
            issues = validate_template_formatting(content)
            if issues:
                print(f"❌ 发现 {len(issues)} 个格式化问题:")
                for line_num, issue in issues:
                    print(f"  第{line_num}行: {issue}")
            else:
                print("✅ 未发现模板格式化问题")
            sys.exit(1 if issues else 0)
        
        print(f"正在格式化 {args.file} 中的C++代码块...")
        
        # 创建备份
        if args.backup:
            backup_file = args.file + '.backup'
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已创建备份文件: {backup_file}")
        
        # 格式化C++代码块
        formatted_content = format_latex_cpp_blocks(content)
        
        # 预览模式
        if args.dry_run:
            if content != formatted_content:
                print("📝 预览更改:")
                print("=" * 50)
                # 简单的diff显示
                original_lines = content.split('\n')
                formatted_lines = formatted_content.split('\n')
                changes_found = False
                for i, (orig, fmt) in enumerate(zip(original_lines, formatted_lines), 1):
                    if orig != fmt:
                        changes_found = True
                        print(f"第{i}行:")
                        print(f"- {orig}")
                        print(f"+ {fmt}")
                        print()
                if not changes_found:
                    print("🎉 未发现需要格式化的内容")
            else:
                print("🎉 文件已经是正确格式，无需更改")
            sys.exit(0)
        
        # 写入格式化后的内容
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        print(f"✅ 格式化完成: {args.file}")
        print("所有C++代码块已按统一风格格式化")
        
        # 格式化后再次验证
        issues = validate_template_formatting(formatted_content)
        if issues:
            print(f"⚠️  格式化后仍存在 {len(issues)} 个问题，建议检查:")
            for line_num, issue in issues[:5]:  # 只显示前5个问题
                print(f"  第{line_num}行: {issue}")
        else:
            print("🎯 格式化验证通过!")
        
    except Exception as e:
        print(f"❌ 格式化失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()