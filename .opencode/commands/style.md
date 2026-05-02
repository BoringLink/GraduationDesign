---
description: 中文风格转换（8 种风格：口语/知乎/小红书/公众号/学术/文艺/微博/小说）
subtask: true
---

# /style — 中文风格转换

将中文文本转换为特定写作风格。默认先跑 humanize 去 AI 词，再套风格。`--no-humanize` 可关闭预处理。

## 输入

用户通过 $ARGUMENTS 提供风格名和文本。

格式：`$ARGUMENTS` = `[风格名] [文本或文件路径]`

- 第一个参数 ($1) = 风格名
- 其余部分 = 文本内容或文件路径

## 可用风格

| 风格名 | 说明 |
|--------|------|
| `casual` | 口语化，日常聊天 |
| `zhihu` | 知乎风格，理性分析 |
| `xiaohongshu` | 小红书风格，活泼种草 |
| `wechat` | 公众号风格，深度长文 |
| `academic` | 学术风格，严谨论述 |
| `literary` | 文艺风格，优美散文 |
| `weibo` | 微博风格，简短犀利 |
| `novel` | 长篇叙事 (剔除 AI prompt artifact + markdown headers + dialogue 保护) |

## 步骤

1. 从 $ARGUMENTS 中解析出风格名和文本：
   - $1 = 风格名（如 xiaohongshu）
   - 其余 = 文本内容或文件路径

2. 判断文本是文件路径还是纯文本：
   - 如果是存在的文件路径 → 直接使用
   - 如果是纯文本 → 保存到临时文件：
     ```bash
     cat > /tmp/style_input.txt << 'STY_EOF'
     [文本内容]
     STY_EOF
     ```

3. 运行风格转换：
   ```bash
   .opencode/skills/humanize-chinese/humanize style INPUT_FILE --style $1 -o /tmp/style_output.txt
   ```
   加 `--no-humanize` 可跳过 humanize 预处理。

4. 展示转换后的文本给用户。

## 示例用法

```
/style xiaohongshu 在当今快节奏的生活中，时间管理具有至关重要的意义。
/style zhihu 论文.txt
/style novel 第三章.txt
```