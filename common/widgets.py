from django.core.files.storage import DefaultStorage
from django.forms.widgets import HiddenInput
from django.utils import formats


class HiddenImageInput(HiddenInput):
    def _format_value(self, value):
        value = DefaultStorage().url(value)
        if self.is_localized:
            return formats.localize_input(value)
        return value