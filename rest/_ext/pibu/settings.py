import os
from django.conf import settings


IMAGE_STUB_FILE = settings.STATIC_URL+"common/images/logoStub.png"
IMAGE_MAX_WIDTH = 1024
IMAGE_MAX_HEIGHT = 768
IMAGE_MAX_SIZE = 5*1024*1024 #5 MB in bytes
MEDIA_URL = settings.MEDIA_URL
MEDIA_TEMP_URL = os.path.abspath(settings.MEDIA_ROOT +"temp/")