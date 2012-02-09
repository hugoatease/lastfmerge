import json
import time

source = raw_input('Source Userame: ')
target = raw_input('Target Username: ')
f = open(target+'.json', 'r')
data = json.loads(f.read())
f.close()

holes = list()

available = 0
for track in data:
    if track['Duration'] != None:
        result = {'Begin' : track['Time'] + track['Duration'], 'End' : int(time.time()) }
        available = available + (result['End'] - result['Begin'])
        holes.append(result)
        break

i = 0
while i <= len(data) - 2 :
    if data[i + 1]['Duration'] != None:
        if (data[i]['Time'] - (data[i+1]['Duration'] + data[i+1]['Time']))  > 3600*2 and (time.time() - data[i]['Time']) < 3600*24*15:
            dic = {'Begin': data[i+1]['Time'] + data[i+1]['Duration'],  'End' : data[i]['Time']}
            holes.append(dic)
            available = available + (dic['End'] - dic['Begin'])
    i = i +1

scrobbles = list()
f = open(source+'.json', 'r')
data = json.loads(f.read())
f.close()

goal = 0
for track in data:
    if track['Duration'] != None:
        goal = goal + track['Duration']

if available - goal < 0:
    print "WARNING : All scrobbles can't be proceed cause of a lack of space on the new account."
for hole in holes:
    i = hole['Begin']
    for track in data:
        if track['Duration'] != None:
            if i + track['Duration'] < hole['End']:
                scrobbles.append( {'Artist' : track['Artist'], 'Name' : track['Name'], 'Time' : i} )
                i = i + track['Duration']
                data.remove(track)

f = open('scrobbles.json', 'w')
f.write(json.dumps(scrobbles))
f.close()