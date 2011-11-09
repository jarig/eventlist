from django.forms.util import flatatt
from django.forms.widgets import HiddenInput
from django.utils import formats
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import settings

class HiddenImageInput(HiddenInput):
    def _format_value(self, value):
        value = settings.MEDIA_URL + '/' + str(value)
        if self.is_localized:
            return formats.localize_input(value)
        return value