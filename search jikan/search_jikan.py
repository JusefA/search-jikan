import json
from jikanpy import Jikan
import time
import arrow

jikan = Jikan()

print('Parsing file...')
pstart = arrow.utcnow()

predata = {'animes':[]}
mfile = open('C:\\Users\\jusef\\Downloads\\mangas.txt','r')

rating = 0
genres = []

cond = []
for x in mfile:         #This conditiones the source file so it only has the names
    if x.find('[') != -1:
        n = x.split('[')
        cond.append(n[0])

    elif x.find('(') != -1:
        n = x.split('(')
        cond.append(n[0])

    else:
        cond.append(x.replace('\n','').strip())

cond = list(dict.fromkeys(cond))    #Removing double entries

for x in cond:      #Converting all names to a py dict format
    predata['animes'].append({'name':x, 'rating':rating, 'genres':genres})



with open('animes.json', 'w') as f:
    json.dump(predata, f, indent=4)
    f.close()

with open('animes.json') as f:
    data = json.load(f)
    f.close()

pend = arrow.utcnow()
print('Parsing file finished in',(pend-pstart).total_seconds()*1000,'ms')
print('Beginning Jikan API requests...')
apistart = arrow.utcnow()

gfc = 0
mnum = len(data['animes'])

for x in data['animes']:
    time.sleep(4)
    print('Query Request Posted!')
    query = jikan.search('anime',x['name'])
    print('Request Fulfilled!')
    c = 0
    found = False
    for r in query['results']:
        if r['title'].lower() == x['name'].lower():
            print('Exact Request Posted!')
            dmexact = jikan.anime(r['mal_id'])
            print('Request Fulfilled!')
            gfc = gfc + 1
            print('Genres Found |',gfc,'of',mnum)
            found = True
            for g in dmexact['genres']:
                x['genres'].append(g['name'])
            x['rating'] = dmexact['score']
            x['mal_id'] = dmexact['mal_id']
            break

    if found:
        with open('animes.json', 'w') as f:
            json.dump(data,f,indent=4)
            f.close()
        continue

    else:
        time.sleep(3)

    for r in query['results']:
        print('Exact Request Posted!')
        exact = jikan.anime(r['mal_id'])
        print('Request Fulfilled!')
        if exact['title_english'] != None:
            if exact['title_english'].lower() == x['name'].lower():
                gfc = gfc + 1
                print('Genres Found |',gfc,'of',mnum)
                found = True
                for g in exact['genres']:
                    x['genres'].append(g['name'])
                x['rating'] = exact['score']
                x['mal_id'] = exact['mal_id']
                
                break
        

        for syn in exact['title_synonyms']:
            if syn.lower() == x['name'].lower():
                gfc = gfc + 1
                print('Genres Found |',gfc,'of',mnum)
                found = True
                for g in exact['genres']:
                    x['genres'].append(g['name'])
                x['rating'] = exact['score']
                x['mal_id'] = exact['mal_id']
                break

        if found:
            break

        c = c + 1
        if c > 1:
            print('No exact MAL match found for',x['name'],"Falling back to first result...")
            print('Final Exact Request Posted!')
            fresult = jikan.anime(query['results'][0]['mal_id'])
            print('Final Request Fulfilled!')
            for g in fresult['genres']:
                    x['genres'].append(g['name'])
            x['rating'] = fresult['score']
            x['mal_id'] = fresult['mal_id']
            gfc = gfc + 1
            print('Genres Found |',gfc,'of',mnum)
            break
        
    with open('animes.json', 'w') as f:
        json.dump(data,f,indent=4)
        f.close()
    time.sleep(4)

apiend = arrow.utcnow()
print('Jikan API requests finished in',(apiend-apistart).total_seconds(),'s')
