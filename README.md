# CTRL-F Extension
#To get what we have up and running:
####1.) from the root of our git project `cd to POC/flask_tut`
####2.) `export FLASK_APP=hello.py`
####3.) `python -m flask run` 
this launches flask on `http://127.0.0.1:5000/` but if you don't have everything installed it may not work.  Also if you have a different version of flask/python it may not work.  See http://flask.pocoo.org/docs/0.11/quickstart/#quickstart
####4.) in chrome address bar type `chrome://extensions/`
####5.) Click load unpacked extension and select POC/chrome_restart/ (poorly named for now) from our project.  
Note: developer mode checkbox in top right must be checked.
####This should allow for you to hit the button in chrome and see action in your terminal where flask is running.  It may break but the ajax call works.  Much work to be done.
