

Some scripts to extract data from http://www.theses.fr

# scrap_theses_searchEngine.js

Download theses metadata info as json files either from theses ID list or search engine results.

Store data into theses_metadata.json

# hydrate_thesis.js

Parse thesis HTML pages to get unavailable info from API (keywords)

Store data in theses_metadata_abstract_keywords.json

# get_all_theses_from_dirs.js

From a theses_metadata.json file : 
- extract thesis director id list
- get all thesis directed by those director from API
- store list of theses id in all_theses_ids.csv

# json2csv.js

transform theses_metadata_abstract_keywords.json into theses_metadata.csv
