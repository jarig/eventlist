from exceptions import KeyError
import re
from django.core.files.storage import DefaultStorage
from django.forms.models import model_to_dict

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

def modelToDict(modelObj, include=None, exclude=None):
    # exclude - list of keys to be excluded from resulted dict
    dic = model_to_dict(modelObj)
    keys = dic.keys()
    if include is not None: keys = include
    if exclude is not None: keys = list(set(keys) - set(exclude))
    obj = {}
    for key in keys:
        obj[key] = unicode(dic[key])
    return obj

def json(data):
    result = {}
    for key in data.keys():
        #test[sadsd][asdas]
        #test[sadsd][xxx]
        rKey = re.match("(.+)(\[.+\])",key)
        if rKey is None:
            result[key] = data[key]
            continue
        result[rKey.group(1)] = {}
        rData = _formData(rKey.group(2), result[rKey.group(1)])
        rData = data[key]
    return result


def _formData(keyString, result):
    while keyString is not None and keyString != "":
        reObj = re.match("\[(.+?)\]", keyString)
        if reObj is None: break
        key = reObj.group(1)
        try:
            result[key]
        except KeyError: #no such key
            result = result[key] = {} #create new dict and get reference to it
        keyString = re.sub(r'\['+key+'\](.+)',r'\1',keyString)
    return result