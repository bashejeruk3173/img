from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Authentication Key (change this for security)
AUTH_KEY = "your_secret_key"

# Base directory for storing images
BASE_DIR = "/manga"

@app.route("/download", methods=["POST"])
def download_image():
    # Authentication
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {AUTH_KEY}":
        return jsonify({"error": "Unauthorized"}), 403

    # Get parameters
    image_url = request.json.get("image_url")
    manga = request.json.get("manga")
    chapter = request.json.get("chapter")

    if not all([image_url, manga, chapter]):
        return jsonify({"error": "Missing parameters"}), 400

    # Define directory structure
    manga_path = os.path.join(BASE_DIR, manga, chapter)
    
    if not os.path.exists(manga_path):
        return jsonify({"error": "Directory does not exist"}), 404

    # Download image
    try:
        image_data = requests.get(image_url, stream=True)
        if image_data.status_code != 200:
            return jsonify({"error": "Failed to download image"}), 500

        image_filename = os.path.basename(image_url)
        image_path = os.path.join(manga_path, image_filename)

        with open(image_path, "wb") as f:
            for chunk in image_data.iter_content(1024):
                f.write(chunk)

        return jsonify({"file_path": image_path})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
