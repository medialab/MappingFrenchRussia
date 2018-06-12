# Tâches réalisées en décembre

## Base Thèses

### Arbre des directions

`MFR-Actions/Aggrégation_Bases_Publications_Scientifiques/Visualisations/Thèses`

Il s'agit d'une arborescence (fondée sur d3) des thèses, avec une coloration
et un tri des thèses par nombre de descendants.

Les thèses ayant moins de deux descendants ne sont pas incluses.
Les codirections sont considérées comme des directions à part entière,
et les thèses codirigées ne sont pas réintroduites dans les thèses dirigées
par les codirecteurs de la codirection.
Les codirections n'ayant pas amené plus de deux descendants sont donc élaguées
de la visualisation.

### Réseau de codirection

`MFR-Actions/Aggrégation_Bases_Publications_Scientifiques/Stats/Thèses/director_topic_network.gexf`

Il s'agit d'un réseau (au format GEXF) biparti codirecteurs-sujets, les liens
entre les codirecteurs et les sujets se faisant au travers des thèses en codirections.

### Aggrégations sur les directeurs et les sujets

`MFR-Actions/Aggrégation_Bases_Publications_Scientifiques/Stats/Thèses`

Il s'agit de différents CSV proposant des aggrégations de la base thèse,
portant sur les directeurs de thèses et les sujets qu'ils encadrent.

Un readme est présent dans le dossier pour le détail du contenu des différents fichiers.

## Base BnF

`MFR-Actions/Aggrégation_Bases_Publications_Scientifiques/Stats/BnF`

Il s'agit de CSV à propos des sujets de la BnF (leur nombre d'occurence notamment)
et des éléments de ces sujets (un sujet est composé d'éléments séparés par `--`).

Il y a également une matrice d'appartenance des publications aux différents éléments de sujet.

## Base INA

`MFR-Actions/bases NOEL 2017/INA`

### Listes globales

Il s'agit de CSV comprenant la liste de tout les acteurs, sujets et rôles
dans toute la base INA (radio, tv nationale, tv régionale, tv satellite).

### Listes acteurs-catégorie

Il s'agit de CSV donnant par base la liste des acteurs avec leur catégorie de rôle
(journaliste ou non) selon une catégorie d'émission (journal ou non).

### Réseaux acteurs-sujets

Il s'agit d'un réseau par base (au format GEXF) biparti acteurs-sujets, les liens
entre acteurs et sujets étant la participation de l'acteur à une émission
comportant ce sujet.


## Script sur l'entièreté de la base

### Scripts dans OpenRefine

Il s'agit de différents scripts de complétion et nettoyage des données:

- Suppression d'informations inutiles dans les noms d'auteurs (translitérations alternative, mentions "auteur du texte")
- Correction d'encodage des titre scanR
- Complétion de certaines dates de publication dans la base EBSEES
- Constitution d'une série d'heuristique pour évaluer la période étudiée pour les publications BnF

### Scripts hors d'OpenRefine

- Script de déduplication des publications entre les bases (mais non appliqué faute d'une ancre suffisamment stable pour le moment)
- Script de repliage des noms d'auteurs pour une même publication (équivalent du "join multi-valued cells" d'OpenRefine)

## Dates d'études

`MFR-Actions/bases NOEL 2017/mfr_time_studied_year_matrix.csv`

Il s'agit d'une matrice année de publication vs année d'études.
Elle est constituée à partir du champ sur la période étudiée, constitué à la main
pour la base thèses et par script (via une série d'heuristique) pour les publications BnF.

Un score de 100 est attribué à chaque publication. Ce score est réparti équitablement
sur les différentes année de la période étudiée par la publication.