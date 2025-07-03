#!/bin/bash
# 用法: ./run.sh [源文件] [超时时间]
# 例子: ./run.sh a.cpp 5s
set -euo pipefail
# 参数与默认值
src=${1:-a.cpp}
t=${2:-1s}
bin=${src%.cpp}
in=${bin}.in
# 编译（仅在源文件更新时）
if [ ! -f "${bin}_asan" ] || [ "$src" -nt "${bin}_asan" ]; then
    g++ -std=c++20 -Og -g -fsanitize=address \
        -o${bin}_asan "$src" || { echo CE >&2; exit 1; }
fi
# 不加检查 速度正常
# g++ -std=c++20 -O2 -Wall -Wextra -o"$bin" "$src" || { echo CE >&2; exit 1; }
# 记录开始时间（毫秒）
s=$(date +%s%3N)
# 运行并限时
set +e; timeout "$t" "./${bin}_asan" <"$in"; st=$?; set -e
# 记录结束时间（毫秒）
e=$(date +%s%3N)
# 输出运行时间
echo "run time: $((e-s)) ms"
# 处理超时
[ $st -eq 124 ] && echo TLE
# 以程序自身退出码退出
exit $st