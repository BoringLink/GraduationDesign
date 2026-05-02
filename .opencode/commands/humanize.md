---
description: 去除中文文本的 AI 痕迹（v5.0 改写 + 对比）
subtask: true
---

# /humanize — 去除中文文本的 AI 痕迹（v5.0）

改写中文文本以去除 AI 写作痕迹。流程：检测 → 改写（best-of-N）→ 对比验证。

v5.0 使用 **scene-aware LR humanize loss** (general / academic / longform 三路), **best-of-N humanize** (默认 N=10 取最低 LR), **165 替换模式**, **40+ paraphrase 模板**, **段落级反制** (paragraph length CV / 跨段 trigram 重复), 加 **CiLin 同义词词林** 38873 with collision blacklist。

## 输入

用户通过 $ARGUMENTS 提供中文文本（直接文本或文件路径）。

## 步骤

1. 判断输入是文件路径还是纯文本：
   - 如果 $ARGUMENTS 是一个存在的文件路径 → 直接使用
   - 如果 $ARGUMENTS 是纯文本 → 先保存到临时文件：
     ```bash
     cat > /tmp/humanize_input.txt << 'HUM_EOF'
     $ARGUMENTS
     HUM_EOF
     ```

2. 运行前后对比（检测 + 改写 + 双评分一步完成）：
   ```bash
   .opencode/skills/humanize-chinese/humanize compare INPUT_FILE -a -o /tmp/humanize_output.txt
   ```

3. 如果结果仍不够理想，可尝试：
   - 激进模式：`-a`（已在上方命令中启用）
   - CiLin 同义词扩展：加 `--cilin`
   - 风格化改写：加 `--style zhihu` / `--style novel` 等
   - 快速模式：加 `--quick`（18× 速度，跳统计 + best-of）

4. 展示给用户：
   - 原分 → 改写后分（通用文本目标 < 50，学术论文目标 < 40）
   - 改写后的文本
   - 关键改动说明

## 可选参数

| 参数 | 说明 |
|------|------|
| `-a` | 激进模式，强制全量 pipeline |
| `--cilin` | CiLin 同义词扩展 (38,873 词) |
| `--quick` | 快速模式（18× 速度，单次 humanize） |
| `--best-of-n N` | 自调 N（默认 10，N=1 = 单次 humanize） |
| `--scene novel` | 长文本/小说场景 |
| `--scene academic` | 学术论文场景 |
| `--style S` | 同时转换风格 |

## 目标评分 (v5.0 fused)

| 输入类型 | 目标改写后分 |
|----------|-------------|
| 刻板 AI 样板文 | < 35 (LOW, from 90+) |
| 自然 ChatGPT | 5-15 (LOW, from 15-25) |
| 学术论文 | < 35 (LOW, 双低) |
| 长篇博客/小说 (≥1500 字) | ~41 (MEDIUM) |