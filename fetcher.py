import config, common
import json

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
first = parser( common.jsonfetch( url(username, page ), use_cache=False ) )
result = first['Result']
total = first['Total']

page = 2

while page <= total:
    print str(page) + ' / ' + str(total)
    pageresult = parser( common.jsonfetch( url(username, page ), use_cache=False ) )['Result']
    for i in pageresult:
        result.append(i)
    page = page + 1

f = open(username + '.json', 'w')
f.write(json.dumps(result, f))
f.close()