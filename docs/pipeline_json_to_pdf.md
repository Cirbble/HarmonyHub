# JSON → MusicXML → PDF Pipeline

## Overview

Three-stage pipeline that converts LLM-generated exercise data into a rendered PDF of western staff notation.

Stage 0: `generate_exercise()` → `List[dict]`
Stage 1: `convert_to_musicxml()` → `.musicxml` — `processing/musicxml/converter.py`
Stage 2: `convert_to_pdf()` → `.pdf` — `processing/musicxml/pdf_renderer.py`

## Stage 0 — Note Generation (`lib/music_generation/generator.py`)

- Calls the Mistral API (`mistral-medium`) to produce a JSON array of note objects.
- Each note has: `note` (scientific pitch, e.g. `"C4"`, `"Bb3"`, or `"rest"`), `duration` (eighth-note units), `cumulative_duration` (running total).
- Duration sum must equal `measures × units_per_measure` (4/4 → 8 units/measure; 3/4 → 6).
- LLM temperature: 0.7 for Advanced, 0.5 otherwise.
- Post-processing: `clean_note_string()` strips LLM ornamentation artefacts; `scale_json_durations()` rescales all durations so their sum is exactly `total_units`.
- Three-level fallback chain: instrument-specific fixed pattern → ascending scale in key → propagate exception.

## Stage 1 — JSON → MusicXML (`processing/musicxml/converter.py`)

- Builds a `music21` Score with key, time signature, clef, and instrument metadata from the JSON file.
- Normalises flat notation: `b` → `-` (music21 convention, e.g. `Bb4` → `B-4`).
- Converts durations: `quarterLength = units × 0.5` (eighth-note units to music21 quarterLength).
- Notes that cross barlines are split into tied pairs; tie types assigned are `start`, `continue`, and `stop`. Ties are never applied to rests.

## Stage 2 — MusicXML → PDF (`processing/musicxml/pdf_renderer.py`)

Uses three libraries in sequence: **Verovio** (MusicXML → SVG per page), **lxml** (SVG repair), **svglib + ReportLab** (SVG → PDF).

Verovio renders at A4 dimensions. Three SVG fixes are applied before conversion to work around svglib incompatibilities:

- **Flatten nested `<svg>`** — promotes the inner `viewBox` to the outer element so coordinates scale correctly.
- **Inline `<use>` elements** — replaces SMuFL glyph references with deep copies (iterated up to 5 times for nested references).
- **Fix title rendering** — strips tooltip `<title>` elements, removes `font-size="0px"`, promotes `text-anchor` from `<tspan>` to parent `<text>`.

Each page is scaled to fit A4 and drawn to the ReportLab canvas. Temp SVG files are cleaned up in a `finally` block.

## File Locations

All output files share the base name `exercise_{instrument}_{level}_{measures}m`.

| File | Path |
|---|---|
| JSON notes | `output/exercise_Trumpet_Intermediate_4m.json` |
| MusicXML | `output/exercise_Trumpet_Intermediate_4m.musicxml` |
| PDF | `output/exercise_Trumpet_Intermediate_4m.pdf` |

## Implementation Notes

- Verovio requires its font resources to be set explicitly via `tk.setResourcePath()` when running inside Flask; the path is derived from `verovio.__file__` at runtime to avoid working-directory dependency.
- The barline-splitting algorithm must handle notes longer than one measure (ties spanning three or more pieces).
- music21's `score.write('musicxml')` produces standard MusicXML compatible with both Verovio (PDF) and OSMD (browser rendering).
