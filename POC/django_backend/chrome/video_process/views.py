from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import json
import youtube_dl
import requests
import wave

url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
username = '040c9c9a-791a-4a22-9989-d1c891148d96'
password = 'NNmNJPOAqdsU'

headers={'content-type': 'audio/wav'}

#TODO
#have global variable here that will hold the index of the video

# Create your views here.

def index(request):
    link = request.GET.get('link')
    print(link)
    print('attempting to get youtube video')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/home/sallese/chrome-extension-MBN/testing.wav',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    audio = open('/home/sallese/chrome-extension-MBN/eric.wav', 'rb')
    print("sending video to watson")
    r = requests.post(url, auth=(username, password), headers=headers, data=audio)
    jsonObject = r.json()
    text = jsonObject['results'][0]['alternatives'][0]['transcript']
    print(text)
    return HttpResponse(str(text))


def check_index(request):
    #This function should be called when /video_process/checkindex is hit.
    #It should do the following:
    ####check the db if the link sent is in the db of indexes
    ####if the link is in the index db it should return true
    ####if not it should download the video, index it, and then return true
    ####if the video can't be indexed it should return false
    
    #TODO
    #When this function is called the global index variable should be cleared and updated
    
    return HttpResponse(True)

def process_search_term(request):
    #This function should be called when /video_process/processSearchTerm is hit
    #A search term should be passed to this view
    #It should do the following:
    ####Search the index for the term given
    ####Return an array of times
    return HttpResponse(True)
