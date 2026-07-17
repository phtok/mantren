#!/usr/bin/env node
// Exportiert sämtliche Inhalte der Webapp in ein einzelnes, maschinen- und
// KI-lesbares Markdown-Dokument (export/mantren-webapp-volltext.md).
// Aufruf: node scripts/export-textdokument.mjs

import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import YAML from 'yaml';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const data = (f) => join(root, 'src', 'data', f);
const json = (f) => JSON.parse(readFileSync(data(f), 'utf8'));

const mantren = YAML.parse(readFileSync(data('mantren.yaml'), 'utf8'));
const vortraege = json('vortraege.json');
const kommentar = json('mantren-kommentar.json');
const glossar = json('glossar.json');
const onboarding = json('onboarding.json');
const quellen = json('quellen.json');
const fr = json('uebersetzung-fr.json');
const nomsDivins = json('noms-divins.json');

const out = [];
const w = (...lines) => out.push(...lines);

const label = (k) =>
  k
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());

// Generischer Renderer für verschachtelte JSON-Strukturen (Quellen-Apparat u. Ä.)
function renderValue(value, depth = 0) {
  const indent = '  '.repeat(depth);
  if (value == null) return;
  if (typeof value === 'string' || typeof value === 'number') {
    w(`${indent}${value}`, '');
  } else if (Array.isArray(value)) {
    for (const item of value) {
      if (item && typeof item === 'object' && !Array.isArray(item)) {
        const entries = Object.entries(item).filter(([, v]) => v != null);
        w(`${indent}- ${entries.map(([k, v]) => `**${label(k)}:** ${typeof v === 'object' ? JSON.stringify(v) : v}`).join(' · ')}`);
      } else {
        w(`${indent}- ${item}`);
      }
    }
    w('');
  } else if (typeof value === 'object') {
    for (const [k, v] of Object.entries(value)) {
      if (k.startsWith('_') || v == null) continue;
      if (typeof v === 'string' || typeof v === 'number') {
        w(`${indent}- **${label(k)}:** ${v}`);
      } else {
        w(`${indent}- **${label(k)}:**`);
        renderValue(v, depth + 1);
      }
    }
    w('');
  }
}

// ───────────────────────────── Kopf ─────────────────────────────
w(
  '# Mantren — Rudolf Steiners mantrisches Spätwerk',
  '',
  '**Gesamtexport aller Inhalte der Web-App** <https://phtok.github.io/mantren/>',
  '',
  `Exportiert am ${new Date().toISOString().slice(0, 10)} aus den Inhaltsquellen der App (\`src/data/\`).`,
  'Dieses Dokument enthält den vollständigen Textbestand der Webapp: die Lesefassung',
  'der Klassenmantren (Mantrenbüchlein Basel 2024), die Vortragsfassungen der',
  'Klassenstunden (GA 270a/b/c sowie Breslau), den Kommentar zu den Mantren, das',
  'Glossar, die Einführung, die Quellen- und editorische Notiz, die französische',
  'Übersetzung (Arbeitsstand) samt Apparat sowie das Impressum.',
  '',
  '## Inhaltsverzeichnis',
  '',
  '1. Einführung (Onboarding)',
  '2. Die Mantren — Lesefassung des Korpus 1924',
  '3. Die Klassenstunden — Vortragsfassungen',
  '4. Kommentar zu den Mantren',
  '5. Glossar',
  '6. Quellen und editorische Notiz',
  '7. Französische Übersetzung der Mantren (Arbeitsstand)',
  '8. Noms divins — französischer Apparat der Hierarchien-Namen',
  '9. Impressum',
  '',
  '---',
  ''
);

// ─────────────────────── 1. Einführung ───────────────────────
w('# 1. Einführung (Onboarding)', '');
if (onboarding.hinweis) w(`> ${onboarding.hinweis}`, '');
for (const b of onboarding.bildschirme) {
  w(`## ${b.nr}. ${b.titel}`, '');
  if (b.lead) w(`*${b.lead}*`, '');
  if (b.text) w(b.text, '');
}
w('---', '');

// ─────────────────────── 2. Mantren ───────────────────────
w('# 2. Die Mantren — Lesefassung des Korpus 1924', '');
w(
  'Quelle: GA 270, 4. Auflage 2020. Lesefassung von Bodo von Plato, Elke Schmitter',
  'und Anke Steinmetz, Berlin Februar 2024 (Mantrenbüchlein Basel 2024).',
  '',
  'Kapitelgliederung des Korpus:',
  ''
);
for (const c of mantren.chapters) {
  w(`- ${c.title}${c.range ? ` (Stunden ${c.range})` : ''}`);
}
w('');
const chapterTitle = Object.fromEntries(mantren.chapters.map((c) => [c.id, c.title]));
let currentChapter = null;
for (const m of mantren.mantren) {
  if (m.chapter !== currentChapter) {
    currentChapter = m.chapter;
    w(`## ${chapterTitle[currentChapter] ?? currentChapter}`, '');
  }
  const heading = m.title
    ? `${m.number ? `${m.number} — ` : ''}${m.title}`
    : `Mantra ${m.number || m.id}`;
  w(`### ${heading}`, '');
  for (const part of m.parts ?? []) {
    if (part.section) w(`**${part.section}**`, '');
    if (part.regie) w(`*${part.regie}*`, '');
    if (part.lines) {
      for (const line of part.lines) {
        const indented = line.startsWith('/');
        const text = indented ? line.slice(1) : line;
        w(`${indented ? '&nbsp;&nbsp;&nbsp;&nbsp;' : ''}${text}  `);
      }
      w('');
    }
  }
}
w('---', '');

// ─────────────────── 3. Klassenstunden ───────────────────
w('# 3. Die Klassenstunden — Vortragsfassungen', '');
w(
  'Vortragstexte aus GA 270a/b/c (Dornacher Stunden, Wiederholungsstunden,',
  'Einzelstunden Prag/Bern/London) sowie die Breslauer Stunden. Seitenangaben',
  'beziehen sich auf die jeweilige GA-Druckausgabe.',
  ''
);
for (const [id, v] of Object.entries(vortraege)) {
  if (id.startsWith('_')) continue;
  const meta = [v.ort, v.datum, v.ga ? `GA ${v.ga}` : null, v.seiten ? `S. ${v.seiten}` : null]
    .filter(Boolean)
    .join(' · ');
  w(`## ${v.titel} [${id}]`, '');
  if (meta) w(`*${meta}*${v.gruppe ? ` — Gruppe: ${v.gruppe}` : ''}`, '');
  if (v.beschreibung) w(v.beschreibung, '');
  for (const a of v.abschnitte ?? []) {
    const typ = a.typ && a.typ !== 'text' ? ` (${a.typ})` : '';
    if (a.titel) w(`### ${a.titel}${typ}`, '');
    else if (typ) w(`### Abschnitt${typ}`, '');
    if (a.seite) w(`*[S. ${a.seite}]*`, '');
    if (a.typ === 'mantram' || a.typ === 'tafeltext') {
      // Verszeilen als Zeilen erhalten
      for (const line of (a.text ?? '').split('\n')) w(line === '' ? '' : `${line}  `);
      w('');
    } else if (a.text) {
      w(a.text, '');
    }
    if (a.bild) w(`![${a.alt ?? 'Tafelzeichnung'}](${a.bild})`, '');
    else if (a.alt) w(`*Bildbeschreibung: ${a.alt}*`, '');
    if (a.quelle) w(`*Quelle: ${typeof a.quelle === 'string' ? a.quelle : JSON.stringify(a.quelle)}*`, '');
  }
}
w('---', '');

// ─────────────────── 4. Kommentar ───────────────────
w('# 4. Kommentar zu den Mantren', '');
if (kommentar.meta) {
  w('## Werkangaben', '');
  renderValue(kommentar.meta);
}

function renderKommentarEintrag(key, e) {
  w(`## ${key} — ${e.titel ?? ''}`, '');
  if (e.incipit) w(`*Incipit: ${e.incipit}*`, '');
  if (e.rolle) w(`**Rolle:** ${e.rolle}`, '');
  if (e.vortrag) w(`**Vortrag:** ${e.vortrag}${e.anker ? ` (Anker: ${e.anker})` : ''}`, '');
  w('');
  if (e.quelle) {
    w('### Quelle', '');
    renderValue(e.quelle);
  }
  if (e.kerngedanken) {
    w('### Kerngedanken', '');
    for (const [variant, text] of Object.entries(e.kerngedanken)) {
      w(`**${label(variant)}:** ${text}`, '');
    }
  }
  if (e.zitate?.length) {
    w('### Zitate', '');
    for (const z of e.zitate) {
      w(`> ${z.text}`, '>', `> — ${z.quelle}${z.vortrag ? ` (${z.vortrag}${z.anker ? `#${z.anker}` : ''})` : ''}`, '');
    }
  }
  if (e.parallelstellen?.length) {
    w('### Parallelstellen', '');
    for (const p of e.parallelstellen) {
      w(`- ${p.ref}${p.art ? ` — *${p.art}*` : ''}`);
    }
    w('');
  }
  if (e.tafelbild) {
    w('### Tafelbild', '');
    renderValue(e.tafelbild);
  }
  if (e.varianten) {
    w('### Varianten', '');
    if (typeof e.varianten === 'string') w(e.varianten, '');
    else if (e.varianten.prosa) w(e.varianten.prosa, '');
    else renderValue(e.varianten);
  }
  if (e.editorische_hinweise?.length) {
    w('### Editorische Hinweise', '');
    for (const h of e.editorische_hinweise) {
      if (typeof h === 'string') w(`- ${h}`);
      else w(`- ${h.text}${h.quelle ? ` *(${h.quelle})*` : ''}`);
    }
    w('');
  }
}

for (const [key, e] of Object.entries(kommentar.tafeln ?? {})) renderKommentarEintrag(key, e);
for (const [key, e] of Object.entries(kommentar.strophen ?? {})) renderKommentarEintrag(key, e);
w('---', '');

// ─────────────────── 5. Glossar ───────────────────
w('# 5. Glossar', '');
if (glossar.hinweis) w(`> ${glossar.hinweis}`, '');
if (glossar.stand) w(`*Stand: ${glossar.stand}*`, '');
for (const e of glossar.eintraege) {
  w(`## ${e.begriff}`, '');
  if (e.auch?.length) w(`*Auch: ${e.auch.join(', ')}*`, '');
  if (e.kurz) w(e.kurz, '');
  if (e.lang) w(e.lang, '');
  if (e.siehe?.length) w(`Siehe auch: ${e.siehe.join(', ')}`, '');
}
w('---', '');

// ─────────────────── 6. Quellen ───────────────────
w('# 6. Quellen und editorische Notiz', '');
for (const [k, v] of Object.entries(quellen)) {
  if (k.startsWith('_')) continue;
  w(`## ${label(k)}`, '');
  renderValue(v);
}
w('---', '');

// ─────────────────── 7. Französische Übersetzung ───────────────────
w('# 7. Französische Übersetzung der Mantren (Arbeitsstand)', '');
if (fr._hinweis) w(`> ${fr._hinweis}`, '');
if (fr.uebersetzerin) w(`**Übersetzung:** ${fr.uebersetzerin}`, '');
w('');
const deTitel = Object.fromEntries(
  mantren.mantren.map((m) => [m.id, m.title ? `${m.number ? `${m.number} — ` : ''}${m.title}` : `Mantra ${m.number || m.id}`])
);
for (const [id, m] of Object.entries(fr.mantren ?? {})) {
  const de = deTitel[id] ? ` (dt.: ${deTitel[id]})` : '';
  w(`## ${m.titel ?? id}${de} [${id}]`, '');
  for (const s of m.strophen ?? []) {
    if (typeof s === 'string') {
      for (const line of s.split('\n')) w(`${line}  `);
      w('');
    } else if (Array.isArray(s)) {
      for (const line of s) w(`${line}  `);
      w('');
    } else if (s?.lines) {
      if (s.regie) w(`*${s.regie}*`, '');
      for (const line of s.lines) w(`${line}  `);
      w('');
    } else if (s && typeof s === 'object') {
      renderValue(s);
    }
  }
}
w('---', '');

// ─────────────────── 8. Noms divins ───────────────────
w(`# 8. ${nomsDivins.titel ?? 'Noms divins'}`, '');
if (nomsDivins.untertitel) w(`*${nomsDivins.untertitel}*`, '');
if (nomsDivins._hinweis) w(`> ${nomsDivins._hinweis}`, '');
w('');
for (const t of nomsDivins.triaden ?? []) {
  w(`## ${t.triade}`, '');
  for (const r of t.range ?? []) {
    w(`### ${r.latin}`, '');
    if (r.grec) w(`- **Nom grec:** ${r.grec}`);
    if (r.steiner) w(`- **Chez Steiner:** ${r.steiner}`);
    if (r.sens) w(`- **Sens:** ${r.sens}`);
    w('');
  }
}
w('---', '');

// ─────────────────── 9. Impressum ───────────────────
w(
  '# 9. Impressum',
  '',
  '**Projekt:** Mantren — Rudolf Steiners mantrisches Spätwerk. Eine nichtkommerzielle',
  'Web-Ausgabe der Klassenmantren der Freien Hochschule für Geisteswissenschaft am Goetheanum.',
  '',
  '**Herausgabe:** Philipp Tok, Dornach / Basel. Kontakt: philipp@saetzerei.com',
  '',
  '**Übersetzung:** Französische Übersetzung der Mantren: Louis Defèche. Die Rechte an',
  'der Übersetzung liegen bei ihm; sie wird hier als Arbeitsstand mit seinem',
  'Einverständnis wiedergegeben.',
  '',
  '**Inhalte und Rechte:** Werknachweis, Textgrundlage und Rechtestatus sind auf der',
  'Quellenseite ausgewiesen (Abschnitt 6 dieses Dokuments).',
  '',
  '**Haftung:** Die Inhalte werden mit Sorgfalt erstellt, jedoch ohne Gewähr für',
  'Vollständigkeit und Richtigkeit. Für Inhalte verlinkter externer Seiten sind deren',
  'Betreiber verantwortlich.',
  ''
);

const outDir = join(root, 'export');
mkdirSync(outDir, { recursive: true });
const outFile = join(outDir, 'mantren-webapp-volltext.md');
writeFileSync(outFile, out.join('\n'), 'utf8');
console.log(`Geschrieben: ${outFile} (${(out.join('\n').length / 1024).toFixed(0)} KB)`);
