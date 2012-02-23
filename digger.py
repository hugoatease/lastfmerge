import json, time

source = raw_input('Source Userame: ')
target = raw_input('Target Username: ')

def importmsg(data):
    print str(len(data)) + ' scrobbles have been imported.'

try:
    f = open('ignored.json','r')
    print 'Importing ignored.json file...'
    data = json.loads(f.read())
    f.close()
    importmsg(data)
except:
    data = list()

print 'Parsing ' + target + '.json file...'
f = open(target+'.json', 'r')
target_data = json.loads(f.read())
f.close()
importmsg(target_data)
for track in target_data:
    data.append(track)

holes = list()
print 'Searching for running time space...'
for track in data:
    if track['Duration'] != None:
        result = {'Begin' : track['Time'] + track['Duration'], 'End' : int(time.time()) }
        holes.append(result)
        break

print 'Searching for spaces...'
i = 0
while i <= len(data) - 2 :
    if data[i + 1]['Duration'] != None:
        if (data[i]['Time'] - (data[i+1]['Duration'] + data[i+1]['Time']))  > 3600*2 and (time.time() - data[i]['Time']) < 3600*24*12:
            dic = {'Begin': data[i+1]['Time'] + data[i+1]['Duration'],  'End' : data[i]['Time']}
            holes.append(dic)
    i = i +1

scrobbles = list()
print 'Parsing ' + source + '.json file...'
f = open(source+'.json', 'r')
data = json.loads(f.read())
importmsg(data)
f.close()

print 'Filling spaces...'
for hole in holes:
    i = hole['End']
    for track in data:
        if track['Duration'] != None:
            if i - track['Duration'] > hole['Begin']:
                scrobbles.append( {'Artist' : track['Artist'], 'Name' : track['Name'], 'Time' : i - track['Duration']} )
                i = i - track['Duration']
                data.remove(track)
        else:
            data.remove(track)

print 'Writing scrobbles.json file...'
f = open('scrobbles.json', 'w')
f.write(json.dumps(scrobbles))
f.close()

if len(data) > 0:
    f = open('ignored.json', 'w')
    f.write(json.dumps(data))
    f.close()
    print 'NOTICE : All scrobbles can\'t be imported cause of a lack of spaces on the new account.\nIgnored scrobbles have been saved to ignored.json . They will be added to your scrobbles next time you run digger.py'
