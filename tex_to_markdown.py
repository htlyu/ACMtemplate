#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX转Markdown脚本
专门用于将Algorithm-template.tex转换为Markdown格式
"""

import re
import os
import sys
import argparse

class LaTeXToMarkdownConverter:
    def __init__(self):
        self.conversion_rules = [
            # 章节标题转换
            (r'\\section\{([^}]+)\}', r'# \1'),
            (r'\\subsection\{([^}]+)\}', r'## \1'),
            (r'\\subsubsection\{([^}]+)\}', r'### \1'),
            
            # 移除LaTeX前导部分
            (r'\\documentclass.*?\\begin\{document\}', ''),
            
            # 移除LaTeX命令（更全面）
            (r'\\[a-zA-Z]+\{[^}]*\}', ''),
            (r'\\[a-zA-Z]+\[[^\]]*\]', ''),
            (r'\\[a-zA-Z]+', ''),
            
            # 移除LaTeX环境标记
            (r'\\begin\{[^}]+\}', ''),
            (r'\\end\{[^}]+\}', ''),
            
            # 处理特殊字符
            (r'\\textbf\{([^}]+)\}', r'**\1**'),
            (r'\\textit\{([^}]+)\}', r'*\1*'),
            (r'\\texttt\{([^}]+)\}', r'`\1`'),
            
            # 移除注释行
            (r'^%.*$', ''),
            
            # 清理多余空行
            (r'\n\n\n+', '\n\n'),
        ]
    
    def convert_minted_blocks(self, content):
        """转换minted代码块为markdown代码块，保护代码块不被后续处理影响"""
        self.protected_blocks = []
        
        def replace_minted(match):
            language = match.group(1)
            code_content = match.group(2)
            
            # 清理代码内容但保持原有的花括号
            code_lines = code_content.split('\n')
            cleaned_lines = []
            for line in code_lines:
                # 移除行首空格但保持相对缩进和花括号
                stripped = line.rstrip()
                if stripped:
                    cleaned_lines.append(stripped)
                else:
                    cleaned_lines.append('')
            
            # 创建markdown代码块
            markdown_block = f'```{language}\n' + '\n'.join(cleaned_lines) + '\n```'
            
            # 保护这个代码块，用占位符替换
            placeholder = f'__PROTECTED_CODE_BLOCK_{len(self.protected_blocks)}__'
            self.protected_blocks.append(markdown_block)
            return placeholder
        
        # 匹配minted代码块
        pattern = r'\\begin\{minted\}\{([^}]+)\}\n(.*?)\n\\end\{minted\}'
        result = re.sub(pattern, replace_minted, content, flags=re.DOTALL)
        
        return result
    
    def restore_protected_blocks(self, content):
        """恢复被保护的代码块并修复C++模板语法格式"""
        if hasattr(self, 'protected_blocks'):
            for i, block in enumerate(self.protected_blocks):
                # 修复C++模板语法中的空格问题
                block = self.fix_cpp_template_spacing(block)
                placeholder = f'__PROTECTED_CODE_BLOCK_{i}__'
                content = content.replace(placeholder, block)
        return content
    
    def fix_cpp_template_spacing(self, content):
        """修复C++模板语法中的空格问题"""
        # 修复模板参数中的多余空格
        # vector < T> -> vector<T>
        content = re.sub(r'vector\s*<\s*([^>]+?)\s*>', r'vector<\1>', content)
        # array < type, size > -> array<type, size>
        content = re.sub(r'array\s*<\s*([^,>]+?)\s*,\s*([^>]+?)\s*>', r'array<\1, \2>', content)
        # pair < T1, T2 > -> pair<T1, T2>
        content = re.sub(r'pair\s*<\s*([^,>]+?)\s*,\s*([^>]+?)\s*>', r'pair<\1, \2>', content)
        # map < T1, T2 > -> map<T1, T2>
        content = re.sub(r'map\s*<\s*([^,>]+?)\s*,\s*([^>]+?)\s*>', r'map<\1, \2>', content)
        # set < T > -> set<T>
        content = re.sub(r'set\s*<\s*([^>]+?)\s*>', r'set<\1>', content)
        # queue < T > -> queue<T>
        content = re.sub(r'queue\s*<\s*([^>]+?)\s*>', r'queue<\1>', content)
        # stack < T > -> stack<T>
        content = re.sub(r'stack\s*<\s*([^>]+?)\s*>', r'stack<\1>', content)
        # priority_queue < T > -> priority_queue<T>
        content = re.sub(r'priority_queue\s*<\s*([^>]+?)\s*>', r'priority_queue<\1>', content)
        # 处理更复杂的模板，如 priority_queue < T, vector<T>, greater<T> >
        content = re.sub(r'priority_queue\s*<\s*([^,>]+?)\s*,\s*([^,>]+?)\s*,\s*([^>]+?)\s*>', r'priority_queue<\1, \2, \3>', content)
        # 通用模板修复: template < typename T > -> template<typename T>
        content = re.sub(r'template\s*<\s*([^>]+?)\s*>', r'template<\1>', content)
        # 函数模板: function < return_type(args) > -> function<return_type(args)>
        content = re.sub(r'function\s*<\s*([^>]+?)\s*>', r'function<\1>', content)
        # numeric_limits < T > -> numeric_limits<T>
        content = re.sub(r'numeric_limits\s*<\s*([^>]+?)\s*>', r'numeric_limits<\1>', content)
        # 其他常见的STL容器
        content = re.sub(r'unordered_map\s*<\s*([^,>]+?)\s*,\s*([^>]+?)\s*>', r'unordered_map<\1, \2>', content)
        content = re.sub(r'unordered_set\s*<\s*([^>]+?)\s*>', r'unordered_set<\1>', content)
        content = re.sub(r'multimap\s*<\s*([^,>]+?)\s*,\s*([^>]+?)\s*>', r'multimap<\1, \2>', content)
        content = re.sub(r'multiset\s*<\s*([^>]+?)\s*>', r'multiset<\1>', content)
        content = re.sub(r'deque\s*<\s*([^>]+?)\s*>', r'deque<\1>', content)
        content = re.sub(r'list\s*<\s*([^>]+?)\s*>', r'list<\1>', content)
        content = re.sub(r'forward_list\s*<\s*([^>]+?)\s*>', r'forward_list<\1>', content)
        
        # 修复三目运算符的格式: expr?val1:val2 -> expr ? val1 : val2
        content = re.sub(r'(\w+|\)|])\s*\?\s*([^:]+?)\s*:\s*([^;]+)', r'\1 ? \2 : \3', content)
        
        return content
    
    def process_chinese_content(self, content):
        """处理中文内容，保持格式"""
        # 处理算法说明文本
        content = re.sub(r'\\textbf\{用途：\}([^\\]+)', r'**用途：**\1', content)
        content = re.sub(r'\\textbf\{核心思想：\}([^\\]+)', r'**核心思想：**\1', content)
        content = re.sub(r'\\textbf\{时间复杂度：\}([^\\]+)', r'**时间复杂度：**\1', content)
        content = re.sub(r'\\textbf\{空间复杂度：\}([^\\]+)', r'**空间复杂度：**\1', content)
        content = re.sub(r'\\textbf\{应用场景：\}([^\\]+)', r'**应用场景：**\1', content)
        
        return content
    
    def clean_latex_artifacts(self, content):
        """清理LaTeX残留标记，但保护代码块"""
        # 移除LaTeX配置块
        content = re.sub(r'%=+[^=]*=+%', '', content)
        
        # 只移除特定的LaTeX命令，而不是所有带花括号的内容
        known_latex_commands = [
            'textbf', 'textit', 'texttt', 'emph', 'underline',
            'large', 'Large', 'LARGE', 'huge', 'Huge',
            'small', 'footnotesize', 'scriptsize', 'tiny',
            'centering', 'raggedright', 'raggedleft',
            'vspace', 'hspace', 'vfill', 'hfill',
            'label', 'ref', 'cite', 'footnote',
            'maketitle', 'tableofcontents',
            'newpage', 'clearpage', 'pagebreak',
            'noindent', 'indent'
        ]
        
        # 移除特定的LaTeX命令
        for cmd in known_latex_commands:
            content = re.sub(rf'\\{cmd}\{{[^}}]*\}}', '', content)
            content = re.sub(rf'\\{cmd}\[[^\]]*\]', '', content)
            content = re.sub(rf'\\{cmd}', '', content)
        
        # 移除LaTeX环境标记（但不移除环境内容）
        content = re.sub(r'\\begin\{[^}]+\}', '', content)
        content = re.sub(r'\\end\{[^}]+\}', '', content)
        
        # 移除单独成行的花括号
        content = re.sub(r'^\s*\{\s*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\}\s*$', '', content, flags=re.MULTILINE)
        
        # 清理多余的反斜杠（但不影响代码中的转义字符）
        content = re.sub(r'\\\\', '', content)
        # 只移除孤立的反斜杠，不移除可能在代码中的反斜杠
        content = re.sub(r'\\\s', ' ', content)
        content = re.sub(r'\\$', '', content, flags=re.MULTILINE)
        
        # 移除页面控制命令残留
        content = re.sub(r'newpage', '', content)
        content = re.sub(r'clearpage', '', content)
        content = re.sub(r'pagestyle\{[^}]+\}', '', content)
        content = re.sub(r'setcounter\{[^}]+\}\{[^}]+\}', '', content)
        
        # 清理行首行尾空格
        lines = content.split('\n')
        cleaned_lines = [line.strip() for line in lines]
        content = '\n'.join(cleaned_lines)
        
        # 清理多余空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content
    
    def add_markdown_frontmatter(self, content):
        """添加Markdown前言"""
        frontmatter = """# ACM/ICPC 算法模板

这是一个用于算法竞赛的综合性模板库，包含了常用的数据结构、算法实现和竞赛技巧。

---

"""
        return frontmatter + content
    
    def extract_content_only(self, latex_content):
        """提取文档主体内容，忽略前导配置"""
        # 查找 \begin{document} 之后的内容
        begin_doc_match = re.search(r'\\begin\{document\}', latex_content)
        if begin_doc_match:
            start_pos = begin_doc_match.end()
            # 查找 \end{document} 之前的内容
            end_doc_match = re.search(r'\\end\{document\}', latex_content)
            if end_doc_match:
                end_pos = end_doc_match.start()
                return latex_content[start_pos:end_pos]
            else:
                return latex_content[start_pos:]
        else:
            return latex_content

    def convert(self, latex_content):
        """主转换函数"""
        print("🔄 开始转换LaTeX到Markdown...")
        
        # 1. 提取文档主体内容
        print("📄 提取文档主体内容...")
        content = self.extract_content_only(latex_content)
        
        # 2. 转换代码块（在处理其他LaTeX命令之前）
        print("📝 转换代码块...")
        content = self.convert_minted_blocks(content)
        
        # 3. 转换章节标题
        print("📑 转换章节标题...")
        content = re.sub(r'\\section\{([^}]+)\}', r'# \1', content)
        content = re.sub(r'\\subsection\{([^}]+)\}', r'## \1', content)
        content = re.sub(r'\\subsubsection\{([^}]+)\}', r'### \1', content)
        
        # 4. 处理中文说明内容
        print("🈯 处理中文内容...")
        content = self.process_chinese_content(content)
        
        # 5. 清理LaTeX残留
        print("🧹 清理LaTeX残留...")
        content = self.clean_latex_artifacts(content)
        
        # 6. 移除注释行
        content = re.sub(r'^%.*$', '', content, flags=re.MULTILINE)
        
        # 7. 清理多余空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 8. 添加Markdown前言
        print("📄 添加Markdown格式...")
        content = self.add_markdown_frontmatter(content)
        
        # 9. 恢复被保护的代码块
        print("🔒 恢复受保护的代码块...")
        content = self.restore_protected_blocks(content)
        
        return content

def main():
    parser = argparse.ArgumentParser(description='将LaTeX算法模板转换为Markdown')
    parser.add_argument('input', nargs='?', default='Algorithm-template.tex',
                       help='输入的LaTeX文件 (默认: Algorithm-template.tex)')
    parser.add_argument('output', nargs='?', default='Algorithm-template.md',
                       help='输出的Markdown文件 (默认: Algorithm-template.md)')
    parser.add_argument('--encoding', default='utf-8',
                       help='文件编码 (默认: utf-8)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ 错误: 输入文件 {args.input} 不存在")
        sys.exit(1)
    
    try:
        print(f"📖 读取文件: {args.input}")
        with open(args.input, 'r', encoding=args.encoding) as f:
            latex_content = f.read()
        
        converter = LaTeXToMarkdownConverter()
        markdown_content = converter.convert(latex_content)
        
        print(f"💾 写入文件: {args.output}")
        with open(args.output, 'w', encoding=args.encoding) as f:
            f.write(markdown_content)
        
        print(f"✅ 转换完成!")
        print(f"📊 统计信息:")
        print(f"   - 输入文件大小: {len(latex_content):,} 字符")
        print(f"   - 输出文件大小: {len(markdown_content):,} 字符")
        print(f"   - 代码块数量: {markdown_content.count('```')//2}")
        print(f"   - 章节数量: {markdown_content.count('# ')}")
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()