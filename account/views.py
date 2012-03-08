# Create your views here.
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from account.forms import EditForm, RegisterForm
from account.models import openRegister, updateUserData
from django.utils.translation import ugettext as _
from common.utils import modelToDict


@login_required
def getFriends(request):
    #if not request.is_ajax(): return HttpResponse("Wrong request")
    friendships = request.user.friends.all().select_related("friend")
    friends = []
    for fShip in friendships:
        friends.append(modelToDict(fShip.friend,include=['first_name',
                                                 'last_name',
                                                 'avatar',
                                                 'age',
                                                 'sex']))
    data = json.simplejson.dumps(friends, ensure_ascii=False)
    return HttpResponse(data)

@login_required
def edit(request):
    if request.method == "POST":
        editForm = EditForm(request.POST, request.FILES, instance=request.user)
        if editForm.is_valid():
            messages.success(request, _("Your personal information saved"))
            editForm.save(request)
    else:
        editForm = EditForm(instance=request.user)
    return render_to_response("account/accounts_edit.html",
                              {
                                'editForm': editForm
                            },
                              context_instance=RequestContext(request)
                            )

@login_required
def friendlist(request):
    friendships = request.user.friends.all().select_related("friend")
    return render_to_response("account/accounts_friendlist.html",
                              {
                                "friendships": friendships
                              },
                              context_instance=RequestContext(request)
    )

@login_required
def profile(request):
    
    return HttpResponse("Not implemented")

def extLoginProfile(request):
    userInfo = request.REQUEST
    if userInfo.has_key('next'):
        next = userInfo["next"]
    else: next = reverse('common.views.index')
    try:
        try:
            user = authenticate(provider=userInfo["provider"], identity=userInfo["uid"],request=request)
            if user is not None:
                login(request, user)
                updateUserData(user, userInfo["firstName"],userInfo["lastName"],userInfo["photo"])
                messages.success(request,_("You've successfully logged in!"))
                return HttpResponseRedirect(next)
            else:
                # wrong credentials(wrong cookie)
                raise ValueError
        except User.DoesNotExist:
            #register user
            openRegister(provider=userInfo["provider"],identity=userInfo["uid"])
            user = authenticate(provider=userInfo["provider"], identity=userInfo["uid"],request=request)
            login(request, user)
            updateUserData(user, userInfo["firstName"],userInfo["lastName"],userInfo["photo"])
            messages.success(request,_("You've successfully logged in!"))
            return HttpResponseRedirect(next)
    except (KeyError, ValueError): #smthing went wrong
        messages.error(request,_("Login failed!"))
        return HttpResponseRedirect(next)

def nativeLogin(request):
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                if not request.is_ajax():
                    login(request, user)
                    return HttpResponseRedirect("/")
            else:
                return HttpResponse(_("Account not activated"), status=202)
                pass
        else:
            return HttpResponse(_("Wrong password or username"), status=405)
            pass
    #login succeddeed
    return HttpResponse("Success")

@login_required
def logoutProfile(request):
    logout(request)
    messages.success(request,_("Logged out"))
    
    return HttpResponseRedirect("/")


def register(request):
    if request.POST:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(_("Success"))
        data = json.simplejson.dumps(form.errors)
        print data
        return HttpResponse(data, status=405)
    return HttpResponse(_("Bad Request"), status=405)