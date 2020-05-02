import sqlite3
from aep.dataQuery import DataQuery

result = sqlite3.connect('result.db')

resultCursor = result.cursor()

class Calculations:
    def __init__(self):
        """
        :info: calculator class
        """

    def createTableOutput(self):
        """
        :param: none
        :return: creates table output with 7 columns
        """
        result.execute('CREATE TABLE output(debut int, fin int, conso_totale float, debit float, '
                       'entree float, sortie float, bilan float)')

    def insertReceivedData(self):
        """
        :param: none
        :return: inserts into output the received data
        """
        for elem in DataQuery().showConso():
            result.execute('INSERT INTO output(debut, fin, conso_totale, debit) VALUES ({}, {}, {}, {})'
                           .format(
                elem[0], elem[1], elem[2], elem[3]
            )
                )

    def calculations(self):
        """
        :param:
        :return:
        """
        i = 0
        while i < len(DataQuery().showConso()):
            conso_totale_cursor = result.execute('SELECT conso_totale FROM output WHERE debut={}'.format(i))
            debit_de_pompage_cursor = result.execute('SELECT debit FROM output WHERE debut={}'.format(i))
            for conso_totale in conso_totale_cursor:
                for debit_de_pompage in debit_de_pompage_cursor:
                    if debit_de_pompage[0] - conso_totale[0] > 0:
                        result.execute('UPDATE output SET entree={} WHERE debut={}'
                                       .format(round(debit_de_pompage[0] - conso_totale[0], 2), i))
                        result.execute('UPDATE output SET sortie=0 WHERE debut={}'
                                       .format(i))
                    else:
                        result.execute('UPDATE output SET sortie={} WHERE debut={}'
                                       .format(round(debit_de_pompage[0] - conso_totale[0], 2), i))
                        result.execute('UPDATE output SET entree=0 WHERE debut={}'
                                       .format(i))

            entree_cursor = result.execute('SELECT entree FROM output WHERE debut={}'.format(i))
            sortie_cursor = result.execute('SELECT sortie FROM output WHERE debut={}'.format(i))
            for entree in entree_cursor:
                for sortie in sortie_cursor:
                    if i == 0:
                        result.execute('UPDATE output SET bilan={} WHERE debut={}'
                                       .format(
                            round(entree[0] + sortie[0], 2), i
                        ))
                    if i > 0 :
                        ancien_bilan_cursor = result.execute('SELECT bilan FROM output WHERE debut={}'.format(i - 1))
                        for ancien_bilan in ancien_bilan_cursor:
                            result.execute('UPDATE output SET bilan={} WHERE debut={}'
                                .format(
                                round(entree[0] + sortie[0] + ancien_bilan[0], 2), i
                            ))
            i += 1

    def showResults(self):
        """
        :param: none
        :return: return the content of the table result as a list and print it as a table
        """
        results = []
        for each_result in result.execute('SELECT * FROM output'):
            results += [each_result]
            print(each_result)
        return results

    def showTheoricalVolume(self, besoin_journalier):
        entree_cursor = result.execute('SELECT MAX(entree) FROM output')
        sortie_cursor = result.execute('SELECT MIN(sortie) FROM output')
        for max_entree in entree_cursor:
            for min_sortie in sortie_cursor:
                return round(((max_entree[0] + abs(min_sortie[0])) * besoin_journalier)/100, 2)

obj = Calculations()

obj.createTableOutput()

obj.insertReceivedData()

obj.calculations()

obj.showResults()

print('Volume théorique ->', obj.showTheoricalVolume(50000))

result.commit()

resultCursor.close()