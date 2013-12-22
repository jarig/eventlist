# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from messaging.forms import SendMessageForm
from messaging.models import Message


def messagingReceived(request):
    messages = Message.objects.raw("""SELECT MM.*,AU.* FROM messaging_message MM LEFT JOIN messaging_message MM2 ON
                                      MM.author_id=MM2.author_id AND MM.sent < MM2.sent,
                                      auth_user as AU
                                      WHERE MM2.id is NULL and MM.to_id=%s and AU.id=MM.author_id
                                   """
                                   , [request.user.pk])


    return render_to_response("messaging/messaging_received.html",
            {
                "my_messages": messages
            },
            context_instance=RequestContext(request)
    )

def sendMessageTo(request, user=None):
    #TODO check if message is sent to friends
    if request.POST:
        msgForm = SendMessageForm(request.user, request.POST)
        if msgForm.is_valid():
            msg = msgForm.saveMessage(request.user)
            return HttpResponse(json.dumps(msg.pk),'application/json')
        else:
            return HttpResponse(json.dumps(msgForm.errors),'application/json',status=403)
    else:
        msgForm = SendMessageForm(request.user, initial={'to':user})

    return render_to_response("messaging/includes/messaging_send.html",
            {
            "msgForm": msgForm,
            "friend": user,
        },
        context_instance=RequestContext(request)
    )

def deleteMessage(request, msgId):
    Message.objects.get(pk=msgId).delete()
    return HttpResponse("1")