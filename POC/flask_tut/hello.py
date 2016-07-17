from __future__ import unicode_literals
from flask import Flask, jsonify
import youtube_dl
import requests
import json

url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
username = '040c9c9a-791a-4a22-9989-d1c891148d96'
password = 'NNmNJPOAqdsU'

headers={'content-type': 'audio/wav'}


app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hey world"

@app.route('/getspeechtotext')
def getsp():
    print('attempting to get a youtube video')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/home/sallese/flask_tut/test.wav',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=sZdetmEAtxA'])
    audio = open('/home/sallese/flask_tut/obama.wav', 'rb')
    r = requests.post(url, auth=(username, password), headers=headers, data=audio)
    return r.text
