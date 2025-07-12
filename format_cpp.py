#!/usr/bin/env python3
"""
独立的C++代码格式化工具
"""

import re
import sys
import os


class CPPFormatter:
    def __init__(self):
        self.formatting_rules = [
            # 移除行尾空格
            (r'\s+$', ''),
            
            # ============ 运算符间距修复 (高优先级) ============
            # 比较运算符间距
            (r'([a-zA-Z0-9_\]\)])>=([a-zA-Z0-9_\[\(])', r'\1 >= \2'),
            (r'([a-zA-Z0-9_\]\)])<=([a-zA-Z0-9_\[\(])', r'\1 <= \2'),
            (r'([a-zA-Z0-9_\]\)])==([a-zA-Z0-9_\[\(])', r'\1 == \2'),
            (r'([a-zA-Z0-9_\]\)])!=([a-zA-Z0-9_\[\(])', r'\1 != \2'),
            (r'([a-zA-Z0-9_\]\)])>(?![>=])([a-zA-Z0-9_\[\(])', r'\1 > \2'),
            (r'([a-zA-Z0-9_\]\)])<(?![<=])([a-zA-Z0-9_\[\(])', r'\1 < \2'),
            
            # 位移运算符间距
            (r'([a-zA-Z0-9_\]\)])<<([a-zA-Z0-9_\[\(])', r'\1 << \2'),
            (r'([a-zA-Z0-9_\]\)])>>([a-zA-Z0-9_\[\(])', r'\1 >> \2'),
            
            # 逻辑运算符间距
            (r'([a-zA-Z0-9_\]\)])&&([a-zA-Z0-9_\[\(])', r'\1 && \2'),
            (r'([a-zA-Z0-9_\]\)])\|\|([a-zA-Z0-9_\[\(])', r'\1 || \2'),
            
            # 算术运算符间距
            (r'([a-zA-Z0-9_\]\)])\+([a-zA-Z0-9_\[\(])', r'\1 + \2'),
            (r'([a-zA-Z0-9_\]\)])-([a-zA-Z0-9_\[\(])', r'\1 - \2'),
            (r'([a-zA-Z0-9_\]\)])\*([a-zA-Z0-9_\[\(])', r'\1 * \2'),
            (r'([a-zA-Z0-9_\]\)])/([a-zA-Z0-9_\[\(])', r'\1 / \2'),
            (r'([a-zA-Z0-9_\]\)])%([a-zA-Z0-9_\[\(])', r'\1 % \2'),
            
            # 位运算符间距
            (r'([a-zA-Z0-9_\]\)])&([a-zA-Z0-9_\[\(\-])', r'\1 & \2'),
            (r'([a-zA-Z0-9_\]\)])\|([a-zA-Z0-9_\[\(])', r'\1 | \2'),
            (r'([a-zA-Z0-9_\]\)])\^([a-zA-Z0-9_\[\(])', r'\1 ^ \2'),
            
            # 赋值运算符间距
            (r'([a-zA-Z0-9_\]\)])\+=([a-zA-Z0-9_\[\(])', r'\1 += \2'),
            (r'([a-zA-Z0-9_\]\)])-=([a-zA-Z0-9_\[\(])', r'\1 -= \2'),
            (r'([a-zA-Z0-9_\]\)])\*=([a-zA-Z0-9_\[\(])', r'\1 *= \2'),
            (r'([a-zA-Z0-9_\]\)])/=([a-zA-Z0-9_\[\(])', r'\1 /= \2'),
            (r'([a-zA-Z0-9_\]\)])%=([a-zA-Z0-9_\[\(])', r'\1 %= \2'),
            (r'([a-zA-Z0-9_\]\)])\^=([a-zA-Z0-9_\[\(])', r'\1 ^= \2'),
            (r'([a-zA-Z0-9_\]\)])\|=([a-zA-Z0-9_\[\(])', r'\1 |= \2'),
            (r'([a-zA-Z0-9_\]\)])&=([a-zA-Z0-9_\[\(])', r'\1 &= \2'),
            (r'([a-zA-Z0-9_\]\)])=([^=])', r'\1 = \2'),
            
            # ============ 关键字格式化 ============
            # { 前加空格
            (r'(\w)\{', r'\1 {'),
            # 逗号后加空格
            (r',(\S)', r', \1'),
            # 关键字后加空格
            (r'\b(if|for|while|switch)\(', r'\1 ('),
            # else 处理
            (r'}else', '} else'),
            (r'else{', 'else {'),
            # 分号后加空格
            (r';(\S)', r'; \1'),
            
            # ============ 清理 ============
            # 移除多余空格
            (r'  +', ' '),
        ]

    def format_code(self, code):
        """格式化C++代码"""
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # 保存原始缩进
            indent = len(line) - len(line.lstrip())
            content = line.strip()
            
            if content:
                # 应用格式化规则
                for pattern, replacement in self.formatting_rules:
                    content = re.sub(pattern, replacement, content)
            
            # 恢复缩进
            formatted_lines.append(' ' * indent + content if content else '')
        
        return '\n'.join(formatted_lines)

    def format_file(self, file_path):
        """格式化文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            formatted_content = self.format_code(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            print(f"已格式化: {file_path}")
            
        except Exception as e:
            print(f"格式化失败 {file_path}: {e}")


def main():
    formatter = CPPFormatter()
    
    if len(sys.argv) < 2:
        print("用法: python format_cpp.py <文件路径...>")
        sys.exit(1)
    
    for file_path in sys.argv[1:]:
        if os.path.exists(file_path):
            formatter.format_file(file_path)
        else:
            print(f"文件不存在: {file_path}")


if __name__ == "__main__":
    main()