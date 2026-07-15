// Backend für die editierbare französische Übersetzung (Supabase).
// URL und publizierbarer Key sind bewusst öffentlich (durch RLS geschützt:
// anon darf nur lesen). Geschrieben wird nur über die Edge-Function mit Louis'
// Geheim-Token — der steht NIE im Build, nur in seinem privaten Link.
export const FR_BACKEND = {
  url: 'https://dagcsnfrlbpxcmdimnrw.supabase.co',
  anon: 'sb_publishable_SXhY0mrhXjdTnjbJ5Uobtg_zAXW_xGY',
  table: 'mantren_uebersetzung_fr',
  rpc: 'mantren_fr_save',
};
