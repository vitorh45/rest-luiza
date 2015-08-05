from django.shortcuts import render
from django.http import HttpResponse
import requests

def person(request):
    url = requests.get('https://graph.facebook.com/100002348657671').json()
    print url
    return HttpResponse('ok')