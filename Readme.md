# MappingFrenchRussia - Code and (some but not all) data repo

## What's in there

1. Various data extraction script (scrapers, API users, SPARQL query makers)
2. Some data enhancing, cleaning, reconciling scripts
3. Some metrics calculators
4. Not-very-useful visualisation scripts

## How it's organized

- Standalone scripts that affects the joined (aka whole) scientific database are in the repo root (point 2)
- Scripts to be used within OpenRefine for that very same database are in `refine_codes` folder (point 2)
- Scripts concerning INA are in `INA` folder (point 2 and 3)
- Scripts computing some (basic) metrics and generating (basic) graphs are in `stats` folder (point 3)
- Scripts trying to make a good data visualisation (trying is the word) are in `viz` folder (point 4)
- Each other folder is a different source used in the joined scientific database (point 1 and 2)
