"""Teaser 'I Lupi non dormono mai': reel 9:16 (1440x2560) e carosello 4:5.

Uso: python3 tools/lupi.py
Richiede in media/instagram/lupi/: clip-1.mp4, clip-2.mp4, clip-3.mp4, lupo-1.jpg, lupo-2.jpg, lupo-3.jpg
"""
import subprocess, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from prodotto import render, crop45, ASSETS, RED
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "media/instagram/lupi"
logo = (ASSETS / "logo.png").as_uri()
tex916 = (ASSETS / "tex-916.jpg").as_uri()

LINES = ["I Lupi<br>non dormono mai.", "Ma ogni lupo<br>ha il suo rituale.", "Martedì si apre<br>la famiglia."]


def line(text, size):
    return (f"<div style='position:absolute;bottom:{{b}}px;width:100%;text-align:center;padding:0 70px'>"
            f"<div style='width:120px;height:4px;background:{RED};margin:0 auto 30px'></div>"
            f"<div class=name style='font-size:{size}px;line-height:1.12'>{text}</div></div>")


def main():
    tmp = D / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    car = D / "carosello"; car.mkdir(exist_ok=True)
    grad = "<div style='position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.92) 0%,rgba(0,0,0,.6) 22%,rgba(0,0,0,0) 42%)'></div>"
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        for i in (0, 1):
            render(pg, grad + line(LINES[i], 96).replace("{b}", "330"), 1080, 1920, tmp / f"ov-{i + 1}.png")
        render(pg, f"""<div style="position:absolute;inset:0;background:#09090a url({tex916}) center/cover"></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:240px 90px 340px">
<img src="{logo}" style="width:420px;margin-bottom:80px">
<div style="width:120px;height:4px;background:{RED};margin:0 auto 34px"></div>
<div class=name style="font-size:92px;line-height:1.12">{LINES[2]}</div>
<div class=label style="font-size:30px;margin-top:50px">#Ritualized</div></div>""", 1080, 1920, tmp / "end.png", transparent=False)
        pg.set_viewport_size({"width": 1080, "height": 1350})
        for i in range(3):
            crop45(D / f"lupo-{i + 1}.jpg", tmp / f"lupo-{i + 1}-45.jpg")
            top = f"<div style='position:absolute;top:60px;width:100%;text-align:center'><img src='{logo}' style='width:220px'></div>" if i == 2 else ""
            render(pg, f"<div style='position:absolute;inset:0;background:#000 url({(tmp / f'lupo-{i + 1}-45.jpg').as_uri()}) center/cover'></div>"
                       + grad + top + line(LINES[i], 88).replace("{b}", "90"), 1080, 1350, tmp / f"c{i + 1}.png", transparent=False)
            Image.open(tmp / f"c{i + 1}.png").convert("RGB").save(car / f"0{i + 1}-lupi.jpg", quality=95, subsampling=0)
        b.close()

    clip = "scale=1440:2560:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:2560,fps=30,setsar=1,unsharp=5:5:0.4"
    ov = "scale=1440:2560:flags=lanczos,format=rgba"
    fc = (f"[0:v]{clip}[c0];[3:v]{ov}[o0];[c0][o0]overlay=0:0:enable='gte(t,0.6)'[a];"
          f"[1:v]{clip}[c1];[4:v]{ov}[o1];[c1][o1]overlay=0:0:enable='gte(t,0.4)'[b];"
          f"[2:v]{clip}[c];"
          "[5:v]scale=2160:3840,zoompan=z='min(1+0.0005*on,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=105:s=1440x2560:fps=30,setsar=1[e];"
          "[a][b]xfade=transition=fadeblack:duration=0.6:offset=4.4[ab];"
          "[ab][c]xfade=transition=fadeblack:duration=0.6:offset=8.8[abc];"
          "[abc][e]xfade=transition=fadeblack:duration=0.6:offset=13.2[v];[v]format=yuv420p[o]")
    out = D / "reel-lupi.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                    "-t", "5", "-i", str(D / "clip-1.mp4"), "-t", "5", "-i", str(D / "clip-2.mp4"), "-t", "5", "-i", str(D / "clip-3.mp4"),
                    "-loop", "1", "-t", "5", "-i", str(tmp / "ov-1.png"), "-loop", "1", "-t", "5", "-i", str(tmp / "ov-2.png"),
                    "-i", str(tmp / "end.png"),
                    "-filter_complex", fc, "-map", "[o]", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                    "-maxrate", "25M", "-bufsize", "50M", "-movflags", "+faststart", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    main()
