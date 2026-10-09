# «Nach innen» — Vertonung der Mantren als Vorlagen

*Werkstatt · Liedvorlagen · Runde 2 vom 9. 10. 2026*

Auftrag (9. 10. 2026): «Ich wünsche mir eine musikalische Vertonung der
Mantren. Beginne mit 1–7. Inspiration? Arvo Pärt, Ludovico Einaudi, Mine,
Bon Iver, Goldberg Variationen, Francis and the Lights, Rosalía, Brian Eno,
Pascal Schumacher, Billie Eilish, Radiohead. Was ist mit Elevenlabs möglich?
Nach Innen.»

Rückmeldung auf die Erstfassung (sieben Stücke nach Stunden, 9. 10. 2026):
«Die Gliederung nach Stunden geht nicht schön auf, besonders am Anfang. Die
1 ist unsinnig lang. Sie enthält mehrere Lieder. Nutze die Gliederung in
Titel, Motive und Sinnzusammenhänge. Der monotone Ansatz der Vertonung
spricht mich nicht an. Probiere mehr aus. Es braucht keinen künstlichen
Ernst oder starken seelischen Ausdruck. Die Gesangsstimme, die Töne
schaffen die Erlebnisse. Die oder der Singende stellt sich zur Verfügung.
Noch ein wichtiges, gutes Beispiel: Laurie Anderson „Songs from the Bardo".
Die Atmo sollte nicht billig-synthetisch wirken. Komplex, herausfordernd,
vertiefend, tiefe Gefühle ermöglichen. Deine 6. Stunde ist schön. Und sehr
lang. Also probier mehr aus, biete mir mehr an. Ich habe eine leise Ahnung.
Ich brauche Vorlagen, die Resonanz haben.»

Seither gilt: **Eine Vorlage ist eine Sinneinheit** (ein Titel der
Lesefassung: Erdengründe, Daseinswort, Drei Tiere, Willens-Stoß …) **in
einem Ansatz**, 1,3 bis 2,3 Minuten. Derselbe Text darf in zwei Ansätzen
stehen, damit sich vergleichen lässt. Die Stimme dient dem Text und trägt
nicht vor: keine Hauch-Stimme, kein Pathos, kein Vibrato. Instrumente sind
echte, in einem Raum. Der Text ist Wort für Wort die Lesefassung 2024 aus
`src/data/mantren.yaml`; die einzige Wiederholung ist das Daseinswort in
Vorlage 4. Die Musik erzeugt **Eleven Music** (`music_v2_5`) nach einem
Kompositionsplan je Vorlage, den `vertonen.py` aus den Mantren baut. Die
Audiodateien liegen nicht im Repo; sie lassen sich neu bauen, siehe unten.

## Die zwölf Vorlagen (Runde 2)

| Nr | Text | Ansatz | Worauf hören | Dauer |
|---|---|---|---|---|
| 1 | Erdengründe (1.1) | **Bardo.** Gesprochen über Klangschalen, Bordun und Geige, wie eine Anweisung an jemanden, der hinübergeht. Gong am Ende der ersten Hälfte, eine zweite tiefere Stimme auf den letzten zwei Zeilen. | Trägt der gesprochene Text ohne Melodie? Rückschrift 100 %. | 1,9 min |
| 2 | Erdengründe (1.1) | **Litanei.** Derselbe Text auf einem Ton rezitiert, Kadenz am Zeilenende, Harmonium und Cello; in der zweiten Hälfte eine zweite Stimme eine Quinte tiefer (Organum). | Vergleich mit 1: Sprechen oder Psalmodieren? | 1,8 min |
| 3 | Daseinswort (1.3) | **Chor.** A cappella, gemischter Chor in langsamen, sich verschiebenden Akkorden; «O, du Mensch, erkenne dich selbst» im Unisono auf einem tiefen Ton, dann öffnet sich der Akkord. | Die Harmonik: fordernd genug? | 1,5 min |
| 4 | Daseinswort (1.3) | **Ruf und Antwort.** Eine Männerstimme spricht die Zeilen über Filzklavier und gestrichenem Kontrabass, ein Chor aus einer Frauenstimme summt darunter und singt dann das Daseinswort, zweimal. | Vergleich mit 3. Bei 0:21 fehlt der Erkennung eine Zeile («Aus dem Schritte des Zeitenganges») — nachhören. | 2,0 min |
| 5 | Im Anblick der Schwelle (1.2) | **Der Hüter.** Eine Männerstimme, eine Oktave tiefer durch den Vocoder, halb gesprochen; Geige, Waterphone, analoger Bass. «Sieh, ich bin der Erkenntnis einzig Tor» spricht eine unverfremdete leise Frauenstimme. | Das Bardo-Muster der Autoritätsstimme. Rückschrift 100 % (zweiter Lauf; der erste sang erfundene Wörter). | 1,8 min |
| 6 | Drei Tiere (1.4) | **Sprechgesang.** Trocken, in 7/8; jedes Tier ein Instrument: Kontrabassklarinette (blau), präpariertes Klavier (gelbgrau), Glasharmonika (schmutzigrot). «Flügel» wird zum ersten Mal gesungen, mit Streichern. | Ohne den Abgrund-Vorspann (Teil 1 des Mantrams) — der gehört zu Vorlage 5 oder davor. | 2,3 min |
| 7 | Willens-Stoß (3) | **Lied.** Dieselbe schlichte Melodie für alle drei Strophen, Gitarre und Kontrabass, Strophe 2 mit zweiter Stimme in Terzen, Strophe 3 mit Akkordeon; ein Sänger, der nicht vorträgt. | Das Volkslied-Muster. Die Stimme wiederholt einmal «Ätherwesen weht in dir» (0:29). | 2,0 min |
| 8 | Schau die Drei · Tritt ein (7.1, 7.3) | **Hell.** Celesta, Nylongitarre, gebürstete Trommel, eine klare, leichte Popstimme; «Tritt ein» a cappella mit geschichteter Harmonie. | Darf ein Mantram leicht sein? Rückschrift 98 %. | 1,3 min |
| 9 | Erdenwerte I (6: Erde, Wasser, Luft) | **Variationen.** Der Ansatz der Erstfassung als eigenes Lied: fester Bass im Dreiertakt, Filzklavier, dann Cello, dann Streicher ohne Klavier. | Die gelobte 6 in halber Länge. | 2,1 min |
| 10 | Erdenwerte II (6: Licht, Gestalt, Leben) | **Streicher und Puls.** Die zweite Hälfte der Erstfassung als eigenes Lied: Streicher, leiser elektronischer Puls, der Chor aus einer Stimme auf den letzten zwei Zeilen. | Nach dem Text singt die Stimme im Nachspiel erfundene Silben (1:57) — bei Gefallen neu erzeugen. | 2,1 min |
| 11 | Es kämpft (5) | **Zwei Stimmen.** Eine Männerstimme spricht, eine Frauenstimme hält lange wortlose Töne auf den Schlüsselwörtern; Streichquartett in wandernden Dissonanzen, die spät auflösen; gestrichenes Vibraphon. | Bardo mit Pärt: Sprechen und ein Ton. Rückschrift 96 %. | 2,2 min |
| 12 | Tiefe – Weite – Höhe (4) | **Harmonizer.** Eine Stimme durch den Vocoder-Harmonizer, die Akkorde machen den Raum: tief und eng (Cello, Kontrabass), weit und offen (Quartett), hoch und schimmernd (Falsett, Flageoletts, E-Dur). | Die Stimme wiederholt bei 0:41 die ersten Zeilen und singt im Nachspiel «ihrem Tun» — nachhören. | 2,1 min |

Zusammen 23 Minuten, rund 21 000 Credits (dazu zwei Wiederholungen,
Vorlagen 4 und 5, rund 3 400). Alle zwölf sind auf −16 LUFS gemastert.

**Was die Prüfung sagt:** Scribe hat jede Vorlage zurückgeschrieben;
Wortübereinstimmung 83 bis 100 %. Gesprochene Vorlagen (1, 5) erreichen
100 %, gesungene liegen bei 85 bis 98 %, fast immer wegen getrennt
geschriebener Komposita («Welten Gestaltungsmächten»). Wirklich nachzuhören
sind die vier Stellen in der Tabelle (4, 7, 10, 12). **Eine Lehre:** Wo ein
Abschnitt ohne Text eine Stimme erlaubt («(ooh)», wortloser Chor), erfindet
das Modell gern Silben; wortlose Nachspiele bekommen künftig «vocals» in
die Gegen-Stile.

**Den Klang beurteilt Philipp.** Claude kann nicht hören. Die Frage an
jede Vorlage ist nicht «ist sie fertig», sondern «hat sie Resonanz» — dann
wird aus dem Ansatz die Regel für die nächsten Sinneinheiten.

## Die Stimmenprobe (Runde 3)

Auftrag (9. 10. 2026): «Gerne mehr Stimmen. Reifere! Charaktervollere!»

Eleven Music vergibt keine Stimm-IDs; die Stimme ist eine Beschreibung in
den Stilen. Zehn Stimmen singen oder sprechen darum **denselben Text**,
7.2 «Des Hüters letzte Mahnung» (drei kurze Strophen, 1,5 Minuten), jede
in der kleinen Besetzung, die zu ihr passt. So lässt sich die Stimme
vergleichen, nicht das Stück. Eine gewählte Stimme wird dann zur
Beschreibung in den anderen Vorlagen (`stimme` im Eintrag).

| Nr | Stimme | Besetzung | Nachhören |
|---|---|---|---|
| 13 | **Die Alte.** Eine Frau um siebzig, verwitterte Altstimme mit Korn und Luft, mehr gesprochen als gesungen. | Harmonium, Cello | Rückschrift 91 %, nur Schreibweisen. |
| 14 | **Der alte Mann.** Brüchiger tiefer Bariton, halb gesprochen, müde und freundlich. | Nylongitarre, Kontrabass | 96 %. |
| 15 | **Die Liedsängerin.** Ausgebildete Mezzosopranistin um sechzig, volle Stimme, schlicht vorgetragen. | Flügel wie im Kunstlied | 82 %: Die Erkennung hört dreimal «er/sie» statt «dir» und «Willekraft» statt «Glieder Kraft» (0:58) — die Stimme verschleift Konsonanten. |
| 16 | **Der Bass.** Sehr tiefer Bass, Mönchsgesang über einem Bordun aus Männerstimmen. | a cappella | 88 %. |
| 17 | **Die Jazzsängerin.** Rauchig, um fünfundfünfzig, dunkel, singt hinter dem Beat. | Klaviertrio, Besen | 79 %: «wird» als «wir» (dreimal), sonst Komposita. |
| 18 | **Der Kantor.** Alter, dünner heller Tenor, Melismen über der Shrutibox. | Shrutibox | 86 %: «der» als «dir». |
| 19 | **Der Countertenor.** Reif, rein, leicht körnig. | Gambe, Theorbe | 95 %. |
| 20 | **Die Volkssängerin.** Älter, ungeschult, nasal, mit dem Rufklang nordischer Hirtenlieder. | eine Fiedel | 83 %: «wird» als «wir». |
| 21 | **Die Schauspielerin.** Um fünfundsechzig, nur gesprochen, trocken und genau. | Klangschalen, Geige | 91 %, aber bei 0:27 eine erfundene Zeile zwischen den Strophen — nachhören. |
| 22 | **Der Kabarettist.** Trockener Bariton der zwanziger Jahre, spricht-singt mit Biss, leicht ironisch. | Klavier, gedämpfte Trompete, Klarinette | 85 %: «der Weisheit» als «dir weit» (0:28). |

Zusammen 14,7 Minuten, rund 13 000 Credits. Alle auf −16 LUFS.

**Was die Rückschrift hier heisst:** Bei allen zehn fällt «Denkens-Wollens
/ Wollens-Denkens keimerweckend» auseinander; das ist die Zeile, nicht die
Stimme. Niedrige Werte (15, 17, 20) zeigen eher, dass die Stimme Charakter
hat (verschleift, nuschelt, ruft) als dass sie den Text verfehlt. Ob der
Charakter trägt, hört Philipp.

## Die Figuren-Studien (Runde 4)

Rückmeldung auf Runde 2 und 3 (9. 10. 2026), gekürzt: Gesang, nicht
Sprechen (Sprechen höchstens als I-Tüpfel). Nähe und tonale Objektivität.
Kein Pathos, keine Sentimentalität. Gefühle aus den Grenzen des Erlebens,
nicht aus Vertrautheit und Wiederholung: «Wacher werden ins Konkrete.»
Gefällig und einladend bis zu einem Grad, dann die Wachheit steigernd.
Berührt haben 2 (Litanei), 9 (Favorit: minimal, Stimme ohne Effekte,
hingegeben an Rhythmus, Melodie und Text — es fehlen Pausen für den Sinn),
11 (Harmonien der Stimmen), 17 (die Jazzerin; etwas weniger Klischee).
Verworfen: 1, 3 (Chöre bleiben den Engeln der späteren Stunden
vorbehalten), 4, 5, 6 (sentimental), 7 (kitschig), 8, 12. Vorbilder: Pärt,
Rosalía, Einaudi (innerlich gesteigerte Räume), Bach, Mine (Stimme und
Persona als Instrument, dienend), Björk (aus anderen Welten).

**Drei Figurenarten:** der Hüter (differenziert als Weltenwort,
Geistesbote …; erkennbar durch den ganzen Zyklus, eine grosse Seele in der
Stimme — die Jazzerin ohne Klischee), der Mensch (in Nuancen, Rollen und
Gesten), die Engel und Götter (neun Sphärengruppen; aus anderen Welten).
Immer aus dem Sinn schöpfen. Die Studien sind kürzer (40 bis 80 s) und
kommen aus dem ganzen Korpus, nicht nur aus den Stunden 1–7.

| Nr | Figur · Text | Ansatz | Nachhören |
|---|---|---|---|
| 23 | Hüter · Erste Tafel «O Mensch, erkenne dich selbst» | **Tintinnabuli:** Stimme schrittweise, Bratsche nur auf dem Dreiklang, eine Glocke, Klavier in Einzeltönen; Pause nach jeder Zeile. | 92 %. |
| 24 | Hüter · 1.4 «Doch du musst den Abgrund achten» | **Suite:** ein Solocello wie eine Sarabande, die Stimme im Kontrapunkt, sonst nichts. | 89 %. |
| 25 | Hüter · 1.4 «Schau das erste Tier» | **Zuwendung:** Klavier-Ostinato, das den inneren Raum weitet; die Beschreibung des Tiers aus geduldigem, liebevollem Interesse statt aus Gefühl. | 93 %; «deine Furcht» bei 0:22 als «eine» gehört. |
| 26 | Hüter · 9.1 «O Mensch, ertaste …» | **Ruf:** jeder Ruf «O Mensch» anders verziert (Melisma), sparsame Palmas, sauberer Subbass, sonst leer. | 95 %. |
| 27 | Hüter und Mensch · 14.1 «Wo ist der Erde Festigkeit» | **Drei Antworten in einer Stimme:** christlich schlicht und offen, luziferisch hoch, verziert, zu schön (Glasharmonika), ahrimanisch tief, geklippt, hämmernd (col legno). | 96 %. |
| 28 | Mensch · Dritte Tafel «Ich trat in diese Sinnes-Welt» | **Choral:** vierstimmige Choralharmonik am Klavier, ein Akkord je Zeile, die Stimme obenauf, silbisch. | 93 % (zweiter Lauf; der erste sang den Text falsch, 58 %). |
| 29 | Hüter und Ich · 16.2 «Hat verstanden dein Geist?» | **Zwiegespräch:** der Hüter fragt über Harmonium und Cello (der Klang aus 2), das Ich antwortet über sparsamen Klavierakkorden. | 100 %. |
| 30 | Hüter und Engel · 15.1 «Empfinde, wie wir empfinden» | **Andere Welt:** Angeloi, Archangeloi, Archai in einer einzigen hohen Stimme mit mikrotonalem Schimmer, jede Hierarchie eine Stufe höher; Glasharmonika, gestrichene Crotales. Kein Chor. | 95 %. |
| 31 | Mensch · 19+ «Mein Ich ist IHR» | **Strahlend:** Klavier und Streicher schwellen langsam, sakral ohne Pathos, die letzte Zeile lang gehalten. | 85 %; im Nachspiel ein erfundenes «Herr» (0:42). |

Zusammen 7,9 Minuten, rund 7 900 Credits samt einer Wiederholung (28).
Alle auf −16 LUFS.

### Credits sparen

- **Kürzer.** Eine Minute kostet 900 Credits, egal was darin ist. Die
  Studien dieser Runde haben 3 s Vorspiel und 4 s Nachspiel statt 10 und
  12; das allein sparte je Stück ein Viertel.
- **Speichern und weitertragen.** Seit Runde 4 wird jedes Stück bei
  ElevenLabs gespeichert (`store_for_inpainting`), die `song_id` liegt im
  Cache neben dem Plan. Eine gelungene Passage von höchstens 30 s wird
  damit zur **Referenz** für neue Stücke (`conditioning_ref` im ersten
  Abschnitt, `ref` im Eintrag): Stimme und Klang wandern mit, statt neu
  gewürfelt zu werden. Das spart die Wiederholungen, die bisher jede dritte
  Runde kosteten — und macht den Hüter über den Zyklus erkennbar.
- **Ausbessern statt neu bauen.** Ein gespeichertes Stück lässt sich
  abschnittweise ändern (Inpainting): die gebliebenen Teile werden als
  Audio-Referenz eingesetzt, nur der geänderte Abschnitt wird neu erzeugt.
  Noch nicht gebaut; der Weg ist derselbe Endpunkt.
- **Nicht wiederholen, was die Prüfung bestätigt.** Scribe kostet fast
  nichts und sagt, ob die Worte da sind; neu erzeugt wird nur bei
  erfundenem Text (bisher 4, 5, 28).
- **Credit-Stand:** der Schlüssel darf ihn nicht lesen. Ein Credit-Limit
  je Schlüssel setzt Philipp unter
  <https://elevenlabs.io/app/developers/api-keys>.

## Die Doppelstimme (Runde 5)

Rückmeldung auf Runde 4 (9. 10. 2026), gekürzt: 26 ein eigenartiger
Treffer, Text mit Stimmung. 23–25 irrelevant: keine romantischen,
maskulinen Arien. 27 trifft, schönes Liedset — die Stimmen und Rollen in
Frage und Antwort herausarbeiten. 29 hat Seele, aber die Rollen fehlen:
zwei sprechen miteinander, existenzielle Begegnung. 30 sehr gut, das
Zusammenklingen ist eine grosse Spur; weniger Effekt, mehr Akustik. 31
schön, passt nicht: klassischer sakraler Gesang mit Kirchenhall weckt
falsche Assoziationen; die letzte Szene erzählt vom neuen Menschen, der aus
den innersten Erlebnissen geboren heraustritt zu neuen Taten. **Idee:** der
Hüter weiblich, als Doppelstimme, immer ineinanderklingend, die Dominanz
leicht nach Inhalt wechselnd.

| Nr | Figur · Text | Ansatz | Nachhören |
|---|---|---|---|
| 32 | Hüter · 7.1 «O schau die Drei» | **Doppelstimme:** Alt und Mezzo immer zusammen, ineinander, die Führung wechselt mit dem Sinn; nur eine gehaltene Bratsche, keine Effekte. | 98 %. |
| 33 | Hüter und erste Hierarchie · 15.3 «Was wird aus der Lüfte Reizgewalt» | Die Doppelstimme fragt; Throne, Cherubine, Seraphine antworten in einer einzigen hohen Stimme, jede eine Stufe höher, fremd durch Reinheit und Intervalle, nicht durch Effekt; Flageoletts einer Geige. | «Gottes-Welten-Leben» klingt bei 0:28 wie «-Licht»; am Ende ein erfundenes «Geh». |
| 34 | Hüter und Ich · 16.2 «Hat verstanden dein Geist?» | **Begegnung mit Rollen:** die Doppelstimme fragt über Cello und Bratsche, das Ich antwortet allein, eine einzige schlichte Stimme über je einem tiefen Klavierton. | 98 %. |

Zusammen 2,9 Minuten, rund 2 600 Credits. Alle auf −16 LUFS.

**Für 19+ («Mein Ich ist IHR») gilt seither:** kein Kirchenhall, kein
klassisch-sakraler Ton. Die Szene ist ein Heraustreten: wach, hell,
rhythmisch, nach aussen gewandt, mit neuen Verbindungen in die
Götterwelten — noch nicht gebaut.

## Der Dialog (Runde 6)

Rückmeldung auf Runde 5 (9. 10. 2026): «Deutscher Gospel? Komm bitte aus
der Kirche raus. Lieber skandinavische Landschaften. Das Ineinander-Duo
dachte ich zweigeschlechtlich. Kein Fallenlassen in eine Melodie. Alles
gestalten, wach werden lassen von innen. Langsam überraschen. Dehnen.
Wecken. Halten. Konzentration. Die Einzelstimme des Menschen fehlt. Wurde
auch gechort. Realisiere zuerst die Situation und gewinne von da die
stimmigen Stilmittel. „Hat verstanden dein …" ist eine intime
Höhepunktsituation: Der Hüter verabschiedet sich, übergibt seine Rolle dem
Menschen. Er fragt tastend, der Mensch antwortet aus seiner erwachenden
inneren Stimme. Gekrönt und gezeptert wie der Prinz im Märchen. Weniger
lustiges Jubilieren. Die Hallelujas an den richtigen Stellen!»

**Die Situation, aus der die Mittel kommen (16.2):** Der Hüter tritt
zurück. Drei Fragen, jede leiser, jede ein Loslassen; das Duo aus Frau und
Mann immer zusammen, die Führung wechselt (erst sie, dann gleich, dann
er). Der Mensch antwortet allein, eine einzige Stimme, nie verdoppelt: Sie
beginnt fast ohne Ton, wie inneres Sprechen, das zu Klang wird, und gewinnt
Zeile um Zeile Ton. Keine Melodie, in die man fällt; jede Zeile eine
Gestalt, gedehnt, gehalten. **Einmal** klingen die Harmonien hörbar: Bei
«Mögen klingend schaffen mein Ich» tritt die Kantele ein und die beiden
Hüterstimmen klingen für einen Moment mit dem Menschen, dann ziehen sie
sich zurück. Die dritte Antwort steht: ein sehr leiser Rahmentrommel-Puls,
die Fiedel, die Stimme aufrecht, ruhige Autorität ohne Triumph, die letzte
Zeile gehalten und in die Stille entlassen. Klangraum: Fiedel mit
Bordunsaiten, Kantele, trockene Holzstube im Norden. Gegen-Stile: Gospel,
Chor, Orgel, Kathedralenhall, Jubel, Halleluja, Popballade.

| Nr | Mensch | Nachhören |
|---|---|---|
| 35 | junger Mann, leichte schlichte Stimme | Rückschrift 100 %. |
| 36 | junge Frau, gleicher Plan | **nicht erzeugt: Credits aufgebraucht** (siehe unten). |

### Credits: Stand 9. 10. 2026, Abend

Das Konto hat ein Kontingent von 122 129 Credits; nach Vorlage 35 blieben
284. Vorlage 36 (82 s) hätte 1 128 gebraucht — die API meldet
`quota_exceeded` und sagt den Bedarf genau. **Gemessen:** 82 Sekunden
kosten 1 128 Credits, also rund 825 je Minute (nicht 900). Weiter geht es,
wenn das Kontingent erneuert ist: <https://elevenlabs.io/app/subscription>.
Dann: `XI_KEY=… python3 -I docs/vertonung/vertonen.py bauen 36`.

Verbrauch des Tages, gerundet: Erstfassung 22 000, Vorlagen 24 000,
Stimmenprobe 13 000, Figuren 7 900, Doppelstimme 2 600, Dialog 1 100 —
rund 71 000 Credits für 76 Minuten Musik. Was gelernt wurde, steht in den
Rückmeldungen oben; die Richtung ist seit Runde 6 klar genug, dass die
nächsten Stücke keine Stilproben mehr sein müssen.

## Der Dialog als Montage (Runde 7)

Rückmeldung auf 35 (9. 10. 2026): «Eine Stimme nur? Wo ist die Harmonie
der Doppelstimme? Warum hat der Mensch dieselbe Stimme wie der Hüter?
Frage jagt Antwort als wäre es ein Satz … Klare Grundelemente und
Gliederung bitte! Und keine hoppelnde Melodie. Es geht um diesen intimen,
inneren Vorgang, ein Gewahrwerden, kein Volkstänzchen, eher ein Erwachen in
eine neue, höhere Wirklichkeit.»

**Die Ursache liegt im Werkzeug:** Eleven Music hält innerhalb eines
Stücks keine zwei Stimmen auseinander. Was in verschiedenen Abschnitten
als Duo und als Einzelstimme beschrieben ist, mittelt es zu einem Sänger,
und es lässt zwischen den Abschnitten keine Stille — Frage und Antwort
kleben aneinander. Darum ist 35 so geworden, wie es wurde, und darum geht
es so nicht weiter.

**Darum seit Runde 7 die Montage** (`montage` im Eintrag, `montieren()`):
Jede Rolle wird als **eigenes Stück** erzeugt, beide über demselben
Grundton, mit exakt vorgegebenen Abschnittsdauern (bei `music_v2_5`
verbindlich, also schneidbar). Erst danach werden die Abschnitte in der
Folge des Dialogs zusammengesetzt, mit **echter Stille** dazwischen und
ohne jeden Zusatz; der Master ist derselbe wie bisher. Die Stille kostet
nichts; Vorlage 37 braucht 88 Sekunden Musik für 105 Sekunden Stück.

Die Grundelemente der 37, aus der Situation (der Hüter übergibt, der
Mensch erwacht):

1. **Der Bordun** auf D, ein Cello, in beiden Liedern. Der Boden.
2. **Das Duo**, Frau und Mann, gehaltene Töne in Quinte oder Terz, beide
   jederzeit hörbar, die Frage endet offen und steigt leicht. Erst sie etwas
   stärker, dann gleich, dann er.
3. **Die Einzelstimme**, eine junge Frau, nie verdoppelt: Sie beginnt fast
   auf einem Ton, wie inneres Sprechen, das zu Klang wird; schrittweise,
   gehaltene Töne, keine Sprünge, kein Puls, kein Schmuck.
4. **Die Stille**: 2,5 s nach jeder Frage, 3 s nach jeder Antwort. Dort
   geschieht das Gewahrwerden.
5. **Eine Blüte**: bei «Mögen klingend schaffen mein Ich» ein einziger
   Kantele-Akkord, die Stimme öffnet sich ein wenig, dann wieder still.
   Die dritte Antwort heller, offener, der Bordun öffnet sich zur Quinte;
   aufrecht, wach, ohne Triumph; die letzte Zeile lang in die Stille.

| Nr | Stand |
|---|---|
| 37 | **Erzeugt** (9. 10. 2026, nach Erneuerung der Credits): zwei Lieder, 32 s Hüter und 56 s Mensch, montiert zu 1:45. Rückschrift 98 % («klingend» als «klingt» gehört). −16,2 LUFS. Kosten rund 1 200 Credits. |

```sh
XI_KEY=… python3 -I docs/vertonung/vertonen.py bauen 37      # beide Lieder (Cache), dann Montage und Master
XI_KEY=… python3 -I docs/vertonung/vertonen.py pruefen 37    # Rückschrift in der Folge des Dialogs
```

**Was die Montage noch nicht kann:** Ob Duo und Einzelstimme so klingen,
wie beschrieben, entscheidet weiter das Modell je Lied; die Montage
garantiert nur, dass sie **verschiedene** Stimmen sind und dass zwischen
Frage und Antwort Stille steht. Gefällt eine Rolle, wird ihr Lied zur
Referenz (`ref`) für alle weiteren Dialoge.

## Der Dialog, zweiter Schnitt (Runde 8)

Rückmeldung auf 37 (9. 10. 2026): «Es hubbelt. Die Schnitte sind nicht
sauber und der Rhythmus hält nicht. Wieder eine Sprecherin statt einer
Sängerin, im Delirium. Nicht deutlich, ob sie nicht auch den Hüter
mitgesungen hat. Der Gesamtminimalismus und die klare Gliederung sind
stimmige Stilmittel. Der innere Ton ist noch nicht ganz da.»

Drei Ursachen, drei Mittel:

| Fehler | Ursache | Mittel in 38 |
|---|---|---|
| Hubbeln | geschnitten an Abschnittsgrenzen, wo die Stimme noch ausklingt | Jedes Lied hat zwischen den Gesangsteilen 3-s-Abschnitte «nur Bordun»; geschnitten wird in deren Mitte, mit 0,4 s und 0,6 s Blende. Darunter ein durchgehendes **Bordun-Bett** (eigenes 30-s-Lied, geschleift, −9 dB), das die Nähte trägt und in der Stille den Boden hält. |
| Sprecherin im Delirium | selbst bestellt: «beginnt fast ohne Ton, wie inneres Sprechen» | «sung clearly, cantabile, pure tone, simple sustained notes»; Sprech-, Hauch- und Flüsterwörter in den Gegen-Stilen. |
| Hüter nicht vom Menschen zu unterscheiden | das Duo aus Frau und Mann ist das eine Mittel, das Eleven Music nicht verlässlich liefert | Der Hüter eine **einzige tiefe Männerstimme** (Bass-Bariton), der Mensch eine **Frauenstimme** (Mezzo). Die Doppelstimme bleibt als Idee notiert, bis das Werkzeug sie kann. |

Geblieben: Bordun auf D, Stille zwischen Frage und Antwort (1 s nach der
Frage, 1,5 s nach der Antwort, dazu je 1,5 s Bordun aus den Schnitträndern),
eine Kantele-Blüte bei «Mögen klingend schaffen mein Ich», die dritte
Antwort heller und aufrecht.

| Nr | Stand |
|---|---|
| 38 | Erzeugt: Bett 30 s, Hüter 40 s, Mensch 69 s, montiert zu 1:55. Rückschrift 98 %. −16,2 LUFS. Rund 1 900 Credits. |

## Was mit ElevenLabs möglich ist (Stand 9. 10. 2026)

- **Gesang mit vorgegebenem Text.** Eleven Music singt Liedtext in jeder
  Sprache, Deutsch eingeschlossen; die Stilangaben müssen englisch sein.
  Die Rückschrift mit Scribe trifft 83 bis 100 % der Wörter (Tabelle
  oben); fast alle Abweichungen sind Schreibweisen der Erkennung
  («Selbstheit Sein», «Geisteslichtgewalt»).
- **Kompositionsplan statt Prompt.** Ein Stück ist eine Folge von bis zu 30
  Abschnitten, jeder 3 bis 120 Sekunden, jeder mit eigenem Text, eigenen
  Stilen und Gegen-Stilen; gesamt bis 10 Minuten. Damit lässt sich die
  Strophenform der Mantren (drei Strophen Denken–Fühlen–Wollen, der Hüter
  mit drei Tieren) als Form der Musik abbilden: jede Strophe ein Abschnitt
  mit eigenem Klang.
- **Regie im Text.** Abschnittsnamen in eckigen Klammern, Anweisungen in
  geschweiften (`{spoken}`), Laute in runden (`(ooh)`). Die Erkennung hat
  keine Anweisung mitgesungen gehört. **Gesprochener Text** über Musik
  geht (Vorlagen 1, 4, 5, 11): das ist die Bardo-Form.
- **Keine Künstlernamen.** Die API weist Prompts mit Namen ab
  (`bad_prompt`). Jede Inspiration ist darum als Klangbeschreibung
  übersetzt (unten).
- **Nicht steuerbar:** die Stimme selbst (es gibt keine Stimm-ID wie beim
  Vorlesen; «female alto, breathy, close» ist eine Bitte, keine Wahl —
  seit Runde 4 aber **übertragbar**: eine gespeicherte Passage als Referenz,
  § Credits sparen), die Melodie, und die Lautheit (die Stücke kamen zwischen −17 und −31 LUFS
  aus dem Modell — der Master gleicht das aus). Eine Zeile ändern heisst
  das ganze Stück neu erzeugen; der Cache hilft nur bei unverändertem Plan.
- **Preis:** 900 Credits je Minute Musik. Die Erstfassung (24,6 min) kostete
  rund 22 000 Credits, die zwölf Vorlagen samt zwei Wiederholungen rund
  24 000, die Stimmenprobe rund 13 000, die Figuren-Studien rund 7 900,
  die Doppelstimme rund 2 600; die Prüfläufe mit Scribe dazu wenig. Der
  Schlüssel darf den Zähler nicht lesen (`guthaben` meldet 401 ohne das
  Recht «User: Read»); der Stand steht im Konto:
  <https://elevenlabs.io/app/subscription>.
- **Lizenz:** Die Music Terms von ElevenLabs schliessen «religious
  organizations or institutions» aus (siehe `../feature/README.md`
  § Vor einer Veröffentlichung). Für die Werkstatt unerheblich; bevor eine
  anthroposophische Institution die Stücke sendet, ist das zu klären.

## Erstfassung (9. 10. 2026, zurückgebaut)

Sieben Stücke nach Stunden, 24,6 Minuten, als Klammer Arie – fünf
Variationen – Arie da capo, mit einer Hauch-Altstimme als Hüter. Die
Rückmeldung steht oben; geblieben ist der Ansatz der Stunde 6 (Vorlagen 9
und 10). Die Pläne der Erstfassung stehen in der Git-Geschichte (Commit
«Vertonung «Nach innen»: Stunden 1–7»), die Stücke im Cache `clips/`.

## Dateien

| Datei | Inhalt |
|---|---|
| `vertonen.py` | die Vorlagen (Abschnitte, Dauern, Stile), Erzeugung, Master, Prüfung |
| `clips/` | Cache: rohe MP3 und Plan je Vorlage (nicht im Repo) |
| `ausgabe/vorlage-<nr>-<name>.mp3` | die gemasterten Vorlagen mit Titel und Albumtag (nicht im Repo) |

## Neu bauen

Den Schlüssel `elevenlabs` aus dem Schlüsselbund holen und nur als
Umgebungsvariable des einzelnen Befehls übergeben. Er darf nie in eine
Datei. Er braucht die Rechte «Music» und für die Prüfung «Speech to Text».

```sh
python3 -I docs/vertonung/vertonen.py plan 3                   # Plan der Vorlage 3 ansehen, kostet nichts
XI_KEY=… python3 -I docs/vertonung/vertonen.py bauen 1 2 3     # erzeugen (Cache), mastern nach ausgabe/
XI_KEY=… python3 -I docs/vertonung/vertonen.py pruefen 1 2 3   # Scribe schreibt zurück, Vergleich mit dem Text
python3 -I docs/vertonung/vertonen.py bauen                    # alle zwölf aus dem Cache mastern, kostet nichts
```

Ein geänderter Plan erzeugt die Vorlage neu (900 Credits je Minute). Ein
unveränderter Plan kommt aus dem Cache. **Eine neue Vorlage** ist ein
Eintrag in `VORLAGEN` in `vertonen.py`: Sinneinheit, Ansatz in einem Satz,
Abschnitte mit Quelle (Mantram-ID, Teil), Dauer, Stilen.

## Technik

- `POST /v1/music` mit `composition_plan` (Chunks: `text`, `duration_ms`,
  `positive_styles`, `negative_styles`, `context_adherence: high`),
  `model_id: music_v2_5`, Ausgabe `mp3_44100_192`.
- Stile je Abschnitt: Stimme der Vorlage und Haltung («the singer serves
  the text and does not emote», «no vibrato») nur wo Text ist, dazu die
  Instrumente des Abschnitts, «real acoustic instruments recorded in a real
  room», «complex, slowly shifting harmony», Tonart und Tempo. Gegen-Stile:
  billige Synth-Flächen, New Age, Hall-Soße, Rock-Schlagzeug, Rap, Autotune,
  Trailer-Pathos, Theatralik, Hauch-Flüstern, englischer Text; Abschnitte
  ohne Text zusätzlich «vocals».
- Gesprochene Abschnitte tragen `{spoken}` im Text und «spoken, not sung»
  in den Stilen; das Modell hält sich daran (Vorlagen 1, 4, 5, 11).
- Master: `loudnorm` in zwei Durchgängen auf −16 LUFS, −1,5 dBTP,
  linear (keine Verdichtung — die Stille bleibt Stille), MP3 192 kbit/s.
- Prüfung: Scribe (`scribe_v1`, `deu`, Wortmarken) gegen den Liedtext,
  Wort für Wort wie bei den Features (`../feature/pruefen.py`).

## Offen

- Philipps Urteil über 38: Sitzen die Schnitte, sind es zwei Sängerinnen
  bzw. Sänger, ist der innere Ton näher? Dann wird das Hüter-Lied der 38
  zur Referenz und alle Dialoge (12, 14, 15, 16, 17, 18, 19) folgen dem
  Muster; danach die Sinneinheiten der Stunden 1–7 mit Rollen aus dem Sinn.
  Vorlage 36 ist durch 37 und 38 überholt.
- 19+ neu denken: Heraustreten statt Kirche.
- Eine Hörseite im Werk (`src/pages/werkstatt/`), sobald die Stücke
  irgendwo liegen dürfen, wo die Site sie laden kann.
