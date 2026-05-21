import glossarRaw from '../data/glossar.json';

export type GlossarEintrag = {
  id: string;
  begriff: string;
  auch?: string[];
  kurz: string;
  lang?: string;
  beleg?: string;
  verweis_auf?: string[];
};

type Source = {
  version?: string;
  stand?: string;
  hinweis?: string;
  eintraege: GlossarEintrag[];
};

const source = glossarRaw as Source;

export const glossarEintraege: GlossarEintrag[] = source.eintraege || [];

const eintragById = new Map<string, GlossarEintrag>(
  glossarEintraege.map((e) => [e.id, e]),
);

export function glossarEintragById(id: string): GlossarEintrag | undefined {
  return eintragById.get(id);
}

type Term = { phrase: string; id: string; re: RegExp };

function escapeRe(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Wort-Grenzen mit Unicode-Buchstaben/-Ziffern: deckt deutsche Umlaute ab.
function makeRegex(phrase: string): RegExp {
  return new RegExp(
    `(?<![\\p{L}\\p{N}])${escapeRe(phrase)}(?![\\p{L}\\p{N}])`,
    'u',
  );
}

function buildTerms(): Term[] {
  const ts: Term[] = [];
  for (const e of glossarEintraege) {
    ts.push({ phrase: e.begriff, id: e.id, re: makeRegex(e.begriff) });
    if (e.auch) {
      for (const a of e.auch) {
        ts.push({ phrase: a, id: e.id, re: makeRegex(a) });
      }
    }
  }
  // Längere Phrasen zuerst, damit ‹Hüter der Schwelle› vor ‹Hüter› matcht.
  ts.sort((a, b) => b.phrase.length - a.phrase.length);
  return ts;
}

const TERMS: Term[] = buildTerms();

export type LinkifyToken =
  | { kind: 'text'; text: string }
  | { kind: 'term'; phrase: string; eintrag: GlossarEintrag };

// Sucht in `text` die früheste Vorkommnis jedes noch nicht in `seen`
// gemerkten Glossarbegriffs und wandelt sie in einen Term-Token.
// Mutiert `seen` (page-scoped). Aufrufreihenfolge bestimmt First-Occurrence.
export function linkifyFirstOccurrence(
  text: string,
  seen: Set<string>,
): LinkifyToken[] {
  const out: LinkifyToken[] = [];
  let cursor = 0;
  while (cursor < text.length) {
    let bestPos = -1;
    let bestLen = 0;
    let bestId = '';
    let bestPhrase = '';
    const slice = text.slice(cursor);
    for (const term of TERMS) {
      if (seen.has(term.id)) continue;
      const m = term.re.exec(slice);
      if (!m) continue;
      const pos = cursor + m.index;
      if (bestPos === -1 || pos < bestPos) {
        bestPos = pos;
        bestLen = term.phrase.length;
        bestId = term.id;
        bestPhrase = term.phrase;
      }
    }
    if (bestPos === -1) {
      out.push({ kind: 'text', text: text.slice(cursor) });
      break;
    }
    if (bestPos > cursor) {
      out.push({ kind: 'text', text: text.slice(cursor, bestPos) });
    }
    const eintrag = eintragById.get(bestId)!;
    out.push({ kind: 'term', phrase: bestPhrase, eintrag });
    seen.add(bestId);
    cursor = bestPos + bestLen;
  }
  return out;
}
