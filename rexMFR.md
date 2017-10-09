# Documentation sur les extractions des bases de publications scientifiques du projet Mapping French Russia

## Préambule

Cette documentation est structurée par bases, les techniques changeant
d'une base à l'autre.

Les différentes techniques employées sont:

- Le scrap de pages HTML
- Le parsing de XML
- L'interrogation de dépôt RDF via SPARQL

Les technologies utilisées sont:

- Python3
- SPARQL
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [SparqlWrapper](https://github.com/RDFLib/sparqlwrapper)

## Conventions communes

Le séparateur utilisé dans le cas d'un champ contenant plusieurs valeurs est `//` préfixé et suffixé d'un espace.

L'expression régulière utilisée pour filtrer la BNF, Persée et scanR est `(?:.*?)(?:\\W|^)(?:(?:russ(?:i)?e)|(?:sovi[eé]t)|(?:urss(?!a)))(?:.*?)`.

## BNF

### Principe d'extraction

Les notices de bases ont été extraites par scrap du [catalogue de la bnf](http://catalogue.bnf.fr).
Une extraction à partir du dépôt RDF a été envisagée initialement, mais certains
champs nécessaires pour l'étude n'offraient pas de possibilités de récupération simple.

Une notice est une publication d'une oeuvre, qui est potentiellement éditée
plusieurs fois. Aussi, pour avoir le numéros d'édition d'une notice,
il a fallu passer par le service SRU de la BNF.

Le catalogue donnant parfois des notices n'ayant aucun rapport,
elles ont été refiltrées par la suite.

#### Communication entre les services

Le dépôt RDF, les notices du catalogue et le service SRU ont un seul point commun:
le lien d'archivage des notices (le *ark:/quelquechose*). Ce lien d'archivage
est préfixé différemment selon le service utilisé.

#### Les notices du catalogue

Les notices du catalogue ont en plus de leur contenu affiché quelques métadonnées
présentées sous l'ontologie DublinCore. Le même champ est habituellement
disponible en version métadonnées DublinCore, et en allant chercher dans le texte de
la notice, *mais pas toujours*. De plus, selon les notices, des champs qui sont
théoriquement présents sous les deux formes peuvent l'être uniquement dans le texte de la notice.

##### Les co-créateurs d'oeuvre

Ils sont catégorisés selon leur rôle (du moins pour les rôles fréquents dans le dataset).

#### Les notices du SRU

Le SRU exporte des métadonnées sur les notices au format XML selon différentes ontologies,
dont l'Intermarc (ontologie utilisée de manière standard par la BNF).
L'unique information extraite du SRU est le numéros d'édition de la notice,
qui est contenu dans le champs 250$u (selon l'ontologie Intermarc).
Il peut y avoir une zone 250 sans que le champ 250$u soit présent.

### Résultat obtenu

Il s'agit d'un CSV avec 4 champs pour chaque rôle: `Nom et prénom`, `Année de naissance`, `Année de décès`, `Lien vers les oeuvres publiées`.
Le champ consacré au numéros d'édition notifie l'absence d'une zone 250 ou
d'un champs u dans la zone 250. Si le champs est vide, cela signifie que
le champ 250$u existe, mais qu'il ne contient aucune données.
D'autres champs notifiant leur absence dans la notice (telle le champ `Notes`)
procèdent de la même manière, permettant de distinguer une absence de champ
d'un champ vide pour une notice donnée.

## Isidore

### Principe d'extraction

Les notices ont été extraites uniquement à partir du dépôt RDF.

#### Le dépôt RDF

Le soucis avec les dépôt RDF, c'est le temps.
En effet les bases RDF étant orientées graphe (et reposant techniquement
sur des bases relationnelles), une requête demandant un nombre arbitraire
de données va avoir un temps d'éxecution prohibitif par rapport à une
base relationnelle. Les bases RDF en accès public se protègent d'une
requête trop gourmande en refusant d'exécuter une requête dont le temps
d'éxecution **estimé** est supérieur à une borne donnée
(classiquement 3600s, soit 1 heure, mais l'estimation est généreuse).

Le principe de ces bases RDF (interrogées par le langage SPARQL) et de renvoyer
tout les n-uplets qui répondent au critère de l'interrogation.
Aussi, si certains champs demandés ont plusieurs valeurs par noeud
(soit un noeud qui est lié par le type de lien correspondant au champ demandé
à plusieurs valeurs), toutes les *combinaisons de valeurs* seront
renvoyées.
Ainsi, les requêtes ont vite tendance à faire des produits cartésiens,
mais également le fait de rechercher tout les noeuds satisfaisant la requête
va allonger le temps d'éxecution de celle-ci.

Mettre plus de champs allonge donc assez rapidement le temps d'éxecution de la requête.

Ensuite, l'instruction `FILTER` permettant de poser des conditions
arbitraires sur les valeurs des champs, elle est à éviter quand il est possible de faire autrement,
car elle est très mal optimisée par les moteurs d'éxecutions de SPARQL.

Mettre des `FILTER` allonge très rapidement le temps d'éxecution de la requête.

Aussi, l'extraction s'est faite par découpage vertical de la requête.

Il a été demandé dans une première requête une liste
d'id de noeuds de la base (ici des publications) qui répondent à nos
critères de filtre, en espérant que cette requête ne soit pas estimée
trop gourmande.

Ensuite, il a été fait une requête par noeud, en demandant tout les champs.
Cette requête est peu demandeuse pour la base, car le noeud de départ est précisé,
il n'y a donc pas besoin d'aller en chercher d'autres. Par contre il y a toujours
le produit cartésien des valeurs multiples des champs.

### Résultat obtenu

Un CSV avec un seul champs pour les contributeurs (contrairement à la BNF).
Isidore indexe les notices depuis plusieurs aggrégateurs.
Aussi, elles comportent énormément de sujets, pas tous dans la langue voulue,
pas tous très pertinents (généralement, le sujet se compose d'un seul mot).

## EBSEES

### Principe d'extraction

Le site ne proposant pas de solutions satisfaisantes, il a été scrapé dans son
intégralité, puis les notices ont été filtrées une à une.

#### Le filtrage

La base rassemblant uniquement des études déjà relativement proche en terme de sujets de Mapping French Russia,
un filtrage plus simple a été réalisé que celui des autres bases.


### Résultat obtenu

Un CSV avec un seul champ pour les contributeurs. Néanmoins, selon le type
de la ressource, l'information sur l'édition est soit dans le champ
`Publication` ou le champ `Publisher` (orthographié sur le site `Publsiher`).

## scanR

### Principe d'extraction

Des CSV ont été extraits à partir de critères basiques (pour ne pas manipuler la base entière) depuis le site,
puis refiltrés.

### Résultat obtenu

Un CSV avec un champ prénom et un champ nom pour les contributeurs.

## Persée

### Principe d'extraction

La recherche de Persée n'étant pas satisfaisante, à la manière de l'EBSEES toutes
les notices ont été rappatriées via l'API OAI, puis filtrées.

#### L'API OAI

Aucune recherche n'est disponible sur cette API.
Celle-ci donne des notices au format XML selon une des trois ontologies disponible
(DublinCore, MODS, Intermarc).
Le problème est qu'une information subtilement différente est disponible dans chacune
des ontologies, aussi il faut récupérer les 3 XML pour avoir une information propre.

Le scrap est donc quantitativement relativement monstrueux par rapport aux autres.

C'est d'ailleurs le seul des scrap présents qui prend la journée.

### Résultat obtenu

Un CSV avec un seul champ pour les contributeurs. Il n'y a pas de champs lié au
sujet dans cette base.