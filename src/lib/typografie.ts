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

// Nach dem Doppel→Einfach-Schritt sind nur noch ‹ und › im Text. Die Daten
// setzen die innere Zitatebene aber einwärts (›…‹), was der außenzeigenden
// Hauskonvention widerspricht. Ein Paar-Regex auf ‹/› ist unsicher (er kann
// die Lücke zwischen zwei korrekten ‹…›-Paaren als Paar missdeuten). Daher
// klassifiziert outwardSingles jeden Guillemet kontextuell — und zwar über
// das Komplement: ein Guillemet ist nur dann ein Schließer ›, wenn davor ein
// Inhalts- oder Schlusszeichen steht (Buchstabe, Ziffer, Satz-/Schluss-
// zeichen, schließende Klammer/Anführung). Sonst ist es ein Öffner ‹. So
// werden auch Trenner wie der Pfeil → korrekt als Öffner-Kontext gewertet.
const PREV_CLOSES = /[\p{L}\p{N}.,;:!?…%)\]}»›'"„“]/u;

function outwardSingles(s: string): string {
  return s.replace(/[‹›]/g, (_m, off: number, str: string) => {
    const prev = off > 0 ? str[off - 1] : '';
    return prev !== '' && PREV_CLOSES.test(prev) ? '›' : '‹';
  });
}

export function tx(s: string | null | undefined): string {
  if (s == null) return '';
  let r = s;
  r = r.replace(PAIR_RE, '‹$1›');
  r = r.replace(/’/g, "'");   // U+2019 in den Daten ausschließlich Apostroph
  r = r.replace(/‘/g, '‹');   // U+2018 (selten) als öffnend behandeln
  r = r.replace(/‚/g, '‹');   // U+201A (selten) als öffnend behandeln
  r = outwardSingles(r);      // alle ‹/› kontextuell auf außenzeigend drehen
  return r;
}
