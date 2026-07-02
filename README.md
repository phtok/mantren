# Mantren

Rudolf Steiners mantrisches Spätwerk — eine nichtkommerzielle Web-Ausgabe der
Klassenmantren der Freien Hochschule für Geisteswissenschaft am Goetheanum.

Live: <https://phtok.github.io/mantren/>

## Inhalt

- **Mantren** — Lesefassung des Klassenmantren-Korpus 1924 (Erste/Zweite/Dritte
  Tafel, Stunden 1–19, Sonderspruch 19+) nach dem Mantrenbüchlein Basel 2024.
- **Klassenstunden** — Vortragsfassungen aus GA 270a/b/c, Wiederholungs- und
  Einzelstunden (Bern, Prag, London, Breslau).
- **Wandtafelgalerie** — Tafelzeichnungen aus GA 270i, chronologisch.
- **Kommentare** — pro Mantra: Kerngedanken (kurz/kompakt/ausführlich), Zitate,
  Parallelstellen, Tafelbilder, Varianten und editorische Hinweise.
- **Einführung** — Onboarding für den Einstieg.
- **Quellen und editorische Notiz** — Werknachweis, Textgrundlage, Rechtestatus.
- **Universalsuche** — Volltextsuche über Mantren, Klassenstunden, Kommentare
  sowie Quellen und Editorisches.
- **Impressum**.

PWA: lädt sich auf Wunsch komplett offline.

Schriftbild-Umschalter (⋯-Menü): Standard oder Plex-Edition (Richtung II).

## Technik

- Astro 5 (statische Generierung, Output in `dist/`).
- Inhalts-Quellen: `src/data/*.yaml` (Mantren) und `src/data/*.json`
  (Vorträge, Kommentare, Quellen, Glossar, Onboarding).
- Layout/Komponenten: `src/layouts/Base.astro`, `src/components/*.astro`.
- Styles: `src/styles/global.css` (CSS-only, kein Framework).
- Service Worker via `@vite-pwa/astro`.

## Entwicklung

```sh
npm ci
npm run dev      # http://localhost:4321/mantren/
npm run build    # baut nach dist/
npm run preview  # serviert dist/
```

## Deploy

GitHub Pages, getrieben von `.github/workflows/deploy.yml`. Der Workflow läuft
bei Push auf `main` und auf den deploy-freigeschalteten Branch
`claude/mantren-project-setup-KzVI1`:

- Bei `main`-Push: forwardet den Stand automatisch nach
  `claude/mantren-project-setup-KzVI1` und stößt dort den Deploy via
  `workflow_dispatch` an. So geht jede Änderung auf `main` live, ohne dass die
  Pages-Environment-Schutzregel angepasst werden muss.
- Bei Push auf den deploy-Branch: baut die Site und deployt nach GitHub Pages.

Saubererer Weg langfristig: in Repo-Settings → Environments → `github-pages` →
Deployment branches `main` zulassen. Dann kann der Sync-Job entfernt und der
Workflow direkt auf `main` deployt werden.

## Geschenk-Domain: fuer-martje.saetzerei.com (Vercel)

Zweites Deploy-Ziel aus demselben Code. Vercel setzt beim Build `VERCEL=1`;
`astro.config.mjs` schaltet dann auf `site = https://fuer-martje.saetzerei.com`
und `base = /`. Der GitHub-Pages-Deploy bleibt unverändert (und offen).
Die Subdomain ist bewusst unauffällig gewählt — sie soll nicht verraten,
was hinter dem Geschenkpapier steckt.

Nur auf dieser Variante aktiv (`src/lib/geschenk.ts`):

- **Digitales Geschenkpapier** — `/geschenk/` ist die Landingpage: ein
  verschnürtes Paket, kein Formular. Ziehen am roten Band (oder Klick/Enter
  darauf) packt die App aus — das Auspacken selbst ist die Pointe, kein
  Geheimwort nötig.
- **Zugangsschutz** — ohne freigeschalteten Zugang (localStorage-Flag, wird
  beim Auspacken gesetzt) leiten alle Seiten auf `/geschenk/` um. Bewusst
  kein Passwort: der Schutz besteht allein aus der unauffälligen Domain und
  dem Band, das erst gezogen werden muss.
- **Vercel Web Analytics** — Script ist eingebunden; liefert Zahlen, sobald
  im Vercel-Dashboard unter Analytics „Web Analytics“ aktiviert ist.

Lokal testen: `VERCEL=1 npm run build && VERCEL=1 npm run preview`
(oder nur das Gate auf dem Pages-Build: `GESCHENK=1 npm run build`).

Live unter <https://fuer-martje.saetzerei.com> — Vercel-Projekt
`phtoks-projects/mantra` (Fallback-Domain
<https://mantra-taupe.vercel.app>). DNS von saetzerei.com läuft über
Infomaniak (Nameserver `nsany1/2.infomaniak.com`); dort liegt ein
A-Record `fuer-martje.saetzerei.com → 76.76.21.21`.

## Dateistruktur

```
src/
  data/         Inhalte (mantren.yaml, vortraege.json, mantren-kommentar.json,
                quellen.json, glossar.json, onboarding.json)
  pages/        Astro-Seiten (index, universalsuche, einfuehrung, vortraege,
                quellen, tafeln-galerie, impressum, geschenk, [id] = Mantra-Seiten)
  components/   LectureView, MantraView, KommentarKlappe, GlossarTerm
  layouts/      Base.astro
  lib/          mantren.ts, vortraege.ts, kommentar.ts, glossar.ts,
                typografie.ts
  styles/       global.css
public/
  assets/       Tafelbilder und sonstige statische Bilder
  fonts/        Inclusive Sans (selbstgehostet)
```
