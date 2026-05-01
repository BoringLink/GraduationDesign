# LaTeX 论文工程

本目录为毕业论文的最小可维护 LaTeX 源码工程。

## 环境与工具

- 平台：`macOS`
- TeX 发行版：`MacTeX`
- 编译引擎：`XeLaTeX`（通过 `latexmk` 调用）
- 推荐编辑器：VS Code + `LaTeX Workshop`

## 目录结构

- `main.tex`：论文主入口
- `metadata.tex`：封面元数据与基本信息
- `chapters/`：论文章节（摘要、正文、参考文献/附录）
- `styles/`：学校模板样式与封面定义
- `figures/`：论文插图资源
- `references.bib`：BibDesk 管理的参考文献数据库
- `latexmkrc`：编译配置（输出到 `build/`）

## 编译与清理

在 `latex/thesis` 目录执行：

```bash
latexmk -xelatex -interaction=nonstopmode -file-line-error -outdir=build main.tex
```

清理中间文件：

```bash
latexmk -c -outdir=build main.tex
```

彻底清理（含 PDF）：

```bash
latexmk -C -outdir=build main.tex
```

## BibDesk 文献管理

- 使用 BibDesk 打开 `references.bib`，统一维护所有参考文献条目。
- 正文中使用 `\cite{key}` 引用，`key` 与 BibDesk 条目键一致。
- 参考文献页在 `chapters/backmatter.tex` 中通过 `\bibliography{references}` 自动生成，不再手写条目列表。
