"""Segno RITUAL: triangolo equilatero con la punta in su e la scritta RITUAL del logo ufficiale al centro.
La scritta sta sul baricentro del triangolo (2/3 dell'altezza dal vertice), il centro ottico.
Uso: python3 tools/segno_triangolo.py -> brand/abbigliamento/triangolo-t*.svg + tavola-triangolo.png
"""
import math, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import segno as S

ROOT = S.ROOT
OUT = S.OUT
GOLD, RED, BONE, BLACK = S.GOLD, S.RED, S.BONE, S.BLACK
T30 = math.tan(math.radians(30))
# scritta RITUAL nei tracciati ufficiali
WX0, WX1, WY0, WY1 = 141.7, 2126.0, 804.0, 1223.0
WCX, WCY = (WX0 + WX1) / 2, (WY0 + WY1) / 2
WW, WH = WX1 - WX0, WY1 - WY0
MARGINE = 210                                    # aria tra scritta e lati alla quota piu' stretta
H = ((WW / 2 + MARGINE) / T30 + WH / 2) * 1.5    # altezza: la scritta entra sul baricentro con il margine
AY = WCY - 2 * H / 3                             # vertice
BY = AY + H                                      # base
HB = H * T30                                     # mezza base
TRI = f"{WCX},{AY} {WCX-HB},{BY} {WCX+HB},{BY}"
SX = f"{WCX},{AY} {WCX-HB},{BY} {WCX},{BY}"      # triangolo rettangolo 90/60/30
DX = f"{WCX},{AY} {WCX+HB},{BY} {WCX},{BY}"
PAD = 140
VB = (WCX - HB - PAD, AY - PAD, 2 * HB + 2 * PAD, H + 2 * PAD)
SW = 34                                          # spessore del filo, vicino all'asta delle lettere


def scritta(colore):
    return "".join(f'<path fill="{colore}" d="{d}"/>' for d in S.LETTERE)


def tela(body, bg):
    return S.svg(1000, int(1000 * VB[3] / VB[2]), VB, body, bg)


def t1(bg=None, linea=BONE, testo=BONE):
    """Triangolo a filo, scritta al centro."""
    return tela(f'<path fill="{linea}" fill-rule="evenodd" d="{anello()}"/>' + scritta(testo), bg)


def anello(spessore=SW):
    """Contorno del triangolo come forma piena: triangolo esterno meno triangolo interno, offset esatto di
    spessore/2 per parte rispetto al lato (come il filo di T1, angoli vivi). Per un equilatero l'offset dei lati
    equivale a scalare dal baricentro di (r +/- d) / r, con r = raggio inscritto = H/3."""
    gx, gy = WCX, AY + 2 * H / 3
    r = H / 3
    def scala(k):
        pts = [(WCX, AY), (WCX - HB, BY), (WCX + HB, BY)]
        return " ".join(f"{gx + (x - gx) * k:.3f},{gy + (y - gy) * k:.3f}" for x, y in pts)
    est = scala((r + spessore / 2) / r)
    inn = scala((r - spessore / 2) / r)
    return f"M {est.replace(' ', ' L ')} Z M {inn.replace(' ', ' L ')} Z"


def t2(bg=None, sx=BONE, dx=RED, testo=BONE):
    """Le due nature: lo stesso contorno di T1 in un solo pezzo, diviso in verticale dall'asse.
    Meta' sinistra bianca, meta' destra rossa; la destra parte 1 unita' sotto la sinistra, cosi' sul taglio
    non resta nessuna fessura."""
    d = anello()
    top, bot = AY - SW * 3, BY + SW * 3
    clip = (f'<defs><clipPath id="t2s"><rect x="{WCX-HB-SW*3}" y="{top}" width="{HB+SW*3}" height="{bot-top}"/></clipPath>'
            f'<clipPath id="t2d"><rect x="{WCX-1}" y="{top}" width="{HB+SW*3+1}" height="{bot-top}"/></clipPath></defs>')
    return tela(clip + f'<path fill="{dx}" fill-rule="evenodd" clip-path="url(#t2d)" d="{d}"/>'
                f'<path fill="{sx}" fill-rule="evenodd" clip-path="url(#t2s)" d="{d}"/>' + scritta(testo), bg)


def t3(bg=None, sx=GOLD, dx=RED, testo=BONE, base=BONE):
    """Le lame: i due lati sono le lame di forbici e rasoio, si incrociano in cima e escono oltre il vertice."""
    over = 260
    k = over / H
    def lama(x0, y0, x1, y1, w, verso):
        # triangolo lungo: largo alla base, punta oltre il vertice
        dx_, dy_ = x1 - x0, y1 - y0
        L = math.hypot(dx_, dy_)
        nx, ny = -dy_ / L * verso, dx_ / L * verso
        return f"{x0},{y0} {x0+nx*w},{y0+ny*w} {x1},{y1}"
    ax_sx = (WCX + 2 * HB * k * 0.5, AY - over)   # la lama di sinistra prosegue oltre il vertice verso destra
    ax_dx = (WCX - 2 * HB * k * 0.5, AY - over)
    body = (f'<polygon points="{lama(WCX-HB, BY, ax_sx[0], ax_sx[1], 70, -1)}" fill="{sx}"/>'
            f'<polygon points="{lama(WCX+HB, BY, ax_dx[0], ax_dx[1], 70, 1)}" fill="{dx}"/>'
            f'<rect x="{WCX-HB}" y="{BY-SW}" width="{2*HB}" height="{SW}" fill="{base}"/>' + scritta(testo))
    vb = (VB[0], AY - over - PAD, VB[2], H + over + 2 * PAD)
    return S.svg(1000, int(1000 * vb[3] / vb[2]), vb, body, bg)


def t4(bg=None, sx=GOLD, dx=RED, testo=BLACK):
    """Triangolo pieno diviso in due triangoli rettangoli, scritta sopra."""
    return tela(f'<polygon points="{SX}" fill="{sx}"/><polygon points="{DX}" fill="{dx}"/>' + scritta(testo), bg)


def main():
    var = [("T1 · Triangolo a filo", t1, lambda: t1(BONE, BLACK, BLACK)),
           ("T2 · Due nature sul filo", t2, lambda: t2(BONE, BLACK, RED, BLACK)),
           ("T3 · Le lame come lati", t3, lambda: t3(BONE, BLACK, RED, BLACK, BLACK)),
           ("T4 · Triangolo pieno diviso", lambda bg: t4(bg, GOLD, RED, BLACK), lambda: t4(BONE, BLACK, RED, BONE))]
    for i, (nome, f, _) in enumerate(var, 1):
        (OUT / f"triangolo-t{i}.svg").write_text(f(None) if i != 4 else t4(None))
    righe = "".join(f"<div class=r><div class=t>{n}</div><div class=p>{f(BLACK)}{c()}</div></div>" for n, f, c in var)
    html = ("<html><head><style>@font-face{font-family:M;src:url('file://" + str(ROOT) +
            "/media/instagram/abbonamenti-v2/assets/montserrat-latin-700-normal.ttf')}"
            "body{margin:0;background:#141414;font-family:M;color:#ddd;width:1800px}.r{padding:30px 40px}"
            ".t{font-size:32px;letter-spacing:.1em;margin-bottom:14px}.p{display:flex;gap:30px;align-items:flex-start}"
            ".p svg{width:560px;height:auto}</style></head><body>" + righe + "</body></html>")
    tmp = OUT / "_tri.html"
    tmp.write_text(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1800, "height": 800})
        pg.goto("file://" + str(tmp))
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / "tavola-triangolo.png"), full_page=True)
        b.close()
    tmp.unlink()
    print("ok", round(H), round(2 * HB))


if __name__ == "__main__":
    main()
