from __future__ import unicode_literals
from flask import render_template, request, send_file
from app import app
import yt_dlp
from yt_dlp.utils import DownloadError
import os


# Routing to home root
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    arr = os.listdir('app/app/downloads/')
    if len(arr) != 0:
        file = arr[0]
        file_path = r'app/app/downloads/' + file
        if os.path.isfile(file_path):
            os.remove(file_path)
            print("File has been deleted")
        else:
            print("File does not exist")
    url = request.form['query']
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'app/app/downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except DownloadError:
            arr = os.listdir('app/app/downloads/')
            file = arr[0]
            print("Exception has been caught.")
        return send_file(r'downloads/' + file, as_attachment=True)

    return render_template('index.html')
