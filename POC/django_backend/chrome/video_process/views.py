from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.

def index(request):
    listToReturn = json.dumps({"test_list_of_times" : ["1:31", "0:12"]})
    return HttpResponse(listToReturn, content_type="application/json")
