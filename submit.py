import common, webbrowser, json, urllib2
from urllib import urlencode

print '===Authentication==='
if webbrowser.open_new('http://lastfmerge.appspot.com/auth'):
    print 'A login dialog has been opened in your default web browser to achieve the authentication process.\nCheck that you are logged on Last.fm with your target account, switch between accounts if not.'
    print 'If you can\'t see this dialog, go on http://lastfmerge.appspot.com/auth'
else:
    print 'Please go to http://lastfmerge.appspot.com/auth to achieve the authentication process.'

print 'You will be redirected on a confirmation dialog showing a code, please enter your authentication code below.'
servicetoken = raw_input('Authentication code: ')

print 'Checking code validity...',
check_r = common.jsonfetch('http://lastfmerge.appspot.com/check/' + servicetoken, use_cache=False)
if check_r.has_key('Error'):
    print check_r['Message']
else:
    username = check_r['Username']
    print 'Valid for ' + username

    print '\nSelect a submission mode:\n1 : Scrobble tracks.\n2 : Remove previous scrobbled tracks (revert).'
    mode = raw_input('[1,2]> ')
    if mode == '2':
        remove = True
        print 'Reverting operation selected.'
    else:
        remove = False
        print 'Scrobbling operation selected.'
    
    print 'Parsing scrobbles file...'
    f = open('scrobbles.json', 'r')
    scrobbles = json.loads(f.read())
    f.close()
    
    #Dropping unicode scrobbles
    parsed_scrobbles = list()
    for scrobble in scrobbles:
        converted = common.unicodefilter(scrobble)
        if converted != None:
            parsed_scrobbles.append(converted)
    parsed_scrobbles = json.dumps(parsed_scrobbles)
    data = {'scrobbles' : parsed_scrobbles}
    if remove:
        data['mode'] = 'remove'
    data = urlencode( data )
    
    url = 'http://lastfmerge.appspot.com/scrobble/' + servicetoken
    print 'Submitting scrobbles...'
    response = urllib2.build_opener().open(urllib2.Request(url, data)).read()
    print json.loads(response)['Message']