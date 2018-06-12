# EBSEES Zone

## class MetadonneesNotice (from MetadonneesNotice.py)

### Goal

Parse an EBSEES notice

### Usage

Give a BeautifulSoup (version 4) tree (or similar) to parse method

### (public) Methods

#### Usable before parsing

- parse: parse the given notice

#### Non-usable before parsing

- dump: raw dump (aka print) of the object
- valid: check if notice contains target keywords
- to_csv: CSV export (return value)

## downloadToDir_scrapyspider.py

### Goal

Download all notices from EBSEES.

## scrapFromDir.py

### Goal

Parse notices in given directory, export the valid ones to CSV.

## ebsees_reconciliation_etape1.py

### Goal

Add standard (standard as "common for all the datasets") fields with proper formatting.