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


def didascalia_prodotto(slug, carosello=False):
    p = PROD[slug]; nome, frase, tag = RITO[p["ritual"]]
    apertura = "Scorri: prodotto, ingrediente, rituale." if carosello else "Guarda fino alla fine."
    return (f"{p['name']}. {p['category']}.\n\n"
            f"Il cuore della formula: {p['ingredient'].lower()}. {plain(p['ingredient_note'])}.\n"
            + "\n".join(f"· {plain(s)}" for s in p["specs"]) + "\n\n"
            f"{nome}: {frase}.\n"
            f"Lo trovi in salone, con il consiglio giusto per usarlo. {apertura}\n\n"
            f"Regala un rituale.\n\n{DOVE}\n\n"
            f"{TAG} {tag} #barbaitaliana #madeinitaly #estrattinaturali #{p['line']}")


TESTI = {
    "due-nature": ("Due nature. Un solo Rituale.\n\n"
                   "L'ordine ti dà la forma. L'istinto ti dà il carattere.\n"
                   "C'è chi cerca la linea perfetta e chi vuole rompere gli schemi. Ogni uomo li ha entrambi: noi li curiamo tutti e due.\n\n"
                   "Tu da che parte stai? Scrivi A o D nei commenti.\n\n"
                   f"{DOVE}\n\n{TAG} #apollineo #dionisiaco #menstyle"),
    "lupi": ("I Lupi non dormono mai.\nMa ogni lupo ha il suo rituale.\n\n"
             "Bernalda, di notte. Il castello, la piazza, il corso. E una porta che resta accesa.\n\n"
             "Martedì si apre la famiglia. Resta in ascolto.\n\n"
             f"{DOVE}\n\n{TAG} #dionisiaco #bernaldabynight"),
    "abbonamenti": ("Il rituale non è una volta ogni tanto. È un appuntamento con te stesso.\n\n"
                    "Con gli abbonamenti Ritual hai il tuo posto in poltrona ogni mese, a un prezzo che premia la costanza. "
                    "Quattro piani, uno per ogni ritmo: scorri e trova il tuo.\n\n"
                    "I primi iscritti entrano come Soci Fondatori.\n\n"
                    "Entra nella famiglia: prenota in salone o scrivici in DM.\n\n"
                    f"{DOVE}\n\n{TAG} #abbonamento #sociofondatore #cura"),
    "apollineo": ("Ordine. Misura. Controllo.\n\n"
                  "La disciplina non ti limita: ti definisce.\n"
                  "Il Rituale Apollineo è per chi ama la linea pulita: sfumatura a pelle, barba disegnata al millimetro, "
                  "lo stesso gesto ogni settimana.\n\n"
                  "Sei Apollineo? Scrivi A nei commenti.\n\n"
                  f"{DOVE}\n\n{TAG} #apollineo #skinfade #beardgrooming"),
    "dionisiaco": ("Istinto. Eccesso. Libertà.\n\n"
                   "Le regole sono per chi non ha stile.\n"
                   "Il Rituale Dionisiaco è per chi taglia, rompe e ricomincia: texture, mullet, trasformazioni. "
                   "Nessuno schema, solo carattere.\n\n"
                   "Sei Dionisiaco? Scrivi D nei commenti.\n\n"
                   f"{DOVE}\n\n{TAG} #dionisiaco #mullet #texturedhair"),
    "salone": ("Fuori, il mondo corre. Qui dentro, il tempo torna tuo.\n\n"
               "Una poltrona, nessuna fretta. Ogni strumento al suo posto, ogni gesto con il suo perché. "
               "Anche l'attesa fa parte del rito.\n\n"
               "Ritual nasce da un'idea semplice: la cura di sé non è vanità, è disciplina.\n"
               "Non è un taglio. È un rituale.\n\n"
               f"{DOVE}\n\n{TAG} #barbershopinterior #salone"),
    "regalo": ("Il regalo perfetto ha carattere.\n\n"
               "Quest'anno regala un rituale: cura uomo made in Italy con estratti naturali, "
               "vinaccioli, argan, stella alpina, caffeina. Ti aiutiamo noi a scegliere quello giusto per lui.\n\n"
               "Vieni in salone o scrivici in DM.\n\n"
               f"{DOVE}\n\n{TAG} #regalouomo #natale #barbaitaliana"),
    "regalo-ultimi": ("Ultimi giorni per regalare un rituale.\n\n"
                      "Hai ancora un uomo nella lista? Passa in salone: ti prepariamo il regalo giusto, "
                      "con prodotti made in Italy e un consiglio su misura.\n\n"
                      f"{DOVE}\n\n{TAG} #regalouomo #natale #ultimominuto"),
    "quale": ("Quale rituale sei?\n\n"
              "5 scelte, nessuna risposta sbagliata. Conta le A e le D.\n"
              "Più A: sei Apollineo. Ordine, misura, controllo.\n"
              "Più D: sei Dionisiaco. Istinto, eccesso, libertà.\n\n"
              "Scrivi il tuo risultato nei commenti e tagga un amico che è l'esatto opposto.\n\n"
              f"{DOVE}\n\n{TAG} #apollineo #dionisiaco #test"),
    "famiglia": ("Non sei un cliente. Sei uno di noi.\n\n"
                 "Stessa poltrona, stesse mani, ogni settimana. Sappiamo già come prendi il caffè, "
                 "e il tuo taglio lo conosciamo a memoria.\n"
                 "La costanza è il primo rituale: con gli abbonamenti Ritual il tuo posto è sempre pronto.\n\n"
                 "Entra nella famiglia: chiedi in salone o scrivici in DM.\n\n"
                 f"{DOVE}\n\n{TAG} #abbonamento #famiglia #cura"),
    "equilibrio": ("Notifiche. Traffico. Rumore.\n\n"
                   "Qui il telefono resta a faccia in giù. Panno caldo, respiro lungo, una mossa alla volta.\n"
                   "Mezz'ora in cui nessuno ti cerca e tu ritrovi il tuo ritmo.\n\n"
                   "Stacca dal rumore. Ritrova l'equilibrio.\n"
                   "Prenota il tuo momento in DM.\n\n"
                   f"{DOVE}\n\n{TAG} #equilibrio #slowliving #cura"),
    "neon": ("Il nostro segno, acceso.\n\n"
             "Rosso, oro, ghiaccio, viola, bianco: qual è il colore del tuo rituale? Scrivilo nei commenti.\n\n"
             f"{DOVE}\n\n{TAG} #neon #logo"),
}
CAROSELLO = {  # prima riga della didascalia del carosello, al posto di quella del reel
    "due-nature": "Scorri: da una parte l'ordine, dall'altra l'istinto.",
    "lupi": "I Lupi non dormono mai. Scorri.",
    "abbonamenti": "Scorri i quattro piani e scegli il tuo ritmo.",
    "apollineo": "Scorri il Rituale Apollineo.",
    "dionisiaco": "Scorri il Rituale Dionisiaco.",
    "salone": "Scorri e entra nel salone.",
    "quale": "Scorri, rispondi e conta le A e le D.",
    "famiglia": "Scorri: questa è la famiglia Ritual.",
    "equilibrio": "Scorri e stacca dal rumore.",
    "neon": "Scorri i cinque colori.",
}


def carosello_testo(chiave):
    return CAROSELLO[chiave] + "\n\n" + TESTI[chiave]


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
    reel("2026-11-21", "lupi", "lupi/reel-lupi.mp4", rito="dionisiaco")
    car("2026-11-22", "lupi", "lupi/carosello", rito="dionisiaco")
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
                     stato="attende materiale", nota="Servono le riprese del trattamento barba entro il 1° dicembre."))
    prodotto("2026-12-08", "chianti", "2026-12-09")
    prodotto("2026-12-10", "gran-paradiso", "2026-12-11")
    voci.append(dict(data="2026-12-12", ora="18:47", tipo="reel", contenuto="ritualized", rituale="dionisiaco",
                     stato="attende materiale", nota="Serve un prima/dopo dello stesso cliente entro l'8 dicembre."))
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
    # gennaio, sabato e domenica: neon, famiglia, equilibrio (jolly: possono coprire il 5 o il 12 dicembre
    # se le riprese di beard ritual / prima-dopo non arrivano in tempo)
    reel("2027-01-02", "neon", "neon/reel-neon.mp4", rito="entrambi")
    car("2027-01-03", "neon", "neon/carosello", rito="entrambi")
    reel("2027-01-09", "famiglia", "famiglia/reel-famiglia.mp4", rito="entrambi")
    car("2027-01-10", "famiglia", "famiglia/carosello", rito="entrambi")
    reel("2027-01-16", "equilibrio", "equilibrio/reel-equilibrio.mp4", rito="entrambi")
    car("2027-01-17", "equilibrio", "equilibrio/carosello", rito="entrambi")
    for v in voci:
        if v["contenuto"] in ("famiglia", "equilibrio"):
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
