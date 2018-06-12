# Isidore Zone

## liste_oeuvre.py

### Goal

Get Isidore metadata from notice list by SPARQL endpoint.

### Usage

`liste_oeuvre.py [filelist]`

(results saved in \[filelist\].csv)

## liste_dcsource.py

### Goal

Get Isidore source field from notice list by SPARQL endpoint.

### Usage

`liste_dcsource.py [noticelist] [destinationcsvfile]`

## list_domain.py

### Goal

Get the source domain list (and occurence number) of notice list.

### Usage

`liste_domain.py [noticelist]`

## list_domain_scrapyspider.py

Same thing, but with scrapy (so with asynchronous requests).
This time the noticelist is hardcoded.

## post_traitement_id.py

### Goal

Get the http version of the id (aka the Isidore full handle).

### Usage

`post_traitement_id.py [source] [destination] [id column number]`

## post_traitement_rsltvide.py

### Goal

Kicks the empty results of given 2-column CSV.

### Usage

`post_traitement_rsltvide.py [source] [destination]`