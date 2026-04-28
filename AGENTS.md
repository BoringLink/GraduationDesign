# PROJECT KNOWLEDGE BASE

**Generated:** 2026-04-25 (Asia/Shanghai)
**Updated:** Toolchain configuration added
**Scope:** Repository root

## OVERVIEW

This repository contains a graduation thesis (LaTeX) and a backup coding platform project (Nuxt + FastAPI). Thesis writing uses the tools specified below.

---

## 论文工具链配置 (THESIS TOOLCHAIN)

### 编译环境

- **Platform:** macOS (M1 Pro) with MacTeX installed
- **编译入口:** `@latex/thesis/build.sh` (强制使用，不可绕过)
- **编译引擎:** XeLaTeX via latexmk

### 文献管理

- **文献管理工具:** BibDesk (macOS)
- **API配置:** `@.env.semantic-scholar.local` (Semantic Scholar API Key已配置)
- **文献检索技能:** 使用 `@.agent/skills/literature-search/` 技能调用ArXiv和Semantic Scholar API

### 论文优化

- **优化技能:** 使用 `@.agent/skills/thesis-optimizer/` 进行AI检测优化、查重优化、学术润色

### 论文模板

- **模板文件:** `@理工类专业毕业论文模板（更新）.doc`
- **强制要求:** 论文编排必须严格对齐模板格式

### 插图规范

- **学术图生成:** 使用TikZ绘制图表
- **图片题注:** 在图片**下方居中**，使用LaTeX自动编号
- **表格题注:** 在表格**上方居中**，使用LaTeX自动编号

### 参考文献引用规范

- 必须有规范的参考文献引用标注
- 引用处必须真实使用了参考文献内容
- 通过检索确认引用的参考文献确实被使用

---

## 项目结构

```text
毕业设计/
├── latex/thesis/                 # Main thesis source and compile scripts
├── CodingPlatformBak/backend/    # FastAPI backend
├── CodingPlatformBak/frontend/   # Nuxt 3 frontend
├── .opencode/                    # Agent runtime dependencies (do not modify casually)
└── 毕业设计任务书|开题报告|PPT/...   # Supporting documents
```

## WHERE TO LOOK

| Task                       | Location                                                    | Notes                                      |
| -------------------------- | ----------------------------------------------------------- | ------------------------------------------ |
| Thesis compile pipeline    | `latex/thesis/build.sh`                                     | Canonical compile entrypoint               |
| Thesis markdown conversion | `latex/thesis/scripts/convert-draft.sh`                     | Splits draft into abstract/body/backmatter |
| Backend entrypoint         | `CodingPlatformBak/backend/main.py`                         | FastAPI app + uvicorn runtime              |
| Backend tests              | `CodingPlatformBak/backend/tests/`                          | `pytest.ini` defines discovery             |
| Frontend scripts/config    | `CodingPlatformBak/frontend/package.json`, `nuxt.config.ts` | Nuxt build/dev/lint                        |

## CONVENTIONS

- **Mandatory thesis compile rule:** Always compile via `@latex/thesis/build.sh`.
- Frontend formatting preference is encoded in Nuxt ESLint stylistic config: tabs + semicolons.
- Backend tests use pytest naming (`test_*.py`, `test_*`) and `-v --tb=short` defaults.

## ANTI-PATTERNS (THIS PROJECT)

- Do **not** invoke ad-hoc thesis compile commands from root (e.g., direct `latexmk` one-liners) when `@latex/thesis/build.sh` exists.
- Do **not** treat generated/dependency directories as source (`node_modules`, `.venv`, `build`, `__pycache__`).
- Do **not** duplicate root instructions inside child AGENTS files unless the child changes behavior.

## COMMANDS

```bash
# Thesis (canonical)
@latex/thesis/build.sh

# Thesis draft conversion (optional before compile)
zsh "latex/thesis/scripts/convert-draft.sh"
```

## NOTES

- This repo is multi-domain; choose the nearest AGENTS.md in the path you are editing.
- If root and child rules conflict, child path-specific rules win.
- Frontend/backend executable commands are defined in `CodingPlatformBak/**/AGENTS.md` to avoid CWD ambiguity.
