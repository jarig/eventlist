from django.contrib.auth.decorators import login_required
#output ajax modules
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from blog_modules.settings import MODULES

@login_required
def getModuleList(request, style, position):
    modules = MODULES[unicode(style)][int(position)]
    return render_to_response("blog_module/list.html",
        {
            "modules": modules
        },
        context_instance=RequestContext(request)
    )
