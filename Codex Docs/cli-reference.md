# Codex CLI 命令参考

## 基本语法

```bash
codex [OPTIONS] [COMMAND]
```

## 全局选项

| 选项 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--config <PATH>` | `-c` | 指定配置文件 | `codex -c model=gpt-5.4` |
| `--model <MODEL>` | `-m` | 覆盖默认模型 | `codex -m o4` |
| `--sandbox` | - | 启用沙盒模式 | `codex --sandbox` |
| `--search` | - | 启用代码搜索 | `codex --search` |
| `--remote` | - | 启用远程执行 | `codex --remote` |
| `--version` | `-v` | 显示版本 | `codex --version` |
| `--help` | `-h` | 显示帮助 | `codex --help` |

## 交互式命令

### 启动会话

```bash
codex
```

### 指定目录启动

```bash
codex <directory>
codex .
```

## 配置覆盖 (CLI 级)

```bash
# 单个配置项
codex -c model=gpt-5.4

# 多个配置项
codex -c model=gpt-5.4 -c sandbox_mode=workspace-write

# 日志目录
codex -c log_dir=./.codex-log
```

## 子命令

| 命令 | 说明 |
|------|------|
| `codex init` | 初始化当前目录的 Codex 配置 |
| `codex config` | 打开配置文件编辑器 |
| `codex model list` | 列出可用模型 |
| `codex model set <name>` | 设置默认模型 |
| `codex session new` | 创建新会话 |
| `codex session list` | 列出会话历史 |
| `codex session resume <id>` | 恢复指定会话 |
| `codex log` | 查看日志 |
| `codex update` | 检查并更新 |

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | OpenAI API Key |
| `OPENAI_BASE_URL` | 自定义 API 端点 |
| `CODEX_CONFIG_PATH` | 配置文件路径 |

---

**参考链接**:
- [CLI Reference](https://developers.openai.com/codex/cli/reference)
- [Config Basics](https://developers.openai.com/codex/config-basic)