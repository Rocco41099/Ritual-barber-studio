"""Listino prezzi in A4 da stampare, stesso stile del listino abbonamenti.

Uso: python3 tools/listino_a4.py -> media/stampa/listino-prezzi-a4.pdf (+ anteprima png)
Voci prese dall'app di prenotazione (screenshot del 18/11/2026).
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import abbonamenti as A

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "media/stampa"
AS = A.ASSETS.as_uri()
RED, INK, SOFT = A.RED, A.INK, A.SOFT

SEZIONI = [
    ("Capelli", [
        ("Taglio e sfumatura a pelle", 20, 60),
        ("Taglio sartoriale solo forbice", 20, 60),
        ("Taglio classico medio lungo", 18, 40),
        ("Taglio classico corto", 15, 30),
        ("Punti luce avanti e dietro", 15, 30),
        ("Rasatura testa a lama", 10, 20),
        ("Rasatura testa a macchinetta", 5, 10),
    ]),
    ("Barba", [
        ("Rituale barba con vapore caldo, trattamento al fango, pulizia viso, massaggio", 20, 45),
        ("Modellatura barba", 10, 20),
        ("Rasatura barba a lama", 10, 20),
        ("Rasatura barba a macchinetta", 5, 10),
        ("Linee barba e pulizia", 5, 10),
    ]),
    ("Viso e trattamenti", [
        ("Panno caldo, vapore e trattamento viso al fango", 10, 30),
        ("Shampoo rituale e trattamento", 5, 10),
    ]),
]


def riga(nome, prezzo, minuti):
    return f"""<div class=row><div class=n>{nome}<span class=min>{minuti} min</span></div>
<div class=dots></div><div class=pr>{prezzo}<small>€</small></div></div>"""


def sezione(titolo, voci):
    return f"<div class=sec><div class=label>{titolo}</div>{''.join(riga(*v) for v in voci)}</div>"


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
.s{{position:relative;width:210mm;height:297mm;overflow:hidden;color:{INK};font-family:Mont}}
.bg{{position:absolute;inset:0;background:url({AS}/tex-a4.jpg) center/cover}}
.vig{{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 0%,rgba(0,0,0,.35) 75%,rgba(0,0,0,.6) 100%)}}
.frame{{position:absolute;inset:7mm;border:.4mm solid rgba(255,255,255,.22)}}
.c{{position:relative;height:100%;padding:12mm 18mm 11mm;display:flex;flex-direction:column;align-items:center}}
.logo{{width:52mm}}
.title{{font-weight:700;font-size:13pt;letter-spacing:.32em;color:{RED};text-transform:uppercase;display:flex;align-items:center;gap:6mm;margin-top:4mm}}
.title::before,.title::after{{content:"";width:18mm;height:.8mm;background:{RED}}}
.list{{width:100%;margin-top:5mm;display:flex;flex-direction:column;gap:5mm}}
.sec{{border:.35mm solid rgba(255,255,255,.28);background:rgba(9,9,10,.55);padding:4mm 7mm 4.5mm}}
.label{{font-family:Cinzel;font-weight:700;font-size:17pt;text-align:center;margin-bottom:2.5mm}}
.label::after{{content:"";display:block;width:16mm;height:.6mm;background:{RED};margin:1.8mm auto 0}}
.row{{display:flex;align-items:baseline;gap:3mm;margin:2.1mm 0}}
.n{{font-weight:600;font-size:11pt;line-height:1.25;max-width:122mm}}
.min{{font-weight:500;font-size:8.5pt;color:{SOFT};margin-left:2.5mm;white-space:nowrap}}
.dots{{flex:1;border-bottom:.35mm dotted rgba(246,243,238,.35);transform:translateY(-1mm)}}
.pr{{font-family:Cinzel;font-weight:800;font-size:16pt;white-space:nowrap}}
.pr small{{font-family:Mont;font-weight:700;font-size:10pt;margin-left:.6mm;color:{RED}}}
.foot{{margin-top:auto;font-weight:600;font-size:10pt;color:{SOFT};letter-spacing:.04em;text-align:center}}
.foot b{{color:{INK};font-weight:700}}
</style></head><body><div class=s><div class=bg></div><div class=vig></div><div class=frame></div><div class=c>
<img class=logo src="{AS}/logo.png">
<div class=title>Listino prezzi</div>
<div class=list>{''.join(sezione(t, v) for t, v in SEZIONI)}</div>
<div class=foot><b>Ritual Barber Studio</b> · Corso Umberto I 300c, Bernalda · @ritual_barberstudio</div>
</div></div></body></html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_listino.html"
    tmp.write_text(HTML, encoding="utf-8")
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=3)
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(600)
        pg.pdf(path=str(OUT / "listino-prezzi-a4.pdf"), format="A4", print_background=True,
               margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        pg.screenshot(path=str(OUT / "listino-prezzi-a4-anteprima.png"))
        b.close()
    tmp.unlink()


if __name__ == "__main__":
    main()
