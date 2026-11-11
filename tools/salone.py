"""'Il salone': reel 9:16 e carosello 4:5 dalle foto e dal video reali del negozio.

Uso: python3 tools/salone.py
Richiede media/instagram/salone/sorgenti/ con le foto (IMG*.jpg) e il video (VID*.mp4).
Le foto vengono scurite e contrastate per stare nel mondo nero, oro e rosso del brand.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageOps
sys.path.insert(0, str(Path(__file__).parent))
from prodotto import render, ASSETS, RED
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "media/instagram/salone"; SRC = D / "sorgenti"
logo = (ASSETS / "logo.png").as_uri()
tex916 = (ASSETS / "tex-916.jpg").as_uri(); tex45 = (ASSETS / "tex-45.jpg").as_uri()
GRADE = "eq=contrast=1.18:brightness=-0.10:saturation=0.82:gamma=0.92,vignette=PI/4.2"

SCENE = [  # foto, frase
    ("IMG20261026134222.jpg", "Il tuo posto<br>è pronto."),
    ("IMG20261026134300.jpg", "Ogni strumento<br>al suo posto."),
    ("IMG20261026134506.jpg", "Lama, mano,<br>misura."),
    ("IMG20261026134639.jpg", "Qui conta<br>il dettaglio."),
]
VIDEO = "VID20261021130717.mp4"


def grade(src, dst, w, h):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    tmp = dst.with_suffix(".src.jpg"); im.save(tmp, quality=96)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-vf",
                    f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},{GRADE}",
                    "-q:v", "2", str(dst)], check=True)
    tmp.unlink()


def frase(text, size, bottom):
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.92) 0%,rgba(0,0,0,.55) 24%,rgba(0,0,0,0) 44%)'></div>"
            f"<div style='position:absolute;bottom:{bottom}px;width:100%;text-align:center;padding:0 70px'>"
            f"<div style='width:120px;height:4px;background:{RED};margin:0 auto 30px'></div>"
            f"<div class=name style='font-size:{size}px;line-height:1.12'>{text}</div></div>")


def chiusura(big):
    return (f"<img src='{logo}' style='width:{420 if big else 320}px;margin-bottom:{70 if big else 50}px'>"
            f"<div class=name style='font-size:{84 if big else 70}px;line-height:1.12'>Benvenuto<br>nel Rituale.</div>"
            f"<div class=cta style='font-size:{38 if big else 32}px;padding:20px 40px;margin-top:50px'>Prenota in DM</div>"
            f"<div class=note style='font-size:{30 if big else 26}px;margin-top:40px'>Corso Umberto I 300c · Bernalda</div>")


def main():
    tmp = D / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    car = D / "carosello"; car.mkdir(exist_ok=True)
    for i, (f, _) in enumerate(SCENE):
        grade(SRC / f, tmp / f"s{i}-916.jpg", 2160, 3840)
        grade(SRC / f, tmp / f"s{i}-45.jpg", 2160, 2700)
    # video reale: 7 secondi di camminata nel salone, verticale e con la stessa correzione colore
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "3", "-t", "7", "-i", str(SRC / VIDEO), "-an", "-vf",
                    f"scale=1440:2560:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:2560,fps=30,{GRADE},setsar=1",
                    "-c:v", "libx264", "-crf", "14", "-preset", "slow", str(tmp / "walk.mp4")], check=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        render(pg, frase("Il salone.", 120, 340), 1080, 1920, tmp / "ov-walk.png")
        for i, (_, t) in enumerate(SCENE):
            render(pg, frase(t, 96, 340), 1080, 1920, tmp / f"ov-{i}.png")
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex916}) center/cover'></div>"
                   f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:240px 90px 340px'>{chiusura(True)}</div>",
               1080, 1920, tmp / "end.png", transparent=False)
        pg.set_viewport_size({"width": 1080, "height": 1350})
        for i, (_, t) in enumerate(SCENE):
            render(pg, f"<div style='position:absolute;inset:0;background:#000 url({(tmp / f's{i}-45.jpg').as_uri()}) center/cover'></div>"
                       + frase(t, 88, 90), 1080, 1350, tmp / f"c{i}.png", transparent=False)
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex45}) center/cover'></div>"
                   f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:90px'>{chiusura(False)}</div>",
               1080, 1350, tmp / f"c{len(SCENE)}.png", transparent=False)
        b.close()
    for i in range(len(SCENE) + 1):
        Image.open(tmp / f"c{i}.png").convert("RGB").save(car / f"{i + 1:02d}-salone.jpg", quality=95, subsampling=0)

    ov = "scale=1440:2560:flags=lanczos,format=rgba"
    zp = ("scale=2160:3840,zoompan=z='min(1+0.0009*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          ":d={d}:s=1440x2560:fps=30,settb=AVTB,setsar=1")
    args = ["-i", str(tmp / "walk.mp4"), "-loop", "1", "-t", "7", "-i", str(tmp / "ov-walk.png")]
    fc = f"[0:v]fps=30,settb=AVTB,setsar=1[w0];[1:v]{ov}[wo];[w0][wo]overlay=0:0:enable='gte(t,0.6)'[s0];"
    for i in range(len(SCENE)):
        args += ["-i", str(tmp / f"s{i}-916.jpg"), "-loop", "1", "-t", "3", "-i", str(tmp / f"ov-{i}.png")]
        a, o = 2 + 2 * i, 3 + 2 * i
        fc += f"[{a}:v]{zp.format(d=90)}[p{i}];[{o}:v]{ov}[q{i}];[p{i}][q{i}]overlay=0:0[s{i + 1}];"
    e = 2 + 2 * len(SCENE)
    args += ["-i", str(tmp / "end.png")]
    fc += f"[{e}:v]{zp.format(d=120).replace('0.0009', '0.0004')}[e];"
    durs = [7] + [3] * len(SCENE)
    prev = "s0"; off = 0.0
    for i in range(1, len(durs)):
        off += durs[i - 1] - 0.5
        fc += f"[{prev}][s{i}]xfade=transition=fadeblack:duration=0.5:offset={off:.2f}[x{i}];"; prev = f"x{i}"
    off += durs[-1] - 0.5
    fc += f"[{prev}][e]xfade=transition=fadeblack:duration=0.5:offset={off:.2f}[v];[v]format=yuv420p[o]"
    out = D / "reel-salone.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", fc, "-map", "[o]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-maxrate", "25M", "-bufsize", "50M",
                    "-movflags", "+faststart", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    main()
