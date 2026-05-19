import vortraegeRaw from '../data/vortraege.json';

export type Abschnitt = {
  anker: string;
  seite?: string;
  typ: string;
  titel?: string;
  text?: string;
  bild?: string;
  alt?: string;
  quelle?: string;
};

export type Tafelzeichnung = {
  bild: string;
  alt?: string;
  quelle?: string;
};

export type Vortrag = {
  id: string;
  titel: string;
  ort: string;
  datum: string;
  ga: string;
  seiten: string;
  gruppe?: string;
  status?: string;
  status_hinweis?: string;
  faksimile_url?: string;
  faksimile_hinweis?: string;
  abschnitte: Abschnitt[];
  tafelzeichnungen?: Tafelzeichnung[];
};

const source = vortraegeRaw as Record<string, unknown>;

function isVortragLike(v: unknown): v is Omit<Vortrag, 'id'> {
  return !!v && typeof v === 'object' && 'abschnitte' in v;
}

export const vortraege: Vortrag[] = Object.entries(source)
  .filter(([id, v]) => !id.startsWith('_') && isVortragLike(v))
  .map(([id, v]) => ({ id, ...(v as Omit<Vortrag, 'id'>) }));

export function isProtected(v: Vortrag): boolean {
  return v.status === 'geschuetzt-nicht-freigegeben' || (v.gruppe || '').toLowerCase().includes('geschützt');
}

// Öffentliche Vorträge — Index und Suche zeigen nur diese.
// Geschützte Seiten (z. B. Breslau-Volltext) bleiben über die direkte
// URL erreichbar, werden aber nicht in der Übersicht gelistet.
export const vortraegePublic: Vortrag[] = vortraege.filter((v) => !isProtected(v));

export function vortragById(id: string): Vortrag | undefined {
  return vortraege.find((v) => v.id === id);
}

export function vortragNeighbours(id: string): { prev?: Vortrag; next?: Vortrag } {
  // Navigation überspringt geschützte Seiten, damit man nicht versehentlich
  // durch normales Weiterblättern auf nicht-freigegebene Inhalte landet.
  const list = vortraegePublic;
  const idx = list.findIndex((v) => v.id === id);
  if (idx < 0) {
    // Aktuelle Seite ist geschützt — kein Pager.
    return {};
  }
  return {
    prev: idx > 0 ? list[idx - 1] : undefined,
    next: idx < list.length - 1 ? list[idx + 1] : undefined,
  };
}
