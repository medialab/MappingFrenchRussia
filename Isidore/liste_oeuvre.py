#!/usr/bin/python3
from SPARQLWrapper import SPARQLWrapper, JSON
import sys

if (len(sys.argv) == 1):
	print ("Usage:")
	print(sys.argv[0], "[sourcelistfile]")
else:
	sparql = SPARQLWrapper("http://api.rechercheisidore.fr/sparql")
	f = open(sys.argv[1], 'r')
	for source in f:
		#print(i)
		query = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dces: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

select distinct ?titre ?date ?id ?nomauteur ?nomediteur ?sujet ?resume where {
"""+'\n<'+source[:-1]+'>'+""" dcterms:title ?titre;
 dces:date ?date;
 dcterms:identifier ?id;
 dcterms:creator / foaf:name ?nomauteur;
 dcterms:subject / (skos:prefLabel|skos:altLabel) ?sujet.
 OPTIONAL{
"""+'\n{<'+source[:-1]+'>'+"dc:publisher / foaf:name ?nomediteur.} UNION"\
+'\n{<'+source[:-1]+'>'+"dc:description ?resume.}"\
+"""
 }
}
"""
		#print(query)
		data = []
		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		#print(results)
		for headers in results['head']['vars']:
			#print(headers, end=" ")
			data.append(set({}))
		#print()
		for result in results["results"]["bindings"]:
			for i, var in enumerate(results['head']['vars']):
				#print(result[var]['value'], end=" ")
				if (var in result):#OPTIONAL clauses make this check mandatory
#					print(var)
					data[i].add(result[var]['value'])
			#print()
		csv = ""
		for i, headers in enumerate(results['head']['vars']):
			csv += headers + ','
		csv = csv[0:-1]+'\n'
		for i in data:
			csv+='§'
			for num, j in enumerate(i):
				if (num):
					csv += " // "
				csv += j
			csv += '§,'
		csv = csv[0:-1]+'\n'
		print(csv)
		
	f.close()