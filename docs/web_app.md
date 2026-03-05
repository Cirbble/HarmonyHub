# HarmonyHub Web App

## Overview

Single-page Flask app for generating and playing back musical exercises. Server: `app.py`. Frontend: `templates/index.html`.

The browser posts parameters to `/generate`, Flask runs the full pipeline and returns file URLs, and the browser fetches output files directly from `/output/`. In-browser playback uses the `.mid` file and CDN soundfonts, not the server-generated audio.

## Server — `app.py`

### Routes

- `GET /` — serves `templates/index.html`.
- `POST /generate` — accepts a JSON body, runs the pipeline, returns URLs and note data.
- `GET /output/<filename>` — serves any file from `output/` (`.musicxml`, `.mid`, `.wav`, `.mp3`, `.pdf`, `.json`).

### `/generate` pipeline (executed in order)

1. `generate_exercise()` — Mistral API → `List[dict]` with `note`, `duration`, `cumulative_duration`.
2. Write raw note list to `output/<base>.json`.
3. `convert_to_musicxml()` — music21 Score with barline splitting → `output/<base>.musicxml`.
4. `convert_to_pdf()` — Verovio + svglib → `output/<base>.pdf`.
5. `json_to_midi()` — mido MIDI file → `output/<base>.mid`.
6. `midi_to_mp3()` — FluidSynth or sine-wave fallback → `output/<base>.wav` or `.mp3`.

A failure at any step returns a 500 with an error message. `mp3_url` is `null` if audio fails entirely.

### Base filename

`exercise_{instrument}_{level}_{measures}m` — spaces replaced with `_`. Same parameters overwrite previous output.

## Frontend — `templates/index.html`

### Page structure

- `<form id="gen-form">` — instrument, level, key, time signature, measures, tempo, custom prompt.
- `<div id="status">` — "Generating…" / "Rendering…" text.
- `<div id="error-box">` — red error banner (hidden until error).
- `<div id="transport">` — Play / Pause / Stop / Download MIDI / Download MusicXML / Download PDF (hidden until first successful render).
- `<div id="osmd-container">` — OSMD renders the score here.

The form uses a 2-column CSS Grid; the Generate button spans both columns. Transport buttons are outside the form and unaffected by the `form button` CSS selector.

## Score Rendering — OSMD

[OpenSheetMusicDisplay](https://opensheetmusicdisplay.org/) loaded from CDN. Renders MusicXML to SVG in `#osmd-container` with `autoResize: true`. Provides a cursor for playback sync (hidden when not playing).

After render, `buildCursorTimes()` walks the cursor and records `realValue` (whole-note fractions) at each position. Conversion to seconds: `t = realValue × 4 × (60 / tempo)`.

## Playback

### Primary path (CDN soundfonts)

- `Tone.Sampler` loads 7 sample pitches per instrument from the MusyngKite CDN.
- `Midi.fromUrl()` fetches and parses the `.mid` file; all notes are scheduled on `Tone.Transport`.
- Cursor advances are scheduled in parallel via `Tone.Draw` (deferred to animation frame to avoid blocking the audio thread).
- Auto-stop is scheduled at the end of the piece.

### Fallback (CDN unreachable)

`Tone.Synth` with a per-instrument oscillator waveform and ADSR envelope, scheduled from the JSON note list rather than the parsed MIDI.

### Instrument map

| HarmonyHub | GM soundfont | Oscillator fallback |
|---|---|---|
| Trumpet | `trumpet` | sawtooth |
| Piano | `acoustic_grand_piano` | triangle |
| Violin | `violin` | sawtooth |
| Clarinet | `clarinet` | square |
| Flute | `flute` | sine |

### Transport controls

| Button | Action |
|---|---|
| ▶ Play | Resume if paused; restart from beginning otherwise |
| ⏸ Pause | `Tone.Transport.pause()` — holds position |
| ⏹ Stop | Stop, cancel all events, dispose synth, reset cursor |
| Download MIDI | `<a href download>` link to `.mid` |
| Download MusicXML | `<a href download>` link to `.musicxml` |
| Download PDF | `<a href download>` link to `.pdf` |

## Server-side Audio

Used for download artifacts only; in-browser playback uses MIDI + CDN soundfonts.

- **FluidSynth path**: downloads `.sf2` soundfont to `soundfonts/` (cached after first use), renders MIDI → WAV, converts to MP3 via pydub/ffmpeg.
- **Fallback path**: synthesises per-note sine waves with numpy, writes WAV via scipy, attempts MP3 conversion with pydub. Keeps WAV if ffmpeg is absent.

## Implementation Notes

- `activeSynth.dispose()` must be called on stop to release Web Audio nodes; without it, repeated plays accumulate dead nodes in the AudioContext.
- Note times from `@tonejs/midi` are in seconds and passed directly to `Tone.Transport.schedule()`; Transport BPM does not affect them.
- The Play button checks `Tone.Transport.state === 'paused'` to distinguish resume from restart.
