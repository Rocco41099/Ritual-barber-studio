"""'Due nature': Apollineo a sinistra (oro), Dionisiaco a destra (rosso). Reel a schermo diviso,
carosello 4:5 e post singolo.

Uso: python3 tools/poli.py
Richiede media/instagram/rituali/apollineo e dionisiaco con clip-1..3.mp4 e still-1..3.jpg.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from prodotto import render, ASSETS
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "media/instagram/rituali"; A = R / "apollineo"; Dn = R / "dionisiaco"; D = R / "due-nature"
GOLD = "#C9A45C"; WINE = "#B0263A"
logo = (ASSETS / "logo.png").as_uri()
tex916 = (ASSETS / "tex-916.jpg").as_uri(); tex45 = (ASSETS / "tex-45.jpg").as_uri()
COPPIE = [("Ordine.", "Istinto."), ("Misura.", "Eccesso."), ("Controllo.", "Libertà.")]
LUNGA = max((w for c in COPPIE for w in c), key=len)
TITOLO = "Due nature.<br>Un solo Rituale."
SOTTO = "L'ordine ti dà la forma.<br>L'istinto ti dà il carattere."
CHIUSA = "Ogni uomo<br>li ha entrambi.<br>Noi li curiamo<br>tutti e due."


FIT = ("<script>document.fonts.ready.then(()=>{const els=[...document.querySelectorAll('.fit')];"
       "let m=Math.min(...els.map(e=>{let s=parseFloat(e.style.fontSize);"
       "while(e.scrollWidth>e.parentElement.clientWidth&&s>20){s-=2;e.style.fontSize=s+'px'}return s}));els.forEach(e=>e.style.fontSize=m+'px')})</script>")


def divisore(h):
    return (f"<div style='position:absolute;left:50%;top:0;width:4px;height:{h}px;margin-left:-2px;"
            f"background:linear-gradient(180deg,{GOLD},{WINE})'></div>")


def coppia(a, d, size, bottom, h):
    side = lambda t, col, left: (f"<div style='position:absolute;bottom:{bottom}px;{'left' if left else 'right'}:0;width:50%;text-align:center'>"
                                 f"<div class=rit style='font-size:{int(size * .3)}px;color:{col};border-color:{col}'>{'Apollineo' if left else 'Dionisiaco'}</div>"
                                 f"<div class='name fit' style='font-size:{size}px;margin-top:22px;color:{col};white-space:nowrap;padding:0 36px'>{t}</div></div>")
    return ("<div style='position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.9) 0%,rgba(0,0,0,.45) 26%,rgba(0,0,0,0) 44%)'></div>"
            + divisore(h) + side(a, GOLD, True) + side(d, WINE, False)
            + f"<div style='position:absolute;left:0;top:0;width:50%;visibility:hidden'><div class='name fit' style='font-size:{size}px;white-space:nowrap;padding:0 36px'>{LUNGA}</div></div>" + FIT)


def split_bg(a, d):
    return (f"<div style='position:absolute;left:0;top:0;width:50%;height:100%;background:#000 url({a}) center/cover'></div>"
            f"<div style='position:absolute;right:0;top:0;width:50%;height:100%;background:#000 url({d}) center/cover'></div>")


def messaggio(big):
    return (f"<div class=name style='font-size:{100 if big else 82}px;line-height:1.1'>{TITOLO}</div>"
            f"<div style='width:120px;height:4px;background:linear-gradient(90deg,{GOLD},{WINE});margin:{44 if big else 34}px auto'></div>"
            f"<div class=spec style='font-size:{44 if big else 36}px;line-height:1.35'>{SOTTO}</div>")


def main():
    tmp = D / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    car = D / "carosello"; car.mkdir(exist_ok=True)
    au = lambda i: (A / f"still-{i}.jpg").as_uri()
    du = lambda i: (Dn / f"still-{i}.jpg").as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        for i, (a, d) in enumerate(COPPIE):
            render(pg, coppia(a, d, 96, 330, 1920), 1080, 1920, tmp / f"ov-{i + 1}.png")
        render(pg, split_bg(au(3), du(1)) + "<div style='position:absolute;inset:0;background:rgba(0,0,0,.62)'></div>" + divisore(1920)
                   + f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 80px'>"
                   f"<div style='background:rgba(0,0,0,.55);padding:60px 50px'>{messaggio(True)}</div></div>",
               1080, 1920, tmp / "msg.png", transparent=False)
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex916}) center/cover'></div>"
                   f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:240px 90px 340px'>"
                   f"<img src='{logo}' style='width:420px;margin-bottom:70px'>"
                   f"<div style='display:flex;gap:24px;justify-content:center'><div class=rit style='font-size:26px;color:{GOLD};border-color:{GOLD}'>Apollineo</div>"
                   f"<div class=rit style='font-size:26px;color:{WINE};border-color:{WINE}'>Dionisiaco</div></div>"
                   f"<div class=name style='font-size:66px;line-height:1.15;margin-top:50px'>{CHIUSA}</div>"
                   f"<div class=cta style='font-size:36px;padding:20px 40px;margin-top:50px'>Scrivici A o D in DM</div>"
                   f"<div class=note style='font-size:30px;margin-top:40px'>Corso Umberto I 300c · Bernalda</div></div>",
               1080, 1920, tmp / "end.png", transparent=False)
        # carosello 4:5
        pg.set_viewport_size({"width": 1080, "height": 1350})
        for i, (a, d) in enumerate(COPPIE):
            render(pg, split_bg(au(i + 1), du(i + 1)) + coppia(a, d, 84, 90, 1350), 1080, 1350, tmp / f"c{i + 1}.png", transparent=False)
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex45}) center/cover'></div>" + divisore(1350)
                   + f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:90px'>"
                   f"<div style='background:rgba(9,9,10,.92);padding:50px 40px'><img src='{logo}' style='width:280px;margin-bottom:44px'>{messaggio(False)}"
                   f"<div class=cta style='font-size:30px;padding:18px 36px;margin-top:44px'>Scrivici A o D in DM</div></div></div>",
               1080, 1350, tmp / "c4.png", transparent=False)
        # post singolo
        render(pg, split_bg(au(3), du(1)) + "<div style='position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.95) 0%,rgba(0,0,0,.6) 38%,rgba(0,0,0,.1) 60%)'></div>"
                   + "<div style='position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.75) 0%,rgba(0,0,0,0) 22%)'></div>" + divisore(1350) + f"<div style='position:absolute;top:44px;width:100%;text-align:center'><img src='{logo}' style='width:230px;background:rgba(0,0,0,.6);padding:14px 22px'></div>"
                   f"<div style='position:absolute;bottom:80px;width:100%;text-align:center;padding:0 60px'>{messaggio(False)}</div>",
               1080, 1350, tmp / "post.png", transparent=False)
        b.close()
    for i in range(1, 5):
        Image.open(tmp / f"c{i}.png").convert("RGB").save(car / f"{i:02d}-due-nature.jpg", quality=95, subsampling=0)
    Image.open(tmp / "post.png").convert("RGB").save(D / "post-due-nature.jpg", quality=95, subsampling=0)

    half = "scale=1440:2560:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:2560,crop=720:2560,fps=30,settb=AVTB,setsar=1"
    ov = "scale=1440:2560:flags=lanczos,format=rgba"
    zp = ("scale=2160:3840,zoompan=z='min(1+0.0004*on,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          ":d={d}:s=1440x2560:fps=30,settb=AVTB,setsar=1")
    T = 4.0; args = []; fc = ""
    for i in range(3):
        args += ["-t", str(T), "-i", str(A / f"clip-{i + 1}.mp4"), "-t", str(T), "-i", str(Dn / f"clip-{i + 1}.mp4"),
                 "-loop", "1", "-t", str(T), "-i", str(tmp / f"ov-{i + 1}.png")]
        a, d, o = 3 * i, 3 * i + 1, 3 * i + 2
        fc += (f"[{a}:v]{half}[l{i}];[{d}:v]{half}[r{i}];[l{i}][r{i}]hstack[h{i}];[{o}:v]{ov}[o{i}];"
               f"[h{i}][o{i}]overlay=0:0:enable='gte(t,0.4)'[s{i}];")
    args += ["-i", str(tmp / "msg.png"), "-i", str(tmp / "end.png")]
    fc += f"[9:v]{zp.format(d=120)}[s3];[10:v]{zp.format(d=120)}[e];"
    durs = [T, T, T, 4.0]; prev = "s0"; off = 0.0
    for i in range(1, 4):
        off += durs[i - 1] - 0.6
        fc += f"[{prev}][s{i}]xfade=transition=fadeblack:duration=0.6:offset={off:.2f}[x{i}];"; prev = f"x{i}"
    off += durs[3] - 0.6
    fc += f"[{prev}][e]xfade=transition=fadeblack:duration=0.6:offset={off:.2f}[v];[v]format=yuv420p[out]"
    out = D / "reel-due-nature.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", fc, "-map", "[out]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-maxrate", "25M", "-bufsize", "50M",
                    "-movflags", "+faststart", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    main()
