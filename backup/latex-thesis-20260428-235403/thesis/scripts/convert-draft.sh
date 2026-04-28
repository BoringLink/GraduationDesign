#!/bin/zsh
set -euo pipefail

ROOT="/Users/tk/Documents/杭州电子科技大学/毕业设计"
INPUT="${1:-$ROOT/毕业论文-Markdown初稿.md}"
OUTPUT="${2:-$ROOT/latex/thesis/chapters/draft.tex}"
TMP_MD="$(mktemp /tmp/hdu-thesis-md.XXXXXX.md)"
ABSTRACT_OUT="$ROOT/latex/thesis/chapters/abstract.tex"
BODY_OUT="$ROOT/latex/thesis/chapters/body.tex"
BACKMATTER_OUT="$ROOT/latex/thesis/chapters/backmatter.tex"

awk '
BEGIN {
  in_mermaid = 0
  pending_caption = 0
  skipping_note = 0
}
NR == 1 && /^# / {
  next
}
NR == 3 && /^> / {
  skipping_note = 1
}
skipping_note {
  if ($0 ~ /^[[:space:]]*$/) {
    skipping_note = 0
  }
  next
}
in_mermaid {
  if ($0 ~ /^```[[:space:]]*$/) {
    in_mermaid = 0
    pending_caption = 1
    next
  }
  next
}
pending_caption {
  if ($0 ~ /^图[0-9-]+[[:space:]]+/) {
    caption = $0
    sub(/^图[0-9-]+[[:space:]]+/, "", caption)
    print "```{=latex}"
    print "\\mermaidplaceholder{" caption "}{原始 Mermaid 图请参考 Markdown 初稿。}"
    print "```"
    pending_caption = 0
    next
  }
  if ($0 ~ /^[[:space:]]*$/) {
    next
  }
  print "```{=latex}"
  print "\\mermaidplaceholder{Mermaid 图占位}{原始 Mermaid 图请参考 Markdown 初稿。}"
  print "```"
  pending_caption = 0
}
/^```mermaid[[:space:]]*$/ {
  in_mermaid = 1
  next
}
/^---[[:space:]]*$/ {
  next
}
{
  if ($0 ~ /^### /) {
    sub(/^### /, "## ", $0)
  } else if ($0 ~ /^## /) {
    sub(/^## /, "# ", $0)
  }
  if ($0 ~ /^# [0-9]+[[:space:]]+/) {
    sub(/^# [0-9]+[[:space:]]+/, "# ", $0)
  } else if ($0 ~ /^## [0-9]+(\.[0-9]+)*[[:space:]]+/) {
    sub(/^## [0-9]+(\.[0-9]+)*[[:space:]]+/, "## ", $0)
  } else if ($0 ~ /^### [0-9]+(\.[0-9]+)*[[:space:]]+/) {
    sub(/^### [0-9]+(\.[0-9]+)*[[:space:]]+/, "### ", $0)
  }
  print
}
END {
  if (pending_caption) {
    print "```{=latex}"
    print "\\mermaidplaceholder{Mermaid 图占位}{原始 Mermaid 图请参考 Markdown 初稿。}"
    print "```"
  }
}
' "$INPUT" > "$TMP_MD"

pandoc \
  --from markdown \
  --to latex \
  --wrap=none \
  --top-level-division=chapter \
  "$TMP_MD" \
  -o "$OUTPUT"

perl -0pi -e 's/\\chapter\{摘要\}/\\chapter*{摘要}\\addcontentsline{toc}{chapter}{摘要}/g;' "$OUTPUT"
perl -0pi -e 's/\\chapter\{ABSTRACT\}/\\chapter*{ABSTRACT}\\addcontentsline{toc}{chapter}{ABSTRACT}/g;' "$OUTPUT"
perl -0pi -e 's/\\chapter\{参考文献\}/\\chapter*{参考文献}\\addcontentsline{toc}{chapter}{参考文献}/g;' "$OUTPUT"
perl -0pi -e 's/\\chapter\{致谢\}/\\chapter*{致谢}\\addcontentsline{toc}{chapter}{致谢}/g;' "$OUTPUT"
perl -0pi -e 's/\\chapter\{附录\}/\\appendix\\chapter{附录}/g;' "$OUTPUT"
perl -0pi -e 's/\\chapter\{([0-9]+[[:space:]]+[^}]+)\}/\\chapter{$1}/g;' "$OUTPUT"
perl -0pi -e 'BEGIN{$root="% !TeX root = ../main.tex\n\n";} $_=$root.$_ unless /^\Q$root\E/s;' "$OUTPUT"
perl -0pi -e 's/\{\\def\\LTcaptype\{none\}\s*% do not increment counter\s*(\\begin\{longtable\}\[\]\{.*?\\end\{longtable\})\s*\}/$1/gs;' "$OUTPUT"

perl -0ne '
  if (/(.*?)(\\chapter\{引言\}.*?)(\\chapter\*\{参考文献\}.*)/s) {
    print $1;
  } else {
    die "Failed to split abstract section\n";
  }
' "$OUTPUT" > "$ABSTRACT_OUT"

perl -0ne '
  if (/(.*?)(\\chapter\{引言\}.*?)(\\chapter\*\{参考文献\}.*)/s) {
    print $2;
  } else {
    die "Failed to split body section\n";
  }
' "$OUTPUT" > "$BODY_OUT"

perl -0ne '
  if (/(.*?)(\\chapter\{引言\}.*?)(\\chapter\*\{参考文献\}.*)/s) {
    print $3;
  } else {
    die "Failed to split backmatter section\n";
  }
' "$OUTPUT" > "$BACKMATTER_OUT"

rm -f "$TMP_MD"
echo "Converted to $OUTPUT"
