from __future__ import unicode_literals
from flask import render_template, request, send_file
from app import app
import yt_dlp
from yt_dlp.utils import DownloadError
import os
dirname = os.path.dirname(__file__)
print(dirname)
filename = os.path.join(dirname, 'downloads/')
print("________________________")
print(filename)


# Routing to home root
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():

    arr = os.listdir(filename)

    if len(arr) != 0:
        file = arr[0]
        file_path = filename + file
        if os.path.isfile(file_path):
            os.remove(file_path)
            print("File has been deleted")
        else:
            print("File does not exist")

    url = request.form['query']
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'app/downloads/%(title)s.%(ext)s',
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
            arr = os.listdir(filename)
            print(filename)
            print(len(arr))
            file = arr[0]
            print("Exception has been caught.")
            return send_file(filename + file, as_attachment=True)
    return render_template('index.html')
