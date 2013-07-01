from django import forms
from django.forms.models import ModelForm
from account.models import Account
from messaging.models import Message, gen_feed_hash

class SendMessageForm(ModelForm):
    to = forms.ModelChoiceField(queryset=Account.objects.none(),empty_label="")

    def __init__(self, user, *args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)
        self.fields['to'].queryset = user.friends.all()

    class Meta:
        model = Message

    def saveMessage(self, author):
        msg = super(SendMessageForm, self).save(commit=False)
        msg.author = author
        msg.status = Message.STATUS.SENT
        msg.feed = gen_feed_hash()
        msg.save()
        return msg

