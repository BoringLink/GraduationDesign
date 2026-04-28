# Draft: oh-my-opencode config repair

## Requirements (confirmed)
- 修正 oh-my-opencode 配置中的无效模型：
  - Agent Prometheus - Plan Builder: `openai/gpt-5.2` 无效
  - Agent Atlas - Plan Executor: `github-copilot/claude-sonnet-4.6` 无效
  - Agent Sisyphus - Ultraworker: `openai/gpt-5.2` 无效

## Technical Decisions
- 配置主文件位于 `.opencode/oh-my-openagent.json`
- agent 配置集中在 `agents` 段，模型命名需要符合 oh-my-opencode 当前支持的 provider/model 格式

## Research Findings
- `.opencode/oh-my-openagent.json` 中：`prometheus`、`sisyphus` 仍指向 `openai/gpt-5.2`
- 同文件中 `oracle` 使用 `openai/gpt-4o`，`explore` 使用 `openai/gpt-4o-mini`
- `background_task.modelConcurrency` 也引用了 `openai/gpt-5.2`

## Open Questions
- `openai/gpt-5.2` 应替换为哪个当前有效模型？
- `github-copilot/claude-sonnet-4.6` 是否应改为同系列的有效 Claude/Copilot 模型，还是改为其他 provider？
- `background_task.modelConcurrency` 是否需要同步调整以匹配新模型名？

## Scope Boundaries
- INCLUDE: 修正配置文件中的无效模型映射与相关引用
- EXCLUDE: 改动业务代码、执行运行时行为变更
