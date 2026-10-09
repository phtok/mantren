#!/usr/bin/env python3
"""Harte Sprünge im Pegel finden (Schnitte, die Klang treffen): 5-ms-Rahmen, ein Sprung von mehr als
24 dB zwischen zwei Rahmen, wobei der lautere über −40 dBFS liegt. Natürliche Einsätze (Plosive) gibt
es auch; aussagekräftig ist der Vergleich zweier Fassungen.

    python3 -I knacks.py a.mp3 [b.mp3 …]
"""
import subprocess, sys
import numpy as np

for pfad in sys.argv[1:]:
    roh = subprocess.run(['ffmpeg', '-v', 'error', '-i', pfad, '-f', 'f32le', '-ac', '1', '-ar', '44100', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(roh, np.float32)
    fr = 220
    n = len(x) // fr
    e = 10 * np.log10((x[:n * fr].reshape(n, fr) ** 2).mean(1) + 1e-12)
    d = np.diff(e)
    lauter = np.maximum(e[1:], e[:-1])
    hart = np.where((np.abs(d) > 24) & (lauter > -40))[0]
    abbrueche = np.where((d < -24) & (e[:-1] > -40))[0]
    print(f'{pfad}: {len(hart)} harte Sprünge, davon {len(abbrueche)} Abbrüche (Klang → Stille)')
    for i in abbrueche[:12]:
        t = i * fr / 44100
        print(f'   Abbruch bei {int(t // 60):02d}:{t % 60:05.2f}  ({e[i]:.0f} → {e[i + 1]:.0f} dB)')
