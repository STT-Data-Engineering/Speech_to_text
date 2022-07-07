"""Routes for parent Flask app."""
from email.mime import audio
from flask import request, jsonify
import json
from datetime import datetime, timezone, timedelta
from pprint import pprint
import librosa


def extract_audio(audio, sr=8000):
    wav, sample_rate = librosa.load(audio, sr=sr)
    dur = float(len(wav) / sample_rate)
    channel = len(wav.shape)
    print(f"Audio has {channel} channels")
    wav_return = wav
    return wav_return


def init_routes(app):
    """A factory function that takes in the server 
    object and initializes the routes.
    """


    @app.route("/test")
    def test():
        return "Hello, world"

    @app.route('/get_text', methods=["GET"])
    def get_text():
        sentence = "አገራችን ከአፍሪካም ሆነ ከሌሎች የአለም አገራት ጋር ያላትን አለም አቀፋዊ ግንኙነት ወደ ላቀ ደረጃ ያሸጋገረ ሆኗል በአገር ውስጥ አራት አለም"
        return jsonify(text=sentence)

    @app.route('/submit', methods=["POST"])
    def publish_text_audio_pair():
        # data = json.loads(request.data)
        # pprint(data)
        # pprint(request.files)
        # audio = request.files
        pprint(request.data)
        # audio = request.json.data
        # audio = extract_audio(audio)
        # if data.get("transcription").get("type") == 'audio/wav':
            # pprint(request.files)
        return "200"

    

    return app
