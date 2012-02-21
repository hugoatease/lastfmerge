import config
import json, urllib2
from hashlib import md5, sha1

def ws(query):
    return config.server + query

def graburl(url):
    page = urllib2.urlopen(url)
    return page.read()

def cache(url):
    urlhash = sha1(url).hexdigest()
    get = False
    try:
        f = open('cache/' + urlhash + '.cache', 'r')
        data = f.read()
        f.close()
        return data
    except:
        get = True
    if get == True:
        data = graburl(url)
        f = open('cache/' + urlhash + '.cache', 'w')
        f.write(data)
        f.close()
        return data
    
    
def jsonfetch(url, use_cache = True):
    error = 0
    ok = False
    while ok == False and error < 3:
        try:
            if use_cache:
                data = cache(url)
            else:
                data = graburl(url)
            ok = True
        except:
            error = error + 1
    if ok == True:
        return json.loads(data)
    else:
        return None

def unicodefilter(dic):
    raised = False
    for key in dic.keys():
        try:
            dic[key] = str(dic[key])
        except UnicodeEncodeError:
            raised = True
    if raised:
        return None
    else:
        return dic