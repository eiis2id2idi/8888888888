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
        "cookies_loaded": os.path.exists("cookies.txt")
    })


@app.route("/formats")
def formats():

    video_id = request.args.get("id")

    if not video_id:
        return jsonify({
            "error": "id obrigatório"
        }), 400


    url = f"https://www.youtube.com/watch?v={video_id}"


    try:

        opts = {
            "cookiefile": "cookies.txt",
            "quiet": True,
            "noplaylist": True
        }


        with yt_dlp.YoutubeDL(opts) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )


        lista = []

        for f in info.get("formats", []):

            lista.append({
                "format_id": f.get("format_id"),
                "ext": f.get("ext"),
                "acodec": f.get("acodec"),
                "vcodec": f.get("vcodec"),
                "audio": f.get("abr")
            })


        return jsonify({
            "title": info.get("title"),
            "formats": lista
        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
