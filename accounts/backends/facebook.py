import json
import urllib
import urlparse
from django.http import HttpResponse
from accounts import settings
from django.contrib.auth.models import User
from accounts.models import Account

from hashlib import md5

class Facebook:

    def authenticate(self, identity=None, request=None):
        if identity == None or request == None: return None
        # check cookies
        if not self.validate(request): return None
        try:
            user = Account.objects.get(identity=identity, provider=settings.BACKENDS["FACEBOOK"]["NAME"]).user
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
            """
            cookieData = urlparse.parse_qs(request.COOKIES[cookieName])
            kSorted = sorted(cookieData.keys())
            value=""
            for key in kSorted:
                if key == "sig": continue
                value += "%s=%s" % (key, cookieData[key][0])
            print value
            print cookieData['sig'][0]
            print md5(value + settings.BACKENDS["FACEBOOK"]["SECRET"]).hexdigest()
            if cookieData['sig'][0] == md5(value + settings.BACKENDS["FACEBOOK"]["SECRET"]).hexdigest():
                self.identity = cookieData['uid'][0]
                return True
            else:
                raise ValueError()
            """
        except (KeyError, IndexError, AttributeError, ValueError):
            return False