<picture>
  <source media="(max-width: 600px)" srcset="./assets/profile-mobile.svg">
  <img src="./assets/profile.svg" width="100%" alt="Helong（小盒子）｜AI 架构师 · 技术负责人">
</picture>

我从 Java 分布式系统做起，有 16 年以上的软件工程经验。现在主要做模型推理平台和企业知识库，也把团队采用 AI 编程时用到的设计规范、代码评审和 API 验收方法整理出来，写在「小盒子的技术分享」。

## 架构案例

<p>
  <a href="https://xiaobox.github.io/p/2025-11-30-ai-mo-xing-tui-li-ping-tai-jia-gou-she-ji-yu-shi-jian/"><img src="./assets/serving.svg" width="236" alt="推理平台设计 · KServe 弹性伸缩与 vLLM 运行时选型"></a>
  <a href="https://github.com/xiaobox/model-price#how-it-works"><img src="./assets/finops.svg" width="236" alt="模型成本 · 跨云价格归一与供应商报价合并"></a>
  <a href="https://xiaobox.github.io/p/2025-04-07-rag-xi-tong-xiao-guo-nan-ping-2025-nian-bi-bei-de-rag-ping-g/"><img src="./assets/retrieval.svg" width="236" alt="RAG 评估 · 分开衡量检索召回率与答案忠实度"></a>
</p>

## 代表作

**[Model Price](https://github.com/xiaobox/model-price) · 大模型选型与成本比较**<br>
同一个模型在不同云上有不同的名称和计费方式。我把各家报价映射到统一的模型 ID，按每百万 token 比较输入、输出和缓存价格。[在线比价](https://modelprice.boxtech.icu/) · [报价合并实现](https://github.com/xiaobox/model-price/blob/main/backend/services/offering_merger.py)

**[驾驭 AI 编程](https://github.com/xiaobox/driving-ai-coding) · 团队研发工作流**<br>
从需求规格、任务拆分到代码评审，记录团队在哪些环节交给 Agent、在哪些环节由人把关。配套的 Bruno 示例可以从命令行运行，让 Agent 根据失败的断言修正接口测试。[工作流手册](https://github.com/xiaobox/driving-ai-coding/blob/master/ai-coding-workflow-best-practices.md) · [可运行的 API 测试](https://github.com/xiaobox/bruno-demo)

**[Modern MD Editor](https://github.com/xiaobox/mdeditor) · 开源 Markdown 编辑器**<br>
我写公众号时经常遇到排版在粘贴后走样，于是做了这个编辑器。它把代码、公式和图表转换为公众号可粘贴的富文本，并保留预览样式。[在线试用](https://mmdeditor.boxtech.icu/)

[![Modern MD Editor Stars](https://img.shields.io/github/stars/xiaobox/mdeditor?style=flat-square&label=Stars&color=197566&logo=github)](https://github.com/xiaobox/mdeditor/stargazers) [![Modern MD Editor Forks](https://img.shields.io/github/forks/xiaobox/mdeditor?style=flat-square&label=Forks&color=386475&logo=github)](https://github.com/xiaobox/mdeditor/forks)

### 开源足迹

<img src="https://github-stats-extended.vercel.app/api?username=xiaobox&amp;show_icons=true&amp;hide_rank=true&amp;hide=contribs&amp;hide_border=true&amp;bg_color=18262B&amp;title_color=F3EBDA&amp;text_color=C2D7D0&amp;icon_color=F5AF75&amp;custom_title=Open%20source%20activity" alt="Helong 的 GitHub 公开贡献统计" width="304">

[技术博客 · 小盒子的技术分享](https://xiaobox.github.io/)　·　[Java 与分布式系统笔记](https://github.com/xiaobox/Java-Developer-Knowledge-Base)
