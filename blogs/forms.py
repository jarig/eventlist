from django import forms



class NewBlogForm(forms.Form):
    name = forms.CharField(required=True,min_length=5)
    description = forms.CharField(widget=forms.Textarea)
    logo = forms.ImageField()