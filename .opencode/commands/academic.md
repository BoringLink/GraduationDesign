---
description: 学术论文 AIGC 降重（知网/维普/万方，v5.0）
subtask: true
---

# /academic — 学术论文 AIGC 降重（v5.0）

降低学术论文的 AIGC 检测分数。针对知网 (CNKI)、维普 (VIP)、万方 (Wanfang)。

v5.0: **scene-aware academic LR** (中文学术语料 + HC3 academic 子集训练, coef 文件 `lr_coef_academic.json`), **10 学术检测维度**, **165 替换模式** (含 academic-tone 过渡词), **双评分对比** (学术专用 + 通用 detect_cn fused)。

## 输入

用户通过 $ARGUMENTS 提供学术文本（直接文本或文件路径）。

## 步骤

1. 判断输入是文件路径还是纯文本：
   - 如果 $ARGUMENTS 是一个存在的文件路径 → 直接使用
   - 如果 $ARGUMENTS 是纯文本 → 先保存到临时文件：
     ```bash
     cat > /tmp/academic_input.txt << 'ACAD_EOF'
     $ARGUMENTS
     ACAD_EOF
     ```

2. 运行学术降重 + 双评分对比：
   ```bash
   .opencode/skills/humanize-chinese/humanize academic INPUT_FILE -o /tmp/academic_output.txt --compare
   ```

3. 如果评分仍 > 40，尝试激进模式：
   ```bash
   .opencode/skills/humanize-chinese/humanize academic INPUT_FILE -o /tmp/academic_output.txt -a --compare
   ```

4. 快速模式（18× 速度，10k 字符 ~0.3 秒）：
   ```bash
   .opencode/skills/humanize-chinese/humanize academic INPUT_FILE -o /tmp/academic_output.txt --quick
   ```

5. 展示给用户：
   - 双评分：学术专用评分 (11 维) + 通用评分，改写前后对比
   - 改写后的文本
   - **提醒用户**：改完后通读一遍，确认专业术语没被误改、引用格式正确

## 目标评分 (v5.0 fused)

| 分数 | 等级 | 操作 |
|------|------|------|
| 0-29 | LOW / 低 | ✅ 可以提交 |
| 30-49 | MEDIUM / 中 | ⚠️ 建议手动润色 |
| 50+ | HIGH / 高 | 尝试 `-a` 激进模式 + 手动修改 |

## 改写策略说明

- 替换 AI 学术套话（保持学术性）：
  - "本文旨在" → "本研究聚焦于" / "本文尝试"
  - "研究表明" → "前人研究发现" / "相关研究揭示"
  - "被广泛应用" → "得到较多运用"
  - "近年来" → "过去数年间"
  - "首先/其次/最后" → "其一/其二/末了"
  - "因此" → "故而" / "由此" / "据此"
- 注入学术犹豫语（hedging）："可能""在一定程度上""初步来看"
- 增强作者主体性："笔者认为""本研究发现"
- 打破段落结构均匀度
- Hero 样本：学术 100→35 (-65 分)