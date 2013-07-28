from django import forms
from django.utils.translation import gettext
from haystack.forms import SearchForm
from haystack.inputs import Raw
from common.models import Country
from event.models import EventGroup, Event, EventActivity


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
    activities = forms.ChoiceField(required=False)
    city = forms.ModelChoiceField(queryset=Country.objects.all(),
                                  empty_label=gettext("Any"),
                                  required=False,
                                  cache_choices=True)

    def __init__(self, *args, **kwargs):
        super(FastSearchForm, self).__init__(*args, **kwargs)
        self.fields['activities'].choices = self.activities_as_choices()

    def activities_as_choices(self):
        #TODO: cache for a long time
        activities = [["", gettext("Any")]]
        for activity in EventActivity.objects.filter(parent__isnull=True).select_related("subActivities"):
            subActivities = []
            for sub_activity in activity.subActivities.all():
                subActivities.append([sub_activity.name, sub_activity.name])

            new_category = [activity.name, subActivities]
            activities.append(new_category)

        return activities

    def search(self):
        sqs = self.searchqueryset.models(Event)
        #self.load_all = True

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['qText']:
            sqs = sqs.filter(text=Raw("%s~0.5" % self.cleaned_data['qText']))
        else:
            sqs = sqs.filter(actuality__gt=0).order_by("actuality")

        if self.cleaned_data['activities']:
            print self.cleaned_data['activities']
            sqs = sqs.filter(activities=self.cleaned_data['activities'])

        if self.cleaned_data['category']:
            sqs = sqs.filter(groups=str(self.cleaned_data['category']))

        #sqs = sqs.all()[offset:toShow]  # limit amount of results

        if self.load_all:
            sqs = sqs.load_all()

        return sqs