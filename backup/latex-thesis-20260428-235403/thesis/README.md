# LaTeX 论文工程

本目录用于在本项目下持续编写和编译毕业论文。

## 工具链

- `MacTeX`
- `xelatex`
- `latexmk`
- `pandoc`
- VS Code + `LaTeX Workshop`

## 目录说明

- `main.tex`：主入口
- `metadata.tex`：封面元数据
- `styles/`：样式与封面
- `chapters/draft.tex`：完整转换稿
- `chapters/abstract.tex`：摘要与英文摘要
- `chapters/body.tex`：正文
- `chapters/backmatter.tex`：参考文献、致谢、附录
- `build/`：编译产物

## 编译

```bash
cd "/Users/tk/Documents/杭州电子科技大学/毕业设计/latex/thesis"
./scripts/convert-draft.sh
/Library/TeX/texbin/latexmk -xelatex -interaction=nonstopmode -file-line-error -outdir=build main.tex
```

## 说明

- 当前版式以“可稳定编译、便于继续写作”为优先，尽量贴近学校 Word 模板。
- Mermaid 图已预留为 LaTeX 图占位，后续可替换为正式图片或 TikZ 图。
- 当前项目默认使用 `latexmk + xelatex`，这是安装 `MacTeX` 后更标准的本地工作流。
