import urllib
import urllib2
from django.core.files.base import File
from django.core.files.storage import DefaultStorage
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from account import settings
from django.conf import settings as globalSettings

#User._meta.get_field('username')._unique = False
# Create your models here.

class Account(User):
    class SEX:
        MALE = "M"
        FEMALE = "F"
    _SEX = (
        (SEX.MALE,u'male'),
        (SEX.FEMALE,u'female')
    )
    user = models.OneToOneField(User,editable=False, related_name='profile')
    identity = models.CharField(max_length=128, default="",editable=False)
    provider = models.CharField(max_length=128, default="",editable=False)
    rating = models.FloatField(default=0,editable=False)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True, max_length=255, default='')
    sex = models.CharField(max_length=1, choices=_SEX, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("identity", "provider")

    def __unicode__(self):
        print self.username

class FriendShip(models.Model):
    creator = models.ForeignKey(Account, related_name='friends') #those who added I
    friend = models.ForeignKey(Account, related_name='subscribers') #those who added me
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        unique_together = ("creator", "friend")

def openRegister(identity, provider):
    if not settings.REGISTRATION_ALLOWED: return None
    username = provider+str(identity)
    user = User.objects.create_user(username=username, email="",password=settings.SECRET_PASS)
    if settings.ACTIVATION_REQUIRED:
        user.is_active = 0
    user.save()
    Account.objects.create(user=user,identity=identity,provider=provider)
    return user

def updateUserData(user, firstName, lastName, avatarURL, gender=None):
    user.first_name = firstName
    user.last_name = lastName
    profile = user.get_profile()
    profile.sex = gender
    profile.save()
    user.save()

    img_temp = NamedTemporaryFile()
    img_temp.write(urllib2.urlopen(avatarURL).read())
    img_temp.flush()
    storage = DefaultStorage()
    profile.avatar.save(
        "avatar_"+str(user.pk),
        File(img_temp)
    )
