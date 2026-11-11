"""Varianti neon del logo Ritual: insegna LED accesa su sfondi a tema.

Il logo resta quello vero (maschera alfa del PNG), la luce e' calcolata in codice.
Mai il negozio come sfondo nei contenuti col logo.
Uscite in media/instagram/neon/:
  carosello/01..05-<colore>.jpg     (2160x2700)   un colore per slide
  storie/01..05-<colore>.jpg        (1440x2560)
Sfondo: marmo nero con venature e fumo (rosso per il neon rosso, bianco per gli altri), generato con Higgsfield;
nel reel il fumo e' animato (sfondi/fumo-<colore>-916.mp4).
  reel-neon.mp4                     (1440x2560)   accensione con flicker, cambio colori, finale col logo

Uso: python3 tools/neon.py [stills|reel|all]
"""
import subprocess, sys
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "media/instagram/neon"
LOGO = ROOT / "brand/logo/ritual-logo-bianco-trasparente.png"

COLORI = {  # nome: RGB del gas neon
    "rosso": (255, 42, 60),
    "oro": (255, 176, 70),
    "bianco": (255, 236, 214),
    "ghiaccio": (80, 200, 255),
    "viola": (180, 77, 255),
}
ORDINE = ["rosso", "oro", "ghiaccio", "viola", "bianco"]

# Sfondo: marmo nero con venature bianco-grigie e fumo (generato con Higgsfield).
# Fumo rosso per il neon rosso, fumo bianco per gli altri colori.
FUMO = {"rosso": "rosso", "oro": "bianco", "ghiaccio": "bianco", "viola": "bianco", "bianco": "bianco"}


def cover(img, w, h):
    ih, iw = img.shape[:2]
    s = max(w / iw, h / ih)
    r = cv2.resize(img, (round(iw * s), round(ih * s)), interpolation=cv2.INTER_LANCZOS4)
    x = (r.shape[1] - w) // 2
    y = (r.shape[0] - h) // 2
    return r[y:y + h, x:x + w]


def sfondo(fumo, w, h):
    formato = "916" if h / w > 1.5 else "45"
    img = cv2.imread(str(OUT / f"sfondi/marmo-fumo-{fumo}-{formato}.jpg"))[:, :, ::-1].astype(np.float32) / 255
    img = cover(img, w, h)
    xx = np.linspace(-1, 1, w)[None, :]
    yv = np.linspace(-1, 1, h)[:, None]
    vign = np.clip(1 - 0.35 * (xx ** 2 + yv ** 2), 0.3, 1)
    return np.clip(img * 0.85 * vign[..., None], 0, 1)


def maschera(w, h, larghezza=0.74, cy=0.46):
    a = cv2.imread(str(LOGO), cv2.IMREAD_UNCHANGED)[:, :, 3]
    ys, xs = np.nonzero(a > 8)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.float32) / 255
    lw = round(w * larghezza)
    lh = round(a.shape[0] * lw / a.shape[1])
    a = cv2.resize(a, (lw, lh), interpolation=cv2.INTER_AREA)
    m = np.zeros((h, w), np.float32)
    x, y = (w - lw) // 2, round(h * cy - lh / 2)
    m[y:y + lh, x:x + lw] = a
    return m, (w / 2, h * cy)


def blur(m, sigma):
    """Gaussiana veloce: per sigma grandi lavora in risoluzione ridotta."""
    if sigma < 12:
        return cv2.GaussianBlur(m, (0, 0), sigma)
    f = max(1, int(sigma // 6))
    h, w = m.shape
    small = cv2.resize(m, (w // f, h // f), interpolation=cv2.INTER_AREA)
    small = cv2.GaussianBlur(small, (0, 0), sigma / f)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)


def luce(m, colore, w):
    """Strato di luce (nucleo, alone) per una maschera e un colore."""
    c = np.array(colore, np.float32) / 255
    k = w / 1440
    tubo = np.clip(m, 0, 1)
    # anima calda al centro del tratto, colore pieno ai bordi del tubo
    centro = blur(m, 3.0 * k)
    caldo = np.clip((centro - 0.80) / 0.20, 0, 1) * tubo
    nucleo = tubo[..., None] * c * 1.25 + caldo[..., None] * (0.35 + 0.65 * c) * 0.75
    alone = np.zeros(m.shape + (3,), np.float32)
    for sigma, forza in [(3, 1.2), (9, 1.0), (24, 0.65), (70, 0.38), (200, 0.20), (480, 0.10)]:
        b = blur(m, sigma * k)
        alone += (b / max(b.max(), 1e-6))[..., None] * forza   # ogni strato al suo picco
    return nucleo, alone * c


def ombra(m, w, forza=0.55):
    """Scurisce il marmo dietro l'insegna, cosi' le venature non disturbano la lettura."""
    b = blur(m, 60 * w / 1440)
    b = b / max(b.max(), 1e-6)
    return (1 - forza * np.clip(b * 1.6, 0, 1))[..., None]


def componi(bg, nucleo, alone, i=1.0):
    """bg illuminato dall'alone (moltiplicato) + luce additiva, con tonemap morbido."""
    lit = bg * (1 + alone * 2.5 * i) + alone * 0.30 * i + nucleo * i
    lit = 1 - np.exp(-lit * 1.35)               # spalla morbida, niente bruciature piatte
    return lit


def salva(img, path, q=95):
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), (np.clip(img, 0, 1) * 255).astype(np.uint8)[:, :, ::-1],
                [cv2.IMWRITE_JPEG_QUALITY, q])


def stills():
    W, H = 1440, 2560
    m, _ = maschera(W, H)
    CW, CH = 2160, 2700
    mc, _ = maschera(CW, CH, larghezza=0.70, cy=0.47)
    for n, nc in enumerate(ORDINE, 1):
        nu, al = luce(m, COLORI[nc], W)
        salva(componi(sfondo(FUMO[nc], W, H) * ombra(m, W), nu, al), OUT / f"storie/{n:02d}-{nc}.jpg")
        nu, al = luce(mc, COLORI[nc], CW)
        salva(componi(sfondo(FUMO[nc], CW, CH) * ombra(mc, CW), nu, al), OUT / f"carosello/{n:02d}-{nc}.jpg")
    print("stills ok")


def flicker(t):
    """Intensita' 0..1 dell'accensione di un neon nei primi ~0.6 s."""
    seq = [(0.00, 0), (0.08, 1), (0.12, 0), (0.30, 0.7), (0.34, 0.1), (0.42, 1), (0.48, 0.3), (0.56, 1)]
    v = 0
    for t0, val in seq:
        if t >= t0:
            v = val
    return v


def testo_finale(W, H, y0):
    from PIL import Image, ImageDraw, ImageFont
    fdir = ROOT / "media/instagram/abbonamenti-v2/assets"
    cinzel = fdir / "cinzel-latin-700-normal.ttf"
    mont = fdir / "montserrat-latin-700-normal.ttf"
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    righe = [("Il tuo Rituale ti aspetta.", 70, cinzel), ("CORSO UMBERTO I 300C · BERNALDA", 38, mont),
             ("@RITUAL_BARBERSTUDIO", 38, mont)]
    y = y0
    for txt, size, font in righe:
        f = ImageFont.truetype(str(font), size)
        tw = d.textlength(txt, font=f)
        d.text(((W - tw) / 2, y), txt, font=f, fill=255)
        y += size + 34
    return np.asarray(img, np.float32)[..., None] / 255


def frames_clip(path, w, h):
    """Decodifica un clip (fumo animato) in float RGB w x h, applica lo stesso look dello sfondo."""
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(path), "-vf",
                          f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},fps=30",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    xx = np.linspace(-1, 1, w)[None, :]
    yv = np.linspace(-1, 1, h)[:, None]
    vign = (np.clip(1 - 0.35 * (xx ** 2 + yv ** 2), 0.3, 1) * 0.85).astype(np.float32)[..., None]
    return fr, vign


def pingpong(n_tot, n_clip, start=0):
    """Indici avanti-indietro per coprire n_tot frame con un clip di n_clip frame."""
    out, i, d = [], start, 1
    for _ in range(n_tot):
        out.append(i)
        if not 0 <= i + d < n_clip:
            d = -d
        i += d
    return out


def reel():
    W, H, FPS = 1440, 2560, 30
    m, (cx, cy) = maschera(W, H)
    rng = np.random.default_rng(7)
    prep = {nc: luce(m, COLORI[nc], W) for nc in ORDINE}
    om = ombra(m, W)
    clip = {f: frames_clip(OUT / f"sfondi/fumo-{f}-916.mp4", W, H) for f in ("rosso", "bianco")}
    txt = testo_finale(W, H, int(cy + 0.21 * H))
    BUIO, SEG, FINE = 0.8, 2.4, 3.2
    sequenza = ORDINE + ["rosso"]
    tot = BUIO + SEG * len(ORDINE) + FINE
    N = round(tot * FPS)
    # quale fumo per ogni frame + indice nel clip (ping-pong, continuo dentro ogni tratto)
    piano, cur, inizio = [], None, 0
    for f in range(N):
        t = f / FPS
        nc = "rosso" if t < BUIO else sequenza[min(int((t - BUIO) // SEG), len(ORDINE))]
        piano.append(FUMO[nc])
    idx, f = [0] * N, 0
    while f < N:
        g = f
        while g < N and piano[g] == piano[f]:
            g += 1
        n_clip = len(clip[piano[f]][0])
        for k, v in enumerate(pingpong(g - f, n_clip, start=(f * 7) % n_clip)):
            idx[f + k] = v
        f = g
    out = OUT / "reel-neon.mp4"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)],
                         stdin=subprocess.PIPE)
    for f in range(N):
        t = f / FPS
        fr, vign = clip[piano[f]]
        bg = fr[idx[f]].astype(np.float32) / 255 * vign * om
        if t < BUIO:
            img = componi(bg, *prep["rosso"], 0)
        else:
            tt = t - BUIO
            k = min(int(tt // SEG), len(ORDINE))
            tl = tt - k * SEG
            i = flicker(tl)
            if i >= 1:
                i = 1 + rng.normal(0, 0.012)      # ronzio
            img = componi(bg, *prep[sequenza[k]], i)
            if k == len(ORDINE):
                a = np.clip((tl - 0.9) / 0.7, 0, 1)
                img = img * (1 - txt * a) + txt * a * np.array([0.95, 0.92, 0.88], np.float32)
        z = 1 + 0.05 * (t / tot)                  # push-in lento
        M = cv2.getRotationMatrix2D((cx, cy), 0, z)
        img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        p.stdin.write((np.clip(img, 0, 1) * 255).astype(np.uint8).tobytes())
    p.stdin.close()
    p.wait()
    print("reel ok", out)


if __name__ == "__main__":
    cosa = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cosa in ("stills", "all"):
        stills()
    if cosa in ("reel", "all"):
        reel()
