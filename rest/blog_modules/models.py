import hashlib
from django import template
from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.template.base import resolve_variable
from django.template.context import RequestContext
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


    def content(self, context):
        pass

    def render(self, request):
        context = RequestContext(request)
        context["user"] = resolve_variable('user', context)
        context["position"] = request.GET.get("position","")
        return HttpResponse(self.content(context))

    def __unicode__(self):
        return unicode(self.name)

class Dummy(Module):
    name = "Dummy"
    descr = "Dummy"
    type = Module.TYPE.FREE
    hash = hashlib.md5("Dummy").hexdigest()

    def content(self, context):
        t = template.loader.get_template('modules/dummy/index.html')
        return t.render(context)

class ImageSlider(Module):
    name = "Image Slider"
    #logo = ""
    descr = "Shows slide images"#TODO use lazy ugettext
    type = Module.TYPE.FREE
    hash = hashlib.md5("ImageSlider").hexdigest()

    def content(self,context):
        t = template.loader.get_template('modules/image_slider/index.html')
        return t.render(context)

#store params per blog
class ModuleParameter(models.Model):
    #module parameters
    blog = models.ForeignKey(Blog, related_name='modules', editable=False)
    style = models.ForeignKey(BlogStyle, related_name='modules', editable=False)
    module = models.CharField(max_length=32) #path to module (module hash)
    position = models.PositiveSmallIntegerField(db_index=True)
    parameters = models.TextField(blank=True)

    class Meta:
        unique_together = ('blog','module','style',)

