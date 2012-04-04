from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from south.modelsinspector import add_introspection_rules
from _ext.autocomplete.widgets import AutoCompleteWidget


class AutoCompleteCharField(CharField):
    widget = AutoCompleteWidget

    def __init__(self, model, max_length=None, min_length=None, *args, **kwargs):
        self.model = model
        super(AutoCompleteCharField, self).__init__(max_length, min_length, *args, **kwargs)

    def to_python(self, value):
        return self.model(pk=value)

    def widget_attrs(self, widget):
        attrs = super(AutoCompleteCharField, self).widget_attrs(widget) or {}
        attrs["model"] = self.model
        return attrs

    pass


add_introspection_rules([
    (
        [AutoCompleteCharField], # Class(es) these apply to
        [],             # Positional arguments (not used)
            {           # Keyword argument
                'model': ["model", {}],
            },
        ),
], ["^_ext\.autocomplete\.fields\.AutoCompleteCharField"])