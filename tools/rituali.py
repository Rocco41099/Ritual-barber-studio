"""Carosello 'Quale rituale sei?' (4:5), storie 9:16 e reel, piu' post regalo.

Uso: python3 tools/rituali.py   (richiede media/instagram/rituali/apollineo-916.jpg, dionisiaco-916.jpg)
     python3 tools/rituali.py regalo   (richiede media/instagram/regalo/regalo-916.jpg)
"""
import subprocess, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from prodotto import render, crop45, BASE, ASSETS, RED, SOFT
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
GOLD = "#C9A45C"; WINE = "#B0263A"
logo = (ASSETS / "logo.png").as_uri()
tex916 = (ASSETS / "tex-916.jpg").as_uri(); tex45 = (ASSETS / "tex-45.jpg").as_uri()

R = {
 "apollineo": dict(col=GOLD, title="Rituale Apollineo", words="Ordine. Misura. Controllo.",
   lines=["Ogni linea al suo posto.", "Ogni settimana, lo stesso gesto.", "La disciplina non ti limita:<br>ti definisce."],
   serv="Sfumatura a pelle precisa · Barba disegnata · Abbonamento settimanale",
   prod="Amarone · Primitivo · Gran Paradiso · Monte Bianco · Virgilio"),
 "dionisiaco": dict(col=WINE, title="Rituale Dionisiaco", words="Istinto. Eccesso. Libertà.",
   lines=["Le regole sono per chi<br>non ha stile.", "Taglia, rompi, ricomincia.", "Il tuo istinto è il tuo specchio."],
   serv="Wolf cut · Mullet sfumato · Texture · Trasformazioni",
   prod="Bonarda · Nebbiolo · Chianti · Nero d'Avola · Caronte"),
}


def bg(url, grad):
    return f"<div style='position:absolute;inset:0;background:#000 url({url}) center/cover'></div><div style='position:absolute;inset:0;background:{grad}'></div>"


def center(inner, pad):
    return f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:{pad}'>{inner}</div>"


def lab(text, col, size):
    return (f"<div style='font-weight:700;letter-spacing:.3em;color:{col};text-transform:uppercase;display:flex;align-items:center;gap:24px;justify-content:center;font-size:{size}px'>"
            f"<span style='width:70px;height:3px;background:{col}'></span>{text}<span style='width:70px;height:3px;background:{col}'></span></div>")


def rituali():
    d = ROOT / "media/instagram/rituali"; tmp = d / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    car = d / "carosello"; car.mkdir(exist_ok=True); st = d / "storie"; st.mkdir(exist_ok=True)
    for k in R:
        crop45(d / f"{k}-916.jpg", tmp / f"{k}-45.jpg")
    A, D = R["apollineo"], R["dionisiaco"]
    a45 = (tmp / "apollineo-45.jpg").as_uri(); d45 = (tmp / "dionisiaco-45.jpg").as_uri()
    a916 = (d / "apollineo-916.jpg").as_uri(); d916 = (d / "dionisiaco-916.jpg").as_uri()
    dark = "linear-gradient(0deg,rgba(0,0,0,.92) 0%,rgba(0,0,0,.55) 45%,rgba(0,0,0,.35) 100%)"
    slides45 = {
     "01-quale-rituale-sei": f"""<div style='position:absolute;left:0;top:0;width:50%;height:100%;background:#000 url({a45}) 30% center/cover'></div>
<div style='position:absolute;right:0;top:0;width:50%;height:100%;background:#000 url({d45}) 70% center/cover'></div>
<div style='position:absolute;left:50%;top:0;width:4px;height:100%;background:{RED}'></div>
<div style='position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.9) 0%,rgba(0,0,0,.2) 55%,rgba(0,0,0,.6) 100%)'></div>
<div style='position:absolute;top:70px;width:100%;text-align:center'><img src='{logo}' style='width:240px'></div>
<div style='position:absolute;bottom:80px;width:100%;text-align:center;padding:0 60px'>
<div style='display:flex;justify-content:space-between;padding:0 30px;margin-bottom:40px'>
<div class=rit style='font-size:26px;color:{GOLD};border-color:{GOLD}'>Apollineo</div><div class=rit style='font-size:26px;color:{WINE};border-color:{WINE}'>Dionisiaco</div></div>
<div class=name style='font-size:74px'>Due rituali.<br>Un solo specchio.</div>
<div class=name style='font-size:96px;color:{RED};margin-top:20px'>Quale sei?</div></div>""",
    }
    for i, (k, r) in enumerate((("apollineo", A), ("dionisiaco", D)), start=2):
        u = a45 if k == "apollineo" else d45
        lines = "".join(f"<div class=spec style='font-size:44px;margin:14px 0'>{l}</div>" for l in r["lines"])
        slides45[f"0{i}-{k}"] = bg(u, dark) + f"""<div style='position:absolute;bottom:80px;width:100%;text-align:center;padding:0 70px'>
{lab('Rituale', r['col'], 30)}
<div class=name style='font-size:110px;color:{r['col']};margin:18px 0 30px'>{k.capitalize()}</div>
{lines}
<div class=name style='font-size:46px;margin-top:34px;color:{r['col']}'>{r['words']}</div></div>"""
    slides45["04-per-te"] = bg(tex45, "rgba(0,0,0,.2)") + center(f"""
<img src='{logo}' style='width:220px;margin-bottom:46px'>
{lab('Il tuo rituale in salone', RED, 26)}
<div style='margin-top:46px;width:100%'>
<div class=name style='font-size:58px;color:{GOLD}'>Apollineo</div>
<div class=spec style='font-size:34px;margin-top:12px'>{A['serv']}</div>
<div class=note style='font-size:30px;margin-top:10px'>{A['prod']}</div></div>
<div style='width:120px;height:4px;background:{RED};margin:44px 0'></div>
<div style='width:100%'><div class=name style='font-size:58px;color:{WINE}'>Dionisiaco</div>
<div class=spec style='font-size:34px;margin-top:12px'>{D['serv']}</div>
<div class=note style='font-size:30px;margin-top:10px'>{D['prod']}</div></div>""", "90px 80px")
    slides45["05-scrivici"] = bg(tex45, "rgba(0,0,0,.2)") + center(f"""
<img src='{logo}' style='width:480px;margin-bottom:60px'>
<div class=name style='font-size:78px'>Quale rituale sei?</div>
<div style='display:flex;gap:40px;margin:56px 0'>
<div class=name style='font-size:120px;color:{GOLD};border:4px solid {GOLD};width:190px;height:190px;display:flex;align-items:center;justify-content:center'>A</div>
<div class=name style='font-size:120px;color:{WINE};border:4px solid {WINE};width:190px;height:190px;display:flex;align-items:center;justify-content:center'>D</div></div>
<div class=cta style='font-size:40px;padding:20px 44px'>Scrivici A o D in DM</div>
<div class=note style='font-size:32px;margin-top:30px'>Ti consigliamo taglio, prodotti e abbonamento</div>""", "90px")
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome"); pg = b.new_page(device_scale_factor=2)
        for n, html in slides45.items():
            render(pg, html, 1080, 1350, tmp / f"{n}.png", transparent=False)
            Image.open(tmp / f"{n}.png").convert("RGB").save(car / f"{n}.jpg", quality=95, subsampling=0)
        # storie 9:16
        for k, r in (("apollineo", A), ("dionisiaco", D)):
            u = a916 if k == "apollineo" else d916
            lines = "".join(f"<div class=spec style='font-size:50px;margin:16px 0'>{l}</div>" for l in r["lines"])
            render(pg, bg(u, dark) + f"""<div style='position:absolute;bottom:360px;width:100%;text-align:center;padding:0 70px'>
{lab('Rituale', r['col'], 32)}<div class=name style='font-size:124px;color:{r['col']};margin:20px 0 34px'>{k.capitalize()}</div>
{lines}<div class=name style='font-size:52px;margin-top:40px;color:{r['col']}'>{r['words']}</div></div>
<div style='position:absolute;top:220px;width:100%;text-align:center'><img src='{logo}' style='width:260px'></div>""",
                   1080, 1920, st / f"{k}.png", transparent=False)
        render(pg, f"""<div style='position:absolute;left:0;top:0;width:100%;height:50%;background:#000 url({a916}) center 40%/cover'></div>
<div style='position:absolute;left:0;bottom:0;width:100%;height:50%;background:#000 url({d916}) center 60%/cover'></div>
<div style='position:absolute;left:0;top:50%;width:100%;height:4px;background:{RED}'></div>
<div style='position:absolute;inset:0;background:rgba(0,0,0,.35)'></div>
<div style='position:absolute;top:260px;width:100%;text-align:center'><div class=name style='font-size:110px;color:{GOLD}'>Apollineo</div><div class=spec style='font-size:42px'>Ordine. Misura. Controllo.</div></div>
<div style='position:absolute;bottom:420px;width:100%;text-align:center'><div class=name style='font-size:110px;color:{WINE}'>Dionisiaco</div><div class=spec style='font-size:42px'>Istinto. Eccesso. Libertà.</div></div>
<div style='position:absolute;top:50%;width:100%;text-align:center;transform:translateY(-50%)'><div class=name style='display:inline-block;font-size:72px;background:#000;padding:18px 46px;border:3px solid {RED}'>Quale sei?</div></div>""",
               1080, 1920, st / "sondaggio.png", transparent=False)
        b.close()
    # reel dalle storie + chiusura
    inputs = [st / "sondaggio.png", st / "apollineo.png", st / "dionisiaco.png"]
    end = tmp / "end.png"
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome"); pg = b.new_page(device_scale_factor=2)
        render(pg, bg(tex916, "rgba(0,0,0,.2)") + center(f"""<img src='{logo}' style='width:560px;margin-bottom:70px'>
<div class=name style='font-size:84px'>Due rituali.<br>Un solo specchio.</div>
<div class=cta style='font-size:44px;padding:22px 46px;margin-top:60px'>Scrivici A o D in DM</div>""", "240px 90px 340px"),
               1080, 1920, end, transparent=False)
        b.close()
    inputs.append(end)
    reel(inputs, [3.2, 3.6, 3.6, 3.0], d / "reel-rituali.mp4")


def reel(imgs, durs, out):
    args = []; fc = ""
    for i, (im, du) in enumerate(zip(imgs, durs)):
        args += ["-i", str(im)]
        fc += (f"[{i}:v]scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,"
               f"zoompan=z='min(1+0.0007*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(du*30)}:s=1440x2560:fps=30,setsar=1[s{i}];")
    prev = "s0"; off = 0
    for i in range(1, len(imgs)):
        off += durs[i - 1] - 0.5
        fc += f"[{prev}][s{i}]xfade=transition=fadeblack:duration=0.5:offset={off:.2f}[x{i}];"; prev = f"x{i}"
    fc += f"[{prev}]format=yuv420p[o]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", fc, "-map", "[o]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-movflags", "+faststart", str(out)], check=True)
    print(out)


def regalo():
    d = ROOT / "media/instagram/regalo"; tmp = d / "_tmp"; tmp.mkdir(parents=True, exist_ok=True)
    crop45(d / "regalo-916.jpg", tmp / "regalo-45.jpg")
    g45 = (tmp / "regalo-45.jpg").as_uri(); g916 = (d / "regalo-916.jpg").as_uri()
    grad = "linear-gradient(0deg,rgba(0,0,0,.94) 0%,rgba(0,0,0,.7) 34%,rgba(0,0,0,0) 56%)"

    def body(big):
        s = (lambda a, b_: a if big else b_)
        return f"""{lab('Idee regalo per lui', RED, s(32, 28))}
<div class=name style='font-size:{s(104, 86)}px;margin:{s(24, 18)}px 0'>Il regalo perfetto<br>ha carattere.</div>
<div class=spec style='font-size:{s(44, 36)}px'>Cura uomo Made in Italy con <b>estratti naturali</b>:</div>
<div class=note style='font-size:{s(40, 32)}px;margin-top:8px'>vinaccioli, argan, stella alpina, caffeina</div>
<div class=cta style='font-size:{s(44, 38)}px;padding:20px 44px;margin-top:{s(40, 30)}px'>Regala un rituale</div>
<div class=spec style='font-size:{s(36, 30)}px;margin-top:{s(28, 22)}px;color:{SOFT}'>Scegli il suo in salone · Corso Umberto I 300c</div>"""
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome"); pg = b.new_page(device_scale_factor=2)
        render(pg, bg(g45, grad) + f"<div style='position:absolute;top:56px;width:100%;text-align:center'><img src='{logo}' style='width:230px'></div>"
               f"<div style='position:absolute;bottom:60px;width:100%;text-align:center;padding:0 60px'>{body(False)}</div>",
               1080, 1350, tmp / "post.png", transparent=False)
        render(pg, bg(g916, grad) + f"<div style='position:absolute;top:220px;width:100%;text-align:center'><img src='{logo}' style='width:280px'></div>"
               f"<div style='position:absolute;bottom:360px;width:100%;text-align:center;padding:0 60px'>{body(True)}</div>",
               1080, 1920, d / "storia-regalo.png", transparent=False)
        b.close()
    Image.open(tmp / "post.png").convert("RGB").save(d / "post-regalo.jpg", quality=95, subsampling=0)
    print(d)


if __name__ == "__main__":
    regalo() if sys.argv[1:] == ["regalo"] else rituali()
