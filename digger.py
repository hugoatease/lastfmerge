import json

source = raw_input('Source Userame: ')
target = raw_input('Target Username: ')
f = open(target+'.json', 'r')
data = json.loads(f.read())
f.close()

holes = list()

i = 0
while i <= len(data) - 2 :
    if data[i + 1]['Duration'] != None:
        if (data[i]['Time'] - (data[i+1]['Duration'] + data[i+1]['Time']))  > 60*30:
            holes.append( {'Begin': data[i+1]['Time'] + data[i+1]['Duration'],  'End' : data[i]['Time'], 'Size' : data[i]['Time'] - (data[i+1]['Time'] + data[i+1]['Duration']) })
    i = i +1

scrobbles = list()
f = open(source+'.json', 'r')
data = json.loads(f.read())
f.close()

holes.reverse()
scrobbles.reverse()

for hole in holes:
    i = hole['Begin']
    for track in data:
        if track['Duration'] != None:
            if i + track['Duration'] < hole['End']:
                scrobbles.append( {'Artist' : track['Artist'], 'Name' : track['Name'], 'Time' : i} )
                i = i + track['Duration']
                data.remove(track)

print scrobbles

f = open('scrobbles.json', 'w')
f.write(json.dumps(scrobbles))
f.close()