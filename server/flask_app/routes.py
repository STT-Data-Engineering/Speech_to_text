"""Routes for parent Flask app."""
from flask import request, jsonify
from flask_app.helpers import extract_audio

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
        audio = request.files['audio']
        sentence = audio.filename
        audio = extract_audio(audio)
        print("sentence", sentence)

        return "200"

    

    return app
