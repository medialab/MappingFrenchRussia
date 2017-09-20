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

select distinct ?o ?titre ?date ?id ?nomauteur ?sujet where {
"""+'\n<'+source[:-2]+'>'+"""
 dcterms:title ?titre;
 dces:date ?date;
 dcterms:identifier ?id;
 dcterms:creator / foaf:name ?nomauteur;
 dcterms:subject / (skos:prefLabel|skos:altLabel) ?sujet;
}
"""
		print(query)
		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		for result in results["results"]["bindings"]:
			print(result)
	f.close()