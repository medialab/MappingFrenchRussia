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

select distinct ?titre ?date ?id ?nomauteur ?sujet where {
"""+'\n<'+source[:-1]+'>'+""" dcterms:title ?titre;
 dces:date ?date;
 dcterms:identifier ?id;
 dcterms:creator / foaf:name ?nomauteur;
 dcterms:subject / (skos:prefLabel|skos:altLabel) ?sujet.
}
"""
		#print(query)
		data = []
		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		for headers in results['head']['vars']:
			#print(headers, end=" ")
			data.append(set({}))
		print()
		for result in results["results"]["bindings"]:
			for i, var in enumerate(results['head']['vars']):
				#print(result[var]['value'], end=" ")
				data[i].add(result[var]['value'])
			#print()
		for i, headers in enumerate(results['head']['vars']):
			print(headers, ':', end=" ")
			for j in data[i]:
				print(j, end=', ')
			print()
	f.close()