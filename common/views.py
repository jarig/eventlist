# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from common.models import City, Address


def index(request):
    if not request.session.has_key('mode'):
        request.session["mode"] = "user" #set user mode if not set
    if request.session["mode"] == "user":
        return HttpResponseRedirect(reverse('event.views.main'))
    if request.session["mode"] == "publish":
        return HttpResponseRedirect(reverse('blog.views.manage'))
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
    return switchMode(request, 'publish', 'blog.views.manage')


def userMode(request):
    return switchMode(request, 'user', 'event.views.main')

def getCities(request):
    countryId = request.REQUEST.get("country",0)
    cities = City.objects.filter(country=countryId)
    json_serializer = json.Serializer()
    data= json_serializer.serialize(cities, ensure_ascii=False, use_natural_keys=True)
    return HttpResponse(data)
    pass

def getAddress(request):
    adrId = request.REQUEST.get("id",0)
    address = Address.objects.filter(pk=adrId)
    json_serializer = json.Serializer()
    data= json_serializer.serialize(address, ensure_ascii=False, use_natural_keys=True)
    return HttpResponse(data)