from django.core.files.storage import DefaultStorage
from django.forms.util import flatatt
from django.forms.widgets import HiddenInput
from django.utils import formats
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


class PreviewImageInput(HiddenInput):

    def _format_value(self, value):
        value = DefaultStorage().url(value)
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['src'] = force_unicode(self._format_value(value))
        return mark_safe(u'<img%s  /> %s' % (flatatt(final_attrs), super(PreviewImageInput,self).render(name,value, attrs)))

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        print "DATA: " + str(data)
        print "NAME : " + str(name)
        print "FILES: " + str(files)
        return data.get(name, None)
