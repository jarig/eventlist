# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext

#choose in which blog to create event
from django.utils.translation import ugettext as _
from blog.forms import NewBlogForm
from blog.models import Blog, BlogAccess
from blog_modules.forms import ModuleParameterForm, ModuleParameterFormSet, ModuleParameterModelFormSet
from blog_modules.models import ModuleParameter
from common.forms import AddressForm
from common.models import Country, Address
from menu.models import Menu


@login_required
#@permission_required("publisher.manage")
def manage(request):
    userBlogs = Blog.objects.filter(managers=request.user)
    return render_to_response("blog/blogs_manage.html",
                              {
                                "myBlogs": userBlogs
                              },
                                context_instance=RequestContext(request)
                              )

def renderBlog(request, style='default', blog=None, page=None, mode=None, attr=None):
    #render blog page
    if attr is None: attr = {}
    if page is None or page == "": page = "general"
    if blog is not None:
        style = unicode(blog.style)
        attr['blogId'] = blog.pk

    attr["page"] = page
    attr["blog"] = blog
    attr["mode"] = mode
    attr["style"] = style
    attr["accessLevels"] = BlogAccess.accessLevelConstants
    return render_to_response("blog/%s/%s/%s.html" % (style, mode, page),
                              attr,
                              context_instance=RequestContext(request)
                              )


def view(request, blogId, page=None):
    try:
        blog = Blog.objects.get(pk=blogId)
    except Blog.DoesNotExist:
        raise Http404

    #generate menu
    menu = Menu(RequestContext(request))
    menu.addItem('General','blog.views.view', viewArgs=[blog.id,''])
    menu.addItem('Events','blog.views.view', viewArgs=[blog.id,'events'])

    return renderBlog(request, blog=blog, page=page, mode='view',
        attr={
                "menu": menu.getMenu()
            })

@login_required
@permission_required("publisher.publish")
def edit(request, blogId, page=None):
    try:
        blog = Blog.objects.get(pk=blogId)
        accessLevel = blog.blogaccess_set.get(user=request.user).access
        if not accessLevel >= BlogAccess.PUBLISHER:
            raise Blog.DoesNotExist(_("You don't have permission to edit this blog"))
    except Blog.DoesNotExist or BlogAccess.DoesNotExist:
        raise Http404

    AdrFormSet = modelformset_factory(Address, form=AddressForm, can_delete=True, extra=0)
    ModuleFormSet = modelformset_factory(ModuleParameter, form=ModuleParameterForm, formset=ModuleParameterModelFormSet, can_delete=True, extra=0)
    if request.method == "POST":
        blogForm = NewBlogForm(request.POST, request.FILES, instance=blog)
        adrFormSet = AdrFormSet(request.POST, queryset=blog.addresses.all())
        moduleFormSet = ModuleFormSet(request.POST, prefix="modules", queryset=blog.modules.all())
        if blogForm.is_valid() and adrFormSet.is_valid() and moduleFormSet.is_valid():
            blogForm.submit_blog(request,adrFormSet)
            moduleFormSet.saveModules(blog)
            messages.success(request, _("Changes successfully saved!"))
            return HttpResponseRedirect(reverse('blog.views.edit',kwargs={'blogId':blogId,'page':page}))
    else:
        moduleFormSet = ModuleFormSet(prefix="modules", queryset=blog.modules.all())
        blogForm = NewBlogForm(instance=blog)
        addr = blog.addresses.all().select_related('country','city')
        if len(addr):
            adrFormSet = AdrFormSet(queryset=addr)
        else:
            AdrFormSet.extra = 1
            adrFormSet = AdrFormSet(queryset=blog.addresses.none(),
                                    initial=[{'country': Country.objects.get(name='Estonia').pk}])#TODO select dynamically

    menu = Menu(RequestContext(request))
    if accessLevel > BlogAccess.PUBLISHER:
        menu.addItem('Settings','blog.views.edit', viewArgs=[blog.id,'settings'])
    menu.addItem('General','blog.views.edit', viewArgs=[blog.id,''])
    menu.addItem('Events','blog.views.edit', viewArgs=[blog.id,'events'])

    return renderBlog(request, blog=blog, page=page, mode='edit', attr={
            "adrFormSet": adrFormSet,
            "blogForm": blogForm,
            "menu": menu.getMenu(),
            "moduleFormSet": moduleFormSet,
            "accessLevel": accessLevel
            })

@login_required
@permission_required("publisher.publish")
def create(request):
    AdrFormSet = formset_factory(AddressForm, can_delete=True, can_order=True,extra=0)
    ModuleFormSet = formset_factory(ModuleParameterForm, formset=ModuleParameterFormSet, can_delete=True, extra=0)

    if request.method == "POST":
        blogForm = NewBlogForm(request.POST, request.FILES)
        adrFormSet = AdrFormSet(request.POST)
        moduleFormSet = ModuleFormSet(request.POST, prefix="modules")
        if blogForm.is_valid() and adrFormSet.is_valid() and moduleFormSet.is_valid():
            nBlog = blogForm.submit_blog(request, adrFormSet)
            messages.success(request, _("You've successfully created new blog!"))
            return HttpResponseRedirect(reverse("blog.views.edit", kwargs={"blogId": nBlog.id, "page":""}))
    else:
        blogForm = NewBlogForm(initial={'style':  'default'})
        adrFormSet = AdrFormSet(initial=[{'country': Country.objects.get(name='Estonia').pk}])
        moduleFormSet = ModuleFormSet(prefix="modules")

    menu = Menu(RequestContext(request))
    menu.addItem('General','blog.views.create')

    return renderBlog(request,
                      mode="create",
                      style='default',
                      attr={
                        "blogForm": blogForm,
                        "adrFormSet": adrFormSet,
                        "menu": menu.getMenu(),
                        "moduleFormSet": moduleFormSet,
                        "accessLevel": BlogAccess.OWNER
                           })


@login_required
@permission_required("publisher.publish")
def getBlogAddress(request):
    blogId = request.REQUEST["blogId"]
    blog = Blog.objects.get(pk=blogId)
    addresses = blog.addresses.select_related('country').all()
    json_serializer = json.Serializer()
    data= json_serializer.serialize(addresses, ensure_ascii=False, use_natural_keys=True)
    return HttpResponse(data)
    pass