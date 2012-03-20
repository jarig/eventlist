from exceptions import Exception
import os
from django.core.exceptions import ValidationError
from django.core.files.storage import DefaultStorage
from django.db.models.fields.files import ImageFieldFile
from django.forms import ImageField
from django.utils.translation import ugettext_lazy as _
from south.modelsinspector import add_introspection_rules
from django.db import models
from _ext.pibu.widgets import PreviewImageInput
from common import utils
import settings

from PIL import Image
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO



class ImagePreviewFieldFile(ImageFieldFile):
    def _get_url(self):
        if not self:
            return self.field.stub_file
        return self.storage.url(self.name)
    url = property(_get_url)

    def save(self, name, content, save=True):
        name = self.field.generate_filename(self.instance, content.name) + "."+self.field.format
        srcPath = self.storage.path(name)
        oldPath = content.name
        fp = content

        setattr(self.instance, self.field.name, name)
        self.name = name
        if oldPath.lower().find(settings.MEDIA_TEMP_URL.lower()): return #if not found or not in beginning
        if unicode(srcPath).lower() == unicode(oldPath).lower(): return


        newResizedImage = self.storage.open(self.name, mode='wb')
        #TODO optimization save image in memory if small
        #resizedImageContent = StringIO()
        img = Image.open(content.file)
        img.thumbnail((
            self.field.max_width,
            self.field.max_height
            ), Image.ANTIALIAS)
        img.save(newResizedImage, format=self.field.format)
        fp.close()
        self.storage.delete(oldPath) #delete temp. file

        # Update the filesize cache
        self._size = newResizedImage.size
        self._committed = True

        # Save the object because it has changed, unless save is False
        if save:
            self.instance.save()


class ImagePreviewModelField(models.ImageField):
    attr_class = ImagePreviewFieldFile
    def __init__(self, max_height=settings.IMAGE_MAX_HEIGHT,
                       max_width=settings.IMAGE_MAX_WIDTH,
                       max_size=settings.IMAGE_MAX_SIZE,
                       format='JPEG',
                       stub_file=settings.IMAGE_STUB_FILE, *args, **kwargs):
        self.max_height, self.max_width, self.max_size, self.format = max_height, max_width, max_size*1024, format
        self.stub_file = stub_file
        super(ImagePreviewModelField,self).__init__(*args, **kwargs)
        self.validators.append(self._checkImageConstraints)

    def _checkImageConstraints(self, value):
        size = os.path.getsize(value.path) #in bytes
        if self.max_size <= size:
            raise ValidationError(_("Uploaded image exceeds maximum size - %s" % utils.prettySize(self.max_size)))
        pass

    def formfield(self, **kwargs):
        defaults = {'form_class': ImagePreviewField}
        if 'initial' in kwargs:
            defaults['required'] = False
        defaults.update(kwargs)
        return super(ImagePreviewModelField, self).formfield(**defaults)


# image field with preview before submit functionality
class ImagePreviewField(ImageField):
    widget = PreviewImageInput # Default widget to use when rendering this type of Field.
    errors = {
        "unreachable": _("Image file is unreachable"),
    }

    def to_python(self, data):
        try:
            storage = DefaultStorage()
            fp = storage.open(data)
            return super(ImagePreviewField, self).to_python(fp)
        except Exception:
            raise ValidationError(self.error_messages['invalid_image'])


    def clean(self, data, initial=None):
        if not data.find(settings.MEDIA_URL):
            data = data.replace(settings.MEDIA_URL, "", 1)
        else: #media url not found
            raise ValidationError(self.errors['unreachable'])
        return super(ImagePreviewField, self).clean(data, initial)

    def bound_data(self, data, initial):
        return super(ImagePreviewField, self).bound_data(data, initial)


add_introspection_rules([
    (
        [ImagePreviewModelField], # Class(es) these apply to
        [],             # Positional arguments (not used)
            {           # Keyword argument
                        "max_height": ["max_height", {"default": settings.IMAGE_MAX_HEIGHT}],
                        "max_width": ["max_width", {"default": settings.IMAGE_MAX_WIDTH}],
                        "max_size": ["max_size", {"default": settings.IMAGE_MAX_SIZE}],
                        "format": ["format", {"default": 'JPEG'}],
                        "stub_file": ["stub_file", {"default": settings.IMAGE_STUB_FILE}],
                        },
        ),
], ["^_ext\.pibu\.fields\.ImagePreviewModelField"])