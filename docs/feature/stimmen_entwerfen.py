#!/usr/bin/env python3
"""Drei Stimmen für den Hör-Essay entwerfen und auswählen (ElevenLabs Voice Design).

    XI_KEY=… python3 -I stimmen_entwerfen.py            # entwerfen, prüfen, Vorschlag
    XI_KEY=… python3 -I stimmen_entwerfen.py speichern  # die gewählten im Konto ablegen

Claude kann nicht hören. Gewählt wird messbar: Die Spracherkennung (Scribe)
muss jedes Wort treffen, und das Tempo soll zur Rolle passen.
"""
import base64, difflib, json, os, re, subprocess, sys, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
ORDNER = os.path.join(HIER, 'entwuerfe')
API = 'https://api.elevenlabs.io'

ROLLEN = {
    'ESSAY': {
        'name': 'Essay-Tragend',
        'ziel': 12.0,
        'beschreibung': 'Perfect audio quality. A German woman in her fifties, native speaker of standard High German '
                        '(Hochdeutsch). A warm, resonant, grounded alto with natural depth, the carrying voice of a '
                        'cultural radio essayist. Calm and unhurried, elevated yet natural and personal, never pompous, '
                        'with gentle pauses between thoughts. Close, intimate microphone.',
        'text': 'Das Gespräch. Höher als das Gold. Höher als das Licht. Dieser Essay folgt einem Gespräch, das '
                'hundertneunundzwanzig Jahre umspannt. Es führt von Goethes Märchen zu den Sprüchen, die Rudolf '
                'Steiner am Ende seines Lebens an eine Tafel schrieb. Rudolf Steiner hat dieses Märchen nie '
                'losgelassen. Mit dreissig spricht er darüber in Wien, vor dem Goethe-Verein.',
    },
    'MÄRCHEN': {
        'name': 'Märchen-Frisch',
        'ziel': 13.0,
        'beschreibung': 'Perfect audio quality. A German man around thirty, native speaker of standard High German '
                        '(Hochdeutsch). A fresh, bright and lively storyteller with a light smile in his voice, clear '
                        'diction, playful but tender, reading a classic German fairy tale with a sense of wonder. '
                        'Natural pacing, never rushed.',
        'text': 'Als er vor die Tür hinaus trat, sah er zwei grosse Irrlichter über dem angebundenen Kahne schweben, '
                'die ihm versicherten, dass sie grosse Eile hätten und schon an jenem Ufer zu sein wünschten. '
                'Was ist herrlicher als Gold? fragte der König. Das Licht, antwortete die Schlange. Was ist '
                'erquicklicher als Licht? fragte jener. Das Gespräch, antwortete diese.',
    },
    'STEINER': {
        'name': 'Mantra-Weckend',
        'ziel': 10.0,
        'beschreibung': 'Perfect audio quality. A German man in his forties, native speaker of standard High German '
                        '(Hochdeutsch). A clear, luminous and awake baritone with quiet intensity, speaking slowly '
                        'and deliberately, every word placed with presence, a voice that awakens rather than soothes. '
                        'No pathos, no theatricality, never whispering.',
        'text': 'O Mensch, erkenne dich selbst! So tönt das Weltenwort. Erst wenn die drei von dir besiegt, werden '
                'Flügel deiner Seele wachsen, um den Abgrund zu übersetzen, der dich trennet vom Erkenntnisfelde. '
                'Die Macht, durch welche die Tugend wirkt, offenbart sich dem Willen. Die Weisheit offenbart sich '
                'dem Erkennen.',
    },
}


def anfrage(pfad, koerper=None, multipart=None):
    key = os.environ['XI_KEY']
    if multipart:
        grenze = 'grenze7f3a'
        teile = []
        for k, v in multipart.items():
            if isinstance(v, tuple):
                teile.append(f'--{grenze}\r\nContent-Disposition: form-data; name="{k}"; filename="{v[0]}"\r\n'
                             f'Content-Type: audio/mpeg\r\n\r\n'.encode() + v[1] + b'\r\n')
            else:
                teile.append(f'--{grenze}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
        daten = b''.join(teile) + f'--{grenze}--\r\n'.encode()
        kopf = {'xi-api-key': key, 'Content-Type': f'multipart/form-data; boundary={grenze}'}
    else:
        daten = json.dumps(koerper).encode()
        kopf = {'xi-api-key': key, 'Content-Type': 'application/json'}
    req = urllib.request.Request(API + pfad, data=daten, headers=kopf)
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())


def norm(t):
    return [w for w in re.sub(r'[^\wäöüß ]', ' ', t.lower().replace('ß', 'ss')).split() if w]


def entwerfen():
    os.makedirs(ORDNER, exist_ok=True)
    wahl = {}
    for rolle, r in ROLLEN.items():
        js = os.path.join(ORDNER, f'{rolle}.json')
        if os.path.exists(js):
            vor = json.load(open(js))
        else:
            a = anfrage('/v1/text-to-voice/design?output_format=mp3_44100_128',
                        {'voice_description': r['beschreibung'], 'model_id': 'eleven_ttv_v3', 'text': r['text']})
            vor = []
            for i, v in enumerate(a['previews']):
                pfad = os.path.join(ORDNER, f'{rolle}-{i + 1}.mp3')
                open(pfad, 'wb').write(base64.b64decode(v['audio_base_64']))
                vor.append({'nr': i + 1, 'entwurf': v['generated_voice_id'], 'pfad': pfad})
            json.dump(vor, open(js, 'w'), indent=1)
        beste = None
        for v in vor:
            if 'treffer' not in v:
                stt = anfrage('/v1/speech-to-text', multipart={'model_id': 'scribe_v1', 'language_code': 'de',
                                                              'file': ('p.mp3', open(v['pfad'], 'rb').read())})
                w = [x for x in stt['words'] if x.get('type') == 'word']
                sek = (w[-1]['end'] - w[0]['start']) if w else 1
                v['treffer'] = round(difflib.SequenceMatcher(None, norm(r['text']), norm(stt['text'])).ratio(), 3)
                v['tempo'] = round(len(r['text']) / sek, 1)
                v['erkannt'] = stt['text']
            v['wert'] = round(v['treffer'] * 10 - abs(v['tempo'] - r['ziel']) * 0.6, 2)
            if beste is None or v['wert'] > beste['wert']:
                beste = v
        json.dump(vor, open(js, 'w'), indent=1, ensure_ascii=False)
        for v in vor:
            print(f"{rolle:8} Entwurf {v['nr']}: Treffer {v['treffer']:.3f}  Tempo {v['tempo']:4.1f} Z/s  Wert {v['wert']}"
                  + ('   ← gewählt' if v is beste else ''))
        wahl[rolle] = beste
    json.dump({k: {'entwurf': v['entwurf'], 'nr': v['nr']} for k, v in wahl.items()},
              open(os.path.join(ORDNER, 'wahl.json'), 'w'), indent=1)


def speichern():
    wahl = json.load(open(os.path.join(ORDNER, 'wahl.json')))
    besetzung = {}
    for rolle, w in wahl.items():
        r = ROLLEN[rolle]
        a = anfrage('/v1/text-to-voice', {'voice_name': r['name'], 'voice_description': r['beschreibung'],
                                          'generated_voice_id': w['entwurf']})
        besetzung[rolle] = a['voice_id']
        print(rolle, r['name'], a['voice_id'])
    json.dump(besetzung, open(os.path.join(ORDNER, 'besetzung.json'), 'w'), indent=1)


if __name__ == '__main__':
    speichern() if sys.argv[1:] == ['speichern'] else entwerfen()
