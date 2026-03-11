from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app import app

from src.services.transcription_service import transcribe_audio_file

@app.route("/transcribe", methods=["POST"])
@jwt_required()
def transcribe_audio():

    if "file" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["file"]

    try:
        text = transcribe_audio_file(audio_file)
        return jsonify({"text": text}), 200

    except Exception as e:
        print(f"Transcription Error: {e}")
        return jsonify({"error": "Failed to transcribe audio"}), 500