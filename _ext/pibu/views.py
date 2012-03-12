import time
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.storage import DefaultStorage
from django.shortcuts import render_to_response
from django.template import RequestContext
from _ext.pibu.forms import TempImageForm

@login_required
def uploadTempImage(request):
    imagePath=False
    if request.method == "POST":
        tempImageForm = TempImageForm(request.POST, request.FILES)
        if tempImageForm.is_valid():
            #TODO check if content type is correct
            file = tempImageForm.cleaned_data['image']
            storage = DefaultStorage()
            filename = storage.get_valid_name("temp_"+str(request.user.id) + str(time.time()))
            #fp = storage.open('temp/'+filename)
            imagePath = storage.save('temp/'+filename, file)
            #fp.close()
    else:
        tempImageForm = TempImageForm()
    return render_to_response("common/uploadTempImage.html",
                              {
                                "tempImageForm": tempImageForm,
                                "imagePath": imagePath
                              },
                                context_instance=RequestContext(request)
                              )