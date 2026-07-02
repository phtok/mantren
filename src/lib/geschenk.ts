// Geburtstags-Geschenk: Zugangsschutz für die Geschenk-Domain
// (mantra.saetzerei.com). Alles Build-Zeit-Konfiguration — die Site
// bleibt rein statisch.
//
// - Aktiv, wenn der Build auf Vercel läuft (VERCEL=1 wird dort
//   automatisch gesetzt) oder GESCHENK=1 explizit gesetzt ist.
//   Der GitHub-Pages-Build bleibt dadurch wie bisher offen.
// - Das Geheimwort kommt aus GESCHENK_CODE (Vercel-Projekt-Env),
//   Fallback ist ein Default im Code. Im HTML landet nur der
//   SHA-256-Hash; der Client vergleicht via crypto.subtle.
// - Magic-Link: /geschenk/?s=<geheimwort> löst den Knoten direkt.

import { createHash } from 'node:crypto';

export const aufVercel = !!process.env.VERCEL;
export const geschenkAktiv = aufVercel || process.env.GESCHENK === '1';

export const GESCHENK_CODE_DEFAULT = 'time';

const code = (process.env.GESCHENK_CODE || GESCHENK_CODE_DEFAULT).trim().toLowerCase();

export const zugangHash = createHash('sha256').update(code, 'utf8').digest('hex');

// localStorage-Schlüssel, unter dem der freigeschaltete Zugang liegt.
export const ZUGANG_KEY = 'mantren:zugang';
