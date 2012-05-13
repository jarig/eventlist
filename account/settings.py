
# Social AUTH
from django.conf import settings

BACKENDS = {
    "VKONTAKTE":{
        "CLASS":"account.backends.vkontakte.Vkontakte",
        "NAME":"vk",
        "APP_ID": 633169,
        "API_KEY": "",
        "SECRET": "OFulETvm7McxCF8EEFnx",
    },
    "FACEBOOK":{
        "CLASS":"account.backends.facebook.Facebook",
        "NAME":"fb",
        "APP_ID": 122871594431190,
        "API_KEY": "122871594431190",
        "SECRET": "ad7ecef7ce5bbf85e40eceb22dbb8e90",
    }
}
SECRET_PASS ="+kw*8&m#oy&r", #default pass for user

# Settings
ACTIVATION_REQUIRED = False
REGISTRATION_ALLOWED = True

AVATAR_STUB = settings.STATIC_URL+"common/images/logoStub.png"