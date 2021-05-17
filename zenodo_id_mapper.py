import os
import json
import requests
import pickle

i=1
concepts = []
concept_dois = []
one_offs = []
hits = [0,1]
while len(hits)>0:
    print(i)
    url = 'https://zenodo.org/api/records/?page='+str(i)+'&size=1000&communities=covid-19'
    r = requests.get(url)
    response = json.loads(r.text)
    hits = response['hits']['hits']
    if len(hits)>0:
        for hit in hits:
            try:
                concept_dois.append(hit['conceptdoi'])
                concepts.append(hit['conceptrecid'])
            except:
                one_offs.append(hit['conceptrecid']) 
    
        i=i+1
    else:
        break
        
doi_map = []
failure = []
for eachconcept in concepts:
    query_url = 'https://zenodo.org/api/records/?page=1&size=1000&q=conceptrecid:"'+eachconcept+'"&sort=-version&all_versions=True'
    r = requests.get(query_url)
    response = json.loads(r.text)
    try:
        hits = response['hits']['hits']
        for hit in hits:
            doi_map.append({'version_id':hit['doi'],'concept_id':hit['conceptdoi']})
    except:
         failure.append(eachconcept)

with open(os.path.join(RESULTSPATH,'doi_map.pickle'),'wb') as outfile:
    pickle.dump(doi_map,outfile)
    
with open(os.path.join(RESULTSPATH,'failures.pickle'),'wb') as outfile:
    pickle.dump(failures,outfile)