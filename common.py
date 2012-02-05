import config
from hashlib import md5
import urlparse

def parse_qs(qs):
    result = dict()
    for pair in qs.split('&'):
        sep = pair.split('=')
        result [ sep[0] ] = sep[1]
    return result

def makesig(url):
    #Making an ordered dictionnary of query parameters for the URL
    dic = parse_qs( urlparse.urlparse(url).query )
    try:
        dic.pop('format')
    except:
        pass
    result = str()
    for key in sorted(dic): #While sorting the dictionnary alphabetically
        #Append each <name><value> pair included in dictionnary
        result = result + key + dic[key]

    result = result + config.lastfm['Secret'] #Appending Secret API Key
    #Hashing the string with MD5
    hashobject = md5()
    hashobject.update(result)
    result = hashobject.hexdigest()
    return result

def appendsig(url):
    sig = makesig(url)
    return url + '&api_sig=' + sig