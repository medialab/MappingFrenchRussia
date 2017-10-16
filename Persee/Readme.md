# Persee Zone

## class MetadonneesNotice (from MetadonneesNotice.py)

### Goal

Parse a Persee notice

### Usage

Give a BeautifulSoup (version 4) tree (or similar) to parse method

### (public) Methods

#### Parsing

Persee's parsing suffers from Persee's OAI which carries 3 ontologies
for its XML notices. Consequently parsing the 3 differents XML for a single notice
is needed (because *of course* these 3 XML carry slightly different data).

Then, there is 4 methods used within the parsing process:

- get_id: parse the ID (from any of the 3 XML)
- parse_dc: parse the given notice with DublinCore ontology
(extract title, publisher, date and language)
- parse_mods: parse the given notice with MODS ontology
(extract abstract and names + roles)
- parse_marc: parse the given notice with MarcXml ontology
(extract description)

#### After parsing

- validate: check if notice contains target keywords
- dump: raw dump (aka print) of the object
- to_csv: CSV export (return value)

## scrap_scrapyspider.py

### Goal

Download & parse to CSV targeted notices.

## post_traitement_date.py

### Goal

Filter notices CSV (kick too old - aka pre 1980 - notices).

## persee_reconciliation_etape1.py

### Goal

Add standard (standard as "common for all the datasets") fields with proper formatting.