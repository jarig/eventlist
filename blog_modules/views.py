from django.contrib.auth.decorators import login_required, permission_required
#output ajax modules
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template.context import RequestContext, Context
from blog_modules.settings import MODULES, INSTALLED_MODULES

@login_required
@permission_required("publisher.publish")
def getModuleList(request, style, position):
    modules = MODULES[unicode(style)][int(position)]
    return render_to_response("blog_module/list.html",
        {
            "modules": modules
        },
        context_instance=RequestContext(request)
    )


def renderModule(request, moduleHash=None):
    if moduleHash is None:
        moduleHash = request.GET.get("moduleHash",0)
    if INSTALLED_MODULES.has_key(moduleHash):
        module = INSTALLED_MODULES[moduleHash]
        return module.render(RequestContext(request))
    else:
        return HttpResponseNotFound("Such module doesn't exist")