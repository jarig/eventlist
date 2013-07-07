from django import forms
from django.utils.translation import gettext
from haystack.forms import SearchForm
from event.models import EventGroup, Event


class SearchPeopleForm(forms.Form):
    search = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search',
        'title': 'Search',
    }))


class FastSearchForm(SearchForm):
    qText = forms.CharField(max_length=255, required=False,
                            widget=forms.TextInput(attrs={
                                'placeholder': 'Search',
                                'title': 'Search',
                            })
    )
    category = forms.ModelChoiceField(queryset=EventGroup.objects.all(),
                                      empty_label=gettext("Any"),
                                      required=False,
                                      cache_choices=True)

    def search(self):
        sqs = self.searchqueryset.models(Event)

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['qText']:
            sqs = sqs.filter(category=self.cleaned_data['qText'])

        if self.cleaned_data['category']:
            sqs = sqs.filter(groups=str(self.cleaned_data['category']))

        if self.load_all:
            sqs = sqs.load_all()

        return sqs