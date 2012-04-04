from django.forms.util import flatatt
from django.forms.widgets import TextInput, HiddenInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class AutoCompleteWidget(HiddenInput):

    class Media:
            pass

    def render(self, name, value, attrs=None):
        model = self.attrs.get('model')
        del self.attrs['model']
        modelValue = None
        if value is None:
            value = ''
        if model is not None:
            try:
                modelValue = model.objects.select_related().get(pk=value)
            except Exception:
                modelValue = None

        if modelValue is None: modelValue = ""
        id = attrs.get('id', name)
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        return mark_safe(u'<input id="%s_text" name="%s_text" type="text" value="%s"><input%s />' %
                         (id, id, modelValue, flatatt(final_attrs)))

    pass
