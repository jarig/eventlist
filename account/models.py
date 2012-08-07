import os
import urllib2
from django.core.files.base import File
from django.core.files.storage import DefaultStorage
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.contrib.auth.models import User
from _ext.pibu.fields import ImagePreviewModelField
from account import settings
from _ext.pibu import settings as pibu_settings

#User._meta.get_field('username')._unique = False
# Create your models here.

def account_logo_name(instance, filename):
    return "avatar/%d_avatar" % (int(instance.pk))

def _account_logo_name(pk):
    storage = DefaultStorage()
    avatar = "avatar/%d_avatar.jpeg" % int(pk)
    if storage.exists(avatar):
        return storage.url(avatar)
    return None

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
    avatar = ImagePreviewModelField(upload_to=account_logo_name, max_width=164, blank=True, null=True, max_length=255, default='')
    sex = models.CharField(max_length=1, choices=_SEX, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    friends = models.ManyToManyField('Account', through='FriendShip')

    class Meta:
        unique_together = ("identity", "provider")

    def __unicode__(self):
        return u"%s %s" % ( unicode(self.first_name), unicode(self.last_name) )

class FriendShip(models.Model):
    class STATUS:
        SUBSCRIBED_REFUSED = 0
        SUBSCRIBED = 1
        FRIENDSHIP = 2

    _STATUS = (
        (STATUS.SUBSCRIBED_REFUSED, u'refused in friendship'),
        (STATUS.SUBSCRIBED, u'subscribed'),
        (STATUS.FRIENDSHIP, u'friendship'),
    )
    creator = models.ForeignKey(Account, related_name='+') #those who added I
    friend = models.ForeignKey(Account, related_name='subscribers') #those who added me
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.PositiveSmallIntegerField(choices=_STATUS,default=STATUS.SUBSCRIBED, blank=True, editable=False)
    
    class Meta:
        unique_together = ("creator", "friend")

def openRegister(identity, provider, avatarURL=None, firstName=None, lastName=None):
    if not settings.REGISTRATION_ALLOWED: return None
    username = provider+str(identity)
    #TODO generate random pass
    user = Account.objects.create(identity=identity,provider=provider,username=username, email="")
    if settings.ACTIVATION_REQUIRED:
        user.is_active = 0
    user.set_password(settings.SECRET_PASS)

    updateUserData(user, firstName, lastName, avatarURL)
    return user

def updateUserData(user, firstName, lastName, avatarURL = None, gender=None):
    if firstName: user.first_name = firstName
    if lastName: user.last_name = lastName
    user.save()
    if avatarURL is not None:
        img_temp = NamedTemporaryFile()
        img_temp.write(urllib2.urlopen(avatarURL).read())
        img_temp.flush()
        storage = DefaultStorage()
        name = storage.save(os.path.join(pibu_settings.MEDIA_TEMP_URL, account_logo_name(user,"avatar")), File(img_temp))
        user.avatar.save(
            name,
            storage.open(name)
        )
