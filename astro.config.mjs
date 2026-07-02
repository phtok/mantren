import { defineConfig } from 'astro/config';
import AstroPWA from '@vite-pwa/astro';

// Zwei Deploy-Ziele aus demselben Code:
// - GitHub Pages: Projekt-Site unter https://phtok.github.io/mantren/
// - Vercel: https://mantra.saetzerei.com/ an der Wurzel — die
//   öffentliche Projekt-Domain (kanonisch für site/Manifest/Sitemap).
//   Dasselbe Deployment bedient zusätzlich die Geschenk-Domain
//   fuer-martje.saetzerei.com; welche der beiden gilt, entscheidet zur
//   Laufzeit src/lib/geschenk.ts (OFFENE_HOSTS). Vercel setzt beim
//   Build automatisch VERCEL=1; lokal lässt sich diese Variante mit
//   `VERCEL=1 npm run build` erzeugen.
const aufVercel = !!process.env.VERCEL;
const site = process.env.SITE || (aufVercel ? 'https://mantra.saetzerei.com' : 'https://phtok.github.io');
const base = aufVercel ? '' : '/mantren';

export default defineConfig({
  site,
  base: base || '/',
  // Astro-Routen IMMER mit Trailing-Slash. GitHub Pages macht sonst
  // einen 301-Redirect (z.B. /stunde-1 → /stunde-1/), der offline
  // nicht funktioniert und den SW-Precache aushebelt.
  trailingSlash: 'always',
  build: {
    // CSS direkt ins HTML einbetten — vermeidet Hash-Mismatch zwischen
    // HTML und CSS-Datei bei PWA-Updates (alte HTML referenziert sonst
    // einen CSS-Hash, der nach dem Deploy nicht mehr existiert).
    inlineStylesheets: 'always',
  },
  integrations: [
    AstroPWA({
      registerType: 'autoUpdate',
      base: `${base}/`,
      scope: `${base}/`,
      // Register-Aufruf inline ins HTML; bei iOS Safari (PWA-Standalone)
      // war das ausgelagerte /registerSW.js bisher nicht eingebunden,
      // sodass der SW gar nicht registriert wurde.
      injectRegister: 'inline',
      includeAssets: ['favicon.svg', 'fonts/*.woff2'],
      manifest: {
        name: 'Mantren',
        short_name: 'Mantren',
        description: 'Rudolf Steiners mantrisches Spätwerk – Erste Klasse',
        lang: 'de',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: `${base}/`,
        scope: `${base}/`,
        icons: [
          {
            src: 'favicon.svg',
            sizes: 'any',
            type: 'image/svg+xml',
            purpose: 'any',
          },
        ],
      },
      workbox: {
        // Beim Service-Worker-Install werden ALLE Build-Artefakte ins
        // Precache geladen (Astro baut alle Routen als statisches HTML).
        // Damit ist die ganze App offline verfügbar, sobald der SW einmal
        // installiert war — auch ohne dass ‹offline laden› geklickt wurde.
        navigateFallback: `${base}/`,
        globPatterns: ['**/*.{js,css,html,woff2,svg,png,jpg,jpeg,webp,avif,ico,webmanifest}'],
        // 4 MB pro Datei (Default 2 MB); /universalsuche/ und /vortraege/
        // bringen den JSON-Datenstamm inline und sind die größten HTMLs.
        maximumFileSizeToCacheInBytes: 4 * 1024 * 1024,
        // Neuen SW sofort übernehmen, statt erst beim nächsten Tab-Load.
        clientsClaim: true,
        skipWaiting: true,
      },
    }),
  ],
});
