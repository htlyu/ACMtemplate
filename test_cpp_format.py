#!/usr/bin/env python3
from format_cpp import CPPFormatter

def test_format():
    formatter = CPPFormatter()
    
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
        ("if(condition)", "if (condition)"),
        ("for(int i=0;i<n;i++)", "for (int i = 0; i < n; i++)"),
        ("a+b*c", "a + b * c"),
    ]
    
    print("测试格式化规则...")
    failed = 0
    for input_str, expected in test_cases:
        result = formatter.format_code(input_str).strip()
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