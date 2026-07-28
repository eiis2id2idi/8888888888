from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "YouTube Audio API"
    })


@app.route("/audio")
def audio():

    video_id = request.args.get("id")

    if not video_id:
        return jsonify({
            "error": "id obrigatório"
        }), 400


    try:

        # Instância da API Piped
        api_url = f"https://pipedapi.kavin.rocks/streams/{video_id}"


        response = requests.get(
            api_url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )


        print("STATUS:", response.status_code)
        print("RESPOSTA:", response.text[:300])


        try:
            data = response.json()

        except:

            return jsonify({
                "error": "Extractor não retornou JSON",
                "status": response.status_code,
                "response": response.text[:300]
            }), 500



        audio_url = None


        # Procura stream de áudio
        streams = data.get("audioStreams", [])


        for stream in streams:

            if stream.get("url"):

                audio_url = stream["url"]
                break



        if not audio_url:

            return jsonify({

                "error": "Nenhum áudio encontrado",

                "title": data.get("title"),

                "keys": list(data.keys())

            }), 404



        return jsonify({

            "success": True,

            "title": data.get("title"),

            "thumbnail": data.get("thumbnailUrl"),

            "audio": audio_url

        })



    except requests.exceptions.Timeout:

        return jsonify({
            "error": "Tempo limite excedido"
        }), 500



    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
