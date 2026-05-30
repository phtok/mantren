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

## Dateistruktur

```
src/
  data/         Inhalte (mantren.yaml, vortraege.json, mantren-kommentar.json,
                quellen.json, glossar.json, onboarding.json)
  pages/        Astro-Seiten (index, universalsuche, einfuehrung, vortraege,
                quellen, tafeln-galerie, impressum, [id] = Mantra-Seiten)
  components/   LectureView, MantraView, KommentarKlappe, GlossarTerm
  layouts/      Base.astro
  lib/          mantren.ts, vortraege.ts, kommentar.ts, glossar.ts,
                typografie.ts
  styles/       global.css
public/
  assets/       Tafelbilder und sonstige statische Bilder
  fonts/        Inclusive Sans (selbstgehostet)
```
