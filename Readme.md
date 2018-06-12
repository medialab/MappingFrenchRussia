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

## Root scripts

### reconciliation_etape2_3.py
#### Goal
Reconcile all base by making a block matrix.
To do so, we take all the columns of all base, grouped by base,
and we insert publications grouped by base (BnF, Thèses, and so on),
leaving empty values for each column that doesn't come from the same base.
We finally insert at the beginning some common columns whose values are taken
in a base-specific way.
#### Usage
`reconciliation_etape2_3.py [to be reconciled CSV list] [joined dataset CSV]`

### fold_lines.py
#### Goal
Join rows as with the OpenRefine operation "join multivalued cells".
Much more stupid than it's OpenRefine counterpart, so much more reliable.
#### Usage
`fold_lines.py [joined dataset to be folded] [folded joined dataset]`

### dedup_across.py
#### Goal
Deduplicate publications across bases, filling up all the base-specific data that
we have.
#### Usage
`dedup_across.py [joined dataset to be deduplicated] [deduplicated joined dataset]`
