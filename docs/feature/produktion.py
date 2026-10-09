#!/usr/bin/env python3
"""Produktion des Features «Es ist an der Zeit».

    XI_KEY=… python3 -I produktion.py stimmen     # alle Sprechzeilen erzeugen (Cache)
    XI_KEY=… python3 -I produktion.py klaenge     # Geräusche und Musik erzeugen (Cache)
    python3 -I produktion.py mischen [ausgabe]    # aus dem Cache mischen, kostet nichts

Regie-Liste wie bei «Gewachsen, nicht gebaut» (ROLLE|Text, STILLE|n s,
MUSIK|…, GERÄUSCH|<Prompt>, n s). Unterschied: Eine Zeile wird in einem
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
    'lebendig': 'lively', 'klar': 'clear', 'wach': 'awake',
    'ohne die Stimme zu heben': 'without raising the voice', 'sachlich': None,
}
# Ein zweites Stück aus derselben Werkstatt: STUECK=essay liest essay.txt und essay.json
STUECK = os.environ.get('STUECK', 'manuskript')
if STUECK != 'manuskript':
    _konf = json.load(open(os.path.join(HIER, f'{STUECK}.json'), encoding='utf8'))
    STIMMEN = _konf['stimmen']
ATEM, PAUSE = 0.55, 1.10
LUECKE_WECHSEL, LUECKE_GLEICH = 0.85, 0.65


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
        else:
            raise SystemExit(f'Unbekannte Zeile: {z}')
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


def stimme_erzeugen(cue):
    text, _ = rede_text(cue)
    sid = STIMMEN[cue['rolle']]
    k = schluessel('tts', MODELL, sid, text)
    mp3, js = os.path.join(CACHE, f'tts_{k}.mp3'), os.path.join(CACHE, f'tts_{k}.json')
    if os.path.exists(mp3) and os.path.exists(js):
        return k, False
    antwort = anfrage(f'/v1/text-to-speech/{sid}/with-timestamps?output_format=mp3_44100_128',
                      {'text': text, 'model_id': MODELL, 'language_code': 'de'})
    open(mp3, 'wb').write(base64.b64decode(antwort['audio_base64']))
    json.dump({'text': text, 'alignment': antwort.get('alignment')}, open(js, 'w'), ensure_ascii=False)
    return k, True


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


def zuschneiden(x, schwelle=db(-48)):
    laut = np.where(np.abs(x).max(axis=1) > schwelle)[0]
    if not len(laut):
        return x
    a, e = max(0, laut[0] - int(0.02 * SR)), min(len(x), laut[-1] + int(0.06 * SR))
    return blende(x[a:e], 0.01, 0.03)


def rede_audio(cue):
    text, pausen = rede_text(cue)
    k = schluessel('tts', MODELL, STIMMEN[cue['rolle']], text)
    x = dekodieren(os.path.join(CACHE, f'tts_{k}.mp3'))
    al = json.load(open(os.path.join(CACHE, f'tts_{k}.json')))['alignment']
    zeichen, anf, end = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    if ''.join(zeichen) != text:
        print(f'  Hinweis: Zeitmarken passen nicht zum Text ({cue["rolle"]}: {text[:40]}…), Pausen entfallen')
        pausen = []
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
        luecke = max(0.0, t2 - t1)
        schnitte.append(((t1 + t2) / 2, max(0.12, dauer - luecke)))
    stuecke, letzt = [], 0
    for t, extra in schnitte:
        n = int(t * SR)
        stuecke.append(blende(x[letzt:n].copy(), 0.0 if not stuecke else 0.004, 0.004))
        stuecke.append(stille(extra))
        letzt = n
    stuecke.append(blende(x[letzt:].copy(), 0.004 if stuecke else 0.0, 0.0))
    return zuschneiden(np.concatenate(stuecke))


def mischen(ausgabe):
    cues = lesen()
    # 1. Sprache: Pegel je Stimme angleichen (−20 dBFS RMS)
    reden = {}
    for i, c in enumerate(cues):
        if c['art'] == 'rede':
            reden[i] = rede_audio(c)
    # je Zeile angleichen: −20 dBFS RMS, leise Zeilen 2,5 dB darunter, höchstens +12 dB Verstärkung
    for i, c in enumerate(cues):
        if c['art'] == 'rede':
            ziel = -22.5 if c['text'].startswith('[leise') else -20.0
            reden[i] = reden[i] * db(min(12.0, ziel - rms_db(reden[i])))

    musik = None
    mpfad = os.path.join(CACHE, f'mus_{schluessel("mus", MUSIK_PROMPT, str(MUSIK_DAUER))}.mp3')
    if os.path.exists(mpfad):
        musik = dekodieren(mpfad)
        musik *= db(-20 - rms_db(musik))

    # 2. Zeitleiste
    stimme = []        # (start, audio)
    betten = []        # (start, audio) Geräusche/Musik mit fertiger Hüllkurve
    t, vorige, wartet_stille = 0.0, None, False
    mus_start, mus_offen = None, False
    marken = []

    for i, c in enumerate(cues):
        if c['art'] == 'stille':
            t += c['s']
            wartet_stille = True
        elif c['art'] == 'rede':
            if vorige is not None and not wartet_stille:
                t += LUECKE_GLEICH if vorige == c['rolle'] else LUECKE_WECHSEL
            stimme.append((t, reden[i]))
            marken.append((t, c['rolle'], c['text'][:50]))
            t += len(reden[i]) / SR
            vorige, wartet_stille = c['rolle'], False
        elif c['art'] == 'geraeusch':
            k = schluessel('sfx', c['prompt'], str(c['s']))
            pfad = os.path.join(CACHE, f'sfx_{k}.mp3')
            if not os.path.exists(pfad):
                print(f'  fehlt: Geräusch «{c["prompt"][:50]}» — übersprungen')
                continue
            x = dekodieren(pfad)
            x *= db(-20 - rms_db(x))
            dauer = len(x) / SR
            if dauer <= 6:   # Ereignis: steht frei
                huelle = np.full(len(x), db(-4), dtype=np.float32)
                betten.append((t, blende(x * huelle[:, None], 0.05, 0.4)))
                t += dauer * 0.85
            else:            # Atmo: 3,2 s frei, dann leise unter der Sprache
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
                mus_start, mus_offen = t, True
                betten.append(('schluss', t))
                t += 4.0
                wartet_stille = True
                continue
            raise SystemExit(f'MUSIK unbekannt: {b}')

    gesamt = t + 4.0
    # Musikbetten: frei laut (−10 dB), unter Sprache leise (−21 dB)
    sprache_aktiv = np.zeros(int(gesamt * SR) + SR, dtype=bool)
    for s, a in stimme:
        n0 = int(s * SR)
        sprache_aktiv[n0:n0 + len(a)] = True
    fertig_betten = []
    for b in betten:
        if b[0] == 'musikbett' and musik is not None:
            _, von, bis = b
            n = int((bis - von + 2.5) * SR)
            idx = np.arange(n) % len(musik)
            x = musik[idx].copy()
            aktiv = sprache_aktiv[int(von * SR):int(von * SR) + n]
            aktiv = np.pad(aktiv, (0, max(0, n - len(aktiv))))[:n]
            ziel = np.where(aktiv, db(-21), db(-10)).astype(np.float32)
            huelle = glaetten(ziel, int(0.6 * SR))
            x *= huelle[:, None]
            fertig_betten.append((von, blende(x, 1.5, 2.5)))
        elif b[0] == 'schluss' and musik is not None:
            von = b[1]
            bis = gesamt + 6.0
            n = int((bis - von) * SR)
            idx = np.arange(n) % len(musik)
            x = musik[idx].copy()
            aktiv = sprache_aktiv[int(von * SR):int(von * SR) + n]
            aktiv = np.pad(aktiv, (0, max(0, n - len(aktiv))))[:n]
            ziel = np.where(aktiv, db(-21), db(-10)).astype(np.float32)
            x *= glaetten(ziel, int(0.6 * SR))[:, None]
            fertig_betten.append((von, blende(x, 1.0, 5.0)))
            gesamt = bis
        elif isinstance(b[0], float):
            fertig_betten.append(b)

    mix = np.zeros((int(gesamt * SR) + SR, 2), dtype=np.float32)
    for s, a in stimme + fertig_betten:
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
    print(f'fertig: {ausgabe}  Länge {gesamt / 60:.1f} min  Sprache {sum(len(a) for _, a in stimme) / SR / 60:.1f} min'
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
            if c['art'] == 'geraeusch':
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
