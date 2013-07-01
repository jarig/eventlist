# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect, HttpResponse
from common.models import City, Address


def index(request):
    if not request.session.has_key('mode'):
        request.session["mode"] = "user"  # set user mode if not set
    if request.session["mode"] == "user":
        return HttpResponseRedirect(reverse(settings.USER_MAIN_VIEW))
    if request.session["mode"] == "publish":
        return HttpResponseRedirect(reverse(settings.PUBLISHER_MAIN_VIEW))
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
        request.session[request.session["mode"]] = {'lastPage': referer}
    if request.session.has_key(mode) and request.session[mode]:
        # redirect to current mode last page
        request.session["mode"] = mode
        return HttpResponseRedirect(reverse(defaultView))

    request.session["mode"] = mode
    return HttpResponseRedirect(reverse(defaultView))


@login_required
@permission_required("publisher.publish")
def publisherMode(request):
    return switchMode(request, 'publish', settings.PUBLISHER_MAIN_VIEW)


def userMode(request):
    return switchMode(request, 'user', settings.USER_MAIN_VIEW)

def getCities(request):
    countryId = request.REQUEST.get("country",0)
    cities = City.objects.filter(country=countryId)
    json_serializer = json.Serializer()
    data= json_serializer.serialize(cities, ensure_ascii=False, use_natural_keys=True)
    return HttpResponse(data)
    pass

def findAddress(request):
    term = request.REQUEST.get('term','')
    address = Address.objects.filter(Q(name__icontains=term) | Q(street__icontains=term)).order_by('-name','-street')[:5]
    print address
    json_serializer = json.Serializer()
    data= json_serializer.serialize(address, ensure_ascii=False, use_natural_keys=True)
    return HttpResponse(data)

def getAddress(request):
    adrId = request.REQUEST.get("id",0)
    address = Address.objects.filter(pk=adrId)
    json_serializer = json.Serializer()
    data= json_serializer.serialize(address, ensure_ascii=False, use_natural_keys=True)
    return HttpResponse(data)