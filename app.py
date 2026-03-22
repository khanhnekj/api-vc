from flask import Flask, request, send_file
from gtts import gTTS
import io
import urllib.parse
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "TTS API OK"

@app.route("/tts")
def tts():
    text = request.args.get("text")

    if not text:
        return {"error": "Missing text"}, 400

    try:
        # fix lỗi tiếng Việt
        text = urllib.parse.unquote(text)

        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang="vi", slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        if mp3_fp.getbuffer().nbytes == 0:
            return {"error": "Empty audio"}, 500

        return send_file(mp3_fp, mimetype="audio/mpeg")

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
