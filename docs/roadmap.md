# HarmonyHub Roadmap

## Purpose
- Keep the README focused on what is implemented today.
- Give contributors clear next targets and expected scope.
- Track progress using issues, milestones, and status labels.

## How To Use This Roadmap
- Each roadmap item should map to one GitHub issue.
- Add issue links as they are created.
- Use status and priority to decide what to work on next.
- Use detailed specs in `docs/` as implementation references when available.

## Status Definitions
- `idea`: concept captured, not yet scoped.
- `scoping`: requirements and implementation plan being defined.
- `ready for contributors`: scoped and suitable for external contributions.
- `in progress`: active implementation.
- `blocked`: waiting on dependency, funding, or maintainer decision.
- `done`: merged and available in the repository.

## Priority Definitions
- `high`: unlocks other work or fills a critical gap.
- `medium`: important extension, but not blocking core progress.
- `low`: useful improvement with lower immediate impact.

## Foundation Track

### F1. Generation schema specification
- Status: `scoping`
- Priority: `high`
- Goal: Document and stabilize the JSON schema for generated exercises (`note`, `duration`, `cumulative_duration`, and metadata expectations).
- Dependencies: none
- Issue: pending

### F2. Golden test fixtures for generation and conversion
- Status: `idea`
- Priority: `high`
- Goal: Add versioned sample exercises and expected conversion outputs for regression testing.
- Dependencies: F1
- Issue: pending

### F3. CLI and API documentation hardening
- Status: `idea`
- Priority: `medium`
- Goal: Improve command docs, examples, and environment setup for reproducible use.
- Dependencies: F1
- Issue: pending

## Track A: Notation and Visual Representation

### A1. Western notation renderer in browser
- Status: `ready for contributors`
- Priority: `high`
- Goal: Convert generated JSON exercises to Western staff notation in browser.
- Dependencies: F1
- Issue: pending
- Related doc: `docs/notation-challenge.md`

### A2. Improved interactive piano roll
- Status: `idea`
- Priority: `medium`
- Goal: Add clearer timing interaction, zoom, and note-level inspection.
- Dependencies: F1
- Issue: pending
- Related doc: `docs/interactive-piano-roll.md`

### A3. Alternative notation outputs
- Status: `idea`
- Priority: `medium`
- Goal: Explore color-coded notation and other alternative visual representations.
- Dependencies: A1
- Issue: pending

## Track B: Accessibility and Multimodal I/O

### B1. Multimodal input experiments
- Status: `idea`
- Priority: `medium`
- Goal: Prototype non-text input paths (for example speech instructions or musical input).
- Dependencies: F1
- Issue: pending

### B2. Talking-score style output
- Status: `idea`
- Priority: `medium`
- Goal: Generate audio-guided verbal descriptions of exercises.
- Dependencies: F1
- Issue: pending

### B3. Braille notation pathway (simple melodies first)
- Status: `idea`
- Priority: `medium`
- Goal: Define a practical export path for simple melody exercises.
- Dependencies: F1
- Issue: pending
- Related doc: `docs/braille-notation-output.md`

## Track C: Model Backends and Generation Methods

### C1. Pluggable backend interface
- Status: `idea`
- Priority: `high`
- Goal: Decouple generation logic from a single provider to allow multiple model backends.
- Dependencies: F1
- Issue: pending

### C2. Alternative model backend integration
- Status: `idea`
- Priority: `medium`
- Goal: Add at least one additional backend and compare output behavior.
- Dependencies: C1
- Issue: pending

### C3. Hybrid generation experiments (LLM + symbolic/rule constraints)
- Status: `idea`
- Priority: `medium`
- Goal: Improve controllability and consistency of generated exercises.
- Dependencies: C1
- Issue: pending

## Research and Exploratory Track

### R1. Harmonic accompaniment generation
- Status: `idea`
- Priority: `low`
- Goal: Extend from monophonic exercises to melody plus accompaniment.
- Dependencies: F1, C1
- Issue: pending

### R2. Learner-machine dialogue exercises
- Status: `idea`
- Priority: `low`
- Goal: Explore call-and-response and interactive exercise structures.
- Dependencies: F1, C1
- Issue: pending

## Contribution Notes
- If you pick an item marked `ready for contributors`, open or claim the linked issue first.
- If you pick an `idea` item, start by creating a short scoping issue before coding.
- Keep PRs small and focused on one roadmap item when possible.
