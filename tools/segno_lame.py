"""Segno RITUAL con le lame: forbici e rasoio del logo ufficiale ridotti a due triangoli lunghi (90 gradi al tallone) che si incrociano a 60 gradi; la R divisa a meta.
Uso: python3 tools/segno_lame.py"""
import sys, math
sys.path.insert(0,'tools')
import segno as S
R=S.R; RX0,RX1,RY0,RY1=S.RX0,S.RX1,S.RY0,S.RY1; RW,RH=S.RW,S.RH
GOLD,RED,BONE,BLACK=S.GOLD,S.RED,S.BONE,S.BLACK
CX=RX0+RW*0.5
T30=math.tan(math.radians(30))
def lama(px,py,verso,top_y,bot_y,w):
    """Lama: triangolo rettangolo lungo e stretto. Il dorso sta sulla retta a 60 gradi per (px,py);
    il tallone in alto e' tagliato a 90 gradi rispetto al dorso; la punta in basso."""
    # direzione del dorso (dall'alto verso il basso): verso=+1 scende verso destra
    d=(verso*math.cos(math.radians(60)), math.sin(math.radians(60)))
    t0=(top_y-py)/d[1]; t1=(bot_y-py)/d[1]
    a=(px+d[0]*t0, py+d[1]*t0)          # tallone, sul dorso
    tip=(px+d[0]*t1, py+d[1]*t1)        # punta
    n=(-d[1]*verso, d[0]*verso)         # normale verso l'interno della V
    n=( d[1]*verso*-1, d[0]) if False else (-verso*d[1], verso*d[0])
    b=(a[0]+n[0]*w, a[1]+n[1]*w)        # angolo retto al tallone
    return f"{a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f} {tip[0]:.1f},{tip[1]:.1f}"
def r_divisa(c1,c2):
    return (f'<defs><clipPath id="L"><rect x="0" y="0" width="{CX}" height="3000"/></clipPath>'
            f'<clipPath id="Rr"><rect x="{CX}" y="0" width="3000" height="3000"/></clipPath></defs>'
            f'<g clip-path="url(#L)"><path fill="{c1}" d="{R}"/></g><g clip-path="url(#Rr)"><path fill="{c2}" d="{R}"/></g>')
def S1(bg,c1,c2):
    """Le lame incrociate sotto la R, come forbici e rasoio nel logo: la R sta nel triangolo rovesciato."""
    P=(CX,1545); top=RY0-140; bot=1545+300; w=44
    body=(f'<polygon points="{lama(P[0],P[1],+1,top,bot,w)}" fill="{c1}"/>'
          f'<polygon points="{lama(P[0],P[1],-1,top,bot,w)}" fill="{c2}"/>'+r_divisa(c1,c2))
    vb=(CX-620,top-60,1240,bot-top+120)
    return S.svg(800,int(800*vb[3]/vb[2]),vb,body,bg)
def S3(bg,c1,c2):
    """Triangolo rovesciato: la barra della R prolungata e' il lato in alto, le due lame i lati che si incrociano in basso."""
    P=(CX,1545); top=RY0; bot=1545+260; w=40
    h=P[1]-top; hb=h*T30
    barra=f'<rect x="{CX-hb}" y="{RY0}" width="{2*hb}" height="24.4" fill="{BONE if bg==BLACK else BLACK}"/>'
    body=(f'<polygon points="{lama(P[0],P[1],+1,top,bot,w)}" fill="{c1}"/>'
          f'<polygon points="{lama(P[0],P[1],-1,top,bot,w)}" fill="{c2}"/>'+barra+r_divisa(c1,c2))
    vb=(CX-hb-110,top-110,2*hb+220,bot-top+180)
    return S.svg(800,int(800*vb[3]/vb[2]),vb,body,bg)
def S2(bg,c1,c2):
    """Una sola lama a 60 gradi attraversa la R tagliata a meta': il gesto del taglio."""
    P=(CX,RY0+RH*0.55); top=RY0-160; bot=RY1+160; w=40
    body=(r_divisa(c1,c2)+f'<polygon points="{lama(P[0],P[1],-1,top,bot,w)}" fill="{BONE if bg==BLACK else BLACK}"/>')
    vb=(RX0-260,top-60,RW+520,bot-top+120)
    return S.svg(800,int(800*vb[3]/vb[2]),vb,body,bg)
rows=[("S1 · Lame incrociate, la R nel triangolo",S1(BLACK,GOLD,RED),S1(S.BONE,BLACK,RED)),
      ("S2 · Una lama attraversa la R",S2(BLACK,GOLD,RED),S2(S.BONE,BLACK,RED)),
      ("S3 · Triangolo rovesciato: barra + lame",S3(BLACK,GOLD,RED),S3(S.BONE,BLACK,RED))]
html=("<html><head><style>@font-face{font-family:M;src:url('file:///home/claude/ritual-barber-studio/media/instagram/abbonamenti-v2/assets/montserrat-latin-700-normal.ttf')}"
 "body{margin:0;background:#141414;font-family:M;color:#ddd;width:1800px}.r{padding:30px 40px}.t{font-size:32px;letter-spacing:.1em;margin-bottom:14px}"
 ".p{display:flex;gap:30px;align-items:flex-start}.p svg{width:520px;height:auto}</style></head><body>"+
 "".join(f"<div class=r><div class=t>{t}</div><div class=p>{a}{b}</div></div>" for t,a,b in rows)+"</body></html>")
open("brand/abbigliamento/_lame.html","w").write(html)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1800,"height":800}); pg.goto("file://"+str(__import__("pathlib").Path("brand/abbigliamento/_lame.html").resolve())); pg.wait_for_timeout(400)
    pg.screenshot(path="brand/abbigliamento/tavola-lame.png",full_page=True); b.close()
import os
os.remove("brand/abbigliamento/_lame.html")
for nome, f in [("segno-s1-lame-incrociate", S1), ("segno-s2-lama", S2), ("segno-s3-triangolo-lame", S3)]:
    open(f"brand/abbigliamento/{nome}.svg", "w").write(f(None, GOLD, RED))
print("ok")
