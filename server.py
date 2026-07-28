from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "online"
    })


@app.route("/test")
def test():

    vid = request.args.get("id")

    if not vid:
        return jsonify({"error":"id faltando"})


    url = f"https://youtube.com/watch?v={vid}"


    try:

        opts = {
            "cookiefile": "cookies.txt",
            "quiet": False,
            "noplaylist": True,

            "extractor_args": {
                "youtube": {
                    "player_client": ["android"]
                }
            }
        }


        with yt_dlp.YoutubeDL(opts) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )


        return jsonify({
            "title": info.get("title"),
            "formats": len(info.get("formats", [])),
            "url": info.get("url")
        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
