#Backend - récupération des données

import sqlite3
import csv

class DataQuery:
    def __init__(self, database):
        """
        :object: data collector
        """
        self.data = sqlite3.connect(database)
        self.dataCursor = self.data.cursor()

    def getData(self, file):
        """
        :param file: csv file as a path string
        :return: python list that contains the data stored in the entry
        """
        try:
            with open(file, encoding='utf8') as File:
                reader = csv.reader(File, delimiter=';')
                listed_data = []
                for line in reader:
                    listed_data.append(line)
        except FileNotFoundError:
            return 1
        return listed_data

    # print(listed_data)


    # Creating the tables and grepping the data

    def createTablePaliers(self):
        """
        :param: none
        :return: creates a table named paliers in the database
        """
        self.dataCursor.execute('CREATE TABLE paliers (palier int, debut int, fin int, pourcentage float, total int)')

    def insertPaliers(self, listed_data):
        """
        :param listed_data: csv file which contains the paliers data as a 5 columns table of respectively integer,
                            integer, integer, float and integer values
        :return: creates a row in the table paliers
        """
        for i in range(len(listed_data)):
            vy_listed_data = listed_data[i][0].split(',')
            self.dataCursor.execute('INSERT INTO paliers VALUES ({}, {}, {}, {}, {})'.format(vy_listed_data[0],
                                                                                        vy_listed_data[1],
                                                                                        vy_listed_data[2],
                                                                                        vy_listed_data[3],
                                                                                        vy_listed_data[4]
                                                                                        ))

    def createTableConso(self):
        """
        :param: none
        :return: creates a table named conso in the database
        """
        self.dataCursor.execute('CREATE TABLE conso (debut int, fin int, conso_totale float, debit float)')

    def insertConso(self, listed_data):
        """
            :param listed_data: csv file which contains the data of conso under the form of a 4 rows table which have
                                respectively the values of an integer, integer, float and float
            :return: creates a row in the table paliers
            """
        for i in range(len(listed_data)):
            tri_liste = listed_data[i][0].split(',')
            self.dataCursor.execute('INSERT INTO conso VALUES ({}, {}, {}, {})'.format(tri_liste[0],
                                                                                  tri_liste[1],
                                                                                  tri_liste[2],
                                                                                  tri_liste[3]))

    def showConso(self, ext=0):
        """
        :param: none
        :return: a list of the stored data
        """
        consoList = []
        for a in self.dataCursor.execute('SELECT * FROM conso'):
            consoList += [a]
        return consoList

    def showPaliers(self):
        """
        :param: none
        :return: a list of the stored data
        """
        paliersList = []
        for b in self.dataCursor.execute('SELECT * FROM paliers'):
            paliersList += [b]
        return paliersList

# Obj = DataQuery()

# createTableConso()
# insertConso(getData('conso.csv'))
# createTablePaliers()
# insertPaliers(getData('paliers.csv'))
# showConso()
# showPaliers()

# Obj.data.commit()

# Obj.dataCursor.close()