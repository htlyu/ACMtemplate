#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进的C++代码格式化工具
专门用于处理我们发现的间距问题
"""

import re
import os
import sys
import argparse

def format_cpp_code(code_block):
    """专门格式化C++代码"""
    lines = code_block.split('\n')
    formatted_lines = []
    
    for line in lines:
        # 保持原始缩进
        indent_match = re.match(r'^(\s*)', line)
        indent = indent_match.group(1) if indent_match else ''
        content = line.strip()
        
        if not content:
            formatted_lines.append('')
            continue
        
        # 逐步应用格式化规则
        content = format_operators(content)
        content = format_keywords(content)
        content = format_templates(content)
        content = clean_spacing(content)
        
        formatted_lines.append(indent + content)
    
    return '\n'.join(formatted_lines)

def format_operators(content):
    """格式化运算符间距"""
    # 保护模板中的 < 和 > 
    # 先标记模板
    template_placeholders = []
    template_counter = 0
    
    def replace_template(match):
        nonlocal template_counter
        placeholder = f"__TEMPLATE_{template_counter}__"
        template_placeholders.append((placeholder, match.group(0)))
        template_counter += 1
        return placeholder
    
    # 标记常见的模板模式，更精确的匹配
    content = re.sub(r'\b\w+\s*<[^<>]*?>', replace_template, content)
    
    # 现在安全地处理运算符
    # 双字符运算符 - 确保两边都有空格
    operators = ['>=', '<=', '==', '!=', '<<', '>>', '&&', '||', 
                 '+=', '-=', '*=', '/=', '%=', '^=', '|=', '&=']
    
    for op in operators:
        # 更精确的正则表达式，确保运算符两边都有字符
        pattern = rf'([a-zA-Z0-9_\]\)])\s*{re.escape(op)}\s*([a-zA-Z0-9_\[\(\-])'
        content = re.sub(pattern, rf'\1 {op} \2', content)
    
    # 单字符运算符 (现在模板已被保护)
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*<\s*([a-zA-Z0-9_\[\(])', r'\1 < \2', content)
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*>\s*([a-zA-Z0-9_\[\(])', r'\1 > \2', content)
    
    # 算术运算符
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*\+\s*([a-zA-Z0-9_\[\(])', r'\1 + \2', content)
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*-\s*([a-zA-Z0-9_\[\(])', r'\1 - \2', content)
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*\*\s*([a-zA-Z0-9_\[\(])', r'\1 * \2', content)
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*/\s*([a-zA-Z0-9_\[\(])', r'\1 / \2', content)
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*%\s*([a-zA-Z0-9_\[\(])', r'\1 % \2', content)
    
    # 位运算符
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*&\s*([a-zA-Z0-9_\[\(\-])', r'\1 & \2', content)
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*\|\s*([a-zA-Z0-9_\[\(])', r'\1 | \2', content)
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*\^\s*([a-zA-Z0-9_\[\(])', r'\1 ^ \2', content)
    
    # 赋值运算符
    content = re.sub(r'([a-zA-Z0-9_\]\)])\s*=\s*([^=])', r'\1 = \2', content)
    
    # 恢复模板
    for placeholder, original in template_placeholders:
        content = content.replace(placeholder, original)
    
    return content

def format_keywords(content):
    """格式化关键字"""
    # if, for, while, switch 后加空格
    content = re.sub(r'\b(if|for|while|switch)\(', r'\1 (', content)
    
    # else 前后加空格
    content = re.sub(r'}else', '} else', content)
    content = re.sub(r'else{', 'else {', content)
    
    # 逗号后加空格
    content = re.sub(r',(\S)', r', \1', content)
    
    # 分号后加空格
    content = re.sub(r';(\S)', r'; \1', content)
    
    return content

def format_templates(content):
    """格式化模板"""
    # 首先处理简单的单参数模板
    content = re.sub(r'(\w+)\s*<\s*([^<>,]+)\s*>', r'\1<\2>', content)
    
    # 处理双参数模板 map<string, int>
    content = re.sub(r'(\w+)\s*<\s*([^<>,]+)\s*,\s*([^<>,]+)\s*>', r'\1<\2, \3>', content)
    
    # 处理复杂嵌套模板
    # priority_queue<int, vector<int>, greater<int>>
    content = re.sub(r'(\w+)\s*<\s*([^<>]+),\s*(\w+)\s*<\s*([^<>]+)\s*>,\s*(\w+)\s*<\s*([^<>]+)\s*>', r'\1<\2, \3<\4>, \5<\6>>', content)
    
    # 清理模板结束符间的空格
    content = re.sub(r'>\s*>', '>>', content)
    
    # 处理模板后紧跟变量名的情况 - 添加空格
    content = re.sub(r'>([a-zA-Z_])', r'> \1', content)
    
    return content

def clean_spacing(content):
    """清理空格"""
    # 移除括号内侧多余空格
    content = re.sub(r'\(\s+', '(', content)
    content = re.sub(r'\s+\)', ')', content)
    
    # 清理模板后的多余空格 (> 后面不应该紧跟空格，除非是变量名)
    content = re.sub(r'>\s+([^a-zA-Z_])', r'>\1', content)
    
    # 移除多余空格，但保留单个空格
    content = re.sub(r'  +', ' ', content)
    
    # 移除行尾空格
    content = content.rstrip()
    
    return content

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

def test_formatting_rules():
    """测试格式化规则的正确性"""
    test_cases = [
        # 间距修复测试
        ("i>=0", "i >= 0"),
        ("hh<=tt", "hh <= tt"),
        ("N<<1", "N << 1"),
        ("l+r>>1", "l + r >> 1"),
        ("1<<i", "1 << i"),
        ("data[i]<cur", "data[i] < cur"),
        ("w[q[tt]]>=w[i]", "w[q[tt]] >= w[i]"),
        ("m^=1ULL", "m ^= 1ULL"),
        ("sz[py]+=sz[px]", "sz[py] += sz[px]"),
        ("i&-i", "i & -i"),
        # 模板格式化测试
        ("vector < int > v;", "vector<int> v;"),
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
    parser = argparse.ArgumentParser(description='改进的C++代码格式化工具')
    parser.add_argument('file', nargs='?', default='Algorithm-template.tex', 
                       help='要格式化的LaTeX文件 (默认: Algorithm-template.tex)')
    parser.add_argument('--backup', action='store_true', 
                       help='创建备份文件')
    parser.add_argument('--test', action='store_true',
                       help='运行格式化规则测试')
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
                print("📝 预览更改 (显示前10处差异):")
                print("=" * 50)
                # 简单的diff显示
                original_lines = content.split('\n')
                formatted_lines = formatted_content.split('\n')
                changes_count = 0
                for i, (orig, fmt) in enumerate(zip(original_lines, formatted_lines), 1):
                    if orig != fmt and changes_count < 10:
                        changes_count += 1
                        print(f"第{i}行:")
                        print(f"- {orig}")
                        print(f"+ {fmt}")
                        print()
                if changes_count == 0:
                    print("🎉 未发现需要格式化的内容")
                elif changes_count == 10:
                    print("... (还有更多变更)")
            else:
                print("🎉 文件已经是正确格式，无需更改")
            sys.exit(0)
        
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