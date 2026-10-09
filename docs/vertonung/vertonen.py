#!/usr/bin/env python3
"""«Nach innen» — Vertonung der Mantren der Ersten Klasse, Stunden 1–7 (Eleven Music).

    python3 -I vertonen.py plan 3                    # Kompositionsplan der Stunde 3 zeigen (kostet nichts)
    XI_KEY=… python3 -I vertonen.py bauen 1 2 3      # Stücke erzeugen (Cache: clips/), fertige MP3 nach ausgabe/
    XI_KEY=… python3 -I vertonen.py pruefen 1        # Scribe schreibt das Stück zurück, Vergleich mit dem Liedtext
    XI_KEY=… python3 -I vertonen.py guthaben         # Credit-Stand (nur mit Recht «User: Read»)

Der Liedtext kommt unverändert aus src/data/mantren.yaml (Lesefassung 2024).
Jede Stunde ist ein Stück; jeder Teil eines Mantrams ein Abschnitt (Chunk) mit
eigenem Klang. Stile auf Englisch (Vorgabe der API), keine Künstlernamen (die
API weist sie ab), der Text auf Deutsch.
"""
import difflib, hashlib, json, os, re, subprocess, sys, time, urllib.request, urllib.error, uuid

HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HIER, '..', '..'))
CACHE = os.path.join(HIER, 'clips')
AUSGABE = os.path.join(HIER, 'ausgabe')
API = 'https://api.elevenlabs.io'
MODELL = 'music_v2_5'
FORMAT = 'mp3_44100_192'

# ---------------------------------------------------------------- Klang des Zyklus
# Eine Stimme für den Hüter durch den ganzen Zyklus: eine Altstimme, nah am Mikrofon,
# leise, nie gehoben. Die Mantren sagen «der Hüter spricht» — er ist kein Mann, die
# Stimme ist eine Wahl (siehe README).
STIMME = ['female alto vocalist, very close to the microphone, breathy and quiet, intimate whisper-sung delivery',
          'lyrics sung in German with clear diction', 'every word intelligible', 'slow phrasing with space between lines']
GRUND = ['sacred minimalism', 'inward and contemplative', 'very slow', 'silence is part of the music',
         'warm analog recording', 'great production quality']
NIE = ['drum kit', 'rock drums', 'trap beat', 'rap', 'auto-tune pitch correction', 'EDM', 'cheesy', 'epic trailer',
       'sentimental film strings', 'stadium reverb', 'distorted electric guitar', 'English lyrics', 'spoken announcer',
       'loud', 'fast']

# Klangwelten (ohne Namen, die API lehnt Namen ab — jede Zeile ist eine Übersetzung der Inspiration):
KLAVIER = ['soft felt piano', 'sparse repeating arpeggios', 'simple diatonic harmony', 'single sustained notes left to ring']
TINTINNABULI = ['tintinnabuli texture: one voice moves stepwise while a second voice sounds only the notes of one triad',
                'bell-like sustained string tones', 'long silences between phrases', 'pure consonance']
AMBIENT = ['ambient', 'slowly evolving drone', 'generative texture with no pulse', 'tape-warm pads', 'deep sub bass felt more than heard']
GESCHICHTET = ['stacked vocal harmonies of the same voice, a choir made of one singer', 'vocoder-tinted harmonies',
               'falsetto layers', 'folktronica']
VIBRAPHON = ['vibraphone mallet patterns', 'minimalist chamber jazz', 'bass clarinet', 'gentle interlocking rhythms']
FLAMENCO = ['flamenco-inflected melisma', 'nylon-string guitar', 'sparse palmas handclaps', 'sudden a cappella moments',
            'modern production with sub bass']
GOLDBERG = ['aria and variations over a fixed ground bass', 'sarabande rhythm in slow triple meter', 'baroque voice-leading',
            'each strophe a new variation on the same bass line']
INDIE = ['German indie pop with orchestral strings', 'soft muted electronic pulse', 'warm synth pads', 'intimate pop vocal']
UNRUHE = ['unsettling', 'detuned bowed strings', 'low cello drones', 'sparse electronic glitches', 'odd meter', 'anxious']

# ---------------------------------------------------------------- die sieben Stücke
# Jeder Abschnitt: (Name, Quelle, Dauer s, Stile, Nicht-Stile, Regie im Text)
#   Quelle: (Mantram-ID, Teil-Nr.) → Zeilen aus mantren.yaml; None → ohne Text (Vorspiel, Zwischenspiel, Nachspiel)
#   Regie: Zeilen in geschweiften Klammern, die vor dem Text stehen ({whispered} …)
STUECKE = {
    1: {'titel': 'Erdengründe', 'mantren': ['1.1', '1.2', '1.3', '1.4'], 'tonart': 'D minor', 'tempo': '58 BPM',
        'welt': KLAVIER + TINTINNABULI,
        'teile': [
            ('Vorspiel', None, 14, KLAVIER + TINTINNABULI + ['instrumental introduction', 'a single piano note, then silence, then the arpeggio begins'], ['vocals'], ''),
            ('Erdengründe I', ('1.1', 0, 0, 8), 42, KLAVIER + TINTINNABULI + ['the voice enters almost speaking, on one or two notes'], [], ''),
            ('Erdengründe II', ('1.1', 0, 8, 16), 46, KLAVIER + TINTINNABULI + ['the harmony darkens', 'the piano thins out to single notes'], [], ''),
            ('Im Anblick der Schwelle', ('1.2', 0, 0, 12), 58, TINTINNABULI + ['strings only, no piano', 'the voice floats above sustained string tones', 'growing light'], ['piano'], ''),
            ('Das Tor', ('1.2', 0, 12, 13), 14, ['near silence', 'one low piano note', 'the voice speaks rather than sings'], ['strings'], '{spoken softly, almost whispered}'),
            ('Daseinswort', ('1.3', 0, 0, 12), 56, KLAVIER + TINTINNABULI + ['the full texture returns', 'wide and calm', 'the last line sung on one repeated note'], [], ''),
            ('Zwischenspiel', None, 10, UNRUHE + ['instrumental transition', 'the strings begin to detune'], ['vocals', 'piano'], ''),
            ('Der Abgrund', ('1.4', 0), 26, UNRUHE + ['the voice is tense and low'], ['piano'], ''),
            ('Das erste Tier', ('1.4', 1), 30, UNRUHE + ['dull blue colour: bone-dry pizzicato', 'hollow'], ['piano'], ''),
            ('Das zweite Tier', ('1.4', 2), 30, UNRUHE + ['yellow-grey colour: mocking, thin, nasal muted brass far away'], ['piano'], ''),
            ('Das dritte Tier', ('1.4', 3), 30, UNRUHE + ['dirty red colour: glassy high string harmonics', 'slack and limp'], ['piano'], ''),
            ('Flügel', ('1.4', 4), 34, KLAVIER + GESCHICHTET + ['the key turns to D major', 'the piano returns', 'hope without triumph'], UNRUHE, ''),
            ('Nachspiel', None, 14, KLAVIER + TINTINNABULI + ['instrumental ending', 'the opening arpeggio once more, then one note left to ring into silence'], ['vocals'], ''),
        ]},
    2: {'titel': 'Die drei Tiere', 'mantren': ['2'], 'tonart': 'A minor', 'tempo': 'no pulse',
        'welt': AMBIENT,
        'teile': [
            ('Vorspiel', None, 12, AMBIENT + ['instrumental introduction', 'a drone rises from silence'], ['vocals'], ''),
            ('Des Denkens', ('2', 0), 42, AMBIENT + ['whispered close-mic vocal, almost spoken', 'highest register of the three strophes'], [], '{whispered}'),
            ('Des Fühlens', ('2', 1), 42, AMBIENT + ['whispered close-mic vocal, almost spoken', 'middle register', 'the drone thickens'], [], '{whispered}'),
            ('Des Wollens', ('2', 2), 44, AMBIENT + ['the voice sinks to the lowest register', 'sub bass swells', 'the last line sung, not whispered'], [], ''),
            ('Nachspiel', None, 14, AMBIENT + ['instrumental ending', 'the drone thins to a single sine tone and fades'], ['vocals'], ''),
        ]},
    3: {'titel': 'Willens-Stoß', 'mantren': ['3'], 'tonart': 'F major', 'tempo': '84 BPM',
        'welt': VIBRAPHON,
        'teile': [
            ('Vorspiel', None, 10, VIBRAPHON + ['instrumental introduction', 'vibraphone alone, a four-note pattern'], ['vocals'], ''),
            ('Gedankenweben', ('3', 0), 40, VIBRAPHON + ['vibraphone alone under the voice', 'the voice is light and clear'], ['bass clarinet'], ''),
            ('Gefühle-Strömen', ('3', 1), 42, VIBRAPHON + ['bass clarinet enters', 'a gentle pulse appears', 'the harmony warms'], [], ''),
            ('Willens-Stoß', ('3', 2), 46, VIBRAPHON + GESCHICHTET + ['the stacked choir of one voice enters on the last two lines', 'rising', 'bright'], [], ''),
            ('Nachspiel', None, 12, VIBRAPHON + ['instrumental ending', 'the four-note pattern slows down and stops'], ['vocals'], ''),
        ]},
    4: {'titel': 'Tiefe – Weite – Höhe', 'mantren': ['4'], 'tonart': 'E minor to E major', 'tempo': '66 BPM',
        'welt': GESCHICHTET,
        'teile': [
            ('Vorspiel', None, 10, ['instrumental introduction', 'solo cello in the lowest register', 'double bass drone'] + GESCHICHTET[3:], ['vocals'], ''),
            ('Erdentiefen', ('4', 0), 42, ['male baritone vocalist in his lowest chest register, close and dark', 'cello and double bass only', 'heavy and slow'], ['falsetto', 'strings high'], ''),
            ('Weltenweiten', ('4', 1), 42, ['the same male voice in his warm middle register', 'warm string quartet enters', 'wide stereo image', 'loving'] + GESCHICHTET[:2], [], ''),
            ('Himmelshöhen', ('4', 2), 46, ['the same male voice now in pure falsetto', 'stacked falsetto harmonies'] + GESCHICHTET + ['high string harmonics', 'the key brightens to E major', 'weightless'], ['cello', 'double bass'], ''),
            ('Nachspiel', None, 14, GESCHICHTET + ['instrumental ending', 'wordless falsetto harmonies (ooh) dissolve into air'], [], '(ooh)'),
        ]},
    5: {'titel': 'Es kämpft', 'mantren': ['5'], 'tonart': 'E Phrygian', 'tempo': '72 BPM',
        'welt': FLAMENCO,
        'teile': [
            ('Vorspiel', None, 8, FLAMENCO + ['instrumental introduction', 'nylon-string guitar alone, one Phrygian cadence'], ['vocals'], ''),
            ('Licht und Finsternis', ('5', 0), 44, FLAMENCO + ['the voice fights: full and bright on «Licht», dark and low on «finstren»', 'a cappella on the last two lines'], [], ''),
            ('Warm und Kalt', ('5', 1), 44, FLAMENCO + ['palmas enter softly', 'warm melisma on «Wärme»', 'the sound turns cold and dry on «Kälte»', 'a cappella on the last two lines'], [], ''),
            ('Leben und Tod', ('5', 2), 46, FLAMENCO + ['the fullest strophe', 'sub bass under the guitar', 'then everything stops: the last line a cappella, barely voiced'], [], ''),
            ('Nachspiel', None, 10, FLAMENCO + ['instrumental ending', 'guitar alone, the Phrygian cadence once more, unresolved'], ['vocals'], ''),
        ]},
    6: {'titel': 'Erdenwerte', 'mantren': ['6'], 'tonart': 'G minor', 'tempo': '60 BPM in slow triple meter',
        'welt': GOLDBERG,
        'teile': [
            ('Aria', None, 14, GOLDBERG + KLAVIER + ['instrumental introduction', 'the ground bass alone on felt piano, eight bars'], ['vocals'], ''),
            ('Erde', ('6', 0), 40, GOLDBERG + KLAVIER + ['variation 1: piano alone under the voice'], [], ''),
            ('Wasser', ('6', 1), 40, GOLDBERG + KLAVIER + ['variation 2: a cello joins on the ground bass', 'flowing'], [], ''),
            ('Luft', ('6', 2), 40, GOLDBERG + ['variation 3: strings in long tones, no piano', 'cold and clear', 'the last line warms'], ['piano'], ''),
            ('Zwischenspiel', None, 8, INDIE + ['instrumental transition', 'a soft muted electronic pulse begins under sustained strings'], ['vocals'], ''),
            ('Licht', ('6', 3), 40, INDIE + GOLDBERG[:1] + ['variation 4: the ground bass now in the synth bass', 'the voice closer and more personal'], [], ''),
            ('Gestalt', ('6', 4), 40, INDIE + GOLDBERG[:1] + ['variation 5: orchestral strings swell gently', 'tender on «Liebe zu den Erdenwerten»'], [], ''),
            ('Leben', ('6', 5), 42, INDIE + GESCHICHTET[:1] + GOLDBERG[:1] + ['variation 6: the stacked choir carries the last two lines', 'the pulse stops before the final line'], [], ''),
            ('Aria da capo', None, 16, GOLDBERG + KLAVIER + ['instrumental ending', 'the ground bass alone on felt piano once more, slower, into silence'], ['vocals', 'electronic pulse'], ''),
        ]},
    7: {'titel': 'Schau die Drei', 'mantren': ['7.1', '7.2', '7.3'], 'tonart': 'D major', 'tempo': '58 BPM',
        'welt': KLAVIER + TINTINNABULI,
        'teile': [
            ('Vorspiel', None, 12, KLAVIER + TINTINNABULI + ['instrumental introduction', 'the same arpeggio as the first piece of the cycle, now in D major'], ['vocals'], ''),
            ('Schau die Drei', ('7.1', 0), 48, KLAVIER + TINTINNABULI + ['two female voices in canon, the second following the first one bar later', 'luminous'], [], ''),
            ('Des Kopfes Geist', ('7.2', 0), 24, TINTINNABULI + ['strings only, high and clear', 'a single voice'], ['piano'], ''),
            ('Des Herzens Seele', ('7.2', 1), 28, KLAVIER + ['piano only, warm middle register', 'a single voice'], ['strings'], ''),
            ('Der Glieder Kraft', ('7.2', 2), 24, KLAVIER + TINTINNABULI + ['piano and strings together', 'firm and quiet'], [], ''),
            ('Stille', None, 6, ['near silence', 'one sustained string tone only'], ['vocals', 'piano'], ''),
            ('Tritt ein', ('7.3', 0), 22, ['whispered first, then the three lines sung once in full open voice', 'wide and warm', 'the piano arpeggio returns under the last line'] + GESCHICHTET[:1], [], '{whispered}'),
            ('Nachspiel', None, 20, AMBIENT + KLAVIER[:1] + ['instrumental ending', 'the arpeggio dissolves into an ambient drone', 'long fade into silence'], ['vocals'], ''),
        ]},
}


# ---------------------------------------------------------------- Text aus mantren.yaml
def mantren_laden():
    import yaml
    d = yaml.safe_load(open(os.path.join(REPO, 'src', 'data', 'mantren.yaml'), encoding='utf8'))
    return {m['id']: m for m in d['mantren']}


def zeilen(mantren, quelle):
    mid, teil = quelle[0], quelle[1]
    lines = mantren[mid]['parts'][teil]['lines']
    if len(quelle) == 4:
        lines = lines[quelle[2]:quelle[3]]
    # Der Gesang braucht keine Gedankenstriche und Schrägstriche; Wortlaut bleibt.
    return [re.sub(r'\s*/\s*', ', ', z.replace('–', '').replace('  ', ' ')).strip() for z in lines]


def plan(nr, mantren=None):
    mantren = mantren or mantren_laden()
    st = STUECKE[nr]
    chunks = []
    for i, (name, quelle, dauer, plus, minus, regie) in enumerate(st['teile']):
        text = f'[{name}]'
        if regie:
            text += '\n' + regie
        if quelle:
            text += '\n' + '\n'.join(zeilen(mantren, quelle))
        stile = list(dict.fromkeys((STIMME if quelle else []) + plus + GRUND + [st['tonart'], st['tempo']]))
        nicht = list(dict.fromkeys(NIE + minus))
        if not quelle and 'vocals' not in nicht and '(ooh)' not in regie:
            nicht.append('vocals')
        chunks.append({'text': text, 'duration_ms': int(dauer * 1000), 'positive_styles': stile[:50],
                       'negative_styles': nicht[:50], 'context_adherence': 'high'})
    for c in chunks:
        for z in c['text'].split('\n'):
            assert len(z) <= 200, z
        assert 3000 <= c['duration_ms'] <= 120000, c['text'][:30]
    assert len(chunks) <= 30
    return {'chunks': chunks}


def dauer_s(p):
    return sum(c['duration_ms'] for c in p['chunks']) / 1000


# ---------------------------------------------------------------- ElevenLabs
def anfrage(pfad, koerper=None, binaer=False, versuche=4, methode=None, roh=None, kopf=None):
    key = os.environ['XI_KEY']
    for v in range(versuche):
        daten = roh if roh is not None else (json.dumps(koerper).encode() if koerper is not None else None)
        h = {'xi-api-key': key}
        h.update(kopf or ({'Content-Type': 'application/json'} if koerper is not None else {}))
        req = urllib.request.Request(API + pfad, data=daten, headers=h, method=methode)
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                aus = r.read()
                return aus if binaer else json.loads(aus)
        except urllib.error.HTTPError as e:
            text = e.read().decode('utf8', 'replace')[:600]
            if e.code in (429, 500, 502, 503, 504) and v < versuche - 1:
                time.sleep(6 * (v + 1))
                continue
            raise SystemExit(f'HTTP {e.code} {pfad}: {text}')
    raise SystemExit('keine Antwort')


def schluessel(p):
    return hashlib.sha1(json.dumps(p, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def bauen(nr, mantren):
    st = STUECKE[nr]
    p = plan(nr, mantren)
    k = schluessel(p)
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(AUSGABE, exist_ok=True)
    roh = os.path.join(CACHE, f'mus_{k}.mp3')
    if not os.path.exists(roh):
        print(f'Stunde {nr} «{st["titel"]}»: {len(p["chunks"])} Abschnitte, {dauer_s(p):.0f} s — erzeuge …', flush=True)
        t0 = time.time()
        daten = anfrage(f'/v1/music?output_format={FORMAT}', {'composition_plan': p, 'model_id': MODELL}, binaer=True)
        open(roh, 'wb').write(daten)
        json.dump(p, open(os.path.join(CACHE, f'mus_{k}.plan.json'), 'w'), ensure_ascii=False, indent=1)
        print(f'  {len(daten) / 1e6:.1f} MB in {time.time() - t0:.0f} s', flush=True)
    else:
        print(f'Stunde {nr} «{st["titel"]}»: aus dem Cache')
    ziel = os.path.join(AUSGABE, f'nach-innen-{nr}.mp3')
    mastern(roh, ziel, nr, st['titel'])
    laenge = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ziel],
                                  capture_output=True, text=True).stdout.strip() or 0)
    print(f'  fertig: {ziel}  {laenge / 60:.1f} min')
    return ziel


def mastern(roh, ziel, nr, titel):
    """Die Stücke kommen mit sehr verschiedener Lautheit aus dem Modell (−17 bis −31 LUFS). Master wie im
    Haus: −16 LUFS, −1,5 dBTP, zwei Durchgänge, linear (keine Verdichtung — die Stille bleibt Stille)."""
    mess = subprocess.run(['ffmpeg', '-v', 'info', '-i', roh, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=20:print_format=json',
                           '-f', 'null', '-'], capture_output=True, text=True).stderr
    j = json.loads(mess[mess.rfind('{'):mess.rfind('}') + 1])
    filt = (f'loudnorm=I=-16:TP=-1.5:LRA=20:measured_I={j["input_i"]}:measured_TP={j["input_tp"]}:'
            f'measured_LRA={j["input_lra"]}:measured_thresh={j["input_thresh"]}:offset={j["target_offset"]}:linear=true')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', roh, '-af', filt + ',aresample=44100', '-c:a', 'libmp3lame', '-b:a', '192k',
                    '-metadata', f'title={nr}. Stunde – {titel}', '-metadata', 'album=Nach innen – Mantren der Ersten Klasse',
                    '-metadata', f'track={nr}', '-metadata', 'artist=Sätzerei',
                    '-metadata', 'comment=Eleven Music (synthetisch). Text: Rudolf Steiner, Lesefassung 2024. Plan: Claude (Anthropic).',
                    ziel], check=True)


# ---------------------------------------------------------------- Prüfung (Claude kann nicht hören)
def norm(t):
    t = t.lower().replace('ß', 'ss').replace("'", '').replace('’', '').replace('´', '')
    return re.sub(r'[^\wäöüé-]', '', t)


def scribe(pfad):
    k = hashlib.sha1(open(pfad, 'rb').read()).hexdigest()[:16]
    js = os.path.join(CACHE, f'stt_{k}.json')
    if os.path.exists(js):
        return json.load(open(js))
    grenze = uuid.uuid4().hex
    felder = {'model_id': 'scribe_v1', 'language_code': 'deu', 'timestamps_granularity': 'word', 'diarize': 'false'}
    koerper = b''
    for n, w in felder.items():
        koerper += f'--{grenze}\r\nContent-Disposition: form-data; name="{n}"\r\n\r\n{w}\r\n'.encode()
    koerper += (f'--{grenze}\r\nContent-Disposition: form-data; name="file"; filename="x.mp3"\r\n'
                'Content-Type: audio/mpeg\r\n\r\n').encode() + open(pfad, 'rb').read() + f'\r\n--{grenze}--\r\n'.encode()
    d = anfrage('/v1/speech-to-text', roh=koerper, kopf={'Content-Type': f'multipart/form-data; boundary={grenze}'}, methode='POST')
    json.dump(d, open(js, 'w'), ensure_ascii=False)
    return d


def pruefen(nr, mantren):
    pfad = os.path.join(AUSGABE, f'nach-innen-{nr}.mp3')
    p = plan(nr, mantren)
    ref = []
    for c in p['chunks']:
        for z in c['text'].split('\n')[1:]:
            if z.startswith('{') or z.startswith('('):
                continue
            ref += [norm(w) for w in z.split() if norm(w)]
    d = scribe(pfad)
    stt = [(norm(w['text']), w['start'], w['text']) for w in d.get('words', []) if w.get('type') == 'word' and norm(w['text'])]
    b = [x[0] for x in stt]
    sm = difflib.SequenceMatcher(None, ref, b, autojunk=False)
    print(f'Stunde {nr}: Ähnlichkeit {sm.ratio():.3f}  ({len(ref)} Wörter im Text, {len(b)} erkannt)')
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        t = stt[min(j1, len(stt) - 1)][1] if stt else 0
        print(f'  {op:8} {int(t // 60):02d}:{t % 60:04.1f} Text: {" ".join(ref[i1:i2])[:55]!r:57} erkannt: {" ".join(x[2] for x in stt[j1:j2])[:55]!r}')
    return sm.ratio()


# ---------------------------------------------------------------- Befehle
def main():
    befehl = sys.argv[1] if len(sys.argv) > 1 else 'plan'
    nummern = [int(a) for a in sys.argv[2:]] or sorted(STUECKE)
    mantren = mantren_laden()
    if befehl == 'plan':
        for nr in nummern:
            p = plan(nr, mantren)
            print(f'# Stunde {nr} «{STUECKE[nr]["titel"]}» — {len(p["chunks"])} Abschnitte, {dauer_s(p) / 60:.1f} min, '
                  f'{sum(len(c["text"]) for c in p["chunks"])} Zeichen')
            print(json.dumps(p, ensure_ascii=False, indent=1))
        print(f'# Zyklus gesamt: {sum(dauer_s(plan(n, mantren)) for n in STUECKE) / 60:.1f} min')
    elif befehl == 'bauen':
        for nr in nummern:
            bauen(nr, mantren)
    elif befehl == 'pruefen':
        for nr in nummern:
            pruefen(nr, mantren)
    elif befehl == 'guthaben':
        d = anfrage('/v1/user/subscription')
        print(f'{d.get("character_count")} von {d.get("character_limit")} Credits verbraucht, Tarif {d.get("tier")}')
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
