import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory, render_template

from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from services.text_extraction import extract_text
from services.summarizer import summarize_text
from services.tts_service import generate_audio
from services.video_service import generate_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/process", methods=["POST"])
def process_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    file_ext = filename.rsplit('.', 1)[1].lower()
    extracted_text = extract_text(file_path, file_ext)
    summary = summarize_text(extracted_text)

    audio_path = generate_audio(summary)
    audio_url = f"/uploads/{os.path.basename(audio_path)}"

    video_path = generate_video(summary, audio_path)
    video_url = f"/uploads/{os.path.basename(video_path)}"

    return jsonify({
        "filename": filename,
        "summary": summary,
        "audio_url": audio_url,
        "video_url": video_url
    })

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
