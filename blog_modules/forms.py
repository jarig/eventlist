from django.forms.formsets import BaseFormSet
from django.forms.models import ModelForm, BaseModelFormSet
from django.forms.util import ErrorList
from blog_modules.models import ModuleParameter


class ModuleParameterForm(ModelForm):
    class Meta:
        model = ModuleParameter

    def saveModule(self, blog):
        if self.cleaned_data["DELETE"]:
            #delete module
            self.instance.delete()
            return None
        module = self.save(commit=False)
        module.blog = blog
        module.style = blog.style
        module.save()
        return module

class ModuleParameterModelFormSet(BaseModelFormSet):

    def __init__(self,  *args, **kwargs):
        super(ModuleParameterModelFormSet, self).__init__(*args, **kwargs)
        self.moduleMap = {}
        for form in self.forms:
            if form.instance.module:
                self.moduleMap[form.instance.position] = form.instance.module

    def saveModules(self, blog):
        for form in self.forms:
            form.saveModule(blog)

    def clean(self):
        super(ModuleParameterModelFormSet, self).clean()
        if self.is_bound:
            for form in self.forms:
                if form.is_valid():
                    if form.cleaned_data.has_key("module") and not form.cleaned_data.get('DELETE', False):
                        self.moduleMap[form.cleaned_data["position"]] = form.cleaned_data["module"]

class ModuleParameterFormSet(BaseFormSet):
    #TODO form hash map: style+position=module_hash
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList):
        super(ModuleParameterFormSet, self).__init__(data, files, auto_id, prefix,
            initial, error_class)
        self.moduleMap = {}

    def clean(self):
        super(ModuleParameterFormSet, self).clean()
        if self.is_bound:
            for form in self.forms:
                    if form.is_valid():
                        if form.cleaned_data.has_key("module") and not form.cleaned_data.get('DELETE', False):
                                self.moduleMap[form.cleaned_data["position"]] = form.cleaned_data["module"]