# Create your views here.
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

#choose in which blog to create event
from django.utils.translation import ugettext as _
from blogs.forms import NewBlogForm
from blogs.models import Blog, Types, BlogStyle


def view(request, blogId):
    blog = Blog.objects.get(blogId)
    return render_to_response("blogs/"+blog.style+"/view.html",
                              {
                                "blog": blog
                              },
                                context_instance=RequestContext(request)
                              )

@login_required
#@permission_required("publisher.manage")
def manage(request):
    userBlogs = Blog.objects.filter(managers=request.user)
    return render_to_response("blogs/blogs_manage.html",
                              {
                                "blogs": userBlogs
                              },
                              context_instance=RequestContext(request)
                              )

@login_required
@permission_required("publisher.publish")
def create(request):#create or edit blog view
    blogStyle = BlogStyle.objects.filter(default=True)[:1]
    if not len(blogStyle):
        blogStyle = BlogStyle.objects.all()[:1]

    blogStyle = unicode(blogStyle[0])
    
    if request.method == "POST":
        blogForm = NewBlogForm(request.POST, request.FILES)
        if blogForm.is_valid():
            nBlog = blogForm.create_blog(request)
            messages.success(request, _("You've successfully created new blog!"))
            return HttpResponseRedirect(reverse("blogs.views.edit", kwargs={"blogId": nBlog.id}))
    else:
        blogForm = NewBlogForm(initial={'style':  blogStyle})
    
    return render_to_response("blogs/"+blogStyle+"/create.html",
                              {
                                "blogForm": blogForm,
                                "blogStyle": blogStyle
                              },
                              context_instance=RequestContext(request)
                              )
@login_required
@permission_required("publisher.publish")
def edit(request, blogId):
    blog = Blog.objects.get(pk=blogId)
    blogForm = NewBlogForm(instance=blog)
    
    if request.method == "POST":
        if blogForm.is_valid():
            #blogForm.create_blog(request) edit blog
            messages.success(request, _("Changes saved!"))

    return render_to_response("blogs/"+str(blog.style)+"/create.html",
                              {
                                "blogForm": blogForm,
                                "blogStyle": str(blog.style)
                              },
                              context_instance=RequestContext(request)
                              )


@login_required
@permission_required("publisher.publish")
def uploadTempImage(request):
    imageUrl=False
    if request.method == "POST":
        file = request.FILES["file"]
        print "Content type: " + file.content_type
        basename, extension = os.path.splitext(file.name)
        filename = "temp_"+request.user.first_name + extension
        dest = open(settings.MEDIA_ROOT+ filename,"wb+")
        for chunk in file.chunks():
            dest.write(chunk)
        dest.close()
        imageUrl = settings.MEDIA_URL +filename
    return render_to_response("blogs/blogs_uploadTempImage.html",
                              {
                                "imageUrl": imageUrl
                              },
                              context_instance=RequestContext(request)
                              )

def show(request):
    return HttpResponse("TT")