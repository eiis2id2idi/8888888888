
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
        }), 400


    try:

        # API extractor
        url = f"https://piped.video/api/v1/streams/{video_id}"


        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )


        print("STATUS API:", response.status_code)
        print("RESPOSTA API:", response.text[:500])


        # Verifica se retornou JSON
        try:
            data = response.json()

        except Exception:

            return jsonify({
                "error": "API não retornou JSON",
                "status": response.status_code,
                "response": response.text[:500]
            }), 500



        audio_url = None


        # Procura áudio
        for stream in data.get("audioStreams", []):

            if stream.get("url"):

                audio_url = stream["url"]
                break



        if not audio_url:

            return jsonify({

                "error": "Nenhum áudio encontrado",

                "available_keys": list(data.keys())

            }),404



        return jsonify({

            "title": data.get("title"),

            "thumbnail": data.get("thumbnailUrl"),

            "audio": audio_url

        })



    except requests.exceptions.Timeout:

        return jsonify({
            "error": "Timeout ao acessar extractor"
        }),500



    except Exception as e:

        return jsonify({
            "error": str(e)
        }),500



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
