from django import forms
from django.forms.models import ModelForm
from account.models import Account


class EditForm(ModelForm):

    class Meta:
        model = Account
    
    def save(self, commit=True):
        profile = self.save(commit)
        user = profile.user
        avatar = self.cleaned_data["avatar"]
        
        if avatar is not None:
            profile.avatar.save(
                'avatar_'+str(user.id),
                avatar,
                save=False
            )
            profile.save()
        return profile

class PublisherRequest(forms.Form):
    publisher = forms.BooleanField(required=False, label="I want to publish events")
    publisherRequestText = forms.CharField(widget=forms.Textarea, required=False, label="Request")