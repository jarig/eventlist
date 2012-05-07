from django.forms.models import ModelForm
from messaging.models import Message, gen_feed_hash

class SendMessageForm(ModelForm):

    class Meta:
        model = Message

    def saveMessage(self, author):
        self.cleaned_data["author"] = author.pk
        self.cleaned_data["status"] = Message.STATUS.SENT
        self.cleaned_data["feed"] = gen_feed_hash()
        msg = super(SendMessageForm, self).save()

        return msg

