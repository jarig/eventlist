# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.http import HttpResponse
from event.views import _go
from party.forms import CreateSimplePartyForm

@login_required
def silentCreate(request, eventScheduleId):

    if request.POST:
        createEventPartyForm = CreateSimplePartyForm(request.POST)
        json_serializer = json.Serializer()
        if createEventPartyForm.is_valid():
            #record to event go
            _go(request.user,eventScheduleId)
            party = createEventPartyForm.save()
            data= json.simplejson.dumps({ "id": party.pk }, ensure_ascii=False)
            return HttpResponse(data)
        else:
            data= json_serializer.serialize(createEventPartyForm.errors, ensure_ascii=False)
            return HttpResponse(data)
    return HttpResponse("Invalid request")
    pass
