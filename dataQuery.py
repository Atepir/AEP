#Backend - récupération des données

import sqlite3
import csv

with open('MyDocument.csv', encoding='utf8') as File:
    reader = csv.reader(File, delimiter=';')
    for line in reader:
        print(line)  # La tu auras chaque ligne

