"""Listino abbonamenti in A4 da stampare, stesso stile delle grafiche Instagram.

Uso: python3 tools/abbonamenti_a4.py -> media/stampa/abbonamenti-a4.pdf (+ anteprima png)
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import abbonamenti as A

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "media/stampa"
AS = A.ASSETS.as_uri()
RED, INK, SOFT = A.RED, A.INK, A.SOFT


def card(p):
    items = "".join(f"<li>{x}</li>" for x in p["items"])
    if p.get("plus"):
        items += f"<li class=plus>{p['plus']}</li>"
    ribbon = f"<div class=ribbon>{p['badge']}</div>" if p.get("badge") else "<div class='ribbon empty'></div>"
    return f"""<div class=card>{ribbon}
<div class=freq>{p['freq']}</div>
<div class=price>{p['price']}€<small> /mese</small></div>
<div class=was>invece di <s>{p['was']} €</s></div>
<div class=save>Risparmi {p['save']} € al mese</div>
<div class=visits>{p['visits']}</div>
<div class=rule></div>
<ul>{items}</ul></div>"""


HTML = f"""<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:Cinzel;font-weight:700;src:url({AS}/cinzel-latin-700-normal.woff2)}}
@font-face{{font-family:Cinzel;font-weight:800;src:url({AS}/cinzel-latin-800-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:500;src:url({AS}/montserrat-latin-500-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:600;src:url({AS}/montserrat-latin-600-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:700;src:url({AS}/montserrat-latin-700-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:800;src:url({AS}/montserrat-latin-800-normal.woff2)}}
@page{{size:A4;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
html,body{{width:210mm;height:297mm;background:#09090a}}
.s{{position:relative;width:210mm;height:297mm;overflow:hidden;color:{INK};font-family:Mont;text-align:center}}
.bg{{position:absolute;inset:0;background:url({AS}/tex-a4.jpg) center/cover;opacity:1}}
.vig{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 0%,rgba(0,0,0,.35) 75%,rgba(0,0,0,.6) 100%)}}
.frame{{position:absolute;inset:7mm;border:.4mm solid rgba(255,255,255,.22)}}
.c{{position:relative;height:100%;padding:12mm 14mm 11mm;display:flex;flex-direction:column;align-items:center}}
.logo{{width:52mm}}
.label{{font-weight:700;font-size:13pt;letter-spacing:.32em;color:{RED};text-transform:uppercase;display:flex;align-items:center;gap:6mm;margin-top:4mm}}
.label::before,.label::after{{content:"";width:18mm;height:.8mm;background:{RED}}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;width:100%;margin-top:5mm}}
.card{{border:.35mm solid rgba(255,255,255,.28);background:rgba(9,9,10,.55);padding:3.5mm 4mm 4.5mm;display:flex;flex-direction:column;align-items:center}}
.ribbon{{font-weight:800;font-size:8pt;letter-spacing:.2em;text-transform:uppercase;border:.6mm solid {RED};padding:1.2mm 3.5mm;height:6mm;margin-bottom:2mm}}
.ribbon.empty{{border-color:transparent}}
.freq{{font-weight:700;font-size:10.5pt;letter-spacing:.24em;color:{RED};text-transform:uppercase}}
.price{{font-family:Cinzel;font-weight:800;font-size:42pt;line-height:1;margin-top:1.5mm}}
.price small{{font-family:Mont;font-weight:700;font-size:12pt}}
.was{{font-weight:600;font-size:10pt;color:{SOFT};margin-top:1.5mm}}
.was s{{text-decoration-thickness:.6mm;text-decoration-color:{RED}}}
.save{{margin-top:2.5mm;background:{RED};color:#fff;font-weight:800;font-size:9.5pt;padding:1.4mm 4mm}}
.visits{{font-weight:700;font-size:11pt;margin-top:2.5mm}}
.rule{{width:22mm;height:.7mm;background:{RED};margin:3mm 0 2mm}}
ul{{list-style:none}}
li{{font-weight:600;font-size:10pt;line-height:1.25;margin:.9mm 0}}
li.plus{{font-weight:800;color:#fff;margin-top:2.5mm}}
li.plus::before{{content:"+ ";color:{RED}}}
.extra{{width:100%;margin-top:5mm;border:.35mm solid rgba(255,255,255,.28);background:rgba(9,9,10,.55);padding:3mm 6mm;display:flex;align-items:center;justify-content:center;gap:7mm}}
.extra .p{{font-family:Cinzel;font-weight:800;font-size:28pt}}
.extra .p small{{font-family:Mont;font-weight:700;font-size:10pt}}
.extra .t{{text-align:left;font-weight:600;font-size:11pt;line-height:1.35}}
.extra .t b{{color:{RED};font-weight:800;letter-spacing:.2em;font-size:9pt;text-transform:uppercase;display:block;margin-bottom:1mm}}
.rules{{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;width:100%;margin-top:5mm}}
.r{{display:flex;gap:3mm;text-align:left;align-items:flex-start}}
.r .n{{font-family:Cinzel;font-weight:800;font-size:22pt;color:{RED};line-height:.9}}
.r .st{{font-family:Cinzel;font-weight:700;font-size:11pt;line-height:1.15}}
.r .sd{{font-weight:500;font-size:8.5pt;color:{SOFT};margin-top:1mm;line-height:1.3}}
.foot{{margin-top:auto;font-weight:600;font-size:10pt;color:{SOFT};letter-spacing:.04em}}
.foot b{{color:{INK};font-weight:700}}
</style></head><body><div class=s><div class=bg></div><div class=vig></div><div class=frame></div><div class=c>
<img class=logo src="{AS}/logo.png">
<div class=label>Abbonamenti</div>
<div class=grid>{''.join(card(p) for p in A.PLANS)}</div>
<div class=extra><div class=p>+5€<small> /mese</small></div>
<div class=t><b>Su tutti i piani</b>Shampoo con lozione e massaggio a ogni visita</div></div>
<div class=rules>
 <div class=r><div class=n>1</div><div><div class=st>Scegli il piano</div><div class=sd>e la frequenza che fa per te</div></div></div>
 <div class=r><div class=n>2</div><div><div class=st>Paghi a inizio mese</div><div class=sd>rinnovo automatico, disdici quando vuoi</div></div></div>
 <div class=r><div class=n>3</div><div><div class=st>Prenoti con priorità</div><div class=sd>giorno e orario fissi, secondo disponibilità</div></div></div>
</div>
<div class=foot><b>Ritual Barber Studio</b> · Corso Umberto I 300c, Bernalda · @ritual_barberstudio</div>
</div></div></body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_a4.html"
    tmp.write_text(HTML, encoding="utf-8")
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=3)
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(600)
        pg.pdf(path=str(OUT / "abbonamenti-a4.pdf"), format="A4", print_background=True,
               margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        pg.screenshot(path=str(OUT / "abbonamenti-a4-anteprima.png"))
        b.close()
    tmp.unlink()


if __name__ == "__main__":
    main()
