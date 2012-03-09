from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.utils.translation import ugettext as _
from account.models import Account


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, error_messages={
        "required": _("Email field is required"),
        "invalid": _("Email field is invalid")
    })

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.identity = self.cleaned_data["username"]
        user.provider = "nt"
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = ("username","email")


class EditForm(ModelForm):

    class Meta:
        model = Account
        fields = ("first_name","last_name","email","avatar","sex","age")

    """
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
    """
class PublisherRequest(forms.Form):
    publisher = forms.BooleanField(required=False, label="I want to publish events")
    publisherRequestText = forms.CharField(widget=forms.Textarea, required=False, label="Request")