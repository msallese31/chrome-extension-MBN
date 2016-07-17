import requests
import json

url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
username = '040c9c9a-791a-4a22-9989-d1c891148d96'
password = 'NNmNJPOAqdsU'

headers={'content-type': 'audio/wav'}

audio = open('/home/sallese/flask_tut/obama.wav', 'rb')

r = requests.post(url, auth=(username, password), headers=headers, data=audio)

print json.loads(r.text)
