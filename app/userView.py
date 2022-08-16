from __future__ import unicode_literals
from flask import render_template, request, send_file
from app import app
import yt_dlp
from yt_dlp.utils import DownloadError
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'downloads/')


@app.route('/')
@app.route('/mp3')
def mp3home():
    tp = 'Mp3'
    source = 'YouTube'
    return render_template('index.html', tp=tp, source=source)


@app.route('/mp4')
def mp4home():
    tp = 'Mp4'
    source = 'YouTube'
    return render_template('index.html', tp=tp, source=source)


@app.route('/tiktok')
def tiktokhome():
    tp = 'Video'
    source = 'TikTok'
    return render_template('index.html', tp=tp, source=source)


@app.route('/twitch')
def twitchhome():
    tp = 'Video'
    source = 'Twitch'
    return render_template('index.html', tp=tp, source=source)

@app.route('/download')
def initial():
    tp = 'Mp3'
    source = 'YouTube'
    return render_template('index.html', tp=tp, source=source)


@app.route('/download', methods=['POST'])
def get():
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
    typeFromHtml = request.form['tp']
    if typeFromHtml == 'Mp3':
        type = 'bestaudio/best'
    elif typeFromHtml == 'Twitch' or typeFromHtml == 'Tiktok' or typeFromHtml == 'Mp4' or typeFromHtml == 'Video':
        type = 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/mp4+best[height<=480]'
    else:
        return render_template('index.html')
    ydl_opts = {
        'format': type,
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
            file = arr[0]
            print("Exception has been caught.")
            return send_file(filename + file, as_attachment=True)
    return render_template('index.html')


@app.route('/mp4')
def mp4():
    tp = 'Mp4'
    source = 'YouTube'
    get()
    return render_template('index.html', tp=tp, source=source)


@app.route('/mp3')
def mp3():
    tp = 'Mp3'
    source = 'YouTube'
    get()
    return render_template('index.html', tp=tp, source=source)


@app.route('/tiktok')
def tiktok():
    source = 'TikTok'
    tp = 'Video'
    get()
    return render_template('index.html', tp=tp, source=source)


@app.route('/twitch')
def twitch():
    source = 'Twitch'
    tp = 'Video'
    get()
    return render_template('index.html', tp=tp, source=source)