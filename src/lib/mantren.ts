import { parse } from 'yaml';
// Vite raw-import: stable in dev & build
import raw from '../data/mantren.yaml?raw';

export type Part = {
  regie?: string;
  section?: string;
  lines?: string[];
};

export type Mantra = {
  id: string;
  chapter: string;
  number: string;
  title?: string;
  parts: Part[];
};

export type Chapter = {
  id: string;
  title: string;
  range?: string;
};

type Source = {
  chapters: Chapter[];
  mantren: Mantra[];
};

const source = parse(raw) as Source;

export const chapters: Chapter[] = source.chapters;
export const mantren: Mantra[] = source.mantren;

export function mantraById(id: string): Mantra | undefined {
  return mantren.find((m) => m.id === id);
}

export function neighbours(id: string): { prev?: Mantra; next?: Mantra } {
  const idx = mantren.findIndex((m) => m.id === id);
  if (idx < 0) return {};
  return {
    prev: idx > 0 ? mantren[idx - 1] : undefined,
    next: idx < mantren.length - 1 ? mantren[idx + 1] : undefined,
  };
}

export function mantrenByChapter(chapterId: string): Mantra[] {
  return mantren.filter((m) => m.chapter === chapterId);
}
