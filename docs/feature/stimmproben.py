#!/usr/bin/env python3
"""Stimmproben: dieselbe Probe je Kandidat, gemessen statt gehört (Besetzung «Was die Schlange weiss»).

    XI_KEY=… python3 -I stimmproben.py [ROLLE …]   # Proben in proben/, Messwerte in proben.json

Treffer (Scribe gegen Text), Tempo (Zeichen/s), Grundton (Median F0) und Behauchung:
Harmonizität (HNR) in stimmhaften Rahmen. Gehaucht = wenig Harmonizität.
"""
import difflib, json, os, re, subprocess, sys, urllib.request, urllib.error
import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
SR = 16000
API = 'https://api.elevenlabs.io'
KEY = os.environ['XI_KEY']

TEXTE = {
    'STEINER': 'Nicht die Erklärung, wohl aber die Anregungen zu seelischem Erleben, die mir von der Beschäftigung '
               'mit dem Märchen kamen, waren mir wichtig. Mir wurde, was sich an Seeleninhalt in Anlehnung an das '
               'Märchen ergab, ein wichtiger Meditationsstoff. Ich kam immer wieder darauf zurück.',
    'MARTIN': '[dryly] Dreiundvierzig. Dübellöcher. Ich hab sie gezählt, beim Zuspachteln. Er hat jedes Bild '
              'mindestens zweimal aufgehängt. [laughs] Kohl, Artischocken und Zwiebeln. Das ist ein Mann, der weiss, '
              'was er will.',
    'HÜTER2': '[serious, slowly] Meine Schwelle aber ist gezimmert aus einem jeglichen Furchtgefühl, das noch in dir ist. Hat verstanden dein Geist?',
    'HÜTER': 'Meine Schwelle aber ist gezimmert aus einem jeglichen Furchtgefühl, das noch in dir ist, und aus einer '
             'jeglichen Scheu vor der Kraft, die volle Verantwortung für all dein Tun und Denken selbst zu übernehmen.',
}
KANDIDATEN = {
    'STEINER': {'Hermann': 'b0JqlN5qkeuPi5BoQiHn', 'Karl Wien': 'l0E9rrjDouDB5F727FDZ',
                'Maximilian warm': 'LdrOKpb095fRo6KyS8jU', 'Peter Lang': 'EQIVtVkE7IWwwaRgwyPi',
                'Oskar Baumann': 'VDWBRvOTjy2gFBaEo68H'},
    'MARTIN': {'Andres CH': 'BfwuiKSWxqDOcSYQr6EC', 'Aleks CH': 'LNwPw7XMcJYCXyh2Bo4I',
               'Mats': 'HvPMqVH31pBg9ThkOUPw', 'Piet': '2QhwfRSog8ArO9AfgYMU', 'Sam': 'XUjIlSlGtOp4c6lq8Lbz'},
    'HÜTER': {'Elderbark': '2HmIg4yvRgcH2ZDgiwGz', 'Axel Jones mystisch': 'MWiQPmyHkBd29kLWn9T1',
              'Kathy (Frau)': '9VojQrRhoFFUbqyNRsxF', 'Hartmut Werner': 'qsEcR8IqZUmxT1rxm9G9',
              'Leo Liest (bisher)': '9T2VzpdyzVPMLIjcYVqp'},
    'HÜTER2': {'Kathy (Frau)': '9VojQrRhoFFUbqyNRsxF', 'Hartmut Werner': 'qsEcR8IqZUmxT1rxm9G9',
               'Nikolaus': 'uYBtrwzOqK8qaectN0V2', 'Leo Liest (bisher)': '9T2VzpdyzVPMLIjcYVqp'},
}


def post(pfad, koerper=None, multipart=None):
    if multipart:
        g = 'g7f3a'
        teile = []
        for k, v in multipart.items():
            if isinstance(v, tuple):
                teile.append(f'--{g}\r\nContent-Disposition: form-data; name="{k}"; filename="{v[0]}"\r\n'
                             f'Content-Type: audio/mpeg\r\n\r\n'.encode() + v[1] + b'\r\n')
            else:
                teile.append(f'--{g}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
        daten, kopf = b''.join(teile) + f'--{g}--\r\n'.encode(), {'Content-Type': f'multipart/form-data; boundary={g}'}
    else:
        daten, kopf = json.dumps(koerper).encode(), {'Content-Type': 'application/json'}
    kopf['xi-api-key'] = KEY
    try:
        with urllib.request.urlopen(urllib.request.Request(API + pfad, data=daten, headers=kopf), timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f'HTTP {e.code} {pfad}: {e.read().decode("utf8", "replace")[:300]}')


def norm(t):
    t = re.sub(r'\[[^\]]+\]', ' ', t)
    return [w for w in re.sub(r'[^\wäöüß ]', ' ', t.lower().replace('ß', 'ss')).split() if w]


def messen(pfad):
    roh = subprocess.run(['ffmpeg', '-v', 'error', '-i', pfad, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(roh, dtype=np.float32)
    fr, hop = int(0.04 * SR), int(0.01 * SR)
    f0, hnr = [], []
    pegel = 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    for a in range(0, len(x) - fr, hop):
        s = x[a:a + fr] - x[a:a + fr].mean()
        e = np.sqrt(np.mean(s ** 2))
        if 20 * np.log10(e + 1e-9) < pegel - 6:
            continue
        ac = np.correlate(s, s, 'full')[fr - 1:]
        ac /= ac[0] + 1e-12
        lo, hi = int(SR / 400), int(SR / 70)
        k = lo + int(np.argmax(ac[lo:hi]))
        r = ac[k]
        if r > 0.45:
            f0.append(SR / k)
            hnr.append(10 * np.log10(min(r, 0.999) / (1 - min(r, 0.999))))
    return (float(np.median(f0)) if f0 else 0, float(np.median(hnr)) if hnr else 0,
            len(f0) / max(1, (len(x) - fr) // hop))


def main():
    os.makedirs(os.path.join(HIER, 'proben'), exist_ok=True)
    nur = sys.argv[1:] or list(KANDIDATEN)
    erg = {}
    for rolle in nur:
        text = TEXTE[rolle]
        for name, vid in KANDIDATEN[rolle].items():
            pfad = os.path.join(HIER, 'proben', f'{rolle}-{name.replace(" ", "_")}.mp3')
            if not os.path.exists(pfad):
                open(pfad, 'wb').write(post(f'/v1/text-to-speech/{vid}?output_format=mp3_44100_128',
                                            {'text': text, 'model_id': 'eleven_v4', 'language_code': 'de'}))
            stt = json.loads(post('/v1/speech-to-text', multipart={
                'model_id': 'scribe_v1', 'language_code': 'de', 'file': ('p.mp3', open(pfad, 'rb').read())}))
            w = [x for x in stt.get('words', []) if x.get('type') == 'word']
            sek = (w[-1]['end'] - w[0]['start']) if w else 1
            treffer = difflib.SequenceMatcher(None, norm(text), norm(stt['text'])).ratio()
            f0, hnr, stimmhaft = messen(pfad)
            tempo = len(re.sub(r'\[[^\]]+\]', '', text)) / sek
            erg[f'{rolle}/{name}'] = dict(treffer=round(treffer, 3), tempo=round(tempo, 1), f0=round(f0),
                                          hnr=round(hnr, 1), stimmhaft=round(stimmhaft, 2), erkannt=stt['text'])
            print(f'{rolle:8} {name:22} Treffer {treffer:.3f}  Tempo {tempo:4.1f} Z/s  F0 {f0:5.0f} Hz  '
                  f'HNR {hnr:4.1f} dB  stimmhaft {stimmhaft:.2f}', flush=True)
    alt = json.load(open(os.path.join(HIER, 'proben.json'))) if os.path.exists(os.path.join(HIER, 'proben.json')) else {}
    alt.update(erg)
    json.dump(alt, open(os.path.join(HIER, 'proben.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
