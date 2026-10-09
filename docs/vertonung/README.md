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
  Vorlesen; «female alto, breathy, close» ist eine Bitte, keine Wahl), die
  Melodie, und die Lautheit (die Stücke kamen zwischen −17 und −31 LUFS
  aus dem Modell — der Master gleicht das aus). Eine Zeile ändern heisst
  das ganze Stück neu erzeugen; der Cache hilft nur bei unverändertem Plan.
- **Preis:** 900 Credits je Minute Musik. Die Erstfassung (24,6 min) kostete
  rund 22 000 Credits, die zwölf Vorlagen samt zwei Wiederholungen rund
  24 000; die Prüfläufe mit Scribe dazu wenig. Der
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

- Philipps Urteil über die zwölf Vorlagen: Welche haben Resonanz? Daraus
  wird die Regel für die übrigen Sinneinheiten der Stunden 1–7 (der
  Abgrund 1.4 Teil 1, Mantram 2, 7.2) und dann für 8–19 und die Tafeln.
- Eine Hörseite im Werk (`src/pages/werkstatt/`), sobald die Stücke
  irgendwo liegen dürfen, wo die Site sie laden kann.
