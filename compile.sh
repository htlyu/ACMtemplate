#!/bin/bash

# 算法模板编译脚本
# Author: Claude Code
# Description: 编译LaTeX算法模板文档

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 文件名
TEX_FILE="Algorithm-template.tex"
PDF_FILE="Algorithm-template.pdf"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    ACM/ICPC 算法模板编译工具${NC}"
echo -e "${BLUE}========================================${NC}"

# 检查文件是否存在
if [ ! -f "$TEX_FILE" ]; then
    echo -e "${RED}错误: $TEX_FILE 文件不存在！${NC}"
    exit 1
fi

# 检查xelatex是否可用
if ! command -v xelatex &> /dev/null; then
    echo -e "${RED}错误: xelatex 未找到！请确保已安装LaTeX发行版。${NC}"
    exit 1
fi

# 清理旧的辅助文件
echo -e "${YELLOW}清理旧的辅助文件...${NC}"
rm -f *.aux *.log *.out *.toc *.pyg *.w18 2>/dev/null
rm -rf _minted-* __pycache__ 2>/dev/null

# 第一次编译
echo -e "${YELLOW}第一次编译...${NC}"
if xelatex -shell-escape -interaction=nonstopmode "$TEX_FILE" > compile.log 2>&1; then
    echo -e "${GREEN}第一次编译完成${NC}"
else
    echo -e "${RED}第一次编译失败！查看 compile.log 了解详情${NC}"
    exit 1
fi

# 第二次编译 (生成完整目录)
echo -e "${YELLOW}第二次编译（生成目录）...${NC}"
if xelatex -shell-escape -interaction=nonstopmode "$TEX_FILE" >> compile.log 2>&1; then
    echo -e "${GREEN}第二次编译完成${NC}"
else
    echo -e "${RED}第二次编译失败！查看 compile.log 了解详情${NC}"
    exit 1
fi

# 检查PDF是否生成
if [ -f "$PDF_FILE" ]; then
    PDF_SIZE=$(ls -lh "$PDF_FILE" | awk '{print $5}')
    echo -e "${GREEN}编译成功！${NC}"
    echo -e "${GREEN}PDF文件: $PDF_FILE (大小: $PDF_SIZE)${NC}"
else
    echo -e "${RED}编译失败：PDF文件未生成${NC}"
    exit 1
fi

# 询问是否清理辅助文件
echo -e "${YELLOW}是否清理辅助文件？[Y/n]${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY]|^$) ]]; then
    echo -e "${YELLOW}清理辅助文件...${NC}"
    rm -f *.aux *.log *.out *.toc *.pyg *.w18 compile.log 2>/dev/null
    rm -rf _minted-* __pycache__ 2>/dev/null
    echo -e "${GREEN}清理完成${NC}"
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}编译完成！可以查看 $PDF_FILE${NC}"
echo -e "${BLUE}========================================${NC}"