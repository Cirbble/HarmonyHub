#!/usr/bin/env python

"""
MusicXML Converter
==================
Converts HarmonyHub JSON exercise files to MusicXML format.

Duration encoding: 1 unit = 1 eighth note (quarterLength 0.5).
  1 → eighth, 2 → quarter, 3 → dotted quarter, 4 → half,
  6 → dotted half, 8 → whole.

Notes that cross a barline are automatically split and tied.
Rests (note name == "rest") are never tied across barlines.
"""

import json
import re
from pathlib import Path
from typing import Optional

from music21 import clef as clef_module
from music21 import key, meter, note, stream
from music21 import tie as tie_module


# ---------------------------------------------------------------------------
# Key signature mapping  (HarmonyHub string → music21 tonic string)
# music21 convention: uppercase = major, lowercase = minor, '-' = flat
# ---------------------------------------------------------------------------
_KEY_MAP = {
    # Major keys
    "C Major": "C",   "G Major": "G",   "D Major": "D",   "A Major": "A",
    "E Major": "E",   "B Major": "B",   "F# Major": "F#", "C# Major": "C#",
    "F Major": "F",   "Bb Major": "B-", "Eb Major": "E-", "Ab Major": "A-",
    "Db Major": "D-", "Gb Major": "G-", "Cb Major": "C-",
    # Minor keys
    "A Minor": "a",   "E Minor": "e",   "B Minor": "b",   "F# Minor": "f#",
    "C# Minor": "c#", "G# Minor": "g#", "D# Minor": "d#",
    "D Minor": "d",   "G Minor": "g",   "C Minor": "c",   "F Minor": "f",
    "Bb Minor": "b-", "Eb Minor": "e-", "Ab Minor": "a-",
}

_CLEF_MAP = {
    "treble": clef_module.TrebleClef,
    "bass":   clef_module.BassClef,
    "alto":   clef_module.AltoClef,
    "tenor":  clef_module.TenorClef,
}


def _normalize_note_name(name: str) -> str:
    """Convert HarmonyHub note name to music21 format (e.g. 'Bb4' → 'B-4')."""
    return re.sub(r'([A-G])b', r'\1-', name)


def _parse_key(key_str: str) -> key.Key:
    """Parse a key string like 'C Major' or 'A Minor' into a music21 Key."""
    key_str = key_str.strip()
    if key_str in _KEY_MAP:
        return key.Key(_KEY_MAP[key_str])

    # Generic fallback: split "Tonic Mode" and infer
    parts = key_str.split()
    if len(parts) == 2:
        tonic, mode = parts
        tonic = tonic.replace('b', '-')
        if mode.lower() == 'minor':
            tonic = tonic.lower()
        return key.Key(tonic)

    return key.Key('C')


def _parse_clef(clef_str: str):
    """Return a music21 clef object for the given clef name string."""
    cls = _CLEF_MAP.get(clef_str.lower(), clef_module.TrebleClef)
    return cls()


def _make_element(note_data: dict) -> note.GeneralNote:
    """Create a fresh music21 Note or Rest from a JSON note object."""
    name = note_data['note']
    if name.lower() == 'rest':
        return note.Rest()
    return note.Note(_normalize_note_name(name))


def _set_duration(elem: note.GeneralNote, units: int) -> None:
    """Set quarterLength from eighth-note units (1 unit = 0.5 quarterLength)."""
    elem.duration.quarterLength = units * 0.5


def _apply_tie(elem: note.GeneralNote, start: bool, stop: bool) -> None:
    """Apply tie markings to a Note (ignored for Rests)."""
    if not isinstance(elem, note.Note):
        return
    if start and stop:
        elem.tie = tie_module.Tie('continue')
    elif start:
        elem.tie = tie_module.Tie('start')
    elif stop:
        elem.tie = tie_module.Tie('stop')


def convert_to_musicxml(
    file_path: str,
    key_sig: str,
    time_sig: str,
    clef: str = 'treble',
    output_path: Optional[str] = None,
) -> str:
    """
    Convert a HarmonyHub JSON exercise file to a MusicXML file.

    Args:
        file_path:   Path to the input JSON file.
        key_sig:     Key signature string, e.g. "C Major" or "A Minor".
        time_sig:    Time signature string, e.g. "4/4" or "3/4".
        clef:        Clef name: 'treble' (default), 'bass', 'alto', or 'tenor'.
        output_path: Destination path for the .musicxml file. Defaults to the
                     same directory as the input with a .musicxml extension.

    Returns:
        Absolute path to the generated MusicXML file.
    """
    file_path = Path(file_path)

    with open(file_path, 'r') as f:
        notes_data = json.load(f)

    # Units per measure in eighth-note units, e.g. 4/4 → 8, 3/4 → 6
    numerator, denominator = map(int, time_sig.split('/'))
    units_per_measure = numerator * (8 // denominator)

    # Build score/part structure
    score = stream.Score()
    part = stream.Part()
    score.append(part)

    measure_number = 1
    current_measure = stream.Measure(number=measure_number)
    current_measure.append(_parse_clef(clef))
    current_measure.append(_parse_key(key_sig))
    current_measure.append(meter.TimeSignature(time_sig))
    position = 0  # eighth-note units consumed in current_measure

    def flush():
        """Append the current measure to the part and open a fresh one."""
        nonlocal current_measure, measure_number, position
        part.append(current_measure)
        measure_number += 1
        current_measure = stream.Measure(number=measure_number)
        position = 0

    for note_data in notes_data:
        remaining = int(note_data['duration'])
        is_rest = note_data['note'].lower() == 'rest'
        is_continuation = False  # True once we've tied across at least one barline

        while remaining > 0:
            space = units_per_measure - position

            if remaining <= space:
                # Fits entirely in the current measure
                elem = _make_element(note_data)
                _set_duration(elem, remaining)
                _apply_tie(elem, start=False, stop=is_continuation and not is_rest)
                current_measure.append(elem)
                position += remaining
                remaining = 0

                if position == units_per_measure:
                    flush()
            else:
                # Crosses the barline — fill the rest of this measure
                elem = _make_element(note_data)
                _set_duration(elem, space)
                _apply_tie(
                    elem,
                    start=not is_rest,
                    stop=is_continuation and not is_rest,
                )
                current_measure.append(elem)
                remaining -= space
                position += space
                is_continuation = True
                flush()

    # Append a non-empty trailing measure (partial last measure)
    if position > 0:
        part.append(current_measure)

    if output_path is None:
        output_path = file_path.with_suffix('.musicxml')
    else:
        output_path = Path(output_path)

    score.write('musicxml', fp=str(output_path))
    return str(output_path.resolve())


# ---------------------------------------------------------------------------
# Convenience CLI when run directly
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    fp = input("JSON file path: ").strip()
    ks = input("Key signature (e.g. 'C Major', 'A Minor'): ").strip()
    ts = input("Time signature (e.g. '4/4', '3/4'): ").strip()
    cl = input("Clef [treble/bass/alto/tenor] (default: treble): ").strip() or 'treble'

    out = convert_to_musicxml(fp, ks, ts, cl)
    print(f"Written to: {out}")
