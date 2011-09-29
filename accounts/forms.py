from django import forms
from accounts.models import Account


class EditForm(forms.Form):
    first_name = forms.CharField(required=True,min_length=5, label="First Name")
    last_name = forms.CharField(required=True,min_length=5, label="Last Name")
    avatar = forms.ImageField(required=False)

    def save(self, request):
        profile = request.user.get_profile()
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        avatar = self.cleaned_data["avatar"]
        
        if avatar is not None:
            profile.avatar.save(
                'avatar_'+str(request.user.id),
                avatar,
                save=False
            )
            profile.save()

class PublisherRequest(forms.Form):
    publisher = forms.BooleanField(required=False, label="I want to publish events")
    publisherRequestText = forms.CharField(widget=forms.Textarea, required=False, label="Request")