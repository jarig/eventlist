from django import forms
from django.forms.models import ModelForm
from blogs.models import Types, Blog


class NewBlogForm(ModelForm):
    """
    name = forms.CharField(required=True,min_length=5)
    description = forms.CharField(widget=forms.Textarea)
    blogTypes = Types.objects.all()
    types = forms.CharField(widget=forms.Select(choices=blogTypes))
    logo = forms.ImageField()
    """
    types = forms.ModelMultipleChoiceField(widget=forms.Select, queryset=Types.objects.all().order_by("name"))
    class Meta:
        model = Blog

        