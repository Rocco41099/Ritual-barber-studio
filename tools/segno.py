"""Logo del brand di abbigliamento RITUAL, costruito dai tracciati del logo ufficiale.

- ritual-logotipo.svg : la scritta RITUAL esatta del logo del salone (senza forbici e senza 'Barber Studio')
- segno-v1..v4.svg    : la R divisa a meta', quattro costruzioni
Uso: python3 tools/segno.py  -> brand/abbigliamento/*.svg + tavola-segno.png
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "brand/logo/ritual-logo-su-nero.svg"
OUT = ROOT / "brand/abbigliamento"
OUT.mkdir(parents=True, exist_ok=True)

GOLD, RED, BONE, BLACK = "#C9A45C", "#B0263A", "#F2EEE6", "#0B0B0B"

paths = re.findall(r'<path[^>]*d="([^"]+)"', SRC.read_text())
LETTERE = paths[10:16]          # R, i, T, U, A, L
R = paths[10]
# riquadro della R nel file ufficiale
RX0, RX1, RY0, RY1 = 142.0, 456.5, 808.0, 1215.5
RW, RH = RX1 - RX0, RY1 - RY0
CX = RX0 + RW * 0.5            # asse del taglio: a meta esatta della R (prima versione, scelta da Rocco)


def svg(w, h, vb, body, bg=None):
    rect = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}">{rect}{body}</svg>')


def logotipo(colore=BONE, bg=None):
    vb = (120, 780, 2030, 470)
    body = "".join(f'<path fill="{colore}" d="{d}"/>' for d in LETTERE)
    return svg(2030, 470, vb, body, bg)


PAD = 90
VB = (RX0 - PAD - 40, RY0 - PAD, RW + 2 * PAD + 80, RH + 2 * PAD)
CLIP = (f'<defs><clipPath id="sx"><rect x="{RX0-60}" y="{RY0-60}" width="{CX-(RX0-60)}" height="{RH+120}"/></clipPath>'
        f'<clipPath id="dx"><rect x="{CX}" y="{RY0-60}" width="{RW}" height="{RH+120}"/></clipPath></defs>')


def v1(sx=BONE, dx=BONE, bg=None):
    """Taglio netto: la R tagliata in verticale, meta' destra sfalsata verso l'alto."""
    gap, shift = 10, -26
    body = (CLIP + f'<g clip-path="url(#sx)"><path fill="{sx}" d="{R}"/></g>'
            f'<g transform="translate({gap},{shift})"><g clip-path="url(#dx)"><path fill="{dx}" d="{R}"/></g></g>')
    return svg(1000, int(1000 * VB[3] / VB[2]), VB, body, bg)


def v2(bg=None, sx=GOLD, dx=RED):
    """Due materie: meta' Ordine piena oro, meta' Istinto solo contorno rosso, separate da un filo."""
    body = (CLIP + f'<g clip-path="url(#sx)"><path fill="{sx}" d="{R}"/></g>'
            f'<g clip-path="url(#dx)"><path fill="none" stroke="{dx}" stroke-width="7" d="{R}"/></g>'
            f'<line x1="{CX}" y1="{RY0-45}" x2="{CX}" y2="{RY1+45}" stroke="{BONE}" stroke-width="3"/>')
    return svg(1000, int(1000 * VB[3] / VB[2]), VB, body, bg)


def v3(bg=None, sx=GOLD, dx=RED):
    """Bifronte: la R e la sua immagine speculare si toccano sull'asse: due nature che guardano in direzioni opposte."""
    asse = RX0 - 6
    vb = (asse - RW - PAD, RY0 - PAD, 2 * (RW + PAD), RH + 2 * PAD)
    body = (f'<g transform="translate({2*asse},0) scale(-1,1)"><path fill="{sx}" d="{R}"/></g>'
            f'<path fill="{dx}" d="{R}"/>')
    return svg(1400, int(1400 * vb[3] / vb[2]), vb, body, bg)


def v4(bg=None, sx=GOLD, dx=RED, filo=BONE):
    """La Linea: R intera attraversata dal segno verticale che esce sopra e sotto; meta' oro, meta' rossa."""
    body = (CLIP + f'<g clip-path="url(#sx)"><path fill="{sx}" d="{R}"/></g>'
            f'<g clip-path="url(#dx)"><path fill="{dx}" d="{R}"/></g>'
            f'<rect x="{CX-4}" y="{RY0-80}" width="8" height="{RH+160}" fill="{filo}"/>')
    vb = (VB[0], RY0 - PAD - 10, VB[2], RH + 2 * PAD + 20)
    return svg(1000, int(1000 * vb[3] / vb[2]), vb, body, bg)


# --- geometrie triangolari: triangolo equilatero (60 gradi) diviso dalla sua altezza in due
#     triangoli rettangoli (90, 60, 30 gradi). L'altezza e' l'asse che divide la R.
import math
TAN30 = math.tan(math.radians(30))
AY = RY0 - 360                  # vertice
BY = RY1 + 70                   # base
HB = (BY - AY) * TAN30          # mezza base
TRI_VB = (CX - HB - 70, AY - 70, 2 * HB + 140, BY - AY + 140)
SX_TRI = f"{CX},{AY} {CX-HB},{BY} {CX},{BY}"   # rettangolo: 90 gradi alla base sull'asse, 60 in basso a sinistra
DX_TRI = f"{CX},{AY} {CX+HB},{BY} {CX},{BY}"
CLIP_T = (f'<defs><clipPath id="tsx"><polygon points="{SX_TRI}"/></clipPath>'
          f'<clipPath id="tdx"><polygon points="{DX_TRI}"/></clipPath>'
          f'<clipPath id="sx"><rect x="{CX-HB-10}" y="{AY-10}" width="{HB+10}" height="{BY-AY+20}"/></clipPath>'
          f'<clipPath id="dx"><rect x="{CX}" y="{AY-10}" width="{HB+10}" height="{BY-AY+20}"/></clipPath></defs>')


def _tri_svg(body, bg):
    return svg(1000, int(1000 * TRI_VB[3] / TRI_VB[2]), TRI_VB, body, bg)


def v5(bg=None, sx=GOLD, dx=RED, filo=BONE):
    """Triangolo diviso: R dentro un triangolo equilatero a filo; l'altezza divide R e triangolo."""
    body = (CLIP_T + f'<polygon points="{SX_TRI}" fill="none" stroke="{sx}" stroke-width="9" stroke-linejoin="miter"/>'
            f'<polygon points="{DX_TRI}" fill="none" stroke="{dx}" stroke-width="9" stroke-linejoin="miter"/>'
            f'<g clip-path="url(#sx)"><path fill="{sx}" d="{R}"/></g><g clip-path="url(#dx)"><path fill="{dx}" d="{R}"/></g>'
            f'<line x1="{CX}" y1="{AY}" x2="{CX}" y2="{BY}" stroke="{filo}" stroke-width="5"/>')
    return _tri_svg(body, bg)


def v6(bg=BLACK, sx=GOLD, dx=RED):
    """Triangolo pieno: due triangoli rettangoli 90/60 pieni, la R scavata in negativo."""
    body = (CLIP_T + f'<mask id="m"><rect x="{TRI_VB[0]}" y="{TRI_VB[1]}" width="{TRI_VB[2]}" height="{TRI_VB[3]}" fill="white"/>'
            f'<path fill="black" d="{R}"/><rect x="{CX-3}" y="{AY}" width="6" height="{BY-AY}" fill="black"/></mask>'
            f'<g mask="url(#m)"><polygon points="{SX_TRI}" fill="{sx}"/><polygon points="{DX_TRI}" fill="{dx}"/></g>')
    return _tri_svg(body, bg)


def v7(bg=None, sx=GOLD, dx=RED):
    """Spaccato: le due meta' del triangolo, ognuna con la sua meta' di R, si separano lungo l'asse."""
    g = 28
    body = (CLIP_T + f'<g transform="translate({-g},0)"><polygon points="{SX_TRI}" fill="none" stroke="{sx}" stroke-width="9"/>'
            f'<g clip-path="url(#sx)"><path fill="{sx}" d="{R}"/></g></g>'
            f'<g transform="translate({g},0)"><polygon points="{DX_TRI}" fill="none" stroke="{dx}" stroke-width="9"/>'
            f'<g clip-path="url(#dx)"><path fill="{dx}" d="{R}"/></g></g>')
    vb = (TRI_VB[0] - g, TRI_VB[1], TRI_VB[2] + 2 * g, TRI_VB[3])
    return svg(1000, int(1000 * vb[3] / vb[2]), vb, body, bg)


def main():
    (OUT / "ritual-logotipo-bianco.svg").write_text(logotipo(BONE))
    (OUT / "ritual-logotipo-nero.svg").write_text(logotipo(BLACK))
    varianti = {
        "segno-v1-taglio": v1(),
        "segno-v2-due-materie": v2(),
        "segno-v3-bifronte": v3(),
        "segno-v4-linea": v4(),
        "segno-v5-triangolo-diviso": v5(),
        "segno-v6-triangolo-pieno": v6(),
        "segno-v7-spaccato": v7(),
    }
    for k, s in varianti.items():
        (OUT / f"{k}.svg").write_text(s)
    # tavola di confronto: ogni variante su nero e su bianco osso
    celle = []
    for k, f in [("V1 · Taglio netto", lambda bg: v1(BONE, BONE, bg)), ("V2 · Due materie", lambda bg: v2(bg)),
                 ("V3 · Bifronte", lambda bg: v3(bg)), ("V4 · La linea", lambda bg: v4(bg)),
                 ("V5 · Triangolo diviso (60° / 90°)", lambda bg: v5(bg)), ("V6 · Triangolo pieno", lambda bg: v6(bg)),
                 ("V7 · Spaccato", lambda bg: v7(bg))]:
        nero = f(BLACK)
        chiaro = (v1(BLACK, BLACK, BONE) if k.startswith("V1") else
                  v2(BONE, GOLD, RED) if k.startswith("V2") else
                  v3(BONE, BLACK, RED) if k.startswith("V3") else
                  v4(BONE, BLACK, RED, BLACK) if k.startswith("V4") else
                  v5(BONE, BLACK, RED, BLACK) if k.startswith("V5") else
                  v6(BONE, BLACK, RED) if k.startswith("V6") else v7(BONE, BLACK, RED))
        celle.append(f"<div class=c><div class=t>{k}</div><div class=p>{nero}{chiaro}</div></div>")
    html = ("<html><head><style>@font-face{font-family:M;src:url('file://" + str(ROOT) +
            "/media/instagram/abbonamenti-v2/assets/montserrat-latin-700-normal.ttf')}"
            "body{margin:0;background:#141414;font-family:M;color:#ddd;width:2400px}"
            ".c{padding:30px 40px}.t{font-size:34px;letter-spacing:.12em;margin-bottom:16px}"
            ".p{display:flex;gap:30px}.p svg{width:560px;height:auto;flex:none}"
            ".h{padding:40px;background:#0b0b0b}.h svg{width:1300px;height:auto}</style></head><body>"
            f"<div class=h>{logotipo(BONE, BLACK)}</div>" + "".join(celle) + "</body></html>")
    (OUT / "_tavola.html").write_text(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 2400, "height": 1000})
        pg.goto("file://" + str(OUT / "_tavola.html"))
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / "tavola-segno.png"), full_page=True)
        b.close()
    (OUT / "_tavola.html").unlink()
    print("ok")


if __name__ == "__main__":
    main()
