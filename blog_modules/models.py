from django.conf import settings
from django.db import models
from blog.models import Blog, BlogStyle

class Module(object):
    #abstract class for creating modules
    class TYPE:
        FREE = 0
        PREMIUM = 1

    name = ""
    logo = "%s%s" % (settings.STATIC_URL, "blog_module/dummy/logo.png")
    descr = ""
    type = ""
    hash = None #generated hash = __class__.name*secret

    @staticmethod
    def render():
        #render for editing/creation/view of module
        pass

    def path(self):
        #TODO change to hash
        return self.__class__.__name__

    def __unicode__(self):
        return unicode(self.name)


class ImageSlider(Module):
    name = "Image Slider"
    #logo = ""
    descr = "Shows slide images"
    type = Module.TYPE.FREE

    @staticmethod
    def render():
        pass


def generate_module_hashes():
    #generate hashes and form hash map for instant access
    pass

#store params per blog
class ModuleParameter(models.Model):
    #module parameters
    blog = models.ForeignKey(Blog, related_name='modules', editable=False)
    style = models.ForeignKey(BlogStyle, related_name='modules', editable=False)
    module = models.CharField(max_length=16) #path to module (modules hash)
    position = models.PositiveSmallIntegerField(db_index=True)
    parameters = models.TextField()

    class Meta:
        unique_together = ('blog','module','style',)

