# TODO

## Offline-Zugriff funktioniert nicht zuverlässig

**Symptom (User-Test, Flugmodus):** Nicht alle Kapitel sind offline
erreichbar, obwohl der „offline bereit"-Button grün gezeigt hatte.

**Wahrscheinliche Ursachen, die zu prüfen sind:**

- Workbox-Precache-Manifest deckt nicht alle Routen ab. `globPatterns`
  in `astro.config.mjs` listet `**/*.{js,css,html,woff2,svg,png,ico,webmanifest}`
  — der Build erzeugt aber `dist/<id>/index.html` für jede Mantra-Route,
  was die Glob fängt. Trotzdem manuell verifizieren, ob alle 40+ Routen
  im Workbox-Manifest landen (`dist/sw.js` inspizieren).
- `navigateFallback: '${base}/'` fängt unbekannte Routen ab — könnte bei
  Routen mit Sonderzeichen wie `19+` oder `7.1` ein Problem sein. Test:
  diese Routen einzeln im Flugmodus aufrufen.
- Der manuelle `fetch()`-Loop im Offline-Button trifft den SW, der die
  Antworten cached. Wenn der SW aber nicht aktiv war zum Zeitpunkt des
  Buttondrucks (z. B. erster Besuch, SW installierte gerade noch),
  landen die Responses nur im HTTP-Cache, nicht im SW-Cache. Beim
  Flugmodus-Test ist dann genau dieses Mantra nicht da.
- iOS Safari hat eigenwillige SW-Lebenszeiten (~7 Tage ohne Besuch
  -> Eviction). Eventuell mit `apple-touch-icon` + größerem
  `apple-mobile-web-app` Setup robuster.

**Mögliche Lösungen, die zu evaluieren sind:**

1. Statt nur über den SW: zusätzlich die `Cache API` direkt nutzen und
   alle URLs explizit in einen named Cache (`mantren-v1`) legen. Dann
   im SW oder via `fetch`-Handler aus diesem Cache servieren.
2. Beim Buttondruck warten, bis `navigator.serviceWorker.ready`
   resolved hat, bevor `fetch()` läuft. Sonst sind die Requests am SW
   vorbei.
3. Per `caches.open(...).then(cache => cache.addAll(urls))` direkt in
   den Workbox-Cache schreiben. Klarer und unabhängig vom SW-Timing.
4. Bereit-Indikator erst grün setzen, nachdem stichprobenartig geprüft
   wurde, dass die URLs auch wirklich im Cache liegen
   (`caches.match(url)`).

## Monetarisierung

**Modell:** Verkauf von Magiclinks, gebunden an echte E-Mail-Adresse.
Einmalige Basis-Lizenz (~30 €), keine Abos. Updates der Basis-Daten
inklusive (Vertrauen). Zusatzmodule als Einzelkäufe. Vorteile: DSGVO-
konform, keine App-Store-Gebühr, klare Eigentumsverhältnisse,
Missbrauchskonten gezielt sperrbar.

**Basis-Lizenz (einmalig):**

- Volltext aller Klassenstunden (GA 270a–d, soweit verfügbar)
- Strophen-Kommentare in drei Tiefenstufen
- Tafelbilder (Standardauflösung)
- **Verschlüsselte Lesezeichen und eigene Notizen** – pflichtmäßig,
  nicht optional. Ende-zu-ende-verschlüsselt; Schlüssel beim Nutzer,
  Sync nur über zero-knowledge. Bindung an die Lizenz-Mailadresse.
- Lebenslange Updates der Basis-Daten

**Zusatzmodule (separat zukaufbar):**

- **Audio-Rezitationen** – Mantren von Kennern eingesprochen, mehrere
  Stimmen (m/w), Originaltempo + langsam-meditativ. Vermutlich stärkster
  Treiber der Zahlungsbereitschaft.
- **Kennerkommentare** als „Stimmen" – Witzenmann, Prokofieff, lokale
  Schulträger; je Stimme ein Add-on.
- **Faksimile-Tafelbilder** in hoher Auflösung mit Zoom, Originalfarben
  rekonstruiert.
- **Originalseiten als PDF** (GA-Faksimile), wo rechtlich möglich.
- **Querschnitte** – thematische Zusammenstellungen (Hüter, Drei-Tiere,
  Christus-Sonne, Michael-Imagination) über alle Stunden.
- **Esoterische Geographie** – Karten der Vortragsorte, biographische
  Einordnung Steiners im April 1924.
- **Meditationspraxis** – Tipps und Hinweise zur Technik, Erfahrungen
  und Anleitungen erfahrener Meditierender; Haltung, Atem, Zeit-/
  Ortswahl, Umgang mit Hindernissen, Umgang mit Bildern. Sensibel
  kuratiert, ohne Guru-Ton; verschiedene Schulrichtungen sichtbar
  nebeneinander.

**Werkzeug-Features (Teil der Basis oder separates Werkzeug-Modul):**

- **Rezitations-Modus** – Mantram groß, Zeile-für-Zeile-Aufdeckung,
  Pausensteuerung, Schweigetimer nach jedem Vers.
- **Tagesrhythmus / Wochenrhythmus** – passende Strophe pro Wochentag
  (Saturn/Sonne/Mond-Zuordnung der Wiederholungsstunden).
- **Memorier-Trainer** (Spaced Repetition, gegen Sichtprüfung).
- **Druckansicht / EPUB-Export** der eigenen Auswahl.

**Gemeinschaft (vorsichtig dosieren):**

- **Lese-Kreis-Funktion** – kleine Gruppen, gemeinsamer Wochenrhythmus,
  asynchron; kein „Social", sondern Verabredung.
- **Gruppenlizenz mit Verwaltungsfunktion** – Inhaber kauft N Plätze
  und trägt die E-Mail-Adressen ein, die Magiclinks erhalten. Plätze
  sind später umsetzbar (z. B. wenn ein Teilnehmer ausscheidet),
  Verwaltungsoberfläche zeigt Stand der eingelösten / offenen Plätze.
  Sinnvoll für Familien (3–5 Plätze) und für Klassenträger / Lese-
  kreise (10–25 Plätze, mit gestaffeltem Preis pro Platz).

**Offene technische Punkte:**

- Magiclink-Backend (E-Mail-Versand, Token-Erzeugung, Konto-Sperre).
- Lizenzprüfung im PWA-Kontext (offline-tolerant, mit periodischer
  Re-Validierung).
- Modul-Freischaltung (welche Daten/Assets sind Teil welcher Lizenz;
  Auslieferung erst nach Prüfung).
- Zahlungsabwicklung (Stripe? SEPA? Rechnung?) – DSGVO und keine
  App-Store-Bindung sind die Leitplanken.
- Priorisierung erstes Zusatzmodul nach der Basis: Audio-Rezitation,
  erster Kennerkommentar oder Faksimile-Hochauflösung – offen.

## Monetarisierung — Drehung auf Service-Logik (21.5.2026)

**Die Sorge.** Wenn der Eindruck entsteht, dass ‹die Texte verkauft
werden› — Steiners gemeinfreier Wortlaut oder selbst der erläuternde
Anmerkungs-Apparat, der ja zum Werk gehört — droht ein Aufschrei in
der anthroposophischen Community. Marie Steiners eigenes Ringen um
die Überlieferung steht im Hintergrund jeder Preisseite.

**Die Drehung.** Der eigentliche Wert ist nicht der Text, sondern die
Handhabung: Werkzeug, Aufbereitung, Vertrauen in die Pflege, das
geräteübergreifende Notizsystem, das ‹Du-darfst-vergessen, das System
weiss noch›. Konsequent gedacht: **Alle Texte bleiben frei, bezahlt
wird ausschliesslich die Dienstleistung am Werk.** Das löst den
Konflikt strukturell — niemand kann sagen, hier werde Steiner
verkauft.

**Was wirklich gern gezahlt wird, in diesem Zusammenhang:**

1. **Audio-Rezitationen.** Vermutlich stärkster Treiber: wer hört,
   kann meditieren ohne lesen zu müssen. Mehrere Stimmen (m/w),
   Originaltempo + langsam-meditativ. Klar abgegrenzte Eigenleistung
   der Sprecher.
2. **Print-on-Demand der eigenen Auswahl.** Gebundenes Heft mit
   eigenen Lesezeichen und Notizen, eigener Reihenfolge — kein
   Werkverkauf, sondern persönlicher Buchgegenstand.
3. **Cloud-Sync verschlüsselter Notizen** über Geräte hinweg.
   Infrastruktur, ehrlich bezahlbar.
4. **Rezitations- und Werkzeug-Modus.** Zeile-für-Zeile-Aufdeckung,
   Schweigetimer, Wochenrhythmus mit Saturn/Sonne/Mond-Zuordnung,
   Memorier-Trainer mit Spaced Repetition.
5. **Gruppen-Verwaltung.** Lesekreise mit Verwaltungsoberfläche, N
   Plätze, Plätze umsetzbar bei Wechseln. Service für Klassenträger.
6. **Wandtafel-HD-Faksimile.** Hochauflösende Reproduktionen aus
   GA 270i mit Zoom und Originalfarben — Editionsleistung.
7. **Faksimile-Sammelband.** Klartextnachschriften Helene Finckhs in
   einem Band, statt 19 verstreute PDFs.
8. **Kennerkommentare als ‹Stimmen›.** Witzenmann, Prokofieff, lokale
   Schulträger — explizit fremde Beiträge, kein Steiner-Verkauf.
9. **Esoterische Geographie.** Karten der Vortragsorte, Biographie
   Steiners im April 1924. Forschungsleistung.
10. **Meditationspraxis-Modul.** Kuratierte Anleitungen Erfahrener,
    Schulrichtungen nebeneinander, ohne Guru-Ton.

**Was niemand gern zahlt:**

- Reinen Zugriff auf Mantren-Wortlaut.
- Anmerkungsstufen ‹kompakt› oder ‹ausführlich› hinter Paywall — das
  fühlt sich an wie Werk-Salami.
- Vortrags-Apparat als Bezahlinhalt — Steiners Wort hinter Schloss
  zu setzen ist die maximal angreifbare Geste.

**Was sich aus der Drehung ergibt:**

- Die App ist in voller Tiefe frei lesbar: Mantren, alle drei
  Anmerkungsstufen, Vorträge, Tafelbilder in mittlerer Auflösung,
  Quellen, Glossar, Wandtafelgalerie.
- Die App-Schicht ist die ‹Bibliothek›, die App-Dienste sind das
  ‹Café›: bequem, schön, persönlich — und bezahlt.
- **Förder-Mitgliedschaft** als freiwilliger Beitrag (Pay-what-you-want
  ab z. B. 24 €/Jahr) für Leser, die einfach die Pflege unterstützen
  wollen, ohne ein einzelnes Modul zu brauchen. Träger-Status,
  vielleicht ein Bändchen im UI, sonst nichts. Kein Hauch von
  Werk-Bezahlung, nur Dank.

**Beispielpreise (Stützpfeiler, nicht final):**

| Modul                                          | Preis             |
|------------------------------------------------|-------------------|
| Audio, eine Stimme                             | 39 € einmalig     |
| Audio, mehrere Stimmen + Tempi                 | 69 € einmalig     |
| Notiz-Sync (lebenslang)                        | 24 € einmalig     |
| Werkzeug-Paket (Rezitation, Wochenrhythmus, Memorier) | 19 € einmalig |
| Print-on-Demand eigene Auswahl                 | 18–35 € pro Druck |
| HD-Wandtafel-Faksimile                         | 29 € einmalig     |
| Kennerkommentar pro Stimme                     | 19 € einmalig     |
| Meditationspraxis-Modul                        | 29 € einmalig     |
| Esoterische Geographie                         | 19 € einmalig     |
| Förder-Mitgliedschaft                          | 24 €/Jahr (PWYW)  |
| Gruppen-Verwaltung (10 Plätze für Notiz-Sync)  | 99 € einmalig     |

**Sprachregel.** Nie ‹kaufen›, immer ‹freischalten›, ‹beitragen›, ‹die
Pflege unterstützen›. Nie ‹Inhalt›, sondern ‹Dienst› oder ‹Werkzeug›.
Auf der Bezahlseite einleitend: ‹Alle Texte dieser Seite sind frei
zugänglich. Dieses Modul bezahlt die Eigenleistung der Bearbeitenden /
Sprechenden / Pflegenden.›

**Anschluss an das frühere Pro/Max-Modell.** Verworfen in der dort
vorgeschlagenen Form. Wer ‹alle Anmerkungen› und ‹alle Vorträge›
hinter Stufen setzt, gibt die Drehung wieder her. Die Stufen-Logik
funktioniert nur, wenn das Bezahlte eindeutig App-Dienstleistung ist.

### Marktschätzung (21.5.2026)

**Adressierbare Gruppen weltweit:**

| Gruppe                                              | Grösse        | Affinität  |
|-----------------------------------------------------|---------------|------------|
| Mitglieder der Allgemeinen Anthroposophischen Ges.  | ~40–50 Tsd.   | grund­sätzlich |
| davon Mitglieder der Ersten Klasse                  | ~10–15 Tsd.   | hoch       |
| davon **aktive** Klassenstunden-Teilnehmende        | ~5–8 Tsd.     | sehr hoch  |
| Forschende, Waldorflehrer:innen, Therapeut:innen mit Interesse am Spätwerk, ohne Klassen-Mitgliedschaft | ~3–8 Tsd. | mittel     |

Der adressierbare Kern sind die **~5'000–8'000 aktiven Klassenmitglieder**, plus ein weicher Rand bis ~15'000 Menschen weltweit.

**Konversionsannahmen:**

- Free-Nutzung: 10–20 % der adressierbaren Gruppe finden die Seite im 1. Jahr; mit Multiplikatoren (Dornach, Sektionsrundbriefe, Vortragsreisen) eher 25 %.
- Zahlende Konversion über freiwillige Module: 5–15 % der aktiven Nutzer:innen pro Jahr.
- Lebenslange Einmal-Lizenzen → Käufer-Stock baut sich kumulativ auf; Spitze typischerweise in Jahr 2, Plateau ab Jahr 3.

**Drei Szenarien Käufer/Jahr (realistisch revidiert):**

| Szenario     | Jahr 1 | Jahr 2 | Jahr 3 | Total 3 J |
|--------------|-------:|-------:|-------:|----------:|
| Konservativ  |     80 |    130 |    150 |       360 |
| Realistisch  |    200 |    400 |    450 |     1'050 |
| Optimistisch |    400 |    700 |    800 |     1'900 |

Das ‹optimistische› Szenario entspricht etwa 20 % Marktdurchdringung der aktiven Klassenmitglieder in drei Jahren, bei einer zahlenden Konversion von 1:3. Sportlich; braucht Empfehlungen aus Dornach / Sektion oder gut sichtbare Promo.

**Cashflow im neuen optimistischen Szenario (AOV 60 CHF, BS, Einzelfirma):**

| Posten                          |  Jahr 1 |  Jahr 2 |  Jahr 3 |
|---------------------------------|--------:|--------:|--------:|
| Brutto-Umsatz                   | 24'000  | 42'000  | 48'000  |
| Reingewinn nach Auslagen+Audio  | ~17'000 | ~38'000 | ~44'000 |
| **Netto-Cash nach AHV + ESt**   | **~13'000** | **~28'000** | **~32'000** |

Auch im günstigen Fall **kein Vollerwerb in den ersten drei Jahren** — solides Nebeneinkommen, das die Pflegezeit langsam abdeckt.

**Hebel, die die Zahlen realistisch heben:**

1. Empfehlung von Dornach oder einer Sektion — einmaliger Schub.
2. Druckausgabe-Bundle: Mantrenbüchlein kaufen → Notiz-Sync gratis dabei.
3. Mantrenwerkstätten als Vertriebskanal (Basel + Folgewerkstätten); pro Veranstaltung 30–80 Teilnehmende, davon 30–50 % Käufer.
4. Englische Übersetzung der App-Oberfläche → adressierbarer Markt verdoppelt sich.
5. Audio bei Tagungen einmal vorgespielt → starke Mund-zu-Mund-Wirkung.

**Ohne diese Hebel:** ehrliche Obergrenze ~300–500 Käufer/Jahr. Das ‹realistische› Szenario ist dann die Erwartung, nicht das ‹konservative›.
