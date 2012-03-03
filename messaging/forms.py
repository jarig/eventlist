from django.forms.models import ModelForm
from messaging.models import Message

class SendMessageForm(ModelForm):

    class Meta:
        model = Message

