from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from menu.models import Menu


@login_required
def findPlace(request):
    return render_to_response("search/search_find.html",
                          {#data here
                            "subMenuItems": generateMenu(request)
                          },
                          context_instance=RequestContext(request)
                          )
@login_required
def findParty(request):
    return render_to_response("search/search_find.html",
                          {#data here
                            "subMenuItems": generateMenu(request)
                          },
                          context_instance=RequestContext(request)
                          )

def generateMenu(request):
    menu = Menu(RequestContext(request))
    menu.addItem('Place','search.views.findPlace')
    menu.addItem('Party','search.views.findParty')
    return menu.getMenu()