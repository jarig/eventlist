# Create your views here.
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from account.forms import EditForm, RegisterForm
from account.models import openRegister, updateUserData, FriendShip, Account
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
            editForm.save()
            return HttpResponseRedirect(reverse('account.views.edit'))
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
                updateUserData(user, userInfo["firstName"],userInfo["lastName"]) #update basic info
                messages.success(request,_("You've successfully logged in!"))
                return HttpResponseRedirect(next)
            else:
                # wrong credentials(wrong cookie)
                raise ValueError
        except User.DoesNotExist:
            #register user
            openRegister(provider=userInfo["provider"],
                                identity=userInfo["uid"],
                                avatarURL=userInfo["photo"],
                                firstName=userInfo["firstName"],
                                lastName=userInfo["lastName"])
            user = authenticate(provider=userInfo["provider"], identity=userInfo["uid"],request=request)
            login(request, user)
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
    try:
        if request.POST:
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse(_("Success"))
            data = json.simplejson.dumps(form.errors.values())
            #print data
            return HttpResponse(data, status=405)
    except Exception as e:
        print e
        raise e
    return HttpResponse(_("Bad Request"), status=405)


@login_required
def addFriend(request, user):
    try:
        fr = FriendShip.objects.get(creator=Account(pk=user), friend=request.user) #if friend already added me
        fr.status = FriendShip.STATUS.FRIENDSHIP
        fr.save()
    except FriendShip.DoesNotExist: #friend didn't add me before
        fs, created = FriendShip.objects.get_or_create(creator=request.user, friend=Account(pk=user))
        if not created:
            if fs.status == FriendShip.STATUS.SUBSCRIBED_REFUSED:
                fs.status = FriendShip.STATUS.SUBSCRIBED
            fs.save()
    next = request.REQUEST.get("next",reverse("account.views.friendlist"))
    return HttpResponseRedirect(next)

@login_required
def removeFriend(request, friend):
    fShips = FriendShip.objects.filter(Q(creator=request.user, friend=Account(pk=friend))
                               | Q(creator=Account(pk=friend), friend=request.user)).all()
    for fShip in fShips:
        if fShip.status == FriendShip.STATUS.SUBSCRIBED_REFUSED: continue
        if fShip.creator == request.user:
            fShip.delete()
            continue
        #creator == friend
        if fShip.status == FriendShip.STATUS.SUBSCRIBED:
            fShip.status = FriendShip.STATUS.SUBSCRIBED_REFUSED
        elif fShip.status == FriendShip.STATUS.FRIENDSHIP:
            fShip.status = FriendShip.STATUS.SUBSCRIBED
        fShip.save()

    pass