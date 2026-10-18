# Arbeitsregeln für dieses Repo

## Sessionwechsel: Zeichen geben, Nachfolgerin anbieten, Modell prüfen

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
> weil <ein Satz>. **Sag ‹ja›.**

Nie mitten in einer Etappe, nie ungefragt starten.

**Bei ‹ja›** startet die alte Session die neue mit `create_session`:
ein Repo (`source_url`), das gewählte `model`, ein Titel, und als
`prompt` eine Übergabe, die ohne den alten Verlauf trägt — Auftrag,
Stand (Branch, PR, erledigt, offen), wo es geschrieben steht, nächster
Schritt. Verweisen statt nacherzählen. Läuft die neue Session
(`get_session` mit ihrer ID), meldet die alte den Titel und archiviert
sich selbst (`archive_session` mit der eigenen ID aus `get_session` ohne
ID). Ist die Arbeit fertig und kommt nichts nach, archiviert sich die
Session nach dem ‹fertig› des Inhabers. Vorher müssen alle beobachteten
PRs gemergt oder geschlossen sein.

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
die Meldung es dazu. Nicht für gesäte Kinder-Sessions und Routinen:
die enden mit ihrem Auftrag.


Urtext: `CLAUDE.md` im Repo `phtok/designs` — dort ändern und von dort verteilen.
