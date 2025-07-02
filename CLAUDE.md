# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an ACM/ICPC competitive programming template repository containing a comprehensive LaTeX document with algorithm implementations and reference materials. The repository serves as a competitive programming reference book that can be compiled into a PDF for contests.

## Core Files

- `Algorithm-template.tex` - Main LaTeX template file containing all algorithm implementations and competitive programming references
- Generated files: `.aux`, `.bbl`, `.log`, `.out`, `.pdf`, `.synctex.gz`, `.toc` - LaTeX compilation artifacts
- Reference PDFs: Various external algorithm reference materials in Chinese

## LaTeX Structure

The main template is organized into the following sections:
- 数据结构 (Data Structures) - ST tables, segment trees, etc.
- 树 (Trees) - Tree algorithms and data structures  
- 图论 (Graph Theory) - Graph algorithms
- 字符串 (Strings) - String algorithms
- 动态规划 (Dynamic Programming) - DP algorithms
- 数论 (Number Theory) - Mathematical algorithms
- 线性代数 (Linear Algebra) - Matrix operations
- 杂项 (Miscellaneous) - Other algorithms

## Common Commands

### Compile LaTeX
```bash
pdflatex Algorithm-template.tex
```

### Full compilation with bibliography
```bash
pdflatex Algorithm-template.tex
bibtex Algorithm-template
pdflatex Algorithm-template.tex  
pdflatex Algorithm-template.tex
```

### Clean generated files
```bash
rm -f *.aux *.bbl *.log *.out *.synctex.gz *.toc
```

## Template Configuration

The LaTeX template uses:
- `ctexart` document class for Chinese language support
- A4 paper with custom margins optimized for competitive programming
- Two-column layout in code sections
- Custom code highlighting for C++ with specific color scheme
- Header shows "Callmeplayxcpc", "scutsky's template", and page numbers

## Code Style

- All algorithm implementations are in C++
- Code blocks use custom `cpp` style with syntax highlighting  
- Comments and variable names may be in Chinese
- Focus on competitive programming efficiency over production code standards