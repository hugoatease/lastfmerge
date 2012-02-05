import config
import urllib2, json
from hashlib import sha1

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
        page = urllib2.urlopen(url)
        data = page.read()
        f = open('cache/' + urlhash + '.cache', 'w')
        f.write(data)
        f.close()
        return data
    
    
def jsonfetch(url):
    error = 0
    ok = False
    while ok == False and error < 3:
        try:
            data = cache(url)
            ok = True
        except:
            error = error + 1
    if ok == True:
        return json.loads(data)
    else:
        return None

def url(username, page):
    return 'http://ws.audioscrobbler.com/2.0/?format=json&api_key='+config.lastfm['Key']+'&method=user.getrecenttracks&limit=200&user=' + username + '&page=' + str(page) 

def parser(data):
    total = int(data['recenttracks']['@attr']['totalPages'])
    result = list()
    for track in data['recenttracks']['track']:
        artist = track['artist']['#text']
        name = track['name']
        try:
            ts = int(track['date']['uts'])
            mbid = track['album']['mbid']
        except:
            ts = None
            mbid = None
        
        result.append( {'Artist' : artist, 'Name' : name, 'Time' : ts, 'Mbid' : mbid} )
    return {'Result' : result, 'Total' : total}

username = raw_input('Last.fm Username: ')
page = 1
print str(page)
first = parser( jsonfetch( url(username, page ) ) )
result = first['Result']
total = first['Total']

page = 2

while page <= total:
    print str(page) + ' / ' + str(total)
    pageresult = parser( jsonfetch( url(username, page ) ) )['Result']
    for i in pageresult:
        result.append(i)
    page = page + 1

f = open(username + '.db', 'w')
f.write(json.dumps(result, f))
f.close()