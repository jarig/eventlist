from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template.context import RequestContext



def create(request):
    return HttpResponse("Create Event")

def main(request):
    test = "testVar, REQUEST: "
    for var in request.REQUEST:
        test += var + "="+ request.REQUEST[var]

    return render_to_response("events/events_main.html",
                              {
                              },
                              context_instance=RequestContext(request)
                              )

