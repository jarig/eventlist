# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

#choose in which blog to create event
from blogs.forms import NewBlogForm
from blogs.models import Blog, Types

@login_required
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
def create(request):
    if request.method == "POST":
        blogForm = NewBlogForm(request.POST)
        if blogForm.is_valid():
            return HttpResponse("Valid form")
    else:
        blogForm = NewBlogForm()
    blogTypes = Types.objects.all()
    return render_to_response("blogs/blogs_create.html",
                              {
                                "blogForm": blogForm,
                                "blogTypes": blogTypes
                              },
                              context_instance=RequestContext(request)
                              )


def show(request):
    return HttpResponse("TT")