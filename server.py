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
        "cookies": os.path.exists("cookies.txt")
    })


@app.route("/audio")
def audio():

    video_id = request.args.get("id")

    if not video_id:
        return jsonify({
            "error": "id faltando"
        })


    url = f"https://www.youtube.com/watch?v={video_id}"


    try:

        ydl_opts = {

            "cookiefile": "cookies.txt",

            "noplaylist": True,

            "quiet": False,

            "format": "worstaudio/worst",

            "extractor_args": {
                "youtube": {
                    "player_client": [
                        "android",
                        "web"
                    ]
                }
            },

            "http_headers": {
                "User-Agent":
                "Mozilla/5.0 (Linux; Android 13)"
            }
        }


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )


        return jsonify({
            "success": True,
            "title": info.get("title"),
            "formats": len(info.get("formats", [])),
            "audio": info.get("url")
        })


    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
