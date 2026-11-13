"""Didascalie Instagram di Ritual Barber Studio, scritte una per una.

Regole (docs/brand-profile.md e doc "Strategia di comunicazione e vendita", da Daniel Pink):
prima riga = domanda entro ~125 caratteri, una sola cornice, massimo tre benefici, dettaglio
onesto quando serve, una sola CTA, la riga più forte in fondo prima dell'indirizzo,
3–5 hashtag, la parola "rituale" sempre presente. Nessuna urgenza finta, nessuna promessa miracolosa.
"""

DOVE = "📍 Ritual Barber Studio · Corso Umberto I 300c, Bernalda"


def post(testo, tag, gancio_carosello=None):
    return {"testo": testo.strip(), "tag": tag, "carosello": gancio_carosello}


def componi(voce, carosello=False):
    """Didascalia finale: per il carosello cambia solo la prima riga (il gancio)."""
    testo = voce["testo"]
    if carosello and voce.get("carosello"):
        testo = voce["carosello"] + "\n" + testo.split("\n", 1)[1]
    return f"{testo}\n\n{DOVE}\n\n{voce['tag']}"


PRODOTTI = {
    "amarone": post("""
Il ciuffo perfetto alle 8, sparito alle 11?

Amarone è il gel a tenuta forte della linea Barba Italiana: una passata al mattino e la forma regge fino a sera.
Tenuta 8, lucentezza 5. Con olio di vinaccioli dai vigneti italiani, antiossidante. Senza siliconi, parabeni e SLS.

Al prossimo taglio te lo applichiamo noi, così vedi come tiene.

Rituale Apollineo: ogni linea al suo posto, fino a sera.""",
        "#ritualbarberstudio #barbaitaliana #gelcapelli #apollineo",
        "Quanto deve tenere un gel per meritarsi la parola «forte»?"),

    "chianti": post("""
Gel o pasta? E se non dovessi scegliere?

Chianti è un pastagel: la tenuta del gel con la morbidezza della pasta.
Tenuta 7, lucentezza 7: forma decisa e capello che brilla. Con olio di vinaccioli, che nutre. Senza siliconi, paraffina e SLS.

Scrivici in DM com'è il tuo capello: ti diciamo se è quello giusto.

Per chi il rituale della mattina se lo inventa ogni giorno.""",
        "#ritualbarberstudio #barbaitaliana #pastagel #dionisiaco",
        "Ti piace un capello che si nota, ma resta morbido?"),

    "nebbiolo": post("""
Perché il ciuffo crolla sempre prima di pranzo?

Spesso è il prodotto: troppo morbido per il tuo capello.
Nebbiolo è una pasta opaca a tenuta 8: struttura forte, zero lucido, texture cremosa che si lavora facilmente. L'olio di vinaccioli evita di seccare il capello.

Mandalo a quell'amico che si sistema il ciuffo ogni dieci minuti.

Effetto naturale, forma che non molla. Rituale Dionisiaco, zero lucido.""",
        "#ritualbarberstudio #barbaitaliana #pastaopaca #mattehair",
        "Opaco o lucido: tu da che parte stai?"),

    "primitivo": post("""
I tuoi ricci decidono ogni mattina da che parte andare?

Primitivo è un gel disciplinante a fissaggio leggero, pensato per capelli ricci e mossi: tiene a bada il crespo senza l'effetto bagnato.
Con olio di vinaccioli, che protegge il capello e gli dà luce.

Al prossimo appuntamento lo proviamo sui tuoi ricci.

Ordine con i tuoi ricci, non contro. Anche questo è un rituale.""",
        "#ritualbarberstudio #barbaitaliana #capelliricci #anticrespo",
        "Il crespo d'inverno: lo combatti o lo guidi?"),

    "nero-d-avola": post("""
Qualche capello bianco che proprio non ti convince?

Nero d'Avola è un gel con un riflesso scuro: mentre ti pettini rende i bianchi meno evidenti, in modo naturale. Tenuta leggera, con olio di vinaccioli per morbidezza e luce.

Una cosa chiara: non è una tinta. Non copre del tutto, attenua.

In salone te lo mostriamo su una ciocca, prima di decidere.

Nessun cambio di colore. Solo meno grigio in vista, nel tuo rituale di ogni mattina.""",
        "#ritualbarberstudio #barbaitaliana #capellibianchi #grigio",
        "Tinta sì o tinta no? C'è una via di mezzo."),

    "bonarda": post("""
Capelli in ordine, ma senza che si veda il prodotto?

Bonarda è un'acqua fissativa: si spruzza, si modella con le dita e resta flessibile.
Effetto opaco tipo acqua di mare, tenuta 7, zero lucido. Con olio di vinaccioli, per dare volume senza peso.

Salvalo per quando vuoi un look più naturale.

Il capello di chi torna dal mare. Anche a febbraio: questo è il rituale.""",
        "#ritualbarberstudio #barbaitaliana #seasalt #capelliuomo",
        "Ti manca il capello di agosto?"),

    "soave": post("""
Capelli secchi e pettine che si incastra a ogni passata?

Soave è uno spray idratante: districa, ammorbidisce e rinfresca il cuoio capelluto.
Lascia una scia di incenso, patchouli e ylang ylang. Senza siliconi, paraffina e SLS.

Al prossimo appuntamento te lo spruzziamo noi: senti il profumo.

Dieci secondi di gesto, e il rituale della mattina cambia.""",
        "#ritualbarberstudio #barbaitaliana #capelliuomo #incenso",
        "Che profumo hanno i tuoi capelli?"),

    "tiziano": post("""
Barba ruvida che punge, a te e a chi ti sta vicino?

Spesso non è la barba: è la pelle secca sotto.
Tiziano è un olio da barba con argan, avocado e macadamia: poche gocce e il pelo diventa morbido e lucido. Prima della rasatura ammorbidisce il pelo. Con burro di karité e vitamina E, senza siliconi, parabeni e SLS.

Raccontaci in DM com'è la tua barba: ti diciamo quante gocce servono.

Una barba morbida si nota. Soprattutto da vicino.""",
        "#ritualbarberstudio #barbaitaliana #oliobarba #beardoil",
        "Quante gocce servono per una barba morbida?"),

    "caronte": post("""
Ti accorgi che i capelli si stanno diradando?

Caronte è una lozione stimolante con caffeina e menta piperita, più acido ialuronico e pantenolo. Si applica sul cuoio capelluto e dà un effetto a tutto volume.

Non fa miracoli in una settimana: chiede costanza, ogni giorno. E se la caduta è forte, il primo passo è un dermatologo.

In salone guardiamo insieme il tuo cuoio capelluto e ti diciamo se fa per te.

Prima te ne occupi, più capelli tieni. Il rituale comincia oggi.""",
        "#ritualbarberstudio #barbaitaliana #caduta #capelliuomo",
        "Lo noti di più sotto la luce del bagno?"),

    "gran-paradiso": post("""
Ti radi e dopo dieci minuti la pelle brucia?

Gran Paradiso è una crema post rasatura con stella alpina e liquirizia, ippocastano e ribes nero.
Idrata, lenisce e rinfresca, anche la pelle sensibile.

Salvalo per la prossima rasatura.

Il rituale della rasatura finisce quando la pelle smette di tirare.""",
        "#ritualbarberstudio #barbaitaliana #dopobarba #pellesensibile",
        "Pelle sensibile e rasatura possono andare d'accordo?"),

    "monte-bianco": post("""
Per te rasatura vuol dire irritazione?

Spesso il problema è la schiuma: troppo leggera, e la lama tira.
Monte Bianco è una mousse da rasatura densa e senza gas, che fa scorrere la lama sulla pelle invece che contro. Con stella alpina e ribes nero. Senza siliconi, paraffina e SLS.

Prenota una rasatura in salone e senti la differenza.

La lama scorre, la pelle respira. Il rituale è questo.""",
        "#ritualbarberstudio #barbaitaliana #rasatura #shaving",
        "Schiuma in bomboletta o mousse senza gas?"),

    "virgilio": post("""
Cosa fai subito dopo la rasatura?

Se la risposta è «niente», la pelle se ne accorge.
Virgilio è un tonico viso a tripla azione: lenisce, rinfresca e idrata in uno spruzzo. Camomilla e mentolo, con bisabololo e acido ialuronico.

Scrivi nei commenti cosa usi tu dopo la lama.

Un gesto di tre secondi che chiude il rituale.""",
        "#ritualbarberstudio #barbaitaliana #tonico #dopobarba",
        "Brucia o rinfresca? Dipende da cosa usi dopo la lama."),

    "barbera": post("""
Ciocche piatte che a metà mattina sembrano tutte uguali?

Barbera è una cera definente: separa e definisce ogni ciocca e tiene la forma tutto il giorno.
Con olio di vinaccioli, per definire senza seccare.

Al prossimo taglio te la applichiamo noi: vedi la differenza allo specchio.

Il carattere sta nei dettagli. Il rituale anche.""",
        "#ritualbarberstudio #barbaitaliana #ceracapelli #dionisiaco",
        "Cera, pasta o gel: quale serve al tuo taglio?"),

    "le-madonie": post("""
Viso spento a fine giornata, anche quando hai dormito?

Le Madonie è un siero viso idratante e tonificante con la manna delle Madonie, la linfa del frassino di Sicilia.
Poche gocce al mattino e la pelle torna tonica e idratata.

Salvalo per il tuo rituale del mattino.

Dalla Sicilia, una goccia alla volta.""",
        "#ritualbarberstudio #barbaitaliana #sieroviso #skincareuomo",
        "Hai mai sentito parlare della manna delle Madonie?"),

    "felice": post("""
Pelle opaca e pori che sembrano sempre chiusi?

Felice è un fango detossinante granulare con bucce d'uva bio, limoni di Sicilia, mele del Trentino e crusca.
Pulisce in profondità e libera la pelle dalle impurità.

Mandalo a chi rimanda la pulizia del viso da mesi.

Il rituale del fango, come in salone. A casa tua.""",
        "#ritualbarberstudio #barbaitaliana #fangoviso #skincareuomo",
        "Uva, limone e mela: ricetta della nonna o skincare?"),

    "monte-cimone": post("""
Occhiaie da notti troppo corte?

Monte Cimone è un filler rimpolpante per il contorno occhi con aceto balsamico di Modena invecchiato.
Contro occhiaie e borse, per uno sguardo più disteso con un gesto al mattino.

Non sostituisce il sonno: aiuta il tuo sguardo a non raccontarlo a tutti.

Salvalo per il prossimo lunedì mattina. Il rituale parte dagli occhi.""",
        "#ritualbarberstudio #barbaitaliana #occhiaie #skincareuomo",
        "Aceto balsamico sul viso? Sì, e c'è un perché."),

    "donatello": post("""
Pelle ruvida e opaca anche dopo la rasatura?

Donatello è una crema peeling che esfolia delicatamente: toglie lo strato spento e lascia il viso liscio, pulito e luminoso.
Con lavanda e melissa, mirtillo e liquirizia.

Chiedici in salone ogni quanto usarla sulla tua pelle.

Prima si toglie il vecchio, poi arriva il nuovo. Anche questo è un rituale.""",
        "#ritualbarberstudio #barbaitaliana #peeling #skincareuomo",
        "Quando hai fatto l'ultimo peeling?"),

    "ovidio": post("""
Pelle lucida già a metà giornata?

Ovidio è un tonico astringente e purificante: riequilibra la pelle e la libera dall'effetto lucido.
Con uva, zenzero e boswellia, un tonico balsamico che dà energia.

Scrivici in DM com'è la tua pelle a mezzogiorno: ti diciamo se fa per te.

Meno lucido, più presenza. Il rituale che rimette in ordine la pelle.""",
        "#ritualbarberstudio #barbaitaliana #tonicoviso #skincareuomo",
        "Zenzero sul viso: a cosa serve davvero?"),

    "passerina": post("""
Capelli fini che si appiattiscono appena esci di casa?

Passerina è una polvere texturizzante: un pizzico alla radice e il volume arriva subito.
Effetto opaco e naturale.

Al prossimo taglio te la proviamo alla radice: due secondi e vedi.

Più volume, stesso capello. Il rituale più veloce che c'è.""",
        "#ritualbarberstudio #barbaitaliana #volume #capellifini",
        "Volume vero con un pizzico di polvere?"),

    "ercole": post("""
Quanti minuti hai, la mattina, per te?

Ercole è una doccia shampoo tonificante: corpo e capelli in un solo gesto.
Arancia e ginepro per l'energia, dattero e aloe per la morbidezza.

Mandalo a chi ha tre flaconi sulla mensola della doccia.

Un flacone, un gesto, e sei pronto. Il rituale della mattina, semplificato.""",
        "#ritualbarberstudio #barbaitaliana #docciashampoo #corpo",
        "Corpo e capelli con un solo prodotto: si può?"),

    "nettuno": post("""
La pelle tira appena esci dalla doccia?

Nettuno è una doccia shampoo idratante e rinfrescante: con olio di argan, aloe bio e dattero, idrata e ammorbidisce pelle e capelli insieme.

Scrivici in DM e te lo mettiamo da parte.

La doccia come dovrebbe essere: fresca, e senza pelle che tira. Il rituale comincia lì.""",
        "#ritualbarberstudio #barbaitaliana #docciashampoo #argan",
        "Argan e aloe sotto la doccia: che differenza fa?"),

    "scala": post("""
Più capelli sul cuscino del solito?

Scala è uno shampoo coadiuvante anticaduta con bergamotto e ginepro, menta ed eucalipto.
Rinvigorisce e dà volume, lavaggio dopo lavaggio.

È un coadiuvante: dà risultati con la costanza, non in un giorno. Se la caduta è forte, non basta da solo.

In salone ti diciamo se abbinarlo a una lozione come Caronte o Farnese.

Ogni lavaggio conta. È un rituale, non un colpo di fortuna.""",
        "#ritualbarberstudio #barbaitaliana #anticaduta #capelliuomo",
        "Uno shampoo può davvero aiutare contro la caduta?"),

    "farnese": post("""
Capelli più sottili di qualche anno fa?

Farnese è una lozione coadiuvante anticaduta da usare ogni giorno: caffeina, citrullina e vitamina PP, con un'azione stimolante ed energizzante sul cuoio capelluto.

Non è una cura miracolosa: chiede costanza. E se la caduta è forte, parlane con un dermatologo.

Passa in salone: guardiamo insieme il cuoio capelluto.

Ogni giorno, un passo in più. Il rituale che premia chi non molla.""",
        "#ritualbarberstudio #barbaitaliana #anticaduta #caffeina",
        "Caffeina sul cuoio capelluto: perché?"),
}


BRAND = {
    "due-nature": post("""
Ordine o istinto: tu da che parte stai?

L'ordine ti dà la forma. L'istinto ti dà il carattere. Ogni uomo li ha tutti e due, e noi li curiamo entrambi: il Rituale Apollineo per chi vuole ogni linea al suo posto, il Dionisiaco per chi lo stile se lo inventa.

Scrivi A o D nei commenti.

Due nature. Un solo Rituale.""",
        "#ritualbarberstudio #apollineo #dionisiaco #bernalda",
        "Quale delle due nature ti somiglia di più?"),

    "famiglia": post("""
E se il barbiere sapesse già come porti la barba?

Stessa poltrona, stesse mani, ogni volta. I tuoi attrezzi sono pronti prima che tu entri e il tuo posto è sempre libero: è quello che succede con gli abbonamenti Ritual.

Chiedi in salone come funziona.

Non sei un cliente. Sei uno di noi.""",
        "#ritualbarberstudio #abbonamento #famigliaritual #bernalda",
        "Cosa cambia quando il barbiere ti conosce davvero?"),

    "abbonamenti": post("""
Quanto vale avere il tuo posto in poltrona sempre pronto?

Con gli abbonamenti Ritual il taglio smette di essere una cosa da incastrare: diventa un appuntamento fisso con te stesso, a un prezzo che premia la costanza. Quattro piani, uno per ogni ritmo.
Chi entra adesso entra come Socio Fondatore.

Scrivici in DM il tuo ritmo: ti diciamo quale piano fa per te.

Il rituale non si rincorre. Ti aspetta.""",
        "#ritualbarberstudio #abbonamento #sociofondatore #bernalda",
        "Ogni settimana o ogni tre: qual è il tuo ritmo?"),

    "apollineo": post("""
Ti piace quando ogni linea è al suo posto?

Il Rituale Apollineo è per chi ama la precisione: sfumatura a pelle, barba disegnata al millimetro, lo stesso gesto ogni volta, fatto bene.
Ordine. Misura. Controllo.

Se ti ci riconosci, scrivi A nei commenti.

La disciplina non ti limita: ti definisce.""",
        "#ritualbarberstudio #apollineo #skinfade #beardgrooming",
        "Quanto ti dà fastidio una linea storta?"),

    "dionisiaco": post("""
E se questa volta cambiassi tutto?

Il Rituale Dionisiaco è per chi taglia, rompe e ricomincia: texture, mullet, trasformazioni che si notano.
Istinto. Eccesso. Libertà.

Se ti ci riconosci, scrivi D nei commenti.

Nessuno schema. Solo carattere.""",
        "#ritualbarberstudio #dionisiaco #mullet #texturedhair",
        "Da quanto tempo porti lo stesso taglio?"),

    "salone": post("""
Lo sapevi che anche l'attesa fa parte del rituale?

Qui ogni strumento ha il suo posto e ogni gesto il suo perché. Una poltrona, la luce giusta, i quadri alle pareti, nessuna fila.

Vieni a vederlo dal vivo: prenota in DM.

Fuori il mondo corre. Qui il tempo torna tuo.""",
        "#ritualbarberstudio #barbershop #bernalda #salone",
        "Hai mai fatto caso a cosa c'è appeso alle nostre pareti?"),

    "regalo": post("""
Cosa regali a un uomo che ha già tutto?

Un rituale. Cura uomo made in Italy con estratti naturali, scelta insieme a te: raccontaci com'è lui, barba, capelli, pelle, e il regalo giusto lo troviamo noi.

Scrivici in DM o passa in salone.

Il regalo perfetto ha carattere. Regala un rituale.""",
        "#ritualbarberstudio #regalouomo #natale #barbaitaliana"),

    "regalo-ultimi": post("""
Hai ancora un uomo nella lista dei regali?

Passa in salone: in pochi minuti ti prepariamo il regalo giusto, con prodotti made in Italy e un consiglio su misura per lui.

Il 24 arriva per tutti. Il rituale giusto, per chi passa prima.""",
        "#ritualbarberstudio #regalouomo #natale #bernalda"),

    "quale": post("""
Quale rituale sei?

Cinque scelte, nessuna risposta sbagliata. Conta le A e le D: più A sei Apollineo, ordine e misura. Più D sei Dionisiaco, istinto e libertà.

Scrivi il tuo risultato nei commenti.

Ogni uomo ha due nature. Una, però, parla più forte.""",
        "#ritualbarberstudio #apollineo #dionisiaco #test",
        "Cinque domande per scoprire quale rituale sei: pronto?"),

    "neon": post("""
Di che colore è il tuo rituale?

Rosso, oro, ghiaccio, viola o bianco: il nostro segno acceso in cinque luci diverse.

Scrivi il tuo colore nei commenti.

Stesso segno. La luce la scegli tu.""",
        "#ritualbarberstudio #neon #logo #bernalda",
        "Cinque luci, un solo segno: quale accenderesti?"),

    "equilibrio": post("""
Quando è stata l'ultima volta che nessuno ti ha cercato per mezz'ora?

Qui il telefono resta a faccia in giù. Panno caldo e vapore, fango sul viso, un gesto alla volta: mezz'ora per te, e il tuo ritmo torna.

Prenota il tuo momento in DM.

Stacca dal rumore. Ritrova l'equilibrio, un rituale alla volta.""",
        "#ritualbarberstudio #equilibrio #slowliving #bernalda",
        "Riesci a staccare davvero per mezz'ora?"),

    "beard-ritual": post("""
La tua barba la curi o la sopporti?

Il Beard Ritual è il trattamento completo: panno caldo per ammorbidire, contorni disegnati a rasoio, olio e balsamo con estratti naturali.
Linee nette, pelle che respira, barba che resta in ordine.

Prenota il tuo Beard Ritual in DM.

Non è solo barba. È il tuo biglietto da visita.""",
        "#ritualbarberstudio #beardritual #barba #apollineo"),

    "ritualized": post("""
Quanto può cambiare un uomo in un'ora di poltrona?

Questo è Ritualized: stesso cliente, prima e dopo. Nessun filtro, solo forbici, rasoio e la voglia di cambiare.

Se vuoi il tuo, scrivici RITUALIZED in DM.

Entri com'eri. Esci come sei.""",
        "#ritualbarberstudio #ritualized #primaedopo #dionisiaco"),
}


VISUAL = {
    "rasoio": post("""
Quanti secondi servono per un contorno perfetto?

Pochi, se la mano è ferma. Il rasoio non perdona: o il gesto è preciso, o si vede. Per questo da noi ogni contorno si fa con calma.

La precisione non si improvvisa. Si allena, rituale dopo rituale.""",
        "#ritualbarberstudio #rasoio #straightrazor #bernalda"),

    "vapore": post("""
Perché il panno caldo arriva prima della lama?

Il calore ammorbidisce il pelo e prepara la pelle: la lama scorre senza tirare e la pelle si irrita meno. E quei due minuti di vapore sono già un modo per staccare.

Il rituale comincia prima della lama.""",
        "#ritualbarberstudio #pannocaldo #hottowel #rasatura"),

    "poltrona": post("""
Hai un posto dove il tempo è solo tuo?

Una poltrona, la luce giusta, nessuna fila. Qui ogni appuntamento ha il suo spazio.

Siediti. Il resto può aspettare: adesso c'è il tuo rituale.""",
        "#ritualbarberstudio #barberchair #barbershop #bernalda"),

    "uomo-barba": post("""
Cosa dice di te il tuo stile, prima ancora che tu parli?

Un taglio pulito e una barba curata sono il primo messaggio che mandi: a un colloquio come a cena.

Salvalo per ricordartelo la prossima volta che rimandi il taglio.

Lo stile è disciplina che si vede. Il rituale la rende abitudine.""",
        "#ritualbarberstudio #menstyle #barba #gentleman"),

    "prodotti": post("""
Sai cosa c'è dentro quello che metti sulla pelle ogni mattina?

In salone consigliamo cura uomo made in Italy con estratti naturali, e per ogni prodotto ti diciamo cosa contiene e a cosa serve. Niente formule a caso.

Al prossimo appuntamento chiedici quale fa per te.

Quello che usi ogni giorno dice chi sei. Sceglilo come un rituale.""",
        "#ritualbarberstudio #barbaitaliana #madeinitaly #estrattinaturali"),

    "pennello": post("""
Hai mai fatto la barba con il pennello?

Schiuma calda montata a mano, il pelo che si alza, la lama che scorre senza tirare. È il modo più antico, e resta quello che preferiamo.

Certi rituali non vanno aggiornati. Vanno rispettati.""",
        "#ritualbarberstudio #shavingbrush #wetshave #rasatura"),

    "lime-olio": post("""
Possono bastare tre gocce per cambiare una barba?

Se sono le gocce giuste, sì. L'olio da barba nutre il pelo, ammorbidisce la pelle sotto e calma il prurito dei primi giorni. Poche gocce ogni mattina, massaggiate fino alla radice.

Non fa miracoli in una notte: lavora con la costanza.

La cura sta nei dettagli. Il rituale anche.""",
        "#ritualbarberstudio #beardoil #oliobarba #barba"),

    "lime-polsino": post("""
Ti sei mai sentito pronto prima ancora di uscire di casa?

Con un taglio fresco ti guardi allo specchio e non c'è niente da correggere: resta solo da sistemare il polsino.

Essere pronti è un'abitudine. Il rituale la costruisce.""",
        "#ritualbarberstudio #menstyle #gentleman #dettagli"),

    "lime-logo": post("""
Rosso o lime: quale ti rappresenta?

Il nostro segno ha un nuovo colore. Stessa disciplina, energia diversa.

Scrivi R o L nei commenti.

Cambia il colore. Il rituale resta.""",
        "#ritualbarberstudio #lime #logo #bernalda"),
    "lime-la-lama": post("""
Cosa c'entra una katana con un barbiere?

Più di quanto sembri. Una lama vale quanto la mano che la guida: precisione, calma, nessun gesto di troppo. È lo stesso principio che seguiamo in poltrona.

Scrivi nei commenti se l'avevi notata in salone.

La lama si rispetta. Il rituale anche.""",
        "#ritualbarberstudio #katana #precisione #bernalda"),

    "lime-strumenti": post("""
Quanti attrezzi servono per un taglio fatto bene?

Due pettini, due forbici, un rasoio. Pochi, scelti, sempre al loro posto: ognuno ha un compito preciso e nessuno si improvvisa.

Salvalo se anche tu ami l'ordine.

Ogni attrezzo al suo posto. È così che comincia il rituale.""",
        "#ritualbarberstudio #barbertools #forbici #apollineo"),

    "lime-sfere": post("""
Hai mai fatto caso a cosa ti aspetta alla cassa?

Due sfere di vetro, un piatto nero, il marmo. Dettagli che non servono a tagliare, ma a farti capire dove sei appena entri.

Vieni a vederle dal vivo: prenota in DM.

Il rituale comincia prima della poltrona.""",
        "#ritualbarberstudio #interiordesign #dettagli #bernalda"),

    "lime-xceed": post("""
Cosa c'è dietro una sfumatura perfetta?

Mani allenate e strumenti all'altezza. Le nostre tosatrici Gamma+ Xceed sono cariche e pronte prima che tu entri, così il tempo in poltrona è tutto per il tuo taglio.

Scrivi nei commenti che tosatrice usi a casa.

Gli strumenti contano. Il rituale li rende precisi.""",
        "#ritualbarberstudio #gammapiu #xceed #skinfade"),
}
