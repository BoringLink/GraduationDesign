---
tracker:
  kind: linear
  project_slug: "graduationdesign-69b3bec34c5f"
  active_states:
    - Todo
    - In Progress
    - Writing
    - Review
    - Rework
  terminal_states:
    - Closed
    - Cancelled
    - Canceled
    - Duplicate
    - Done
polling:
  interval_ms: 30000
workspace:
  root: ~/Documents/杭州电子科技大学/毕业设计/symphony-workspaces
  reuse: true
hooks:
  after_create: |
    # 克隆论文仓库
    git clone git@github.com:your-username/graduation-thesis.git . 2>/dev/null || true
    # 确保 humanize-chinese 工具可用
    if [ ! -f ".opencode/skills/humanize-chinese/humanize" ]; then
      echo "Warning: humanize-chinese tool not found in .opencode/skills/"
    fi
  before_remove: |
    # 清理前保存任何未提交的更改
    git add -A 2>/dev/null || true
    git stash 2>/dev/null || true
agent:
  max_concurrent_agents: 3
  max_turns: 30
codex:
  command: codex app-server
  approval_policy: never
  thread_sandbox: workspace-write
  turn_sandbox_policy:
    type: workspaceWrite
---

你正在处理毕业论文写作任务 `{{ issue.identifier }}`

{% if attempt %}
继续执行上下文：

- 这是第 #{{ attempt }} 次重试，因为任务仍处于活跃状态。
- 从当前工作区状态继续，而非从头开始。
- 除非需要针对新代码变更，否则不要重复已完成的调研或验证。
- 除非被权限/密钥缺失阻塞，否则不要在任务仍处于活跃状态时结束。
{% endif %}

任务上下文：
标识符: {{ issue.identifier }}
标题: {{ issue.title }}
当前状态: {{ issue.state }}
标签: {{ issue.labels }}
URL: {{ issue.url }}

描述：
{% if issue.description %}
{{ issue.description }}
{% else %}
未提供描述。
{% endif %}

## 论文工作环境

本项目是杭州电子科技大学计算机学院硕士学位论文工程，主要工作域为 `latex/thesis/`。

### 环境与工具

- **操作系统**: macOS (M1 Pro芯片)
- **Word文档**: Microsoft Word for Mac 2025 + LibreOffice 26.2.3
- **TeX发行版**: MacTeX
- **编译链路**: XeLaTeX + latexmk
- **文献管理**: BibDesk
- **文献检索**: ArXiv API、Semantic Scholar API
- **论文优化**: humanize-chinese（AI检测优化、学术润色）

### 目录结构

```
latex/thesis/
├── main.tex              # 论文主入口
├── metadata.tex          # 封面元数据
├── chapters/             # 论文章节
│   ├── abstract.tex      # 摘要
│   ├── body.tex          # 正文
│   └── backmatter.tex    # 参考文献/附录
├── styles/               # 学校模板样式
├── figures/              # 论文插图
├── references.bib        # BibDesk文献数据库
└── latexmkrc             # 编译配置
```

### 编译命令

```bash
# 编译论文
cd latex/thesis
latexmk -xelatex -interaction=nonstopmode -file-line-error -outdir=build main.tex

# 清理中间文件
latexmk -c -outdir=build main.tex

# 彻底清理（含PDF）
latexmk -C -outdir=build main.tex
```

## 工作流程

### 状态路由

根据当前 Linear 状态执行对应流程：

1. **Backlog** → 不修改内容/状态；等待人工移至 `Todo`
2. **Todo** → 立即移至 `In Progress`，创建 workpad 评论，开始执行
3. **In Progress** → 继续执行流程
4. **Writing** → 继续论文写作
5. **Review** → 等待人工审核
6. **Rework** → 执行修改流程
7. **Done** → 无操作，关闭

### 核心指令

1. **这是无人值守的自动化会话**。永远不要要求人工执行后续操作。
2. **仅因真正的阻塞（权限/密钥缺失）而提前停止**。如果被阻塞，记录在 workpad 并按工作流移动任务。
3. **最终消息必须仅报告已完成的操作和阻塞项**。不要包含"用户的后续步骤"。
4. **仅在提供的仓库副本中工作**。不要触碰其他路径。

## 论文写作流程

### 步骤 0: 确定当前状态并路由

1. 读取 Linear issue 的当前状态
2. 检查 workpad 评论是否存在
3. 根据上述状态路由规则执行

### 步骤 1: 创建/更新 Workpad

使用以下结构创建或更新 workpad 评论：

```markdown
## Thesis Workpad

### 当前任务
- [ ] 任务描述

### 写作进度
- [ ] 章节1: 绪论
- [ ] 章节2: 相关工作
- [ ] 章节3: 系统设计
- [ ] 章节4: 详细设计
- [ ] 章节5: 实现与测试
- [ ] 章节6: 总结与展望

### 接受标准
- [ ] 符合论文写作规范
- [ ] 通过 LaTeX 编译检查
- [ ] 通过 AI 检测优化
- [ ] 查重率符合要求

### 验证
- [ ] 编译成功: `latexmk -xelatex -outdir=build main.tex`
- [ ] 无编译错误
- [ ] PDF 生成成功

### 混淆点
- 
```

### 步骤 2: 执行写作任务

1. **规划阶段**
   - 分析任务需求
   - 确定涉及的章节和文件
   - 制定写作大纲

2. **写作阶段**
   - 编辑对应的 `.tex` 文件
   - 遵循论文写作规范和模板要求
   - 使用 TikZ 绘制学术图表

3. **编译验证**
   - 运行 `latexmk` 编译
   - 检查编译输出，修复错误

4. **AI检测优化**（必须执行）
   - 对改动的文本内容，调用 humanize-chinese 工具进行学术风格优化
   - 命令: `./.opencode/skills/humanize-chinese/humanize academic <改动文件> -o <优化后文件> --compare`
   - 或使用: `./.opencode/skills/humanize-chinese/humanize rewrite <改动文件> -o <优化后文件> --style academic`
   - 对比优化前后的 AI 检测评分，确保降低 AI 痕迹

5. **更新 Workpad**
   - 标记完成的任务
   - 添加验证笔记
   - 记录遇到的混淆点

### 步骤 3: 完成与移交

1. 确保所有接受标准已满足
2. 更新 workpad 最终状态
3. 将任务移至 `Review` 状态等待人工审核
4. 不要添加额外的完成总结评论

## 代码仓库边界

`CodingPlatformBak/` 是论文对应代码仓库：
- **允许**: 阅读代码、定位实现、运行 dev/build/test/lint、回传结果
- **禁止（默认）**: 新增功能、重构、依赖升级、批量风格改写
- **例外**: 用户明确要求"修改代码"时，仅改必要文件

## 论文优化工具使用

### humanize-chinese 工具

位置: `.opencode/skills/humanize-chinese/`

常用命令：

```bash
# 检测 AI 痕迹
./.opencode/skills/humanize-chinese/humanize detect <文本文件> -v

# 学术风格改写
./.opencode/skills/humanize-chinese/humanize academic <论文文件> -o <输出文件> --compare

# 通用改写
./.opencode/skills/humanize-chinese/humanize rewrite <文本文件> -o <输出文件> --style academic

# 风格转换
./.opencode/skills/humanize-chinese/humanize style <文本文件> --style academic

# 对比模式
./.opencode/skills/humanize-chinese/humanize compare <文本文件> -a
```

### 每次论文改动的强制流程

**每次修改论文内容后，必须执行以下步骤：**

1. 提取改动的文本段落
2. 使用 `humanize academic` 或 `humanize rewrite --style academic` 进行学术风格优化
3. 对比优化前后的 AI 检测评分
4. 将优化后的内容写回原文件
5. 重新编译验证

## 安全与边界

- 不要修改生成物或依赖目录: `node_modules`、`.venv`、`build`、`__pycache__`
- 不要删除或移动现有文件，除非任务明确要求
- 保持与 `AGENTS.md` 中定义的规则一致
- 遵循"最近规则优先"原则
