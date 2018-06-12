# Stats zone

This is where goes all the data analysis helpers about the joined scientific
publication dataset.

## gen_stats.py
### Goal
Generate some basic metrics about directors and topics across years
for the thesis dataset.
### Usage
Use the correct iterator in the script, and then run:
`gen_stats.py [thesis dataset] [destination metric CSV]`

## draw_codirection_fields_network.py
### Goal
Draw the bipartite codirectors-fields network (thesis dataset).
### Usage
`draw_codirection_fields_network.py [thesis dataset] [destination bipartite network GEXF]`

## get_nopubli_after_thesis.py
### Goal
Points out each graduated PhD that does not seem to follow with an academic career
(no publications after the thesis).
### Usage
`get_nopubli_after_thesis.py [source CSV] > [non academic phd graduated list]`
Please note that standard error outputs the number of publications authors as well as
the number of should-have-written-something-already graduated PhD.

## topic_first_apparition_yearly.py
### Goal
Get the list of thesis topic first apparition.
### Usage
`topic_first_apparition_yearly.py [source CSV] [destination CSV]`

## extract_thesis_per_year.py
### Goal
Get the number of thesis directors and authors per year.
It can be used to make a ratio directors/authors which would
represent global directors dispersion. This ratio should be between 0 and 1.
### Usage
`extract_thesis_per_year.py [source CSV] [destination CSV]`

## BnF_subject_stats.py
### Goal
Get the list of BnF topics and their occurences.
### Usage
`BnF_subject_stats.py [source CSV] [destination CSV]`