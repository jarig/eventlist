from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm


class EditForm(ModelForm):

    class Meta:
        model = User
    
    def save(self, commit=True):
        user = self.save(commit)
        profile = user.get_profile()
        #first_name = self.cleaned_data["first_name"]
        #last_name = self.cleaned_data["last_name"]
        avatar = self.cleaned_data["avatar"]
        
        if avatar is not None:
            profile.avatar.save(
                'avatar_'+str(user.id),
                avatar,
                save=False
            )
            profile.save()

class PublisherRequest(forms.Form):
    publisher = forms.BooleanField(required=False, label="I want to publish events")
    publisherRequestText = forms.CharField(widget=forms.Textarea, required=False, label="Request")