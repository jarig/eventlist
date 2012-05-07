# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from account.models import Account
from messaging.forms import SendMessageForm
from messaging.models import Message


def messagingReceived(request):
    messages = request.user.received_messages.filter(status__lt=Message.STATUS.SENT).select_related("author").order_by('-sent')[:20]
    return render_to_response("messaging/messaging_received.html",
            {
                "messages": messages
            },
            context_instance=RequestContext(request)
    )

def sendMessageTo(request, user=None):
    if request.POST:
        msgForm = SendMessageForm(request.POST)
        if msgForm.is_valid():
            msg = msgForm.saveMessage(request.user)
            return HttpResponse(simplejson.dumps(msg.pk),'application/json')
        else:
            return HttpResponse(simplejson.dumps(msgForm.errors),'application/json',status=403)
    else:
        msgForm = SendMessageForm(initial={'to':user})

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