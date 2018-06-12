# BNF Zone

## class MetadonneesNotice (from MetadonneesNotice.py)

### Goal

Parse a BNF notice (from catalogue.bnf.fr)

### Usage

Give a BeautifulSoup (version 4) tree (or similar) to parse method

### (public) Methods

#### Usable before parsing

- dump_schema: give the CSV line corresponding to the CSV export schema (return value)
- parse: parse the given notice

#### Non-usable before parsing

- dump: raw dump (aka print) of the object
- to_csv: CSV export (return value)

## zone250U_scrapyspider.py

### Goal

Get from BNF SRU (http API returning XML) the Intermarc 250$u field
(aka notice edition number), as well as parsing the result.

## post_traitement_filtre_regex.py

### Goal

Refilter BNF notices (we got them through catalogue.bnf.fr) with a small regex.

## bnf_reconciliation_etape1.py

### Goal

Add standard (standard as "common for all the datasets") fields with proper formatting.