import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from blogs.models import Blog
from event.forms import NewEventForm


@login_required
@permission_required('publisher.publish')
def create(request, blogId=None):

    blog = None
    if blogId is not None:
        blog = Blog.objects.get(pk=blogId)

    if request.method == "POST":
        eventForm = NewEventForm(request.POST, request.FILES)
        if eventForm.is_valid():
            eventForm.save()
            #redirect to show event
    else:
        eventForm = NewEventForm(initial={'blogId':0,
                                          'dateFrom':datetime.datetime.today()})
    
    return render_to_response("events/events_event.html",
                                  {
                                    "blog": blog,
                                    "eventForm": eventForm,
                                  },
                                  context_instance=RequestContext(request)
                                  )


def main(request):
    return render_to_response("events/events_main.html",
                              {
                              },
                              context_instance=RequestContext(request)
                              )

