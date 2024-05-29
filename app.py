from flask import Flask, send_from_directory, request, jsonify, render_template
import os
import subprocess

app = Flask(__name__)
MEDIA_FOLDER = 'media'


@app.route('/')
def index():
    return render_template('media_list.html')


@app.route('/media/<path:filename>')
def serve_media(filename):
    return send_from_directory(MEDIA_FOLDER, filename)


@app.route('/media/list')
def list_media():
    media_files = []
    for root, dirs, files in os.walk(MEDIA_FOLDER):
        for file in files:
            if file.endswith(('.mp4', '.jpg', '.jpeg', '.png')):
                media_files.append(os.path.relpath(os.path.join(root, file), MEDIA_FOLDER))
    return jsonify(media_files)


def transcode_video(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', output_file]
    subprocess.run(command)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
