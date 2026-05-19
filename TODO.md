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

**Werkzeug-Features (Teil der Basis oder separates Werkzeug-Modul):**

- **Rezitations-Modus** – Mantram groß, Zeile-für-Zeile-Aufdeckung,
  Pausensteuerung, Schweigetimer nach jedem Vers.
- **Tagesrhythmus / Wochenrhythmus** – passende Strophe pro Wochentag
  (Saturn/Sonne/Mond-Zuordnung der Wiederholungsstunden).
- **Memorier-Trainer** (Spaced Repetition, gegen Sichtprüfung).
- **Druckansicht / EPUB-Export** der eigenen Auswahl.
- **Privates Notizbuch** pro Strophe, verschlüsselt, nur lokal; Sync
  optional ende-zu-ende-verschlüsselt.

**Gemeinschaft (vorsichtig dosieren):**

- **Lese-Kreis-Funktion** – kleine Gruppen, gemeinsamer Wochenrhythmus,
  asynchron; kein „Social", sondern Verabredung.
- **Familien-/Gruppenlizenz** (3–5 Plätze, Rabatt) – entspricht der
  Schul-Praxis gemeinsamer Stunden.

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
