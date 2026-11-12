"""Reel 9:16 + carosello 4:5 per un prodotto, in stile Ritual.

Uso: python3 tools/prodotto.py <slug> [<slug> ...]
Richiede in media/instagram/prodotti/<slug>/: hero-916.jpg, ing-916.jpg, clip.mp4 (hero-45.jpg facoltativo)
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "media/instagram/abbonamenti-v2/assets"
RED = "#d0283c"
SOFT = "#d6d0c6"
RITUALS = {"apollineo": ("Rituale Apollineo", "#C9A45C"), "dionisiaco": ("Rituale Dionisiaco", "#B0263A")}
PRODUCTS = json.loads((ROOT / "tools/prodotti.json").read_text(encoding="utf-8"))

FONTS = "".join(
    f"@font-face{{font-family:{fam};font-weight:{w};src:url({ASSETS.as_uri()}/{f})}}"
    for fam, w, f in [
        ("Cinzel", 700, "cinzel-latin-700-normal.woff2"), ("Cinzel", 800, "cinzel-latin-800-normal.woff2"),
        ("Mont", 600, "montserrat-latin-600-normal.woff2"), ("Mont", 700, "montserrat-latin-700-normal.woff2"),
        ("Mont", 800, "montserrat-latin-800-normal.woff2")])

BASE = f"""{FONTS}*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;color:#f6f3ee;font-family:Mont;overflow:hidden;position:relative}}
.label{{font-weight:700;letter-spacing:.3em;color:{RED};text-transform:uppercase;display:flex;align-items:center;gap:24px;justify-content:center}}
.label::before,.label::after{{content:"";width:70px;height:3px;background:{RED}}}
.name{{font-family:Cinzel;font-weight:800;line-height:1.02;text-shadow:0 4px 30px rgba(0,0,0,.85)}}
.spec{{font-weight:700;text-shadow:0 2px 16px rgba(0,0,0,.95)}}
.spec b{{color:#ff5a6a}}
.note{{font-weight:600;color:{SOFT};text-shadow:0 2px 16px rgba(0,0,0,.95);line-height:1.3}}
.cta{{display:inline-block;background:{RED};color:#fff;font-weight:800;letter-spacing:.06em}}
.rit{{display:inline-block;font-weight:800;letter-spacing:.22em;text-transform:uppercase;border:3px solid;padding:12px 26px;background:rgba(0,0,0,.45)}}
"""


def render(pg, html, w, h, out, transparent=True):
    f = Path(out).with_suffix(".html")
    f.write_text(f"<!doctype html><html><head><meta charset=utf-8><style>{BASE}</style></head>"
                 f"<body style='width:{w}px;height:{h}px'>{html}</body></html>", encoding="utf-8")
    pg.set_viewport_size({"width": w, "height": h})
    pg.goto(f.as_uri())
    pg.wait_for_timeout(400)
    pg.screenshot(path=str(out), omit_background=transparent)


def crop45(src, dst):
    im = Image.open(src).convert("RGB")
    tw = im.width; th = round(tw * 5 / 4)
    if th > im.height:
        th = im.height; tw = round(th * 4 / 5)
    l = (im.width - tw) // 2; t = (im.height - th) // 2
    im.crop((l, t, l + tw, t + th)).save(dst, quality=95)


def specs(p, size):
    return "".join(f"<div class=spec style='font-size:{size}px;margin:12px 0'>{s}</div>" for s in p["specs"])


def badge(p, size):
    name, col = RITUALS[p["ritual"]]
    return f"<div class=rit style='font-size:{size}px;color:{col};border-color:{col};background:rgba(0,0,0,.72)'>{name}</div>"


def build(slug):
    p = PRODUCTS[slug]
    d = ROOT / "media/instagram/prodotti" / slug
    tmp = d / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    car = d / "carosello"; car.mkdir(exist_ok=True)
    if not (d / "hero-45.jpg").exists():
        crop45(d / "hero-916.jpg", d / "hero-45.jpg")
    crop45(d / "ing-916.jpg", tmp / "ing-45.jpg")
    tex916 = (ASSETS / "tex-916.jpg").as_uri(); tex45 = (ASSETS / "tex-45.jpg").as_uri()
    logo = (ASSETS / "logo.png").as_uri()
    ing45 = (tmp / "ing-45.jpg").as_uri(); hero45 = (d / "hero-45.jpg").as_uri()
    big_name = 150 if len(p["name"]) < 10 else 118

    def end_body(big):
        return f"""
<img src="{logo}" style="width:{560 if big else 500}px;margin-bottom:{70 if big else 54}px">
{badge(p, 30 if big else 28)}
<div class=name style="font-size:{88 if big else 80}px;margin-top:{50 if big else 40}px">{p['tagline']}</div>
<div style="width:140px;height:4px;background:{RED};margin:{50 if big else 40}px 0"></div>
<div class=cta style="font-size:{44 if big else 40}px;padding:22px 46px">Disponibile in salone</div>
<div class=spec style="font-size:{40 if big else 34}px;margin-top:40px;color:{SOFT}">Corso Umberto I 300c · Bernalda</div>"""

    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(device_scale_factor=2)
        render(pg, f"""<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.9) 0%,rgba(0,0,0,.6) 28%,rgba(0,0,0,0) 45%)"></div>
<div style="position:absolute;bottom:380px;width:100%;text-align:center">
<div class=label style="font-size:34px">{p['category']}</div>
<div class=name style="font-size:{big_name}px;margin-top:20px">{p['name']}</div></div>""", 1080, 1920, tmp / "ov-title.png")
        render(pg, f"""<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.92) 0%,rgba(0,0,0,.65) 30%,rgba(0,0,0,0) 48%)"></div>
<div style="position:absolute;bottom:380px;width:100%;text-align:center;padding:0 70px">
<div class=label style="font-size:30px">{p.get("ing_label", "Estratto naturale")}</div>
<div class=name style="font-size:96px;margin-top:22px">{p['ingredient']}</div>
<div class=note style="font-size:44px;margin-top:24px">{p['ingredient_note']}</div></div>""", 1080, 1920, tmp / "ov-ing.png")
        render(pg, f"""<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.95) 0%,rgba(0,0,0,.8) 34%,rgba(0,0,0,0) 52%)"></div>
<div style="position:absolute;bottom:380px;width:100%;text-align:center;padding:0 70px">
<div class=label style="font-size:30px">{p['name']}</div>
<div style="margin-top:18px">{specs(p, 50)}</div></div>""", 1080, 1920, tmp / "ov-info.png")
        render(pg, f"""<div style="position:absolute;inset:0;background:#09090a url({tex916}) center/cover"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:240px 90px 340px;text-align:center">{end_body(True)}</div>""",
               1080, 1920, tmp / "end.png", transparent=False)
        render(pg, f"""<div style="position:absolute;inset:0;background:#000 url({hero45}) center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.97) 0%,rgba(0,0,0,.85) 20%,rgba(0,0,0,0) 40%),linear-gradient(180deg,rgba(0,0,0,.7) 0%,rgba(0,0,0,0) 14%)"></div>
<div style="position:absolute;top:40px;width:100%;text-align:center">{badge(p, 24)}</div>
<div style="position:absolute;bottom:60px;width:100%;text-align:center">
<div class=label style="font-size:30px">{p['category']}</div>
<div class=name style="font-size:{120 if len(p['name'])<10 else 100}px;margin-top:14px">{p['name']}</div></div>""", 1080, 1350, tmp / "c1.png", transparent=False)
        render(pg, f"""<div style="position:absolute;inset:0;background:#000 url({ing45}) center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.95) 0%,rgba(0,0,0,.75) 42%,rgba(0,0,0,0) 66%)"></div>
<div style="position:absolute;bottom:64px;width:100%;text-align:center;padding:0 70px">
<div class=label style="font-size:28px">{p.get("ing_label", "Estratto naturale")}</div>
<div class=name style="font-size:84px;margin:18px 0 8px">{p['ingredient']}</div>
<div class=note style="font-size:36px;margin-bottom:26px">{p['ingredient_note']}</div>
<div style="width:120px;height:4px;background:{RED};margin:0 auto 18px"></div>
{specs(p, 38)}</div>""", 1080, 1350, tmp / "c2.png", transparent=False)
        render(pg, f"""<div style="position:absolute;inset:0;background:#09090a url({tex45}) center/cover"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:90px;text-align:center">{end_body(False)}</div>""",
               1080, 1350, tmp / "c3.png", transparent=False)
        b.close()
    for i in (1, 2, 3):
        Image.open(tmp / f"c{i}.png").convert("RGB").save(car / f"{i:02d}-{slug}.jpg", quality=95, subsampling=0)

    def zp(frames, z):
        return (f"scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,"
                f"zoompan=z='min(1+{z}*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1440x2560:fps=30,setsar=1")
    ov = "scale=1440:2560:flags=lanczos,format=rgba"
    fc = (
        "[0:v]scale=1440:2560:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:2560,fps=30,setsar=1,unsharp=5:5:0.4[v0];"
        f"[1:v]{ov}[t];[v0][t]overlay=0:0:enable='gte(t,0.4)'[a];"
        f"[2:v]{zp(105, 0.0009)}[i0];[3:v]{ov}[io];[i0][io]overlay=0:0[i];"
        f"[4:v]{zp(105, 0.0008)}[h0];[5:v]{ov}[ho];[h0][ho]overlay=0:0[h];"
        f"[6:v]{zp(90, 0.0005)}[e];"
        "[a][i]xfade=transition=fade:duration=0.5:offset=4.5[ai];"
        "[ai][h]xfade=transition=fade:duration=0.5:offset=7.5[aih];"
        "[aih][e]xfade=transition=fadeblack:duration=0.5:offset=10.5[v];[v]format=yuv420p[o]")
    out = d / f"reel-{slug}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-t", "5", "-i", str(d / "clip.mp4"),
           "-loop", "1", "-t", "5", "-i", str(tmp / "ov-title.png"),
           "-i", str(d / "ing-916.jpg"), "-loop", "1", "-t", "3.5", "-i", str(tmp / "ov-ing.png"),
           "-i", str(d / "hero-916.jpg"), "-loop", "1", "-t", "3.5", "-i", str(tmp / "ov-info.png"),
           "-i", str(tmp / "end.png"),
           "-filter_complex", fc, "-map", "[o]", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
           "-b:v", "0", "-maxrate", "25M", "-bufsize", "50M", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(out)


if __name__ == "__main__":
    for s in sys.argv[1:]:
        build(s)
