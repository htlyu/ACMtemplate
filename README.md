# ACM/ICPC 算法模板

这是一个用于算法竞赛的综合性模板库，包含了常用的数据结构、算法实现和竞赛技巧。

## 文件结构

- `Algorithm-template.tex` - 主要的LaTeX模板文件，包含所有算法实现
- `Algorithm-template.pdf` - 编译生成的PDF文件，可打印带到比赛现场
- 其他参考资料PDF文件

## 算法分类

模板按以下类别组织：

### 数据结构
- ST表、线段树、FHQ-Treap
- 并查集、树状数组
- 平衡树、LCT（Link-Cut Tree）
- 可持久化数据结构

### 树算法
- 重链剖分、树链剖分
- 树上启发式合并
- 虚树、点分治
- LCA算法

### 图论
- 最短路算法
- 最小生成树
- 网络流、费用流
- 强连通分量、2-SAT

### 字符串
- KMP、Z算法
- Manacher算法
- 后缀数组、后缀自动机
- 回文自动机、Palindrome series

### 动态规划
- 背包问题
- 区间DP、树形DP
- 数位DP、状压DP
- DP优化技巧

### 数论
- 快速幂、扩展欧几里得
- 中国剩余定理
- 原根、离散对数
- 数论变换

### 线性代数
- 矩阵运算
- 高斯消元
- 线性基

### 杂项
- 整体二分
- CDQ分治
- 莫队算法

## 编译方法

### 基本编译
```bash
xelatex -shell-escape Algorithm-template.tex
```

### 完整编译（包含目录）
```bash
xelatex -shell-escape Algorithm-template.tex
xelatex -shell-escape Algorithm-template.tex
```

### 清理生成文件
```bash
rm -f *.aux *.log *.out *.synctex.gz *.toc *.pyg
rm -rf _minted-Algorithm-template/
```

## 🛠️ 辅助脚本

本项目包含了多个实用脚本，帮助管理和维护算法模板：

### 🔍 脚本快速参考

| 脚本名称 | 主要功能 | 使用场景 | 命令 |
|---------|---------|---------|------|
| `format_all.sh` | 一键格式化+编译 | 日常维护 | `./format_all.sh` |
| `convert_to_markdown.sh` | LaTeX转Markdown | 生成网页版 | `./convert_to_markdown.sh` |
| `format_tex_cpp.py` | C++代码格式化 | 代码风格统一 | `python3 format_tex_cpp.py` |
| `tex_to_markdown.py` | LaTeX转换核心 | 精确控制转换 | `python3 tex_to_markdown.py` |
| `format_template.py` | LaTeX格式标准化 | 模板维护 | `python3 format_template.py` |
| `format_cpp.py` | 独立C++文件格式化 | 外部代码整理 | `python3 format_cpp.py *.cpp` |

### 📝 代码格式化脚本

#### `format_tex_cpp.py` - LaTeX中C++代码格式化
**功能**: 格式化LaTeX文件中的所有C++代码块，统一代码风格
**用法**:
```bash
# 格式化默认文件
python3 format_tex_cpp.py

# 格式化指定文件
python3 format_tex_cpp.py your-file.tex

# 创建备份
python3 format_tex_cpp.py --backup
```
**特点**:
- 自动识别minted代码块
- 运算符前后加空格 (`a+b` → `a + b`)
- 关键字后加空格 (`if(` → `if (`)
- 统一括号和逗号格式

#### `format_cpp.py` - 独立C++文件格式化
**功能**: 格式化独立的C++源文件
**用法**:
```bash
python3 format_cpp.py file1.cpp file2.cpp
```

#### `format_template.py` - LaTeX模板格式化
**功能**: 统一LaTeX模板格式，标准化数学符号和命令
**用法**:
```bash
python3 format_template.py Algorithm-template.tex
```
**特点**:
- 统一数学符号 (`\le` → `\leqslant`)
- 标准化代码块格式
- 优化空行和缩进

#### `format_all.sh` - 一键格式化
**功能**: 一键格式化所有C++代码，可选择重新编译LaTeX
**用法**:
```bash
./format_all.sh
```
**流程**:
1. 格式化所有C++代码块
2. 询问是否重新编译LaTeX文档
3. 自动运行两次编译生成完整目录

### 📄 文档转换脚本

#### `tex_to_markdown.py` - LaTeX转Markdown
**功能**: 将LaTeX算法模板转换为Markdown格式
**用法**:
```bash
# 使用默认文件名
python3 tex_to_markdown.py

# 指定输入输出文件
python3 tex_to_markdown.py input.tex output.md
```
**特点**:
- 转换章节标题 (`\section{}` → `# 标题`)
- 转换代码块 (`\begin{minted}{cpp}` → ` ```cpp`)
- 保留中文算法说明
- 清理LaTeX命令和环境

#### `convert_to_markdown.sh` - 便捷转换脚本
**功能**: 一键转换LaTeX到Markdown，包含预览功能
**用法**:
```bash
./convert_to_markdown.sh

# 指定文件
./convert_to_markdown.sh input.tex output.md
```
**特点**:
- 显示转换进度和统计信息
- 可选择预览转换结果
- 友好的用户交互界面

### 📋 使用建议

#### 日常维护工作流
1. **添加新算法后**:
   ```bash
   ./format_all.sh  # 格式化代码并重新编译
   ```

2. **生成Markdown版本**:
   ```bash
   ./convert_to_markdown.sh  # 转换为Markdown格式
   ```

3. **代码风格检查**:
   ```bash
   python3 format_tex_cpp.py --backup  # 格式化前创建备份
   ```

#### 脚本优先级
- **日常使用**: `format_all.sh`, `convert_to_markdown.sh`
- **精细控制**: `format_tex_cpp.py`, `tex_to_markdown.py`
- **特殊需求**: `format_template.py`, `format_cpp.py`

## 使用说明

1. 模板设计为可打印格式，适合在比赛中使用
2. 所有算法都包含了详细的实现和使用说明
3. 代码注释采用中文，便于理解
4. 复杂算法包含了使用场景和核心思想的解释

## 模板特色

- **双栏布局** - 节省纸张空间
- **语法高亮** - 使用minted包实现C++代码高亮
- **中文支持** - 完整的中文注释和说明
- **实用导向** - 所有算法都经过竞赛验证

## 📁 文件说明

### 核心文件
- `Algorithm-template.tex` - 主LaTeX模板文件（源文件）
- `Algorithm-template.pdf` - 编译生成的PDF文件（比赛用）
- `Algorithm-template.md` - Markdown版本（网页查看）
- `README.md` - 项目说明文档
- `CLAUDE.md` - Claude Code 工作指令

### 配置文件
- `compile_command.txt` - LaTeX编译命令参考
- `_minted-Algorithm-template/` - minted生成的代码高亮文件

### 脚本文件详细说明

#### 格式化脚本
- **`format_all.sh`** - 最常用的脚本，一键完成代码格式化和LaTeX编译
- **`format_tex_cpp.py`** - 核心格式化引擎，处理LaTeX中的C++代码块
- **`format_cpp.py`** - 处理独立的.cpp文件
- **`format_template.py`** - 标准化LaTeX模板格式和数学符号

#### 转换脚本  
- **`convert_to_markdown.sh`** - 用户友好的转换界面，包含预览功能
- **`tex_to_markdown.py`** - 转换引擎，将LaTeX转换为Markdown

#### 使用建议
```bash
# 新手推荐：使用Shell脚本，交互友好
./format_all.sh           # 格式化代码
./convert_to_markdown.sh   # 转换文档

# 高级用户：直接使用Python脚本，更多控制选项
python3 format_tex_cpp.py --backup
python3 tex_to_markdown.py input.tex output.md
```

## 🎯 工作流程建议

### 添加新算法
1. 在LaTeX中添加算法代码和说明
2. 运行 `./format_all.sh` 格式化并编译
3. 运行 `./convert_to_markdown.sh` 生成Markdown版本
4. 提交更改到版本控制

### 代码维护
1. 定期运行 `python3 format_tex_cpp.py` 保持代码风格一致
2. 使用 `--backup` 选项在重要操作前创建备份
3. 验证PDF和Markdown版本的一致性

## TODO

- [ ] 优化点分治算法中的子树大小计算方法
- [ ] 添加更多动态规划优化技巧  
- [ ] 完善字符串算法的应用示例
- [ ] 继续完善其他复杂算法的使用说明文档
- [ ] 添加脚本的单元测试
- [ ] 优化Markdown转换的表格处理
- [ ] 增加代码块的语法检查功能

## 贡献

欢迎提交Issue和Pull Request来改进模板内容。

## 许可证

本模板仅供学习和竞赛使用。