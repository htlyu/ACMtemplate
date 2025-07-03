#!/bin/bash

# 一键格式化脚本
# 格式化Algorithm-template.tex中的所有C++代码块

set -euo pipefail

echo "🔧 开始格式化C++代码..."

# 检查Python脚本是否存在
if [ ! -f "format_tex_cpp.py" ]; then
    echo "❌ 错误: format_tex_cpp.py 脚本不存在"
    exit 1
fi

# 检查目标文件是否存在
TARGET_FILE="${1:-Algorithm-template.tex}"
if [ ! -f "$TARGET_FILE" ]; then
    echo "❌ 错误: 目标文件 $TARGET_FILE 不存在"
    exit 1
fi

echo "📝 目标文件: $TARGET_FILE"

# 选项处理
BACKUP_FLAG=""
DRY_RUN_FLAG=""
VALIDATE_FLAG=""

while getopts "bdv" opt; do
    case $opt in
        b) BACKUP_FLAG="--backup" ;;
        d) DRY_RUN_FLAG="--dry-run" ;;
        v) VALIDATE_FLAG="--validate" ;;
        \?) echo "用法: $0 [-b] [-d] [-v] [文件名]" >&2
            echo "  -b: 创建备份文件"
            echo "  -d: 预览模式（不实际修改）"
            echo "  -v: 只验证，不格式化"
            exit 1 ;;
    esac
done

# 运行格式化脚本
echo "🏃 执行格式化..."
if python3 format_tex_cpp.py $BACKUP_FLAG $DRY_RUN_FLAG $VALIDATE_FLAG "$TARGET_FILE"; then
    if [ -n "$DRY_RUN_FLAG" ]; then
        echo "👀 预览模式完成"
        exit 0
    elif [ -n "$VALIDATE_FLAG" ]; then
        echo "🔍 验证完成"
        exit 0
    fi
    
    echo "✅ 格式化完成！"
    echo "📄 所有C++代码块已按统一风格格式化"
    
    # 可选：重新编译LaTeX
    read -p "是否重新编译LaTeX文档？ (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📖 正在编译LaTeX文档..."
        if command -v xelatex > /dev/null 2>&1; then
            xelatex -shell-escape "$TARGET_FILE" > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo "✅ LaTeX编译完成！"
                echo "📄 PDF已生成: ${TARGET_FILE%.tex}.pdf"
            else
                echo "⚠️  LaTeX编译出现问题，请检查日志"
            fi
        else
            echo "❌ 未找到xelatex，无法编译LaTeX文档"
        fi
    fi
else
    echo "❌ 格式化失败！"
    exit 1
fi