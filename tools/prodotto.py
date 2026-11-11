"""Reel 9:16 + carosello 4:5 per un prodotto, in stile Ritual.

Uso: python3 tools/prodotto.py <slug>
Richiede in media/instagram/prodotti/<slug>/: hero-916.jpg, hero-45.jpg, clip.mp4
"""
import json, subprocess, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "media/instagram/abbonamenti-v2/assets"
RED = "#d0283c"
SOFT = "#d6d0c6"

PRODUCTS = json.loads((ROOT / "tools/prodotti.json").read_text(encoding="utf-8"))

FONTS = "".join(
    f"@font-face{{font-family:{fam};font-weight:{w};src:url({ASSETS.as_uri()}/{f})}}"
    for fam, w, f in [
        ("Cinzel", 700, "cinzel-latin-700-normal.woff2"), ("Cinzel", 800, "cinzel-latin-800-normal.woff2"),
        ("Mont", 600, "montserrat-latin-600-normal.woff2"), ("Mont", 700, "montserrat-latin-700-normal.woff2"),
        ("Mont", 800, "montserrat-latin-800-normal.woff2")])

BASE = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;color:#f6f3ee;font-family:Mont;overflow:hidden}}
.label{{font-weight:700;letter-spacing:.3em;color:{RED};text-transform:uppercase;display:flex;align-items:center;gap:24px;justify-content:center}}
.label::before,.label::after{{content:"";width:70px;height:3px;background:{RED}}}
.name{{font-family:Cinzel;font-weight:800;line-height:1;text-shadow:0 4px 30px rgba(0,0,0,.8)}}
.spec{{font-weight:700;text-shadow:0 2px 16px rgba(0,0,0,.9)}}
.spec b{{color:{RED}}}
.cta{{display:inline-block;background:{RED};color:#fff;font-weight:800;letter-spacing:.06em}}
"""


def render(pg, html, w, h, out, transparent=True):
    pg.set_viewport_size({"width": w, "height": h})
    f = Path(out).with_suffix(".html")
    f.write_text(f"<!doctype html><html><head><meta charset=utf-8><style>{BASE}</style></head><body style='width:{w}px;height:{h}px'>{html}</body></html>", encoding="utf-8")
    pg.goto(f.as_uri())
    pg.wait_for_timeout(400)
    pg.screenshot(path=str(out), omit_background=transparent)


def specs_html(p, size):
    return "".join(f"<div class=spec style='font-size:{size}px;margin:14px 0'>{s}</div>" for s in p["specs"])


def build(slug):
    p = PRODUCTS[slug]
    d = ROOT / "media/instagram/prodotti" / slug
    tmp = d / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    tex916 = (ASSETS / "tex-916.jpg").as_uri(); tex45 = (ASSETS / "tex-45.jpg").as_uri()
    logo = (ASSETS / "logo.png").as_uri()
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page()
        # --- reel overlays 1080x1920 ---
        render(pg, f"""<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.9) 0%,rgba(0,0,0,.6) 28%,rgba(0,0,0,0) 45%)"></div>
<div style="position:absolute;bottom:380px;width:100%;text-align:center">
<div class=label style="font-size:34px">{p['category']}</div>
<div class=name style="font-size:150px;margin-top:20px">{p['name']}</div></div>""", 1080, 1920, tmp / "ov-title.png")
        render(pg, f"""<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.95) 0%,rgba(0,0,0,.8) 34%,rgba(0,0,0,0) 52%)"></div>
<div style="position:absolute;bottom:380px;width:100%;text-align:center;padding:0 70px">
<div class=label style="font-size:30px">{p['name']}</div>
<div style="margin-top:18px">{specs_html(p, 50)}</div></div>""", 1080, 1920, tmp / "ov-info.png")
        render(pg, f"""<div style="position:absolute;inset:0;background:#09090a url({tex916}) center/cover"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:240px 90px 340px;text-align:center">
<img src="{logo}" style="width:560px;margin-bottom:80px">
<div class=name style="font-size:92px">{p['tagline']}</div>
<div style="width:140px;height:4px;background:{RED};margin:56px 0"></div>
<div class=cta style="font-size:44px;padding:22px 46px">Disponibile in salone</div>
<div class=spec style="font-size:40px;margin-top:44px;color:{SOFT}">Corso Umberto I 300c · Bernalda</div></div>""", 1080, 1920, tmp / "end.png", transparent=False)
        # --- carosello 1080x1350 ---
        car = d / "carosello"; car.mkdir(exist_ok=True)
        hero45 = (d / "hero-45.jpg").as_uri()
        render(pg, f"""<div style="position:absolute;inset:0;background:#000 url({hero45}) center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.88) 0%,rgba(0,0,0,0) 30%)"></div>
<div style="position:absolute;bottom:60px;width:100%;text-align:center">
<div class=label style="font-size:30px">{p['category']}</div>
<div class=name style="font-size:120px;margin-top:14px">{p['name']}</div></div>""", 1080, 1350, tmp / "c1.png", transparent=False)
        render(pg, f"""<div style="position:absolute;inset:0;background:#09090a url({tex45}) center/cover"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:100px;text-align:center">
<img src="{logo}" style="width:240px;margin-bottom:50px">
<div class=label style="font-size:30px">{p['category']}</div>
<div class=name style="font-size:110px;margin:24px 0 10px">{p['name']}</div>
<div style="width:140px;height:4px;background:{RED};margin:36px 0"></div>
{specs_html(p, 46)}</div>""", 1080, 1350, tmp / "c2.png", transparent=False)
        render(pg, f"""<div style="position:absolute;inset:0;background:#09090a url({tex45}) center/cover"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:100px;text-align:center">
<img src="{logo}" style="width:520px;margin-bottom:64px">
<div class=name style="font-size:84px">{p['tagline']}</div>
<div style="width:140px;height:4px;background:{RED};margin:46px 0"></div>
<div class=cta style="font-size:42px;padding:20px 44px">Disponibile in salone</div>
<div class=spec style="font-size:36px;margin-top:36px;color:{SOFT}">Corso Umberto I 300c · Bernalda</div></div>""", 1080, 1350, tmp / "c3.png", transparent=False)
        b.close()
    from PIL import Image
    for i in (1, 2, 3):
        Image.open(tmp / f"c{i}.png").convert("RGB").save(car / f"{i:02d}-{slug}.jpg", quality=95, subsampling=0)
    # --- reel: clip 5s con titolo + hero 4s con specifiche + chiusura 3s ---
    hero = d / "hero-916.jpg"; clip = d / "clip.mp4"; out = d / f"reel-{slug}.mp4"
    fc = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v0];"
        "[v0][1:v]overlay=0:0:enable='gte(t,0.4)'[a];"
        "[2:v]scale=2160:3840,zoompan=z='min(1+0.0008*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=120:s=1080x1920:fps=30,setsar=1[h];"
        "[h][3:v]overlay=0:0[b];"
        "[4:v]scale=2160:3840,zoompan=z='min(1+0.0005*on,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=90:s=1080x1920:fps=30,setsar=1[e];"
        "[a][b]xfade=transition=fade:duration=0.5:offset=4.5[ab];"
        "[ab][e]xfade=transition=fadeblack:duration=0.5:offset=8[v];[v]format=yuv420p[o]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-t", "5", "-i", str(clip),
           "-loop", "1", "-t", "5", "-i", str(tmp / "ov-title.png"),
           "-i", str(hero),
           "-loop", "1", "-t", "4", "-i", str(tmp / "ov-info.png"),
           "-i", str(tmp / "end.png"),
           "-filter_complex", fc, "-map", "[o]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(out)


if __name__ == "__main__":
    build(sys.argv[1])
