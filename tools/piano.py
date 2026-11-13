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
    """Struttura (vedi docs/strategia-comunicazione.md): domanda che fa emergere il problema, esperienza,
    estratto, tre benefici al massimo, un dettaglio onesto se serve, chiusura forte in fondo."""
    p = PROD[slug]; nome, frase, tag = RITO[p["ritual"]]
    # senza estratto naturale (es. Passerina) i benefici bastano: niente riga ripetuta né #estrattinaturali
    estratto = "" if p.get("ing_label") else f"Il cuore della formula: {p['ingredient'].lower()}. {plain(p['ingredient_note'])}.\n"
    prova = "sulla tua pelle" if p["line"] in ("viso", "corpo") else ("sulla tua barba" if p["line"] == "barba" else "sui tuoi capelli")
    return (f"{p['hook']}\n\n"
            f"{p['name']}, {p['category'][0].lower() + p['category'][1:]}. {p['frame']}\n\n"
            f"{estratto}"
            + "\n".join(f"· {plain(x)}" for x in [x for x in p["specs"] if not plain(x).startswith("Con ")][:3]) + "\n\n"
            + (f"{p['onesto']}\n\n" if p.get("onesto") else "")
            + f"{nome}: {frase}.\n"
            f"{'Scorri fino all’ultima slide.' if carosello else 'Guarda fino alla fine.'}\n\n"
            f"Al prossimo appuntamento te lo facciamo provare {prova}.\n\n{DOVE}\n\n"
            f"{TAG} {tag} #barbaitaliana #madeinitaly{'' if p.get('ing_label') else ' #estrattinaturali'} #{p['line']}")


TESTI = {
    "due-nature": ("Ordine o istinto: tu da che parte stai?\n\n"
                   "L'ordine ti dà la forma. L'istinto ti dà il carattere. Ogni uomo li ha entrambi: noi li curiamo tutti e due.\n\n"
                   "Scrivi A o D nei commenti.\n"
                   "Due nature. Un solo Rituale.\n\n"
                   f"{DOVE}\n\n{TAG} #apollineo #dionisiaco #menstyle"),
    "abbonamenti": ("Quanto vale avere il tuo posto in poltrona sempre pronto?\n\n"
                    "Con gli abbonamenti Ritual il taglio non è più una cosa da incastrare: è un appuntamento fisso con te stesso, "
                    "a un prezzo che premia la costanza. Quattro piani, uno per ogni ritmo: scorri e trova il tuo.\n\n"
                    "Chi entra ora entra come Socio Fondatore.\n\n"
                    "Entra nella famiglia: chiedi in salone o scrivici in DM.\n\n"
                    f"{DOVE}\n\n{TAG} #abbonamento #sociofondatore #cura"),
    "apollineo": ("Ti piace quando ogni linea è al suo posto?\n\n"
                  "Il Rituale Apollineo è per chi ama la precisione: sfumatura a pelle, barba disegnata al millimetro, "
                  "lo stesso gesto ogni settimana.\n"
                  "Ordine. Misura. Controllo.\n\n"
                  "Sei Apollineo? Scrivi A nei commenti.\n"
                  "La disciplina non ti limita: ti definisce.\n\n"
                  f"{DOVE}\n\n{TAG} #apollineo #skinfade #beardgrooming"),
    "dionisiaco": ("E se questa volta cambiassi tutto?\n\n"
                   "Il Rituale Dionisiaco è per chi taglia, rompe e ricomincia: texture, mullet, trasformazioni.\n"
                   "Istinto. Eccesso. Libertà.\n\n"
                   "Sei Dionisiaco? Scrivi D nei commenti.\n"
                   "Nessuno schema, solo carattere.\n\n"
                   f"{DOVE}\n\n{TAG} #dionisiaco #mullet #texturedhair"),
    "salone": ("Quando è stata l'ultima volta che nessuno ti ha messo fretta?\n\n"
               "Una poltrona, ogni strumento al suo posto, ogni gesto con il suo perché. Anche l'attesa fa parte del rito.\n"
               "La cura di sé non è vanità: è disciplina.\n\n"
               "Fuori il mondo corre. Qui dentro il tempo torna tuo.\n"
               "Non è un taglio. È un rituale.\n\n"
               f"{DOVE}\n\n{TAG} #barbershopinterior #salone"),
    "regalo": ("Cosa regali a un uomo che ha già tutto?\n\n"
               "Un momento solo per lui. Cura uomo made in Italy con estratti naturali: vinaccioli, argan, stella alpina, caffeina.\n"
               "Dicci com'è lui: barba, capelli, pelle. Il regalo giusto lo scegliamo insieme.\n\n"
               "Vieni in salone o scrivici in DM.\n"
               "Il regalo perfetto ha carattere. Regala un rituale.\n\n"
               f"{DOVE}\n\n{TAG} #regalouomo #natale #barbaitaliana"),
    "regalo-ultimi": ("Hai ancora un uomo nella lista dei regali?\n\n"
                      "Passa in salone: in pochi minuti ti prepariamo il regalo giusto, con prodotti made in Italy e un consiglio su misura.\n\n"
                      "Il 24 arriva per tutti. Il rituale giusto, solo per chi passa prima.\n\n"
                      f"{DOVE}\n\n{TAG} #regalouomo #natale #ultimominuto"),
    "quale": ("Quale rituale sei?\n\n"
              "5 scelte, nessuna risposta sbagliata. Conta le A e le D.\n"
              "Più A: sei Apollineo. Ordine, misura, controllo.\n"
              "Più D: sei Dionisiaco. Istinto, eccesso, libertà.\n\n"
              "Scrivi il tuo risultato nei commenti e tagga un amico che è l'esatto opposto.\n\n"
              f"{DOVE}\n\n{TAG} #apollineo #dionisiaco #test"),
    "famiglia": ("E se il barbiere sapesse già come porti la barba?\n\n"
                 "Stessa poltrona, stesse mani, ogni settimana. I tuoi attrezzi sono pronti prima che tu entri, "
                 "e il tuo posto è sempre libero.\n"
                 "Con gli abbonamenti Ritual non rincorri il tempo: è lui ad aspettarti.\n\n"
                 "Chiedi in salone o scrivici in DM.\n"
                 "Non sei un cliente. Sei uno di noi.\n\n"
                 f"{DOVE}\n\n{TAG} #abbonamento #famiglia #cura"),
    "equilibrio": ("Quando è stata l'ultima volta che nessuno ti ha cercato per mezz'ora?\n\n"
                   "Qui il telefono resta a faccia in giù. Panno caldo e vapore, fango sul viso, una mossa alla volta.\n"
                   "Mezz'ora per te, e il tuo ritmo torna.\n\n"
                   "Stacca dal rumore. Ritrova l'equilibrio.\n\n"
                   f"{DOVE}\n\n{TAG} #equilibrio #slowliving #cura"),
    "neon": ("Qual è il colore del tuo rituale?\n\n"
             "Rosso, ghiaccio, viola, bianco: scrivilo nei commenti.\n"
             "Il nostro segno, acceso.\n\n"
             f"{DOVE}\n\n{TAG} #neon #logo"),
    "beard-ritual": ("La tua barba la curi o la sopporti?\n\n"
                     "Il Beard Ritual è il trattamento completo della barba: panno caldo per ammorbidire, contorni disegnati a rasoio, "
                     "olio e balsamo con estratti naturali.\n"
                     "Linee nette. Pelle che respira. Una barba che resta al suo posto tutto il giorno.\n\n"
                     "Una barba curata non cresce da sola: si costruisce, una seduta alla volta.\n"
                     "Non è solo barba. È il tuo biglietto da visita.\n\n"
                     f"{DOVE}\n\n{TAG} #beardritual #beardgrooming #barba #apollineo"),
    "ritualized": ("Quanto può cambiare un uomo in un'ora di poltrona?\n\n"
                   "Questo è Ritualized: stesso cliente, prima e dopo. Nessun filtro, solo forbici, rasoio e la voglia di cambiare.\n\n"
                   "Se vuoi il tuo, scrivici RITUALIZED in DM e lo progettiamo insieme.\n"
                   "Entri com'eri. Esci come sei.\n\n"
                   f"{DOVE}\n\n{TAG} #ritualized #primaedopo #transformation #dionisiaco"),
}
# post singoli della visual identity (immagini con logo, senza testo in grafica)
VISUAL = {
    "rasoio": ("Quanto conta la precisione in un gesto di pochi secondi?\n\n"
               "Il rasoio non perdona: o la mano è ferma, o si vede. Per questo ogni contorno, da noi, è fatto con calma.\n\n"
               "La precisione non si improvvisa. Si allena.\n\n"
               f"{DOVE}\n\n{TAG} #rasoio #straightrazor #precisione"),
    "vapore": ("Ti ricordi l'ultima volta che ti sei fermato davvero?\n\n"
               "Panno caldo e vapore: pochi minuti e la pelle è pronta. La testa pure.\n\n"
               "Il rito comincia prima della lama.\n\n"
               f"{DOVE}\n\n{TAG} #pannocaldo #hottowel #relax"),
    "poltrona": ("Hai un posto dove il tempo è solo tuo?\n\n"
                 "Una poltrona, la luce giusta, nessuna fretta. Qui ogni appuntamento ha il suo spazio e nessuno ti mette in fila.\n\n"
                 "Siediti. Il resto può aspettare.\n\n"
                 f"{DOVE}\n\n{TAG} #barberchair #poltrona"),
    "uomo-barba": ("Cosa dice di te il tuo stile, prima ancora che tu parli?\n\n"
                   "Un taglio pulito e una barba curata non sono vanità: sono il primo messaggio che mandi.\n\n"
                   "Lo stile è disciplina che si vede.\n\n"
                   f"{DOVE}\n\n{TAG} #menstyle #barba #gentleman"),
    "prodotti": ("Sai cosa metti sulla pelle ogni mattina?\n\n"
                 "In salone usiamo e consigliamo cura uomo made in Italy con estratti naturali: ogni ingrediente ha un perché. "
                 "Al prossimo appuntamento chiedici quale fa per te.\n\n"
                 "Quello che usi ogni giorno dice chi sei.\n\n"
                 f"{DOVE}\n\n{TAG} #barbaitaliana #madeinitaly #estrattinaturali"),
    "pennello": ("Hai mai fatto la barba con il pennello?\n\n"
                 "Schiuma calda montata a mano, il pelo che si alza, la lama che scorre senza tirare. "
                 "È il modo più antico, e ancora il migliore.\n\n"
                 "Certi gesti non vanno aggiornati. Vanno rispettati.\n\n"
                 f"{DOVE}\n\n{TAG} #shavingbrush #wetshave #rasaturatradizionale"),
    "lime-olio": ("Possono bastare tre gocce per cambiare una barba?\n\n"
                  "L'olio da barba nutre il pelo, ammorbidisce la pelle sotto e calma il prurito dei primi giorni. "
                  "Poche gocce ogni mattina, massaggiate fino alla radice.\n\n"
                  "Non fa miracoli in una notte: lavora con la costanza.\n"
                  "La cura sta nei dettagli. Anche nei più piccoli.\n\n"
                  f"{DOVE}\n\n{TAG} #beardoil #olioperbarba #barba"),
    "lime-polsino": ("Ti sei mai sentito pronto prima ancora di uscire di casa?\n\n"
                     "Con un taglio fresco ti guardi allo specchio e non c'è niente da correggere: "
                     "resta solo da sistemare il polsino.\n\n"
                     "Essere pronti è un'abitudine.\n\n"
                     f"{DOVE}\n\n{TAG} #menstyle #gentleman #dettagli"),
    "lime-logo": ("Rosso o lime: quale ti rappresenta?\n\n"
                  "Il nostro segno ha un nuovo colore. Stessa disciplina, energia diversa.\n\n"
                  "Scrivi R o L nei commenti.\n"
                  "Cambia il colore. Il rito resta.\n\n"
                  f"{DOVE}\n\n{TAG} #logo #lime #brandidentity"),
}
CAROSELLO = {  # prima riga della didascalia del carosello, al posto di quella del reel
    "due-nature": "Scorri: da una parte l'ordine, dall'altra l'istinto.",
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
