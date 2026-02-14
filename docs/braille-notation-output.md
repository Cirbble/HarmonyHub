# Braille Music Notation Output (MVP: monophonic)

## Problem
HarmonyHub currently exports JSON, MIDI, MP3, and piano-roll PNG. It does not provide Braille music notation output, which limits access for blind and low-vision musicians and educators.

## Goal
Add Braille music notation as a first-class output format for generated exercises.

## Source Strategy
- Primary source for MVP: generated exercise JSON (`note`, `duration`, `cumulative_duration`).
- Future upgrade path: use MusicXML as primary source when notation export is available.
- Do not use MIDI as the primary transcription source for this issue (MIDI loses notation semantics needed for reliable Braille mapping).

## Scope (MVP)
- Support monophonic exercises only.
- Convert generated exercise data to Braille music text output.
- Add CLI output option for Braille export.
- Export as a plain text file format suitable for downstream Braille workflows.

## Library Guidance
- Recommended baseline: `music21` (already in project dependencies).
- Alternative libraries are allowed if the contributor justifies:
  - transcription quality and coverage,
  - maintenance activity and reliability,
  - license compatibility for project use.

## Acceptance Criteria
- Works on at least 3 generated HarmonyHub exercises.
- Deterministic conversion (same input -> same output).
- Unit tests cover core mapping logic and edge cases (accidentals, octave changes, and duration mapping).
- Documentation states supported symbols/rules and known limitations.

## Non-goals (MVP)
- Polyphonic or multi-voice transcription.
- Real-time Braille rendering during playback.
- Full advanced engraving semantics not represented in current input.

## Implementation Notes
- Keep conversion logic modular so data source can later move from JSON to MusicXML.
- Keep mapping rules explicit and testable (avoid hidden heuristics).
- Include one minimal sample input/output pair in tests or docs.
