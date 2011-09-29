from django import forms
from django.db import transaction
from django.forms.models import ModelForm
from django.utils.translation import ugettext as _
from blogs.models import Types, Blog, BlogAccess


class NewBlogForm(ModelForm):
    types = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple,
                                           queryset=Types.objects.all().order_by("name"),
                                           error_messages={'list':_('At least 1 type required')})

    @transaction.commit_on_success
    def create_blog(self, request):#create new blog
        newBlog = self.save(commit=False)
        #add info

        newBlog.save()
        
        #access to blog
        bAccess = BlogAccess(blog=newBlog, user=request.user, access='OW')
        bAccess.save()

        self.save()
        
        return newBlog



    class Meta:
        model = Blog
        exclude = ('managers','rating','priority','type','logo')
        

        