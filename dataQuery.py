#Backend - récupération des données

import sqlite3
import csv

with open('vol_conso_totale.csv', encoding='utf8') as File:
    reader = csv.reader(File, delimiter=';')
    listed_data = []
    for line in reader:
        listed_data.append(line)

print(listed_data)

connexion = sqlite3.connect('data.db')

c = connexion.cursor()

# Creating the tables and grepping the data

#c.execute('CREATE TABLE paliers (palier int, debut int, fin int, pourcentage float, '
#          'total int)')
for i in range(len(listed_data)):
    vy_listed_data = listed_data[i][0].split(',')
    c.execute('INSERT INTO paliers VALUES ({}, {}, {}, {}, {})'.format(vy_listed_data[0],
                                                                       vy_listed_data[1],
                                                                       vy_listed_data[2],
                                                                       vy_listed_data[3],
                                                                       vy_listed_data[4]
                                                                       ))

# c.execute('CREATE TABLE conso (debut int, fin int, float conso_totale)')
for i in range(len(listed_data)):
    tri_liste = listed_data[i][0].split(',')
    c.execute('INSERT INTO conso VALUES ({}, {}, {})'.format(tri_liste[0],
                                                             tri_liste[1],
                                                             tri_liste[2]))

for a in c.execute('SELECT * FROM conso'):
    print(a)

for b in c.execute('SELECT * FROM palier'):
    print(b)

connexion.commit()

c.close()
