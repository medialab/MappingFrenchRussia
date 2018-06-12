#!/usr/bin/python3
from SPARQLWrapper import SPARQLWrapper, JSON
import sys

# /!\ This code is **TAB INDENTED** /!\

# Get the main (aka without dc:source because it was added after) fields of given notice list.

num_start = 6781 #Last one is only Bibliographical ressource => garbage

if len(sys.argv) == 1:
    print ("Usage:")
    print(sys.argv[0], "[sourcelistfile]")
    sys.exit()

sparql = SPARQLWrapper("http://api.rechercheisidore.fr/sparql")
f = open(sys.argv[1], 'r')
for numligne, source in enumerate(f):
    print('\r' + str(numligne), end='')
    if numligne > num_start:
        query = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dces: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

select distinct ?titre ?date ?id ?nomauteur ?nomediteur ?nomcontrib ?sujet ?resume where {
"""+'\n<'+source[:-1]+'>'+""" dcterms:title ?titre;
 dces:date ?date;
 dcterms:identifier ?id;
 dcterms:creator / foaf:name ?nomauteur;
 dcterms:subject / (skos:prefLabel|skos:altLabel) ?sujet.
 OPTIONAL{
"""+'\n{<'+source[:-1]+'>'+" dc:publisher / foaf:name ?nomediteur.} UNION"\
+'\n{<'+source[:-1]+'>'+" dc:description ?resume.} UNION"\
+'\n{<'+source[:-1]+'>'+" dc:contributor / foaf:name ?nomcontrib.}"\
+"""
 }
}
"""
        #print(query)
        data = []
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        output = sparql.query()
    #    try:
    #        output = sparql.query()
    #    except urllib.error.HTTPError as e:
    #        if (e.code != 503):
    #            raise e
    #        while (e.code == 503):
    #            try:
    #                output = sparql.query()
    #            except urllib.error.HTTPError as e:
    #                if (e.code != 503):
    #                    raise e
        results = output.convert()
        #print(results)
        for headers in results['head']['vars']:
        #print(headers, end=" ")
            data.append(set({}))
        #print()
        for result in results["results"]["bindings"]:
            for i, var in enumerate(results['head']['vars']):
                #print(result[var]['value'], end=" ")
                if var in result:#Sparql OPTIONAL clauses make this check mandatory
                    #print(var)
                    data[i].add(result[var]['value'])
        #print()
        csv = ""
        #for i, headers in enumerate(results['head']['vars']):
        #    csv += headers + ','
        #csv = csv[0:-1]+'\n'
        for i in data:
            csv+='§'
            for num, j in enumerate(i):
                if (num):
                    csv += " // "
                csv += j
            csv += '§,'
        csv = csv[0:-1]+'\n'
        g = open(sys.argv[1].split('.')[0]+'.csv', 'a')
        g.write(csv)
        g.close()
        #print(csv)
f.close()
#f.open(sys.argv[1].split('.')[0]+'.csv', 'w')
#f.write(csv)
#f.close()
print("Written")
