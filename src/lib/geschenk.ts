// Geburtstags-Geschenk: Zugangsschutz für die Geschenk-Domain.
// Alles Build-Zeit-Konfiguration — die Site bleibt rein statisch.
//
// Aktiv, wenn der Build auf Vercel läuft (VERCEL=1 wird dort automatisch
// gesetzt) oder GESCHENK=1 explizit gesetzt ist. Der GitHub-Pages-Build
// bleibt dadurch wie bisher offen.
//
// Kein Geheimwort: der Schutz besteht allein aus der unauffälligen
// Domain und dem Geschenkband, das erst gezogen werden muss. Ohne
// freigeschalteten Zugang (localStorage) leiten alle Seiten auf
// /geschenk/ um; das Ziehen am Band merkt sich den Zugang.

export const aufVercel = !!process.env.VERCEL;
export const geschenkAktiv = aufVercel || process.env.GESCHENK === '1';

export const ZUGANG_KEY = 'mantren:zugang';
export const ZUGANG_WERT = 'ausgepackt';
