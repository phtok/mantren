# Konzept — Funktion für die Übersetzerin

*Notizbuch · Übersetzungs-Werkbank · Parallelvarianten*

Stand: 2026-06-04 · Entwurf zur Diskussion · **noch nichts umgesetzt**

---

## 1. Worum es geht

Mantren ist heute eine rein **statische, offline-fähige Lese-Ausgabe** (Astro →
GitHub Pages, PWA). Aller Nutzerzustand lebt im `localStorage` (Theme,
Schriftbild, Tafel-Sichtbarkeit) — es gibt keinen Server, kein Konto, keine
Anmeldung.

Die gewünschte Funktion bricht mit dieser Annahme. Sie ist **kein Lese-Feature**,
sondern eine **Arbeitsumgebung für eine Übersetzerin**, die über Jahre hinweg im
Umgang mit den Mantren eine Übersetzung in ihre Sprache entwickelt. Drei
Bausteine, die zusammengehören:

1. **Notizbuch** — freie Notizen, pro Mantra und als Sammelstelle.
2. **Übersetzungs-Werkbank** — eigene Übersetzung eingeben und über die Zeit in
   Varianten weiterentwickeln.
3. **Parallelvarianten** — Fassungen synoptisch nebeneinander vergleichen
   (mobil: zwischen ihnen wischen).

Entscheidend ist die im Rückgespräch geschärfte Anforderung:

> Die Übersetzung bleibt **in Arbeit**, sie entwickelt sich über Jahre. Das
> Werkzeug muss **hinter einem Login** leben. Die Übersetzende darf je **eine
> Variante freischalten** — für alle Lesenden in ihrer Sprache, mit
> **Autorinnenvermerk**.

Daraus folgen drei tragende Konsequenzen, die dieses Konzept durchziehen:

- **Dauerhaftigkeit.** Die Arbeit muss Jahre überdauern, geräteübergreifend, und
  darf nicht an `localStorage` hängen (Cache-Löschung, Gerätewechsel = Verlust).
  → Server-Persistenz hinter Login.
- **Evolution statt Endstand.** Nicht „die Übersetzung", sondern ein wachsender
  Bestand aus Varianten und Zwischenständen. Das Notizbuch ist Teil dieses
  Werdens, kein Beiwerk.
- **Zwei Welten, sauber getrennt.** Die private Werkbank (dynamisch, angemeldet)
  und die öffentliche Lese-Ausgabe (statisch, anonym, archivisch) bleiben
  getrennt. Veröffentlichen ist die kontrollierte Brücke dazwischen.

---

## 2. Nutzer:innen und Rollen

| Rolle | Zugang | Sieht / kann |
|---|---|---|
| **Lesende** | anonym, kein Login | die öffentliche Ausgabe; zusätzlich **freigeschaltete** Übersetzungen je Sprache (mit Autorinnenvermerk) |
| **Übersetzende** | Login | eigene Werkbank für **ihre** Sprache: Notizbuch, eigene Varianten, Historie, Vergleich; darf je Sprache **eine** Variante freischalten |
| **Herausgeber** (Philipp) | Login | vergibt Übersetzer-Zugänge pro Sprache; sieht/verwaltet Freischaltungen; redaktionelle Aufsicht |

Wichtig: Lesende bekommen **nie** ein Login aufgedrängt. Die öffentliche Ausgabe
bleibt so frei, schlank und offline-fähig wie heute. Login ist ausschließlich die
Tür zur Werkbank.

---

## 3. Die drei Bausteine

### 3.1 Notizbuch

Zweck: ein Arbeitsjournal im Umgang mit den Mantren — Beobachtungen,
Wortfindungen, Fragen, Querbezüge.

- **Inline pro Mantra.** Auf jeder Mantra-Seite ein aufklappbares Notizfeld
  (analog zur bestehenden `KommentarKlappe`), gebunden an die Mantra-ID und
  optional an eine Strophe/Zeile. Bewusst nah am Text, im selben Lesefluss.
- **Sammelseite `/notizbuch/`.** Alle Notizen der Übersetzenden an einem Ort,
  chronologisch und nach Mantra gefiltert, durchsuchbar (die bestehende
  Universalsuche ist ein gutes Vorbild). Von hier **Export** (Download als
  Markdown/JSON) — Datenhoheit bei der Übersetzerin.
- Notizen sind **immer privat**; sie werden nie mit veröffentlicht.

Anknüpfung im Code: Aufklapp-Muster und Persistenz-Konventionen existieren
bereits (`KommentarKlappe.astro`, `localStorage`-Präferenzen in `Base.astro`).
Neu ist nur, dass der Inhalt server-seitig und pro Konto liegt.

### 3.2 Übersetzungs-Werkbank

Das Herzstück. Die Übersetzerin gibt ihre Übersetzung **parallel zum Original**
ein — strukturiert wie der Korpus selbst:

- Gliederung folgt dem Datenmodell: pro **Mantra** → **Strophe (part)** →
  **Zeile**. So bleibt die Übersetzung Zeile für Zeile am Original ausgerichtet
  (vgl. `Part.lines` in `src/lib/mantren.ts`).
- Eine **Variante** ist eine vollständige alternative Wiedergabe. Die Übersetzerin
  hält **mehrere** Varianten nebeneinander (z. B. „wörtlich", „klanglich",
  „Fassung 2026") und entwickelt sie weiter.
- **Evolution / Historie.** Weil die Arbeit über Jahre läuft, werden
  Zwischenstände als datierte Schnapshots gehalten. Die Übersetzerin kann
  zurückblättern — die Werkbank ist zugleich Werkstatt und Gedächtnis. Das
  verbindet sie eng mit dem Notizbuch (3.1).
- **Status je Variante:** Entwurf → in Arbeit → reif → *freigeschaltet*. Nur
  genau eine pro Sprache kann freigeschaltet sein (siehe 4).

Wir können die vorhandene Form `VarianteFassung` (`src/lib/kommentar.ts`)
konzeptionell weiterverwenden — Steiners Fassungen und die Übersetzer-Varianten
teilen sich dieselbe Grundgestalt (Name, Text, Quelle/Vermerk, Anker).

### 3.3 Parallelvarianten (synoptisch, mobil-wischbar)

Hier laufen **zwei Bedeutungen** von „Variante" zusammen — und das ist Absicht:

1. **Steiners Fassungen** — die im Apparat bereits gepflegten Lesarten
   (`varianten.fassungen` in `mantren-kommentar.json`, heute als Liste in der
   Klappe gerendert).
2. **Die Varianten der Übersetzerin** — ihre eigenen Wiedergaben und
   Zwischenstände aus 3.2. *Diese* sind ihr auf lange Sicht am wichtigsten.

Beide werden in **einer synoptischen Ansicht** vergleichbar, **Strophe für
Strophe ausgerichtet**:

- **Desktop:** Spalten nebeneinander — z. B. Original | Steiner-Fassung B |
  Übersetzer-Variante „wörtlich" | Übersetzer-Variante „klanglich".
- **Mobil:** eine Spalte sichtbar, **nach links/rechts wischen** wechselt die
  Variante (eine Karte pro Variante). Das Wisch-Muster gibt es schon — der
  Seiten-Pager in `Base.astro` nutzt `touchstart/touchend`; dieselbe Mechanik
  lässt sich auf den Variantenwechsel übertragen.
- Welche Spalten/Karten gezeigt werden, ist wählbar (Original an/aus, welche
  Fassungen, welche eigenen Varianten).

Auf der **öffentlichen** Seite ist dieselbe Synopse die natürliche Heimat der
freigeschalteten Übersetzung: Lesende sehen Original neben der veröffentlichten
Übersetzung ihrer Sprache.

---

## 4. Veröffentlichen & Autorinnenvermerk

Der bewusste Übergang von privat zu öffentlich:

- Die Übersetzende wählt **genau eine** ihrer Varianten und schaltet sie für ihre
  Sprache **frei**. Erneutes Freischalten **ersetzt** die vorige; die alte bleibt
  als Stand in der Historie erhalten (nichts geht verloren).
- Jede Freischaltung trägt einen **Autorinnenvermerk** (Name/Kürzel, optional
  kurzer Vermerk, Datum, ggf. Lizenz). Er erscheint bei den Lesenden an der
  veröffentlichten Übersetzung.
- **Pro Sprache eine** freigeschaltete Fassung zur Zeit. Mehrere Sprachen
  nebeneinander sind möglich (je eigene:r Übersetzer:in).
- Notizen und nicht freigeschaltete Varianten bleiben **privat**.

Offene Frage zur Form der Veröffentlichung — zwei Wege (siehe 5):
- **(A) In den Korpus zurückschreiben:** Freischalten erzeugt einen Eintrag in
  den Daten (`src/data/…`) → normaler Build/Deploy. Die öffentliche Ausgabe
  bleibt damit *vollständig statisch, offline-fähig und archivisch* — passt zum
  Charakter des Projekts. Trade-off: Freischalten ist kein Sofort-Effekt, sondern
  läuft über einen Build (z. B. automatischer Commit/PR + Deploy).
- **(B) Zur Laufzeit ausliefern:** Die öffentliche Seite holt freigeschaltete
  Übersetzungen dynamisch. Sofort sichtbar, aber bricht mit „rein statisch" und
  erschwert echtes Offline.

**Empfehlung: (A).** Es erhält die Werte des Projekts (frei, ohne Tracking,
offline, dauerhaft) und hält die öffentliche Ausgabe sauber. Die Latenz beim
Freischalten ist für ein über Jahre wachsendes Werk unkritisch.

---

## 5. Architektur — Login & Persistenz (der eigentliche Schritt)

### 5.1 Leitbild: zwei Schichten

```
┌─────────────────────────────────────────────┐
│  ÖFFENTLICH  — statisch, anonym, offline      │
│  Astro/GitHub Pages (wie heute)               │
│  + freigeschaltete Übersetzungen je Sprache   │
└───────────────▲───────────────────────────────┘
                │  Freischalten (Brücke, kontrolliert)
┌───────────────┴───────────────────────────────┐
│  WERKBANK  — dynamisch, hinter Login           │
│  Notizbuch · eigene Varianten · Historie       │
│  · Vergleich · Export                          │
│  (Auth + Datenbank, z. B. Supabase)            │
└─────────────────────────────────────────────┘
```

Die öffentliche Schicht bleibt im Kern, was sie ist. Die Werkbank kommt als
**eigener, angemeldeter Bereich** hinzu (eigene Route, z. B. `/werkbank/`, oder
separates kleines Frontend). Veröffentlichen ist die einzige, kontrollierte
Verbindung.

### 5.2 Backend-Option

Ein **Backend-as-a-Service** passt hier gut, weil es Auth + Datenbank +
Zeilen-genaue Zugriffsregeln + Export ohne eigenen Serverbetrieb mitbringt.
**Supabase** (Postgres + Auth + Row-Level-Security) ist der naheliegende
Kandidat — in dieser Arbeitsumgebung war ein Supabase-Connector sogar bereits
angebunden. Alternativen: ein kleiner eigener Dienst, oder Git-basiert (jede
Speicherung = Commit) — letzteres elegant für die Historie, aber zu schwergängig
für tägliches Notieren.

Auth: E-Mail-Magic-Link genügt (kein Passwort-Handling), wenige Konten.

### 5.3 Datenmodell (Skizze)

```
uebersetzer        (id, name, sprache, vermerk_default, rolle)
notiz              (id, autor, mantra_id, strophe?, zeile?, text, erstellt, geaendert)
variante           (id, autor, sprache, name, status, erstellt, geaendert)
variante_text      (variante_id, mantra_id, strophe, zeile, text)   ← Zeilenraster
variante_snapshot  (id, variante_id, stand_json, datum)             ← Historie
freischaltung      (sprache, variante_id, autor_vermerk, datum)     ← je Sprache eine
```

- Das **Zeilenraster** (`mantra_id/strophe/zeile`) spiegelt `Part.lines` und hält
  Original und Übersetzung deckungsgleich für die Synopse.
- **Zugriffsregeln:** Übersetzende sehen/ändern nur ihre eigenen Zeilen; nur
  `freischaltung`-Inhalte fließen nach öffentlich.
- **Snapshots** tragen die „über Jahre"-Anforderung.

### 5.4 Auswirkungen auf das Bestehende

- **Offline/PWA:** öffentliche Seite unverändert offline-fähig. Die Werkbank
  braucht online (sinnvoll: lokaler Entwurfspuffer + Sync, damit unterwegs nichts
  verloren geht).
- **Datenschutz:** Projekt ist betont tracking-frei (`robots: noai,noimageai`,
  selbstgehostete Fonts). Login-Bereich muss das fortführen: nur funktionale
  Daten, keine Analytik, klarer Export/Löschpfad.
- **Build/Deploy:** bei Weg (A) ein Schritt „freigeschaltete Übersetzungen →
  Datendatei → Deploy" (vgl. bestehender Workflow `.github/workflows/deploy.yml`).

---

## 6. Leseseite mit Sprachen

- **Sprachwahl** (analog zum bestehenden Schriftbild-/Theme-Umschalter im
  ⋯-Menü). Auswahl bleibt im `localStorage`.
- Ist für die gewählte Sprache eine Übersetzung freigeschaltet, erscheint sie in
  der **Synopse** neben dem Original (3.3) — mit **Autorinnenvermerk**.
- Ohne Freischaltung: alles wie heute, nur Original. Keine leeren Hüllen.

---

## 7. Datenschutz, Offline, Datenhoheit

- **Privat by default:** Notizen und Entwürfe verlassen die Werkbank nie ohne
  bewusste Freischaltung.
- **Export jederzeit:** vollständiger Download aller eigenen Inhalte
  (Notizbuch + Varianten + Historie) als Markdown/JSON.
- **Kein Tracking** im Login-Bereich, im Geist der öffentlichen Ausgabe.
- **Eigentum:** die Übersetzerin behält die Rechte; der Autorinnenvermerk macht
  Urheberschaft sichtbar. Lizenzfrage pro Freischaltung klären.

---

## 8. Phasenplan (Vorschlag)

1. **Notizbuch, lokal.** Inline-Notizfeld + Sammelseite + Export, vorerst
   `localStorage`. Sofort nützlich, kein Backend, kein Risiko. Validiert die UX.
2. **Synopse / Parallelvarianten.** Vergleichsansicht (Desktop-Spalten,
   Mobil-Wischen) zunächst nur für Steiners vorhandene Fassungen. Rein
   Frontend, statisch.
3. **Login + Werkbank.** Auth + Datenbank; Notizbuch und eigene Varianten
   wandern server-seitig (Migration aus 1). Historie/Snapshots.
4. **Freischalten + Leseseite mit Sprachen.** Veröffentlichungs-Brücke (Weg A),
   Autorinnenvermerk, Sprachwahl für Lesende.

Phasen 1–2 liefern früh Wert und sind reversibel; der schwere Schnitt (Login,
Persistenz) kommt erst, wenn die Form steht.

---

## 9. Offene Entscheidungen

- **Backend:** Supabase oder Alternative? Self-hosted vs. gehostet?
- **Veröffentlichungsweg:** (A) zurück in den statischen Korpus *(empfohlen)* vs.
  (B) Laufzeit-Auslieferung.
- **Granularität der Synopse:** Ausrichtung pro Strophe genügend, oder Zeile für
  Zeile?
- **Mehrsprachigkeit:** wie viele Sprachen/Übersetzer:innen absehbar? Eine pro
  Sprache, oder mehrere konkurrierende Fassungen je Sprache?
- **Lizenz** der freigeschalteten Übersetzungen.
- **Notiz-Bindung:** nur pro Mantra, oder auch pro Strophe/Zeile?

---

*Dieses Dokument beschreibt das Konzept. Implementiert ist noch nichts.*
