import sqlite3
from aep.dataQuery import DataQuery
import matplotlib.pyplot as plot
import numpy as np
from xlwt import Workbook

class Calculations:
    def __init__(self, database, result, diagram):
        """
        :info: calculator class
        """
        self.database = database
        self.result = sqlite3.connect(result)
        self.resultCursor = self.result.cursor()
        self.diagram = diagram

    def createTableOutput(self):
        """
        :param: none
        :return: creates table output with 7 columns
        """
        self.result.execute('CREATE TABLE output(debut int, fin int, conso_totale float, debit float, '
                       'entree float, sortie float, bilan float)')

    def insertReceivedData(self):
        """
        :param: none
        :return: inserts into output the received data
        """
        for elem in DataQuery(self.database).showConso():
            self.result.execute('INSERT INTO output(debut, fin, conso_totale, debit) VALUES ({}, {}, {}, {})'
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
        while i < len(DataQuery(self.database).showConso()):
            conso_totale_cursor = self.result.execute('SELECT conso_totale FROM output WHERE debut={}'.format(i))
            debit_de_pompage_cursor = self.result.execute('SELECT debit FROM output WHERE debut={}'.format(i))
            for conso_totale in conso_totale_cursor:
                for debit_de_pompage in debit_de_pompage_cursor:
                    if debit_de_pompage[0] - conso_totale[0] > 0:
                        self.result.execute('UPDATE output SET entree={} WHERE debut={}'
                                       .format(round(debit_de_pompage[0] - conso_totale[0], 2), i))
                        self.result.execute('UPDATE output SET sortie=0 WHERE debut={}'
                                       .format(i))
                    else:
                        self.result.execute('UPDATE output SET sortie={} WHERE debut={}'
                                       .format(round(debit_de_pompage[0] - conso_totale[0], 2), i))
                        self.result.execute('UPDATE output SET entree=0 WHERE debut={}'
                                       .format(i))

            entree_cursor = self.result.execute('SELECT entree FROM output WHERE debut={}'.format(i))
            sortie_cursor = self.result.execute('SELECT sortie FROM output WHERE debut={}'.format(i))
            for entree in entree_cursor:
                for sortie in sortie_cursor:
                    if i == 0:
                        self.result.execute('UPDATE output SET bilan={} WHERE debut={}'
                                       .format(
                            round(entree[0] + sortie[0], 2), i
                        ))
                    if i > 0 :
                        ancien_bilan_cursor = self.result.execute('SELECT bilan FROM output WHERE debut={}'.format(i - 1))
                        for ancien_bilan in ancien_bilan_cursor:
                            self.result.execute('UPDATE output SET bilan={} WHERE debut={}'
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
        for each_result in self.result.execute('SELECT * FROM output'):
            results += [each_result]
            print(each_result)
        return results

    def showTheoricalVolume(self, besoin_journalier):
        entree_cursor = self.result.execute('SELECT MAX(entree) FROM output')
        sortie_cursor = self.result.execute('SELECT MIN(sortie) FROM output')
        for max_entree in entree_cursor:
            for min_sortie in sortie_cursor:
                return round(((max_entree[0] + abs(min_sortie[0])) * besoin_journalier)/100, 2)

    def showTotalVolume(self, besoin_journalier):
        return self.showTheoricalVolume(besoin_journalier) + 0.2 * self.showTheoricalVolume(besoin_journalier)

    def showTotalVolumeQuarter(self, besoin_journalier):
        return (self.showTheoricalVolume(besoin_journalier) + 0.2 * self.showTheoricalVolume(besoin_journalier))/4

    def showDiameter(self, besoin_journalier):
        Vt = self.showTotalVolume(besoin_journalier)
        return ((4*Vt)/(3.14*0.8))**(1/3)

    def showHeight(self, besoin_journalier):
        return self.showDiameter(besoin_journalier) * 0.8

    def saveOutput(self, output):
        book = Workbook()
        feuille = book.add_sheet('feuille 1')

        # En-tete
        feuille.write(0, 0, 'Période (heure début)')
        feuille.write(0, 1, 'Période (heure fin)')
        feuille.write(0, 2, 'Consommation totale (%)')
        feuille.write(0, 3, 'Débit de pompage (%)')
        feuille.write(0, 4, "Entrée d'eau dans la cuve (%)")
        feuille.write(0, 5, "Sortie d'eau de la cuve (%)")
        feuille.write(0, 6, "Bilan d'eau dans la cuve (%)")

        # Remplissage
        for index in range(len(DataQuery(self.database).showConso())):
            ligne = feuille.row(index+1)
            for elem in range(7):
                ligne.write(elem, self.showResults()[index][elem])

        book.save(output)

    def drawFigure(self):
        draw = plot.figure()

        x = ["{}-{}".format(_, _+1) for _ in range(24)]
        height = []
        for elem in self.result.execute('SELECT conso_totale FROM output'):
            height += elem

        width = 0.6

        i = 0
        for debit in self.result.execute('SELECT debit FROM output'):
            plot.axhline(y=debit, color='red', xmin=i, xmax=i+0.04)
            i += 0.04

        ash = plot.axhline(y=0, color='red', xmin=0, xmax=0.04)
        conso = plot.bar(x, height, width, color='b')
        plot.legend((conso, ash), ('consommation totale', 'paliers'))
        plot.savefig(self.diagram)
        plot.show()

"""
obj = Calculations()

obj.createTableOutput()

obj.insertReceivedData()

obj.calculations()

obj.showResults()

print('Volume théorique ->', obj.showTheoricalVolume(50000))

print('Volume total ->', obj.showTotalVolume(50000))

print('Le quart du volume total ->', obj.showTotalVolumeQuarter(50000))

print('Diametre ->', obj.showDiameter(50000))

print('Hauteur ->', obj.showHeight(50000))

obj.drawFigure()

result.commit()

resultCursor.close()
"""
