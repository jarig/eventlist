from django.db.models.fields.files import ImageField
from common import forms
from south.modelsinspector import add_introspection_rules


add_introspection_rules([], ["^common\.fields\.ImagePreviewField"])

class ImagePreviewField(ImageField):

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.ImagePreviewField}
        if 'initial' in kwargs:
            defaults['required'] = False
        defaults.update(kwargs)
        return super(ImagePreviewField, self).formfield(**defaults)
