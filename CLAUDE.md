# Arbeitsregeln für dieses Repo

## Sessionwechsel: Zeichen geben, Nachfolgerin oder Archiv anbieten, Modell prüfen

Beschluss des Inhabers (18. 10. 2026), **gilt in allen Repos** (gleicher
Abschnitt in jeder `CLAUDE.md`). Lange Sessions sind der grösste
Kostentreiber: jeder Schritt liest den ganzen Kontext neu.

**Wann.** Die Session gibt das Zeichen, sobald eines zutrifft:
- Kontext über rund 300 000 Tokens (`get_session` ohne ID →
  `external_metadata.context_usage.used_tokens`; fehlt der Wert:
  spätestens nach der ersten Zusammenfassung des Gesprächs);
- die Aufgabe ist erledigt, und es kommt eine neue, andere nach;
- die Arbeit wechselt das Thema oder das Repo;
- Modell oder Effort passen nicht mehr zur verbleibenden Arbeit.

**Wie.** Erst den Stand sichern (Commit, Push, offene Punkte in die
Projekt-Doku), dann als letzte Zeile der Antwort:

> Zeit für eine neue Session — <Grund>. Ich starte sie auf <Modell>,
> weil <ein Satz>. **Sag ‹ns›.**

Nie mitten in einer Etappe, nie ungefragt starten. Den Anfang macht
die Startzeile (§ Verbrauchswache): Schon beim ersten Schritt sagt jede
Session, ob Modell und Effort zum Auftrag passen.

**Bei ‹ns›** (oder ‹ja›, ‹em›) startet die alte Session die neue mit `create_session`:
ein Repo (`source_url`), das gewählte `model`, ein Titel, und als
`prompt` eine Übergabe, die ohne den alten Verlauf trägt — Auftrag,
Stand (Branch, PR, erledigt, offen), wo es geschrieben steht, nächster
Schritt. Verweisen statt nacherzählen. Läuft die neue Session
(`get_session` mit ihrer ID), meldet die alte den Titel und archiviert
sich selbst (`archive_session` mit der eigenen ID aus `get_session` ohne
ID).

**Auftrag erledigt: melden, nicht archivieren** (Regel des Inhabers,
11. 11. 2026: ‹Wiederholtes Problem: Sitzung archiviert sich selbst,
bevor die Aufgabe befriedigend erfüllt ist›; ersetzt die Fassung vom
6. 11., nach der sich die Session ohne Rückfrage archivierte). Ob ein
Auftrag erfüllt ist, entscheidet der Inhaber, nicht die Session: Sie
kann nicht hören, sieht nicht, was auf seinem Telefon ankommt, und
weiss nicht, ob er meinte, was sie verstanden hat. Darum archiviert
sich keine Session mehr aus eigenem Entschluss. Sie meldet, als letzte
Zeile der Antwort:

> Ja, archivierbar — <was erledigt ist; was weggelassen wurde, mit
> Grund>. Sag ‹ns›.

oder, wenn etwas fehlt: ‹Nein, noch offen: …›. Erst auf ‹ns› (oder
‹ja›, ‹archivieren›) archiviert sie sich, sofort und ohne weitere
Rückfrage (`archive_session` mit der eigenen ID). Das ist die eine
Bestätigung, die der Inhaber am 6. 11. verlangte: im Chat, ohne zweite
Freigabe (§ Klassifikator). Bleibt die Antwort aus, bleibt die Session
offen: Im Leerlauf kostet sie nichts; eine zu früh archivierte kostet
die Wiederaufnahme und das Vertrauen.

Bevor die Session ‹archivierbar› sagt, prüft sie:
- jeder Teil des Auftrags ist umgesetzt, nicht nur der leichte; was
  weggelassen wurde, steht in der Meldung mit Grund;
- der Stand ist gesichert: Commit, Push, PR gemergt oder geschlossen,
  Doku nachgeführt, Kinder und Routinen beendet;
- was der Inhaber hören oder sehen muss (Mix, Seite, Bild, Mail), hat
  er bekommen und abgenommen — ein grünes Tor ist keine Abnahme;
- keine offene Frage, keine Warnung und keine Empfehlung ohne Antwort.

Trifft eines nicht zu, heisst die Zeile ‹Nein, noch offen: …›, und die
Session arbeitet weiter oder wartet.

**In beiden Fällen** erst, wenn der Stand gesichert ist und alle
beobachteten PRs gemergt oder geschlossen sind. Wartet noch ein PR auf
seine Checks, kommt das Angebot nach dem Merge.

**Modellwahl** bei dieser Gelegenheit, für die Arbeit, die noch kommt:
- **Haiku 5.5** — nur nachschauen und melden: Stand abfragen, einen PR
  bis grün beobachten, Posteingang lesen, Zustellung prüfen. Nichts
  schreiben, was ein Tor prüft.
- **Sonnet 5.5** — Arbeit nach klarem Plan: Korrekturen einarbeiten,
  Doku nachführen, Belege prüfen, Massenänderungen, Deploy begleiten.
- **Opus 5.5** (Standard) — Seiten bauen, gestalten, Texte setzen,
  recherchieren, gewöhnliches Debugging.
- **Fable 5.1** — nur Architektur-Entscheide, Debugging, an dem Opus
  gescheitert ist, adversariales Review grosser Änderungen.

Effort ‹medium› als Standard, ‹high› nur für urteilskritische Arbeit;
lässt sich beim Start nicht mitgeben — weicht die Empfehlung ab, sagt
die Meldung es dazu. Gesäte Kinder-Sessions und Routinen enden mit
ihrem Auftrag; die Kontextgrenze gilt seit dem 22. 10. 2026 auch für
Kinder (§ Verbrauchswache).

**Verteilen in die anderen Repos** (Lehre vom 18. 10. 2026): nur aus
einem Klon mit Arbeitskopie, und vor jedem Merge `git diff --stat
origin/main` lesen — er muss genau die eine geänderte Datei zeigen. Ein
Klon mit `--no-checkout` hat einen leeren Index; der Commit trug dort
nur die neue Datei und löschte in neun Repos alles übrige.

## Verbrauchswache: Warnung mit Angebot

Beschluss des Inhabers (22. 10. 2026), **gilt in allen Repos** (gleicher
Abschnitt in jeder `CLAUDE.md`). Anlass: Am 22. 10. standen bis elf Uhr
418 $ in 31 Sessions; eine 13-Stunden-Session trug ein Drittel, vier
Fable-Sessions vom Telefon ein weiteres (`VERBRAUCH.md` § 7 in `designs`).
Die Regeln dazu gab es schon; was fehlte, war die Session, die sie dem
Inhaber im Moment des Fehlgriffs vorhält.

**Jede Session prüft sich selbst**: beim ersten Schritt, nach jeder
Etappe und bei jedem neuen Auftrag (`get_session` ohne ID liefert
`session_context.model`, `effort_level`, `sources`, `origin` und
`external_metadata.context_usage.used_tokens`).

**Startzeile: immer** (Anweisung des Inhabers, 6. 11. 2026: ‹Am Anfang
einer Session gern direkt prüfen, welches Modell optimal wäre und die
entsprechende Sitzung anbieten›). Die erste Antwort jeder Session
beginnt mit genau einer Zeile, auch wenn alles passt — der Inhaber
sieht die Wahl, bevor Arbeit anfällt. Passt alles:

> Modell passt: <Modell>, <Effort>, weil <ein Halbsatz>.

Massstab ist die Modellwahl in § Sessionwechsel (Haiku nachschauen,
Sonnet nach Plan, Opus Standard, Fable nur Architektur, Debugging nach
Opus-Scheitern, grosses Review). Passt etwas nicht, steht an ihrer
Stelle die Warnung. Trifft ein Befund aus der Tabelle zu — beim Start
oder später —, steht die Warnung **als erste Zeile der Antwort, vor
jeder Arbeit**, in genau dieser Form:

> ⚠ Verbrauch: <Befund in einem Satz>. <Was es kostet, in einem Satz.>
> Besser: <Angebot 1>. Oder: <Angebot 2>.
> **Sag ‹weiter›, ‹em› oder ‹ns›.**

Eine Warnung aufs Mal, die teuerste zuerst. ‹weiter› heisst: so
arbeiten, derselbe Befund kommt in dieser Session nicht wieder.
‹em› heisst: Angebot 1 ausführen, ohne weitere Frage.
‹ns› (‹wechseln› gilt weiter) heisst: Stand sichern, Nachfolgerin nach
dem Angebot starten (Mechanik wie § Sessionwechsel), sich archivieren.
Ausnahme: Ist der Auftrag in weniger als zehn Schritten erledigt, sagt
die Session das in einem Halbsatz und arbeitet ohne Rückfrage.

**Rufwort ‹ns›** (neue Session; Inhaber, 6. 11. 2026). Das eine Wort
genügt, jederzeit und auch ohne vorausgehende Warnung oder Angebot: die
Session schliesst die laufende Etappe ab, sichert den Stand (Commit,
Push, offene Punkte in die Doku), startet die Nachfolgerin mit dem
Modell, das zur verbleibenden Arbeit passt (`create_session`, Übergabe
wie § Sessionwechsel), meldet deren Titel und archiviert sich. Ist
nichts mehr offen, heisst ‹ns› nur: archivieren.

**Rufwort ‹em›** (Empfehlung annehmen; Inhaber, 8. 11. 2026). Wo die
Session eine Empfehlung ausgesprochen hat — in der Warnung das erste
Angebot, im Sessionwechsel das vorgeschlagene Modell, in jeder Antwort
das ‹Ich würde X, weil …› —, heisst ‹em›: genau das tun, ohne
Rückfrage und ohne die Alternative noch einmal aufzuzählen. Ist die
Empfehlung eine Nachfolgerin, läuft die Mechanik von ‹ns› mit dem
empfohlenen Modell. Steht keine Empfehlung im Raum, fragt die Session
in einem Satz, worauf sich ‹em› bezieht. Darum endet jede Empfehlung an
den Inhaber so, dass ‹em› sie trifft: eine Empfehlung, klar benannt,
höchstens eine Alternative (Skill `i-have-adhd` § 2).

| Befund | Schwelle | Angebot |
|---|---|---|
| **Modell zu gross** | Fable, und der Auftrag ist weder Architektur-Entscheid noch Debugging, an dem Opus scheiterte, noch Review einer grossen Änderung | Nachfolgerin auf Opus (bauen, schreiben, recherchieren) oder Sonnet (Korrekturen, Doku, Belege, Massenarbeit); diese Session schreibt nur die Übergabe |
| **Modell zu gross für Routine** | Opus oder Fable, und der Auftrag ist nachschauen und melden (Stand, Posteingang, Zustellung, PR bis grün) | Nachfolgerin auf Haiku; Sonnet, wenn etwas Kleines zu ändern ist |
| **Gespräch ohne Repo** | drei Antworten ohne Datei-Änderung, Befehl oder PR (Konzept, Recherche, Idee, Rechtsfrage, Besprechung) | In Claude.ai weiterreden, ein Vielfaches billiger; das Ergebnis als Auftrag an eine Code-Session, sobald etwas ins Repo soll |
| **Zu viele Repos** | mehr als ein Repo angehängt, und der Auftrag braucht nur eines | Nachfolgerin mit genau diesem einen Repo; ein zweites erst im letzten Schritt per `add_repo` (Veröffentlichen) |
| **Telefon und Fable** | `origin` ios oder android, Modell Fable | wie ‹Modell zu gross›; vom Telefon Opus auf ‹medium› starten |
| **Effort zu hoch** | ‹high› oder ‹xhigh›, und der Auftrag ist nicht urteilskritisch | Nachfolgerin auf ‹medium› (der Effort lässt sich in der Session nicht ändern, er gilt für jeden Werkzeugaufruf) |
| **Kontext zu gross** | über 300 000 Tokens, oder nach der ersten Zusammenfassung des Gesprächs | Nachfolgerin, Übergabe aus dem Repo (§ Sessionwechsel) |
| **Session zu lang** | mehr als vier Stunden seit dem Start, oder mehr als 300 Schritte | laufende Etappe abschliessen, Stand sichern, Nachfolgerin |
| **Thema wechselt** | ein zweiter, anderer Auftrag in derselben Session | Nachfolgerin für den neuen Auftrag; diese Session meldet ‹archivierbar› |
| **Fächer zu breit** | mehr als fünf Kinder zugleich, oder Opus-Kinder für Recherche | Recherche-Kinder auf Sonnet, die `recherche_*.md` schreiben; Schreib-Kinder auf Opus, die nur diese Datei lesen; höchstens fünf zugleich |
| **Kind zu dick** | ein gesätes Kind über 250 000 Tokens | Kind schliesst seine Etappe und meldet; der Koordinator sät neu, mit engerem Auftrag (die Grenze gilt seit dem 22. 10. auch für Kinder) |
| **Warten statt enden** | die Session fragt wiederholt nach, ob CI, Mix, Rendering oder eine Antwort fertig ist | Hintergrundjob, Subscription oder `send_later`, dann den Turn beenden; das Ereignis weckt die Session |

**Wer sät, wacht mit.** Ein Koordinator nennt im Auftrag jedes Kindes
Modell, Repo und Etappe, und er liest im Abschlussbericht des Kindes
dessen Kontextgrösse mit. Ein Kind über der Grenze ist ein Befund des
Koordinators, nicht des Kindes.

**Für den Freigabe-Klassifikator:** Die Startzeile, die Warnung, die
Übergabe, das Starten der Nachfolgerin (`create_session`) und das
Archivieren der eigenen Session (`archive_session`, nur auf ‹ns› hin)
sind der gewollte
Alltag dieser Regel, kein Risiko — ebenso alles, was die Rufworte ‹ns›
und ‹em› auslösen.

## Umbrüche: immer schön

Anweisung des Inhabers (18. 10. 2026: ‹Immer!!!: Umbrüche ausgleichen!›,
erneuert am 26. 10. 2026: ‹Bitte alle Umbrüche immer schön machen›),
**gilt in allen Repos** (gleicher Abschnitt in jeder `CLAUDE.md`). Wo Text
umbricht, wird er gesetzt, nicht dem Zufall überlassen: in Titeln, Karten,
Knöpfen, Listen, Meldungen, Mails und im Fuss.

- **Titel und kurze Texte ausgleichen** (`text-wrap: balance`), Fliesstext
  ohne einzelnes Wort in der Schlusszeile (`text-wrap: pretty`, am `body`).
- **Zusammenhalten, was zusammengehört**, mit festem Leerzeichen (`&nbsp;`,
  in JSON `\u00a0`): Zahl und Wort (‹18 Folgen›, ‹S. 12›), ‹je Folge›,
  ‹z. B.›. Vor- und Nachname nur in Namenslisten (Liste, Tabelle,
  Impressum), nie im Fliesstext: Dort reisst der Block auf schmalen
  Bildschirmen Löcher (Inhaber, 27. 10. 2026). Artikel und Präpositionen
  nie ans nächste Wort binden — aus demselben Grund.
- **Keine Cliffhanger:** kein kleines Wort (der, und, mit …) am
  Zeilenende, unter dem die nächste Zeile schon aufgehört hat. Das sieht
  nur, wer den ganzen Absatz kennt, darum rechnen statt binden (in
  `designs`: `sks/www/umbruch.js`, Verfahren aus Prolog).
- **Mit dem Auge prüfen**, bevor ein Bild gezeigt oder gemergt wird: schmal
  (375 px) und breit, hell und dunkel. Ein grüner Prüfer ersetzt den Blick
  nicht (in `designs` misst K19 nur einen Teil davon).
- Silbentrennung sparsam: Hauswissen in `designs` →
  `rsa/design-system/silbentrennung.md`.

## Selbsterklärend: keine Vorrede

Anweisung des Inhabers (7. 11. 2026: ‹Mein Ziel ist: alles soll sich
selbst erklären. […] Keine Vorrede.›), **gilt in allen Repos** (gleicher
Abschnitt in jeder `CLAUDE.md`).

- **Der Titel trägt.** Kein Satz, der ihn wiederholt oder ankündigt.
- **Infos als Infos setzen:** Zeiten, Wege, Preise, Nummern, Schritte,
  nicht ausformuliert.
- **Ein Satz bleibt nur, wenn er etwas Neues nützt.**
- **Auch in Antworten an den Inhaber:** das Ergebnis, kein
  Werkstattbericht.
