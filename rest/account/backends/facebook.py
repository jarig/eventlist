import json
import urllib
import urlparse
from django.http import HttpResponse
from account import settings
from django.contrib.auth.models import User
from account.models import Account

from hashlib import md5

class Facebook:

    def authenticate(self, identity=None, request=None):
        if identity is None or request is None: return None
        # check cookies
        if not self.validate(request): return None
        try:
            user = Account.objects.get(identity=identity, provider=settings.BACKENDS["FACEBOOK"]["NAME"])
            return user
        except Account.DoesNotExist:
            raise User.DoesNotExist
    
    
    def validate(self, request):
        #cookieName = "fbsr_%s" % str(settings.BACKENDS["FACEBOOK"]["APP_ID"])
        #https://graph.facebook.com/me?access_token=
        try:
            accessToken = request.REQUEST["accessToken"]
            uid = request.REQUEST["uid"]
            resp = urllib.urlopen("https://graph.facebook.com/me?access_token=" + accessToken)
            data = json.loads(resp.read())
            print data["id"] == uid
            return data["id"] == uid
        except (KeyError, IndexError, AttributeError, ValueError):
            return False