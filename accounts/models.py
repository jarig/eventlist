from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from accounts import settings
from django.conf import settings as globalSettings

User._meta.get_field('username')._unique = False
# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User)

    identity = models.CharField(max_length=128, default="")
    provider = models.CharField(max_length=128, default="")
    avatar = models.CharField(max_length=255)
    customAvatar = models.ImageField(upload_to=globalSettings.MEDIA_ROOT, blank=True, max_length=255)
    rating = models.FloatField(default=0)



def openRegister(identity, provider):
    if not settings.REGISTRATION_ALLOWED: return None
    username = provider+str(identity)
    user = User.objects.create_user(username=username, email="",password=settings.SECRET_PASS)
    if settings.ACTIVATION_REQUIRED:
        user.is_active = 0
    user.save()
    Account.objects.create(user=user,identity=identity,provider=provider)
    return user

def updateUserData(user, firstName, lastName, avatarURL):
    user.first_name = firstName
    user.last_name = lastName
    profile = user.get_profile()
    profile.avatar = avatarURL
    profile.save()
    user.save()

""" Not required
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
"""