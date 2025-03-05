from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Cookies file ka path (Assuming file is in the same directory as app.py)
COOKIES_PATH = "./cookies.txt"

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    if not os.path.exists(COOKIES_PATH):
        return jsonify({"error": "Cookies file not found"}), 500

    try:
        ydl_opts = {
            "format": "best",
            "cookies": COOKIES_PATH
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"title": info["title"], "url": info["url"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render environment variable PORT use karein, default 5000 agar not set hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
