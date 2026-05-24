// Zentrale Offline-URL-Liste. Wird in Base.astro als <script id="offline-urls">
// auf jeder Seite eingebettet, damit der ‹offline laden›-Button auf der
// App-Seite (und perspektivisch von überall) funktioniert.

import { mantren } from './mantren';
import { vortraegePublic } from './vortraege';

export function buildOfflineUrls(base: string): string[] {
  const b = base.endsWith('/') ? base : `${base}/`;
  return [
    b,
    ...mantren.map((m) => `${b}${m.id}/`),
    `${b}vortraege/`,
    ...vortraegePublic.map((v) => `${b}${v.id}/`),
    `${b}quellen/`,
    `${b}einfuehrung/`,
    `${b}tafeln-galerie/`,
    `${b}universalsuche/`,
    `${b}impressum/`,
    `${b}offline/`,
    `${b}fonts/inclusive-sans.woff2`,
    `${b}fonts/plex-sans-300-normal.woff2`,
    `${b}fonts/plex-sans-400-normal.woff2`,
    `${b}fonts/plex-sans-500-normal.woff2`,
    `${b}fonts/plex-mono-400-normal.woff2`,
    `${b}fonts/plex-mono-400-italic.woff2`,
    `${b}fonts/plex-mono-500-normal.woff2`,
    `${b}favicon.svg`,
  ];
}
