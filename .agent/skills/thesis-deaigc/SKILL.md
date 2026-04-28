---
name: thesis-deaigc
description: |
  (Project - Skill) 论文全篇优化编排器（短名：thesis-deaigc）。用于处理长篇学位论文的章节一致性、术语统一、语气校准与修改报告生成。
  当用户提到“整篇论文降AIGC痕迹/去AI味/全篇重写优化/文献综述太像AI/需要按章节汇报进度/要输出修改报告/分工给Agent Team做完整闭环”时，应优先使用本 Skill。
  Use for global thesis rewriting, anti-template academic polishing, reducing AI-generated patterns ("去AI味/降AIGC"), and chapter-by-chapter style normalization with strict ethical guardrails.
---

# Thesis DeAIGC

## Purpose

Use this skill to process **full-length academic theses** (10k+ words) with a global, chapter-aware workflow.
The goal is to improve human-like academic expression, reduce repetitive template patterns, and preserve argument rigor.

This skill **does not** support academic fraud. It must preserve logic, keep citations honest, and mark unverifiable additions for user validation.

## Trigger Conditions

Apply this skill when the user asks for one or more of the following:

- Full-thesis rewriting or style unification (not single-paragraph proofreading)
- “去AI味 / 降AIGC痕迹 / 全篇降噪 / 全文统一语气”
- Chapter-by-chapter optimization with progress reporting
- A final “修改报告 / rewrite report / change log”
- Cross-chapter term consistency or transition sentence stitching

If request is only local typo fixing, use normal editing flow instead.

## Interaction Protocol

At initialization, **verify** the following 3 parameters.
Ask the user **only for missing information** (do not re-ask if already provided):

1. 您的论文所属学科是什么（如应用经济学、机械自动化、计算机视觉）？
2. 学校或学院是否指定检测/查重系统（如知网、维普、源文鉴）与格式规范（如 GB/T 7714）？
3. 是否允许我对“示例数据/案例”仅给出占位建议并统一标注“[需由用户核实真实性]”？

Then confirm scope:

- Input format(s): `.tex`, `.docx`, `.md`
- Chapter boundaries and priorities
- Deadline and preferred reporting cadence

## Global Processing Pipeline

### Phase 1 — Scan & Model (全局扫描与特征建模)

1. Build a chapter map (intro, literature review, methods, experiments, conclusion, etc.).
2. Extract and lock a core terminology glossary to prevent cross-chapter drift.
3. Diagnose high-risk “AI-like pattern zones”:
   - repetitive discourse markers
   - overly symmetric sentence cadence
   - low lexical burstiness
   - repetitive summary-first paragraph openings
4. Produce a risk heatmap by chapter.

For very long documents, scan iteratively (chapter-by-chapter or by offsets/windows).
Do not assume the full thesis can be loaded into context in a single pass.

### Phase 2 — Segmented Execution (结构化分片执行)

Process by block with different rewrite weights:

- 引言/背景：提升问题动机与场景锚定
- 文献综述：增强对比关系与批判性视角
- 方法/实验：增加步骤颗粒度与观察性叙述
- 结论/建议：强化边界条件、局限性与后续方向

Execution constraints for long-form files:

- Read and rewrite iteratively (chapter by chapter / section by section).
- Persist intermediate outputs and continue from last completed section.
- Do not attempt to output a full 10k+ word thesis in one response; provide staged outputs and final assembly instructions.
- When editing `.tex`, preserve macros, labels, citations, environments, and compile-critical syntax.

### Phase 3 — Logic Splicing (跨章节逻辑缝合)

1. Add transition anchors at chapter openings and endings.
2. Ensure claims in later chapters reference definitions established earlier.
3. Calibrate authorial tone globally (consistent academic voice from Chapter 1 to acknowledgements).

### Phase 4 — Final Audit (格式与规范自动化)

1. Restore citation and bibliography format (default GB/T 7714 unless user-specified).
2. Validate terminology consistency and abbreviation expansions.
3. Emit final deliverables:
   - rewritten thesis text
   - 《降噪修改报告》 with chapter-level strategy trace

## Agent Team Execution Blueprint (整篇论文直达闭环)

When task scope is full-thesis, orchestrate an Agent Team instead of single-agent sequential editing.

### Team Roles

1. **Lead Orchestrator (总控代理)**
   - Owns chapter planning, task dispatch, merge order, and final acceptance gate.
   - Maintains a master tracker: chapter status, risk list, unresolved questions.

2. **Chapter Optimizers (章节优化代理，2-6个并行)**
   - Each agent handles assigned chapters end-to-end using `[L/S/C/T]` strategies.
   - Must preserve thesis claims, formulas, citations, and terminology glossary.

3. **Consistency Reviewer (一致性审校代理)**
   - Verifies cross-chapter term consistency, symbol consistency, and argument continuity.
   - Enforces transition anchors between adjacent chapters.

4. **Citation & Format Reviewer (格式与引用代理)**
   - Checks citation rendering and bibliography style (GB/T 7714 or user-required standard).
   - Ensures no reference is dropped, malformed, or fabricated.

5. **Final Integrator (总装代理)**
   - Merges all revised chapters, resolves merge conflicts, generates final report package.

### Orchestration Protocol

1. **Plan**: split thesis into chapter-level work units with clear acceptance criteria.
2. **Dispatch**: run chapter optimizers in parallel for independent chapters.
3. **Merge**: integrate chapter outputs into a unified draft.
4. **Review**: run consistency + format reviewers on merged draft.
5. **Repair Loop**: return failed chapters to chapter optimizer with explicit defect list.
6. **Finalize**: produce final thesis + 《降噪修改报告》 + verification checklist.

### Mandatory Artifacts per Chapter

- `chapter_output`: revised chapter content
- `change_log`: what changed and why (with strategy tags)
- `risk_notes`: unresolved factual/citation risks
- `handoff_note`: constraints for downstream merger/reviewer

### Team Completion Criteria (Definition of Done)

- All chapters reach `Completed` state.
- Cross-chapter terminology conflicts = 0 unresolved.
- Citation/format checks pass against target spec.
- Final report includes strategy trace and user verification checklist.
- Any synthetic data/case remains explicitly marked ` [需由用户核实真实性] `.

## Integrated Methodologies (20)

### Language-level
- **[L-1] 语法熵增**: vary clause structure, insertion, inversion, mixed sentence lengths
- **[L-2] 语态对冲**: non-linear active/passive alternation where semantically valid
- **[L-3] 词汇升阶**: replace generic wording with domain-precise terminology
- **[L-4] 学术连接词重配**: diversify connectors beyond fixed templates
- **[L-5] 语义微偏移**: adjust non-core modifiers to reduce repetitive probability peaks

### Structure-level
- **[S-1] 逻辑逆转叙述**: occasionally derive method from conclusion-backtracking narrative
- **[S-2] 深度批判**: add limitations and conflict points when summarizing prior work
- **[S-3] 逻辑细分**: expand single claims into layered reasoning (assumption → mechanism → implication)
- **[S-4] 异常锚定**: allow bounded, human-like insight jumps with explicit rationale
- **[S-5] 长程关联**: deliberately reference earlier chapters to maintain chain-of-thought continuity

### Content-level
- **[C-1] 场景耦合**: tie arguments to recent domain developments when relevant
- **[C-2] 局部数据化**: convert vague claims into quantifiable placeholders when evidence exists
- **[C-3] 实证介入感**: add observation-oriented narration where methodologically reasonable
- **[C-4] 文献对峙结构**: represent multi-source disagreement and justified stance
- **[C-5] 案例颗粒化**: attach micro-level examples to abstract principles

### Tuning-level
- **[T-1] 多表述路径改写**: rephrase through alternative semantic pathways to avoid templating
- **[T-2] 标点节奏重调**: optimize punctuation rhythm for academic readability
- **[T-3] 去模版化**: remove rigid sequence templates (“首先/其次/最后” overuse)
- **[T-4] 引用重塑**: transform direct quotation into analytical paraphrase with source fidelity
- **[T-5] 非完美润色**: preserve moderate human texture, avoid over-sterilized prose

## Progress Feedback Format

During long runs, provide chapter-based updates like:

> 正在处理第二章（文献综述），已应用 [L-3] 词汇升阶 + [C-4] 文献对峙结构，当前完成度 62%。下一步将进行跨段落逻辑缝合与引用重塑。

## Output Contract

Always return:

1. **Optimized Thesis Body** (full or chapter-delimited)
2. **《降噪修改报告》** containing:
   - changed sections and why
   - strategies used (`[L-*]/[S-*]/[C-*]/[T-*]`)
   - risk notes and unresolved items
   - user verification checklist

Report template:

```markdown
# 降噪修改报告
## 1. 任务范围与输入约束
## 2. 章节处理摘要
## 3. 关键改写点（含策略标签）
## 4. 一致性与格式修复结果
## 5. 风险与人工复核清单
```

## Constraints & Ethics

- Never alter core claims into different conclusions.
- Never invent citations or unverifiable factual claims.
- Any synthetic example/data must be explicitly marked:
  **[需由用户核实真实性]**
- Keep optimization transparent: user can inspect why each major rewrite occurred.
- If user requests deceptive or fraudulent rewriting, refuse that part and continue with compliant academic-quality editing.
