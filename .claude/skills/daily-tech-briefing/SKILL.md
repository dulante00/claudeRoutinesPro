---
name: daily-tech-briefing
description: 每日 LLM 与科技新闻简报,抓取、筛选、整理成中文摘要并通过 Slack Connector 推送到 Slack
---

# 每日 LLM 与科技新闻简报

## 任务目标

每天早上生成一份简洁的中文科技新闻简报,通过 Slack Connector 推送到 Slack 频道。
内容聚焦 LLM、AI、前沿科技,过滤营销和水文。

---

## 信息源(按优先级从高到低)

### 一级源(必查)

#### 顶级中文媒体
- **机器之心** https://www.jiqizhixin.com/
- **量子位** https://www.qbitai.com/
- **极客公园** https://www.geekpark.net/ (深度产品体验 + 创始人独家访谈，质量高于一般媒体)

#### 国际头部模型厂商官方博客(各系列唯一权威发布渠道)
- **Anthropic** https://www.anthropic.com/news (Claude 系列)
- **OpenAI** https://openai.com/blog (GPT / Sora / Codex 系列)
- **Google DeepMind** https://blog.google/technology/ai/ (Gemini / Gemma / Veo 系列)
- **Meta AI** https://ai.meta.com/blog/ (Llama 系列；当前最重要的开源模型线，此前完全缺失)
- **Hugging Face Blog** https://huggingface.co/blog (开源生态风向标；新模型/数据集/工具发布首发地)

#### 国产大模型官方渠道(仅在有明确发布时查阅)
- **阿里 Qwen** https://qwenlm.github.io/blog/ (通义千问 / Qwen 系列官方)
- **字节豆包** https://team.doubao.com/zh/special/blog (豆包 / 云雀模型官方)
- **智谱 AI** https://zhipuai.cn/news (GLM 系列官方)
- **MiniMax** https://www.minimaxi.com/news (MiniMax / Hailuo 系列)
- **月之暗面 Kimi** https://kimi.moonshot.cn/ (Moonshot 系列；通过 36 氪/机器之心补充)
- **小米 AI** https://ai.mi.com/ (MiMo / 小米大模型；同时关注小米官方微博 https://weibo.com/xiaomi)
- **零一万物** https://www.lingyiwanwu.com/news (Yi 系列)
- **Mistral AI** https://mistral.ai/news/ (欧洲开源旗帜；Mistral / Mixtral 系列)
- **xAI** https://x.ai/blog (Grok 系列官方)

### 二级源(有余力就查)

#### 中文媒体补充
- **36氪 AI 频道** https://36kr.com/information/AI/
- **钛媒体 AI** https://www.tmtpost.com/ (商业化 + 融资报道，与 36 氪互补)
- **虎嗅科技** https://www.huxiu.com/ (AI 商业模式深度分析)
- **智东西** https://zhidx.com/ (具身智能 + AI 硬件 + 端侧模型)
- **InfoQ 中文** https://www.infoq.cn/topic/AI (工程师向，架构/工程实践)
- **少数派** https://sspai.com/ (AI 工具产品向，消费者视角)

#### 英文媒体
- **VentureBeat AI** https://venturebeat.com/category/ai (模型发布当日必有深度报道，英文 AI 媒体中覆盖最稳定)
- **TechCrunch AI** https://techcrunch.com/category/artificial-intelligence/ (融资 + 产品新闻)
- **The Verge AI** https://www.theverge.com/ai-artificial-intelligence (产品向，大众读者视角)
- **Ars Technica** https://arstechnica.com/ (技术细节准确，模型评测 + 基础设施)
- **9to5Google** https://9to5google.com/ (Google / Android AI 产品第一手)
- **9to5Mac** https://9to5mac.com/ (Apple / Anthropic 产品第一手)
- **Hacker News** https://news.ycombinator.com/ (挑 AI/LLM 相关高分帖，用中文总结)

#### 实时排行榜与动态追踪(重要：反映市场真实采用情况)
- **OpenRouter Rankings** https://openrouter.ai/rankings (各模型实时 token 调用量排行；腾讯 Hy3 等数据直接从此获取，不依赖二手报道)
- **LMArena / LMSYS Chatbot Arena** https://lmarena.ai/ (人类偏好 Elo 排行榜；排名变化本身是新闻)
- **ArtificialAnalysis** https://artificialanalysis.ai/ (模型速度 / 价格 / 质量综合横评；有新模型时必查)
- **Hugging Face 趋势模型** https://huggingface.co/models?sort=trending (开源社区热度风向)

#### AI 编码工具 Changelog（开发者受众极大，更新即新闻）
- **Cursor Changelog** https://changelog.cursor.com/ (AI 编码工具中迭代最快，功能更新频率高)
- **GitHub Copilot Blog** https://github.blog/tag/github-copilot/ (用户基数最大的 AI 编码助手；Microsoft 出品)
- **Windsurf / Codeium Blog** https://codeium.com/blog (Cursor 主要竞争对手；Cascade Agent 模式)
- **Replit Blog** https://blog.replit.com/ (在线 AI 编码平台；覆盖非专业开发者群体)

#### AI 推理基础设施（速度 / 成本基准本身构成新闻）
- **Groq Blog** https://groq.com/blog/ (LPU 极速推理；速度基准刷新时必报)
- **Cerebras Blog** https://cerebras.net/blog/ (晶圆级芯片；推理速度世界纪录保持者)
- **Together AI Blog** https://www.together.ai/blog (开源模型推理平台；反映开源模型商用采用情况)
- **Replicate Blog** https://replicate.com/blog (模型 API 化；哪些模型被开发者大量调用)

### 三级源(深度补充)

#### 学术与研究
- **arXiv cs.CL** https://arxiv.org/list/cs.CL/recent (NLP / LLM 方向论文)
- **arXiv cs.AI** https://arxiv.org/list/cs.AI/recent (AI 系统 / 推理 / Agent 方向)
- **Papers with Code** https://paperswithcode.com/ (论文 + 开源代码追踪，比 arXiv 更易筛选热门)

#### AI 工具目录（发现新兴工具）
- **There's An AI For That** https://theresanaiforthat.com/ (最大 AI 工具目录；每日新增工具列表，适合发现冷门但实用工具)
- **Product Hunt AI** https://www.producthunt.com/ ("Product of the Day" AI 类；发布首日热度反映市场兴趣)
- **Simon Willison's Blog** https://simonwillison.net/ (AI 工具实践顶级博主；每篇含可核实具体测评数据)

#### AI 垂直领域官方渠道（视频 / 语音 / 图像 / 音乐）
- **Runway ML Blog** https://runwayml.com/blog/ (视频生成领域引领者；Gen 系列官方)
- **ElevenLabs Blog** https://elevenlabs.io/blog (语音合成领域引领者；每次更新都影响语音 AI 格局)
- **Suno Blog** https://suno.com/blog (AI 音乐生成代表产品)
- **Stability AI News** https://stability.ai/news (Stable Diffusion 系列；图像/视频开源生态核心)
- **Kling AI / 快手可灵** https://klingai.com/ (国内视频生成代表；通过 36 氪/量子位追踪)

#### AI Agent 框架（开发者生态关键基础设施）
- **LangChain Blog** https://blog.langchain.dev/ (最广泛使用的 Agent 框架；新版本即影响数十万开发者)
- **LlamaIndex Blog** https://www.llamaindex.ai/blog (RAG / 检索增强生成代表框架)
- **CrewAI Blog** https://www.crewai.com/blog (多 Agent 协作框架；企业采用增速快)

#### GitHub 精确追踪
- **GitHub Trending Python（日榜）** https://github.com/trending/python?since=daily (每日 AI 开源项目热度；Python 榜比综合榜 AI 信号更纯)
- **ollama Releases** https://github.com/ollama/ollama/releases (本地 LLM 运行工具；用户基数最大的本地推理工具)
- **vLLM Releases** https://github.com/vllm-project/vllm/releases (生产级高性能推理引擎；主流云厂商后端)
- **llama.cpp Releases** https://github.com/ggerganov/llama.cpp/releases (端侧 / 边缘推理基准工具)
- **open-webui Releases** https://github.com/open-webui/open-webui/releases (本地模型 Web UI；新功能集成速度快)
- **ComfyUI Releases** https://github.com/comfyanonymous/ComfyUI/releases (图像 / 视频生成工作流；节点式 AI 创作社区核心)

#### 开发者社区（噪声高但首发信号强）
- **Reddit r/LocalLLaMA** https://www.reddit.com/r/LocalLLaMA/ (开源 / 本地模型最活跃社区；新模型量化包、跑分、破解限制首发地)
- **Reddit r/MachineLearning** https://www.reddit.com/r/MachineLearning/ (学术向；顶级论文讨论)
- **Reddit r/singularity** https://www.reddit.com/r/singularity/ (AI 进展综合讨论；热门帖反映大众认知风向)

#### 播客 / Newsletter
- **Dwarkesh Podcast** https://www.dwarkesh.com/ (AI/科技顶级人物长篇访谈；黄仁勋、Altman、Amodei 等；每次发布几乎是行业级事件，优先级高于普通三级源)
- **The Batch (Andrew Ng)** https://www.deeplearning.ai/the-batch/ (吴恩达每周 AI 精选；深度准确，适合周末补充)
- **TLDR AI** https://tldr.tech/ai (每日 AI 简报聚合；条目密度高，适合扫漏兜底)
- **Latent Space Podcast** https://www.latent.space/ (AI 工程师向；深度技术访谈，受众为 ML 工程师和研究员)

---

## 筛选规则

**时间窗口:** 仅保留过去 24 小时内发布的内容(含当天,排除昨天已推过的)。

**日期锚定(必须执行):**
在抓取任何内容前,先运行以下命令获取今天的准确日期:
```bash
date +%Y-%m-%d
```
将输出结果作为 `TODAY` 变量,后续所有时间判断以此为基准。
- 每篇文章必须找到明确的发布时间戳,**无法确认日期的文章直接跳过**
- 发布年份 ≠ `TODAY` 年份的文章**强制丢弃**,无论内容多相关
- 发布日期早于 `TODAY - 1天` 的文章**强制丢弃**

**优先级排序:**
1. 🔥 重大模型发布(GPT、Claude、Gemini、Llama、Qwen、国产大模型新版本；**必须从厂商官方博客核实，不依赖二手报道**)
2. 🔥 突破性论文(被广泛讨论,而非普通 arXiv 预印本)
3. 👀 重要产品更新(影响开发者或普通用户的功能)
4. 👀 行业重大动态(融资、收购、政策)
5. 👀 排行榜重大变化(OpenRouter 使用量榜首易主、LMArena Elo 分超越 GPT-4 级等；变化量需量化，如"超越前代 10 倍"而非"排名靠前")
6. 📌 其他有意思的科技消息

**国产模型追踪特别说明:**
- 小米 MiMo / AI 相关：优先查 https://ai.mi.com/ 和小米官方微博，其次 36 氪/极客公园
- 字节豆包：优先查 https://team.doubao.com/zh/special/blog，次查 36 氪/机器之心
- 阿里 Qwen：优先查 https://qwenlm.github.io/blog/，同时查 HuggingFace 新模型页
- 上述国产模型如当天官方无新发布，不必强行纳入简报

**GitHub / 开源社区来源使用规则:**
- GitHub Releases 必须有明确的 tag 日期（如 `v0.6.0 · released today`），无日期不引用
- GitHub Trending 只收录当天新上榜且与 AI/LLM 直接相关的项目；纯爬虫、数据集类项目跳过
- Reddit 帖子只收录评论数 >200 或 upvote >1000 的高热帖；内容必须含具体事实（新模型跑分、新工具发布），纯讨论/吐槽帖跳过
- 社区信息在简报中归入"📌 简讯"，不进入"🔥 必读"，除非有官方一手来源交叉验证

**AI 工具新品收录门槛（Product Hunt / There's An AI For That）:**
- 只收录满足以下至少两条的工具：① 有具体功能描述（非"AI驱动的XX平台"）；② 有可量化的性能/定价数据；③ 在 Product Hunt 日榜前 3 或周榜前 10；④ 有知名 VC 背书或创始人背景值得关注
- 纯"AI 包装"的普通 SaaS 工具一律过滤

**必须过滤掉:**
- 标题党("震惊!""颠覆!""碾压")
- 纯营销稿、厂商软文
- 同一事件的重复报道(只保留最权威一家)
- 纯观点文章、无新事实的评论
- 炒作性质的"AI 要取代 XX 职业"类内容
- **无法提炼出具体名称+数字的模糊报道**（如"多家公司纷纷布局 AI"此类无实质内容的综述）

---

## 输出格式

用 Markdown 格式生成,符合 Slack Block Kit 格式,总长度控制在 **2000 字以内**(Slack 不限制屏幕)。

结构如下:

```markdown
# 📰 今日科技简报 (YYYY-MM-DD)

## 🔥 必读 (最多 10 条)

### 1. [标题]
**一句话摘要**(30字内)

具体说明(50字内,交代 who/what/why)

🔗 [原文链接](URL) · 来源:xxx

---

### 2. ...

## 👀 值得看 (最多 10 条)

### 1. [标题]
摘要(50字内)
🔗 [链接](URL) · 来源:xxx

---

## 📌 简讯 (最多 10 条,仅标题+链接)

- [标题1](URL) · 来源
- [标题2](URL) · 来源
- ...

---

_本简报由 Claude Code Routine 自动生成,如需调整偏好请修改 skill 文件_
```

**格式要点:**
- 所有内容必须中文,英文标题需翻译(可保留原文在括号里)
- 数字、模型名、产品名用英文原文保留(如 GPT-5、Claude 4.7)
- 如果 24 小时内真的没有值得推的内容,直接推 "今日无重点新闻,保持关注" 即可,不要硬凑
- Slack 消息使用 Block Kit 富文本格式,支持链接、加粗、代码块等

**摘要质量强制要求（每条新闻必须包含以下要素,缺少则不得发布）:**

1. **Who（主体）** — 明确写出公司/团队/作者名称,不得用"某公司""研究团队"等模糊词
   - ✅ "Anthropic 发布 Claude Sonnet 4.6"
   - ❌ "某 AI 公司发布新模型"

2. **What（具体内容）** — 必须写出具体的模型名/技术名/产品名,禁止泛指
   - ✅ "基于 GQA + Flash Attention 3 的量化方法"
   - ❌ "新的量化技术"

3. **数字/指标** — 有性能数字必须引用,无数字则说明具体功能变化
   - ✅ "MMLU 提升 8 分,推理速度提升 3×,首 token 延迟降至 120ms"
   - ❌ "性能大幅提升"

4. **Why it matters（为何重要）** — 一句话说明对开发者/用户的实际影响

**摘要自检清单（生成后逐条检查,不通过则重写）:**
- [ ] 摘要中有具体名称,无"某某""相关"等模糊词
- [ ] 包含至少一个可核实的具体数字或功能点
- [ ] 读者无需点链接就能判断是否值得深入了解
- [ ] 未使用以下禁用短语:"详情见原文"、"取得突破"(未说明是什么突破)、"大幅提升"(未量化)、"多家公司"(未点名)

---

## 新闻存档规则

**每次推送成功后，将当日简报以 Markdown 格式保存到 repo 的 `news/` 目录：**

- 目录结构：`news/YYYY-MM/YYYYMMDD.md`
  - 子目录按年月创建，如 `news/2026-05/`
  - 文件按年月日命名，如 `20260514.md`
- 内容格式：使用标准 Markdown（`**bold**`、`[text](url)`），并在文件末尾附加「微信公众号版」区块，方便直接复制发文
- 创建时机：Slack 推送成功后，`git add` 连同 `briefing_history.json` 一起提交

**微信公众号版：生成 HTML 文件，浏览器粘贴**

微信公众号编辑器是富文本编辑器，不支持 Markdown 直接粘贴（链接失效、出现多余符号）。
正确做法：生成 HTML → 浏览器打开 → 全选复制 → 粘贴到公众号编辑器，链接、加粗、排版全部保留。

**生成命令：**
```bash
python3 .claude/skills/daily-tech-briefing/gen_wechat_html.py news/YYYY-MM/YYYYMMDD.html
```

**`gen_wechat_html.py` 使用说明：**
- 位于 `.claude/skills/daily-tech-briefing/gen_wechat_html.py`
- 每次运行前，将当日简报数据填入脚本顶部的 `MUST_READ` / `WORTH_READING` / `BRIEFS` 三个列表
- 字符串中如需中文引号请用 `「」` 替代 `""` 以避免 Python 语法冲突
- 脚本输出一个 HTML 文件，**用户在浏览器中打开 → Ctrl+A 全选 → Ctrl+C 复制 → 粘贴到公众号编辑器**

**HTML 格式规范：**
- 纯数字编号，去掉 emoji 分级符
- 链接以 `<a href>` 标签呈现，粘贴后自动变为可点击超链接
- 无任何 Markdown 语法残留（无 `[text](url)`、无 `🔗`）
- Inline CSS 样式确保排版风格适配公众号
- 末尾固定署名"每日 AI 科技简报，由 Claude Code 自动整理发布。"

**创建命令示例：**
```bash
mkdir -p news/$(date +%Y-%m)
# 写入文件后：
git add briefing_history.json news/$(date +%Y-%m)/$(date +%Y%m%d).md
git commit -m "📰 更新 $(date +%Y-%m-%d) 科技简报"
```

---

## 去重机制

**读取历史记录:**
每次运行前,先读取 repo 根目录的 `briefing_history.json`,获取过去 7 天推送过的标题/URL 列表。

**筛选时去重:**
丢弃标题高度相似或 URL 相同的条目。

**运行后更新:**
把本次推送的所有条目(标题+URL+日期)追加写入 `briefing_history.json`,保留最近 7 天。

**文件格式示例:**
```json
{
  "history": [
    {
      "date": "2026-04-22",
      "items": [
        {"title": "xxx", "url": "https://..."}
      ]
    }
  ]
}
```

---

## 推送步骤

生成好内容后，**优先使用 Slack MCP 工具**推送，curl webhook 作为降级方案。

### 推送方式一（主推）：Slack MCP 工具

直接调用 `mcp__Slack__slack_send_message`，无需配置 webhook。

**固定频道：**
- 频道名：`#news`
- 频道 ID：`C0AUAEKABAP`（jackliugroup workspace）

**消息格式规则（必须遵守，否则报 invalid_blocks）：**
- 使用 Slack mrkdwn 格式，**不是** Markdown
- 加粗：`*文字*`（不是 `**文字**`）
- 链接：`<URL|显示文字>`（不是 `[文字](URL)`）
- 分隔线：**不要使用 `---`**，会导致 invalid_blocks 错误
- 每条消息控制在 **1500 字以内**；内容较多时拆成多条，后续条目用 `thread_ts` 回复到同一线程

**推送模板：**
```
第一条（发到频道）：
📰 *今日科技简报 (YYYY-MM-DD)*

*🔥 必读*

*1. 标题*
摘要（含 who/what/数字）
🔗 <URL|原文> · 来源名

*2. 标题*
...

第二条（用 thread_ts 回复）：
*👀 值得看*
...

*📌 简讯*
• <URL|标题> · 来源
...

_本简报由 Claude Code Routine 自动生成_
```

**调用示例：**
```
# 第一条
mcp__Slack__slack_send_message(
    channel_id="C0AUAEKABAP",
    message="📰 *今日科技简报 (2026-04-22)*\n\n*🔥 必读*\n..."
)
# 保存返回的 message_ts

# 后续条目作为线程回复
mcp__Slack__slack_send_message(
    channel_id="C0AUAEKABAP",
    thread_ts="<上一条的 message_ts>",
    message="*👀 值得看*\n..."
)
```

### 推送方式二（降级）：curl SLACK_WEBHOOK_URL

仅在 MCP 工具不可用时使用。注意：`SLACK_WEBHOOK_URL` 环境变量可能已过期（返回 403），优先排查 MCP 方式。

---

## 异常处理

- **所有信息源都访问失败:** 推送一条"今日新闻抓取失败，请检查网络或源站可用性"到 Slack，并退出
- **MCP 推送失败 + webhook 也失败:** 把内容保存到 repo 的 `last_failed.md`，方便下次运行时重试或人工查看
- **内容为空:** 推送"今日无重点新闻，保持关注"
- **消息格式错误（invalid_blocks）:** 检查是否使用了 `---`、`**bold**` 或 `[text](url)` 等 Markdown 格式，改为 Slack mrkdwn 格式

---

## 执行流程总结

1. 切换到固定分支（参见 CLAUDE.md 分支策略）:
   ```bash
   git fetch origin
   git checkout claude/daily-briefing 2>/dev/null || git checkout -b claude/daily-briefing origin/main
   git pull origin claude/daily-briefing 2>/dev/null || true
   ```
2. 运行 `date +%Y-%m-%d` 获取今天日期,记为 `TODAY`
3. 读取 `briefing_history.json` 获取近 7 天已推送列表
4. 按优先级遍历信息源,抓取过去 24 小时内容(严格以 `TODAY` 为基准过滤年份和日期)
5. 应用筛选规则 + 去重
6. 按"必读 / 值得看 / 简讯"三档组织内容
7. 生成中文 Markdown
8. 通过 Slack MCP 工具推送到 #news 频道（优先）；若不可用则 curl SLACK_WEBHOOK_URL
9. 推送成功后:
   - 更新 `briefing_history.json`
   - 将简报保存为 `news/YYYY-MM/YYYYMMDD.md`（存档用 Markdown）
   - 将当日数据填入 `gen_wechat_html.py` 并运行，生成 `news/YYYY-MM/YYYYMMDD.html`（微信公众号可直接粘贴的富文本 HTML）
   - `git add briefing_history.json news/YYYY-MM/YYYYMMDD.md news/YYYY-MM/YYYYMMDD.html && git commit -m "📰 更新 TODAY 科技简报"`
   - `git push -u origin claude/daily-briefing`
10. **合并到 main**（有实质改动时执行）:
    ```bash
    git checkout main
    git pull origin main
    git merge claude/daily-briefing --no-ff -m "merge: daily-briefing TODAY"
    git push origin main
    git checkout claude/daily-briefing
    ```
    - 若合并冲突或 push 失败，保留分支现状，输出告警，**不强制合并**
11. 输出本次推送摘要到 Routine 日志（含标题列表 + 合并状态）

