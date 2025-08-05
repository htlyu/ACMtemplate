# 算法模板编译指南

## 快速开始

### 编译LaTeX文档
运行编译脚本：
```bash
./compile.sh
```

### 清理辅助文件
运行清理脚本：
```bash
./clean.sh
```

## 手动编译

如果需要手动编译，请按以下步骤：

```bash
# 清理旧文件
rm -f *.aux *.log *.out *.toc *.pyg *.w18
rm -rf _minted-Algorithm-template/

# 第一次编译
xelatex -shell-escape Algorithm-template.tex

# 第二次编译（生成完整目录）
xelatex -shell-escape Algorithm-template.tex
```

## 文件说明

- `Algorithm-template.tex` - 主要的LaTeX源文件
- `Algorithm-template.pdf` - 编译生成的PDF文件
- `compile.sh` - 自动编译脚本
- `clean.sh` - 清理辅助文件脚本
- `CLAUDE.md` - Claude Code项目说明文档

## 常见问题

### 编译失败
- 确保安装了XeLaTeX和相关包
- 确保系统已安装Python和pygments（用于代码高亮）
- 检查`compile.log`文件了解详细错误信息

### 中文显示问题
- 确保系统已安装中文字体
- XeLaTeX会自动处理中文字符

### 代码高亮问题
- 确保已安装pygments：`pip install pygments`
- 确保LaTeX可以执行shell命令（-shell-escape参数）

## 注意事项

1. 编译需要运行两次才能生成完整的目录
2. 首次编译可能需要下载一些LaTeX包，请耐心等待
3. 编译过程中会生成很多辅助文件，可以使用`clean.sh`清理