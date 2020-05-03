# Adduction en Eau Potable (AEP)
## Programme d'aide au calcul et à l'analyse des données
Le projet AEP est née de notre volonté à
 rendre plus faciles certains calculs aliénants 
 qui peuvent survenir dans l'étude des données
 statistiques pour l'optimisation des adductions
 en eau potable.
 
 Ainsi, ce programme vous permettra, à partir
 d'une entrée spécifique (deux fichiers aux formats .csv et typés de la classique manière), de générer un ensemble de sortie comprenant:
 <ul>
<li>Une <b>image représentant le diagramme relatif à votre modèle d'étude</b>; </li>
<li><b>Deux bases de données locales Sqlite3</b> contenant pour l'une vos données d'entrée et pour l'autre, vos données de sortie; </li>
<li>Et enfin <b>un fichier Excel</b> au format <i>.xls</i> contenant un recapitulatif de votre modèle d'étude ainsi que les résultats du programme.</li>
</ul>

## Pourquoi ce module ?
Les calculs pour ingéniorales peuvent parfois se réveler aliénantes, trouver un  model de calcul qui retire ce mécanisme de cette tache constitue un soulagement aussi bien par la facilité que l'efficacité qu'offre un tel module. 

Mais les avantages ne se limitent pas là.
En effet, en mettant en place des bases de données relationnelles, nous assurons de la portabilité et de la possibilité d'extensibilité illimitée du module qui, complété, pourrait permettre bien plus de calculs et sauver les nuits blanches de plus d'un ingénieur.

## Installation (clonage)
Pour cloner le répertoire, la commande est un git : 

```shell script
git clone https://github.com/atepir/aep
```

## Examples d'utilisation (avec les données de test)
### 1. En ligne de commande
Depuis le répertoire de téléchargement, rejoindre le dossier aep en utilisant la commande :

```shell script
cd aep
```
Ensuite, lancer le script <b>\_\_main__.py</b> avec les bons paramètres. Par exemple, avec les fichiers d'exemple, on aurait :
```shell script
python __main__.py -c "test_inputs/conso.csv" -p "test_inputs/paliers.csv" -d "test_results/test_database.db" -s "test_results/test_output_db.db" -o "test_results/test_output.xls" -i "test_results/output_img.png" -v 50000
```
### 2. Dans un script en tant que module
Ceci est l'option idéale pour accéder à toutes les options de manière individuelle. Parfait pour les améliorations du présent module. Pour ce faire, rien de plus simple: après clonage du répertoire, importer aep de la manière habituelle c'est-à-dire :
```python
import aep
```
ou
```python
from aep import *
```
ou encore
```python
import aep as import_name
```
encore
```python
from aep import calculations
from aep import dataQuery
```
## Spécifications
Pour les spécifications relatives aux données d'entrée, veuillez vous repporter aux exemples et aux fichiers d'exemples

## Licence d'attribution
<a rel="license" href="http://creativecommons.org/licenses/by-sa/1.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/1.0/88x31.png" /></a><br />Cette œuvre est mise à disposition selon les termes de la <a rel="license" href="http://creativecommons.org/licenses/by-sa/1.0/">Licence Creative Commons Attribution -  Partage dans les Mêmes Conditions 1.0 Générique</a>.

## Contacts
Pour toute question, veuillez nous contactez aux adresses `akibale@gmail.com` et `atepir0@gmail.com`.