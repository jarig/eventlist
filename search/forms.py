from django import forms

class SearchPeopleForm(forms.Form):
    search = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs= {
                                                                        'placeholder':'Search',
                                                                        'title': 'Search',
                                                                    }))
class FastSearchForm(forms.Form):
    search = forms.CharField(min_length=1, max_length=255, required=True, widget=forms.TextInput(attrs= {
                                                                                                'placeholder':'Search',
                                                                                                'title': 'Search',
                                                                                                })
    )
    pass