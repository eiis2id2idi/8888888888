from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "YouTube Audio API",
        "cookies": os.path.exists("cookies.txt")
    })


@app.route("/audio")
def audio():

    video_id = request.args.get("id")

    if not video_id:
        return jsonify({
            "error": "Informe o id do vídeo"
        }), 400


    youtube_url = f"https://www.youtube.com/watch?v={video_id}"


    try:

        options = {

            # pega somente áudio
            "format": "bestaudio/best",

            # não pega playlist
            "noplaylist": True,

            # não baixa arquivo
            "skip_download": True,

            # usa cookies
            "cookiefile": "cookies.txt",

            # evita muitos logs
            "quiet": True,

            # alguns ajustes de conexão
            "nocheckcertificate": True,

            "http_headers": {
                "User-Agent":
                "Mozilla/5.0 (Linux; Android 13)"
            }
        }


        with yt_dlp.YoutubeDL(options) as ydl:

            info = ydl.extract_info(
                youtube_url,
                download=False
            )


        audio_url = info.get("url")


        if not audio_url:

            return jsonify({
                "error": "Não encontrou URL de áudio"
            }), 404



        return jsonify({

            "success": True,

            "title": info.get("title"),

            "thumbnail": info.get("thumbnail"),

            "duration": info.get("duration"),

            "audio": audio_url

        })


    except Exception as e:

        print("ERRO:", e)

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
