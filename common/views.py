# Create your views here.
import md5
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import time
from common.models import City


def index(request):
    if not request.session.has_key('mode'):
        request.session["mode"] = "user" #set user mode if not set
    if request.session["mode"] == "user":
        return HttpResponseRedirect(reverse('event.views.main'))
    if request.session["mode"] == "publish":
        return HttpResponseRedirect(reverse('blogs.views.manage'))
    pass

def switchMode(request, mode, defaultView):
    referer = request.META.get('HTTP_REFERER')
    if not referer: referer = reverse(defaultView)
    
    if not request.session.has_key('mode') or not request.session["mode"]:
        request.session["mode"] = 'user' #default mode
        
    try:
        # save last mode page
        request.session[request.session["mode"]]["lastPage"] = referer
    except KeyError:
        request.session[request.session["mode"]] = {'lastPage':referer}
    if request.session.has_key(mode) and request.session[mode]:
        # redirect to current mode last page
        request.session["mode"] = mode
        return HttpResponseRedirect(reverse(defaultView))

    request.session["mode"] = mode
    return HttpResponseRedirect(reverse(defaultView))


@login_required
@permission_required("publisher.publish")
def publisherMode(request):
    return switchMode(request, 'publish', 'blogs.views.manage')


def userMode(request):
    return switchMode(request, 'user', 'event.views.main')


@login_required
@permission_required("publisher.publish")
def uploadTempImage(request):
    imageUrl=False
    if request.method == "POST":
        file = request.FILES["file"]
        #TODO check if content type is correct
        print "Content type: " + file.content_type
        basename, extension = os.path.splitext(file.name)
        filename = "temp_"+request.user.first_name + str(time.time())
        dest = open(settings.MEDIA_ROOT + '/temp/'+ filename,"wb+")
        for chunk in file.chunks():
            dest.write(chunk)
        dest.close()
        imageUrl = settings.MEDIA_URL + '/temp/' + filename
    return render_to_response("common/uploadTempImage.html",
                              {
                                "imageUrl": imageUrl
                              },
                              context_instance=RequestContext(request)
                              )

def getCities(request):
    countryId = request.REQUEST.get("country",0)
    cities = City.objects.filter(country=countryId)
    json_serializer = json.Serializer()
    data= json_serializer.serialize(cities, ensure_ascii=False, use_natural_keys=True)
    return HttpResponse(data)
    pass