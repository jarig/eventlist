# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


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
        return HttpResponseRedirect(request.session[mode]["lastPage"])

    request.session["mode"] = mode
    return HttpResponseRedirect(reverse(defaultView))


@login_required
@permission_required("publisher.publish")
def publisherMode(request):
    return switchMode(request, 'publish', 'blogs.views.manage')

@login_required
def userMode(request):
    return switchMode(request, 'user', 'event.views.main')


