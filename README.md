# HarmonyHub: Adaptive, Accessible Music Practice

Open-source toolkit for generating **inclusive, pedagogically sound music exercises** from structured prompts. HarmonyHub pairs rule-based + AI-assisted generation with accessibility-first outputs (MIDI/MP3/JSON/notation variants) to support teachers, students, and researchers.

> Built in the open with INCF / Google Summer of Code 2025 roots—now welcoming contributors, classrooms, and research partners.

## Quick Links
- [Get Started](#get-started)
- [CLI Usage](#cli-usage)
- [Repo Structure](#repo-structure)
- [Contribute](#contribute)
- [Academic & Classroom Use](#academic--classroom-use)
- [Roadmap](#roadmap)
- [Community Principles](#community-principles)

## Why HarmonyHub
Traditional method books assume a “standard” learner. HarmonyHub flips that by generating practice materials that adapt to the learner: key, level, time signature, focus, and accessibility needs. Outputs can be visual, auditory, or multi-sensory—ready for classrooms, community music programs, or individual study.

## Features at a Glance
- 🎛️ Promptable exercise generation via CLI (instrument, level, key, time signature, measures).
- 🎼 Outputs today: JSON note data, MIDI, MP3 audio (soundfonts or fallback), and piano-roll visualization when requested.
- 🎚️ Utilities: metronome generator; JSON→MIDI/MP3 converter.
- 🧰 Modular Python library + Typer CLI for quick experiments and scripting.

### Direction (theory + roadmap, not yet shipped)
Grounded in disability studies and inclusive music pedagogy, HarmonyHub aims to add adaptable notation, accessibility-aware representations, and richer pedagogical controls. Those pieces are under active design and tracked in issues/roadmap.

## Get Started
Prereqs: Python 3.10+ recommended; `fluidsynth` optional but improves audio quality.

```bash
pip install -r requirements.txt
# Optional: ensure fluidsynth is available for rich soundfonts
```

### Smoke test
```bash
python cli.py generate --instrument Trumpet --level Intermediate --key "C Major" --time-signature "4/4" --measures 4 --output-format all
```
Outputs are saved under `./output` (JSON, MIDI, MP3, visualization PNG when `--output-format all`).

## CLI Usage
- Generate exercise
```bash
python cli.py generate --instrument Piano --level Beginner --key "G Major" --time-signature "3/4" --measures 8 --tempo 72 --output-format all
```
- Metronome
```bash
python cli.py metronome --tempo 60 --time-signature "4/4" --measures 4
```
- Convert saved JSON to MIDI/MP3
```bash
python cli.py convert --input-file exercise.json --output-format mp3 --instrument Flute
```
- Discover options
```bash
python cli.py info
```

## Repo Structure
```
├── lib/
│   └── music_generation/
│       ├── constants.py      # Config + URLs for models/soundfonts
│       ├── generator.py      # Exercise generation pipeline
│       └── theory.py         # Music theory helpers
├── processing/
│   ├── midi/converter.py     # JSON → MIDI
│   ├── audio/converter.py    # MIDI → MP3 (soundfonts + fallback)
│   └── visualization/visualizer.py  # Piano roll render
├── cli.py                    # Typer-based CLI
├── tests/                    # Unit tests
├── requirements.txt
└── Dockerfile
```

## Contribute
We welcome open-source contributors, students, and mentors.
- **Issues & Ideas:** Start a GitHub issue for bugs, features, or accessibility requests.
- **Pull Requests:** Add tests (`python -m unittest discover tests`) and keep functions documented.
- **Google Summer of Code (INCF):** Use this repo as the working codebase; propose features such as adapted notation exports, new instruments, or UI/UX prototypes.
- **Good first tasks:**
  - Improve MusicXML/notation export coverage.
  - Expand soundfont set and caching.
  - Add accessibility fixtures (color/size schemas) to visualization.
  - Write sample prompts + tutorials for common classroom needs.
- **Open challenge:** Build a browser renderer that converts generated JSON exercises into Western staff notation. See `docs/notation-challenge.md`.

## Academic & Classroom Use
- **Research:** The framework can act as a controllable stimulus generator for studies in music learning, HCI, or accessibility. Cite the project and include prompt + parameter logs for reproducibility.
- **Teaching:** Use the CLI to generate leveled drills, rhythm patterns, or call/response material. Export MIDI/MP3 for LMS uploads or play-alongs.
- **Case studies:** Phase 2 focuses on participatory design with L’Arche London; we’re eager to partner on parallel studies—open an issue to discuss protocols and ethics.

## Roadmap (2025–2026)
- Phase 1: Robust generative backend, multiple representations, automated tests and docs.
- Phase 2: Co-designed interfaces in community settings; accessibility feature hardening (Braille, haptics, enlarged/colored notation presets).
- Stretch: Web service wrapper + auth, educator-facing prompt templates, dataset of vetted exercises.

## Community Principles
- Accessibility and inclusion first; avoid ableist defaults.
- Transparent pedagogy: generated outputs must be explainable and editable by teachers.
- Collaboration over competition: academic + open-source contributions are equally valued.
- Ethical AI use: no hidden data collection; prioritize user consent and agency.

## Demo & Links
- Hugging Face space (prototype): https://huggingface.co/spaces/SHIKARICHACHA/adaptive-music-exercise-generator
- INCF GSoC 2025 project page (coming from proposal)—watch issues for updates.

## Contact
Open an issue for feature requests or email the maintainer team via GitHub profiles. If you’re proposing a study or classroom deployment, include timeline, site, and accessibility goals so we can align support.
