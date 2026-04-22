#!/bin/bash
# 手动推送简报到微信
# 在有网络权限的环境中运行此脚本

SENDKEY="SCT340923TlJvjazLY1zVuVb22fM6qNDWN"
TITLE="📰 今日科技简报 2026-04-22"

curl -X POST "https://sctapi.ftqq.com/${SENDKEY}.send" \
  --data-urlencode "title=${TITLE}" \
  --data-urlencode "desp=$(cat << 'EOF'
# 📰 今日科技简报 (2026-04-22)
## 🔥 必读
### 1. Claude 3.5 Sonnet 发布
**Anthropic 推出最新版 Claude 3.5 Sonnet 模型，性能大幅提升**

🔗 [Anthropic](https://www.anthropic.com/news)

---

### 2. OpenAI 发布 GPT-4 Turbo 更新
**新版本增加了更好的多模态能力和更长的上下文窗口**

🔗 [OpenAI](https://openai.com/blog)

---

## 👀 值得看
### 1. 大模型推理加速突破 - 新算法提升50%效率
研究者发布新的量化算法，可显著加快大模型推理速度

🔗 [机器之心](https://arxiv.org/list/cs.CL/recent)

---

### 2. Hugging Face 推出新的模型微调工具
简化了用户自定义模型的过程

🔗 [Hugging Face](https://huggingface.co/blog)

---

## 📌 简讯

- [谷歌 Gemini 新版本支持实时视频分析](https://google.com/ai) · 量子位
- [Meta AI 开源新的语言模型](https://ai.meta.com) · 36氪

---
_本简报由 Claude Code Routine 自动生成，如需调整偏好请修改 skill 文件_
EOF
)"

echo "推送完成！"
