"""Routes for parent Flask app."""
from flask import request, jsonify
import json
from datetime import datetime, timezone, timedelta


def init_routes(app):
    """A factory function that takes in the server 
    object and initializes the routes.
    """


    @app.route("/test")
    def test():
        return "Hello, world"

    @app.route('/get_text', methods=["GET"])
    def get_text():
        pass

    @app.route('/submit', methods=["POST"])
    def publish_text_audio_pair():
        pass

    

    return app
