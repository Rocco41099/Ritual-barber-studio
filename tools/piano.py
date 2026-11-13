"""Piano di pubblicazione Instagram e didascalie.

Uso: python3 tools/piano.py
Scrive publish/piano.json (calendario con file e didascalie) e publish/didascalie.md (da leggere e correggere).
Non pubblica nulla: i post li pubblica Rocco dall'app. tools/kit_pubblicazione.ps1 prepara sul PC una cartella per ogni uscita.
Prepara anche le versioni per Instagram: storie in JPEG e carosello del salone a 10 slide (limite di Instagram).

Logica: ogni slot pubblica il reel alle 18:47; il giorno dopo alle 12:47 esce la versione carosello.
I post che aspettano riprese reali hanno stato "attende materiale" e non vengono pubblicati.
"""
import json, shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
M = ROOT / "media/instagram"
OUT = ROOT / "publish"
RAW = "https://raw.githubusercontent.com/Rocco41099/Ritual-barber-studio/main/"
DOVE = "📍 Ritual Barber Studio · Corso Umberto I 300c, Bernalda\nPrenota in DM."
TAG = "#ritualbarberstudio #ritualized #bernalda #matera #basilicata #barbershop #barbiere"
PROD = json.loads((ROOT / "tools/prodotti.json").read_text())
RITO = {"apollineo": ("Rituale Apollineo", "per chi vuole ogni linea al suo posto", "#apollineo"),
        "dionisiaco": ("Rituale Dionisiaco", "per chi lo stile se lo inventa", "#dionisiaco")}


PC = "C:\\Users\\rocco\\OneDrive\\Desktop\\Ritual content marketing\\"
SCELTA_SALONE = [1, 3, 4, 5, 6, 8, 9, 10, 12, 13]  # slide del carosello salone usate su Instagram (max 10)


def sul_pc(u):
    """Percorso del file originale nella cartella Ritual content marketing del PC."""
    rel = u.replace(RAW + "media/instagram/", "")
    if rel.startswith("prodotti/"):
        rel = rel.replace("prodotti/", "prodotti/2K/", 1)
    if rel.startswith("salone/carosello-ig/"):
        n = int(rel.split("/")[-1][:2])
        rel = f"salone/carosello/{SCELTA_SALONE[n - 1]:02d}-salone.jpg"
    if rel.endswith(".jpg") and "/storie/" in rel or rel == "regalo/storia-regalo.jpg":
        rel = rel[:-4] + ".png"
    return PC + rel.replace("/", "\\")


def url(p):
    return RAW + str(Path(p).relative_to(ROOT)).replace("\\", "/")


def jpg(png):
    out = Path(png).with_suffix(".jpg")
    Image.open(png).convert("RGB").save(out, quality=93, subsampling=0)
    return out


def caro(cartella, n=None):
    fs = sorted(Path(cartella).glob("*.jpg"))
    return [url(f) for f in (fs if n is None else fs[:n])]


def plain(s):
    return s.replace("<br>", " ").replace("<b>", "").replace("</b>", "")


import didascalie as D  # testi scritti uno per uno (vedi docs/brand-profile.md)


def didascalia_prodotto(slug, carosello=False):
    return D.componi(D.PRODOTTI[slug], carosello)


TESTI = {k: D.componi(v) for k, v in D.BRAND.items()}
VISUAL = {k: D.componi(v) for k, v in D.VISUAL.items()}


def carosello_testo(chiave):
    return D.componi(D.BRAND[chiave], True)


def main():
    OUT.mkdir(exist_ok=True)
    # versioni per Instagram
    ig = M / "salone/carosello-ig"; ig.mkdir(exist_ok=True)
    for f in ig.glob("*.jpg"):
        f.unlink()
    for i, n in enumerate(SCELTA_SALONE, start=1):
        shutil.copy(M / f"salone/carosello/{n:02d}-salone.jpg", ig / f"{i:02d}-salone.jpg")
    storie_q = [url(jpg(p)) for p in sorted((M / "rituali/quale-rituale/storie").glob("*.png"))]
    storia_regalo = url(jpg(M / "regalo/storia-regalo.png"))

    R = lambda p: url(M / p)
    voci = []

    def reel(data, chiave, video, didascalia=None, rito=""):
        voci.append(dict(data=data, ora="18:47", tipo="reel", contenuto=chiave, video_url=R(video),
                         didascalia=didascalia or TESTI[chiave], rituale=rito, stato="pronto"))

    def car(data, chiave, cartella, didascalia=None, n=None, rito=""):
        voci.append(dict(data=data, ora="12:47", tipo="carosello", contenuto=chiave, image_urls=caro(M / cartella, n),
                         didascalia=didascalia or carosello_testo(chiave), rituale=rito, stato="pronto"))

    def prodotto(data, slug, data_car):
        reel(data, slug, f"prodotti/{slug}/reel-{slug}.mp4", didascalia_prodotto(slug), PROD[slug]["ritual"])
        car(data_car, slug, f"prodotti/{slug}/carosello", didascalia_prodotto(slug, True), rito=PROD[slug]["ritual"])

    reel("2026-11-17", "due-nature", "rituali/due-nature/reel-due-nature.mp4", rito="entrambi")
    car("2026-11-18", "due-nature", "rituali/due-nature/carosello", rito="entrambi")
    prodotto("2026-11-19", "amarone", "2026-11-20")
    # la famiglia apre la settimana degli abbonamenti (la narrazione del lupo è stata eliminata)
    reel("2026-11-21", "famiglia", "famiglia/reel-famiglia.mp4", rito="entrambi")
    car("2026-11-22", "famiglia", "famiglia/carosello", rito="entrambi")
    reel("2026-11-24", "abbonamenti", "abbonamenti-v2/reel-abbonamenti.mp4", rito="apollineo")
    car("2026-11-25", "abbonamenti", "abbonamenti-v2/carosello", n=9, rito="apollineo")
    reel("2026-11-26", "apollineo", "rituali/apollineo/reel-apollineo.mp4", rito="apollineo")
    car("2026-11-27", "apollineo", "rituali/apollineo/carosello", rito="apollineo")
    reel("2026-11-28", "salone", "salone/reel-salone.mp4", rito="entrambi")
    car("2026-11-29", "salone", "salone/carosello-ig", rito="entrambi")
    voci.append(dict(data="2026-12-01", ora="18:47", tipo="post", contenuto="regalo", image_url=R("regalo/post-regalo.jpg"),
                     didascalia=TESTI["regalo"], rituale="entrambi", stato="pronto"))
    voci.append(dict(data="2026-12-01", ora="18:52", tipo="storia", contenuto="regalo", image_url=storia_regalo, stato="pronto"))
    reel("2026-12-03", "dionisiaco", "rituali/dionisiaco/reel-dionisiaco.mp4", rito="dionisiaco")
    car("2026-12-04", "dionisiaco", "rituali/dionisiaco/carosello", rito="dionisiaco")
    voci.append(dict(data="2026-12-05", ora="18:47", tipo="reel", contenuto="beard-ritual", rituale="apollineo",
                     didascalia=TESTI["beard-ritual"], stato="attende materiale", nota="Servono le riprese del trattamento barba entro il 1° dicembre."))
    prodotto("2026-12-08", "chianti", "2026-12-09")
    prodotto("2026-12-10", "gran-paradiso", "2026-12-11")
    voci.append(dict(data="2026-12-12", ora="18:47", tipo="reel", contenuto="ritualized", rituale="dionisiaco",
                     didascalia=TESTI["ritualized"], stato="attende materiale", nota="Serve un prima/dopo dello stesso cliente entro l'8 dicembre."))
    reel("2026-12-15", "quale", "rituali/quale-rituale/reel-quale-rituale.mp4", rito="entrambi")
    car("2026-12-16", "quale", "rituali/quale-rituale/carosello", rito="entrambi")
    for i, u in enumerate(storie_q):
        voci.append(dict(data="2026-12-15", ora="manuale", tipo="storia", contenuto=f"quale-{i + 1}", image_url=u, stato="manuale",
                         nota=f"Storia {i + 1}/5: pubblicala dall'app aggiungendo l'adesivo sondaggio A / D."))
    prodotto("2026-12-17", "tiziano", "2026-12-18")
    voci.append(dict(data="2026-12-19", ora="18:47", tipo="post", contenuto="regalo-ultimi", image_url=R("regalo/post-regalo.jpg"),
                     didascalia=TESTI["regalo-ultimi"], rituale="entrambi", stato="pronto"))
    voci.append(dict(data="2026-12-19", ora="18:52", tipo="storia", contenuto="regalo-ultimi", image_url=storia_regalo, stato="pronto"))
    prodotto("2026-12-22", "caronte", "2026-12-23")
    prodotto("2026-12-24", "monte-bianco", "2026-12-27")
    gennaio = ["nebbiolo", "virgilio", "primitivo", "nero-d-avola", "soave", "bonarda"]
    giorni = ["2027-01-12", "2027-01-14", "2027-01-19", "2027-01-21", "2027-01-26", "2027-01-28"]
    for slug, g in zip(gennaio, giorni):
        g = g.replace("2026-01", "2027-01")
        prodotto(g, slug, g[:8] + f"{int(g[8:]) + 1:02d}")
    febbraio = ["le-madonie", "barbera", "ercole", "monte-cimone", "passerina", "scala", "donatello", "farnese",
                "nettuno", "ovidio", "felice"]
    giorni = ["2027-02-02", "2027-02-04", "2027-02-09", "2027-02-11", "2027-02-16", "2027-02-18", "2027-02-23",
              "2027-02-25", "2027-03-02", "2027-03-04", "2027-03-09"]
    for slug, g in zip(febbraio, giorni):
        prodotto(g, slug, g[:8] + f"{int(g[8:]) + 1:02d}")
    # gennaio, sabato e domenica: neon, equilibrio (jolly: può coprire il 5 o il 12 dicembre
    # se le riprese di beard ritual / prima-dopo non arrivano in tempo); 9-10 gennaio liberi per i nuovi format
    reel("2027-01-02", "neon", "neon/reel-neon.mp4", rito="entrambi")
    car("2027-01-03", "neon", "neon/carosello", rito="entrambi")
    reel("2027-01-16", "equilibrio", "equilibrio/reel-equilibrio.mp4", rito="entrambi")
    car("2027-01-17", "equilibrio", "equilibrio/carosello", rito="entrambi")
    for v in voci:
        if v["contenuto"] == "equilibrio":
            v["nota"] = "Jolly: se mancano le riprese, può prendere il posto del 5 o del 12 dicembre."
    voci.sort(key=lambda v: (v["data"], v["ora"]))
    for i, v in enumerate(voci, start=1):
        v["id"] = f"{v['data']}-{v['tipo']}-{v['contenuto']}"
        u = [v[k] for k in ("video_url", "image_url") if k in v] + v.get("image_urls", [])
        if u:
            v["file_pc"] = [sul_pc(x) for x in u]
        if "image_urls" in v:
            assert 2 <= len(v["image_urls"]) <= 10, v["id"]
        if "didascalia" in v:
            assert len(v["didascalia"]) <= 2200, v["id"]
    (OUT / "piano.json").write_text(json.dumps({"account": "17841417416017365", "fuso": "Europe/Rome", "voci": voci},
                                               ensure_ascii=False, indent=1), encoding="utf-8")
    # didascalie leggibili
    righe = ["# Ritual Barber Studio · Piano di pubblicazione e didascalie", ""]
    for v in voci:
        n = f"{len(v.get('image_urls', []))} slide" if "image_urls" in v else ""
        righe += [f"## {v['data']} · {v['ora']} · {v['tipo']} · {v['contenuto']} {('(' + n + ')') if n else ''}".rstrip(),
                  f"Stato: {v['stato']}" + (f" — {v['nota']}" if v.get("nota") else ""), ""]
        if v.get("file_pc"):
            righe += ["File: " + ", ".join(f.split("\\")[-1] for f in v["file_pc"]), ""]
        if v.get("didascalia"):
            righe += ["```", v["didascalia"], "```", ""]
    (OUT / "didascalie.md").write_text("\n".join(righe), encoding="utf-8")
    print(len(voci), "voci")


if __name__ == "__main__":
    main()
