"""data.json から各候補のリンクページ（<slug>/index.html）とトップページを生成する。"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE = "https://komei-tokushima.github.io"
# 確認用（久栄さん専用）ページ。どこからもリンクせず、検索エンジンにも載せない。
PRIVATE_DIR = "kakunin-ac47f119aeaf"
SERVICES = {
    "hp": ("ホームページ", "#0b5cad"),
    "x": ("X（旧Twitter）", "#000000"),
    "instagram": ("Instagram", "#d62976"),
    "facebook": ("Facebook", "#1877f2"),
    "line": ("公式LINE", "#06c755"),
    "join": ("後援会 入会申込", "#c8102e"),
}

PAGE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}｜公明党</title>
<meta name="description" content="{title}の公式リンク集">
<style>
:root {{ --c: {color}; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #f4f6f9; color: #222;
  font-family: "Hiragino Sans", "Noto Sans JP", "Yu Gothic", sans-serif; }}
header {{ background: var(--c); color: #fff; text-align: center; padding: 28px 16px 24px; }}
.area {{ font-size: 14px; opacity: .9; margin: 0 0 6px; }}
h1 {{ font-size: 30px; margin: 0; letter-spacing: .08em; }}
.party {{ display: inline-block; margin-top: 10px; padding: 2px 12px; border: 1px solid #fff;
  border-radius: 999px; font-size: 13px; }}
main {{ max-width: 480px; margin: 0 auto; padding: 20px 16px 32px; }}
a.btn {{ display: block; margin: 0 0 14px; padding: 16px; border-radius: 12px; background: #fff;
  color: #222; text-decoration: none; font-size: 18px; font-weight: 700; text-align: center;
  border-left: 8px solid var(--s); box-shadow: 0 1px 3px rgba(0,0,0,.12); }}
a.btn:active {{ background: #eef1f5; }}
footer {{ text-align: center; font-size: 12px; color: #777; padding-bottom: 24px; }}
</style>
</head>
<body>
<header>
<p class="area">{area}</p>
<h1>{name}</h1>
<span class="party">公明党</span>
</header>
<main>
{buttons}
</main>
<footer>公明党徳島県本部</footer>
</body>
</html>
"""


def button(kind, url):
    label, color = SERVICES[kind]
    return (f'<a class="btn" style="--s:{color}" href="{html.escape(url)}" '
            f'target="_blank" rel="noopener">{label}</a>')


def main():
    people = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    items = []
    for p in people:
        buttons = "\n".join(button(k, p["links"][k]) for k in SERVICES if k in p["links"])
        out = ROOT / p["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(PAGE.format(title=html.escape(p["name"]), name=html.escape(p["name"]),
                                   area=html.escape(p["area"]), color=p["color"],
                                   buttons=buttons), encoding="utf-8")
        items.append(f'<a class="btn" style="--s:{p["color"]}" href="{p["slug"]}/">{html.escape(p["name"])}</a>')
    (ROOT / "index.html").write_text(PAGE.format(title="公明党徳島 リンク集", name="リンク集",
                                                 area="公明党徳島県本部", color="#0b5cad",
                                                 buttons="\n".join(items)), encoding="utf-8")
    build_private(people)


PRIVATE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="referrer" content="no-referrer">
<title>まとめQR 確認用</title>
<style>
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #f4f6f9; color: #222;
  font-family: "Hiragino Sans", "Noto Sans JP", "Yu Gothic", sans-serif; }}
header {{ background: #333; color: #fff; padding: 16px; text-align: center; }}
header h1 {{ margin: 0; font-size: 20px; }}
header p {{ margin: 6px 0 0; font-size: 12px; opacity: .8; }}
nav {{ display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; padding: 12px 16px 0;
  max-width: 560px; margin: 0 auto; }}
nav a {{ padding: 6px 10px; border-radius: 999px; background: #fff; color: #222;
  text-decoration: none; font-size: 13px; border: 2px solid var(--c); }}
main {{ max-width: 560px; margin: 0 auto; padding: 12px 16px 32px; }}
section {{ background: #fff; border-radius: 12px; margin: 0 0 16px; overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,.12); scroll-margin-top: 8px; }}
section h2 {{ margin: 0; padding: 10px 14px; background: var(--c); color: #fff; font-size: 18px; }}
section h2 small {{ font-size: 12px; font-weight: 400; opacity: .9; margin-left: 6px; }}
a.row {{ display: block; padding: 10px 14px; border-top: 1px solid #e6e9ee; color: #222;
  text-decoration: none; }}
a.row:active {{ background: #eef1f5; }}
a.row b {{ display: block; font-size: 15px; border-left: 5px solid var(--s); padding-left: 8px; }}
a.row span {{ display: block; font-size: 12px; color: #667; margin-top: 3px; word-break: break-all;
  padding-left: 13px; }}
a.row.top {{ background: #fafbfc; }}
</style>
</head>
<body>
<header>
<h1>まとめQR 確認用（9人）</h1>
<p>非公開の確認用ページです。URLを他の人に共有しないでください。</p>
</header>
<nav>
{nav}
</nav>
<main>
{sections}
</main>
</body>
</html>
"""


def private_row(label, color, url, cls="row"):
    u = html.escape(url)
    return (f'<a class="{cls}" style="--s:{color}" href="{u}" target="_blank" rel="noopener noreferrer">'
            f'<b>{html.escape(label)}</b><span>{u}</span></a>')


def build_private(people):
    nav, sections = [], []
    for i, p in enumerate(people, 1):
        num = f"{i:02d}"
        name = html.escape(p["name"])
        nav.append(f'<a style="--c:{p["color"]}" href="#{p["slug"]}">{num} {name}</a>')
        rows = [private_row("まとめページ（QRの飛び先）", "#333", f'{BASE}/{p["slug"]}/', "row top")]
        rows += [private_row(SERVICES[k][0], SERVICES[k][1], p["links"][k])
                 for k in SERVICES if k in p["links"]]
        sections.append(f'<section id="{p["slug"]}" style="--c:{p["color"]}">'
                        f'<h2>{num} {name}<small>{html.escape(p["area"])}</small></h2>\n'
                        + "\n".join(rows) + "\n</section>")
    out = ROOT / PRIVATE_DIR / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(PRIVATE.format(nav="\n".join(nav), sections="\n".join(sections)), encoding="utf-8")


if __name__ == "__main__":
    main()
