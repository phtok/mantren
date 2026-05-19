import kommentarRaw from '../data/mantren-kommentar.json';
import type { Mantra } from './mantren';

export type Quelle = {
  ga: string;
  stunde: string;
  ort: string;
  datum: string;
  seiten: string;
  wiederholung_in_stunde?: string | null;
  anmerkung?: string | null;
};

export type Kerngedanken = {
  kurz: string;
  kompakt: string;
  ausfuehrlich: string[];
};

export type Zitat = {
  text: string;
  quelle: string;
};

export type Parallelstelle = {
  ref: string;
  art?: string;
  vortrag?: string | null;
  anker?: string | null;
};

export type Tafelbild = {
  bild: string;
  vortrag?: string | null;
  anker?: string | null;
  beschreibung: string;
  quelle: string;
};

export type Kommentar = {
  titel?: string;
  incipit?: string;
  rolle?: string;
  vortrag?: string | null;
  anker?: string | null;
  quelle: Quelle;
  parallelstellen?: Parallelstelle[];
  kerngedanken: Kerngedanken;
  zitate?: Zitat[];
  tafelbild?: Tafelbild;
};

type KommentarLike = Kommentar | { status?: string };

type Source = {
  _schema?: unknown;
  meta?: unknown;
  strophen?: Record<string, KommentarLike>;
  tafeln?: Record<string, KommentarLike>;
};

const source = kommentarRaw as Source;

function isComplete(c: KommentarLike | undefined): c is Kommentar {
  if (!c || typeof c !== 'object') return false;
  const k = c as Kommentar;
  return !!(k.kerngedanken && k.quelle && (k.kerngedanken.kurz || k.kerngedanken.kompakt || (k.kerngedanken.ausfuehrlich && k.kerngedanken.ausfuehrlich.length)));
}

// Mantra-Seite (App-ID) → geordnete Kommentar-Schlüssel.
// - Länge 1: eine Klappe für die ganze Seite.
// - Länge > 1: eine Klappe je Strophe in der Reihenfolge der parts.
// /mantren/erste-tafel rendert den Weltenwort-Kommentar 8.1.
// /mantren/8 hat in der App 3 Strophen (Sieh hinter/in/über) → 8.2/8.3/8.4;
//   8.1 (Weltenwort) gehört zur App-Seite erste-tafel.
const MANTRA_TO_KEYS: Record<string, string[]> = {
  '1.1': ['1.1'],
  '1.2': ['1.2'],
  '1.3': ['1.3'],
  '1.4': ['1.4'],
  '3': ['3.1', '3.2', '3.3'],
  '4': ['4.1', '4.2', '4.3'],
  '5': ['5.1', '5.2', '5.3'],
  '6': ['6.1', '6.2', '6.3', '6.4', '6.5', '6.6'],
  '7.1': ['7.1'],
  '7.2': ['7.2'],
  '7.3': ['7.3'],
  '8': ['8.2', '8.3', '8.4'],
  '9.1': ['9.1'],
  '9.2': ['9.2'],
  'erste-tafel': ['8.1'],
  // GA 270b
  '10': ['10.1'],
  '11.1': ['11.1'],
  '11.2': ['11.2'],
  '11.3': ['11.3'],
  '12.1': ['12.1'],
  '12.2': ['12.2'],
  '13': ['13.1', '13.2', '13.3'],
  '14.1': ['14.1'],
  '15.1': ['15.1'],
  '16.1': ['16.1'],
  '16.2': ['16.2'],
  '17': ['17.1'],
  '18': ['18.1'],
  '19.1': ['19.1'],
};

export type KommentarEntry = { key: string; kommentar: Kommentar };

export type KommentareForMantra = {
  mode: 'page' | 'per-part';
  entries: KommentarEntry[];
};

export function kommentareForMantra(mantra: Mantra): KommentareForMantra | undefined {
  const keys = MANTRA_TO_KEYS[mantra.id];
  if (!keys || keys.length === 0) return undefined;
  const entries: KommentarEntry[] = [];
  for (const key of keys) {
    const k = source.strophen?.[key];
    if (isComplete(k)) entries.push({ key, kommentar: k });
  }
  if (entries.length === 0) return undefined;
  const mode: 'page' | 'per-part' = entries.length === 1 ? 'page' : 'per-part';
  return { mode, entries };
}

export function firstTafelbild(entries: KommentarEntry[]): Tafelbild | undefined {
  for (const e of entries) {
    if (e.kommentar.tafelbild) return e.kommentar.tafelbild;
  }
  return undefined;
}
