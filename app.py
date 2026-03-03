#!/usr/bin/env python

"""
HarmonyHub Flask Web App
========================
Lightweight web interface for generating and viewing sheet music exercises.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_from_directory

load_dotenv()

from lib.music_generation.generator import generate_exercise
from processing.midi.converter import json_to_midi
from processing.musicxml.converter import convert_to_musicxml

app = Flask(__name__)

OUTPUT_DIR = Path("./output")
OUTPUT_DIR.mkdir(exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)

    instrument = data.get("instrument", "Trumpet")
    level = data.get("level", "Intermediate")
    key = data.get("key", "C Major")
    time_signature = data.get("time_signature", "4/4")
    measures = int(data.get("measures", 4))
    tempo = int(data.get("tempo", 60))
    custom_prompt = data.get("custom_prompt", "")

    try:
        notes = generate_exercise(instrument, level, key, time_signature, measures, custom_prompt)
    except Exception as e:
        return jsonify({"error": f"Generation failed: {e}"}), 500

    safe_instrument = instrument.replace(" ", "_")
    safe_level = level.replace(" ", "_")
    base_filename = f"exercise_{safe_instrument}_{safe_level}_{measures}m"

    json_path = OUTPUT_DIR / f"{base_filename}.json"
    musicxml_path = OUTPUT_DIR / f"{base_filename}.musicxml"
    midi_path = OUTPUT_DIR / f"{base_filename}.mid"

    try:
        with open(json_path, "w") as f:
            json.dump(notes, f, indent=2)

        convert_to_musicxml(
            str(json_path),
            key,
            time_signature,
            output_path=str(musicxml_path),
            title=base_filename,
        )

        midi_obj = json_to_midi(notes, instrument, tempo, time_signature, measures)
        midi_obj.save(str(midi_path))
    except Exception as e:
        return jsonify({"error": f"Conversion failed: {e}"}), 500

    return jsonify({
        "musicxml_url": f"/output/{base_filename}.musicxml",
        "midi_url":     f"/output/{base_filename}.mid",
        "notes":        notes,
        "tempo":        tempo,
    })


@app.route("/output/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR.resolve(), filename)


if __name__ == "__main__":
    app.run(debug=True)
