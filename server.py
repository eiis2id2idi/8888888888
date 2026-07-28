from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status":"online",
        "service":"Audio Server"
    })


@app.route("/audio")
def get_audio():

    video_id = request.args.get("id")

    if not video_id:
        return jsonify({
            "error":"id obrigatório"
        }),400


    url = "https://www.youtube.com/watch?v=" + video_id


    try:

        options = {
            "format":"bestaudio",
            "quiet":True,
            "noplaylist":True
        }


        with yt_dlp.YoutubeDL(options) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )


        return jsonify({

            "title": info.get("title"),

            "audio": info.get("url"),

            "thumbnail": info.get("thumbnail")

        })


    except Exception as e:

        return jsonify({
            "error":str(e)
        }),500



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
