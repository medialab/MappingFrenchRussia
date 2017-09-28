# EBSEES Zone

## class MetadonneesNotice

### Goal

Parse an EBSEES notice

### Usage

Give a BeautifulSoup (version 4) tree (or similar) to parse method

### (public) Methods

#### Usable before parsing

- parse: parse the given notice

#### Non-usable before parsing

- dump: raw dump (aka print) of the object
- valid: return the validity of the notice (does it contains one of our keywords ?)
- to_csv: CSV export (return value)