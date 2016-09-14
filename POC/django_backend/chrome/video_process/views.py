from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import youtube_dl
import requests
import wave
import os
from multiprocessing import Process, Lock
from multiprocessing.dummy import Pool as ThreadPool
import datetime
from time import sleep
import wave
from gevent.pool import Pool
from urlparse import urlparse
import httplib, sys
from Queue import Queue
import grequests
import subprocess
import re


url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?continuous=true&timestamps=true'
username = '040c9c9a-791a-4a22-9989-d1c891148d96'
password = 'NNmNJPOAqdsU'

headers = {
	'content-type': 'audio/wav',
		'timestamps': 'true'
}
w = []
mutex = Lock()
fileMutex = Lock()
audio = ''

switch = 0
num_txt_files = 0

#TODO
#have global variable here that will hold the index of the video

# Create your views here.

def index(request):
	print("dummy")
	return HttpResponse("Index for video_process")

def cleanup():
	os.system('rm temp.wav || true;rm speech-to-text-websockets-python/recordings/*.wav || true;rm speech-to-text-websockets-python/output/*.txt || true;rm speech-to-text-websockets-python/recordings.txt || true')

def split_wav(split_start, split_end, file_index):
	print("splitting")
	input_file = wave.open('/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/temp.wav', 'r')
	width = input_file.getsampwidth()
	rate = input_file.getframerate()
	fpms = rate / 1000 # frames per ms
	#programmatically figure out start and end split
	length = (split_end - split_start) * fpms
	start_index = split_start * fpms
	path = str('/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/speech-to-text-websockets-python/recordings/') + str(file_index) + ".wav"
	# os.mkdir(path)
	output_file = wave.open(path, "w")
	output_file.setparams((input_file.getnchannels(), width, rate, length, input_file.getcomptype(), input_file.getcompname()))
	
	input_file.rewind()
	anchor = input_file.tell()
	input_file.setpos(anchor + start_index)
	output_file.writeframes(input_file.readframes(length))
	input_file.close()
	output_file.close()
	print("finished split")
	print("writing to recordings.txt")
	if(file_index == 0):
		print(file_index)
		with open("/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/speech-to-text-websockets-python/recordings.txt", "w") as myfile:
			myfile.write(str('/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/speech-to-text-websockets-python/recordings/') + str(file_index) + ".wav\n")
	else:
		print(file_index)
		with open("/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/speech-to-text-websockets-python/recordings.txt", "a") as myfile:
			myfile.write(str('/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/speech-to-text-websockets-python/recordings/') + str(file_index) + ".wav\n")		


def multi_thread(num_threads):
	threads = []
	for i in range(num_threads):
		# p = Process(target=watson_request, args=(i,))
		p = Process(target=test_wat, args=(i,))
		p.start()
		# threads.append(p)
	print("ALL THREADS STARTED AT")
	print(datetime.datetime.now())

def do_something(response, **kwargs):
	print(response)

def greqs(num_threads):
	async_list = []
	for i in range(num_threads):
		audio = open("/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/%d.wav" % i, 'rb')
		req = grequests.post(url, auth=(username, password), headers=headers, data=audio, hooks = {'response' : do_something})
		print(req.kwargs)
		async_list.append(req)
	response = grequests.map(async_list)
	print(response.json)




def get_wav_length(file):
	wave_file = wave.open(file, 'r')
	frames = wave_file.getnframes()
	rate = wave_file.getframerate()
	duration = frames / float(rate)
	return duration

# def copy_sockets_solution(threads):
# 	q = Queue.Queue()
# 	for i in range(threads):





def get_split_times(total_length):
	#total_length is the total length of the video in seconds
	#num_pieces IS THE NUMBER OF 2 MINUTE PIECES
	num_pieces = total_length / 120
	print(num_pieces)
	
	#piece_length IS THE LENGTH OF THE PIECES THEMSELVES
	if(num_pieces <= 400):
		piece_length = 120
	else:
		num_pieces = 400
		piece_length = total_length / num_pieces
	splits = []
	start_time = 0.0
	for i in range(0, int(num_pieces)):
		print("piece number %d" % i)
		print("start at %f" % start_time)
		print("end at %f" % (start_time + piece_length))
		splits.append(((start_time * 1000), ((start_time + piece_length) * 1000)))
		start_time += piece_length
	if((num_pieces % int(num_pieces)) > 0):
		splits.append(((start_time * 1000), (total_length * 1000)))
	print(splits)
	print(len(splits))
	return splits
	#piece_length WILL ALWAYS BE 120 SECONDS UNLESS A VIDEO 
	#GOES PAST 50 PIECES (WHICH MEANS IT WOULD REQUIRE > 50 THREADS).
	#50 IS A MADE UP NUMBER RIGHT NOW BUT THERE MUST BE SOME SAFE
	#NUMBER OF THREADS TO USE

def check_urls(req_num):

	def fetch(file_index):
		print("fetching req# %d" %i)
		audio = open("/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/%d.wav" % file_index, 'rb')
		response = requests.post(url, auth=(username, password), headers=headers, data=audio)
		print "Status: [%s] URL: %s" % (response.status_code, url)
		print(datetime.datetime.now())

	pool = Pool(req_num)
	for i in range(req_num):
		pool.spawn(fetch, i)
	pool.join()


def watson_request(file_index):
	print ("Openening: /home/sallese/chrome-extension-MBN/POC/django_backend/chrome/%d.wav" % file_index)
	fileMutex.acquire()
	audio = open("/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/%d.wav" % file_index, 'rb')
	fileMutex.release()
	print("About to call %d.wav request" % file_index)
	r = requests.post(url, auth=(username, password), headers=headers, data=audio)
	# print("%d.wav request finished" % file_index) 
	jsonObject = r.json()
	# print(jsonObject)
	# text = jsonObject['results'][0]['alternatives'][0]['transcript']
	# print(text)
#    for text in jsonObject['results'][0]['alternatives'][0]['timestamps']:
 #       print(text)
	mutex.acquire()
	for text in jsonObject['results']:
		for words in text['alternatives'][0]['timestamps']:
			w.append(words)
	mutex.release()
	print(words[-1])
	print("Request number %d is done with mutex" % file_index)
	print(datetime.datetime.now())
	# print(w)

def dummy_threading_function(i):
	print "thread %d sleeps for 2 seconds" % i
	sleep(5)
	print "thread %d woke up" % i

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
	cleanup()
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

	print(datetime.datetime.now())
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([link])

	print(datetime.datetime.now())

	#Stupid youtube-dl made me do this
	for filename in os.listdir("."):
		if filename.endswith(".wav"):
			os.rename(filename, "temp.wav")
	wav_length = get_wav_length('/home/sallese/chrome-extension-MBN/POC/django_backend/chrome/temp.wav')
	print(wav_length)
	#Get the split times
	splits = get_split_times(wav_length)
	#Split the wav into pieces
	for i, split in enumerate(splits):
		split_wav(int(split[0]), int(split[1]), i)

	print(datetime.datetime.now())
	num_threads = len(splits)
	print("NUMBER OF SPLITS")
	print(num_threads)

	num_threads = num_threads

	now = str(datetime.datetime.now()).replace(" ","")
	f = open('info-%s.txt' % now, 'a')

	now = str(datetime.datetime.now()).replace(" ","")
	f.write("Called Watson at: %s" % now + "\n")
	
	os.system('python speech-to-text-websockets-python/sttClient.py -credentials 040c9c9a-791a-4a22-9989-d1c891148d96:NNmNJPOAqdsU -model en-US_BroadbandModel -threads %d' % num_threads)
	#words_with_index = jsonObject['results'][0]['alternatives'][0]['timestamps']
	now = str(datetime.datetime.now()).replace(" ","")
	f.write("Finished Watson at: %s" % now + "\n")
	f.write("num_threads = %d" % num_threads + "\n")
	f.write("number of splits = %d" % len(splits) + "\n")
	f.close()

	num_txt_files = len(splits) - 1

	w = []

	for i in range(num_txt_files):
		with open('speech-to-text-websockets-python/output/%d.json.txt' % i) as f:
			content = f.readlines()
			for index, d in enumerate(content):
				current_line = content[index].split()
				current_line.append(i*2)
				w.append(current_line)

	return HttpResponse(json.dumps(w), content_type="application/json")

def process_search_term(request):
	w = []
	words = []
	for i in range(7):
		with open('speech-to-text-websockets-python/output/%d.json.txt' % i) as f:
			content = f.readlines()
			for index, d in enumerate(content):
				current_line = content[index].split()
				current_line.append(i*2)
				words.append(current_line[0])
				w.append(current_line)

	path = request.get_full_path()

	print(w)

	result = re.findall(r'w[0-9]=(.*?)&',path)
	print(result)

	for searchT in result:
		if(searchT in s for index, s in enumerate(words)):
			print(searchT)
			print w[index]


	words = []
	words.append(request.GET.get('w1'))
	words.append(request.GET.get('w2'))
	words.append(request.GET.get('w3'))
	words.append(request.get_full_path())
	# if len(sys.argv) > 1:
	# 	for i in range(len(sys.argv)-1):
	# 		words.append(request.GET.get('w%d' % i))

	return HttpResponse(json.dumps(result))