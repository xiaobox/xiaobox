#!/usr/bin/env python3
"""生成个人主页的 README.md 和两个工作流文件。

配色、文案、组件参数都集中在这里，改完运行一次：
    python3 scripts/build_readme.py
“最近在写”列表由 GitHub Actions 维护，脚本会原样保留 README 里现有的那一段。
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, urlencode

USER = "xiaobox"
RAW = f"https://raw.githubusercontent.com/{USER}/{USER}/output"

# ---------- 配色（头图的渐变色在 make_hero.py 里） ----------
LIGHT = dict(accent="7C3AED", icon="0891B2", text="24292F", border="D0D7DE")
DARK = dict(accent="A78BFA", icon="22D3EE", text="C9D1D9", border="30363D")
BADGE = "7C3AED"


def q(params: dict) -> str:
    return urlencode(params, quote_via=quote, safe=":")


def picture(light: str, dark: str, alt: str, extra: str = "") -> str:
    return (
        "<picture>"
        f'<source media="(prefers-color-scheme: dark)" srcset="{dark}">'
        f'<img src="{light}" alt="{alt}"{extra}>'
        "</picture>"
    )


# ---------- 头图、打字动画、页脚 ----------
TYPING_LINES = [
    "模型推理平台 · KServe / vLLM",
    "企业 RAG 与知识库",
    "AI 研发工作流 · 规范 / 评审 / 验收",
    "公众号「小盒子的技术分享」",
]


def typing(color: str) -> str:
    return "https://readme-typing-svg.demolab.com?" + q(
        dict(
            font="Noto Sans SC",  # 带中文字形，各系统显示一致
            weight=500,
            size=21,
            duration=2800,
            pause=1400,
            color=color,
            center="true",
            vCenter="true",
            width=640,
            height=44,
            lines=";".join(TYPING_LINES),
        )
    )


# ---------- 徽章 ----------
def badge(label: str, message: str, color: str, logo: str = "", style="for-the-badge") -> str:
    def esc(s):
        return quote(s.replace("-", "--").replace("_", "__"), safe="")

    url = f"https://img.shields.io/badge/{esc(label)}-{esc(message)}-{color}?style={style}"
    if logo:
        url += f"&logo={logo}&logoColor=white"
    return url


badges = [
    (badge("公众号", "小盒子的技术分享", "07C160", "wechat"), "https://xiaobox.github.io/", "公众号：小盒子的技术分享"),
    (badge("Blog", "xiaobox.github.io", "4F46E5", "rss"), "https://xiaobox.github.io/", "技术博客"),
    (
        f"https://img.shields.io/github/stars/{USER}?style=for-the-badge&logo=github&label=Stars&color={BADGE}",
        f"https://github.com/{USER}?tab=repositories&sort=stargazers",
        "GitHub Stars 总数",
    ),
]

# ---------- 技术栈 ----------
ICONS = "java,spring,python,fastapi,ts,js,vue,react,docker,kubernetes,mysql,redis,kafka,nginx,linux,git"


def skills(theme: str) -> str:
    return f"https://skillicons.dev/icons?i={quote(ICONS, safe='')}&theme={theme}&perline=8"


AI_TAGS = ["KServe", "vLLM", "LlamaIndex", "RAG", "Agent 工作流"]


# ---------- 统计卡（由 GitHub Actions 生成到 output 分支） ----------
def card_opts(theme: dict, **kw) -> dict:
    base = dict(
        username=USER,
        title_color=theme["accent"],
        icon_color=theme["icon"],
        text_color=theme["text"],
        bg_color="00000000",
        border_color=theme["border"],
        border_radius=10,
        locale="cn",
    )
    base.update(kw)
    return base


STATS = dict(show_icons="true", rank_icon="github", hide="prs,contribs", include_all_commits="true",
             custom_title="GitHub 数据", card_width=410)
# 语言卡只列前 4 种；它比统计卡矮 10px，所以卡片窄一点、README 里两张图统一按 150 高显示，宽度正好对齐
LANGS = dict(layout="compact", langs_count=4, hide="html,css,scss,bru", exclude_repo="github-slideshow",
             custom_title="最常用的语言", card_width=382)
CARD_HEIGHT = 150

CARDS = {
    "stats.svg": ("stats", card_opts(LIGHT, ring_color=LIGHT["accent"], **STATS)),
    "stats-dark.svg": ("stats", card_opts(DARK, ring_color=DARK["accent"], **STATS)),
    "langs.svg": ("top-langs", card_opts(LIGHT, **LANGS)),
    "langs-dark.svg": ("top-langs", card_opts(DARK, **LANGS)),
}

SNAKE = {
    "snake.svg": "color_snake=#06B6D4&color_dots=#EBEDF0,#DDD6FE,#A78BFA,#7C3AED,#5B21B6",
    "snake-dark.svg": "color_snake=#22D3EE&color_dots=#161B22,#3B2A6B,#5B3FB8,#7C5CF0,#A78BFA",
}


def star(repo: str) -> str:
    return (
        f'<a href="https://github.com/{USER}/{repo}">'
        f'<img src="https://img.shields.io/github/stars/{USER}/{repo}?style=flat-square&label=%E2%98%85&color={BADGE}" '
        f'alt="{repo} 的 Star 数" align="right"></a>'
    )


def build(posts_md: str) -> str:
    L = []
    a = L.append
    a('<div align="center">')
    a("")
    a('<picture>'
      '<source media="(max-width: 600px)" srcset="./assets/hero-mobile.svg">'
      '<img src="./assets/hero.svg" width="100%" alt="Helong · 小盒子｜AI 架构师 · 技术负责人">'
      '</picture>')
    a("")
    a(
        '<a href="https://xiaobox.github.io/">'
        + picture(typing(LIGHT["accent"]), typing(DARK["accent"]), "在做的事：" + "；".join(TYPING_LINES))
        + "</a>"
    )
    a("")
    a("<p>")
    for src, href, alt in badges:
        a(f'<a href="{href}"><img src="{src}" alt="{alt}"></a>')
    a("</p>")
    a("")
    a("</div>")
    a("")
    a(
        "我从 Java 分布式系统做起，有 16 年以上的软件工程经验。现在主要做模型推理平台和企业知识库，"
        "也把团队采用 AI 编程时用到的设计规范、代码评审和 API 验收方法整理出来，写在「小盒子的技术分享」。"
    )
    a("")
    a("## 🧭 架构案例")
    a("")
    cases = [
        ("case-serving.svg", "推理平台设计", "KServe 弹性伸缩与 vLLM 运行时选型",
         "https://xiaobox.github.io/p/2025-11-30-ai-mo-xing-tui-li-ping-tai-jia-gou-she-ji-yu-shi-jian/"),
        ("case-finops.svg", "模型成本", "跨云价格归一与供应商报价合并",
         "https://github.com/xiaobox/model-price#how-it-works"),
        ("case-rag.svg", "RAG 评估", "分开衡量检索召回率与答案忠实度",
         "https://xiaobox.github.io/p/2025-04-07-rag-xi-tong-xiao-guo-nan-ping-2025-nian-bi-bei-de-rag-ping-g/"),
    ]
    a("<table>")
    a("<tr>")
    for img, title, desc, href in cases:
        a('<td width="33%" valign="top">')
        a(f'<a href="{href}"><img src="./assets/{img}" width="100%" alt="{title} · {desc}"></a>')
        a("<br>")
        a(f'<a href="{href}">{desc} →</a>')
        a("</td>")
    a("</tr>")
    a("</table>")
    a("")
    a("## 🛠 技术栈")
    a("")
    a('<p align="center">')
    a(picture(skills("light"), skills("dark"), "Java、Spring、Python、FastAPI、TypeScript、JavaScript、Vue、React、Docker、Kubernetes、MySQL、Redis、Kafka、Nginx、Linux、Git"))
    a("</p>")
    a('<p align="center">')
    a(" ".join(f"<kbd>{t}</kbd>" for t in AI_TAGS))
    a("</p>")
    a("")
    a("## 🚀 开源项目")
    a("")
    projects = [
        [
            ("📝", "Modern MD Editor", "mdeditor", True,
             "我写公众号时经常遇到排版在粘贴后走样，于是做了这个编辑器。它把代码、公式和图表转换为公众号可粘贴的富文本，并保留预览样式。",
             [("在线试用", "https://mmdeditor.boxtech.icu/")]),
            ("💹", "Model Price", "model-price", True,
             "同一个模型在不同云上有不同的名称和计费方式。我把各家报价映射到统一的模型 ID，按每百万 token 比较输入、输出和缓存价格。",
             [("在线比价", "https://modelprice.boxtech.icu/"),
              ("报价合并实现", "https://github.com/xiaobox/model-price/blob/main/backend/services/offering_merger.py")]),
        ],
        [
            ("🤖", "驾驭 AI 编程", "driving-ai-coding", False,
             "从需求规格、任务拆分到代码评审，记录团队在哪些环节交给 Agent、在哪些环节由人把关。配套的 Bruno 示例可以从命令行运行，让 Agent 根据失败的断言修正接口测试。",
             [("工作流手册", "https://github.com/xiaobox/driving-ai-coding/blob/master/ai-coding-workflow-best-practices.md"),
              ("可运行的 API 测试", "https://github.com/xiaobox/bruno-demo")]),
            ("☕", "Java 与分布式系统笔记", "Java-Developer-Knowledge-Base", True,
             "从工程师到架构师、技术负责人一路用到的知识图谱：JVM、并发、中间件、微服务、系统设计与技术管理。",
             [("打开目录", "https://github.com/xiaobox/Java-Developer-Knowledge-Base#内容结构")]),
        ],
    ]
    for row in projects:
        a("<table>")
        a("<tr>")
        for emoji, title, repo, stars, desc, links in row:
            a('<td width="50%" valign="top">')
            if stars:
                a(star(repo))
            a(f'<a href="https://github.com/{USER}/{repo}"><b>{emoji} {title}</b></a>')
            a("<br><br>")
            a(desc)
            a("<br><br>")
            a(" · ".join(f'<a href="{h}">{t}</a>' for t, h in links))
            a("</td>")
        a("</tr>")
        a("</table>")
        a("")
    a("## ✍️ 最近在写")
    a("")
    a("<!-- BLOG-POST-LIST:START -->")
    a(posts_md.strip())
    a("<!-- BLOG-POST-LIST:END -->")
    a("")
    a("[全部文章 →](https://xiaobox.github.io/)")
    a("")
    a("## 📊 GitHub 数据")
    a("")
    a('<p align="center">')
    a(picture(f"{RAW}/stats.svg", f"{RAW}/stats-dark.svg", "GitHub 数据：Star 数、提交数、Issue 数", f' height="{CARD_HEIGHT}"'))
    a(picture(f"{RAW}/langs.svg", f"{RAW}/langs-dark.svg", "最常用的语言", f' height="{CARD_HEIGHT}"'))
    a("</p>")
    a('<p align="center">')
    a(picture(f"{RAW}/snake.svg", f"{RAW}/snake-dark.svg", "贪吃蛇吃掉过去一年的贡献格子", ' width="100%"'))
    a("</p>")
    a("")
    a('<img src="./assets/footer.svg" width="100%" alt="">')
    a("")
    return "\n".join(L)


def workflows() -> dict:
    steps = []
    names = {"stats.svg": "统计卡（浅色）", "stats-dark.svg": "统计卡（深色）", "langs.svg": "语言卡（浅色）", "langs-dark.svg": "语言卡（深色）"}
    for fname, (card, opts) in CARDS.items():
        steps.append(
            f"      - name: {names[fname]}\n"
            f"        uses: stats-organization/github-readme-stats-action@v2\n"
            f"        with:\n"
            f"          card: {card}\n"
            f"          options: '{json.dumps(opts, ensure_ascii=False, separators=(',', ':'))}'\n"
            f"          path: dist/{fname}\n"
            f"          token: ${{{{ secrets.GITHUB_TOKEN }}}}\n"
            f"          fail_on_error: true\n"
        )
    snake = "\n".join(f"            dist/{k}?{v}" for k, v in SNAKE.items())
    assets = f"""name: 更新主页图片

# 每天生成一次统计卡、语言卡和贪吃蛇动画，强推到 output 分支（只保留最新一次提交）；
# README 里的图片从 output 分支引用。任何一步取数失败就整体失败，线上保留上一次的图。
on:
  schedule:
    - cron: "40 20 * * *" # 北京时间每天 04:40
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - .github/workflows/profile-assets.yml

permissions:
  contents: write

concurrency:
  group: profile-assets
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: 准备输出目录
        run: mkdir -p dist

{chr(10).join(steps)}
      - name: 贪吃蛇动画
        uses: Platane/snk/svg-only@v3
        with:
          github_user_name: ${{{{ github.repository_owner }}}}
          outputs: |
{snake}

      - name: 发布到 output 分支
        env:
          GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
        run: |
          cd dist
          ls -la
          git init -q -b output
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add -A
          git commit -q -m "更新主页图片"
          git push -f "https://x-access-token:${{GITHUB_TOKEN}}@github.com/${{GITHUB_REPOSITORY}}.git" output
"""
    posts = """name: 更新最新文章

# 每 4 小时读一次博客 RSS，把 README 里 BLOG-POST-LIST 两个标记之间的列表换成最新 5 篇；
# 列表没变化就不会产生提交。
on:
  schedule:
    - cron: "25 */4 * * *"
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: blog-posts
  cancel-in-progress: false

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: 读取 RSS 并更新 README
        uses: gautamkrishnar/blog-post-workflow@v1
        env:
          TZ: Asia/Shanghai
        with:
          feed_list: https://xiaobox.github.io/index.xml
          max_post_count: 5
          tag_post_pre_newline: true
          template: "- <code>$date</code> [$title]($url)$newline"
          date_format: "mm-dd"
          commit_message: "更新最新文章列表"
          committer_username: "github-actions[bot]"
          committer_email: "41898282+github-actions[bot]@users.noreply.github.com"
"""
    return {"profile-assets.yml": assets, "blog-posts.yml": posts}


MARK_START, MARK_END = "<!-- BLOG-POST-LIST:START -->", "<!-- BLOG-POST-LIST:END -->"


def current_posts(readme: Path) -> str:
    """取出 README 里现有的文章列表（由工作流维护），重新生成时原样放回去。"""
    if readme.exists():
        m = re.search(re.escape(MARK_START) + "(.*?)" + re.escape(MARK_END), readme.read_text(encoding="utf-8"), flags=re.S)
        if m:
            return m.group(1).strip("\n")
    return ""


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    readme = root / "README.md"
    text = build(current_posts(readme))
    readme.write_text(text, encoding="utf-8")
    wf = root / ".github" / "workflows"
    wf.mkdir(parents=True, exist_ok=True)
    for name, body in workflows().items():
        (wf / name).write_text(body, encoding="utf-8")
    if len(sys.argv) > 1:  # 可选：把统计卡参数另存一份 JSON，方便本地预览时取同样的图
        Path(sys.argv[1]).write_text(
            json.dumps({"cards": {k: [c, q(o)] for k, (c, o) in CARDS.items()}, "snake": SNAKE}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    print(f"README.md（{len(text)} 字符）和 {', '.join(workflows())} 已生成")
