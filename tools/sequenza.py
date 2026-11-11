"""Reel a scene (clip + frase) con chiusura sul logo, piu' carosello 4:5 dagli stessi fotogrammi.

Uso: python3 tools/sequenza.py apollineo|dionisiaco|lupi
Ogni progetto vive in media/instagram/<cartella>/ con clip-N.mp4 e still-N.jpg.
Regola: ogni video finisce sul logo, che resta a schermo fino all'ultimo fotogramma.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from prodotto import render, crop45, ASSETS, RED
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
GOLD = "#C9A45C"; WINE = "#B0263A"
logo = (ASSETS / "logo.png").as_uri()
tex916 = (ASSETS / "tex-916.jpg").as_uri(); tex45 = (ASSETS / "tex-45.jpg").as_uri()

PROGETTI = {
 "apollineo": dict(dir="rituali/apollineo", col=GOLD, label="Rituale Apollineo",
   frasi=["Ordine.", "Misura.", "Controllo."],
   fine="La disciplina<br>non ti limita:<br>ti definisce.", cta="Scrivici A in DM"),
 "dionisiaco": dict(dir="rituali/dionisiaco", col=WINE, label="Rituale Dionisiaco",
   frasi=["Istinto.", "Eccesso.", "Libertà."],
   fine="Le regole sono<br>per chi non ha stile.", cta="Scrivici D in DM"),
 "lupi": dict(dir="lupi", col=RED, label="#Ritualized",
   frasi=["I Lupi<br>non dormono mai.", "Ma ogni lupo<br>ha il suo rituale."],
   fine="Martedì si apre<br>la famiglia.", cta=None),
}


def frase(text, col, size, bottom):
    return (f"<div style='position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.92) 0%,rgba(0,0,0,.55) 24%,rgba(0,0,0,0) 44%)'></div>"
            f"<div style='position:absolute;bottom:{bottom}px;width:100%;text-align:center;padding:0 70px'>"
            f"<div style='width:120px;height:4px;background:{col};margin:0 auto 30px'></div>"
            f"<div class=name style='font-size:{size}px;line-height:1.12'>{text}</div></div>")


def chiusura(P, big):
    cta = f"<div class=cta style='font-size:{38 if big else 32}px;padding:20px 40px;margin-top:50px'>{P['cta']}</div>" if P["cta"] else ""
    return (f"<img src='{logo}' style='width:{420 if big else 320}px;margin-bottom:{70 if big else 50}px'>"
            f"<div class=rit style='font-size:{28 if big else 24}px;color:{P['col']};border-color:{P['col']}'>{P['label']}</div>"
            f"<div class=name style='font-size:{84 if big else 70}px;line-height:1.12;margin-top:40px'>{P['fine']}</div>{cta}"
            f"<div class=note style='font-size:{30 if big else 26}px;margin-top:40px'>Corso Umberto I 300c · Bernalda</div>")


def build(key):
    P = PROGETTI[key]; D = ROOT / "media/instagram" / P["dir"]
    tmp = D / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    car = D / "carosello"; car.mkdir(exist_ok=True)
    n = len(P["frasi"])
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        for i, t in enumerate(P["frasi"]):
            render(pg, frase(t, P["col"], 110 if len(t) < 14 else 92, 340), 1080, 1920, tmp / f"ov-{i + 1}.png")
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex916}) center/cover'></div>"
                   f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:240px 90px 340px'>{chiusura(P, True)}</div>",
               1080, 1920, tmp / "end.png", transparent=False)
        pg.set_viewport_size({"width": 1080, "height": 1350})
        for i, t in enumerate(P["frasi"]):
            crop45(D / f"still-{i + 1}.jpg", tmp / f"still-{i + 1}-45.jpg")
            render(pg, f"<div style='position:absolute;inset:0;background:#000 url({(tmp / f'still-{i + 1}-45.jpg').as_uri()}) center/cover'></div>"
                       + frase(t, P["col"], 100 if len(t) < 14 else 84, 90), 1080, 1350, tmp / f"c{i + 1}.png", transparent=False)
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex45}) center/cover'></div>"
                   f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:90px'>{chiusura(P, False)}</div>",
               1080, 1350, tmp / f"c{n + 1}.png", transparent=False)
        b.close()
    for i in range(n + 1):
        Image.open(tmp / f"c{i + 1}.png").convert("RGB").save(car / f"{i + 1:02d}-{key}.jpg", quality=95, subsampling=0)

    clip = "scale=1440:2560:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:2560,fps=30,settb=AVTB,setsar=1,unsharp=5:5:0.4"
    ov = "scale=1440:2560:flags=lanczos,format=rgba"
    durs = []
    for i in range(n):
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                  str(D / f"clip-{i + 1}.mp4")], capture_output=True, text=True).stdout)
        durs.append(min(d, 6.0))
    args = []; fc = ""
    for i in range(n):
        args += ["-t", f"{durs[i]:.2f}", "-i", str(D / f"clip-{i + 1}.mp4")]
    for i in range(n):
        args += ["-loop", "1", "-t", f"{durs[i]:.2f}", "-i", str(tmp / f"ov-{i + 1}.png")]
    args += ["-i", str(tmp / "end.png")]
    for i in range(n):
        fc += f"[{i}:v]{clip}[c{i}];[{n + i}:v]{ov}[o{i}];[c{i}][o{i}]overlay=0:0:enable='gte(t,0.5)'[s{i}];"
    fc += (f"[{2 * n}:v]scale=2160:3840,zoompan=z='min(1+0.0004*on,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
           f":d=120:s=1440x2560:fps=30,settb=AVTB,setsar=1[e];")
    prev = "s0"; off = 0.0
    for i in range(1, n):
        off += durs[i - 1] - 0.6
        fc += f"[{prev}][s{i}]xfade=transition=fadeblack:duration=0.6:offset={off:.2f}[x{i}];"; prev = f"x{i}"
    off += durs[n - 1] - 0.6
    fc += f"[{prev}][e]xfade=transition=fadeblack:duration=0.6:offset={off:.2f}[v];[v]format=yuv420p[o]"
    out = D / f"reel-{key}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", fc, "-map", "[o]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-maxrate", "25M", "-bufsize", "50M",
                    "-movflags", "+faststart", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    for k in sys.argv[1:]:
        build(k)
