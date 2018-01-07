import subprocess as spr
import sys
"""
Generate sound wav file and play it.
tested player on OSX, Ubuntu16.04
"""


RATE = 44100


def get_note(note, length=None):
    import struct
    from math import sin, pi

    if length is None:
        length = round(RATE/4)

    wv_data = b""
    for i in range(0, length):
        max_vol = 2 ** 15 - 1.0
        raw = round(max_vol * sin(i * 2 * pi * note / RATE))
        wv_data += struct.pack('h', raw)
        wv_data += struct.pack('h', raw)
    return wv_data


def generate_sound_file(freqs, filename='noise.wav'):
    import wave

    noise_output = wave.open(filename, 'w')
    noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

    wv_data = b"".join([get_note(n) for n in freqs])

    noise_output.writeframes(wv_data)

    noise_output.close()


def play(filepath):
    try:
        if sys.platform == 'darwin':
            spr.call(["afplay", filepath])
        elif 'win' in sys.platform:
            spr.call(["start", "wmplayer", filepath])
        else:
            # Linux or other non-tested platform such as BSD*
            try:
                spr.call(["aplay", filepath])
            except Exception:
                spr.call(["xdg-open", filepath])

    except Exception as e:
        print("Play sound error", e)


def calculate_note_freq(note):
    '''Calculate note frequency base on its name
    # TODO
    '''
    note = note.upper()
    pass


def cli():
    # argparse notes a4 c7 a3
    notes = ['A4', 'A#4', 'B4', 'C5', 'C#5', 'D', 'D#5',
             'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5']
    freqs = []
    for i, note in enumerate(notes):
        freq = (2**(1/12))**i * 440
        freqs.append(freq)
        print("Pitch %s  %.2f Hz" % (note, freq))
    filename = 'noise.wav'
    generate_sound_file(freqs, filename)
    play(filename)


if __name__ == "__main__":
    cli()
