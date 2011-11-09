import os
from django.core.files.base import File
from django.core.urlresolvers import resolve

def urlToPath(url):
    resObj = resolve(url)
    logoPath = resObj.kwargs['path']
    if logoPath[0] == '/': logoPath = logoPath.replace("/","", 1)
    root = resObj.kwargs['document_root']
    return os.path.join(root, logoPath)

def uploadLocalImage(url, filename, uploadFunc):
    logoPath = urlToPath(url)
    uploadFunc(
        filename,
        File(open(logoPath,'rb'))
    )
    if os.path.exists(logoPath): os.remove(logoPath)
  