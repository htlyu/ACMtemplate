#!/usr/bin/env python3
"""
简化版格式化工具，专门修复我们发现的间距问题
"""
import re

def format_cpp_line(line):
    """格式化单行C++代码"""
    # 保持缩进
    indent = len(line) - len(line.lstrip())
    content = line.strip()
    
    if not content:
        return line
    
    # 运算符间距修复
    # 精确匹配常见的问题模式
    replacements = [
        # 比较运算符
        (r'([a-zA-Z0-9_\]\)])>=([a-zA-Z0-9_\[\(])', r'\1 >= \2'),
        (r'([a-zA-Z0-9_\]\)])<=([a-zA-Z0-9_\[\(])', r'\1 <= \2'),
        (r'([a-zA-Z0-9_\]\)])>(?![>=])([a-zA-Z0-9_\[\(])', r'\1 > \2'),
        (r'([a-zA-Z0-9_\]\)])<(?![<=])([a-zA-Z0-9_\[\(])', r'\1 < \2'),
        (r'([a-zA-Z0-9_\]\)])!=([a-zA-Z0-9_\[\(])', r'\1 != \2'),
        (r'([a-zA-Z0-9_\]\)])==([a-zA-Z0-9_\[\(])', r'\1 == \2'),
        
        # 位运算符
        (r'([a-zA-Z0-9_\]\)])<<([a-zA-Z0-9_\[\(])', r'\1 << \2'),
        (r'([a-zA-Z0-9_\]\)])>>([a-zA-Z0-9_\[\(])', r'\1 >> \2'),
        (r'([a-zA-Z0-9_\]\)])&([a-zA-Z0-9_\[\(\-])', r'\1 & \2'),
        (r'([a-zA-Z0-9_\]\)])\|([a-zA-Z0-9_\[\(])', r'\1 | \2'),
        (r'([a-zA-Z0-9_\]\)])\^([a-zA-Z0-9_\[\(])', r'\1 ^ \2'),
        
        # 算术运算符
        (r'([a-zA-Z0-9_\]\)])\+([a-zA-Z0-9_\[\(])', r'\1 + \2'),
        (r'([a-zA-Z0-9_\]\)])-([a-zA-Z0-9_\[\(])', r'\1 - \2'),
        (r'([a-zA-Z0-9_\]\)])\*([a-zA-Z0-9_\[\(])', r'\1 * \2'),
        (r'([a-zA-Z0-9_\]\)])/([a-zA-Z0-9_\[\(])', r'\1 / \2'),
        (r'([a-zA-Z0-9_\]\)])%([a-zA-Z0-9_\[\(])', r'\1 % \2'),
        
        # 赋值运算符
        (r'([a-zA-Z0-9_\]\)])\+=([a-zA-Z0-9_\[\(])', r'\1 += \2'),
        (r'([a-zA-Z0-9_\]\)])-=([a-zA-Z0-9_\[\(])', r'\1 -= \2'),
        (r'([a-zA-Z0-9_\]\)])\*=([a-zA-Z0-9_\[\(])', r'\1 *= \2'),
        (r'([a-zA-Z0-9_\]\)])/=([a-zA-Z0-9_\[\(])', r'\1 /= \2'),
        (r'([a-zA-Z0-9_\]\)])%=([a-zA-Z0-9_\[\(])', r'\1 %= \2'),
        (r'([a-zA-Z0-9_\]\)])\^=([a-zA-Z0-9_\[\(])', r'\1 ^= \2'),
        (r'([a-zA-Z0-9_\]\)])\|=([a-zA-Z0-9_\[\(])', r'\1 |= \2'),
        (r'([a-zA-Z0-9_\]\)])&=([a-zA-Z0-9_\[\(])', r'\1 &= \2'),
        (r'([a-zA-Z0-9_\]\)])=([^=])', r'\1 = \2'),
        
        # 逻辑运算符
        (r'([a-zA-Z0-9_\]\)])&&([a-zA-Z0-9_\[\(])', r'\1 && \2'),
        (r'([a-zA-Z0-9_\]\)])\|\|([a-zA-Z0-9_\[\(])', r'\1 || \2'),
        
        # 关键字
        (r'\b(if|for|while|switch)\(', r'\1 ('),
        (r'}else', '} else'),
        (r'else{', 'else {'),
        (r'(\w)\{', r'\1 {'),
        
        # 逗号和分号
        (r',(\S)', r', \1'),
        (r';(\S)', r'; \1'),
        
        # 模板简化 - 先处理内部空格，再处理外部空格
        (r'(\w+)\s*<\s*([^<>,]+)\s*>\s*', r'\1<\2> '),
        (r'(\w+)\s*<\s*([^<>,]+)\s*,\s*([^<>,]+)\s*>\s*', r'\1<\2, \3> '),
        # 清理模板结尾多余空格（除非后面是字母）
        (r'>\s+(?![a-zA-Z_])', '>'),
        (r'>([a-zA-Z_])', r'> \1'),
        
        # 清理
        (r'\(\s+', '('),
        (r'\s+\)', ')'),
        (r'  +', ' '),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    return ' ' * indent + content

def test_format():
    test_cases = [
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
        ("vector < int > v;", "vector<int> v;"),
        ("map < string, int > mp;", "map<string, int> mp;"),
        ("if(condition)", "if (condition)"),
        ("for(int i=0;i<n;i++)", "for (int i = 0; i < n; i++)"),
        ("a+b*c", "a + b * c"),
        ("vector<int>v(n,0);", "vector<int> v(n, 0);"),
    ]
    
    print("测试格式化规则...")
    failed = 0
    for input_str, expected in test_cases:
        result = format_cpp_line(input_str).strip()
        if result != expected:
            print(f"❌ 失败: '{input_str}' -> '{result}', 期望: '{expected}'")
            failed += 1
        else:
            print(f"✅ 通过: '{input_str}' -> '{result}'")
    
    if failed == 0:
        print("🎉 所有测试通过!")
    else:
        print(f"❌ {failed} 个测试失败")

if __name__ == '__main__':
    test_format()