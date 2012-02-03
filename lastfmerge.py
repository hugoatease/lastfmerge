# -*- coding: utf-8 -*-

import config, common, datastore, bottle
from google.appengine.api import urlfetch
from google.appengine.api.labs import taskqueue
from google.appengine.ext.db import Key
import simplejson, datetime
app = bottle.Bottle()
bottle.debug(True)

@app.route('/')
def index():
    return "<h3>Hello world</h3>"

@app.route('/begin/:legacy')
def lastauth(legacy):
    bottle.response.set_cookie('legacy', legacy, path='/')
    bottle.redirect('http://www.last.fm/api/auth/?cb=http://lastfmerge.appspot.com/callback&api_key=' + config.lastfm['Key'])

@app.route('/callback')
def lastcallback():
    legacy = bottle.request.get_cookie('legacy')
    token = bottle.request.query.token
    
    response = urlfetch.fetch( common.appendsig('http://ws.audioscrobbler.com/2.0/?method=auth.getSession&format=json&api_key=' + config.lastfm['Key'] + '&token=' + token) ).content
    data = simplejson.loads(response)

    username = data['session']['name']
    session = data['session']['key']
    
    userentity = datastore.Users(legacy = legacy, username = username, session = session)
    userentity.put()
    userkey = userentity.key()
    
    return str(userkey)
    
@app.route('/fetch/:username')
def fetch(username):
    taskqueue.add(url='/tasks/fetch/' + username + '/1', method='GET')

@app.route('/tasks/fetch/:username/:page')
def fetchtask(username, page):
    page = int(page)
    c = urlfetch.fetch( 'http://ws.audioscrobbler.com/2.0/?format=json&api_key='+config.lastfm['Key']+'&method=user.getrecenttracks&limit=200&user=' + username + '&page=' + str(page) ).content
    data = simplejson.loads(c)
    total = int(data['recenttracks']['@attr']['totalPages'])
    
    for track in data['recenttracks']['track']:
        artist = track['artist']['#text']
        name = track['name']
        try:
            ts = int(track['date']['uts'])
        except:
            ts = None
        if ts != None:
            date = datetime.datetime.fromtimestamp(ts)
        
        songentity = datastore.Songs(artist = artist, name = name)
        songentity.put()
        songkey = songentity.key()
    
    if page < total:
        taskqueue.add(url='/tasks/fetch/' + username + '/' + str(page + 1), method='GET')

bottle.run(app, server = 'gae')
