from django import forms
from django.contrib.auth.models import User
from accounts.models import Account
from publisher.models import PublisherRequest

class RequestForm(forms.Form):
    requestMessage = forms.CharField(widget=forms.Textarea,
                                     required=True,
                                     min_length=10,
                                     label="Request")

    def save(self, request):
        cleanMessage = self.cleaned_data["requestMessage"]
        request = PublisherRequest(user=request.user, message=cleanMessage)
        request.save()
        pass
    