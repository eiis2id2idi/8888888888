from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "YouTube yt-dlp Audio API"
    })


@app.route("/audio")
def audio():

    video_id = request.args.get("id")

    if not video_id:
        return jsonify({
            "error": "id obrigatório"
        }), 400


    youtube_url = f"https://www.youtube.com/watch?v={video_id}"


    try:

        options = {

            # tenta pegar somente áudio
            "format": "bestaudio/best",

            # não baixa arquivo
            "noplaylist": True,

            # reduz logs
            "quiet": True,

            # evita alguns bloqueios simples
            "nocheckcertificate": True,

            "http_headers": {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
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
                "error": "URL de áudio não encontrada"
            }), 404


        return jsonify({

            "success": True,

            "title": info.get("title"),

            "thumbnail": info.get("thumbnail"),

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


    for instance in PIPED_INSTANCES:

        try:

            url = f"{instance}/streams/{video_id}"

            print("Tentando:", url)


            response = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=15
            )


            print(
                "Status:",
                response.status_code
            )


            if response.status_code != 200:
                errors.append(
                    f"{instance}: HTTP {response.status_code}"
                )
                continue


            try:
                data = response.json()

            except:

                errors.append(
                    f"{instance}: resposta não é JSON"
                )
                continue



            audio_url = None


            for stream in data.get("audioStreams", []):

                if stream.get("url"):

                    audio_url = stream["url"]
                    break



            if audio_url:

                return jsonify({

                    "success": True,

                    "source": instance,

                    "title": data.get("title"),

                    "thumbnail": data.get("thumbnailUrl"),

                    "audio": audio_url

                })


            errors.append(
                f"{instance}: sem áudio"
            )


        except Exception as e:

            errors.append(
                f"{instance}: {str(e)}"
            )


        time.sleep(1)



    return jsonify({

        "success": False,

        "error": "Nenhum extractor funcionou",

        "details": errors

    }), 500



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=10000
                    )
