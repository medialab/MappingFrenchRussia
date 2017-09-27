# BNF Zone

## class MetadonneesNotice

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