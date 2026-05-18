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
