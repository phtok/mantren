// Französische Übersetzung, am Korpus ausgerichtet (Schlüssel = Mantra-ID).
// Die Strophen laufen parallel zu den Zeilen-Parts des Originals; reine
// Regie-/Section-Parts zählen nicht mit (vgl. Zählung in MantraView).
import raw from '../data/uebersetzung-fr.json';

export type FrMantra = {
  // Pro Zeilen-Strophe ein Array französischer Zeilen.
  strophen: string[][];
};

type FrData = {
  uebersetzerin: string;
  sprache: string;
  mantren: Record<string, FrMantra>;
};

const data = raw as unknown as FrData;

export const uebersetzerin: string = data.uebersetzerin;
export const sprache: string = data.sprache;

export function frForMantra(id: string): FrMantra | undefined {
  return data.mantren[id];
}
