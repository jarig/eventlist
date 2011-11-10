import os
from django.core.files.base import File
from django.core.files.storage import DefaultStorage

def urlToPath(url):
    return DefaultStorage().path(url)

def resolveMediaPath(dbPath):
    return DefaultStorage().url(dbPath)

def uploadLocalImage(filepath, filename, uploadFunc, overwrite=True):
    storage = DefaultStorage()
    uploadFunc(
        filename,
        storage.open(filepath)
    )
    #if overwrite: #delete old file
    #    dirname = os.path.dirname(filepath)
    #   storage.delete(os.path.join(dirname,filename))
  