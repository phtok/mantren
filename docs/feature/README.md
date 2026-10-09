# Feature «Es ist an der Zeit»

*Werkstatt · Radio-Feature · Stand 2026-10-09*

Ein Radio-Feature von 20:50 Minuten nach der
[Studie zu Goethes Märchen und den Klassenmantren](../studie-goethe-maerchen.md).
Stilistisch richtet es sich nach den Feature-Formaten von Deutschlandfunk
Kultur und MDR Kultur. Die Erzählregeln stammen aus der Podcast-Reihe
«Gewachsen, nicht gebaut». Die Stimmen sind synthetisch (ElevenLabs).

Die Audiodatei liegt nicht im Repo, weil sie zu groß ist (25 MB). Sie lässt
sich aus diesen Dateien neu bauen, siehe unten.

## Dateien

| Datei | Inhalt |
|---|---|
| `manuskript.txt` | Regie-Liste, die Quelle für alles: `ROLLE\|Text`, `STILLE\|n s`, `MUSIK\|…`, `GERÄUSCH\|<Prompt>, n s` |
| `sendemanuskript.md` | dieselbe Fassung zum Lesen, mit Zeitmarken der Mischung vom 9. 10. 2026 |
| `produktion.py` | erzeugt Stimmen, Geräusche und Musik, mischt und mastert |

## Neu bauen

Den Schlüssel `elevenlabs` aus dem Schlüsselbund holen und nur als
Umgebungsvariable des einzelnen Befehls übergeben. Er darf nie in eine Datei.
Der Schlüssel braucht die Rechte «Text to Speech», «Sound Effects» und
«Music», für die Prüfung zusätzlich «Speech to Text».

```sh
XI_KEY=… python3 -I docs/feature/produktion.py stimmen     # Sprechzeilen (Cache: clips/)
XI_KEY=… python3 -I docs/feature/produktion.py klaenge     # Geräusche und Musik
python3 -I docs/feature/produktion.py mischen /tmp/es-ist-an-der-zeit.mp3
```

Alles Erzeugte wird nach Inhalt im Ordner `clips/` neben dem Skript
gecacht. Ein neues Mischen kostet nichts, eine geänderte Zeile kostet nur
diese Zeile. `clips/` gehört nicht ins Repo.

## Besetzung

| Rolle | Stimme (ElevenLabs) | warum |
|---|---|---|
| Erzählerin | NWR Erzählerin `nzC30P1U2LuQhAoEQcYi` | warm, ruhig; bekannt aus dem Podcast |
| Chronist | NWR Chronist `IcDVpTMW6YwgOc2vCZgG` | sachlich: Ansagen, Orte, Daten, Absage |
| Zitator Goethe | Märchen-Erzähler `hMURwqm1rkRSDLdNzQCM` | älterer Erzähler, langsam |
| Zitator Steiner | Christian Plasa `NBqeXKdZHweef6y0B67V` | neutral warm, keine Nachahmung |
| Stimme der Mantren | Märchen-Leise `6dD0VbyJ548lcuDpD5ew` | leise, fern, sehr ruhig |

Die Zitatoren lesen Zitate. Sie ahmen niemanden nach, und die Absage sagt
das.

## Regeln, die gelten

- **Leitsatz** «Es ist an der Zeit», wörtlich und in Stille, dazu im Titel
  und in der Absage. Im Märchen hört Lilie ihn dreimal; das Feature baut
  darauf.
- **Ein Gedanke pro Satz**, bis etwa 14 Wörter. Wiederholen statt
  variieren. Die Hörerin wird orientiert: drei Stationen, angesagt vom
  Chronisten.
- **Höhepunkt:** Musik aus, Stille, ein kurzer Satz, Stille, Wiederholung.
  Das sind «Kein einziges Mal», «Weisheit. Schein. Tugend. — Dieselben
  Worte» und «Mich aufzuopfern, ehe ich aufgeopfert werde».
- **Keine Musik unter Fakten.** Musik liegt nur unter Titel und Absage. Die
  Brücken stehen 7 s frei, Atmos laufen 23 dB unter der Sprache.
- **Zitate** stehen nur dort, wo sie in der Studie gegen die Quellen
  geprüft sind. Goethe folgt der Ausgabe letzter Hand mit modernisierter
  Schreibung, Steiner GA 22 und 28, die Mantren der Lesefassung 2024.
  Jahreszahlen stehen ausgeschrieben im Text.

## Technik

- `eleven_v4`, `language_code: de`. Es gibt keine `voice_settings`, und
  `speed` wirkt bei v4 nicht. Tempo entsteht nur über den Text, die Tags
  und echte Stille.
- **Neu gegenüber dem Podcast:** Jede Zeile wird in einem Stück gesprochen
  (`/with-timestamps`), damit der Satzbogen erhalten bleibt. `[Atem]`
  (0,55 s) und `[Pause]` (1,1 s) setzt der Mischer danach an die markierte
  Stelle, anhand der Zeitmarken je Zeichen. Der Podcast hatte an jeder
  Marke einen eigenen Aufruf gemacht; dabei brach die Satzmelodie.
- Regie-Tags auf Deutsch im Manuskript, ins Englische übersetzt
  (`ruhig` → `calm`, `leise` → `quietly`, `ohne die Stimme zu heben` →
  `without raising the voice` …).
- Pegel je Zeile −20 dBFS RMS, Zeilen mit `[leise …]` −22,5 dBFS. Lücke
  bei Sprecherwechsel 0,85 s, beim selben Sprecher 0,65 s.
- Master: `loudnorm` in zwei Durchgängen auf −16 LUFS, −1,5 dBTP, MP3
  160 kbit/s. Messung: −16,4 LUFS, LRA 6,7 LU, Spitze −1,8 dBFS.

## Prüfung (Claude kann nicht hören)

Die fertige Mischung wird mit ElevenLabs Scribe (`scribe_v1`)
zurückgeschrieben und Wort für Wort gegen das Manuskript verglichen. Ergebnis
der Endfassung: 98,5 % Übereinstimmung, keine mitgesprochenen Regie-Tags,
alle Jahreszahlen richtig. Die übrigen Abweichungen sind Schreibweisen der
Erkennung («Goethe-Anum», «Eleven Labs»). Zwei Wortformen sind geglättet:
«goldne» klingt als «goldene», «vorübereilt'st» vermutlich als
«vorübereilst».

**Lehre:** `[leise]` an kurzen Höhepunkt-Sätzen ergibt ein Flüstern, 11 bis
14 dB unter dem Pegel der Stimme. Die Erkennung verlor «Kein einziges Mal».
Am Höhepunkt trägt die Stille, darum steht dort `[ruhig, langsam]`. Den
Klang beurteilt Philipp.

## Kosten (9. 10. 2026, Aktionspreis v4 bis 12. 10.)

Rund 14 000 Zeichen Sprache, fünf Geräusche (zusammen 66 s), 45 s Musik
und drei Prüfläufe mit Scribe. Laut Preisliste kosten Geräusche 40 Credits
je Sekunde und Musik 900 Credits je Minute. Den genauen Verbrauch zeigt
das ElevenLabs-Konto; der Schlüssel darf den Zähler nicht lesen.

## Vor einer Veröffentlichung

- **Musiklizenz:** Die Music Terms von ElevenLabs (Stand 26. 5. 2026, § 2a)
  schließen u. a. «religious organizations or institutions» aus. Für
  private Nutzung ist das unerheblich. Bevor eine anthroposophische
  Institution das Feature sendet, ist das zu klären, oder die Musik wird
  ersetzt (sie liegt nur unter Titel, Brücken und Absage).
- «Figaro» war von 2004 bis 2016 der Name von MDR Kultur. Ein heutiges
  Format dieses Namens gibt es nicht.
