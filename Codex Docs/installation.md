# Codex CLI 安装指南

## 系统要求

- **macOS**: 10.15+
- **Linux**: Ubuntu 20.04+ / Debian 11+
- **Windows**: WSL2 (推荐) 或 PowerShell

## 安装方式

### 方式一: npm (跨平台)

```bash
npm install -g @openai/codex
```

### 方式二: Homebrew (macOS/Linux)

```bash
brew install --cask codex
```

### 方式三: 直接下载

从 GitHub Releases 下载预编译的二进制文件:
- https://github.com/openai/codex/releases

## 验证安装

```bash
codex --version
```

## 首次运行与登录

```bash
codex
```

首次运行时会提示选择登录方式:
1. **ChatGPT 账号登录** - 使用 chatgpt.com 账号
2. **API Key 登录** - 使用 OpenAI API Key

### 使用 API Key

```bash
export OPENAI_API_KEY="sk-..."
```

或通过配置指定:

```toml
# ~/.codex/config.toml
api_key = "sk-..."
```

## 卸载

```bash
# npm
npm uninstall -g @openai/codex

# Homebrew
brew uninstall codex
```

---

**参考链接**:
- [官方 Quickstart](https://developers.openai.com/codex/quickstart?setup=cli)
- [GitHub README](https://github.com/openai/codex/blob/main/README.md)