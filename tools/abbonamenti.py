"""Genera le grafiche abbonamenti in due formati: 9:16 (reel/storie) e 4:5 (feed).

Uso: python3 tools/abbonamenti.py  -> scrive i PNG in media/instagram/abbonamenti-v2/
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "media/instagram/abbonamenti-v2"
ASSETS = OUT / "assets"

RED = "#d0283c"
INK = "#f6f3ee"
SOFT = "#c9c3b9"

PLANS = [
    dict(price="15", was="40", save="25", freq="Ogni settimana", visits="4 visite al mese",
         items=["Linee barba", "Pulizia collo", "Contorno e basette o punti luce"]),
    dict(price="25", was="36", save="11", freq="Ogni 2 settimane", visits="2 visite al mese",
         items=["Linee barba", "Pulizia collo", "Ritocco sfumatura"]),
    dict(price="30", was="43", save="13", freq="Ogni 2 settimane", visits="2 visite al mese",
         items=["Linee barba", "Pulizia collo", "Ritocco sfumatura"], plus="1 taglio e shampoo al mese"),
    dict(price="36", was="53", save="17", freq="Ogni 2 settimane", visits="2 visite al mese",
         items=["Disegno linee e modellatura barba", "Pulizia collo", "Ritocco sfumatura"],
         plus="1 taglio e shampoo al mese", badge="Il più completo"),
]


def css(fmt):
    tall = fmt == "916"
    return f"""
@font-face{{font-family:Cinzel;font-weight:700;src:url(assets/cinzel-latin-700-normal.woff2)}}
@font-face{{font-family:Cinzel;font-weight:800;src:url(assets/cinzel-latin-800-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:500;src:url(assets/montserrat-latin-500-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:600;src:url(assets/montserrat-latin-600-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:700;src:url(assets/montserrat-latin-700-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:800;src:url(assets/montserrat-latin-800-normal.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:{1920 if tall else 1350}px;background:#09090a;overflow:hidden}}
.s{{position:relative;width:100%;height:100%;color:{INK};font-family:Mont;
  display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
  padding:{'240px 96px 340px' if tall else '110px 96px'}}}
.bg{{position:absolute;inset:0;background:url(assets/tex-{fmt}.jpg) center/cover;opacity:.75}}
.vig{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 0%,rgba(0,0,0,.55) 70%,rgba(0,0,0,.85) 100%)}}
.frame{{position:absolute;inset:40px;border:1.5px solid rgba(255,255,255,.22)}}
.c{{position:relative;width:100%;display:flex;flex-direction:column;align-items:center}}
.logo{{width:{300 if tall else 250}px;margin-bottom:{70 if tall else 44}px}}
.logo.big{{width:{620 if tall else 520}px;margin-bottom:{90 if tall else 56}px}}
.label{{font-weight:700;font-size:{36 if tall else 32}px;letter-spacing:.32em;color:{RED};text-transform:uppercase;
  display:flex;align-items:center;gap:28px}}
.label::before,.label::after{{content:"";width:90px;height:3px;background:{RED}}}
.title{{font-family:Cinzel;font-weight:700;font-size:{92 if tall else 80}px;line-height:1.12;margin-top:{48 if tall else 32}px}}
.sub{{font-weight:600;font-size:{54 if tall else 46}px;margin-top:{48 if tall else 30}px}}
.badge{{margin-top:{80 if tall else 50}px;border:3px solid {RED};padding:22px 40px;font-weight:700;
  font-size:{32 if tall else 30}px;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}}
.price{{font-family:Cinzel;font-weight:800;font-size:{300 if tall else 230}px;line-height:.95;margin-top:{36 if tall else 20}px}}
.price small{{font-family:Mont;font-weight:700;font-size:{56 if tall else 46}px;letter-spacing:0}}
.was{{font-weight:600;font-size:{44 if tall else 38}px;color:{SOFT};margin-top:{18 if tall else 10}px}}
.was s{{text-decoration-thickness:4px;text-decoration-color:{RED}}}
.save{{display:inline-block;margin-top:{34 if tall else 22}px;background:{RED};color:#fff;font-weight:800;
  font-size:{40 if tall else 34}px;padding:14px 34px;letter-spacing:.04em}}
.visits{{font-weight:700;font-size:{48 if tall else 40}px;margin-top:{30 if tall else 18}px}}
.rule{{width:140px;height:4px;background:{RED};margin:{56 if tall else 34}px 0}}
ul{{list-style:none}}
li{{font-weight:600;font-size:{50 if tall else 42}px;line-height:1.25;margin:{18 if tall else 12}px 0}}
li.plus{{color:#fff;font-weight:800;margin-top:{34 if tall else 20}px}}
li.plus::before{{content:"+ ";color:{RED}}}
.ribbon{{font-weight:800;font-size:{34 if tall else 30}px;letter-spacing:.2em;text-transform:uppercase;
  border:3px solid {RED};padding:14px 30px;margin-bottom:{40 if tall else 24}px}}
.steps{{width:100%;text-align:left;margin-top:{60 if tall else 36}px}}
.step{{display:flex;gap:40px;align-items:flex-start;margin:{52 if tall else 34}px 0}}
.num{{font-family:Cinzel;font-weight:800;font-size:{120 if tall else 96}px;color:{RED};line-height:.9;width:110px;text-align:center}}
.st{{font-family:Cinzel;font-weight:700;font-size:{58 if tall else 50}px;line-height:1.1}}
.sd{{font-weight:500;font-size:{42 if tall else 36}px;color:{SOFT};margin-top:12px;line-height:1.3}}
.ben .st{{font-size:{52 if tall else 44}px}}
.ben .step{{margin:{40 if tall else 24}px 0;gap:30px}}
.dot{{width:22px;height:22px;background:{RED};margin-top:{18 if tall else 14}px;flex:none}}
.small{{font-weight:600;font-size:{40 if tall else 34}px;color:{SOFT};margin-top:{30 if tall else 20}px;line-height:1.35}}
.handle{{font-weight:700;font-size:{42 if tall else 36}px;margin-top:{60 if tall else 36}px;letter-spacing:.04em}}
"""


def page(fmt, inner):
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{css(fmt)}</style></head>
<body><div class=s><div class=bg></div><div class=vig></div><div class=frame></div><div class=c>{inner}</div></div></body></html>"""


def slides():
    yield "01-copertina", """
<img class="logo big" src="assets/logo.png">
<div class=label>Abbonamenti</div>
<div class=title>Il tuo Rituale,<br>sempre in ordine.</div>
<div class=sub>Da 15 € al mese</div>
<div class=badge>Soci Fondatori · massimo 144 posti</div>"""
    for i, p in enumerate(PLANS, start=2):
        items = "".join(f"<li>{x}</li>" for x in p["items"])
        if p.get("plus"):
            items += f"<li class=plus>{p['plus']}</li>"
        ribbon = f"<div class=ribbon>{p['badge']}</div>" if p.get("badge") else ""
        yield f"0{i}-piano-{p['price']}", f"""
<img class=logo src="assets/logo.png">
{ribbon}<div class=label>{p['freq']}</div>
<div class=price>{p['price']}€<small> /mese</small></div>
<div class=was>invece di <s>{p['was']} €</s></div>
<div class=save>Risparmi {p['save']} € al mese</div>
<div class=visits>{p['visits']}</div>
<div class=rule></div>
<ul>{items}</ul>"""
    yield "06-extra", """
<img class=logo src="assets/logo.png">
<div class=label>Su tutti i piani</div>
<div class=price>+5€<small> /mese</small></div>
<div class=rule></div>
<div class=title style="margin-top:0">Shampoo con lozione<br>e massaggio<br>a ogni visita.</div>"""
    yield "07-come-funziona", """
<img class=logo src="assets/logo.png">
<div class=label>Come funziona</div>
<div class=steps>
 <div class=step><div class=num>1</div><div><div class=st>Scegli il tuo piano</div><div class=sd>e la frequenza che fa per te</div></div></div>
 <div class=step><div class=num>2</div><div><div class=st>Paghi a inizio mese</div><div class=sd>rinnovo automatico,<br>disdici quando vuoi</div></div></div>
 <div class=step><div class=num>3</div><div><div class=st>Prenoti con priorità</div><div class=sd>giorno e orario fissi,<br>secondo disponibilità</div></div></div>
</div>"""
    yield "08-soci-fondatori", """
<img class=logo src="assets/logo.png">
<div class=label>Formula</div>
<div class=title style="margin-top:28px">Soci Fondatori.</div>
<div class=small>Massimo 144 soci,<br>poi le iscrizioni si chiudono.</div>
<div class="steps ben">
 <div class=step><div class=dot></div><div><div class=st>Prezzo bloccato 12 mesi</div><div class=sd>anche se il listino aumenta</div></div></div>
 <div class=step><div class=dot></div><div><div class=st>Regalo di compleanno</div><div class=sd>un prodotto a scelta con il 33% di sconto</div></div></div>
 <div class=step><div class=dot></div><div><div class=st>Prenotazione prioritaria</div><div class=sd>il tuo posto fisso in agenda</div></div></div>
 <div class=step><div class=dot></div><div><div class=st>Piano flessibile</div><div class=sd>puoi cambiarlo dal mese successivo</div></div></div>
</div>"""
    yield "09-entra-nella-famiglia", """
<img class="logo big" src="assets/logo.png">
<div class=title>Entra nella famiglia.</div>
<div class=rule></div>
<div class=sub style="margin-top:0">Prenota il tuo piano<br>in salone o in DM</div>
<div class=small>Corso Umberto I 300c · Bernalda</div>
<div class=handle>@ritual_barberstudio</div>"""


def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome")
        for fmt, h in (("916", 1920), ("45", 1350)):
            (OUT / fmt).mkdir(parents=True, exist_ok=True)
            pg = b.new_page(viewport={"width": 1080, "height": h}, device_scale_factor=2)
            for name, inner in slides():
                tmp = OUT / f"_tmp.html"
                tmp.write_text(page(fmt, inner), encoding="utf-8")
                pg.goto(tmp.as_uri())
                pg.wait_for_timeout(250)
                pg.screenshot(path=str(OUT / fmt / f"{name}.png"))
            tmp.unlink()
        b.close()


if __name__ == "__main__":
    main()
