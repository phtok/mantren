# «Nach innen» — Vertonung der Mantren, Stunden 1–7

*Werkstatt · Liederzyklus · Erstfassung 9. 10. 2026*

Auftrag: «Ich wünsche mir eine musikalische Vertonung der Mantren. Beginne
mit 1–7. Inspiration? Arvo Pärt, Ludovico Einaudi, Mine, Bon Iver, Goldberg
Variationen, Francis and the Lights, Rosalía, Brian Eno, Pascal Schumacher,
Billie Eilish, Radiohead. Was ist mit Elevenlabs möglich? Nach Innen.»

Sieben Stücke, eines je Stunde, 24 Minuten. Der Text ist Wort für Wort die
Lesefassung 2024 aus `src/data/mantren.yaml`; nichts ist gekürzt, nichts
umgestellt. Die Musik erzeugt **Eleven Music** (`music_v2_5`) nach einem
Kompositionsplan je Stück, den `vertonen.py` aus den Mantren baut. Die
Audiodateien liegen nicht im Repo (35 MB); sie lassen sich aus diesen
Dateien neu bauen, siehe unten.

## Was mit ElevenLabs möglich ist (Stand 9. 10. 2026)

- **Gesang mit vorgegebenem Text.** Eleven Music singt Liedtext in jeder
  Sprache, Deutsch eingeschlossen; die Stilangaben müssen englisch sein.
  Die Rückschrift mit Scribe trifft 82 bis 98 % der Wörter (Tabelle
  unten); fast alle Abweichungen sind Schreibweisen der Erkennung
  («Selbstheit Sein», «Geisteslichtgewalt»).
- **Kompositionsplan statt Prompt.** Ein Stück ist eine Folge von bis zu 30
  Abschnitten, jeder 3 bis 120 Sekunden, jeder mit eigenem Text, eigenen
  Stilen und Gegen-Stilen; gesamt bis 10 Minuten. Damit lässt sich die
  Strophenform der Mantren (drei Strophen Denken–Fühlen–Wollen, der Hüter
  mit drei Tieren) als Form der Musik abbilden: jede Strophe ein Abschnitt
  mit eigenem Klang.
- **Regie im Text.** Abschnittsnamen in eckigen Klammern, Anweisungen in
  geschweiften (`{whispered}`), Laute in runden (`(ooh)`). Die Erkennung
  hat keine Anweisung mitgesungen gehört.
- **Keine Künstlernamen.** Die API weist Prompts mit Namen ab
  (`bad_prompt`). Jede Inspiration ist darum als Klangbeschreibung
  übersetzt (unten).
- **Nicht steuerbar:** die Stimme selbst (es gibt keine Stimm-ID wie beim
  Vorlesen; «female alto, breathy, close» ist eine Bitte, keine Wahl), die
  Melodie, und die Lautheit (die Stücke kamen zwischen −17 und −31 LUFS
  aus dem Modell — der Master gleicht das aus). Eine Zeile ändern heisst
  das ganze Stück neu erzeugen; der Cache hilft nur bei unverändertem Plan.
- **Preis:** 900 Credits je Minute Musik. Der Zyklus (24,6 min) kostete
  rund 22 000 Credits, die sieben Prüfläufe mit Scribe dazu wenig. Der
  Schlüssel darf den Zähler nicht lesen (`guthaben` meldet 401 ohne das
  Recht «User: Read»); der Stand steht im Konto:
  <https://elevenlabs.io/app/subscription>.
- **Lizenz:** Die Music Terms von ElevenLabs schliessen «religious
  organizations or institutions» aus (siehe `../feature/README.md`
  § Vor einer Veröffentlichung). Für die Werkstatt unerheblich; bevor eine
  anthroposophische Institution die Stücke sendet, ist das zu klären.

## Die Form: Arie, Variationen, Arie

Der Zyklus borgt sich von den Goldberg-Variationen die Klammer: Stunde 1
ist die Arie, Stunde 7 die Arie da capo — dasselbe Klavier-Arpeggio,
dieselbe Tintinnabuli-Fläche, d-Moll am Anfang, D-Dur am Ende. Dazwischen
fünf Stunden, jede in einer eigenen Klangwelt, weil der Hüter in jeder
Stunde anders spricht.

| Stunde | Stück | Klangwelt (Inspiration, als Beschreibung) | Dauer |
|---|---|---|---|
| 1 | **Erdengründe** (1.1–1.4) | Filzklavier und Tintinnabuli (Einaudi, Pärt); die Altstimme nah, fast gesprochen (Eilish). «Sieh, ich bin der Erkenntnis einzig Tor» gesprochen über einer Klaviernote. Die drei Tiere mit verstimmten Streichern und Glitches (Radiohead), jedes in seiner Farbe: stumpfblau pizzicato, gelbgrau gedämpftes Blech, schmutzigrot gläserne Flageoletts. «Flügel» kippt nach D-Dur mit geschichteten Stimmen (Bon Iver). | 6,7 min |
| 2 | **Die drei Tiere** (2) | Ambient-Drone ohne Puls (Eno), Subbass, die Stimme geflüstert (Eilish). Drei Strophen, jede eine Lage tiefer: Denken, Fühlen, Wollen. Die letzte Zeile wird gesungen. | 2,6 min |
| 3 | **Willens-Stoß** (3) | Vibraphon-Muster und Bassklarinette (Schumacher), 84 bpm. Strophe 1 Vibraphon allein, Strophe 2 Puls, Strophe 3 der Chor aus einer Stimme (Francis and the Lights) auf «Weltschöpfermacht im Geistes-Ich». | 2,5 min |
| 4 | **Tiefe – Weite – Höhe** (4) | Eine Männerstimme in drei Lagen: Bruststimme über Cello und Kontrabass (Erdentiefen), Mittellage über Streichquartett (Weltenweiten), Falsett in Schichten mit Vocoder-Farbe (Himmelshöhen; Bon Iver). e-Moll nach E-Dur. | 2,6 min |
| 5 | **Es kämpft** (5) | Phrygisch, Nylongitarre, sparsame Palmas, Melismen (Rosalía), moderner Subbass. Jede Strophe ein Kampf; die letzten zwei Zeilen jeder Strophe a cappella. | 2,5 min |
| 6 | **Erdenwerte** (6) | Sechs Variationen über einen festen Bass in langsamem Dreiertakt (Goldberg). Erde, Wasser, Luft: Klavier, dann Cello, dann Streicher. Dann die zweite Regie «wie wenn das Weltenwort selber ertönte»: Indie-Pop mit Streichern und leisem elektronischem Puls (Mine), der Chor trägt «Es lässt den Gott im Menschen walten». | 4,7 min |
| 7 | **Schau die Drei** (7.1–7.3) | Arie da capo in D-Dur, zwei Frauenstimmen im Kanon. Kopf, Herz, Glieder je ein kurzer Abschnitt (Streicher, Klavier, beides). Stille. «Tritt ein» erst geflüstert, dann einmal voll gesungen; das Arpeggio löst sich in eine Drone (Eno) und verklingt. | 3,1 min |

**Die Stimme des Hüters ist eine Altstimme.** Die Mantren sagen «der Hüter
spricht», aber der Hüter ist kein Mann, und der Auftrag nennt drei
Sängerinnen. Nur Stunde 4 ist eine Männerstimme, weil der Weg von der
Tiefe in die Höhe dort mit einer Stimme durch drei Lagen geht. Eleven Music
vergibt keine Stimm-IDs; dieselbe Beschreibung ergibt in jedem Stück eine
ähnliche, nicht dieselbe Stimme.

## Dateien

| Datei | Inhalt |
|---|---|
| `vertonen.py` | die sieben Pläne (Abschnitte, Dauern, Stile), Erzeugung, Master, Prüfung |
| `clips/` | Cache: rohe MP3 und Plan je Stück (nicht im Repo) |
| `ausgabe/nach-innen-<n>.mp3` | die gemasterten Stücke mit Titel und Albumtag (nicht im Repo) |

## Neu bauen

Den Schlüssel `elevenlabs` aus dem Schlüsselbund holen und nur als
Umgebungsvariable des einzelnen Befehls übergeben. Er darf nie in eine
Datei. Er braucht die Rechte «Music» und für die Prüfung «Speech to Text».

```sh
python3 -I docs/vertonung/vertonen.py plan 3                   # Plan der Stunde 3 ansehen, kostet nichts
XI_KEY=… python3 -I docs/vertonung/vertonen.py bauen 1 2 3     # erzeugen (Cache), mastern nach ausgabe/
XI_KEY=… python3 -I docs/vertonung/vertonen.py pruefen 1 2 3   # Scribe schreibt zurück, Vergleich mit dem Text
python3 -I docs/vertonung/vertonen.py bauen                    # alle sieben aus dem Cache mastern, kostet nichts
```

Ein geänderter Plan erzeugt das Stück neu (900 Credits je Minute). Ein
unveränderter Plan kommt aus dem Cache.

## Technik

- `POST /v1/music` mit `composition_plan` (Chunks: `text`, `duration_ms`,
  `positive_styles`, `negative_styles`, `context_adherence: high`),
  `model_id: music_v2_5`, Ausgabe `mp3_44100_192`.
- Stile je Abschnitt: Stimme (nur wo Text ist) + Klangwelt des Abschnitts +
  Grundton des Zyklus («sacred minimalism», «silence is part of the
  music») + Tonart und Tempo des Stücks. Gegen-Stile: Schlagzeug, Rap,
  Autotune, Trailer-Pathos, englischer Text; Abschnitte ohne Text
  zusätzlich «vocals».
- Master: `loudnorm` in zwei Durchgängen auf −16 LUFS, −1,5 dBTP,
  linear (keine Verdichtung — die Stille bleibt Stille), MP3 192 kbit/s.
- Prüfung: Scribe (`scribe_v1`, `deu`, Wortmarken) gegen den Liedtext,
  Wort für Wort wie bei den Features (`../feature/pruefen.py`).

## Prüfung der Erstfassung (9. 10. 2026)

| Stunde | Wörter | Übereinstimmung | Wirkliche Abweichungen |
|---|---|---|---|
| 1 | 379 | 97,5 % | keine (nur Schreibweisen: «Geist Gedanken», «Schlaf» für «schlaff») |
| 2 | 98 | 93,9 % | keine |
| 3 | 98 | 81,6 % | «dem» als «im» (01:07); der Rest sind getrennt geschriebene Komposita |
| 4 | 94 | 96,3 % | keine; das «(ooh)» des Nachspiels wird als «Huh» erkannt |
| 5 | 112 | 96,4 % | «in» als «im» (00:21) |
| 6 | 201 | 90,2 % | «wandeln» als «andämmern» (00:49) — nachhören |
| 7 | 113 | 93,9 % | «Menschenstreben» als «schön Streben» (02:07) — nachhören |

Lautheit nach dem Master: alle sieben −16,2 bis −16,4 LUFS, Spitzen −1,6
bis −6,1 dBFS. Vor dem Master lagen sie zwischen −17 und −31 LUFS.

**Den Klang beurteilt Philipp.** Claude kann nicht hören; die Prüfung sagt
nur, dass die Worte da sind. Was zu beurteilen ist: ob die Altstimme als
Hüter trägt, ob die drei Tiere in Stunde 1 zu weit vom Zyklus wegführen,
ob Stunde 5 (Flamenco) und 6b (Indie-Pop) im Ganzen bestehen, und ob die
Stücke lieber eine Stimme teilen sollen (dann Stunde 4 anpassen).

## Offen

- Stunden 8–19 und die drei Tafeln (die Erste Tafel «O Mensch, erkenne dich
  selbst» könnte als Prolog vor Stunde 1 stehen: das Weltenwort, das in
  Stunde 1.3 als Daseinswort wiederkehrt).
- Eine Hörseite im Werk (`src/pages/werkstatt/`), sobald die Stücke
  irgendwo liegen dürfen, wo die Site sie laden kann (35 MB sind zu viel
  fürs Repo).
