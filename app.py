from flask import Flask, request, jsonify, abort
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

IMAGE_EXTENSIONS = {"png","jpg","jpeg","gif","bmp","webp"}
VIDEO_EXTENSIONS = {"mp4","mov","avi","mkv","webm","flv","mpeg"}

# Directory inside the container where uploads are stored. Mount a host folder
# into this path when running the container (see README).
UPLOAD_DIR = os.environ.get('UPLOAD_DIR', '/app/uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 * 1024  # 4 GiB max

def allowed_file(filename, mimetype):
    if '.' in filename:
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in IMAGE_EXTENSIONS or ext in VIDEO_EXTENSIONS:
            return True
    if mimetype:
        if mimetype.startswith('image/') or mimetype.startswith('video/'):
            return True
    return False

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status':'ok'}), 200

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error':'no file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'no selected file'}), 400
    if not allowed_file(file.filename, file.mimetype):
        return jsonify({'error':'file type not allowed'}), 400

    # Optional subdirectory (sanitized simple name)
    subdir = request.form.get('subdir', '').strip()
    if subdir:
        # sanitize: allow only alnum, dash, underscore
        import re
        if not re.fullmatch(r'[A-Za-z0-9_\-]+', subdir):
            return jsonify({'error':'invalid subdir name'}), 400
        target_dir = os.path.join(UPLOAD_DIR, subdir)
    else:
        target_dir = UPLOAD_DIR

    os.makedirs(target_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')
    saved_name = f"{timestamp}_{filename}"
    save_path = os.path.join(target_dir, saved_name)
    file.save(save_path)

    # Return the path relative to the container upload dir
    rel_path = os.path.relpath(save_path, UPLOAD_DIR)
    return jsonify({'success': True, 'saved_as': rel_path}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
