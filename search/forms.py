from django import forms
from django.utils.translation import gettext
from event.models import EventGroup


class SearchPeopleForm(forms.Form):
    search = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs= {
                                                                        'placeholder':'Search',
                                                                        'title': 'Search',
                                                                    }))


class FastSearchForm(forms.Form):
    search = forms.CharField(max_length=255, widget=forms.TextInput(attrs= {
                                                                            'placeholder':'Search',
                                                                            'title': 'Search',
                                                                            })
    )
    category = forms.ModelChoiceField(queryset=EventGroup.objects.all(),
                                      empty_label=gettext("Any"),
                                      cache_choices=True)
    pass