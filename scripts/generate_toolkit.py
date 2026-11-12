import base64
import html
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CARDS = ASSETS / "cards"
CARDS.mkdir(parents=True, exist_ok=True)

# Colors and styling matching the clean dark card theme
BG, PANEL, LINE = "#0d0f17", "#141724", "#2a2f47"
INK, MUTED, FAINT = "#f5f6fb", "#a9aecb", "#6b7194"
SKY, VIOLET, MINT, PINK = "#38bdf8", "#a78bfa", "#34d399", "#f472b6"
FONT = "'Inter','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace"

STYLE = (
    "<style>"
    "@keyframes up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}"
    "@keyframes fade{from{opacity:0}to{opacity:1}}"
    "@keyframes draw{to{stroke-dashoffset:0}}"
    "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    ".a{animation:up .7s cubic-bezier(.2,.8,.2,1) both}"
    ".f{animation:fade .9s ease both}"
    ".d{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.8s cubic-bezier(.4,0,.2,1) .2s forwards}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important;stroke-dashoffset:0!important}}"
    "</style>"
)

TOOLKIT = [
    ("Languages", ["cpp", "py", "js", "ts", "bash"]),
    ("Frontend", ["html", "css", "react", "nextjs", "tailwind"]),
    ("Backend & data", ["nodejs", "express", "postgres", "mysql"]),
    ("Tools", ["git", "github", "docker", "linux", "vscode", "visualstudio", "pycharm", "npm", "vercel"]),
    ("AI & MCP", ["antigravity", "stitch"]),
]

def esc(s):
    return html.escape(str(s))

def frame(w, h, body, title):
    bg = f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{BG}" stroke="{LINE}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>{STYLE}{bg}{body}</svg>\n')

def text(x, y, s, size=13, fill=INK, weight=500, anchor="start", font=FONT, ls=0, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')

def eyebrow(x, y, s, fill=MUTED):
    return text(x, y, s.upper(), 11, fill, 700, font=MONO, ls=1.6)

def delay(sec):
    return f'style="animation-delay:{sec:.2f}s"'

def fetch_skillicon(name: str) -> str:
    url = f"https://skillicons.dev/icons?i={name}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return "data:image/svg+xml;base64," + base64.b64encode(resp.read()).decode()

def main():
    icons_data = {}
    
    # 1. Fetch skillicons
    all_skill_icons = [
        "cpp", "py", "js", "ts", "bash",
        "html", "css", "react", "nextjs", "tailwind",
        "nodejs", "express", "postgres", "mysql",
        "git", "github", "docker", "linux", "vscode", "visualstudio", "pycharm", "npm", "vercel"
    ]
    for name in all_skill_icons:
        try:
            icons_data[name] = fetch_skillicon(name)
            print(f"Fetched {name}")
        except Exception as e:
            print(f"Failed {name}: {e}")

    # 2. Local custom icons (Antigravity & Stitch)
    antigravity_path = ASSETS / "antigravity.png"
    if antigravity_path.exists():
        icons_data["antigravity"] = "data:image/png;base64," + base64.b64encode(antigravity_path.read_bytes()).decode()

    stitch_path = ASSETS / "stitch.png"
    if stitch_path.exists():
        icons_data["stitch"] = "data:image/png;base64," + base64.b64encode(stitch_path.read_bytes()).decode()

    # 3. Build card SVG
    w, size, gap, row_h = 840, 46, 12, 70
    h = 40 + row_h * len(TOOLKIT) + 10
    body, k = "", 0
    for r, (label, icons) in enumerate(TOOLKIT):
        y = 34 + r * row_h
        hl = (label == "AI & MCP")
        if r:
            body += f'<line x1="32" y1="{y - 12}" x2="{w - 32}" y2="{y - 12}" stroke="{LINE}" stroke-dasharray="2 6"/>'
        body += f'<g class="f" {delay(r * .12)}>{eyebrow(36, y + 28, label, SKY if hl else MUTED)}</g>'
        for i, name in enumerate(icons):
            if name in icons_data:
                x = 230 + i * (size + gap)
                body += (f'<g class="a" {delay(.15 + k * .045)}><image x="{x}" y="{y}" width="{size}" height="{size}" '
                         f'href="{icons_data[name]}"/></g>')
                k += 1
        if hl:
            body += f'<g class="f" {delay(1.2)}>{text(230 + len(icons) * (size + gap) + 12, y + 28, "Antigravity AI · Stitch MCP", 13, MUTED, 500)}</g>'

    svg_content = frame(w, h, body, "Toolkit")
    
    out_cards = CARDS / "toolkit.svg"
    out_cards.write_text(svg_content, encoding="utf-8")
    print(f"Saved: {out_cards}")

    out_assets = ASSETS / "toolkit.svg"
    out_assets.write_text(svg_content, encoding="utf-8")
    print(f"Saved: {out_assets}")

if __name__ == "__main__":
    main()
