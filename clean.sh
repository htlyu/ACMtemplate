#!/bin/bash

# 清理LaTeX辅助文件脚本
# Author: Claude Code

echo "清理LaTeX辅助文件..."

# 删除LaTeX生成的辅助文件
rm -f *.aux *.log *.out *.toc *.pyg *.w18 compile.log 2>/dev/null

# 删除minted生成的目录
rm -rf _minted-* 2>/dev/null

# 删除Python缓存
rm -rf __pycache__ 2>/dev/null

# 删除其他可能的临时文件
rm -f *.fls *.fdb_latexmk *.synctex.gz 2>/dev/null

echo "清理完成！"