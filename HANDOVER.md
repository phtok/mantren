# HANDOVER — Mantren-Web-App

Stand: Mai 2026. Übergabe für einen neuen Chat / eine neue Session. Wer
dieses Dokument liest, soll danach genauso arbeiten können wie der
bisherige Assistent. Bitte zuerst `TODO.md` und diese Datei lesen,
*dann* `src/data/vortraege.json` oder `src/data/mantren-kommentar.json`
gezielt nach Bedarf öffnen — die Datenfiles sind groß.

---

## 1 · Projekt in einem Satz

Statische Web-App zu Rudolf Steiners *Klassenstunden der Freien Hochschule
für Geisteswissenschaft am Goetheanum 1924* (GA 270): die Mantren des
Zyklus als App-Seiten mit dreistufigen Begleitkommentaren, die
Vortragstexte (Klassenstunden, Wiederholungs- und Einzelstunden) als
Lesefassungen, dazu Wandtafelzeichnungen und ein editorischer Apparat.

Ziel: ein ruhiges, lesefreundliches Werkzeug für Anthroposophen, mobil
und offline tauglich, später monetarisierbar (siehe `TODO.md`).

---

## 2 · Tech-Stack

- **Astro** (Static Site Generator) — `astro build` erzeugt `dist/`
- **TypeScript** (lose), kein React/Vue; serverseitig gerendert, kein
  Client-Hydration
- **Vanilla CSS** in `src/styles/global.css` — kein Tailwind, kein
  CSS-in-JS. Theme via CSS-Variablen (Hell-/Dunkelmodus über
  `.theme-invert` auf `<html>`)
- **PWA** über `@vite-pwa/astro-integration` mit Workbox-Precaching
- **`is:inline`-Skripte** für kleine Interaktionen (TTS, Tafel-
  Fullscreen, Suche, Offline-Button, Topbar-Verhalten, Tafel-Wegklapper)
- **Daten** als JSON in `src/data/`, plus `mantren.yaml` für das
  Mantren-Verzeichnis selbst
- Hosting: GitHub Pages (Repo `phtok/mantren`, Base-URL `/mantren/`)

Build-Befehl: `npm run build`. Kein Dev-Server in dieser Session
gestartet — die remote Container-Umgebung ist ephemer, alles muss
gepusht werden, damit es bleibt.

---

## 3 · Git, Branch, Push-Regel

- **Entwicklung NUR auf:** `claude/mantren-project-setup-KzVI1`.
  Nie auf andere Branches schreiben oder forcieren.
- **GitHub-MCP nur für `phtok/mantren`.** Kein anderes Repo.
- **Push ausschließlich auf explizite Bestätigung des Users.**
  Der Stop-Hook erinnert nach jedem Commit; trotzdem nicht von selbst
  pushen — der User möchte das so. Nach „push" / „Klar" / „push!" wird
  gepusht.
- Commit-Nachrichten in Deutsch, klein, mit `area: Beschreibung`-Schema
  (`data:`, `assets:`, `ui:`, `feat:`, `style:`, `audio:` …).
  Mehrzeiliger Body als HEREDOC mit `git commit -m "$(cat <<'EOF' …`.
  Trailer-Zeile am Ende des Bodies: `https://claude.ai/code/session_…`
  (Session-ID).
- Keine Marketing-Modellnamen in Commits, PR-Titeln, Code-Kommentaren
  oder Repo-Artefakten. Nur im Chat.
- `gh` CLI ist nicht verfügbar — GitHub-Operationen über `mcp__github__*`-
  Tools.

---

## 4 · Sprachliche Konventionen (verbindlich)

- **Anführungszeichen**: durchgängig `‹…›` (U+2039 / U+203A).
  Niemals `„…"`, `"…"`, `«…»`, `»…«`, `'…'` oder ASCII `"`. Apostroph =
  ASCII `'`. Keine `<em>`/`<strong>` in den Daten.
- Sichtbarer Text läuft durch `lib/typografie.ts` (`tx(...)`) — die
  Datenpflege ist konform, der Renderer wendet nur leichte
  Typografie an.
- Antworten an den User in **Deutsch**, knapp, eher technisch-sachlich.
- Code-Kommentare sparsam, nur wenn das *Warum* nicht offensichtlich ist.
  Keine erklärenden Multi-Paragraph-Docstrings.

---

## 5 · Domänen-Wissen (kompakt)

Rudolf Steiner hielt vom 15. Februar bis 20. September 1924 die
„Klassenstunden" — die esoterische Schulung der Ersten Klasse der Freien
Hochschule. Vorgesehen waren 38 Stunden, gehalten wurden 38, überliefert
sind 30 Nachschriften.

Aufbau in der App:
- **19 Dornacher Hauptstunden** (`stunde-1` … `stunde-19`),
  zugehöriger Vortragstext in GA 270a (Stunden 1–9) und GA 270b
  (Stunden 10–19).
- **7 Wiederholungsstunden** im September 1924 (`wh-1` … `wh-7`),
  GA 270c.
- **4 Einzelstunden mit Nachschrift**: Prag 3.4. (`prag-1`), Prag 5.4.
  (`prag-2`), Bern 17.4. (`bern`), Notizen 2. Londoner Stunde 27.8.
  (`london-2`), alle GA 270c.
- **2 Breslauer Stunden** 12./13.6. (`breslau-1`, `breslau-2`),
  Sonderquelle Perseus Verlag Basel 2016 (Stenogramm Kolisko,
  Übertragung Gradenwitz). Zusätzlich ein **geschützter**
  `breslau-volltext` (Sprechwortlaut in eigener Nacherzählung, nicht
  zur Veröffentlichung).

Mantren-Korpus (App-Seiten unter `/mantren/<id>`):
- Vier Bögen (laut Mantrenbüchlein Basel 2024):
  - „Geschichte der Verwandlung 1–7" — App-IDs 1.1…7.3
  - „Leib in neuer Umgebung 8–10" — IDs 8 (mit erste-tafel separat),
    9.1, 9.2, 10
  - „Zusammenleben mit Hierarchien 11–16" — 11.1 … 16.2
  - „Kosmische Wesen bezeugen 17–19+" — 17, 18, 19.1, 19.2, 19.3, 19+
- Drei Tafel-Seiten (`erste-tafel`, `zweite-tafel`, `dritte-tafel`),
  Mantren in eigener Rubrik.
- Spezialseite `/2` = Strophe 2.1 „Erklärung der drei Tiere – Des
  dritten Tieres glasig Auge" (neu seit GA 270c-Apparat).

**Wandtafelzeichnungen** (GA 270i Tafelband): 13 Tafeln, alle in
`public/assets/tafeln/` als getrimmte JPEGs:
- Stunden 5, 6, 7, 8 (GA 270a)
- Stunden 10, 11, 12, 13, 14, 17 (GA 270b)
- wh-1, wh-6, wh-7 (GA 270c — wh-6 im Tafelband irrtümlich als ‹Zweite
  Wiederholungsstunde› bezeichnet; Editionsfehler in `quellen.json`
  dokumentiert)

**Quellen** (in `quellen.json`):
1. Mantrenbüchlein (Basel 2024) — primäre Ausgangsbasis (Titelei,
   Nummerierung, Gruppierung).
2. GA 270a — Manuskriptdruck 1977, Stunden 1–9.
3. GA 270b — Manuskriptdruck 1977, Stunden 10–19 + Apparat.
4. GA 270c — Manuskriptdruck 1977, Wiederholungs- und Einzelstunden.
5. GA 270i — Tafelband.
6. Breslau Perseus 2016 — Status `geschuetzt-nicht-freigegeben`
   (Editionsleistung urheberrechtlich geschützt; nur bibliografischer
   Nachweis + Steiners gemeinfreier Sprechwortlaut in Nacherzählung).
7. Finckh-Faksimiles (rudolfsteinerausgaben.com) — primäre
   Verifikationsquelle, frei zugängliche PDFs der
   Klartextnachschriften.
8. GA 270, 5. Auflage 2022 — maßgebliche Referenzausgabe, noch nicht
   systematisch eingearbeitet.
9. rsarchive.org — freie englische Online-Referenz.

**Rechtsstand** (recherchiert): Steiners Werk ist seit 31.12.1975 in der
Schweiz und über Art. 7 Abs. 8 RBÜ in Deutschland gemeinfrei
(LG München I, rkr.). Geschützt bleibt die *Editionsleistung* jeder
Ausgabe.

---

## 6 · Daten-Architektur

Drei JSON-Dateien in `src/data/` und eine YAML-Datei sind die einzige
Quelle der Wahrheit:

### `mantren.yaml`
Mantren-Verzeichnis (Kapitel + Mantren mit `parts: [{regie, section,
lines}]`). Wird in `lib/mantren.ts` als YAML eingelesen. **Bitte nicht
ohne Not anfassen** — die Reihenfolge bestimmt die Pager-Navigation und
die Index-Sortierung. Hier wohnen die *Steiner-Mantra-Texte selbst*.

### `vortraege.json`
Schlüssel = Pfad (`stunde-1`, `wh-3`, `prag-2`, `breslau-1` …).
Pro Vortrag:
```jsonc
{
  "titel": "Erste Stunde",
  "ort": "Dornach",
  "datum": "1924-02-15",
  "ga": "270a",
  "seiten": "21–40",
  "gruppe": "Geschichte der Verwandlung",  // bestimmt die Index-Gruppe
  "status": "geschuetzt-nicht-freigegeben", // optional, nur breslau-volltext
  "status_hinweis": "…",                   // Banner-Text
  "faksimile_url": "https://…/19240215-nachschrift.pdf",  // optional
  "faksimile_hinweis": "…",                // optional
  "abschnitte": [
    { "anker": "einleitung", "seite": "21", "typ": "text", "titel": "…", "text": "…" },
    { "anker": "m1", "seite": "24", "typ": "mantram", "titel": "…", "text": "…" },
    { "anker": "m1-deutung", "seite": "25", "typ": "deutung", "text": "…" },
    // typ ∈ text | mantram | wiederholung | deutung | tafelzeichnung | hinweis
  ],
  "tafelzeichnungen": []
}
```

### `mantren-kommentar.json`
Drei Top-Level-Sektionen: `_schema`, `meta`, `tafeln`, `strophen`.
`strophen` ist ein Dict mit Schlüsseln `1.1`, `1.2`, …, `19.1`, `2.1`
(45 Einträge). Pro Strophe (Kerntyp; siehe `lib/kommentar.ts`):
```jsonc
{
  "titel": "…",
  "incipit": "…",
  "rolle": "…",
  "vortrag": "stunde-1",          // optional, Deeplink-Ziel
  "anker": "m1",                  // optional, Deeplink-Ziel
  "quelle": { "ga": "270a", "stunde": "Erste Stunde", "ort": "Dornach", "datum": "…",
              "seiten": "…", "wiederholung_in_stunde": "…?", "anmerkung": "…?" },
  "parallelstellen": [{ "ref": "…", "art": "…?", "vortrag": "…?", "anker": "…?" }],
  "kerngedanken": { "kurz": "…", "kompakt": "…", "ausfuehrlich": ["…", "…"] },
  "zitate": [{ "text": "…", "quelle": "…" }],
  "tafelbild": { "bild": "assets/tafeln/…jpg", "vortrag": "…?", "anker": "…?",
                 "beschreibung": "…", "quelle": "…" },
  "varianten": { "prosa": "…?", "fassungen": [
    { "fassung": "GA 270c, …", "text": "…", "quelle": "…", "abweichung": "…" }
  ]},
  "editorische_hinweise": [{ "text": "…", "quelle": "…" }]
}
```

`varianten` und `editorische_hinweise` sind **additive** Felder seit
GA 270c; nicht jede Strophe hat sie. Mapping App-Pfad → Kommentar-IDs in
`src/lib/kommentar.ts` `MANTRA_TO_KEYS`.

### `quellen.json`
Strukturierter Apparat (Werk, Quellen[], Textgrundlage,
editorische_konventionen_webausgabe, ueberlieferung, rechtestatus,
weiterfuehrende_literatur, klassenstunden_uebersicht, bearbeitung,
mantren_register). Quellen tragen unterschiedliche Felder; Renderer
(`src/pages/quellen.astro`) ist **field-tolerant** — neue Felder einfach
in die `quelleFields`-Liste eintragen.

---

## 7 · Code-Architektur

```
src/
├── data/                       (Source of Truth, JSON+YAML)
├── lib/
│   ├── mantren.ts              Mantren + Kapitel + neighbours, rollingTitle
│   ├── kommentar.ts            Kommentar-Typen + MANTRA_TO_KEYS-Mapping
│   ├── vortraege.ts            Vortrag-Typen + vortraegePublic + isProtected
│   └── typografie.ts           tx(...) für ‹…›-Konvention
├── components/
│   ├── MantraView.astro        Mantra-Strophen + per-Part-Klappen
│   ├── KommentarKlappe.astro   Drei-Tiefen-Klappe + Apparat (Varianten/Hinweise)
│   └── LectureView.astro       Vortrag + TTS-Player + Faksimile-Link
├── layouts/
│   └── Base.astro              <head>, Topbar, Theme-Toggle, Tafel-Fullscreen,
│                               TTS-Klick-Handler, Pager-Verhalten, Swipe-Nav
├── pages/
│   ├── index.astro             Mantren-Index + Suche + Offline-Lader + Footer
│   ├── [id].astro              Dynamische Route: Mantra ODER Vortrag, je nach ID
│   ├── vortraege.astro         Vortrags-Index gruppiert + Suche
│   └── quellen.astro           Statische Quellen-/Impressums-Seite
└── styles/
    └── global.css              Alle Styles, kommentiert nach Sektionen
```

**Wichtige Erkenntnisse:**
- `pages/[id].astro` rendert *sowohl* Mantren als auch Vortrags-Seiten
  (Typ-Diskriminierung über `props.kind`). `getStaticPaths` summiert
  beide Arrays.
- Protected pages (`isProtected(v)`): `breslau-volltext` ist in
  `vortraege` enthalten (Route existiert), aber `vortraegePublic`
  filtert sie aus — kein Index-Eintrag, kein Pager-Nachbar, keine
  Suche. Nur per direkter URL erreichbar. Banner via
  `<aside class="protected-banner">` oben auf der Seite.
- Theme-Toggle, Tafel-Wegklapper, TTS-Voice-Pick alles via
  `localStorage`-Keys (`theme`, `mantren:tafel-vis`, `mantren:tts-voice`).
  Hell/Dunkel und Tafel-Pref werden im `<head>`-Inline-Skript schon
  *vor* dem ersten Paint angewendet, um FOUC zu vermeiden.

---

## 8 · UI-/Style-Erkenntnisse aus dem Chat

Was der User stilistisch akzeptiert / verworfen hat:

- **Schlicht, nicht aufgeräumt-clean.** Lieber zu wenig als zu viel.
  Keine Rahmen-Kästen, keine Filled-Icons (▶ ⏸ ■ war „nicht stimmig",
  ersetzt durch Textlinks „Vorlesen / Pause / Stopp").
- **Klapptitel grauer** (`var(--muted)`, nicht `var(--text)`).
- **Klappe braucht Luft.** `.klappe` hat `margin: 5rem 0 0;
  padding-top: 2rem` — vorher klebten Kurzmantren zu nah am Apparat.
- **Tafelbild auf Desktop bewusst groß.** Mantra-Seiten mit Tafel
  weiten `main` über `:has()` auf 1320 / 1480 px (statt 980). Tafel-
  Spalte hat ~ 1fr, Textspalte 34rem. Tafel ist per Button wegklappbar
  („Tafel ausblenden ›") und der Zustand bleibt erhalten.
- **TTS-Marker muss klar sichtbar sein.** Aktueller Stand: ▸-Pfeil
  links neben dem Abschnitt (pulsierend), 4 px Balken in Textfarbe,
  Hintergrund `rgba(127,127,127,0.13)` — funktioniert in beiden Modi.
- **Farben** kommen aus Variablen in `:root` und `.theme-invert`:
  `--bg`, `--text`, `--muted`, `--muted-soft`, `--line`, `--petrol`,
  `--petrol-soft`, `--input-bg`. Dunkelmodus hat *Sepia-Hauch*
  (`#d8d3c8` Text, `#37322d` Linien) statt blau-grau.

---

## 9 · Block-Prompt-Workflow

Der User liefert Inhalte als ZIP-Uploads mit einer festen Struktur:

```
<block>.zip
├── <thema>-prompt-<bezeichnung>.md   (Master-Prompt mit eingebetteten ```json-Blöcken)
├── vortraege.json                    (Standalone-Datei)
├── mantren-kommentar.json            (oft, manchmal nur im Prompt)
├── quellen.json
└── impressum.md                      (optionale Prosa-Variante)
```

**Vorgehen pro Block** (bisher: GA 270a/b/c, Breslau, plus Tafelbilder
für 270b/c):

1. Upload entpacken nach `/tmp/upload_<name>/`.
2. Master-Prompt lesen (Counts und sha256:16-Marker am Anfang).
3. Wenn Standalone-Dateien vorhanden: per `cp` nach `src/data/`.
   Wenn nur im Master-Prompt: Regex-Extraktion der ```json-Blöcke und
   per `Write`-Tool schreiben.
4. **Validieren**: für jeden Datei-Block Bytegröße + sha256:16 gegen
   den `<!-- sha256:16 = … -->`-Marker prüfen.
5. **Counts checken** wie im Prompt angegeben (z. B. 33 Vortragsseiten,
   45 Strophen, 9 Quellen).
6. **Code-Anbindung nachziehen** wenn neue Felder dabei sind:
   - `Vortrag`-Typ in `lib/vortraege.ts`
   - `Kommentar`-Typ in `lib/kommentar.ts`
   - `MANTRA_TO_KEYS` ergänzen falls neue App-Pfade
   - Renderer in `KommentarKlappe.astro`, `LectureView.astro`,
     `quellen.astro`
   - CSS-Klassen in `global.css`
7. `npm run build` — auf 73 → 76 Seiten achten.
8. Commit mit der *vom Prompt vorgegebenen* Message.
9. **Nicht pushen** — auf Bestätigung warten.

**Tafelbilder** (separater `assets-prompt-*.md`):
- Base64-Blöcke pro Datei, im Markdown unter `## Datei N — \`name\``.
- Ziel ist `public/assets/tafeln/` (nicht `assets/tafeln/`, das vom
  Prompt genannte Verzeichnis ist eine Vereinfachung).
- Python-Skript via Bash: Regex extrahieren → base64-decode → sha256-,
  Bytegröße- und Dimensions-Check → Write.
- Commit-Message exakt wie vom Prompt vorgegeben.

---

## 10 · Audio / TTS — Stand und Plan B

Aktuelle Implementierung: **Browser-`speechSynthesis`** (kostenlos), nur
am ersten Vortrag (`stunde-1`) als Test eingebaut, in
`LectureView.astro` via `is:inline`-Skript. Features:
- Stimmen-Picker mit `<optgroup>` „Deutsch (N) / andere Sprachen (M)",
  Default = beste lokale Stimme (Premium/Enhanced/Neural-Heuristik).
- Tempo-Slider 0.6–1.3.
- Chunkt nach `<section class="abschnitt">`, hebt aktuellen Abschnitt
  hervor, scrollt nur wenn nötig (`block: 'start'`).
- Chrome-Workaround alle 9 s `pause+resume` gegen 15-Sekunden-Abbruch.
- Speichert Auswahl in `localStorage` (`mantren:tts-voice`).

**Erkenntnis:** Browser-TTS klingt schlecht (iOS Safari hat nur eine
deutsche Stimme ohne Premium-Download). Workaround: User auf
Settings → Bedienungshilfen → Gesprochene Inhalte → Stimmen → Deutsch
verweisen, dort Premium-Stimmen laden lassen.

**Plan B (noch nicht umgesetzt)**: Cloud-TTS — ElevenLabs, Google
Neural2, Azure Neural, OpenAI TTS. Demo-URLs siehe Chatverlauf. Idee:
einmaliges Pre-Rendering aller Vorträge → MP3s im Repo, kein laufender
Cloud-Call. Kosten überschlägig 20–30 € einmalig. User testet die
Demos und entscheidet danach.

---

## 11 · Stand der App (Mai 2026)

- 76 statische Seiten in `dist/` (Mantren + alle Vortrags-IDs +
  index, vortraege, quellen).
- Datenbasis: 33 Vortragsseiten, 45 Strophen-Kommentare, 9 Quellen,
  13 Tafelbilder.
- PWA installierbar, Offline-Lader auf der Startseite („offline
  laden" → „offline bereit"); Manifest deckt alle Vortrags-IDs +
  `/quellen` mit ab.
- TTS-Test auf `/stunde-1`, sonst keine Audio-Features.
- Branch `claude/mantren-project-setup-KzVI1` ist gepusht und aktuell.

---

## 12 · Offene Punkte / Roadmap (siehe auch `TODO.md`)

- **Offline-Zugriff** ist nicht 100 % zuverlässig (siehe TODO §1).
  Verdacht auf Workbox-Manifest-Lücken bei Routen mit Sonderzeichen
  (`19+`, `7.1`), iOS-Safari-SW-Eviction.
- **Monetarisierung** (siehe TODO §2): Magiclink-Modell, Basis-
  Lizenz ~30 €, Module separat. Audio-Rezitationen sind aktuell der
  stärkste vermutete Zahlungsgrund.
- **GA 270, 5. Auflage 2022** als Quelle gelistet, aber inhaltlich
  noch nicht eingearbeitet (Hinweise/Tafeln/Varianten).
- **Suche** ist derzeit per-Seite (Mantren-Index und Vortrags-Index
  getrennt). Ein globaler Sucheinstieg fehlt.
- **Cloud-TTS** ausstehend (Plan B oben).

---

## 13 · Wie die nächste Session anfängt

1. `HANDOVER.md` und `TODO.md` lesen.
2. `git log -8 --oneline` für Kontext der letzten Commits.
3. Bei neuem ZIP-Upload: dem Block-Prompt-Workflow folgen (Abschnitt 9).
4. Bei UI-Änderungen: User mag schlichte Inline-Textlinks lieber als
   Buttons mit Rahmen. Immer `npm run build` zur Verifikation.
5. **Niemals** ohne ausdrückliche Bestätigung pushen. Der Stop-Hook
   erinnert, aber das ist kein Push-Befehl.
6. Antworten in Deutsch, knapp, sachlich. Code-Stellen im Format
   `file_path:line_number` referenzieren.
