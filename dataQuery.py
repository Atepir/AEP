#Backend - récupération des données

import sqlite3
import csv

with open('conso.csv', encoding='utf8') as File:
    reader = csv.reader(File, delimiter=';')
    listed_data = []
    for line in reader:
        listed_data.append(line)

print(listed_data)

connexion = sqlite3.connect('data.db')

c = connexion.cursor()

# Creating the tables and grepping the data

def createTablePaliers():
    """
    :param: none
    :return: creates a table named paliers in the database
    """
    c.execute('CREATE TABLE paliers (palier int, debut int, fin int, pourcentage float, total int)')

def insertPaliers(listed_data):
    """
    :param listed_data: csv file which contains the paliers data as a 5 columns table of respectively integer,
                        integer, integer, float and integer values
    :return: creates a row in the table paliers
    """
    for i in range(len(listed_data)):
        vy_listed_data = listed_data[i][0].split(',')
        c.execute('INSERT INTO paliers VALUES ({}, {}, {}, {}, {})'.format(vy_listed_data[0],
                                                                           vy_listed_data[1],
                                                                           vy_listed_data[2],
                                                                           vy_listed_data[3],
                                                                           vy_listed_data[4]
                                                                           ))

def createTableConso():
    """
    :param: none
    :return: creates a table named conso in the database
    """
    c.execute('CREATE TABLE conso (debut int, fin int, conso_totale float, debit float)')

def insertConso(listed_data):
    """
        :param listed_data: csv file which contains the data of conso under the form of a 4 rows table which have
                            respectively the values of an integer, integer, float and float
        :return: creates a row in the table paliers
        """
    for i in range(len(listed_data)):
        tri_liste = listed_data[i][0].split(',')
        c.execute('INSERT INTO conso VALUES ({}, {}, {}, {})'.format(tri_liste[0],
                                                                 tri_liste[1],
                                                                 tri_liste[2],
                                                                     tri_liste[3]))

def showConso():
    """
    :param: none
    :return: prints the data stored in the table conso
    """
    for a in c.execute('SELECT * FROM conso'):
        print(a)

def showPaliers():
    """
    :param: none
    :return: prints the data stored in the table paliers
    """
    for b in c.execute('SELECT * FROM paliers'):
        print(b)



connexion.commit()

c.close()
