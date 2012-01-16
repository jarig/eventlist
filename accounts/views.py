# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from accounts.forms import EditForm
from accounts.models import openRegister, updateUserData
from django.utils.translation import ugettext as _


@login_required
def edit(request):
    if request.method == "POST":
        editForm = EditForm(request.POST, request.FILES, instance=request.user)
        if editForm.is_valid():
            messages.success(request, _("Your personal information saved"))
            editForm.save(request)
    else:
        editForm = EditForm(instance=request.user)
    return render_to_response("accounts/accounts_edit.html",
                              {
                                'editForm': editForm
                            },
                              context_instance=RequestContext(request)
                            )

@login_required
def friendlist(request):
    friendships = request.user.friends.all().select_related("friend")
    return render_to_response("accounts/accounts_friendlist.html",
                              {
                                "friendships": friendships
                              },
                              context_instance=RequestContext(request)
    )

def messages(request):
    return render_to_response("accounts/accounts_friendlist.html",
                              {
                                 
                              },
                              context_instance=RequestContext(request)
    )

@login_required
def profile(request):
    
    return HttpResponse("Not implemented")

def extLoginProfile(request):
    userInfo = request.REQUEST
    try:
        try:
            user = authenticate(provider=userInfo["provider"], identity=userInfo["uid"],request=request)
            if user != None:
                login(request, user)
                updateUserData(user, userInfo["firstName"],userInfo["lastName"],userInfo["photo"])
                messages.success(request,_("You've successfully logged in!"))
                return HttpResponseRedirect(userInfo["next"])
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
            return HttpResponseRedirect(userInfo["next"])
    except (KeyError, ValueError): #smthing went wrong
        messages.error(request,_("Login failed!"))
        return HttpResponseRedirect(userInfo["next"])

def nativeLogin(request):
    return HttpResponseRedirect("/")
    #return HttpResponseRedirect(request.REQUEST["next"])

@login_required
def logoutProfile(request):
    logout(request)
    messages.success(request,_("Logged out"))
    
    return HttpResponseRedirect("/")
