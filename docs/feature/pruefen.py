#!/usr/bin/env python3
"""Mischung gegen Manuskript prüfen (Claude kann nicht hören).

    python3 -I pruefen.py <manuskript.txt> <scribe.json>

scribe.json ist die Antwort von ElevenLabs Scribe auf die fertige MP3
(timestamps_granularity=word). Ausgegeben werden die Ähnlichkeit und jede
Abweichung mit Zeitmarke und Rolle: mitgesprochene Regie, verschluckte oder
verlesene Wörter, falsch gelesene Zahlen.
"""
import difflib, json, re, sys

ZAHLEN = {'129': 'hundertneunundzwanzig', '1795': 'siebzehnhundertfünfundneunzig', '1891': 'achtzehnhunderteinundneunzig',
          '1900': 'neunzehnhundert', '1910': 'neunzehnhundertzehn', '1918': 'neunzehnhundertachtzehn',
          '1924': 'neunzehnhundertvierundzwanzig', '1925': 'neunzehnhundertfünfundzwanzig', '2024': 'zweitausendvierundzwanzig',
          '11': 'elfter', '19': 'neunzehn', '24': 'vierundzwanzig', '27': 'siebenundzwanzigster', '30': 'dreissig',
          '39': 'neununddreissig', '49': 'neunundvierzig', '57': 'siebenundfünfzig', '63': 'dreiundsechzig'}


def norm(t):
    t = t.lower().replace('ß', 'ss').replace("'", '').replace('’', '')
    return ZAHLEN.get(re.sub(r'[^\wäöüé-]', '', t), re.sub(r'[^\wäöüé-]', '', t))


def main(manuskript, scribe):
    rollen = r'^([A-ZÄÖÜ]+)\|(.*)$'
    ref = []
    for z in open(manuskript, encoding='utf8'):
        m = re.match(rollen, z.rstrip('\n'))
        if m and m.group(1) not in ('STILLE', 'MUSIK', 'GERÄUSCH'):
            ref += [(norm(w), m.group(1)) for w in re.sub(r'\[[^\]]*\]', ' ', m.group(2)).split() if norm(w)]
    d = json.load(open(scribe))
    stt = [(norm(w['text']), w['start'], w['text']) for w in d['words'] if w.get('type') == 'word' and norm(w['text'])]
    a, b = [x[0] for x in ref], [x[0] for x in stt]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    print(f'Ähnlichkeit {sm.ratio():.3f}  ({len(a)} Wörter im Manuskript, {len(b)} erkannt)')
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        t = stt[min(j1, len(stt) - 1)][1]
        rolle = ref[min(i1, len(ref) - 1)][1]
        print(f'{op:8} {int(t // 60):02d}:{t % 60:04.1f} {rolle:10} Manuskript: {" ".join(a[i1:i2])[:50]!r:52} erkannt: {" ".join(x[2] for x in stt[j1:j2])[:50]!r}')


if __name__ == '__main__':
    main(*sys.argv[1:3])
