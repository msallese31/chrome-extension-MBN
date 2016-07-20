from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import json
import youtube_dl
import requests
import wave
import os

url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?continuous=true'
username = '040c9c9a-791a-4a22-9989-d1c891148d96'
password = 'NNmNJPOAqdsU'

headers = {
	'content-type': 'audio/wav',
}

#TODO
#have global variable here that will hold the index of the video

# Create your views here.

def index(request):
    return HttpResponse("Index for video_process")


def check_index(request):
    #This function should be called when /video_process/checkindex is hit.
    #It should do the following:
    ####check the db if the link sent is in the db of indexes
    ####if the link is in the index db it should return true
    ####if not it should download the video, index it, and then return true
    ####if the video can't be indexed it should return false
    
    #TODO
    #When this function is called the global index variable should be cleared and updated

    #check the DB for link coming from front end (don't know yet how we're getting the link)

    #if link in DB return true

    #else download video, pass to watson, and index:
    link = request.GET.get('link')
    print(link)
    print('attempting to get youtube video')
    ydl_opts = {
        'format': 'bestaudio/best',
        # 'outtmpl': "/tmp/temp",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    #Stupid youtube-dl made me do this
    for filename in os.listdir("."):
    	if filename.endswith(".wav"):
    		os.rename(filename, "temp.wav")

    audio = open('/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/temp.wav', 'rb')
    r = requests.post(url, auth=(username, password), headers=headers, data=audio)
    jsonObject = r.json()
    print(jsonObject)
    text = jsonObject['results'][0]['alternatives'][0]['transcript']
    print(text)
    os.remove('/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/temp.wav')
    return HttpResponse(True)

def process_search_term(request):
    #This function should be called when /video_process/processSearchTerm is hit
    #A search term should be passed to this view
    #It should do the following:
    ####Search the index for the term given
    ####Return an array of times
    return HttpResponse(True)
