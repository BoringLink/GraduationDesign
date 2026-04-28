# AGENTS.md（oh-my-openagents 统一规则）

**Scope:** Repository root  
**适用对象:** OpenCode + oh-my-openagents  
**主任务:** 毕业论文写作与论文相关验证

## 1) 项目定位

- 本仓库以论文工程为主，主要工作域是 `latex/thesis/`。
- `CodingPlatformBak/` 是论文对应代码仓库，默认仅用于阅读实现、运行开发与测试，不做代码改写。
- 仅在用户明确要求“修改代码”时，才允许对 `CodingPlatformBak/**` 进行最小必要变更。

## 2) 论文环境与工具（必须优先遵循）

- 操作系统与硬件：`macOS (M1 Pro)`
- TeX 发行版：`MacTeX`
- 编译链路：`XeLaTeX` + `latexmk`
- 文献管理：`BibDesk`
- 文献检索：`ArXiv`、`Semantic Scholar`（本地配置：`.env.semantic-scholar.local`）
- 论文优化：`thesis-optimizer`（AI检测优化、查重优化、学术润色）

## 3) 论文编译与清理（以实际文件为准）

- 以 `latex/thesis/README.md` 为准
- 在 `latex/thesis` 目录执行：
  - 编译：`latexmk -xelatex -interaction=nonstopmode -file-line-error -outdir=build main.tex`
  - 清理：`latexmk -c -outdir=build main.tex`
  - 彻底清理：`latexmk -C -outdir=build main.tex`
- 编译行为与输出目录配置由 `latex/thesis/latexmkrc` 约束。

## 4) 论文写作规范

- 论文排版严格对齐 `理工类专业毕业论文模板（更新）.doc`。
- 学术图优先使用 TikZ。
- 图片题注位于图片下方居中；表格题注位于表格上方居中；均使用 LaTeX 自动编号。
- 参考文献必须规范引用，且正文内容需真实对应被引文献。

## 5) 代码仓使用边界（CodingPlatformBak）

- 允许：阅读代码、定位实现、运行 `dev/build/test/lint`、回传结果。
- 禁止（默认）：新增功能、重构、依赖升级、批量风格改写、目录结构调整。
- 如用户明确要求改代码：仅改必要文件，并保持与子目录 `AGENTS.md` 约定一致。

## 6) 多层规则解析

- 多域仓库按“最近规则优先”：编辑哪个路径，就读取该路径最近的 `AGENTS.md`。
- 若根规则与子目录规则冲突，子目录规则优先。
- 不要修改生成物或依赖目录：`node_modules`、`.venv`、`build`、`__pycache__`。
