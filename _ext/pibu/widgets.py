from django.core.files.storage import DefaultStorage
from django.core.urlresolvers import reverse
from django.forms.util import flatatt
from django.forms.widgets import HiddenInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from _ext.pibu import settings

class PreviewImageInput(HiddenInput):
    class Media:
            js = ('img_preview_widget/ImageUploader.js',)

    label_upload = _("Upload")

    preview_postfix = u"_img"

    def _onClickAction(self, previewId, inputId):
        return mark_safe(u'ImageUploader.openUploadWindow(\'#%s\',\'%s\',\'%s\')' %
                         ( previewId, inputId, reverse("_ext.pibu.views.uploadTempImage")) )

    def _getUploadButton(self, previewId, inputId):
        uploadText =  self.label_upload
        uploadAction = self._onClickAction(previewId, inputId)
        return mark_safe(u'<a href="#" onclick="%s;">%s' % ( uploadAction, uploadText) + u'</a>')

    def _format_value(self, value):
        value = DefaultStorage().url(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if attrs is None or not attrs.has_key("render"):
            return super(PreviewImageInput,self).render(name, value, attrs)
        elif attrs["render"] == "preview":
            img_id = final_attrs['id']+self.preview_postfix
            if value == '': value = settings.IMAGE_STUB_FILE
            final_attrs['src'] = force_unicode(self._format_value(value))
            final_attrs['onclick'] = self._onClickAction(img_id, force_unicode(final_attrs['id']))
            return mark_safe(u'<img id=%s %s/>' % (img_id, flatatt(final_attrs)))
        elif attrs["render"] == "upload":
            return self._getUploadButton(force_unicode(final_attrs['id']+self.preview_postfix), final_attrs['id'])
