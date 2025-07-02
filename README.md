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

## TODO

- [ ] 优化点分治算法中的子树大小计算方法
- [ ] 添加更多动态规划优化技巧
- [ ] 完善字符串算法的应用示例
- [ ] 继续完善其他复杂算法的使用说明文档

## 贡献

欢迎提交Issue和Pull Request来改进模板内容。

## 许可证

本模板仅供学习和竞赛使用。