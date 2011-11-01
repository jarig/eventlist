from django import forms
from django.db import transaction
from django.forms.models import ModelForm
from django.utils.translation import ugettext as _
from blogs.models import Blog, BlogAccess, FacilityType


class NewBlogForm(ModelForm):
    facilities = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple,
                                           queryset=FacilityType.objects.all().order_by("name"),
                                           error_messages={'list':_('At least 1 type required')})

    @transaction.commit_on_success
    def submit_blog(self, request):#create new blog
        bId = self.instance.pk
        
        newBlog = self.save(commit=False)
        #add info
        
        newBlog.save()

        #access to blog
        if bId is None: #new blog
            bAccess = BlogAccess(blog=newBlog, user=request.user, access=BlogAccess.OWNER)
            bAccess.save()

        self.save()
        return newBlog



    class Meta:
        model = Blog
        exclude = ('managers','rating','priority','type','logo')
        

        