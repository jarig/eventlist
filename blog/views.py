# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext

#choose in which blog to create event
from django.utils.translation import ugettext as _
from blog.forms import NewBlogForm
from blog.models import Blog, BlogStyle, BlogAccess, BlogModule
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

def renderBlog(request, style='default',blog=None, page=None, mode=None, attr=None):
    #render blog page
    if attr is None: attr = {}
    attr["mode"] = mode
    attr['accessLevel'] = 0
    if blog is not None:
        style = unicode(blog.style)
        attr['accessLevel'] = blog.blogaccess_set.get(user=request.user).access
        attr['blogId'] = blog.id
    elif mode == 'create':
        attr['accessLevel'] = BlogAccess.OWNER

    attr["page"] = page
    if page is None or page == '':
        page = 'general'
        attr["page"] = ''

    attr["accessLevels"] = BlogAccess.accessLevelConstants

    #generate menu
    menu = Menu(RequestContext(request))
    if mode != 'create': #view or edit
        if mode == 'edit' and attr['accessLevel'] >= BlogAccess.ADMIN:
            menu.addItem('Settings','blog.views.'+mode, viewArgs=[blog.id,'settings'])
        menu.addItem('General','blog.views.'+mode, viewArgs=[blog.id,''])
        menu.addItem('Events','blog.views.'+mode, viewArgs=[blog.id,'events'])
    else:#create
        menu.addItem('General','blog.views.create')
        
    attr["menu"] = menu.getMenu()
    return render_to_response("blog/"+style+"/"+page+".html",
                              attr,
                              context_instance=RequestContext(request)
                              )


def view(request, blogId, page=None):
    try:
        blog = Blog.objects.get(pk=blogId)
    except Blog.DoesNotExist:
        raise Http404
    
    return renderBlog(request, blog=blog, mode='view', page=page, attr={"blog":blog})

@login_required
@permission_required("publisher.publish")
def edit(request, blogId, page=None):
    try:
        blog = Blog.objects.get(pk=blogId)
        if not BlogAccess.objects.filter(Q(blog=blog) & Q(user=request.user) &
                                         (Q(access__gte=BlogAccess.PUBLISHER))).exists():
            raise Blog.DoesNotExist(_("You don't have permission to edit this blog"))
    except Blog.DoesNotExist:
        raise Http404

    AdrFormSet = modelformset_factory(Address, form=AddressForm, can_delete=True, extra=0)
    if request.method == "POST":
        blogForm = NewBlogForm(request.POST, request.FILES, instance=blog)
        adrFormSet = AdrFormSet(request.POST, queryset=blog.addresses.all())
        if blogForm.is_valid() and adrFormSet.is_valid():
            blogForm.submit_blog(request,adrFormSet)
            messages.success(request, _("Changes successfully saved!"))
            return HttpResponseRedirect(reverse('blog.views.edit',kwargs={'blogId':blogId,'page':page}))
    else:
        blogForm = NewBlogForm(instance=blog)
        addr = blog.addresses.all()
        if len(addr):
            adrFormSet = AdrFormSet(queryset=addr)
        else:
            AdrFormSet.extra = 1
            adrFormSet = AdrFormSet(queryset=blog.addresses.none(),
                                    initial=[{'country': Country.objects.get(name='Estonia').pk}])
    
    return renderBlog(request,
                      blog=blog,
                      page=page,
                      mode="edit",
                      attr={
                            "blogForm": blogForm,
                            "adrFormSet": adrFormSet
                           })

@login_required
@permission_required("publisher.publish")
def create(request):
    blogStyle = ''
    AdrFormSet = formset_factory(AddressForm, can_delete=True, can_order=True,extra=0)
    if request.method == "POST":
        blogForm = NewBlogForm(request.POST, request.FILES)
        adrFormSet = AdrFormSet(request.POST)
        if blogForm.is_valid() and adrFormSet.is_valid():
            nBlog = blogForm.submit_blog(request, adrFormSet)
            messages.success(request, _("You've successfully created new blog!"))
            return HttpResponseRedirect(reverse("blog.views.edit", kwargs={"blogId": nBlog.id, "page":""}))
    else:
        defStyle = BlogStyle.objects.filter(default=True)
        if len(defStyle): blogStyle = defStyle[0]
        blogForm = NewBlogForm(initial={'style':  blogStyle})
        adrFormSet = AdrFormSet(initial=[{'country': Country.objects.get(name='Estonia').pk}])
    
    return renderBlog(request,
                      mode="create",
                      attr={
                        "blogForm": blogForm,
                        "adrFormSet": adrFormSet
                           })


@login_required
@permission_required("publisher.publish")
def getAvailableModules(request):
    modules = BlogModule.objects.all()
    json_serializer = json.Serializer()
    data= json_serializer.serialize(modules, ensure_ascii=False, use_natural_keys=True)
    return HttpResponse(data)

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