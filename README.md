# HarmonyHub: Adaptive Music Exercise Generator

Open-source toolkit for generating structured music exercises from pedagogical and musical inputs. HarmonyHub is designed as an adaptable digital music book that can support teaching, practice, and research workflows.

> Built in the open with INCF / Google Summer of Code 2025 roots—now welcoming contributors, classrooms, and research partners.

## Quick Links
- [Get Started](#get-started)
- [CLI Usage](#cli-usage)
- [Repo Structure](#repo-structure)
- [Contribute](#contribute)
- [Academic & Classroom Use](#academic--classroom-use)
- [Community Principles](#community-principles)
- [Demo & Links](#demo--links)
- [License](#license)

## Why HarmonyHub
Instrument-learning materials are often static and difficult to adapt to different contexts. HarmonyHub approaches this as a generative system: users provide musical parameters (or text instructions), and the system produces machine-readable and playable exercises that can be reused in teaching and research.

## Features at a Glance
- Parameterized generation via CLI: instrument, difficulty level, tonality/key, time signature, exercise length (measures), tempo, and optional text prompt.
- Current outputs: structured JSON (`note`, `duration`, `cumulative_duration`), MIDI, MP3, and piano-roll PNG visualization.
- Backend model path: Mistral API integration in the generation pipeline.
- Utilities: metronome generation and JSON-to-MIDI/MP3 conversion.
- Architecture: Typer CLI with modular Python packages for generation and processing.

### Project Direction (not yet implemented)
The broader research direction is to expand both inputs and outputs: richer multimodal inputs (for example speech or musical inputs), additional model backends, and alternative output representations such as Braille notation, talking-score style outputs, color-coded notation, and richer interactive visualizations.

## Get Started
Prereqs: Python 3.10+ recommended; `fluidsynth` optional but improves audio quality.

```bash
pip install -r requirements.txt
# Optional: ensure fluidsynth is available for rich soundfonts
```

### Configure Mistral API Key
The project uses the Mistral API to generate music exercises. You need to set up your API key:

1. Sign up for a Mistral API account at [https://console.mistral.ai/](https://console.mistral.ai/)
2. Create an API key from your dashboard
3. Edit the `.env` file in the project root and replace `your_mistral_api_key_here` with your actual API key

```bash
# .env file
MISTRAL_API_KEY=your_actual_api_key_here
```

Alternatively, you can set the environment variable directly:
```bash
export MISTRAL_API_KEY=your_actual_api_key_here  # Linux/Mac
set MISTRAL_API_KEY=your_actual_api_key_here     # Windows CMD
$env:MISTRAL_API_KEY="your_actual_api_key_here"  # Windows PowerShell
```

### Smoke test
```bash
python cli.py generate --instrument Trumpet --level Intermediate --key "C Major" --time-signature "4/4" --measures 4 --output-format all
```
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
├── LICENSE                   # AGPL-3.0 license text
├── lib/
│   └── music_generation/
│       ├── constants.py      # Config + URLs for models/soundfonts
│       ├── generator.py      # Exercise generation pipeline
│       └── theory.py         # Music theory helpers
├── processing/
│   ├── midi/converter.py     # JSON → MIDI
│   ├── audio/converter.py    # MIDI → MP3 (soundfonts + fallback)
│   └── visualization/visualizer.py  # Piano roll render
├── docs/                     # Contributor issue/specification docs
│   ├── notation-challenge.md
│   ├── interactive-piano-roll.md
│   ├── braille-notation-output.md
│   ├── voice-prompt-input.md
│   └── roadmap.md
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
- **Case studies:** Phase 2 focuses on participatory design in community music settings; we’re eager to partner on parallel studies—open an issue to discuss protocols and ethics.

## Community Principles
- Accessibility and inclusion first; avoid ableist defaults.
- Transparent pedagogy: generated outputs must be explainable and editable by teachers.
- Collaboration over competition: academic + open-source contributions are equally valued.
- Ethical AI use: no hidden data collection; prioritize user consent and agency.

## Demo & Links
- Hugging Face space (prototype): https://huggingface.co/spaces/SHIKARICHACHA/adaptive-music-exercise-generator
- INCF GSoC 2025 project page (coming from proposal)—watch issues for updates.

## License
This repository is licensed under the GNU Affero General Public License v3.0 (`AGPL-3.0`).
See `LICENSE` for the full license text.

## Contact
Open an issue for feature requests or email the maintainer team via GitHub profiles. If you’re proposing a study or classroom deployment, include timeline, site, and accessibility goals so we can align support.
