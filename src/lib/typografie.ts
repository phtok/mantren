// Anführungs-Normalisierung für die Anzeige.
// Konvention: alle Anführungen ‹…› (U+2039 / U+203A).
// Apostroph im Fließtext: ASCII '.
// Wirkt nur als Renderfilter; Datendateien bleiben unverändert.
//
// Hintergrund: Die Daten verwenden teils deutsche (»…«), teils schweizerische
// («…») Guillemet-Konvention sowie deutsche curly-Doubles („…“). Ein einfaches
// Pro-Glyph-Mapping würde »…« in ›…‹ verkehrt drehen. Daher: paarweise matchen
// und beide Enden gemeinsam zu ‹…› ersetzen, Richtung egal.

const PAIR_RE = /[«»„“”]([^«»„“”]*?)[«»„“”]/g;

export function tx(s: string | null | undefined): string {
  if (s == null) return '';
  let r = s;
  r = r.replace(PAIR_RE, '‹$1›');
  r = r.replace(/’/g, "'");   // U+2019 in den Daten ausschließlich Apostroph
  r = r.replace(/‘/g, '‹');   // U+2018 (selten) als öffnend behandeln
  r = r.replace(/‚/g, '‹');   // U+201A (selten) als öffnend behandeln
  return r;
}
