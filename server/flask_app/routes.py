"""Routes for parent Flask app."""
import sys
sys.path.append('../scripts')
from all_kafka import AllKafka
from flask import request, jsonify
from flask_app.helpers import extract_audio
from flask_app.helpers import get_uuid
from pprint import pprint
from kafka.errors import NoBrokersAvailable



def init_routes(app):
    """A factory function that takes in the server 
    object and initializes the routes.
    """
    try:
        producer = AllKafka.create_producer()
        consumer = AllKafka.create_consumer(topic="text")
    except NoBrokersAvailable:
        print("NoBrokersAvailable")

    @app.route("/test")
    def test():
        return "Hello, world"

    @app.route('/get_text', methods=["GET"])
    def get_text():
        print("sending text")
        try:
            for s in consumer:
                print(s.value)
            # sentence = next(consumer)
            # print(sentence)
                sentence = s.value
            # sentence = "አገራችን ከአፍሪካም ሆነ ከሌሎች የአለም አገራት ጋር ያላትን አለም አቀፋዊ ግንኙነት ወደ ላቀ ደረጃ ያሸጋገረ ሆኗል በአገር ውስጥ አራት አለም"
                return jsonify(text=sentence)
        except NameError:
            print("Consumer not init")
            sentence = "አገራችን ከአፍሪካም ሆነ ከሌሎች የአለም አገራት ጋር ያላትን አለም አቀፋዊ ግንኙነት ወደ ላቀ ደረጃ ያሸጋገረ ሆኗል በአገር ውስጥ አራት አለም"
            return jsonify(text=sentence)

    @app.route('/submit', methods=["POST"])
    def publish_text_audio_pair():
        audio = request.files['audio']
        sentence = audio.filename
        audio = extract_audio(audio)
        print(audio.shape)
        audio = audio.tolist()
        id = get_uuid()
        data = {
            "id": id,
            "sentence": sentence,
            "audio": audio
        }
        try:
            res = producer.send("text.audio.pair", value=data)
            print(res)
        except NameError:
            print("Producer not created")

        # pprint(data)

        return "200"

    return app
