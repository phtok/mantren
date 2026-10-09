#!/usr/bin/env python3
"""Produktion des Features «Es ist an der Zeit».

    XI_KEY=… python3 -I produktion.py stimmen     # alle Sprechzeilen erzeugen (Cache)
    XI_KEY=… python3 -I produktion.py klaenge     # Geräusche und Musik erzeugen (Cache)
    python3 -I produktion.py mischen [ausgabe]    # aus dem Cache mischen, kostet nichts

Regie-Liste wie bei «Gewachsen, nicht gebaut» (ROLLE|Text, STILLE|n s,
MUSIK|…, GERÄUSCH|<Prompt>, n s). Seit «Was die Schlange weiss» dazu ATMO|<Prompt>, n s
(Szenenbett bis zum nächsten ATMO, weicht den Textrollen), RAUM|<Name> (Nachhall der
Lebensstimmen) und MUSIK|Platte an/aus (Musik als Schallplatte im Zimmer). Unterschied: Eine Zeile wird in einem
Stück gesprochen (der Satzbogen bleibt), die Atempausen setzt der Mischer
nach den Zeitmarken je Zeichen an die markierten Stellen.
"""
import base64, hashlib, json, os, re, subprocess, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HIER, 'clips')
SR = 44100
API = 'https://api.elevenlabs.io'
MODELL = 'eleven_v4'

STIMMEN = {
    'ERZÄHLERIN': 'nzC30P1U2LuQhAoEQcYi',  # NWR Erzählerin
    'CHRONIST': 'IcDVpTMW6YwgOc2vCZgG',    # NWR Chronist
    'GOETHE': 'jhhOoZ28WmHOJDBuCSGG',      # Märchen-Erzählerin, die Stimme der Textprobe (Wunsch 9. 10. 2026)
    'STEINER': 'NBqeXKdZHweef6y0B67V',     # Christian Plasa
    'MANTRA': '6dD0VbyJ548lcuDpD5ew',      # Märchen-Leise
}
TAGS = {
    'ruhig': 'calm', 'langsam': 'slowly', 'leise': 'quietly', 'eindringlich': 'serious',
    'amüsiert': 'amused', 'warm': 'warm', 'traurig': 'sad',
    'lebendig': 'lively', 'klar': 'clear', 'wach': 'awake', 'erschrocken': 'startled',
    'ohne die Stimme zu heben': 'without raising the voice', 'sachlich': None,
    'trocken': 'dryly', 'lacht': 'laughs', 'lacht leise': 'chuckles', 'überrascht': 'surprised',
    'zögernd': 'hesitant', 'nachdenklich': 'thoughtful',
}
# Ein zweites Stück aus derselben Werkstatt: STUECK=essay liest essay.txt und essay.json
STUECK = os.environ.get('STUECK', 'manuskript')
if STUECK != 'manuskript':
    _konf = json.load(open(os.path.join(HIER, f'{STUECK}.json'), encoding='utf8'))
    STIMMEN = _konf['stimmen']
# Verse (Mantren) werden Zeile für Zeile gesprochen: Die Stimme zieht die Zeilen sonst
# lückenlos zusammen, und jeder nachträgliche Schnitt träfe Klang.
GETRENNT = set(_konf.get('getrennt', ['MANTRA'])) if STUECK != 'manuskript' else {'MANTRA'}
_konf = _konf if STUECK != 'manuskript' else {}
ATEM, PAUSE = 0.55, 1.10
# Gesprächstempo je Stück (Lehre aus «Durchsichtig»: 0,85 s zwischen allen Zeilen macht Bröckchen).
LUECKE_WECHSEL, LUECKE_GLEICH = _konf.get('luecken', [0.85, 0.65])
# Texte (Märchen, Mantren, Zitate) stehen in eigenem Raum: die Atmo weicht, Lebensstimmen klingen im Raum der Szene.
TEXTROLLEN = set(_konf.get('textrollen', []))
RAEUME = _konf.get('raeume', {})          # Szene oder Rolle -> [Nachhall s, Anteil dB, Vorverzögerung s] oder null
KONTEXT = bool(_konf.get('kontext', False))  # Nachbarzeilen als previous/next_text für Gesprächszeilen
EREIGNIS_MAX = _konf.get('ereignis_max', 6)
EREIGNIS_VORLAUF = _konf.get('ereignis_vorlauf', 999)


# ---------------------------------------------------------------- Regie-Liste
def lesen(pfad=os.path.join(HIER, f'{STUECK}.txt')):
    cues = []
    for z in open(pfad, encoding='utf8'):
        z = z.rstrip('\n')
        if not z or z.startswith('#'):
            continue
        art, _, rest = z.partition('|')
        if art in STIMMEN:
            cues.append({'art': 'rede', 'rolle': art, 'text': rest})
        elif art == 'STILLE':
            cues.append({'art': 'stille', 's': float(rest.split()[0])})
        elif art == 'GERÄUSCH':
            prompt, _, dauer = rest.rpartition(',')
            cues.append({'art': 'geraeusch', 'prompt': prompt.strip(), 's': float(dauer.split()[0])})
        elif art == 'MUSIK':
            cues.append({'art': 'musik', 'befehl': rest.strip()})
        elif art == 'ATMO':
            prompt, _, dauer = rest.rpartition(',')
            cues.append({'art': 'atmo', 'prompt': prompt.strip(), 's': float(dauer.split()[0])})
        elif art == 'RAUM':
            cues.append({'art': 'raum', 'name': rest.strip()})
        else:
            raise SystemExit(f'Unbekannte Zeile: {z}')
    if KONTEXT:
        # Gesprächszeilen kennen die Nachbarzeile des Gesprächs (nicht über Texte und Musik hinweg)
        def gespraech(j):
            return 0 <= j < len(cues) and cues[j]['art'] == 'rede' and cues[j]['rolle'] not in TEXTROLLEN \
                and cues[j]['rolle'] not in GETRENNT
        def nachbar(i, schritt):
            j = i + schritt
            while 0 <= j < len(cues) and cues[j]['art'] == 'stille':
                j += schritt
            return ohne_regie(cues[j]['text'])[:300] if gespraech(j) else None
        for i, c in enumerate(cues):
            if gespraech(i):
                c['vorher'], c['nachher'] = nachbar(i, -1), nachbar(i, 1)
    return cues


def tag_englisch(inhalt):
    teile = [t.strip() for t in inhalt.split(',')]
    en = [TAGS[t] for t in teile if t in TAGS and TAGS[t]]
    unbekannt = [t for t in teile if t not in TAGS]
    if unbekannt:
        raise SystemExit(f'Unbekannter Tag: {unbekannt}')
    return ('[' + ', '.join(en) + ']') if en else ''


def schluessel(*teile):
    return hashlib.sha1('\x1f'.join(teile).encode()).hexdigest()[:16]


# ---------------------------------------------------------------- ElevenLabs
def anfrage(pfad, koerper, binaer=False, versuche=5):
    key = os.environ['XI_KEY']
    for v in range(versuche):
        req = urllib.request.Request(API + pfad, data=json.dumps(koerper).encode(),
                                     headers={'xi-api-key': key, 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                daten = r.read()
                return daten if binaer else json.loads(daten)
        except urllib.error.HTTPError as e:
            text = e.read().decode('utf8', 'replace')[:300]
            if e.code in (429, 500, 502, 503, 504) and v < versuche - 1:
                time.sleep(4 * (v + 1))
                continue
            raise SystemExit(f'HTTP {e.code} {pfad}: {text}')
    raise SystemExit('keine Antwort')


def rede_text(cue):
    """Der gesendete Text ohne Pausenmarken; Marken als Zeichenposition darin."""
    gesendet, pausen = '', []
    for teil in re.split(r'(\[[^\]]+\])', cue['text']):
        if teil.startswith('['):
            inhalt = teil[1:-1]
            if inhalt in ('Atem', 'Pause'):
                pausen.append([len(gesendet), ATEM if inhalt == 'Atem' else PAUSE])
            else:
                en = tag_englisch(inhalt)
                if en:
                    gesendet += (' ' if gesendet and not gesendet.endswith(' ') else '') + en + ' '
        else:
            if gesendet.endswith(' ') and teil.startswith(' '):
                teil = teil.lstrip(' ')
            gesendet += teil
    return gesendet.strip(), pausen


def segmente(cue):
    """Für Verse: die Zeile an [Atem]/[Pause] zerlegt; jedes Stück trägt die Regie der Zeile.
    Liefert (gesendeter Text, Pause danach in s)."""
    roh = cue['text']
    m = re.match(r'^((?:\s*\[[^\]]+\])*)', roh)
    kopf = ''.join(t for t in re.findall(r'\[[^\]]+\]', m.group(1)) if t not in ('[Atem]', '[Pause]'))
    rest = roh[m.end():]
    teile = re.split(r'(\[Atem\]|\[Pause\])', rest)
    aus = []
    for i in range(0, len(teile), 2):
        stueck = teile[i].strip()
        if not stueck:
            continue
        pause = 0.0
        if i + 1 < len(teile):
            pause = ATEM if teile[i + 1] == '[Atem]' else PAUSE
        text, _ = rede_text({'text': kopf + ' ' + stueck})
        aus.append((text, pause))
    return aus


def tts(sid, text, vorher=None, nachher=None):
    k = schluessel('tts', MODELL, sid, text, vorher or '', nachher or '')
    mp3, js = os.path.join(CACHE, f'tts_{k}.mp3'), os.path.join(CACHE, f'tts_{k}.json')
    if os.path.exists(mp3) and os.path.exists(js):
        return k, False
    koerper = {'text': text, 'model_id': MODELL, 'language_code': 'de'}
    if vorher:
        koerper['previous_text'] = vorher
    if nachher:
        koerper['next_text'] = nachher
    antwort = anfrage(f'/v1/text-to-speech/{sid}/with-timestamps?output_format=mp3_44100_128', koerper)
    open(mp3, 'wb').write(base64.b64decode(antwort['audio_base64']))
    json.dump({'text': text, 'alignment': antwort.get('alignment')}, open(js, 'w'), ensure_ascii=False)
    return k, True


def ohne_regie(t):
    return re.sub(r'\s*\[[^\]]+\]\s*', ' ', t).strip()


def stimme_erzeugen(cue):
    sid = STIMMEN[cue['rolle']]
    if cue['rolle'] in GETRENNT:
        seg = segmente(cue)
        neu = False
        for j, (text, _) in enumerate(seg):
            vorher = ohne_regie(seg[j - 1][0]) if j > 0 else None
            nachher = ohne_regie(seg[j + 1][0]) if j + 1 < len(seg) else None
            _, frisch = tts(sid, text, vorher, nachher)
            neu = neu or frisch
        return 'segmente', neu
    text, _ = rede_text(cue)
    if not cue.get('vorher') and not cue.get('nachher'):
        k = schluessel('tts', MODELL, sid, text)   # Cache aus der Zeit vor previous/next_text
        if os.path.exists(os.path.join(CACHE, f'tts_{k}.mp3')) and os.path.exists(os.path.join(CACHE, f'tts_{k}.json')):
            return k, False
    return tts(sid, text, cue.get('vorher'), cue.get('nachher'))


def klang_erzeugen(art, prompt, dauer):
    k = schluessel(art, prompt, str(dauer))
    mp3 = os.path.join(CACHE, f'{art}_{k}.mp3')
    if os.path.exists(mp3):
        return k, False
    if art == 'sfx':
        daten = anfrage('/v1/sound-generation?output_format=mp3_44100_128',
                        {'text': prompt, 'duration_seconds': dauer, 'prompt_influence': 0.4}, binaer=True)
    else:
        daten = anfrage('/v1/music?output_format=mp3_44100_128',
                        {'prompt': prompt, 'music_length_ms': int(dauer * 1000), 'model_id': 'music_v2_5',
                         'force_instrumental': True}, binaer=True)
    open(mp3, 'wb').write(daten)
    return k, True


MUSIK_PROMPT = ('Solo concert harp, slow and spacious, calm, intimate, sparse arpeggios in D major '
                'with gentle suspended notes, warm low strings very softly underneath, no percussion, '
                'no vocals, reflective, like the opening of a cultural radio feature, 72 bpm')
MUSIK_DAUER = 45
if STUECK != 'manuskript':
    MUSIK_PROMPT, MUSIK_DAUER = _konf['musik']['prompt'], _konf['musik']['dauer']


# ---------------------------------------------------------------- Audio
def dekodieren(pfad, kanaele=2):
    roh = subprocess.run(['ffmpeg', '-v', 'error', '-i', pfad, '-f', 'f32le', '-ac', str(kanaele),
                          '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(roh, dtype=np.float32).reshape(-1, kanaele).copy()


def db(x):
    return 10 ** (x / 20)


def rms_db(x):
    x = x[np.abs(x).max(axis=1) > 1e-4] if x.ndim == 2 else x
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def stille(s):
    return np.zeros((int(round(s * SR)), 2), dtype=np.float32)


def blende(x, ein=0.005, aus=0.005):
    n1, n2 = int(ein * SR), int(aus * SR)
    if n1:
        x[:n1] *= np.linspace(0, 1, n1)[:, None]
    if n2:
        x[-n2:] *= np.linspace(1, 0, n2)[:, None]
    return x


def zuschneiden(x, schwelle=db(-55)):
    """Stille an den Rändern kürzen, aber den Atem vor dem ersten Wort und den Ausklang
    stehen lassen (Lehre der Textprobe: «der Anfang huckelt, es fehlt Luft vor dem ersten Wort»)."""
    laut = np.where(np.abs(x).max(axis=1) > schwelle)[0]
    if not len(laut):
        return x
    a = max(0, laut[0] - min(int(0.25 * SR), laut[0]))
    e = min(len(x), laut[-1] + int(0.3 * SR))
    return blende(x[a:e].copy(), 0.02, 0.08)


def cos_blende(x, ein=0.015, aus=0.015):
    """Weiche Blenden (Kosinus) an Schnittstellen."""
    n1, n2 = min(len(x), int(ein * SR)), min(len(x), int(aus * SR))
    if n1:
        x[:n1] *= (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, n1)))[:, None]
    if n2:
        x[-n2:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, n2)))[:, None]
    return x


def leiseste_stelle(m, von, bis):
    """Mitte des leisesten 12-ms-Fensters zwischen von und bis (Sekunden) und sein Pegel in dB."""
    a, b = max(0, int(von * SR)), min(len(m), int(bis * SR))
    fr = int(0.012 * SR)
    if b - a <= fr:
        return a, 0.0
    leist = np.convolve(m[a:b] ** 2, np.ones(fr) / fr, mode='valid')
    i = int(np.argmin(leist))
    return a + i + fr // 2, 10 * np.log10(leist[i] + 1e-12)


SCHNITT_STATISTIK = {'gesetzt': 0, 'ausgelassen': 0}


def rede_audio(cue):
    sid = STIMMEN[cue['rolle']]
    if cue['rolle'] in GETRENNT:
        seg = segmente(cue)
        stuecke = []
        for j, (text, pause) in enumerate(seg):
            vorher = ohne_regie(seg[j - 1][0]) if j > 0 else None
            nachher = ohne_regie(seg[j + 1][0]) if j + 1 < len(seg) else None
            k = schluessel('tts', MODELL, sid, text, vorher or '', nachher or '')
            x = zuschneiden(dekodieren(os.path.join(CACHE, f'tts_{k}.mp3')))
            stuecke.append(x)
            if pause:
                stuecke.append(stille(max(0.1, pause - 0.2)))   # zuschneiden lässt rund 0,2 s Ausklang stehen
        return np.concatenate(stuecke)
    text, pausen = rede_text(cue)
    k = schluessel('tts', MODELL, sid, text, cue.get('vorher') or '', cue.get('nachher') or '')
    pfad = os.path.join(CACHE, f'tts_{k}.mp3')
    if not os.path.exists(pfad):   # Cache aus der Zeit vor previous/next_text
        k = schluessel('tts', MODELL, sid, text)
        pfad = os.path.join(CACHE, f'tts_{k}.mp3')
    x = dekodieren(pfad)
    al = json.load(open(os.path.join(CACHE, f'tts_{k}.json')))['alignment']
    zeichen, anf, end = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    if ''.join(zeichen) != text:
        print(f'  Hinweis: Zeitmarken passen nicht zum Text ({cue["rolle"]}: {text[:40]}…), Pausen entfallen')
        pausen = []
    m = x.mean(axis=1)
    ref = rms_db(x)
    schnitte = []
    for pos, dauer in pausen:
        i1 = pos - 1
        while i1 >= 0 and zeichen[i1] in ' ':
            i1 -= 1
        i2 = pos
        while i2 < len(zeichen) and zeichen[i2] in ' ':
            i2 += 1
        if i1 < 0 or i2 >= len(zeichen):
            continue
        t1, t2 = end[i1], anf[i2]
        # nur in echter Stille schneiden: leisestes Fenster rund um die Fuge suchen
        n, pegel = leiseste_stelle(m, t1 - 0.04, t2 + 0.06)
        if pegel - ref > -35:
            SCHNITT_STATISTIK['ausgelassen'] += 1
            continue
        SCHNITT_STATISTIK['gesetzt'] += 1
        luecke = max(0.0, t2 - t1)
        schnitte.append((n, max(0.12, dauer - luecke)))
    stuecke, letzt = [], 0
    for n, extra in schnitte:
        stuecke.append(cos_blende(x[letzt:n].copy(), 0.0 if not stuecke else 0.015, 0.015))
        stuecke.append(stille(extra))
        letzt = n
    stuecke.append(cos_blende(x[letzt:].copy(), 0.015 if stuecke else 0.0, 0.0))
    return zuschneiden(np.concatenate(stuecke))


def hall_ir(nachhall, vorlauf, seed=7):
    """Synthetischer Nachhall: abklingendes, leicht abgedunkeltes Rauschen, je Kanal eigenes (Breite)."""
    rng = np.random.default_rng(seed)
    nd, n = int(vorlauf * SR), int((vorlauf + nachhall * 1.1) * SR)
    t = np.arange(n - nd) / SR
    ir = np.zeros((n, 2), dtype=np.float32)
    for k in range(2):
        r = np.convolve(rng.standard_normal(n - nd), np.ones(5) / 5, mode='same')
        ir[nd:, k] = r * np.exp(-6.91 * t / nachhall)
    return ir / np.sqrt((ir ** 2).sum(axis=0, keepdims=True))


def falten(x, ir):
    n = len(x) + len(ir) - 1
    N = 1 << (n - 1).bit_length()
    aus = np.empty((n, 2), dtype=np.float32)
    for k in range(2):
        aus[:, k] = np.fft.irfft(np.fft.rfft(x[:, k], N) * np.fft.rfft(ir[:, k], N), N)[:n]
    return aus


def verhallen(x, raum):
    """Trockenes Signal plus Nachhall; der Nachhall klingt über das Ende hinaus."""
    if not raum:
        return x
    nachhall, anteil, vorlauf = raum
    nass = falten(x, hall_ir(nachhall, vorlauf))
    nass *= db(anteil) * (10 ** (rms_db(x) / 20)) / (10 ** (rms_db(nass) / 20))
    nass[:len(x)] += x
    return blende(nass, 0.0, 0.3)


def frequenzband(x, unten, oben):
    """Schlichter FFT-Bandpass (für die Schallplatte im Zimmer)."""
    N = 1 << (len(x) - 1).bit_length()
    f = np.fft.rfftfreq(N, 1 / SR)
    maske = np.clip((f - unten * 0.7) / (unten * 0.3), 0, 1) * np.clip((oben * 1.3 - f) / (oben * 0.3), 0, 1)
    aus = np.empty_like(x)
    for k in range(2):
        aus[:, k] = np.fft.irfft(np.fft.rfft(x[:, k], N) * maske, N)[:len(x)]
    return aus


def schleife(x, n, ueber=1.5):
    """Atmo auf Länge n bringen: Stücke mit Kreuzblende aneinander."""
    if len(x) >= n:
        return x[:n].copy()
    u = int(ueber * SR)
    aus = x.copy()
    ein = np.linspace(0, 1, u, dtype=np.float32)[:, None]
    while len(aus) < n:
        aus = np.concatenate([aus[:-u], aus[-u:] * (1 - ein) + x[:u] * ein, x[u:]])
    return aus[:n]


def knistern(n, seed=11):
    """Plattenknistern: leises Rauschen und vereinzelte Knackser."""
    rng = np.random.default_rng(seed)
    r = np.convolve(rng.standard_normal(n), np.ones(3) / 3, mode='same') * 0.004
    for i in rng.integers(0, n, n // SR * 6):
        r[i:i + 30] += rng.uniform(0.02, 0.08) * np.exp(-np.arange(min(30, n - i)) / 6)
    return np.stack([r, r * 0.9], axis=1).astype(np.float32)


def mischen(ausgabe):
    cues = lesen()
    # 1. Sprache: Pegel je Zeile (−20 dBFS RMS, leise Zeilen 2,5 dB darunter), dann Raum der Szene oder Rolle
    reden, dauer_trocken, raum_name = {}, {}, None
    for i, c in enumerate(cues):
        if c['art'] == 'raum':
            raum_name = c['name']
        elif c['art'] == 'rede':
            x = rede_audio(c)
            ziel = -22.5 if c['text'].startswith('[leise') else -20.0
            x = x * db(min(12.0, ziel - rms_db(x)))
            dauer_trocken[i] = len(x) / SR
            if c['rolle'] in RAEUME:
                x = verhallen(x, RAEUME[c['rolle']])
            elif c['rolle'] not in TEXTROLLEN and raum_name:
                x = verhallen(x, RAEUME.get(raum_name))
            reden[i] = x

    musik = None
    mpfad = os.path.join(CACHE, f'mus_{schluessel("mus", MUSIK_PROMPT, str(MUSIK_DAUER))}.mp3')
    if os.path.exists(mpfad):
        musik = dekodieren(mpfad)
        musik *= db(-20 - rms_db(musik))

    # 2. Zeitleiste
    stimme = []        # (start, audio, rolle)
    betten = []        # (start, audio) fertig, oder ('art', …) zur späteren Hüllkurve
    t, vorige, wartet_stille = 0.0, None, False
    mus_start, mus_offen = None, False
    atmo_offen, platte_start = None, None
    marken = []

    def atmo_schliessen(bis):
        nonlocal atmo_offen
        if atmo_offen:
            betten.append(('atmo', atmo_offen[0], bis, atmo_offen[1]))
            atmo_offen = None

    for i, c in enumerate(cues):
        if c['art'] == 'stille':
            t += c['s']
            wartet_stille = True
        elif c['art'] == 'raum':
            continue
        elif c['art'] == 'rede':
            if vorige is not None and not wartet_stille:
                if (vorige in TEXTROLLEN) != (c['rolle'] in TEXTROLLEN):
                    t += max(LUECKE_WECHSEL, _konf.get('luecke_text', LUECKE_WECHSEL))
                else:
                    t += LUECKE_GLEICH if vorige == c['rolle'] else LUECKE_WECHSEL
            stimme.append((t, reden[i], c['rolle']))
            marken.append((t, c['rolle'], c['text'][:50]))
            t += dauer_trocken[i]
            vorige, wartet_stille = c['rolle'], False
        elif c['art'] == 'atmo':
            k = schluessel('sfx', c['prompt'], str(c['s']))
            pfad = os.path.join(CACHE, f'sfx_{k}.mp3')
            atmo_schliessen(t + 1.5)
            if not os.path.exists(pfad):
                print(f'  fehlt: Atmo «{c["prompt"][:50]}» — übersprungen')
                continue
            atmo_offen = (t, pfad)
            t += 2.5
            wartet_stille = True
        elif c['art'] == 'geraeusch':
            k = schluessel('sfx', c['prompt'], str(c['s']))
            pfad = os.path.join(CACHE, f'sfx_{k}.mp3')
            if not os.path.exists(pfad):
                print(f'  fehlt: Geräusch «{c["prompt"][:50]}» — übersprungen')
                continue
            x = dekodieren(pfad)
            x *= db(-20 - rms_db(x))
            dauer = len(x) / SR
            if dauer <= EREIGNIS_MAX:   # Ereignis: steht frei
                betten.append((t, blende(x * db(-4), 0.05, 0.4)))
                t += min(dauer * 0.85, EREIGNIS_VORLAUF)
            else:            # Atmo alter Art: 3,2 s frei, dann leise unter der Sprache
                vor = 3.2
                huelle = np.full(len(x), db(-23), dtype=np.float32)
                n_vor, n_ueb = int(vor * SR), int(1.2 * SR)
                huelle[:n_vor] = db(-8)
                huelle[n_vor:n_vor + n_ueb] = np.linspace(db(-8), db(-23), min(n_ueb, len(x) - n_vor))
                betten.append((t, blende(x * huelle[:, None], 1.0, 2.5)))
                t += vor
            wartet_stille = True
        elif c['art'] == 'musik':
            b = c['befehl']
            if b == 'Platte an':
                platte_start = t
                marken.append((t, 'MUSIK', b))
                continue
            m = re.match(r'Platte, frei ([\d.]+) s', b)
            if m:
                t += float(m.group(1))
                wartet_stille = True
                continue
            if b == 'Platte aus':
                if platte_start is not None:
                    betten.append(('platte', platte_start, t + 0.15))
                    platte_start = None
                continue
            m = re.match(r'Thema, frei ([\d.]+) s', b)
            if m:
                frei = float(m.group(1))
                if not mus_offen:
                    mus_start, mus_offen = t, True
                marken.append((t, 'MUSIK', b))
                t += frei
                wartet_stille = True
                continue
            if b == 'Thema aus' and mus_offen:
                mus_offen = False
                betten.append(('musikbett', mus_start, t + 0.5))
                t += 2.0   # die Blende klingt aus, bevor gesprochen wird
                wartet_stille = True
                continue
            m = re.match(r'Thema, Brücke ([\d.]+) s', b)
            if m:
                lang = float(m.group(1))
                if musik is not None:
                    ab = 20.0
                    x = musik[int(ab * SR):int((ab + lang + 2.5) * SR)].copy()
                    x = blende(x * db(-10), 0.8, 2.5)
                    betten.append((t + 0.3, x))
                marken.append((t, 'MUSIK', b))
                t += lang + 0.8
                wartet_stille = True
                continue
            if b == 'Thema, Schluss':
                atmo_schliessen(t + 3.0)
                mus_start, mus_offen = t, True
                betten.append(('schluss', t))
                t += 4.0
                wartet_stille = True
                continue
            raise SystemExit(f'MUSIK unbekannt: {b}')

    gesamt = t + 4.0
    atmo_schliessen(gesamt)
    # Masken: wo spricht wer?
    N = int(gesamt * SR) + 12 * SR
    sprache_aktiv = np.zeros(N, dtype=bool)
    text_aktiv = np.zeros(N, dtype=bool)
    for s, a, rolle in stimme:
        n0 = int(s * SR)
        sprache_aktiv[n0:n0 + len(a)] = True
        if rolle in TEXTROLLEN:
            text_aktiv[max(0, n0 - int(0.6 * SR)):n0 + len(a) + int(0.4 * SR)] = True

    def huelle_bett(von, n, frei, unter, text=None):
        a, b = int(von * SR), int(von * SR) + n
        sa = np.pad(sprache_aktiv[a:b], (0, max(0, n - len(sprache_aktiv[a:b]))))[:n]
        ziel = np.where(sa, db(unter), db(frei)).astype(np.float32)
        if text is not None:
            ta = np.pad(text_aktiv[a:b], (0, max(0, n - len(text_aktiv[a:b]))))[:n]
            ziel = np.where(ta, db(text), ziel).astype(np.float32)
        return glaetten(ziel, int(0.6 * SR))

    fertig_betten = []
    for b in betten:
        if b[0] == 'atmo':
            _, von, bis, pfad = b
            x = dekodieren(pfad)
            x *= db(-20 - rms_db(x))
            n = int((bis - von) * SR)
            x = schleife(x, n)
            ziel = huelle_bett(von, n, -24, -24, -44)
            ziel[:int(2.5 * SR)] = np.maximum(ziel[:int(2.5 * SR)], db(-11))
            x *= glaetten(ziel, int(0.8 * SR))[:, None]
            fertig_betten.append((von, blende(x, 1.2, 1.5)))
        elif b[0] == 'platte' and musik is not None:
            _, von, bis = b
            n = int((bis - von) * SR)
            x = schleife(musik, n, 0.5)
            x = frequenzband(x, 180, 6500)
            x = (x * 0.75 + x[:, ::-1] * 0.25) + knistern(n)
            x = verhallen(x, RAEUME.get('wohnung'))[:n]
            x *= huelle_bett(von, n, -12, -26, -26)[:, None]
            fertig_betten.append((von, blende(x, 0.05, 0.25)))
        elif b[0] == 'musikbett' and musik is not None:
            _, von, bis = b
            n = int((bis - von + 2.5) * SR)
            x = musik[np.arange(n) % len(musik)].copy()
            x *= huelle_bett(von, n, -10, -21)[:, None]
            fertig_betten.append((von, blende(x, 1.5, 2.5)))
        elif b[0] == 'schluss' and musik is not None:
            von = b[1]
            bis = gesamt + 6.0
            n = int((bis - von) * SR)
            x = musik[np.arange(n) % len(musik)].copy()
            x *= huelle_bett(von, n, -10, -21)[:, None]
            fertig_betten.append((von, blende(x, 1.0, 5.0)))
            gesamt = bis
        elif isinstance(b[0], float):
            fertig_betten.append(b)

    mix = np.zeros((int(gesamt * SR) + 12 * SR, 2), dtype=np.float32)
    for s, a in [(s, a) for s, a, _ in stimme] + fertig_betten:
        n0 = int(s * SR)
        n1 = min(len(mix), n0 + len(a))
        mix[n0:n1] += a[:n1 - n0]
    mix = mix[:int(gesamt * SR)]

    wav = ausgabe.rsplit('.', 1)[0] + '.wav'
    with open(wav + '.raw', 'wb') as f:
        f.write(mix.astype(np.float32).tobytes())
    # Master: Lautheit −16 LUFS, Spitze −1,5 dBTP, zwei Durchgänge
    mess = subprocess.run(['ffmpeg', '-v', 'info', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', wav + '.raw',
                           '-af', 'loudnorm=I=-16:TP=-1.5:LRA=14:print_format=json', '-f', 'null', '-'],
                          capture_output=True, text=True).stderr
    j = json.loads(mess[mess.rfind('{'):mess.rfind('}') + 1])
    filt = (f'loudnorm=I=-16:TP=-1.5:LRA=14:measured_I={j["input_i"]}:measured_TP={j["input_tp"]}:'
            f'measured_LRA={j["input_lra"]}:measured_thresh={j["input_thresh"]}:offset={j["target_offset"]}:linear=true')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', wav + '.raw',
                    '-af', filt + ',aresample=44100', '-c:a', 'libmp3lame', '-b:a', '160k',
                    '-metadata', 'title=' + (_konf['titel'] if STUECK != 'manuskript' else '«Es ist an der Zeit» – Goethes Märchen und Rudolf Steiners mantrisches Spätwerk'),
                    '-metadata', 'artist=Sätzerei', '-metadata', 'comment=Synthetische Stimmen (ElevenLabs). Text und Produktion: Claude (Anthropic).',
                    ausgabe], check=True)
    os.remove(wav + '.raw')
    json.dump([{'t': round(a, 2), 'rolle': b, 'text': c} for a, b, c in marken],
              open(ausgabe.rsplit('.', 1)[0] + '.marken.json', 'w'), ensure_ascii=False, indent=0)
    print(f"Schnitte für Atem: {SCHNITT_STATISTIK['gesetzt']} gesetzt, {SCHNITT_STATISTIK['ausgelassen']} ausgelassen (keine Stille an der Stelle)")
    print(f'fertig: {ausgabe}  Länge {gesamt / 60:.1f} min  Sprache {sum(dauer_trocken.values()) / 60:.1f} min'
          f'  Musik {"ja" if musik is not None else "fehlt"}')


def glaetten(ziel, n):
    if n < 2:
        return ziel
    kern = np.ones(n, dtype=np.float32) / n
    pad = np.pad(ziel, (n // 2, n - n // 2 - 1), mode='edge')
    return np.convolve(pad, kern, mode='valid').astype(np.float32)


# ---------------------------------------------------------------- Befehle
def main():
    os.makedirs(CACHE, exist_ok=True)
    befehl = sys.argv[1] if len(sys.argv) > 1 else 'mischen'
    cues = lesen()
    if befehl == 'stimmen':
        nur = sys.argv[2] if len(sys.argv) > 2 else None
        reden = [c for c in cues if c['art'] == 'rede' and (nur is None or c['rolle'] == nur)]
        zeichen = sum(len(rede_text(c)[0]) for c in reden)
        print(f'{len(reden)} Zeilen, {zeichen} Zeichen')
        neu = 0
        with ThreadPoolExecutor(3) as ex:
            for k, frisch in ex.map(stimme_erzeugen, reden):
                neu += frisch
        print(f'neu erzeugt: {neu}')
    elif befehl == 'klaenge':
        for c in cues:
            if c['art'] in ('geraeusch', 'atmo'):
                k, frisch = klang_erzeugen('sfx', c['prompt'], c['s'])
                print('sfx', k, 'neu' if frisch else 'Cache', c['prompt'][:50])
        k, frisch = klang_erzeugen('mus', MUSIK_PROMPT, MUSIK_DAUER)
        print('mus', k, 'neu' if frisch else 'Cache')
    elif befehl == 'mischen':
        mischen(sys.argv[2] if len(sys.argv) > 2 else os.path.join(HIER, f'{STUECK}.mp3'))
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
