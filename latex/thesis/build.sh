#!/bin/zsh
set -euo pipefail

DIR="/Users/tk/Documents/杭州电子科技大学/毕业设计/latex/thesis"
LATEXMK="/Library/TeX/texbin/latexmk"

cd "$DIR"

mkdir -p build
find build -mindepth 1 -maxdepth 1 -exec rm -rf {} +

/Users/tk/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
	"$DIR/scripts/create_hdu_docx_template.py"

"$LATEXMK" -xelatex -interaction=nonstopmode -file-line-error -outdir=build main.tex
"$LATEXMK" -xelatex -interaction=nonstopmode -file-line-error -outdir=build main-body.tex

/Users/tk/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
	"$DIR/scripts/export_docx_from_template.py"

echo "Built: build/main.pdf, build/main-body.pdf, build/main.docx"
