from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    test = "testVar, REQUEST="+request.REQUEST
    return render_to_response("main/index.html",{"test":test})