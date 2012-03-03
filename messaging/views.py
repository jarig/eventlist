# Create your views here.
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from messaging.forms import SendMessageForm
from messaging.models import Message


def messagingReceived(request):
    messages = request.user.received_messages.all().order_by('-sent')[:20]
    return render_to_response("messaging/messaging_received.html",
            {
                "messages": messages
            },
            context_instance=RequestContext(request)
    )


def sendMessage(request):
    data = None
    if request.POST:
        msgForm = SendMessageForm(request.POST)
        if msgForm.is_valid():
            msgForm.save()
        json_serializer = json.Serializer()
        data = json_serializer.serialize(msgForm.errors, ensure_ascii=False, use_natural_keys=True)
    else:
        data = "{error: \"Wrong request\"}"
    return HttpResponse(data)

def deleteMessage(request, msgId):
    Message.objects.get(pk=msgId).delete()
    return HttpResponse("1")