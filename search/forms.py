from django import forms

class SearchPeopleForm(forms.Form):
    search = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs= {
                                                                        'placeholder':'Search',
                                                                        'title': 'Search',
                                                                    }))
