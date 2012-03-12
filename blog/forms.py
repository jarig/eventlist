from django import forms
from django.db import transaction
from django.forms.models import ModelForm
from django.utils.translation import ugettext as _
from blog.models import Blog, BlogAccess, FacilityType


class NewBlogForm(ModelForm):
    facilities = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'placeholder':"Select facility"}),
                                           queryset=FacilityType.objects.all().order_by("name"),
                                           error_messages={'list':_('At least 1 type required')},
                                           required=False)

    @transaction.commit_on_success
    def submit_blog(self, request, adrFormSet):#create new blog
        bId = self.instance.pk


        newBlog = self.save()
        #add info
        for adrForm in adrFormSet:
            adrForm.fields["name"].data = self.cleaned_data["name"]
            newBlog.addresses.add(adrForm.save())
        newBlog.save()

        #access to blog
        if bId is None: #new blog
            bAccess = BlogAccess(blog=newBlog, user=request.user, access=BlogAccess.OWNER)
            bAccess.save()

        return newBlog


    class Meta:
        model = Blog
        exclude = ('managers','rating','priority','type')
        

        