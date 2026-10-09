#!/usr/bin/env python3
"""«Nach innen» — Vertonung der Mantren der Ersten Klasse als Vorlagen (Eleven Music).

    python3 -I vertonen.py plan 3                    # Kompositionsplan der Vorlage 3 zeigen (kostet nichts)
    XI_KEY=… python3 -I vertonen.py bauen 1 2 3      # Vorlagen erzeugen (Cache: clips/), fertige MP3 nach ausgabe/
    XI_KEY=… python3 -I vertonen.py pruefen 1        # Scribe schreibt das Stück zurück, Vergleich mit dem Liedtext
    XI_KEY=… python3 -I vertonen.py guthaben         # Credit-Stand (nur mit Recht «User: Read»)

Der Liedtext kommt unverändert aus src/data/mantren.yaml (Lesefassung 2024).
Jede Vorlage ist eine Sinneinheit (ein Titel der Lesefassung) in einem Ansatz;
jeder Teil des Mantrams ein Abschnitt (Chunk) mit eigenem Klang. Stile auf Englisch (Vorgabe der API), keine Künstlernamen (die
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

# ---------------------------------------------------------------- Haltung (Runde 2, 9. 10. 2026)
# «Es braucht keinen künstlichen Ernst oder starken seelischen Ausdruck. Die Gesangsstimme, die
# Töne schaffen die Erlebnisse. Die oder der Singende stellt sich zur Verfügung.» — darum keine
# Hauch-Stimme mehr, kein Pathos; Instrumente echt, in einem Raum; Harmonik darf fordern.
DIENT = ['plain unaffected delivery: the singer serves the text and does not emote', 'no vibrato, straight tone',
         'lyrics in German, every word intelligible']
ECHT = ['real acoustic instruments recorded in a real room', 'natural room reverb', 'complex, slowly shifting harmony',
        'great production quality']
NIE = ['cheap synth pads', 'preset synthesizer sounds', 'stock ambient pad', 'new age', 'digital reverb wash',
       'rock drums', 'trap beat', 'rap', 'auto-tune pitch correction', 'EDM', 'epic trailer', 'cheesy', 'sentimental',
       'theatrical', 'dramatic emoting', 'heavy vibrato', 'breathy ASMR whisper', 'English lyrics', 'loud']
GOLDBERG = ['aria and variations over a fixed ground bass', 'sarabande rhythm in slow triple meter', 'baroque voice-leading',
            'each strophe a new variation on the same bass line']

# ---------------------------------------------------------------- die Vorlagen
# Jede Vorlage: eine Sinneinheit (Titel der Lesefassung), ein Ansatz. Abschnitte:
#   (Name, Quelle, Dauer s, Stile, Nicht-Stile, Regie im Text)
#   Quelle: (Mantram-ID, Teil-Nr.[, von, bis]) → Zeilen aus mantren.yaml; None → ohne Text
#   Regie: Zeile in geschweiften Klammern vor dem Text ({spoken} …); Laute in runden ((mmm))
BARDO = ['Tibetan singing bowls struck and left to ring', 'low tanpura-like string drone', 'solo violin harmonics',
         'recorded in a large stone room', 'no pulse']
VORLAGEN = [
    {'nr': 1, 'slug': 'erdengruende-bardo', 'titel': 'Erdengründe', 'text': '1.1',
     'ansatz': 'Gesprochen über Klangschalen, Bordun und Geige, wie eine Anweisung an jemanden, der hinübergeht.',
     'tonart': 'drone on D', 'tempo': 'no pulse', 'stimme': ['spoken word: a calm female speaking voice reciting plainly, unhurried', 'spoken, not sung'],
     'teile': [
        ('Eingang', None, 12, BARDO + ['instrumental introduction', 'one bowl, silence, a second bowl'], [], ''),
        ('Erdengründe', ('1.1', 0, 0, 8), 44, BARDO + ['a gong once at the end of the section'], [], '{spoken}'),
        ('Finsternis', ('1.1', 0, 8, 16), 46, BARDO + ['the drone deepens', 'a second, lower speaking voice doubles the last two lines'], [], '{spoken}'),
        ('Ausgang', None, 12, BARDO + ['instrumental ending', 'the bowls ring out into silence'], [], ''),
     ]},
    {'nr': 2, 'slug': 'erdengruende-litanei', 'titel': 'Erdengründe', 'text': '1.1',
     'ansatz': 'Derselbe Text als Litanei: auf einem Ton rezitiert, Kadenz am Zeilenende, Harmonium und Cello.',
     'tonart': 'D Dorian', 'tempo': 'free, speech rhythm', 'stimme': ['liturgical chant on a single reciting tone with a small cadence at the end of each line', 'female voice', 'medieval plainchant style'],
     'teile': [
        ('Eingang', None, 8, ['Indian harmonium drone', 'cello sustained', 'instrumental introduction'], [], ''),
        ('Erdengründe', ('1.1', 0, 0, 8), 44, ['Indian harmonium drone', 'cello sustained'], [], ''),
        ('Finsternis', ('1.1', 0, 8, 16), 46, ['Indian harmonium drone', 'cello sustained', 'a second voice joins a fifth below on the cadences, organum'], [], ''),
        ('Ausgang', None, 8, ['Indian harmonium drone', 'cello sustained', 'instrumental ending'], [], ''),
     ]},
    {'nr': 3, 'slug': 'daseinswort-chor', 'titel': 'Daseinswort', 'text': '1.3',
     'ansatz': 'A cappella, gemischter Chor in langsamen Akkorden; die letzte Zeile im Unisono.',
     'tonart': 'A minor with cluster harmony', 'tempo': 'very slow', 'stimme': ['mixed a cappella choir SATB, slow homophonic chords', 'Renaissance polyphony meeting modern cluster harmony', 'straight tone'],
     'teile': [
        ('Daseinswort', ('1.3', 0, 0, 11), 60, ['recorded in a stone chapel', 'the chords shift under each line'], [], ''),
        ('Erkenne dich', ('1.3', 0, 11, 12), 20, ['the whole choir in unison on one low note, then the chord opens wide'], [], ''),
        ('Nachklang', None, 10, ['the last chord held, wordless hum, fading'], [], '(mmm)'),
     ]},
    {'nr': 4, 'slug': 'daseinswort-ruf-und-antwort', 'titel': 'Daseinswort', 'text': '1.3',
     'ansatz': 'Derselbe Text als Ruf und Antwort: gesprochen, dann singt der Chor aus einer Stimme das Daseinswort.',
     'tonart': 'F major', 'tempo': '60 BPM', 'stimme': [],
     'teile': [
        ('Eingang', None, 8, ['felt piano, a single repeated note', 'bowed upright bass', 'instrumental introduction'], [], ''),
        ('Aus den Weiten', ('1.3', 0, 0, 6), 40, ['a male speaking voice says each line plainly', 'spoken, not sung', 'felt piano', 'bowed upright bass'], [], '{spoken}'),
        ('Da ertönet', ('1.3', 0, 6, 11), 36, ['the same male speaking voice', 'spoken, not sung', 'stacked vocal harmonies of one female voice hum underneath and grow'], [], '{spoken}'),
        ('Das Daseinswort', ('1.3', 0, 11, 12), 26, ['now sung: a stacked choir made of one female voice, harmonized in wide chords', 'the line sung twice, slowly, no other words'], [], ''),
        ('Ausgang', None, 8, ['felt piano', 'instrumental ending'], [], ''),
     ]},
    {'nr': 5, 'slug': 'schwelle-hueter', 'titel': 'Im Anblick der Schwelle', 'text': '1.2',
     'ansatz': 'Der Hüter als verfremdete Stimme (Oktave tiefer, Vocoder), halb gesprochen; die letzte Zeile unverfremdet und leise.',
     'tonart': 'C minor', 'tempo': 'slow', 'stimme': [],
     'teile': [
        ('Eingang', None, 10, ['bowed metal, waterphone', 'violin', 'warm analog modular synth bass through a real speaker', 'instrumental introduction'], [], ''),
        ('Geistesbote', ('1.2', 0, 0, 9), 50, ['a low male voice pitch-shifted down an octave through a vocoder, half spoken half sung on a few notes', 'a voice of authority, dry and close', 'violin long tones above', 'analog synth bass'], [], ''),
        ('Abgrund', ('1.2', 0, 9, 12), 24, ['the same processed low voice', 'only the written lines, no improvised words', 'the texture thins', 'waterphone'], [], ''),
        ('Das Tor', ('1.2', 0, 12, 13), 14, ['the processing drops away: an unprocessed quiet female voice speaks the line plainly', 'spoken, not sung', 'near silence'], [], '{spoken}'),
        ('Ausgang', None, 8, ['violin alone', 'instrumental ending'], [], ''),
     ]},
    {'nr': 6, 'slug': 'drei-tiere-sprechgesang', 'titel': 'Drei Tiere', 'text': '1.4',
     'ansatz': 'Sprechgesang, trocken, in 7/8; jedes Tier ein Instrument (Kontrabassklarinette, präpariertes Klavier, Glasharmonika); «Flügel» wird zum ersten Mal gesungen.',
     'tonart': 'E minor', 'tempo': '7/8, slow irregular pulse', 'stimme': ['talk-singing (Sprechgesang) female voice, matter-of-fact'],
     'teile': [
        ('Eingang', None, 8, ['bass clarinet', 'prepared piano', 'dry close-miked', 'instrumental introduction'], [], ''),
        ('Das erste Tier', ('1.4', 1), 30, ['contrabass clarinet, bone-dry', 'muted and hollow'], [], ''),
        ('Das zweite Tier', ('1.4', 2), 30, ['prepared piano with metallic buzz', 'thin and mocking'], [], ''),
        ('Das dritte Tier', ('1.4', 3), 30, ['glass harmonica, glassy high tones', 'slack'], [], ''),
        ('Flügel', ('1.4', 4), 34, ['the voice sings for the first time, a simple rising line, plainly', 'strings enter', 'open'], [], ''),
        ('Ausgang', None, 8, ['strings', 'instrumental ending'], [], ''),
     ]},
    {'nr': 7, 'slug': 'willens-stoss-lied', 'titel': 'Willens-Stoß', 'text': '3',
     'ansatz': 'Ein Lied: dieselbe schlichte Melodie für alle drei Strophen, Gitarre und Kontrabass, ein Sänger, der nicht vorträgt.',
     'tonart': 'G major', 'tempo': '76 BPM', 'stimme': ['male voice singing simply, like a folk singer who does not perform', 'a plain unadorned melody, the same for every strophe'],
     'teile': [
        ('Vorspiel', None, 8, ['steel-string acoustic guitar fingerpicking', 'upright bass', 'recorded live in a wooden room', 'instrumental introduction'], [], ''),
        ('Strophe 1', ('3', 0), 34, ['steel-string acoustic guitar fingerpicking', 'upright bass'], [], ''),
        ('Strophe 2', ('3', 1), 34, ['steel-string acoustic guitar fingerpicking', 'upright bass', 'a second voice in parallel thirds'], [], ''),
        ('Strophe 3', ('3', 2), 36, ['steel-string acoustic guitar fingerpicking', 'upright bass', 'accordion joins', 'fuller'], [], ''),
        ('Nachspiel', None, 8, ['acoustic guitar', 'instrumental ending'], [], ''),
     ]},
    {'nr': 8, 'slug': 'schau-die-drei-hell', 'titel': 'Schau die Drei · Tritt ein', 'text': '7.1 + 7.3',
     'ansatz': 'Hell und leicht: Celesta, Nylongitarre, gebürstete Trommel, eine klare Popstimme; «Tritt ein» a cappella.',
     'tonart': 'C major', 'tempo': '96 BPM', 'stimme': ['light clear female pop voice, unforced, with a slight smile'],
     'teile': [
        ('Intro', None, 6, ['celesta', 'glockenspiel', 'nylon-string guitar', 'soft brushed drums', 'German indie pop', 'bright and playful', 'instrumental introduction'], [], ''),
        ('Schau die Drei', ('7.1', 0), 46, ['celesta', 'nylon-string guitar', 'soft brushed drums', 'German indie pop', 'bright and playful'], [], ''),
        ('Tritt ein', ('7.3', 0), 16, ['the beat stops', 'a cappella with a stacked harmony of the same voice'], ['drums'], ''),
        ('Outro', None, 8, ['celesta', 'instrumental ending'], [], ''),
     ]},
    {'nr': 9, 'slug': 'erdenwerte-I', 'titel': 'Erdenwerte I', 'text': '6 (Erde, Wasser, Luft)',
     'ansatz': 'Der Ansatz der Erstfassung, als eigenes Lied: Variationen über einen festen Bass, Filzklavier, Cello, Streicher.',
     'tonart': 'G minor', 'tempo': '60 BPM in slow triple meter', 'stimme': ['female voice'],
     'teile': [
        ('Aria', None, 10, GOLDBERG + ['soft felt piano', 'the ground bass alone', 'instrumental introduction'], [], ''),
        ('Erde', ('6', 0), 36, GOLDBERG + ['soft felt piano', 'variation 1: piano alone under the voice'], [], ''),
        ('Wasser', ('6', 1), 36, GOLDBERG + ['soft felt piano', 'variation 2: a cello joins on the ground bass', 'flowing'], [], ''),
        ('Luft', ('6', 2), 36, GOLDBERG + ['variation 3: strings in long tones, no piano', 'cold and clear'], ['piano'], ''),
        ('Ausgang', None, 8, GOLDBERG + ['soft felt piano', 'the ground bass once more, slower', 'instrumental ending'], [], ''),
     ]},
    {'nr': 10, 'slug': 'erdenwerte-II', 'titel': 'Erdenwerte II', 'text': '6 (Licht, Gestalt, Leben)',
     'ansatz': 'Die zweite Hälfte der Erstfassung als eigenes Lied: Streicher, leiser elektronischer Puls, der Chor aus einer Stimme am Ende.',
     'tonart': 'G minor to B flat major', 'tempo': '60 BPM', 'stimme': ['female voice, close and personal'],
     'teile': [
        ('Eingang', None, 8, ['sustained strings', 'soft muted electronic pulse', 'warm analog synth bass', 'instrumental introduction'], [], ''),
        ('Licht', ('6', 3), 36, GOLDBERG[:1] + ['sustained strings', 'soft muted electronic pulse', 'the ground bass in the synth bass', 'German indie pop with orchestral strings'], [], ''),
        ('Gestalt', ('6', 4), 36, GOLDBERG[:1] + ['orchestral strings swell gently', 'soft muted electronic pulse', 'German indie pop with orchestral strings'], [], ''),
        ('Leben', ('6', 5), 38, GOLDBERG[:1] + ['a stacked choir of the same voice carries the last two lines', 'the pulse stops before the final line'], [], ''),
        ('Ausgang', None, 10, ['strings alone', 'instrumental ending', 'fading'], [], ''),
     ]},
    {'nr': 11, 'slug': 'es-kaempft-zwei-stimmen', 'titel': 'Es kämpft', 'text': '5',
     'ansatz': 'Zwei Stimmen: eine spricht den Text, eine hält lange Töne auf den Schlüsselwörtern; Streichquartett in wandernden Dissonanzen.',
     'tonart': 'B minor, dissonant', 'tempo': 'slow', 'stimme': ['a male speaking voice reads plainly', 'spoken, not sung', 'a female singing voice holds single long wordless tones over the key words'],
     'teile': [
        ('Eingang', None, 8, ['string quartet harmonics', 'bowed vibraphone', 'instrumental introduction'], [], ''),
        ('Licht und Finsternis', ('5', 0), 38, ['string quartet in slowly shifting dissonant chords that resolve late'], [], '{spoken}'),
        ('Warm und Kalt', ('5', 1), 38, ['string quartet', 'the held tones rise', 'bowed vibraphone'], [], '{spoken}'),
        ('Leben und Tod', ('5', 2), 40, ['string quartet', 'the held tone stays alone after the last line'], [], '{spoken}'),
        ('Ausgang', None, 8, ['one sustained tone, then silence', 'instrumental ending'], [], ''),
     ]},
    {'nr': 12, 'slug': 'tiefe-weite-hoehe-vocoder', 'titel': 'Tiefe – Weite – Höhe', 'text': '4',
     'ansatz': 'Eine Stimme durch den Harmonizer: die Akkorde machen den Raum — tief und eng, weit und offen, hoch und schimmernd.',
     'tonart': 'E minor to E major', 'tempo': '64 BPM', 'stimme': ['talk-sung male voice through a vocoder harmonizer, many-voiced chords from one voice', 'folktronica'],
     'teile': [
        ('Eingang', None, 8, ['vocoder chord, wordless', 'cello', 'instrumental introduction'], [], '(ooh)'),
        ('Erdentiefen', ('4', 0), 36, ['a low dense cluster chord', 'cello and double bass', 'narrow'], [], ''),
        ('Weltenweiten', ('4', 1), 36, ['a wide open chord', 'string quartet', 'stereo width'], [], ''),
        ('Himmelshöhen', ('4', 2), 36, ['a high shimmering chord, falsetto layers', 'string harmonics', 'E major'], ['cello', 'double bass'], ''),
        ('Ausgang', None, 8, ['vocoder chord fading, wordless', 'instrumental ending'], [], '(ooh)'),
     ]},
]
# ---------------------------------------------------------------- Stimmenprobe (Runde 3, 9. 10. 2026)
# «Gerne mehr Stimmen. Reifere! Charaktervollere!» — Eleven Music vergibt keine Stimm-IDs; die Stimme
# ist eine Beschreibung. Zehn Stimmen singen oder sprechen denselben Text (7.2, Des Hüters letzte
# Mahnung), jede in der Besetzung, die zu ihr passt. Die Haltung bleibt: dienen, nicht vortragen.
def stimme(nr, slug, titel, ansatz, stimme, instrumente, tonart, tempo, haltung=None, regie='', dauern=(6, 24, 26, 24, 8)):
    return {'nr': nr, 'slug': f'stimme-{slug}', 'titel': titel, 'text': '7.2', 'ansatz': ansatz, 'stimme': stimme,
            'tonart': tonart, 'tempo': tempo, 'haltung': haltung,
            'teile': [('Eingang', None, dauern[0], instrumente + ['instrumental introduction'], [], ''),
                      ('Des Kopfes Geist', ('7.2', 0), dauern[1], instrumente, [], regie),
                      ('Des Herzens Seele', ('7.2', 1), dauern[2], instrumente, [], regie),
                      ('Der Glieder Kraft', ('7.2', 2), dauern[3], instrumente, [], regie),
                      ('Ausgang', None, dauern[4], instrumente + ['instrumental ending'], [], '')]}


SPRECHEND = ['spoken word, not sung', 'speaks plainly, serves the text', 'every word intelligible, German']
VORLAGEN += [
    stimme(13, 'alt-siebzig', 'Die Alte', 'Eine Frau um siebzig, verwitterte Altstimme mit Korn und Luft, mehr gesprochen als gesungen; Harmonium und Cello.',
           ['a weathered contralto, a woman around seventy, grain and air in the voice, unhurried, half speaks half sings on few notes', 'lived-in, warm, unforced'],
           ['Indian harmonium drone', 'cello sustained', 'recorded close in a quiet room'], 'D Dorian', 'free, speech rhythm'),
    stimme(14, 'bariton-alt', 'Der alte Mann', 'Ein alter Mann, brüchiger tiefer Bariton, halb gesprochen, müde und freundlich; Nylongitarre.',
           ["an old man's cracked low baritone, half spoken, world-weary and kind", 'rough edges, breath audible, no polish'],
           ['nylon-string guitar, slow fingerpicking', 'upright bass', 'recorded in a wooden room'], 'A minor', '64 BPM'),
    stimme(15, 'mezzo-lied', 'Die Liedsängerin', 'Eine ausgebildete Mezzosopranistin um sechzig, volle Stimme, aber schlicht vorgetragen; Klavier wie ein Kunstlied.',
           ['a trained mezzo-soprano around sixty, full mature voice with natural warmth, art song (Lied) delivery kept plain', 'rich lower register, controlled'],
           ['grand piano, art song accompaniment, sparse', 'recorded in a concert hall'], 'E flat major', '60 BPM',
           haltung=['the singer serves the text and does not dramatize', 'lyrics in German, every word intelligible']),
    stimme(16, 'bass-moench', 'Der Bass', 'Ein sehr tiefer Bass, Mönchsgesang, über einem Bordun aus Männerstimmen; a cappella.',
           ['a very deep basso profondo, Orthodox church bass, monastic chant', 'enormous low notes, slow, dark'],
           ['a cappella', 'a drone of low male voices humming underneath', 'recorded in a stone monastery'], 'low C', 'very slow'),
    stimme(17, 'jazz-rauchig', 'Die Jazzsängerin', 'Eine rauchige Jazzsängerin um fünfundfünfzig, dunkles Timbre, singt hinter dem Beat; Klaviertrio, gebürstet.',
           ['a smoky jazz singer in her mid-fifties, dark timbre, sings behind the beat, conversational phrasing', 'husky, intimate, late-night'],
           ['jazz piano trio', 'upright bass', 'brushed drums, very soft', 'slow ballad', 'recorded live in a small club'], 'D flat major', '58 BPM ballad',
           haltung=['the singer serves the text, no vocal acrobatics', 'lyrics in German, every word intelligible']),
    stimme(18, 'tenor-kantor', 'Der Kantor', 'Ein alter Kantor, dünner heller Tenor, Melismen über einer Shrutibox; fast allein.',
           ["an elderly cantor's tenor, thin and bright, slightly nasal, long melismatic lines", 'liturgical, unaccompanied feel, ornamented'],
           ['shruti box drone', 'otherwise unaccompanied', 'recorded in a synagogue-like hall'], 'E Phrygian dominant', 'free, unmeasured'),
    stimme(19, 'countertenor', 'Der Countertenor', 'Ein reifer Countertenor, rein und leicht körnig; Gambe und Theorbe.',
           ['a mature countertenor, pure head voice with a slight grain, early music style', 'floating, precise'],
           ['viola da gamba', 'theorbo', 'early music chamber', 'recorded in a chapel'], 'G minor', 'slow, in 3'),
    stimme(20, 'volkssaengerin', 'Die Volkssängerin', 'Eine ältere ungeschulte Sängerin, nasal, mit dem Ruf-Klang nordischer Hirtenlieder; eine Fiedel, sonst nichts.',
           ['an untrained older woman folk singer, nasal and bright, the open calling tone of Nordic herding songs', 'raw, outdoors, no polish'],
           ['solo fiddle, sparse, between the lines', 'outdoor air, distant space'], 'A Mixolydian', 'free'),
    stimme(21, 'schauspielerin', 'Die Schauspielerin', 'Eine Theaterschauspielerin um fünfundsechzig, nur gesprochen, trocken und genau; Klangschalen und Geige.',
           ['a stage actress around sixty-five, dry, precise stage diction, warm low speaking voice'] + SPRECHEND,
           ['Tibetan singing bowls', 'solo violin harmonics', 'low string drone', 'no pulse', 'recorded in a large stone room'], 'drone on D', 'no pulse',
           haltung=SPRECHEND, regie='{spoken}'),
    stimme(22, 'kabarett-bariton', 'Der Kabarettist', 'Ein trockener Kabarett-Bariton der zwanziger Jahre, spricht-singt mit Biss, leicht ironisch; Klavier und gedämpfte Trompete.',
           ['a dry cabaret baritone in the style of 1920s Berlin theatre song, speak-singing with bite, slightly ironic, never sentimental', 'crisp consonants'],
           ['upright piano, cabaret', 'muted trumpet', 'clarinet', 'recorded in a small theatre'], 'F minor', '72 BPM, slow tango feel',
           haltung=['the singer serves the text', 'lyrics in German, every word intelligible']),
]
# ---------------------------------------------------------------- Figuren (Runde 4, 9. 10. 2026)
# Rückmeldung auf Runde 2 und 3: Gesang, nicht Sprechen. Nähe und tonale Objektivität. Kein Pathos,
# keine Sentimentalität. Drei Figurenarten: der Hüter (erkennbar, eine grosse Seele in der Stimme —
# die Jazzerin ohne Klischee), der Mensch (in Nuancen und Gesten), die Engel/Götter (aus anderen
# Welten; die Chöre bleiben den späteren Stunden vorbehalten). Pausen für den Sinn (Lehre aus 9).
HUETERIN = ['a mature contralto with jazz-trained phrasing: exact pitch, dark warm timbre, flexible conversational timing, a big soul serving the text',
            'no smoky-bar cliché, no scoops, no breathiness, no swing']
MENSCH = ['a plain male voice, close and personal, tonally exact, like a person speaking in song',
          'the persona present and serving, never self-absorbed, the voice used like an instrument']
ANDERE_WELT = ['a single high clear voice from another world, glassy, with a microtonal shimmer around it', 'not a choir',
               'weightless, precise, strange']
PAUSEN = ['a rest after every line, the accompaniment waits', 'unhurried: the sense of each line lands before the next']


def studie(nr, slug, titel, figur, ansatz, stimme, tonart, tempo, teile, vor=3, nach=4, instrumente=None, ref=None):
    """Kurze Studie: Vorspiel 3 s, Textabschnitte, Nachspiel 4 s. teile: (Name, Quelle, Dauer, Stile[, Regie])."""
    instrumente = instrumente or (teile[0][3] if teile else [])
    t = [('Eingang', None, vor, instrumente + ['instrumental introduction, brief'], [], '')]
    for teil in teile:
        name, quelle, dauer, stile = teil[:4]
        t.append((name, quelle, dauer, stile + PAUSEN, [], teil[4] if len(teil) > 4 else ''))
    t.append(('Ausgang', None, nach, instrumente + ['instrumental ending, brief'], [], ''))
    return {'nr': nr, 'slug': slug, 'titel': titel, 'text': figur, 'ansatz': ansatz, 'stimme': stimme,
            'tonart': tonart, 'tempo': tempo, 'teile': t, 'ref': ref}


TINT = ['tintinnabuli: the voice moves stepwise, a viola sounds only the notes of one triad', 'a single bell', 'piano, single notes left to ring']
VORLAGEN += [
    studie(23, 'weltenwort', 'Weltenwort', 'Hüter · Erste Tafel',
           'Der Hüter als Weltenwort: Tintinnabuli (Stimme schrittweise, Bratsche auf dem Dreiklang, eine Glocke), eine Pause nach jeder Zeile.',
           HUETERIN, 'A minor', 'very slow', [('Weltenwort', ('erste-tafel', 0, 0, 8), 44, TINT)]),
    studie(24, 'abgrund', 'Am Abgrund', 'Hüter · 1.4',
           'Der Hüter am Abgrund: ein Solocello wie in einer Suite, die Stimme im Kontrapunkt dazu.',
           HUETERIN, 'E minor', 'sarabande, slow', [('Der Abgrund', ('1.4', 0), 36, ['solo cello like a Baroque suite sarabande', 'the voice in counterpoint with the cello line', 'nothing else'])]),
    studie(25, 'erstes-tier', 'Das erste Tier', 'Hüter · 1.4',
           'Die Beschreibung des Tiers aus liebevollem Interesse: ein Klavier-Ostinato, das den inneren Raum langsam weitet; Aufmerksamkeit statt Gefühl.',
           HUETERIN, 'D minor', '66 BPM', [('Das erste Tier', ('1.4', 1), 40, ['felt piano ostinato that slowly widens the inner space', 'patient, attentive tone, describing a frightened creature with care', 'warm, exact, never sentimental'])]),
    studie(26, 'ruhesterne', 'O Mensch', 'Hüter · 9.1',
           'Die Lehre des Hüters mit dem Ruf «O Mensch»: jeder Ruf anders verziert (Melisma), sparsame Palmas, sauberer Subbass, sonst leer.',
           HUETERIN, 'E Phrygian', '70 BPM', [('Erde und Wasser', [('9.1', 1), ('9.1', 2)], 28, ['melisma on «O Mensch», each call ornamented differently', 'sparse palmas handclaps', 'deep clean sub bass', 'otherwise empty space']),
                                              ('Luft und Feuer', [('9.1', 3), ('9.1', 4)], 28, ['melisma on «O Mensch»', 'sparse palmas handclaps', 'deep clean sub bass', 'the space fills a little'])]),
    studie(27, 'wo-ist', 'Wo ist der Erde Festigkeit', 'Hüter und Mensch · 14.1',
           'Der Hüter fragt, die Seele antwortet dreifach in einer Stimme: christlich schlicht und offen, luziferisch hoch und zu schön, ahrimanisch hart und hämmernd.',
           HUETERIN, 'B minor', 'slow', [('Die Frage', ('14.1', 0), 12, ['string quartet sustained'] + HUETERIN),
                                        ('Christus', ('14.1', 2), 10, MENSCH + ['plain, warm, straight tone, open vowels', 'string quartet sustained']),
                                        ('Luzifer', ('14.1', 3), 10, MENSCH + ['the same voice now high, airy, ornamented, sweet, floating upward, slightly too beautiful', 'glass harmonica']),
                                        ('Ahriman', ('14.1', 4), 10, MENSCH + ['the same voice now low, clipped, percussive, hard consonants, hammering rhythm', 'col legno strings'])],
           instrumente=['string quartet sustained']),
    studie(28, 'ich-trat', 'Ich trat in diese Sinnes-Welt', 'Mensch · Dritte Tafel',
           'Der Mensch als Ich: Choralharmonik am Klavier, ein Akkord je Zeile, die Stimme obenauf; Nähe und tonale Objektivität.',
           MENSCH, 'G major', 'chorale, slow', [('Ich trat', ('dritte-tafel', 0), 46, ['four-part chorale harmony on piano, one chord per line, the voice on top', 'clear cadences', 'syllabic: one note per syllable, the words exactly as written'])]),
    studie(29, 'hat-verstanden', 'Hat verstanden dein Geist?', 'Hüter und Ich · 16.2',
           'Zwiegespräch: der Hüter fragt über Harmonium und Cello (der Klang aus Vorlage 2), das Ich antwortet über Klavierakkorden.',
           HUETERIN, 'D Dorian', 'free, speech rhythm',
           [('Frage 1', ('16.2', 0), 7, HUETERIN + ['Indian harmonium drone', 'cello sustained']),
            ('Antwort 1', ('16.2', 1), 16, MENSCH + ['piano chords, sparse']),
            ('Frage 2', ('16.2', 2), 7, HUETERIN + ['Indian harmonium drone', 'cello sustained']),
            ('Antwort 2', ('16.2', 3), 16, MENSCH + ['piano chords, sparse']),
            ('Frage 3', ('16.2', 4), 7, HUETERIN + ['Indian harmonium drone', 'cello sustained']),
            ('Antwort 3', ('16.2', 5), 16, MENSCH + ['piano chords, sparse', 'the harmonium returns under the last line'])],
           instrumente=['Indian harmonium drone', 'cello sustained']),
    studie(30, 'empfinde', 'Empfinde, wie wir empfinden', 'Hüter und Engel · 15.1',
           'Der Hüter fragt; Angeloi, Archangeloi, Archai antworten in einer einzigen hohen Stimme aus einer anderen Welt, jede Hierarchie eine Stufe höher; Glasharmonika, gestrichene Crotales.',
           HUETERIN, 'F sharp, open', 'no pulse',
           [('Die Frage', ('15.1', 0), 9, HUETERIN + ['glass harmonica', 'bowed crotales']),
            ('Angeloi', ('15.1', 2), 9, ANDERE_WELT + ['glass harmonica', 'bowed crotales']),
            ('Archangeloi', ('15.1', 3), 9, ANDERE_WELT + ['a step higher', 'glass harmonica']),
            ('Archai', ('15.1', 4), 9, ANDERE_WELT + ['another step higher, at the edge of hearing', 'bowed crotales'])],
           instrumente=['glass harmonica', 'bowed crotales']),
    studie(31, 'feuermaechte', 'Mein Ich ist IHR', 'Mensch · 19+',
           'Der Mensch vor den Hierarchien: Klavier und Streicher schwellen langsam, strahlend und doch schlicht, sakral ohne Pathos.',
           MENSCH, 'E major', 'slow', [('Feuermächte', ('19+', 0), 42, ['piano and strings slowly swelling', 'radiant but plain', 'sacral without pathos', 'the last line held long'])], nach=5),
]
# ---------------------------------------------------------------- Doppelstimme (Runde 5, 9. 10. 2026)
# Rückmeldung auf Runde 4: 26 ein Treffer, 27 trifft, 29 hat Seele, 30 sehr gut — das Zusammenklingen
# ist die Spur; weniger Effekt, mehr Akustik. Keine romantischen, maskulinen Arien (23–25). 31 schön,
# aber Kirchenhall weckt falsche Assoziationen. Idee: der Hüter weiblich, als Doppelstimme, immer
# ineinanderklingend, die Dominanz leicht nach Inhalt wechselnd. Und mit den Rollen arbeiten: zwei
# sprechen miteinander, existenzielle Begegnung.
DOPPEL = ['two female voices, a contralto and a mezzo-soprano, always sounding together, interweaving in close harmony',
          'one voice slightly leads and the lead shifts with the sense of the line', 'acoustic, no effects, no electronics',
          'exact, plain, no vibrato, serving the text']
ICH = ['a single plain human voice, mid-range, close, warm, no vibrato, not operatic', 'alone, exposed, honest']
AKUSTISCH_FERN = ['a single high clear voice, otherworldly through purity and unusual intervals, not through effects',
                  'acoustic, dry, close', 'not a choir']
VORLAGEN += [
    studie(32, 'doppelstimme-schau-die-drei', 'O schau die Drei', 'Hüter als Doppelstimme · 7.1',
           'Der Hüter als Doppelstimme: Alt und Mezzo immer zusammen, ineinander, die Führung wechselt mit dem Sinn; nur eine gehaltene Bratsche.',
           DOPPEL, 'A minor', 'slow', [('Schau die Drei', ('7.1', 0), 46, ['a single sustained viola underneath, nothing else'])],
           instrumente=['a single sustained viola']),
    studie(33, 'doppelstimme-erste-hierarchie', 'Was wird aus der Lüfte Reizgewalt', 'Hüter als Doppelstimme und erste Hierarchie · 15.3',
           'Der Hüter fragt als Doppelstimme; Throne, Cherubine, Seraphine antworten in einer einzigen hohen Stimme, jede eine Stufe höher — akustisch, ohne Effekt, über Flageoletts einer Geige.',
           DOPPEL, 'F sharp, open', 'no pulse',
           [('Die Frage', ('15.3', 0), 10, DOPPEL + ['solo violin harmonics']),
            ('Throne', ('15.3', 2), 9, AKUSTISCH_FERN + ['solo violin harmonics']),
            ('Cherubine', ('15.3', 3), 9, AKUSTISCH_FERN + ['a step higher', 'solo violin harmonics']),
            ('Seraphine', ('15.3', 4), 9, AKUSTISCH_FERN + ['another step higher, at the edge of hearing', 'solo violin harmonics'])],
           instrumente=['solo violin harmonics']),
    studie(34, 'begegnung-hat-verstanden', 'Hat verstanden dein Geist?', 'Hüter als Doppelstimme und Ich · 16.2',
           'Existenzielle Begegnung mit getrennten Rollen: der Hüter fragt als Doppelstimme über Cello und Bratsche, das Ich antwortet allein, eine einzige schlichte Stimme über je einem tiefen Klavierton.',
           DOPPEL, 'D minor', 'free, speech rhythm',
           [('Frage 1', ('16.2', 0), 7, DOPPEL + ['cello and viola sustained']),
            ('Antwort 1', ('16.2', 1), 16, ICH + ['one low piano note per line, nothing else']),
            ('Frage 2', ('16.2', 2), 7, DOPPEL + ['cello and viola sustained']),
            ('Antwort 2', ('16.2', 3), 16, ICH + ['one low piano note per line, nothing else']),
            ('Frage 3', ('16.2', 4), 7, DOPPEL + ['cello and viola sustained']),
            ('Antwort 3', ('16.2', 5), 16, ICH + ['one low piano note per line', 'the cello returns very softly under the last line'])],
           instrumente=['cello and viola sustained']),
]
# ---------------------------------------------------------------- Der Dialog (Runde 6, 9. 10. 2026)
# Rückmeldung auf Runde 5: «Deutscher Gospel? Komm bitte aus der Kirche raus. Lieber skandinavische
# Landschaften. Das Ineinander-Duo dachte ich zweigeschlechtlich. Kein Fallenlassen in eine Melodie.
# Alles gestalten, wach werden lassen von innen. Langsam überraschen. Dehnen. Wecken. Halten.
# Konzentration. Die Einzelstimme des Menschen fehlt. Realisiere zuerst die Situation und gewinne von
# da die Stilmittel.» — 16.2 ist eine intime Höhepunktsituation: Der Hüter verabschiedet sich und
# übergibt seine Rolle dem Menschen. Er fragt tastend, der Mensch antwortet aus der erwachenden
# inneren Stimme; am Ende ist er eingeweiht, gekrönt und gezeptert wie der Prinz im Märchen. Weniger
# Jubilieren; die Hallelujas an den richtigen Stellen.
NORDEN = ['Nordic folk colours: a single fiddle with drone strings, a plucked kantele, sparse',
          'cool clear air, wide open landscape, dry wooden-room acoustics', 'no church, no organ, no reverb wash']
GESTALTEN = ['everything shaped, no melody to fall into: each line a shaped gesture', 'slow surprises: a stretched syllable, a held note, a sudden quiet',
             'concentration, awake, inward']
HUETER_DUO = ['the Guardian as a duo: one female and one male voice always sounding together, interwoven, never apart',
              'asked tentatively, quietly, unhurried, as if about to let go']
NIE_KIRCHE = ['gospel', 'choir', 'church organ', 'cathedral reverb', 'jubilant', 'hallelujah', 'triumphant', 'pop ballad', 'swelling strings']


def dialog(nr, slug, mensch, mensch_wort):
    ich = [mensch, 'alone, a single voice, never doubled', 'the awakening inner voice: begins almost without tone, like inner speech becoming sound, and gains tone line by line',
           'held notes, stretched syllables, honest, no ornament']
    return {'nr': nr, 'slug': slug, 'titel': 'Hat verstanden dein Geist?', 'text': f'Hüter (Duo) und Mensch ({mensch_wort}) · 16.2',
            'ansatz': f'Der Abschied des Hüters: das Duo aus Frau und Mann fragt dreimal tastend, der Mensch ({mensch_wort}) antwortet allein aus der erwachenden inneren Stimme; einmal, bei «Mögen klingend schaffen mein Ich», klingen die Harmonien hörbar; am Ende steht er aufrecht, ohne Jubel. Norden statt Kirche.',
            'stimme': [], 'tonart': 'D, open modal', 'tempo': 'free, slow, speech rhythm',
            'teile': [
                ('Eingang', None, 4, NORDEN + ['a single fiddle drone, cool and clear', 'instrumental introduction, brief'], NIE_KIRCHE, ''),
                ('Frage 1', ('16.2', 0), 7, HUETER_DUO + ['the female voice slightly leading'] + NORDEN + GESTALTEN + ['fiddle drone only'], NIE_KIRCHE, ''),
                ('Antwort 1', ('16.2', 1), 16, ich + GESTALTEN + ['no accompaniment except a faint fiddle drone far away', 'a held breath before the last line'], NIE_KIRCHE, ''),
                ('Frage 2', ('16.2', 2), 7, HUETER_DUO + ['both voices equal, gentler than the first question'] + NORDEN + GESTALTEN + ['fiddle drone only'], NIE_KIRCHE, ''),
                ('Antwort 2', ('16.2', 3), 17, ich + GESTALTEN + ['on the last two lines the kantele enters and the two Guardian voices quietly sound with the human in harmony for a moment: the harmonies become audible, then withdraw'], NIE_KIRCHE, ''),
                ('Frage 3', ('16.2', 4), 7, HUETER_DUO + ['the male voice slightly leading', 'firm but tender, the last question'] + NORDEN + GESTALTEN + ['fiddle drone only'], NIE_KIRCHE, ''),
                ('Antwort 3', ('16.2', 5), 18, ich + GESTALTEN + ['grounded now: a very soft frame drum pulse and the fiddle', 'the voice standing upright, calm authority without triumph', 'the last line held and released into silence'], NIE_KIRCHE, ''),
                ('Ausgang', None, 6, NORDEN + ['fiddle drone and kantele fade', 'one struck kantele tone, then silence', 'instrumental ending, brief'], NIE_KIRCHE, ''),
            ]}


VORLAGEN += [
    dialog(35, 'dialog-hat-verstanden-er', 'a young man, light plain tenor-range voice, close, unforced, no vibrato', 'junger Mann'),
    dialog(36, 'dialog-hat-verstanden-sie', 'a young woman, light plain mid-range voice, close, unforced, no vibrato', 'junge Frau'),
]
# ---------------------------------------------------------------- Der Dialog als Montage (Runde 7, 9. 10. 2026)
# Rückmeldung auf 35: «Eine Stimme nur? Wo ist die Harmonie der Doppelstimme? Warum hat der Mensch
# dieselbe Stimme wie der Hüter? Frage jagt Antwort als wäre es ein Satz. Klare Grundelemente und
# Gliederung bitte! Keine hoppelnde Melodie. Ein Gewahrwerden, kein Volkstänzchen, eher ein Erwachen
# in eine neue, höhere Wirklichkeit.»
# Grundelemente: (1) der Bordun auf D, in beiden Liedern; (2) das Duo, Frau und Mann, gehaltene Töne in
# Quinte oder Terz, beide hörbar, die Frage offen endend; (3) die Einzelstimme, eine junge Frau, auf
# einem Ton beginnend, schrittweise, kein Puls; (4) die Stille zwischen Frage und Antwort; (5) eine
# einzige Blüte bei «Mögen klingend schaffen mein Ich».
BORDUN = ['a low sustained cello drone on D underneath, nothing else', 'no pulse, no rhythm, no dance']
LANGSAM = ['very slow, long held tones, stepwise motion, mostly repeated notes, no leaps', 'no melody to fall into',
           'dry intimate acoustics, no reverb wash']
DUO_FM = ['two voices, one female contralto and one male baritone, singing together in sustained parallel harmony a fifth or a third apart, both clearly audible at all times',
          'the question left open, rising slightly at the end', 'tentative, quiet, letting go, serving the text',
          'lyrics in German, every word intelligible', 'no vibrato']
MENSCHIN = ['a single young woman, light clear voice, alone, never doubled, no harmony',
            'begins almost on one repeated pitch, like inner speech becoming tone, and gains tone line by line',
            'syllabic, no ornament, plain, serving the text', 'lyrics in German, every word intelligible', 'no vibrato']
VORLAGEN += [
    {'nr': 37, 'slug': 'montage-hat-verstanden', 'titel': 'Hat verstanden dein Geist?', 'text': 'Hüter (Duo) und Mensch · 16.2, montiert',
     'ansatz': 'Hüter und Mensch getrennt erzeugt, über demselben Bordun auf D, dann mit echter Stille montiert: das Duo aus Frau und Mann fragt in gehaltenen Quinten, die junge Frau antwortet allein, schrittweise, ohne Puls; eine Blüte bei «Mögen klingend schaffen mein Ich».',
     'stimme': [], 'tonart': 'D, open modal, drone on D', 'tempo': 'very slow, no pulse',
     'montage': {
        'lieder': {
            'hueter': {'nicht': NIE_KIRCHE + ['solo voice', 'single voice'],
                       'teile': [('Bordun', None, 5, BORDUN + ['the cello drone alone, instrumental']),
                                 ('Frage 1', ('16.2', 0), 9, DUO_FM + BORDUN + LANGSAM + ['the female voice slightly stronger']),
                                 ('Frage 2', ('16.2', 2), 9, DUO_FM + BORDUN + LANGSAM + ['both voices equal, gentler']),
                                 ('Frage 3', ('16.2', 4), 9, DUO_FM + BORDUN + LANGSAM + ['the male voice slightly stronger, the last question, tender'])]},
            'mensch': {'nicht': NIE_KIRCHE + ['duet', 'two voices', 'drums', 'percussion'],
                       'teile': [('Antwort 1', ('16.2', 1), 18, MENSCHIN + LANGSAM + ['a faint cello drone on D far away', 'a held breath before the last line']),
                                 ('Antwort 2', ('16.2', 3), 19, MENSCHIN + LANGSAM + ['a faint cello drone on D', 'on the last two lines a single kantele chord blooms once and the voice opens a little, then quiet again']),
                                 ('Antwort 3', ('16.2', 5), 19, MENSCHIN + LANGSAM + ['brighter, more open register, the drone opens to a fifth', 'calm, upright, awake, no triumph', 'the last line held long into silence'])]},
        },
        'folge': [('hueter', 0, 0.0), ('hueter', 1, 2.5), ('mensch', 0, 3.0), ('hueter', 2, 2.5), ('mensch', 1, 3.0), ('hueter', 3, 2.5), ('mensch', 2, 0.0)],
        'schluss': 4.0,
     }},
]
VORLAGE = {v['nr']: v for v in VORLAGEN}


# ---------------------------------------------------------------- Text aus mantren.yaml
def mantren_laden():
    import yaml
    d = yaml.safe_load(open(os.path.join(REPO, 'src', 'data', 'mantren.yaml'), encoding='utf8'))
    return {m['id']: m for m in d['mantren']}


def zeilen(mantren, quelle):
    if isinstance(quelle, list):
        return [z for q in quelle for z in zeilen(mantren, q)]
    mid, teil = quelle[0], quelle[1]
    lines = mantren[mid]['parts'][teil]['lines']
    if len(quelle) == 4:
        lines = lines[quelle[2]:quelle[3]]
    # Der Gesang braucht keine Gedankenstriche und Schrägstriche; Wortlaut bleibt.
    return [re.sub(r'\s*/\s*', ', ', z.lstrip('/').replace('–', '').replace('  ', ' ')).strip() for z in lines]


def plan(nr, mantren=None):
    mantren = mantren or mantren_laden()
    v = VORLAGE[nr]
    if v.get('montage'):
        m = v['montage']
        plaene = {name: lied_plan(v, name, mantren) for name in m['lieder']}
        return {'chunks': [plaene[name]['chunks'][i] for name, i, _ in m['folge']], 'montage': True}
    chunks = []
    for name, quelle, dauer, plus, minus, regie in v['teile']:
        text = f'[{name}]'
        if regie:
            text += '\n' + regie
        if quelle:
            text += '\n' + '\n'.join(zeilen(mantren, quelle))
            if name == 'Das Daseinswort':   # die eine Wiederholung des Zyklus
                text += '\n' + '\n'.join(zeilen(mantren, quelle))
        stile = list(dict.fromkeys(((v['stimme'] + (v.get('haltung') or DIENT)) if quelle else []) + plus + ECHT + [v['tonart'], v['tempo']]))
        nicht = list(dict.fromkeys(NIE + minus))
        if not quelle and '(' not in regie:
            nicht.append('vocals')
        chunks.append({'text': text, 'duration_ms': int(dauer * 1000), 'positive_styles': stile[:50],
                       'negative_styles': nicht[:50], 'context_adherence': 'high'})
    if v.get('ref'):   # (Vorlage-Nr, von s, bis s[, Stärke]): Klang und Stimme dieser Passage weitertragen
        nr_ref, von, bis = v['ref'][:3]
        sid = song_id(nr_ref, mantren)
        if sid:
            chunks[0]['conditioning_ref'] = {'song_id': sid, 'range': {'start_ms': int(von * 1000), 'end_ms': int(bis * 1000)}}
            chunks[0]['condition_strength'] = v['ref'][3] if len(v['ref']) > 3 else 'high'
        else:
            print(f'  Hinweis: Vorlage {nr_ref} ist nicht gespeichert (kein song_id), Referenz entfällt')
    for c in chunks:
        for z in c['text'].split('\n'):
            assert len(z) <= 200, z
        assert 3000 <= c['duration_ms'] <= 120000, c['text'][:30]
    assert len(chunks) <= 30
    return {'chunks': chunks}


def dauer_s(p):
    return sum(c['duration_ms'] for c in p['chunks']) / 1000


# ---------------------------------------------------------------- ElevenLabs
def anfrage(pfad, koerper=None, binaer=False, versuche=4, methode=None, roh=None, kopf=None, mit_kopf=False):
    key = os.environ['XI_KEY']
    for v in range(versuche):
        daten = roh if roh is not None else (json.dumps(koerper).encode() if koerper is not None else None)
        h = {'xi-api-key': key}
        h.update(kopf or ({'Content-Type': 'application/json'} if koerper is not None else {}))
        req = urllib.request.Request(API + pfad, data=daten, headers=h, method=methode)
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                aus = r.read()
                if mit_kopf:
                    return dict(r.headers), aus
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


def multipart(kopf, body):
    """multipart/mixed des detailed-Endpunkts: JSON-Teil und Audio-Teil."""
    ct = next((w for h, w in kopf.items() if h.lower() == 'content-type'), '')
    if 'boundary=' not in ct:
        return None, body
    grenze = ct.split('boundary=')[1].split(';')[0].strip('"').encode()
    meta, audio = None, None
    for teil in body.split(b'--' + grenze)[1:]:
        if teil.strip() in (b'', b'--'):
            continue
        h, _, inhalt = teil.partition(b'\r\n\r\n')
        inhalt = inhalt.rstrip(b'\r\n')
        if b'application/json' in h:
            meta = json.loads(inhalt)
        else:
            audio = inhalt
    return meta, audio


def song_id(nr, mantren):
    k = schluessel(plan(nr, mantren))
    pf = os.path.join(CACHE, f'mus_{k}.plan.json')
    if not os.path.exists(pf):
        return None
    return json.load(open(pf)).get('song_id')


def erzeugen(p, name=''):
    """Ein Kompositionsplan → rohe MP3 im Cache (gespeichert bei ElevenLabs, song_id im Plan-JSON)."""
    k = schluessel(p)
    os.makedirs(CACHE, exist_ok=True)
    roh = os.path.join(CACHE, f'mus_{k}.mp3')
    if os.path.exists(roh):
        print(f'  {name}: aus dem Cache')
        return roh
    print(f'  {name}: {len(p["chunks"])} Abschnitte, {dauer_s(p):.0f} s — erzeuge …', flush=True)
    t0 = time.time()
    kopf, body = anfrage(f'/v1/music/detailed?output_format={FORMAT}',
                         {'composition_plan': p, 'model_id': MODELL, 'store_for_inpainting': True}, mit_kopf=True)
    meta, daten = multipart(kopf, body)
    open(roh, 'wb').write(daten)
    sid = next((w for h, w in kopf.items() if 'song' in h.lower() and 'id' in h.lower()), None)
    json.dump({'plan': p, 'song_id': sid, 'meta': meta}, open(os.path.join(CACHE, f'mus_{k}.plan.json'), 'w'),
              ensure_ascii=False, indent=1)
    if not sid:
        print(f'  Hinweis: kein song_id in den Kopfzeilen: {sorted(kopf)}')
    print(f'  {len(daten) / 1e6:.1f} MB in {time.time() - t0:.0f} s', flush=True)
    return roh


def bauen(nr, mantren):
    v = VORLAGE[nr]
    os.makedirs(AUSGABE, exist_ok=True)
    print(f'Vorlage {nr} «{v["titel"]}»')
    if v.get('montage'):
        roh = montieren(v, mantren)
    else:
        roh = erzeugen(plan(nr, mantren), v['titel'])
    ziel = os.path.join(AUSGABE, f'vorlage-{nr:02d}-{v["slug"]}.mp3')
    mastern(roh, ziel, nr, v['titel'] + ' – ' + v['ansatz'].split(':')[0].split(',')[0])
    laenge = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ziel],
                                  capture_output=True, text=True).stdout.strip() or 0)
    print(f'  fertig: {ziel}  {laenge / 60:.1f} min')
    return ziel


# ---------------------------------------------------------------- Montage: Rollen getrennt erzeugen, dann zusammensetzen
# Lehre aus Vorlage 35: Eleven Music hält in einem Stück keine zwei Stimmen auseinander — der Mensch
# bekam die Stimme des Hüters, die Duo-Harmonie verschwand, Frage jagte Antwort. Darum werden die
# Rollen als eigene Stücke über demselben Grundton erzeugt (Abschnittsdauern sind bei music_v2_5
# exakt, also schneidbar) und erst hier mit echter Stille zusammengesetzt.
SR = 44100


def dekodieren(pfad):
    import numpy as np
    roh = subprocess.run(['ffmpeg', '-v', 'error', '-i', pfad, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(roh, dtype=np.float32).reshape(-1, 2).copy()


def lied_plan(v, name, mantren):
    lied = v['montage']['lieder'][name]
    chunks = []
    for teil in lied['teile']:
        tname, quelle, dauer, plus = teil[:4]
        text = f'[{tname}]'
        if quelle:
            text += '\n' + '\n'.join(zeilen(mantren, quelle))
        stile = list(dict.fromkeys(plus + ECHT + [v['tonart'], v['tempo']]))
        nicht = list(dict.fromkeys(NIE + lied.get('nicht', [])))
        if not quelle:
            nicht.append('vocals')
        chunks.append({'text': text, 'duration_ms': int(dauer * 1000), 'positive_styles': stile[:50],
                       'negative_styles': nicht[:50], 'context_adherence': 'high'})
    return {'chunks': chunks}


def montieren(v, mantren):
    import numpy as np
    m = v['montage']
    audio, grenzen = {}, {}
    for name in m['lieder']:
        p = lied_plan(v, name, mantren)
        x = dekodieren(erzeugen(p, name))
        x *= 10 ** ((-20 - 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)) / 20)   # je Lied −20 dBFS RMS
        audio[name] = x
        t, g = 0, []
        for c in p['chunks']:
            g.append((t, t + c['duration_ms'] / 1000))
            t += c['duration_ms'] / 1000
        grenzen[name] = g
    teile = []

    def stille(sek):
        return np.zeros((int(sek * SR), 2), dtype=np.float32)

    def blende(x, ein=0.04, aus=0.12):
        n1, n2 = int(ein * SR), int(aus * SR)
        x[:n1] *= (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, n1)))[:, None]
        x[-n2:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, n2)))[:, None]
        return x
    for name, i, pause in m['folge']:
        von, bis = grenzen[name][i]
        x = audio[name][int(von * SR):min(len(audio[name]), int(bis * SR))].copy()
        teile.append(blende(x))
        teile.append(stille(pause))
    mix = np.concatenate(teile + [stille(m.get('schluss', 3.0))])
    roh = os.path.join(CACHE, f'mont_{schluessel(m)}.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', roh],
                   input=mix.astype(np.float32).tobytes(), check=True)
    return roh


def mastern(roh, ziel, nr, titel):
    """Die Stücke kommen mit sehr verschiedener Lautheit aus dem Modell (−17 bis −31 LUFS). Master wie im
    Haus: −16 LUFS, −1,5 dBTP, zwei Durchgänge, linear (keine Verdichtung — die Stille bleibt Stille)."""
    mess = subprocess.run(['ffmpeg', '-v', 'info', '-i', roh, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=20:print_format=json',
                           '-f', 'null', '-'], capture_output=True, text=True).stderr
    j = json.loads(mess[mess.rfind('{'):mess.rfind('}') + 1])
    filt = (f'loudnorm=I=-16:TP=-1.5:LRA=20:measured_I={j["input_i"]}:measured_TP={j["input_tp"]}:'
            f'measured_LRA={j["input_lra"]}:measured_thresh={j["input_thresh"]}:offset={j["target_offset"]}:linear=true')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', roh, '-af', filt + ',aresample=44100', '-c:a', 'libmp3lame', '-b:a', '192k',
                    '-metadata', f'title={nr}. {titel}', '-metadata', 'album=Nach innen – Vorlagen',
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
    v = VORLAGE[nr]
    pfad = os.path.join(AUSGABE, f'vorlage-{nr:02d}-{v["slug"]}.mp3')
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
    print(f'Vorlage {nr}: Ähnlichkeit {sm.ratio():.3f}  ({len(ref)} Wörter im Text, {len(b)} erkannt)')
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        t = stt[min(j1, len(stt) - 1)][1] if stt else 0
        print(f'  {op:8} {int(t // 60):02d}:{t % 60:04.1f} Text: {" ".join(ref[i1:i2])[:55]!r:57} erkannt: {" ".join(x[2] for x in stt[j1:j2])[:55]!r}')
    return sm.ratio()


# ---------------------------------------------------------------- Befehle
def main():
    befehl = sys.argv[1] if len(sys.argv) > 1 else 'plan'
    nummern = [int(a) for a in sys.argv[2:]] or sorted(VORLAGE)
    mantren = mantren_laden()
    if befehl == 'plan':
        for nr in nummern:
            p = plan(nr, mantren)
            print(f'# Vorlage {nr} «{VORLAGE[nr]["titel"]}» — {VORLAGE[nr]["ansatz"]}\n#   — {len(p["chunks"])} Abschnitte, {dauer_s(p) / 60:.1f} min, '
                  f'{sum(len(c["text"]) for c in p["chunks"])} Zeichen')
            print(json.dumps(p, ensure_ascii=False, indent=1))
        print(f'# Vorlagen gesamt: {sum(dauer_s(plan(n, mantren)) for n in VORLAGE) / 60:.1f} min')
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
