# 怎么改这个主页

主页由两个脚本生成，只用到 Python 标准库：

| 想改什么 | 改哪里 | 然后运行 |
| --- | --- | --- |
| 简介、项目卡片、技术栈图标、打字动画的几行字、统计卡配色 | `scripts/build_readme.py` | `python3 scripts/build_readme.py` |
| 头图上的名字和头衔、渐变色、三张案例小卡、页脚 | `scripts/make_hero.py` | `python3 scripts/make_hero.py` |

- `README.md` 和 `.github/workflows/*.yml` 是生成出来的。只改一两个字可以直接改 `README.md`，但下次运行脚本会被覆盖，记得把同样的改动写进脚本。
- “最近在写”那一段由工作流每 4 小时从博客 RSS 更新，脚本重新生成时会原样保留。
- 统计卡、语言卡、贪吃蛇由工作流每天生成，放在 `output` 分支；想马上刷新，到仓库的 Actions 页手动运行“更新主页图片”。
