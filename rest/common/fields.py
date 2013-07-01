from django.forms import fields
from south.modelsinspector import add_introspection_rules


class MultiValueFieldImpl(fields.MultiValueField):
    widget = fields.HiddenInput

    def __init__(self, *args, **kwargs):
        """
        Have to pass a list of field types to the constructor, else we
        won't get any data to our compress method.
        """
        all_fields = (
            fields.CharField(),
            )
        super(MultiValueFieldImpl, self).__init__(all_fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Takes the values from the MultiWidget and passes them as a
        list to this function. This function needs to compress the
        list into a single object to save.
        """
        print data_list
        if data_list:
            return None
        return None


add_introspection_rules([
    (
        [MultiValueFieldImpl], # Class(es) these apply to
        [],             # Positional arguments (not used)
            {           # Keyword argument
                        'model': ["model", {}],
                        },
        ),
], ["^common\.fields\.AutoCompleteCharField"])
