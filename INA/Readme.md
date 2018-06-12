# INA Zone

## Preamble

This zone is quite special for several reasons.

First, it is not a scientific publication database, consequently this base
is not included in the joined scientific publications dataset.

Second, data is already extracted thanks to INA staff, so there is
no scraping script here.

Third, data is already (quite) structured.

Consequently, there are some data analysis helpers scripts, but none
about raw data-care.

## get_global_lists.py
### Goal
Get global (global as "across all CSV") lists of:

1. Subjects
2. Roles
3. Participants
### Usage
`get_global_lists.py [subject CSV] [roles CSV] [participants CSV] [list of schematically consistent CSV to operate on]`

## get_journalist_categories.py
### Goal
Get the participants list and their role (either journalist or not)
to each given category
(currently only two modalities: news report and not news report).
### Usage
`get_journalist_categories.py [source CSV] [destination CSV]`

## draw_subject_participants_network.py
### Goal
Generate subjects-participants bipartite graph.
### Usage
`draw_subject_participants_network.py [source CSV] [destination GEXF]`