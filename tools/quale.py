"""'Quale rituale sei?': test a 5 scelte, A (Apollineo, oro, sinistra) contro D (Dionisiaco, rosso, destra).
Reel a schermo diviso, carosello 4:5 da 7 slide, 5 storie 9:16 con lo spazio per il sondaggio.

Uso: python3 tools/quale.py
Richiede media/instagram/rituali/quale-rituale/ con a1..a5.jpg, d1..d5.jpg (fotogrammi) e a1..a5.mp4, d1..d5.mp4 (clip).
Regola: il reel chiude sul logo.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from prodotto import render, ASSETS
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "media/instagram/rituali/quale-rituale"
GOLD = "#C9A45C"; WINE = "#B0263A"
logo = (ASSETS / "logo.png").as_uri()
tex916 = (ASSETS / "tex-916.jpg").as_uri(); tex45 = (ASSETS / "tex-45.jpg").as_uri()
SCELTE = [
    ("La mattina", "Sveglia<br>alle 6.", "La notte<br>non finisce."),
    ("La strada", "Motore lucido.", "Fumo e asfalto."),
    ("La barba", "Linea perfetta.", "Barba libera."),
    ("La musica", "Un vinile,<br>un whisky.", "Amplificatore<br>al massimo."),
    ("Lo stile", "Abito su misura.", "Giacca di pelle."),
]
FIT = ("<script>document.fonts.ready.then(()=>{const els=[...document.querySelectorAll('.fit')];"
       "let m=Math.min(...els.map(e=>{let s=parseFloat(e.style.fontSize);"
       "while((e.scrollWidth>e.parentElement.clientWidth||e.scrollHeight>e.clientHeight+4)&&s>20){s-=2;e.style.fontSize=s+'px'}return s}));"
       "els.forEach(e=>e.style.fontSize=m+'px')})</script>")
LUNGHE = [max((s[1] for s in SCELTE), key=len), max((s[2] for s in SCELTE), key=len)]


def split(a, d, pos="center"):
    return (f"<div style='position:absolute;left:0;top:0;width:50%;height:100%;background:#000 url({a}) {pos}/cover'></div>"
            f"<div style='position:absolute;right:0;top:0;width:50%;height:100%;background:#000 url({d}) {pos}/cover'></div>")


def divisore(h, top=0):
    return (f"<div style='position:absolute;left:50%;top:{top}px;width:4px;height:{h - top}px;margin-left:-2px;"
            f"background:linear-gradient(180deg,{GOLD},{WINE})'></div>")


def testata(tema, n, size):
    band = int(size * 3.6)
    return (f"<div style='position:absolute;top:0;left:0;right:0;height:{band}px;background:#050505'></div>"
            f"<div style='position:absolute;top:{band}px;left:0;right:0;height:{int(size * 2.4)}px;background:linear-gradient(180deg,rgba(5,5,5,1),rgba(0,0,0,0))'></div>"
            f"<div style='position:absolute;top:{int(size * 0.9)}px;width:100%;text-align:center'>"
            f"<div class=label style='font-size:{int(size * .55)}px'>Quale rituale sei? · {n}/5</div>"
            f"<div class=name style='font-size:{size}px;margin-top:14px'>{tema}</div></div>")


def scelte(a, d, size, bottom, h, top=0):
    def lato(t, col, lettera, nome, left):
        return (f"<div style='position:absolute;bottom:{bottom}px;{'left' if left else 'right'}:0;width:50%;text-align:center'>"
                f"<div style='display:inline-flex;align-items:center;gap:14px'>"
                f"<div style='width:{int(size * .9)}px;height:{int(size * .9)}px;border:3px solid {col};color:{col};display:flex;align-items:center;justify-content:center;font-family:Cinzel;font-weight:800;font-size:{int(size * .55)}px;background:rgba(0,0,0,.5)'>{lettera}</div>"
                f"<div class=label style='font-size:{int(size * .3)}px;color:{col}'>{nome}</div></div>"
                f"<div class='name fit' style='font-size:{size}px;margin-top:22px;line-height:1.1;padding:0 30px;height:{int(size * 2.3)}px;display:flex;align-items:flex-start;justify-content:center'>{t}</div></div>")
    misura = "".join(f"<div style='position:absolute;left:0;top:0;width:50%;visibility:hidden'><div class='name fit' style='font-size:{size}px;line-height:1.1;padding:0 30px;height:{int(size * 2.3)}px;white-space:normal'>{t}</div></div>" for t in LUNGHE)
    return ("<div style='position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.94) 0%,rgba(0,0,0,.55) 30%,rgba(0,0,0,0) 48%)'></div>"
            + divisore(h, top) + lato(a, GOLD, "A", "Apollineo", True) + lato(d, WINE, "D", "Dionisiaco", False) + misura + FIT)


def risultati(size):
    blocco = lambda col, lettera, titolo, parole, servizi: (
        f"<div style='border-left:5px solid {col};padding:6px 0 6px 28px;margin:0 0 46px;text-align:left'>"
        f"<div class=name style='font-size:{size}px;color:{col}'>Più {lettera}: {titolo}</div>"
        f"<div class=spec style='font-size:{int(size * .52)}px;margin-top:10px'>{parole}</div>"
        f"<div class=note style='font-size:{int(size * .44)}px;margin-top:8px'>{servizi}</div></div>")
    return (blocco(GOLD, "A", "sei Apollineo.", "Ordine. Misura. Controllo.", "Sfumatura a pelle · Barba disegnata")
            + blocco(WINE, "D", "sei Dionisiaco.", "Istinto. Eccesso. Libertà.", "Texture · Mullet · Trasformazioni"))


def main():
    tmp = D / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    car = D / "carosello"; car.mkdir(exist_ok=True); st = D / "storie"; st.mkdir(exist_ok=True)
    A = lambda i: (D / f"a{i}.jpg").as_uri(); Dd = lambda i: (D / f"d{i}.jpg").as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        # reel: overlay per ogni scelta, apertura, chiusura
        for i, (tema, a, d) in enumerate(SCELTE, start=1):
            render(pg, testata(tema, i, 78) + scelte(a, d, 78, 300, 1920, int(78 * 3.6)), 1080, 1920, tmp / f"ov-{i}.png")
        apertura = (split(A(1), Dd(1)) + "<div style='position:absolute;inset:0;background:rgba(0,0,0,.3)'></div>" + divisore(1920)
                    + "<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 70px'>"
                    f"<img src='{logo}' style='width:300px;margin-bottom:60px'>"
                    "<div style='background:rgba(5,5,5,.9);padding:60px 60px'><div class=name style='font-size:120px;line-height:1.05'>Quale<br>rituale<br>sei?</div>"
                    f"<div style='width:140px;height:5px;background:linear-gradient(90deg,{GOLD},{WINE});margin:50px auto'></div>"
                    "<div class=spec style='font-size:44px;line-height:1.35'>5 scelte. Conta le A e le D.</div></div></div>")
        render(pg, apertura, 1080, 1920, tmp / "intro.png", transparent=False)
        chiusura = (f"<div style='position:absolute;inset:0;background:#09090a url({tex916}) center/cover'></div>"
                    "<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:200px 90px 300px'>"
                    f"<img src='{logo}' style='width:380px;margin-bottom:60px'>"
                    "<div class=name style='font-size:84px;line-height:1.1'>Più A o più D?</div>"
                    "<div class=spec style='font-size:44px;margin:24px 0 60px'>Scrivilo nei commenti.</div>"
                    f"<div style='width:100%'>{risultati(52)}</div>"
                    "<div class=note style='font-size:30px'>Corso Umberto I 300c · Bernalda</div></div>")
        render(pg, chiusura, 1080, 1920, tmp / "end.png", transparent=False)
        # storie con spazio per il sondaggio
        for i, (tema, a, d) in enumerate(SCELTE, start=1):
            render(pg, split(A(i), Dd(i)) + testata(tema, i, 78) + scelte(a, d, 74, 330, 1920, int(78 * 3.6))
                       + "<div style='position:absolute;top:780px;width:100%;text-align:center'>"
                       "<div class=label style='font-size:24px;opacity:.75'>Vota qui sotto</div></div>",
                   1080, 1920, st / f"{i:02d}-quale-rituale.png", transparent=False)
        # carosello 4:5
        pg.set_viewport_size({"width": 1080, "height": 1350})
        render(pg, split(A(1), Dd(1)) + "<div style='position:absolute;inset:0;background:rgba(0,0,0,.3)'></div>" + divisore(1350)
                   + "<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 70px'>"
                   f"<img src='{logo}' style='width:240px;margin-bottom:46px'>"
                   "<div style='background:rgba(5,5,5,.9);padding:50px 60px'><div class=name style='font-size:104px;line-height:1.05'>Quale<br>rituale sei?</div>"
                   f"<div style='width:140px;height:5px;background:linear-gradient(90deg,{GOLD},{WINE});margin:40px auto'></div>"
                   "<div class=spec style='font-size:38px'>5 scelte. Scorri e conta le A e le D.</div></div></div>",
               1080, 1350, tmp / "c0.png", transparent=False)
        for i, (tema, a, d) in enumerate(SCELTE, start=1):
            render(pg, split(A(i), Dd(i)) + testata(tema, i, 64) + scelte(a, d, 66, 70, 1350, int(64 * 3.6)), 1080, 1350, tmp / f"c{i}.png", transparent=False)
        render(pg, f"<div style='position:absolute;inset:0;background:#09090a url({tex45}) center/cover'></div>"
                   "<div style='position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:90px 100px'>"
                   "<div style='text-align:center'><div class=label style='font-size:28px'>Il tuo risultato</div>"
                   "<div class=name style='font-size:76px;margin:20px 0 60px'>Più A o più D?</div></div>"
                   f"{risultati(56)}"
                   "<div style='text-align:center'><div class=cta style='font-size:32px;padding:18px 36px'>Scrivilo nei commenti</div></div></div>",
               1080, 1350, tmp / "c6.png", transparent=False)
        b.close()
    for i in range(7):
        Image.open(tmp / f"c{i}.png").convert("RGB").save(car / f"{i + 1:02d}-quale-rituale.jpg", quality=95, subsampling=0)

    # reel
    half = "scale=1440:2560:force_original_aspect_ratio=increase:flags=lanczos,crop=1440:2560,crop=720:2560,fps=30,settb=AVTB,setsar=1"
    ov = "scale=1440:2560:flags=lanczos,format=rgba"
    zp = ("scale=2160:3840,zoompan=z='min(1+0.0005*on,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          ":d={d}:s=1440x2560:fps=30,settb=AVTB,setsar=1")
    T = 3.4; args = ["-i", str(tmp / "intro.png")]; fc = f"[0:v]{zp.format(d=75)}[s0];"
    for i in range(1, 6):
        args += ["-t", str(T), "-i", str(D / f"a{i}.mp4"), "-t", str(T), "-i", str(D / f"d{i}.mp4"),
                 "-loop", "1", "-t", str(T), "-i", str(tmp / f"ov-{i}.png")]
        a, d, o = 3 * i - 2, 3 * i - 1, 3 * i
        fc += (f"[{a}:v]{half}[l{i}];[{d}:v]{half}[r{i}];[l{i}][r{i}]hstack[h{i}];[{o}:v]{ov}[o{i}];"
               f"[h{i}][o{i}]overlay=0:0:enable='gte(t,0.3)'[s{i}];")
    args += ["-i", str(tmp / "end.png")]
    fc += f"[16:v]{zp.format(d=150)}[s6];"
    durs = [2.5] + [T] * 5 + [5.0]; prev = "s0"; off = 0.0
    for i in range(1, 7):
        off += durs[i - 1] - 0.4
        fc += f"[{prev}][s{i}]xfade=transition={'fadeblack' if i in (1, 6) else 'slideleft'}:duration=0.4:offset={off:.2f}[x{i}];"; prev = f"x{i}"
    fc += f"[{prev}]format=yuv420p[out]"
    out = D / "reel-quale-rituale.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", fc, "-map", "[out]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-maxrate", "25M", "-bufsize", "50M",
                    "-movflags", "+faststart", str(out)], check=True)
    print(out)


if __name__ == "__main__":
    main()
