import common, webbrowser, json, urllib2
from urllib import urlencode
from sys import exit
from os import remove

def auth_prompt():
    print '===Authentication==='
    if webbrowser.open_new( common.ws('/auth') ):
        print 'A login dialog has been opened in your default web browser to achieve the authentication process.\nCheck that you are logged on Last.fm with your target account, switch between accounts if not.'
        print 'If you can\'t see this dialog, go on ' + common.ws('/auth')
    else:
        print 'Please go to ' + common.ws('/auth') + ' to achieve the authentication process.'
    
    print 'You will be redirected on a confirmation dialog showing a code, please enter your authentication code below.'
    return raw_input('Authentication code: ')

def token_check(servicetoken):
    print 'Checking code validity...',
    check_r = common.jsonfetch(common.ws('/check/') + servicetoken, use_cache=False)
    if check_r.has_key('Error'):
        print check_r['Message']
        return False
    else:
        username = check_r['Username']
        print 'Valid for ' + username
        return True

try:
    f = open('token', 'r')
    servicetoken = f.read()
    f.close()
    if token_check(servicetoken) == False:
        remove('token')
        print 'Please launch this script again to set your Token'
        servicetoken = None
except IOError:
    servicetoken = auth_prompt()
    if token_check(servicetoken):
        f = open('token', 'w')
        f.write(servicetoken)
        f.close()
    else:
        servicetoken = None

if servicetoken == None:
    exit()

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

url = common.ws('/scrobble/') + servicetoken
print 'Submitting scrobbles...'
response = urllib2.build_opener().open(urllib2.Request(url, data)).read()
print json.loads(response)['Message']