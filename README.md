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

## Vercel: zwei Domains, ein Deployment

Zweites Deploy-Ziel aus demselben Code, zusätzlich zu GitHub Pages. Vercel
setzt beim Build `VERCEL=1`; `astro.config.mjs` schaltet dann auf
`site = https://mantra.saetzerei.com` und `base = /`. Der GitHub-Pages-Deploy
bleibt unverändert (und offen).

Dasselbe Vercel-Projekt (`phtoks-projects/mantra`) bedient zwei Domains mit
unterschiedlichem Verhalten — welche gilt, entscheidet zur Laufzeit
`location.hostname` (`src/lib/geschenk.ts`, `OFFENE_HOSTS`):

- **mantra.saetzerei.com** — die öffentliche Projekt-Domain. App direkt,
  kein Gate, indexierbar.
- **fuer-martje.saetzerei.com** — die Geschenk-Domain fürs Geburtstags-
  Überraschungspaket, bewusst unauffällig benannt. Nur hier aktiv
  (`src/lib/geschenk.ts`):
  - **Digitales Geschenkpapier** — `/geschenk/` ist die Landingpage: ein
    verschnürtes Paket, kein Formular. Ziehen am roten Band (oder
    Klick/Enter darauf) packt die App aus — das Auspacken selbst ist die
    Pointe, kein Geheimwort nötig.
  - **Zugangsschutz** — ohne freigeschalteten Zugang (localStorage-Flag,
    wird beim Auspacken gesetzt) leiten alle Seiten auf `/geschenk/` um.
    Bewusst kein Passwort: der Schutz besteht allein aus der unauffälligen
    Domain und dem Band, das erst gezogen werden muss.
  - `noindex`, damit die Überraschung nicht in Suchmaschinen auftaucht.

**Vercel Web Analytics** — Script ist auf beiden Domains eingebunden;
liefert Zahlen, sobald im Vercel-Dashboard unter Analytics „Web Analytics“
aktiviert ist.

Lokal testen: `VERCEL=1 npm run build && VERCEL=1 npm run preview`. Für die
host-abhängige Logik selbst unter den echten Namen testen: Einträge in
`/etc/hosts` auf `127.0.0.1` anlegen und
`npm run preview -- --host 0.0.0.0 --allowed-hosts mantra.saetzerei.com,fuer-martje.saetzerei.com`.
(Oder nur das Gate auf dem Pages-Build: `GESCHENK=1 npm run build`.)

Fallback-Domain <https://mantra-taupe.vercel.app> verhält sich wie
fuer-martje.saetzerei.com (nicht in `OFFENE_HOSTS`, also gated). DNS von
saetzerei.com läuft über Infomaniak (Nameserver `nsany1/2.infomaniak.com`);
dort liegen A-Records für beide Subdomains → `76.76.21.21`.

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
