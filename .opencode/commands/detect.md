---
description: 检测中文文本的 AI 痕迹（v5.0 融合评分 0-100）
subtask: true
---

# /detect — 检测中文文本的 AI 痕迹（v5.0）

检测用户提供的中文文本中的 AI 生成痕迹。融合评分 (rule × 0.2 + LR × 0.8)，0-100 分。

20+ 规则维度 + 8 HC3 校准统计特征 (sentence-length CV, short-sentence fraction, comma density, perplexity, GLTR rank buckets, DivEye skew/kurt) + scene-aware LR (general / academic / longform 三路) + 段落级信号 (paragraph length CV / 段内句长 CV / 跨段 trigram 重复)。

## 输入

用户通过 $ARGUMENTS 提供中文文本（直接文本或文件路径）。

## 步骤

1. 判断输入是文件路径还是纯文本：
   - 如果 $ARGUMENTS 是一个存在的文件路径 → 直接使用
   - 如果 $ARGUMENTS 是纯文本 → 先保存到临时文件：
     ```bash
     cat > /tmp/detect_input.txt << 'DETECT_EOF'
     $ARGUMENTS
     DETECT_EOF
     ```

2. 运行检测（使用 verbose 模式）：
   ```bash
   .opencode/skills/humanize-chinese/humanize detect INPUT_FILE -v
   ```
   场景选择：
   - 通用文本（默认）：直接用上述命令
   - 学术论文：加 `--scene academic`
   - 长文本/小说（≥1500 字）：加 `--scene novel`
   - 混合长度：加 `--scene auto`

3. 清晰报告结果：
   - 总分和等级 (LOW / MEDIUM / HIGH / VERY HIGH)
   - 最可疑的句子
   - 发现的关键 AI 模式（规则层 + 统计层指标）

## 评分标准

| 分数 | 等级 | 含义 |
|------|------|------|
| 0-24 | 🟢 LOW | 基本像人写的 |
| 25-49 | 🟡 MEDIUM | 有些 AI 痕迹 |
| 50-74 | 🟠 HIGH | 大概率 AI 生成 |
| 75-100 | 🔴 VERY HIGH | 几乎确定是 AI |

## 统计指标 (v5.0, Cohen's d)

| 指标 | d | 说明 |
|------|---|------|
| 段内句长 CV | -2.08 | v5 长文本最强信号 |
| 段落长度 CV | -1.49 | 人类段长方差大 |
| 句长变异系数 | 1.22 | AI 爱写等长句 |
| 短句占比 | 1.21 | 人类写短句，AI 很少 |
| 跨段 trigram 重复 | +1.13 | AI 易复用短语 |
| 困惑度 | 0.47 | 字符级 trigram |
| GLTR top-10 | 0.44 | AI 选高概率字 |
| 逗号密度 | 0.47 | AI 句子更长不间断 |