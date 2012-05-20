from django.forms.formsets import BaseFormSet
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from blog_modules.models import ModuleParameter


class ModuleParameterForm(ModelForm):
    class Meta:
        model = ModuleParameter


class ModuleParameterFormSet(BaseFormSet):
    #TODO form hash map: md5(style*position)=module_hash
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList):
        super(ModuleParameterFormSet, self).__init__(data, files, auto_id, prefix,
            initial, error_class)
        self.moduleMap = {}

    def _construct_form(self, i, **kwargs):
        form = super(ModuleParameterFormSet, self)._construct_form(i, **kwargs)
        if self.is_bound:
            if form.is_valid():
                self.moduleMap[form.cleaned_data["style"]+form.cleaned_data["position"]] = form.cleaned_data["module"]
        return form