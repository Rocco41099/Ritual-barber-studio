"""'Il salone' v2: reel 9:16 dalle clip animate delle foto reali e carosello 4:5 (copertina, una slide per frase, manifesto, prenotazione).

Uso: python3 tools/salone.py
Richiede in media/instagram/salone/: clip/01..08.mp4 (Higgsfield, 2K o 1080p) e sorgenti/ con le foto.
Regola: il video chiude sempre sul logo.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageOps
sys.path.insert(0, str(Path(__file__).parent))
from prodotto import render, ASSETS, RED
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "media/instagram/salone"; SRC = D / "sorgenti"; CLIP = D / "clip"
logo = (ASSETS / "logo.png").as_uri()
tex916 = (ASSETS / "tex-916.jpg").as_uri(); tex45 = (ASSETS / "tex-45.jpg").as_uri()
GRADE = ("curves=master='0/0 0.15/0.06 0.5/0.46 0.85/0.88 1/0.97',"
         "colorbalance=rh=0.05:gh=0.015:bh=-0.035:rs=0.02:bs=-0.025,eq=saturation=0.85:contrast=1.05,vignette=PI/5")

# clip, layout (full = 9:16 a tutto schermo, band = 16:9 al centro su fondo nero), frase, sottofrase, foto per il carosello
SCENE = [
    ("01", "full", "Fuori,<br>il mondo corre.", "", "6026285101857050210.jpg"),
    ("02", "band", "Qui dentro,<br>il tempo torna tuo.", "", "6026285101857050204.jpg"),
    ("10", "full", "Anche l'attesa<br>fa parte del rito.", "", "6028536901670735534.jpg"),
    ("03", "full", "Una poltrona.<br>Nessuna fretta.", "", "IMG20261026134222.jpg"),
    ("04", "full", "Ogni strumento<br>ha il suo posto.", "Ogni gesto, il suo perché.", "IMG20261026134300.jpg"),
    ("12", "band", "Ogni mossa è pensata.", "Come ogni taglio.", "6028536901670735536.jpg"),
    ("05", "full", "Disciplina<br>e istinto.", "Nello stesso spazio.", "6026285101857050208.jpg"),
    ("11", "full", "Il rosso dell'istinto.", "Il bianco dell'ordine.", "6028536901670735535.jpg"),
    ("06", "band", "La precisione<br>è rispetto.", "", "6026285101857050209.jpg"),
    ("07", "full", "Prima ci prendiamo<br>cura di te.", "Poi del taglio.", "6026285101857050211.jpg"),
    ("08", "band", "Schiuma calda.<br>Lama. Silenzio.", "", "ciotole-pulito.jpg"),
]
FINALE = ("Non è un taglio.<br>È un rituale.", "IMG20261026134721.jpg")
MANIFESTO = ("Ritual nasce da un'idea semplice: la cura di sé non è vanità, è disciplina.<br><br>"
             "Ogni appuntamento è un rito: tempo tuo, mani esperte, estratti naturali.<br><br>"
             "Che tu sia ordine o istinto, qui trovi il tuo.")
SEG = 3.3  # secondi per scena
BAND_Y = 525  # in coordinate 1080x1920


def testo(main, sub, size, top=None, bottom=None, grad=True):
    pos = f"top:{top}px" if top is not None else f"bottom:{bottom}px"
    g = ("<div style='position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.9) 0%,rgba(0,0,0,.5) 26%,rgba(0,0,0,0) 46%)'></div>"
         if grad else "")
    s = f"<div class=spec style='font-size:{int(size * .56)}px;margin-top:26px;color:#e9e2d6'>{sub}</div>" if sub else ""
    return (g + f"<div style='position:absolute;{pos};width:100%;text-align:center;padding:0 70px'>"
            f"<div style='width:120px;height:4px;background:{RED};margin:0 auto 30px'></div>"
            f"<div class=name style='font-size:{size}px;line-height:1.14'>{main}</div>{s}</div>")


def chiusura(big):
    k = 1 if big else .82
    return (f"<img src='{logo}' style='width:{int(420 * k)}px;margin-bottom:{int(60 * k)}px'>"
            f"<div class=name style='font-size:{int(80 * k)}px;line-height:1.12'>Prenota<br>il tuo posto.</div>"
            f"<div class=cta style='font-size:{int(38 * k)}px;padding:20px 40px;margin-top:{int(46 * k)}px'>Scrivici in DM</div>"
            f"<div class=note style='font-size:{int(30 * k)}px;margin-top:{int(40 * k)}px'>Corso Umberto I 300c · Bernalda</div>"
            f"<div class=spec style='font-size:{int(30 * k)}px;margin-top:14px'>@ritual_barberstudio</div>")


def foto(src, dst, w, h, cy=0.5, cx=0.5):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    r = w / h
    if im.width / im.height > r:
        cw, ch = int(im.height * r), im.height
    else:
        cw, ch = im.width, int(im.width / r)
    x = int(min(max(cx * im.width - cw / 2, 0), im.width - cw)); y = int(min(max(cy * im.height - ch / 2, 0), im.height - ch))
    tmp = dst.with_suffix(".src.jpg"); im.crop((x, y, x + cw, y + ch)).save(tmp, quality=97)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-vf",
                    f"scale={w}:{h}:flags=lanczos,unsharp=5:5:0.5,{GRADE}", "-q:v", "2", str(dst)], check=True)
    tmp.unlink()


def main():
    tmp = D / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    car = D / "carosello"; car.mkdir(exist_ok=True)
    for f in car.glob("*.jpg"):
        f.unlink()
    for i, s in enumerate(SCENE):
        foto(SRC / s[4], tmp / f"f{i}-45.jpg", 2160, 2700, cx=0.3 if "ciotole" in s[4] else 0.68 if s[4] == "6028536901670735536.jpg" else 0.5)
    foto(SRC / "6026285101857050206.jpg", tmp / "cover-45.jpg", 2160, 2700)
    foto(SRC / FINALE[1], tmp / "logo-band.jpg", 2560, 1440)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        band_bottom = BAND_Y + 608
        for i, (_, lay, main_, sub, _) in enumerate(SCENE):
            if lay == "full":
                render(pg, testo(main_, sub, 86, bottom=330), 1080, 1920, tmp / f"ov-{i}.png")
            else:
                render(pg, testo(main_, sub, 82, top=band_bottom + 110, grad=False), 1080, 1920, tmp / f"ov-{i}.png")
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex916}) center/cover'></div>",
               1080, 1920, tmp / "bg.png", transparent=False)
        render(pg, testo(FINALE[0], "", 86, top=band_bottom + 110, grad=False), 1080, 1920, tmp / "ov-fin.png")
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex916}) center/cover'></div>"
                   f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:240px 90px 340px'>{chiusura(True)}</div>",
               1080, 1920, tmp / "end.png", transparent=False)
        # carosello 4:5
        pg.set_viewport_size({"width": 1080, "height": 1350})
        render(pg, f"<div style='position:absolute;inset:0;background:#000 url({(tmp / 'cover-45.jpg').as_uri()}) center/cover'></div>"
                   "<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.6) 0%,rgba(0,0,0,0) 22%)'></div>"
                   f"<div style='position:absolute;top:56px;width:100%;text-align:center'><img src='{logo}' style='width:240px'></div>"
                   + testo("Benvenuto<br>nel Rituale.", "Corso Umberto I 300c · Bernalda", 92, bottom=90),
               1080, 1350, tmp / "c00.png", transparent=False)
        for i, (_, _, main_, sub, _) in enumerate(SCENE[1:], start=1):
            alto = SCENE[i][4] == "6028536901670735536.jpg"  # scacchiera: testo in alto per lasciare libera la targhetta
            txt = ("<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.92) 0%,rgba(0,0,0,.5) 26%,rgba(0,0,0,0) 44%)'></div>"
                   + testo(main_, sub, 74, top=80, grad=False)) if alto else testo(main_, sub, 74, bottom=90)
            render(pg, f"<div style='position:absolute;inset:0;background:#000 url({(tmp / f'f{i}-45.jpg').as_uri()}) center/cover'></div>"
                       + txt, 1080, 1350, tmp / f"c{i:02d}.png", transparent=False)
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex45}) center/cover'></div>"
                   f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:110px'>"
                   f"<div class=label style='font-size:28px'>Il nostro manifesto</div>"
                   f"<div class=name style='font-size:70px;margin:30px 0 40px'>Non è un taglio.<br>È un rituale.</div>"
                   f"<div class=spec style='font-size:34px;line-height:1.45;font-weight:600'>{MANIFESTO}</div></div>",
               1080, 1350, tmp / f"c{len(SCENE):02d}.png", transparent=False)
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex45}) center/cover'></div>"
                   f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:90px'>{chiusura(False)}</div>",
               1080, 1350, tmp / f"c{len(SCENE) + 1:02d}.png", transparent=False)
        b.close()
    for i in range(len(SCENE) + 2):
        Image.open(tmp / f"c{i:02d}.png").convert("RGB").save(car / f"{i + 1:02d}-salone.jpg", quality=95, subsampling=0)

    # reel
    full = f"scale=1440:2560:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:2560,fps=30,settb=AVTB,setsar=1,{GRADE}"
    band = f"scale=1440:810:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:810,fps=30,settb=AVTB,setsar=1,{GRADE}"
    ov = "scale=1440:2560:flags=lanczos,format=rgba"
    by = int(BAND_Y * 4 / 3)
    args = []; fc = ""; n = 0

    def inp(*a):
        nonlocal n
        args.extend(a); n += 1; return n - 1
    labels = []
    for i, (c, lay, *_rest) in enumerate(SCENE):
        v = inp("-t", str(SEG), "-i", str(CLIP / f"{c}.mp4"))
        o = inp("-loop", "1", "-t", str(SEG), "-i", str(tmp / f"ov-{i}.png"))
        if lay == "full":
            fc += f"[{v}:v]{full}[v{i}];"
        else:
            g = inp("-loop", "1", "-t", str(SEG), "-i", str(tmp / "bg.png"))
            fc += f"[{g}:v]scale=1440:2560,fps=30,settb=AVTB,setsar=1[g{i}];[{v}:v]{band}[b{i}];[g{i}][b{i}]overlay=0:{by}[v{i}];"
        fc += f"[{o}:v]{ov}[o{i}];[v{i}][o{i}]overlay=0:0:enable='gte(t,0.5)'[s{i}];"
        labels.append(f"s{i}")
    # insegna reale con frase finale
    g = inp("-loop", "1", "-t", str(SEG + 0.4), "-i", str(tmp / "bg.png"))
    l = inp("-i", str(tmp / "logo-band.jpg"))
    o = inp("-loop", "1", "-t", str(SEG + 0.4), "-i", str(tmp / "ov-fin.png"))
    d = int((SEG + 0.4) * 30)
    fc += (f"[{g}:v]scale=1440:2560,fps=30,settb=AVTB,setsar=1[gf];"
           f"[{l}:v]zoompan=z='min(1+0.0008*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={d}:s=1440x810:fps=30,settb=AVTB,setsar=1[lf];"
           f"[gf][lf]overlay=0:{by}[vf];[{o}:v]{ov}[of];[vf][of]overlay=0:0:enable='gte(t,0.5)'[sf];")
    labels.append("sf")
    e = inp("-i", str(tmp / "end.png"))
    fc += (f"[{e}:v]scale=2160:3840,zoompan=z='min(1+0.0004*on,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
           f":d=120:s=1440x2560:fps=30,settb=AVTB,setsar=1[se];")
    labels.append("se")
    durs = [SEG] * len(SCENE) + [SEG + 0.4, 4.0]
    prev = labels[0]; off = 0.0
    for i in range(1, len(labels)):
        off += durs[i - 1] - 0.5
        tr = "fadeblack" if i >= len(labels) - 2 else "fade"
        fc += f"[{prev}][{labels[i]}]xfade=transition={tr}:duration=0.5:offset={off:.2f}[x{i}];"; prev = f"x{i}"
    fc += f"[{prev}]format=yuv420p[out]"
    out = D / "reel-salone.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", fc, "-map", "[out]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-maxrate", "25M", "-bufsize", "50M",
                    "-movflags", "+faststart", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    main()
