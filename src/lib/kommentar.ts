import kommentarRaw from '../data/mantren-kommentar.json';

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

export function kommentarFor(id: string): Kommentar | undefined {
  const fromStrophen = source.strophen?.[id];
  if (isComplete(fromStrophen)) return fromStrophen;
  const fromTafeln = source.tafeln?.[id];
  if (isComplete(fromTafeln)) return fromTafeln;
  return undefined;
}
