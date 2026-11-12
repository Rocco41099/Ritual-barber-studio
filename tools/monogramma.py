"""Logo sintetico RITUAL: una R intera, d'impatto, con uno stile diverso dal logo del salone.
G1/G2 sono R disegnate qui (geometria a 60 e 90 gradi, come il triangolo del logo); le altre sono la R di
caratteri con licenza libera (SIL OFL, utilizzabili anche nei loghi), convertita in tracciato vettoriale.
Uso: python3 tools/monogramma.py [cartella_font]  -> brand/abbigliamento/monogramma/*.svg + tavola-r.png
"""
import math, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brand/abbigliamento/monogramma"
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/fonts/node_modules/@fontsource")
BONE, RED, BLACK = "#F2EEE6", "#B0263A", "#0B0B0B"
T60 = math.tan(math.radians(60))


def r_da_font(file):
    f = TTFont(str(file))
    gs = f.getGlyphSet()
    name = f.getBestCmap()[ord("R")]
    pen = SVGPathPen(gs)
    gs[name].draw(pen)
    bp = BoundsPen(gs)
    gs[name].draw(bp)
    x0, y0, x1, y1 = bp.bounds
    # il font ha y verso l'alto: ribalto e porto la R in un riquadro 0..1000 di altezza
    s = 1000 / (y1 - y0)
    tr = f"translate(0,0) scale({s},{-s}) translate({-x0},{-y1})"
    return pen.getCommands(), tr, (x1 - x0) * s


def _poly(pts):
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def _r_geo(taglio=False):
    """R geometrica piena. Asta, occhiello a punta con facce a 60 gradi, contro-forma parallela all'occhiello,
    gamba a 60 gradi. Ritorna una lista di (tracciato, regola di riempimento)."""
    S = 250                      # spessore asta
    B = 554                      # base dell'occhiello
    xo, xp = 600, 600 + (B / 2) / T60       # inizio faccia e punta esterna dell'occhiello
    stem = [(0, 0), (S, 0), (S, 1000), (0, 1000)]
    if taglio:                   # asta tagliata a 60 gradi in alto e in basso, come una lama
        c = 150
        stem = [(0, c * T60 / 2), (c / 2, 0), (S, 0), (S, 1000), (c / 2, 1000), (0, 1000 - c * T60 / 2)]
    occhiello_est = [(S - 1, 0), (xo, 0), (xp, B / 2), (xo, B), (S - 1, B)]
    m = 150                      # spessore dell'occhiello
    ci0, ci1 = m, B - m
    xi = xo - 90
    occhiello_int = [(S, ci0), (xi, ci0), (xi + (B / 2 - ci0) / T60, B / 2), (xi, ci1), (S, ci1)]
    g0 = 380                     # attacco della gamba sotto l'occhiello
    lw = 255                     # larghezza della gamba
    dx = (1000 - B) / T60
    leg = [(g0, B - 2), (g0 + lw, B - 2), (g0 + lw + dx, 1000), (g0 + dx, 1000)]
    if taglio:                   # la gamba scende oltre la base, punta a lama
        leg = [(g0, B - 2), (g0 + lw, B - 2), (g0 + lw + dx, 1000), (g0 + dx + lw * 0.0, 1000)]
    w = max(xp, g0 + lw + dx)
    # unione geometrica in un'unica sagoma: un solo tracciato pulito, senza giunture (serve al serigrafo)
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    forma = unary_union([Polygon(stem), Polygon(occhiello_est).difference(Polygon(occhiello_int)), Polygon(leg)])
    def anelli(g):
        polys = getattr(g, "geoms", [g])
        out = []
        for pg in polys:
            out.append(_poly(list(pg.exterior.coords)[:-1]))
            out += [_poly(list(h.coords)[:-1]) for h in pg.interiors]
        return " ".join(out)
    return [(anelli(forma), "evenodd")], w


def g1():
    return _r_geo(False)


def g2():
    return _r_geo(True)


FONTS = {
    "bodoni": ("Didone, alta moda", FONT_DIR / "bodoni-moda/files/bodoni-moda-latin-900-normal.woff2"),
    "gotica": ("Gotica, streetwear", FONT_DIR / "unifrakturmaguntia/files/unifrakturmaguntia-latin-400-normal.woff2"),
    "romana": ("Romana decorata", FONT_DIR / "cinzel-decorative/files/cinzel-decorative-latin-900-normal.woff2"),
    "bastone": ("Bastone condensato", FONT_DIR / "anton/files/anton-latin-400-normal.woff2"),
}


def svg(d, tr, w, colore, bg=None, pad=140):
    W, H = w + 2 * pad, 1000 + 2 * pad
    rect = f'<rect x="{-pad}" y="{-pad}" width="{W}" height="{H}" fill="{bg}"/>' if bg else ""
    g = f'<g transform="{tr}">' if tr else "<g>"
    if isinstance(d, list):      # R geometrica: piu' forme, ognuna con la sua regola
        forme = "".join(f'<path fill="{colore}" fill-rule="{fr}" d="{p}"/>' for p, fr in d)
    else:                        # R da font: i contorni del carattere vanno riempiti con la regola nonzero
        forme = f'<path fill="{colore}" fill-rule="nonzero" d="{d}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="{-pad} {-pad} {W:.1f} {H:.1f}">'
            f'{rect}{g}{forme}</g></svg>')


def main():
    voci = [("G1 · Geometrica 60/90", "g1", g1()[0], "", g1()[1]), ("G2 · Geometrica a lama", "g2", g2()[0], "", g2()[1])]
    for k, (titolo, file) in FONTS.items():
        voci.append((titolo, k, *r_da_font(file)))
    righe = []
    for titolo, k, d, tr, w in voci:
        (OUT / f"r-{k}.svg").write_text(svg(d, tr, w, BLACK))
        celle = (svg(d, tr, w, BONE, BLACK), svg(d, tr, w, BLACK, BONE), svg(d, tr, w, RED, BLACK))
        piccola = svg(d, tr, w, BONE, BLACK, pad=60)
        righe.append(f"<div class=r><div class=t>{titolo}</div><div class=p>" + "".join(f"<div class=c>{c}</div>" for c in celle)
                     + f"<div class=s>{piccola}<span>a 1,5 cm</span></div></div></div>")
    html = ("<html><head><style>@font-face{font-family:M;src:url('file://" + str(ROOT) +
            "/media/instagram/abbonamenti-v2/assets/montserrat-latin-700-normal.ttf')}"
            "body{margin:0;background:#141414;font-family:M;color:#ddd;width:1900px}.r{padding:26px 40px}"
            ".t{font-size:30px;letter-spacing:.1em;margin-bottom:12px}.p{display:flex;gap:26px;align-items:flex-end}"
            ".c svg{height:340px;width:auto}.s{display:flex;flex-direction:column;align-items:center;gap:8px;font-size:18px;color:#999}"
            ".s svg{height:57px;width:auto}</style></head><body>" + "".join(righe) + "</body></html>")
    tmp = OUT / "_t.html"
    tmp.write_text(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1900, "height": 900})
        pg.goto("file://" + str(tmp))
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / "tavola-r.png"), full_page=True)
        b.close()
    tmp.unlink()
    print("ok")


if __name__ == "__main__":
    main()
