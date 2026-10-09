#!/usr/bin/env python3
"""Lesbares Sendemanuskript mit Zeitmarken aus Regie-Liste und Marken der Mischung.

    python3 -I sendemanuskript.py feature   # manuskript.txt + es-ist-an-der-zeit.marken.json → sendemanuskript.md
    python3 -I sendemanuskript.py essay     # essay.txt + was-ist-erquicklicher-als-licht.marken.json → essay-sendemanuskript.md
"""
import json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
STUECKE = {
    'feature': {
        'quelle': 'manuskript.txt', 'marken': 'es-ist-an-der-zeit.marken.json', 'ziel': 'sendemanuskript.md',
        'titel': '«Es ist an der Zeit»', 'untertitel': 'Goethes Märchen und Rudolf Steiners mantrisches Spätwerk. Ein Feature',
        'rollen': {'ERZÄHLERIN': 'Erzählerin', 'CHRONIST': 'Chronist', 'GOETHE': 'Zitatorin (Goethe)',
                   'STEINER': 'Zitator (Steiner)', 'MANTRA': 'Stimme der Mantren'},
        'besetzung': 'Erzählerin (NWR Erzählerin) · Chronist (NWR Chronist) · Zitatorin Goethe (Märchen-Erzählerin, die Stimme der Textprobe) · Zitator Steiner (Christian Plasa) · Stimme der Mantren (Märchen-Leise)',
        'musik': 'Harfe',
    },
    'essay': {
        'quelle': 'essay.txt', 'marken': 'was-ist-erquicklicher-als-licht.marken.json', 'ziel': 'essay-sendemanuskript.md',
        'titel': '«Was ist erquicklicher als Licht?»', 'untertitel': 'Goethes Märchen und Rudolf Steiners mantrisches Spätwerk. Ein Hör-Essay',
        'rollen': {'ESSAY': 'Essay (tragend)', 'MÄRCHEN': 'Märchen (frisch)', 'STEINER': 'Steiner (weckend)', 'ANSAGE': 'Ansage'},
        'besetzung': 'Essay, tragend (Essay-Tragend) · Märchen (Märchen-Erzählerin, die Stimme der Textprobe) · Steiner, weckend: Prosa und Mantren (Leo Liest) · Ansage (NWR Chronist)',
        'musik': 'Cello und Harfe',
    },
}


def kopf(t):
    t = t.strip()
    return t[:1] + t[1:].lower().replace('—', '—') if t.isupper() else t


def main(name):
    s = STUECKE[name]
    marken = json.load(open(os.path.join(HIER, s['marken'])))
    zeiten = [m['t'] for m in marken if m['rolle'] != 'MUSIK']
    ende = max(m['t'] for m in marken)
    out = [f"# {s['titel']}", '', f"**{s['untertitel']}**", '', 'Sendemanuskript mit Zeitmarken', '',
           'Idee, Auftrag und Redaktion: Philipp Tok. Text und Produktion: Claude, ein Sprachmodell von Anthropic. '
           'Stimmen, Musik und Geräusche: ElevenLabs (synthetisch). Grundlage: [Studie](../studie-goethe-maerchen.md).', '',
           f"Stimmen: {s['besetzung']}. Goethe nach der Ausgabe letzter Hand, Schreibung modernisiert; Mantren nach der "
           'Lesefassung 2024. Regie *kursiv*.', '', '---', '']
    i = 0
    for z in open(os.path.join(HIER, s['quelle']), encoding='utf8'):
        z = z.rstrip('\n')
        if z.startswith('## '):
            k = z[3:]
            k = re.sub(r'^([IVX]+\. )?(.*)$', lambda m: (m.group(1) or '') + m.group(2).capitalize(), k)
            for alt, neu in (('— ein', '— Ein'), ('— drei', '— Drei'), ('könige', 'Könige'), ('fluss', 'Fluss'),
                             ('leser', 'Leser'), ('leben', 'Leben'), ('kraft', 'Kraft')):
                k = k.replace(alt, neu)
            out += ['', '## ' + k, '']
            continue
        if not z or z.startswith('#'):
            continue
        art, _, rest = z.partition('|')
        if art in s['rollen']:
            t = zeiten[i]
            i += 1
            txt = re.sub(r'\[Atem\]', ' ', rest)
            txt = re.sub(r'\[Pause\]', ' … ', txt)
            tags = re.findall(r'\[([^\]]+)\]', txt)
            txt = re.sub(r'\s+', ' ', re.sub(r'\s*\[[^\]]+\]\s*', ' ', txt)).strip().replace('vorübereiltst', "vorübereilt'st")
            out += [f'`{int(t // 60):02d}:{int(t % 60):02d}` **{s["rollen"][art]}**' + (f' *({", ".join(tags)})*' if tags else '') + '  ', txt, '']
        elif art == 'STILLE':
            out += [f'*Stille, {rest}*', '']
        elif art == 'MUSIK':
            out += [f"*Musik ({s['musik']}): {rest}*", '']
        elif art == 'GERÄUSCH':
            p, _, d = rest.rpartition(',')
            out += [f'*Geräusch ({d.strip()}): {p.strip()}*', '']
    assert i == len(zeiten), (i, len(zeiten))
    text = re.sub(r'\n{3,}', '\n\n', '\n'.join(out) + '\n')
    open(os.path.join(HIER, s['ziel']), 'w').write(text)
    print(s['ziel'], 'geschrieben')


if __name__ == '__main__':
    main(sys.argv[1])
