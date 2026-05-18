import { defineConfig } from 'astro/config';
import AstroPWA from '@vite-pwa/astro';

// GitHub Pages: Projekt-Site unter https://phtok.github.io/mantren/
const site = 'https://phtok.github.io';
const base = '/mantren';

export default defineConfig({
  site,
  base,
  trailingSlash: 'ignore',
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
        navigateFallback: `${base}/`,
        globPatterns: ['**/*.{js,css,html,woff2,svg,png,ico,webmanifest}'],
      },
    }),
  ],
});
