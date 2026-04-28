# Codex CLI Slash 命令

在交互式会话中，可以使用 `/` 开头的命令来执行各种操作。

##通用命令

| 命令 | 说明 |
|------|------|
| `/help` | 显示帮助信息 |
| `/status` | 查看当前状态 |
| `/clear` | 清除当前会话 |

## 模型命令

| 命令 | 说明 |
|------|------|
| `/model` | 切换当前模型 |
| `/model list` | 列出可用模型 |
| `/model set <name>` | 设置默认模型 |

使用方式:
```
> /model
[选择模型] gpt-5.4 / o4 / o4-mini
> /model set gpt-5.4
```

## 会话命令

| 命令 | 说明 |
|------|------|
| `/session new` | 创建新会话 |
| `/session save` | 保存当前会话 |
| `/session list` | 列出历史会话 |
| `/session load <id>` | 加载指定会话 |

## 权限命令

| 命令 | 说明 |
|------|------|
| `/permissions` | 查看当前权限设置 |
| `/permissions add <scope>` | 添加权限 |
| `/permissions remove <scope>` | 移除权限 |

可用权限范围:
- `read` - 读取文件
- `write` - 写入文件
- `execute` - 执行命令
- `network` - 网络访问

## 文件操作命令

| 命令 | 说明 |
|------|------|
| `/read <file>` | 读取文件内容 |
| `/edit <file>` | 编辑文件 |
| `/diff` | 查看待应用的改动 |
| `/apply` | 应用改动 |
| `/reject` | 拒绝改动 |

## 操作命令

| 命令 | 说明 |
|------|------|
| `/run <command>` | 执行命令行 |
| `/test` | 运行测试 |
| `/search <query>` | 搜索代码 |
| `/git` | 执行 Git 操作 |

## 快捷键

| 快捷键 | 说明 |
|--------|------|
| `Ctrl+C` | 中断当前操作 |
| `Ctrl+D` | 退出会话 |
| `Ctrl+L` | 清除屏幕 |
| `Ctrl+P` | 上一个命令 |
| `Ctrl+N` | 下一个命令 |
| `Tab` | 自动补全 |

---

**参考链接**:
- [Slash Commands Guide](https://developers.openai.com/codex/guides/slash-commands/)
- [CLI Reference](https://developers.openai.com/codex/cli/reference)