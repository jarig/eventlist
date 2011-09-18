import re
from django.db import models

# parse jquery's json
def json(data):
    result = {}
    for key in data.keys():
        #test[sadsd][asdas]
        #test[sadsd][xxx]
        rKey = re.match("(.+)(\[.+\])",key)
        if rKey == None:
            result[key] = data[key]
            continue
        result[rKey.group(1)] = {}
        rData = _formData(rKey.group(2), result[rKey.group(1)])
        rData = data[key]
    return result

#[asdas][aasdas]
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
    return result #return reference to resulted dict