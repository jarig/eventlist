from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from account.models import Account
from menu.models import Menu
from search.forms import SearchPeopleForm


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
@login_required
def findPeople(request):
    users = None
    friendsList = None
    if request.GET:
        searchForm = SearchPeopleForm(request.GET)
        if searchForm.is_valid():
            search = searchForm.cleaned_data["search"]
            user = request.user
            friendsList = [i[0] for i in request.user.friends.all().values_list("pk")]
            users = Account.objects.only('first_name','last_name','id','avatar','sex','age').filter(~Q(pk=user)).filter(Q(first_name__icontains=search) |
                                           Q(last_name__icontains=search)).order_by('-rating')[:20]
        pass
    else:
        searchForm = SearchPeopleForm()

    return render_to_response("search/search_people.html",
            {#data here
             "subMenuItems": generateMenu(request),
             "searchForm": searchForm,
             "friendsList": friendsList,
             "users": users,
        },
        context_instance=RequestContext(request)
    )

def generateMenu(request):
    menu = Menu(RequestContext(request))
    menu.addItem('Place','search.views.findPlace')
    menu.addItem('Party','search.views.findParty')
    menu.addItem('People','search.views.findPeople')
    return menu.getMenu()