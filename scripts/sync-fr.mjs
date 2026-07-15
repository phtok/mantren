#!/usr/bin/env node
// Faltet Louis' in Supabase gespeicherte Übersetzungs-Fassungen zurück in die
// statische src/data/uebersetzung-fr.json (Archiv- und Offline-Grundlage).
// Danach die Änderung prüfen, committen und deployen.
//
// Liest öffentlich (RLS erlaubt anon select) — kein Geheimnis nötig.
// Aufruf:  node scripts/sync-fr.mjs   (oder: npm run sync:fr)
// Braucht direkten Netzzugang zu supabase.co.
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const URL_BASE = 'https://dagcsnfrlbpxcmdimnrw.supabase.co';
const ANON = 'sb_publishable_SXhY0mrhXjdTnjbJ5Uobtg_zAXW_xGY';
const TABLE = 'mantren_uebersetzung_fr';

const DATA = resolve(dirname(fileURLToPath(import.meta.url)), '../src/data/uebersetzung-fr.json');

const res = await fetch(
  `${URL_BASE}/rest/v1/${TABLE}?select=mantra_id,fassung,aktualisiert&order=mantra_id`,
  { headers: { apikey: ANON, Authorization: `Bearer ${ANON}` } },
);
if (!res.ok) {
  console.error('Fehler beim Laden aus Supabase:', res.status, await res.text());
  process.exit(1);
}
const rows = await res.json();
if (!rows.length) {
  console.log('Keine Fassungen in der Datenbank — nichts zu übernehmen.');
  process.exit(0);
}

const j = JSON.parse(readFileSync(DATA, 'utf8'));
const geaendert = [];
for (const row of rows) {
  const bloc = row.fassung && row.fassung.bloc;
  if (!Array.isArray(bloc)) continue;
  // Eine bearbeitete Fassung ersetzt den bisherigen Eintrag als durchgehender
  // Block (so, wie Louis sie im Editor eingibt).
  j.mantren[row.mantra_id] = { bloc };
  geaendert.push(row.mantra_id);
}

writeFileSync(DATA, JSON.stringify(j, null, 2) + '\n');
console.log(`${geaendert.length} Fassung(en) übernommen: ${geaendert.join(', ')}`);
console.log('Bitte die Änderung prüfen (git diff), dann committen und deployen.');
