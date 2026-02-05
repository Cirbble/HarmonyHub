# Contributor Mini-Project: JSON → Western Notation (Browser)

**Goal**  
Prototype a browser-based renderer that turns HarmonyHub’s generated JSON exercises into standard Western staff notation.

**Context**  
The CLI currently produces JSON ➜ MIDI ➜ MP3/piano-roll visualization. Western notation is missing. This mini-project helps newcomers learn the codebase while adding a highly requested capability.

**What to build**  
1) Parse the generated JSON (pitch, duration, timing).  
2) Map it to Western notation and render in the browser using VexFlow (or a justified alternative).  
3) Show at least a single-staff melody; multi-measure support is ideal.  
4) Keep the solution ready for integration with the existing CLI or a small web demo.

**Suggested steps**
- Run `python cli.py generate --output-format json` to inspect the exercise structure.
- Sketch the JSON → notation mapping (note names, durations, measures, key/time signatures).
- Implement a minimal web page or component that renders a supplied JSON file/string.
- Document design/technical choices and integration points.

**Deliverable for your PR**
- Working prototype (HTML/JS or TS) committed to the repo (a small demo page is fine).
- Short write-up (max ~1 page) in your PR description covering:
  - Approach and mapping decisions
  - Libraries/tools used and how it could plug into the current pipeline
  - Challenges or musical edge cases
  - Thoughts on limitations of Western notation and future extensions

**Acceptance hints**
- Renders at least one generated exercise without manual edits.
- Clear, readable code; small helper comments where non-obvious.
- No build/tooling sprawl—keep dependencies lightweight.

**Nice-to-have extensions (optional)**
- Support for rests, ties, and basic articulation.
- Simple key/time signature display.
- Toggle between notation and the existing piano roll for the same exercise.

Open a PR referencing this mini-project and include the write-up in the PR description. A maintainer will review and guide next steps.
