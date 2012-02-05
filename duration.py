import config
import sys
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
    

def url(mbid = None, artist = None, name = None):
    if mbid != None:
        return 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&format=json&api_key=' + config.lastfm['Key'] + '&mbid=' + mbid
    elif artist != None and name != None:
        return 'http://ws.audioscrobbler.com/2.0/?method=track.getinfo&format=json&api_key=' + config.lastfm['Key'] + '&artist=' + artist + '&track=' + name

def parser(data, mbid = True):
    if mbid:
        try:
            artist = data['album']['artist']
            tracks = list()
            for track in data['album']['tracks']['track']:
                duration = int(track['duration'])
                name = track['name']
                tracks.append({'Artist' : artist, 'Name' : name, 'Duration' : duration})
            return tracks
        except KeyError:
            return None
    else:
        try:
            artist = data['track']['artist']['name']
            name = data['track']['name']
            duration = int(data['track']['duration'])
            return {'Artist' : artist, 'Name' : name, 'Duration' : duration}
        except KeyError:
            return None

username = raw_input('Last.fm username: ')
f = open(username + '.json', 'r')
data = json.loads(f.read())
f.close()

print 'Total scrobbles: ', str(len(data))
print 'Fetching unique MBIDs...',

mbids = list()
for track in data:
    mbid = track['Mbid']
    if mbids.count(mbid) == 0:
        mbids.append(mbid)

total = len(mbids)

print str(total)
print 'Getting durations, it might take a while...'

i = 0
while i <= (total - 1):
    print str(i+1) + ' / ' + str(total)
    try:
        results = parser( jsonfetch( url(mbids[i]) ), mbid = True )
    except:
        results = None

    if results != None:
        for track in data:
            for td in results:
                if track['Artist'] == td['Artist'] and track['Name'] == td['Name']:
                    track['Duration'] = td['Duration']
                    print track['Artist'], track['Name'], track['Duration']
    i = i + 1

missing = 0
for track in data:
    if track.has_key('Duration') == False:
        missing = missing + 1
print "Missing track's durations: " + str(missing)
finalmissing = 0
i = 0
for track in data:
    if track.has_key('Duration') == False:
        i = i +1
        print str(i) + ' / ' + str(missing)
        try:
            results = parser( jsonfetch(url(mbid=None, artist=track['Artist'], name=track['Name'])), mbid=False)
        except:
            results = None
        if results != None:
            track['Duration'] = results['Duration']
        else:
            track['Duration'] = None
            finalmissing = finalmissing + 1
print finalmissing

f = open(username+'.json', 'w')
f.write(json.dumps(data))
f.close()