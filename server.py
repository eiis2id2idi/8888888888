from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "Audio Extractor API"
    })


@app.route("/audio")
def audio():

    video_id = request.args.get("id")

    if not video_id:
        return jsonify({
            "error": "video id obrigatório"
        }),400


    try:

        url = f"https://piped.video/api/v1/streams/{video_id}"


        r = requests.get(
            url,
            timeout=15
        )


        data = r.json()


        audio = None

        for stream in data.get("audioStreams", []):

            if stream.get("url"):
                audio = stream["url"]
                break


        if not audio:
            return jsonify({
                "error":"audio não encontrado"
            }),404


        return jsonify({

            "title": data.get("title"),

            "thumbnail": data.get("thumbnailUrl"),

            "audio": audio

        })


    except Exception as e:

        return jsonify({
            "error":str(e)
        }),500



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
