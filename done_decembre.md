4. Script de déduplication entre base écrit (mais non appliqué par nécessité de complétion de certaines données auparavant)
DONE 5. INA: sortie de la liste d'acteurs par catégorie en précisant leur rôle + listes globales des participants & sujets & rôles + graphe des acteurs/sujets
6. Matrice pondérée temps d'étude vs année de publication
7. Script jython de complétion des données + formation de la colonne période heuristique dans OR

# Tâches réalisées en décembre

## Base Thèses

### Arbre des directions

`MFR-Actions/Aggrégation_Bases_Publications_Scientifiques/Visualisations/Thèses`

Il s'agit d'une arborescence (fondé sur d3) des thèses, avec une coloration
et un tri des thèses par nombre de descendants.

Les thèses ayant moins de deux descendants ne sont pas incluses.
Les codirections sont considérées comme des directions à part entière,
et les thèses codirigées ne sont pas réintroduite dans les thèses dirigées
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

Il s'agit de CSV donnant par base la liste des acteurs et d'une catégorie de rôle
(journaliste ou non) selon une catégorie d'émission (journal ou non).

### Réseaux acteurs-sujets

Il s'agit d'un réseau (au format GEXF) biparti acteurs-sujets, les liens
entre acteurs et sujets étant la participation de l'acteur à une émission
comportant ce sujet.

## Dates d'études

## Script sur l'entièreté de la base

### Scripts dans OpenRefine

### Scripts hors d'OpenRefine