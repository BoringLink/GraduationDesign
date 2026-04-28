# Codex CLI 配置与参数

## 配置文件位置

Codex 从多个位置读取配置，按优先级从高到低:

1. **命令行参数** (最高优先级)
2. **项目配置**: `./.codex/config.toml`
3. **用户配置**: `~/.codex/config.toml`
4. **系统配置**: `/etc/codex/config.toml`

## 配置文件格式

```toml
# ~/.codex/config.toml 或项目 .codex/config.toml
```

## 常用配置项

### API 与认证

```toml
api_key = "sk-..."
organization = "org-..."
base_url = "https://api.openai.com/v1"
```

### 模型设置

```toml
model = "gpt-5.4"
temperature = 0.7
max_tokens = 4096
```

### 沙盒与安全

```toml
sandbox_mode = "workspace-write"  # workspace-read | workspace-write | strict
allow_read = true
allow_write = true
allow_execute = false
execution_timeout = 300  # 秒
```

### 网络搜索

```toml
web_search = "cached"  # cached | live
search_depth = "medium"  # shallow | medium | deep
```

### 日志

```toml
log_level = "info"  # debug | info | warn | error
log_dir = "./.codex-logs"
```

### 文件处理

```toml
max_file_size = 1048576  # 1MB
ignored_files = [".git/*", "node_modules/*", "*.log"]
```

### 会话

```toml
auto_save = true
session_dir = "./.codex-sessions"
```

### 代理

```toml
http_proxy = "http://localhost:7890"
https_proxy = "http://localhost:7890"
no_proxy = "localhost,127.0.0.1"
```

## 示例配置

### 最小配置

```toml
api_key = "sk-your-api-key-here"
```

### 完整配置

```toml
# OpenAI API
api_key = "sk-your-api-key-here"
organization = "org-your-org-id"

# 模型
model = "gpt-5.4"
temperature = 0.7

# 安全
sandbox_mode = "workspace-write"
allow_execute = false
execution_timeout = 300

# 日志
log_level = "info"
log_dir = "./.codex-logs"

# 网络
web_search = "cached"
```

## 配置验证

```bash
codex config --validate
```

## 查看当前配置

```bash
codex config show
```

---

**参考链接**:
- [Config Basics](https://developers.openai.com/codex/config-basic)
- [CLI Reference](https://developers.openai.com/codex/cli/reference)