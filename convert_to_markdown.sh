#!/bin/bash

# LaTeX到Markdown转换脚本
# 将Algorithm-template.tex转换为Markdown格式

echo "📄 LaTeX到Markdown转换工具"
echo "================================"

# 检查输入文件
INPUT_FILE="${1:-Algorithm-template.tex}"
OUTPUT_FILE="${2:-Algorithm-template.md}"

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ 错误: 输入文件 $INPUT_FILE 不存在"
    exit 1
fi

echo "📖 输入文件: $INPUT_FILE"
echo "📝 输出文件: $OUTPUT_FILE"
echo ""

# 运行转换脚本
python3 tex_to_markdown.py "$INPUT_FILE" "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 转换成功完成！"
    echo ""
    echo "📊 文件信息:"
    echo "   输入文件大小: $(wc -c < "$INPUT_FILE") bytes"
    echo "   输出文件大小: $(wc -c < "$OUTPUT_FILE") bytes"
    echo "   输出文件行数: $(wc -l < "$OUTPUT_FILE") lines"
    echo ""
    
    # 可选：预览文件
    read -p "是否要预览生成的Markdown文件前50行？ (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📖 预览 $OUTPUT_FILE 前50行:"
        echo "================================"
        head -50 "$OUTPUT_FILE"
        echo "================================"
        echo "... (还有更多内容)"
    fi
    
    echo ""
    echo "✅ 转换完成！Markdown文件已保存为: $OUTPUT_FILE"
    echo "💡 提示：你可以使用Markdown编辑器或GitHub查看此文件"
    
else
    echo "❌ 转换失败！"
    exit 1
fi