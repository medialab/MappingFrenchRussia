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