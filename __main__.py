import argparse as ap
from os import system as syst
from os import path

from aep.dataQuery import *
from aep.calculations import *

parser = ap.ArgumentParser(description="Programme d'aide au calcul de données d'adduction en"
                                       " eau potable et de création des diagrammes relatifs."
                                       " Retrouvez des informations plus completes et détaillées"
                                       "sur la page github du programme disponible a l'adresse"
                                       "https://github.com/atepir/aep")
parser.add_argument('-v', help='Le mode verbeux permet de voir les données calculatoires '
                                      'telles que le volume théorique, le volume total, le diamètre'
                                      'ou encore la hauteur. Il prend en argument le '
                               'besoin en eau journalier', default=50000, type=int)
parser.add_argument('-i', help='Nom du diagramme a sa sortie', default='sortie.png')
parser.add_argument('-d', help='Base de donnée locale Sqlite3 pour stoquer les données entrées, '
                               'par defaut -> data.db',
                    default='data.db')
parser.add_argument('-s', help='Base de donnée locale Sqlite3 de sortie des résultats de calcul, '
                               'par defaut -> result.db',
                    default='result.db')
parser.add_argument('-c', help='Fichier csv contenant les données de consommation')
parser.add_argument('-p', help='Fichier csv contenant les données des paliers')
parser.add_argument('-o', help='Nom de sortie de la feuille de style excel,'
                               ' par defaut -> output.xls', default='output.xls')
args = parser.parse_args()

if __name__ == '__main__':
    if path.exists(args.d):
        syst(f"del {args.d}")
    if path.exists(args.s):
        syst(f"del {args.s}")
    obj1 = DataQuery(args.d)
    obj2 = Calculations(args.d, args.s, args.i)
    obj1.createTableConso()
    obj1.insertConso(DataQuery(args.d).getData(args.c))
    obj1.createTablePaliers()
    obj1.insertPaliers(DataQuery(args.d).getData(args.p))
    obj1.data.commit()
    obj1.dataCursor.close()
    obj2.createTableOutput()
    obj2.insertReceivedData()
    obj2.calculations()
    obj2.result.commit()
    obj2.showResults()
    obj2.saveOutput(args.o)
    if args.v:
        print('Volume théorique ->', obj2.showTheoricalVolume(args.v))
        print('Volume total ->', obj2.showTotalVolume(args.v))
        print('Le quart du volume total ->', obj2.showTotalVolumeQuarter(args.v))
        print('Diametre ->', obj2.showDiameter(args.v))
        print('Hauteur ->', obj2.showHeight(args.v))
    obj2.drawFigure()