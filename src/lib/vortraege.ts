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

export function vortragById(id: string): Vortrag | undefined {
  return vortraege.find((v) => v.id === id);
}

export function vortragNeighbours(id: string): { prev?: Vortrag; next?: Vortrag } {
  const idx = vortraege.findIndex((v) => v.id === id);
  if (idx < 0) return {};
  return {
    prev: idx > 0 ? vortraege[idx - 1] : undefined,
    next: idx < vortraege.length - 1 ? vortraege[idx + 1] : undefined,
  };
}
