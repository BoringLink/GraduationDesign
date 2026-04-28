# OpenAI Codex CLI 文档参考 (2026)

本文档整理 OpenAI Codex CLI 的官方操作命令、参数配置及使用示例。

## 目录结构

- [安装与快速开始](./installation.md)
- [CLI 命令参考](./cli-reference.md)
- [配置与参数](./configuration.md)
- [Slash 命令](./slash-commands.md)
- [官方资源链接](./resources.md)

---

## 核心命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `codex` | 启动交互式会话 | `codex` |
| `codex -c <key=value>` | 覆盖配置项 | `codex -c model=gpt-5.4` |
| `codex -m <model>` | 覆盖默认模型 | `codex -m o4` |
| `codex --config <path>` | 指定配置文件 | `codex --config ./config.toml` |
| `/model` | 在会话中切换模型 | 输入 `/model` 后选择 |
| `/status` | 查看当前状态 | 输入 `/status` |
| `/permissions` | 管理权限设置 | 输入 `/permissions` |

---

## 文档来源

- 官方文档: https://developers.openai.com/codex
- GitHub 仓库: https://github.com/openai/codex
- 快速开始: https://developers.openai.com/codex/quickstart?setup=cli
- CLI 参考: https://developers.openai.com/codex/cli/reference
- Slash 命令: https://developers.openai.com/codex/guides/slash-commands/
- 配置基础: https://developers.openai.com/codex/config-basic