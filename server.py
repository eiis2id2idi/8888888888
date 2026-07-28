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
        "cookies_loaded": os.path.exists("cookies.txt")
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

        ydl_opts = {

            # tenta vários formatos
            "format": "bestaudio/best/best",

            "noplaylist": True,

            "skip_download": True,

            # usa autenticação
            "cookiefile": "cookies.txt",

            "quiet": True,

            "nocheckcertificate": True,

            "extract_flat": False,

            "http_headers": {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        }


        print("Extraindo:", youtube_url)


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                youtube_url,
                download=False
            )


        audio_url = info.get("url")


        # caso o formato principal não venha
        if not audio_url and info.get("formats"):

            for fmt in reversed(info["formats"]):

                if fmt.get("url"):

                    audio_url = fmt["url"]
                    break



        if not audio_url:

            return jsonify({
                "error": "Nenhum link de áudio encontrado"
            }), 404



        return jsonify({

            "success": True,

            "title": info.get("title"),

            "thumbnail": info.get("thumbnail"),

            "duration": info.get("duration"),

            "video_id": video_id,

            "audio": audio_url

        })



    except Exception as e:

        print("ERRO:", str(e))

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
    )
