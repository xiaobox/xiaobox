#!/usr/bin/env python3
"""生成 assets/ 里的头图（桌面 / 手机两版）、三张案例小卡和页脚波浪。

纯 SVG，自带动画，不依赖任何外部服务。改名字、头衔、配色后运行一次：
    python3 scripts/make_hero.py
"""
import math
import random
import sys
from pathlib import Path

FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB',"
        "'Microsoft YaHei','Noto Sans CJK SC','Noto Sans SC',sans-serif")
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


def cube(cx, cy, s, top=.96, left=.34, right=.6, stroke=.9, sw=1.6):
    """等轴测小盒子：三块半透明的面。"""
    w, h = s * math.cos(math.radians(30)), s / 2
    T, UR, LR, B, LL, UL, C = ((cx, cy - s), (cx + w, cy - h), (cx + w, cy + h), (cx, cy + s),
                               (cx - w, cy + h), (cx - w, cy - h), (cx, cy))

    def poly(pts, op):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return (f'<polygon points="{d}" fill="#fff" fill-opacity="{op}" stroke="#fff" '
                f'stroke-opacity="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')

    return poly((UL, C, B, LL), left) + poly((C, UR, LR, B), right) + poly((T, UR, C, UL), top)


def orbit(cx, cy, rx, ry, rot, dur, dot, r=6, begin=0):
    """一圈虚线轨道 + 一颗沿轨道跑的小球（转到盒子背面时变淡）。"""
    d = f"M{cx - rx},{cy} a{rx},{ry} 0 1,0 {2 * rx},0 a{rx},{ry} 0 1,0 {-2 * rx},0"
    return (
        f'<g transform="rotate({rot} {cx} {cy})">'
        f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".32" stroke-width="1.4" stroke-dasharray="2 9" stroke-linecap="round"/>'
        f'<circle r="{r}" fill="{dot}">'
        f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="{d}"/>'
        f'<animate attributeName="opacity" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" '
        f'values="1;1;.25;.25;1" keyTimes="0;.5;.56;.94;1"/>'
        f'</circle></g>'
    )


def stars(rng, n, x0, x1, y0, y1):
    out = []
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = rng.choice([1.2, 1.6, 2.0, 2.6])
        dur, begin = rng.uniform(2.6, 5.2), rng.uniform(0, 4)
        out.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity=".15">'
            f'<animate attributeName="opacity" values=".15;.95;.15" dur="{dur:.1f}s" begin="-{begin:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(out)


def waves(W, H, base, amp):
    def layer(y, a, dur, op, phase):
        def d(k):
            y1, y2, y3 = y + a * k, y - a * k, y + a * .6 * k
            return (f"M0 {y1:.0f} C{W * .18:.0f} {y1 - a * 1.6 * k:.0f} {W * .34:.0f} {y2 + a * 2.2 * k:.0f} {W * .5:.0f} {y2:.0f} "
                    f"S{W * .82:.0f} {y3 - a * 1.8 * k:.0f} {W} {y3:.0f} V{H} H0 Z")

        return (f'<path fill="#fff" fill-opacity="{op}" d="{d(1)}">'
                f'<animate attributeName="d" dur="{dur}s" begin="-{phase}s" repeatCount="indefinite" '
                f'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1" '
                f'values="{d(1)};{d(-1)};{d(1)}"/></path>')

    return layer(base, amp, 11, .10, 0) + layer(base + 14, amp * .8, 15, .14, 5)


def hero(W, H, mobile=False):
    rng = random.Random(7)
    rx = 28 if not mobile else 30
    if mobile:
        tx, eyebrow_y, name_y, role_y = 44, 92, 196, 258
        eyebrow_fs, name_fs, role_fs = 22, 104, 36
        cx, cy, s = W - 128, 108, 54
        orbits = orbit(cx, cy + 6, 112, 36, -16, 9, "#A5F3FC", 5) + orbit(cx, cy + 6, 86, 26, 22, 13, "#FBCFE8", 4, -4)
        minis = cube(cx + 66, cy + 112, 15, .8, .3, .5, .7, 1)
        star_box = (W * .35, W - 20, 16, H * .55)
        wave_y, wave_amp = H - 44, 9
    else:
        tx, eyebrow_y, name_y, role_y = 76, 92, 190, 246
        eyebrow_fs, name_fs, role_fs = 19, 100, 33
        cx, cy, s = 930, 150, 86
        orbits = orbit(cx, cy + 8, 208, 62, -16, 9, "#A5F3FC") + orbit(cx, cy + 8, 158, 44, 22, 13, "#FBCFE8", 5, -4)
        minis = (cube(cx - 214, cy - 78, 17, .8, .3, .5, .7, 1.1) + cube(cx + 186, cy + 74, 22, .8, .3, .5, .7, 1.1)
                 + cube(cx + 150, cy - 104, 11, .8, .3, .5, .7, 1))
        star_box = (520, W - 30, 18, H - 90)
        wave_y, wave_amp = H - 52, 12

    def bob(inner, dy, dur, begin=0):
        return (f'<g>{inner}<animateTransform attributeName="transform" type="translate" dur="{dur}s" begin="-{begin}s" '
                f'repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1" '
                f'values="0 0;0 {dy};0 0"/></g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Helong · 小盒子｜AI 架构师 · 技术负责人</title>
<desc id="d">渐变底色上的名字和头衔，右侧是一个悬浮的半透明小盒子，周围有小球绕行。</desc>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4338CA"/><stop offset=".48" stop-color="#7C3AED"/><stop offset="1" stop-color="#0891B2"/></linearGradient>
<radialGradient id="pink"><stop offset="0" stop-color="#F472B6" stop-opacity=".62"/><stop offset="1" stop-color="#F472B6" stop-opacity="0"/></radialGradient>
<radialGradient id="cyan"><stop offset="0" stop-color="#22D3EE" stop-opacity=".7"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<linearGradient id="edge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity=".06"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="7" flood-color="#1E1B4B" flood-opacity=".38"/></filter>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle cx="{W * .12:.0f}" cy="{H * 1.05:.0f}" r="{H * 1.05:.0f}" fill="url(#pink)"><animate attributeName="cx" values="{W * .12:.0f};{W * .26:.0f};{W * .12:.0f}" dur="17s" repeatCount="indefinite"/></circle>
<circle cx="{W * .9:.0f}" cy="{-H * .1:.0f}" r="{H * 1.1:.0f}" fill="url(#cyan)"><animate attributeName="cx" values="{W * .9:.0f};{W * .76:.0f};{W * .9:.0f}" dur="21s" repeatCount="indefinite"/></circle>
{stars(rng, 26 if not mobile else 14, *star_box)}
{waves(W, H, wave_y, wave_amp)}
<circle cx="{cx}" cy="{cy}" r="{s * 2.3:.0f}" fill="url(#halo)"><animate attributeName="opacity" values=".55;1;.55" dur="6s" repeatCount="indefinite"/></circle>
{orbits}
{bob(minis, 7, 7, 2)}
{bob(f'<g filter="url(#soft)">{cube(cx, cy, s)}</g>', -10, 6)}
<g font-family="{FONT}" fill="#fff" filter="url(#soft)">
<text x="{tx}" y="{eyebrow_y}" font-family="{MONO}" font-size="{eyebrow_fs}" font-weight="600" letter-spacing="4" fill-opacity=".86">XIAOBOX · 小盒子</text>
<text x="{tx - 5}" y="{name_y}" font-size="{name_fs}" font-weight="800" letter-spacing="-2.5">Helong</text>
<text x="{tx}" y="{role_y}" font-size="{role_fs}" font-weight="600" letter-spacing="1" fill-opacity=".96">AI 架构师 · 技术负责人</text>
</g>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="{rx}" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
</svg>
'''


def footer(W=1200, H=96):
    def d(k, y, a):
        return (f"M0 {y + a * k:.0f} C{W * .2:.0f} {y - a * 1.8 * k:.0f} {W * .36:.0f} {y + a * 2 * k:.0f} {W * .52:.0f} {y - a * .4 * k:.0f} "
                f"S{W * .84:.0f} {y + a * 1.6 * k:.0f} {W} {y - a * k:.0f} V{H} H0 Z")

    def layer(y, a, dur, op, phase):
        return (f'<path fill="url(#g)" fill-opacity="{op}" d="{d(1, y, a)}">'
                f'<animate attributeName="d" dur="{dur}s" begin="-{phase}s" repeatCount="indefinite" calcMode="spline" '
                f'keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1" values="{d(1, y, a)};{d(-1, y, a)};{d(1, y, a)}"/></path>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="presentation">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4338CA"/><stop offset=".5" stop-color="#7C3AED"/><stop offset="1" stop-color="#0891B2"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="0"/></clipPath></defs>
<g clip-path="url(#c)">{layer(44, 12, 13, .35, 0)}{layer(56, 10, 17, .55, 6)}{layer(70, 7, 11, 1, 3)}</g>
</svg>
'''


def tile(label, title, sub, c0, c1, icon, W=520, H=190):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}：{sub}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<linearGradient id="edge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity=".06"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle cx="{W - 96}" cy="{H / 2:.0f}" r="150" fill="url(#halo)"><animate attributeName="opacity" values=".6;1;.6" dur="6s" repeatCount="indefinite"/></circle>
<g>{icon}<animateTransform attributeName="transform" type="translate" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1" values="0 0;0 -6;0 0"/></g>
<g fill="#fff" font-family="{FONT}">
<text x="32" y="56" font-family="{MONO}" font-size="19" font-weight="600" letter-spacing="3" fill-opacity=".82">{label}</text>
<text x="30" y="118" font-size="50" font-weight="800" letter-spacing="-.5">{title}</text>
<text x="32" y="158" font-size="23" font-weight="500" fill-opacity=".92">{sub}</text>
</g>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="22" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
</svg>
'''


def icon_layers(cx, cy):
    def plate(y, op):
        w, h = 62, 26
        return (f'<polygon points="{cx},{y - h} {cx + w},{y} {cx},{y + h} {cx - w},{y}" fill="#fff" fill-opacity="{op}" '
                f'stroke="#fff" stroke-opacity=".9" stroke-width="2" stroke-linejoin="round"/>')
    return plate(cy + 34, .22) + plate(cy + 6, .45) + plate(cy - 22, .92)


def icon_bars(cx, cy):
    out, x = [], cx - 62
    for hgt, op in ((46, .4), (78, .62), (58, .5), (104, .95)):
        out.append(f'<rect x="{x}" y="{cy + 56 - hgt}" width="24" height="{hgt}" rx="7" fill="#fff" fill-opacity="{op}"/>')
        x += 34
    out.append(f'<path d="M{cx - 72} {cy + 66} H{cx + 76}" stroke="#fff" stroke-opacity=".7" stroke-width="3" stroke-linecap="round"/>')
    return "".join(out)


def icon_search(cx, cy):
    return (f'<circle cx="{cx - 8}" cy="{cy - 6}" r="44" fill="#fff" fill-opacity=".2" stroke="#fff" stroke-width="7"/>'
            f'<path d="M{cx + 25} {cy + 27} L{cx + 58} {cy + 60}" stroke="#fff" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M{cx - 28} {cy - 6} l14 15 l27 -30" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')


TILES = {
    "case-serving.svg": ("MODEL SERVING", "推理平台", "KServe · vLLM", "#4338CA", "#7C3AED", icon_layers(416, 95)),
    "case-finops.svg": ("MODEL FINOPS", "模型成本", "跨云价格归一", "#7C3AED", "#DB2777", icon_bars(416, 92)),
    "case-rag.svg": ("RAG EVALUATION", "RAG 评估", "召回率 · 忠实度", "#0E7490", "#4F46E5", icon_search(416, 95)),
}


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(parents=True, exist_ok=True)
    (out / "hero.svg").write_text(hero(1200, 320), encoding="utf-8")
    (out / "hero-mobile.svg").write_text(hero(640, 340, mobile=True), encoding="utf-8")
    (out / "footer.svg").write_text(footer(), encoding="utf-8")
    for name, args in TILES.items():
        (out / name).write_text(tile(*args), encoding="utf-8")
    for f in ("hero.svg", "hero-mobile.svg", "footer.svg", *TILES):
        print(f, (out / f).stat().st_size, "bytes")
