# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.http import HttpResponse
from party.forms import CreateSimplePartyForm

@login_required
def silentCreate(request):

    if request.POST and request.is_ajax():
        createPartyFormSample = CreateSimplePartyForm(request.POST)
        json_serializer = json.Serializer()
        if createPartyFormSample.is_valid():
            party = createPartyFormSample.save()
            data= json.simplejson.dumps({ "id": party.pk }, ensure_ascii=False)
            return HttpResponse(data)
        else:
            data= json_serializer.serialize(createPartyFormSample.errors, ensure_ascii=False)
            return HttpResponse(data)
    return HttpResponse("Invalid request")
    pass
