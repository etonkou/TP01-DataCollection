
# -----------  EXERCICE 2 ------------------------------ #
# URL: http://www.floatrates.com/feeds.html
# 2. Ecrire un script python:
# 	- récupérer les converstions de devises
# 	- afin d'ajouter à la liste de la question 1.
# 		- la convertion selon 6 devises de votre choix
# 		- puis convertir ces données en fichier EXCEL/CSV
# -------------------------------------------------------- #

from lib.utils import Utils
import pandas as pd
from lib.scrap import Webscrap

URL_main = 'http://www.floatrates.com/feeds.html'
URL = 'http://www.floatrates.com/daily/xof.xml'


if __name__ == '__main__':
    print(Utils.divider())
    print(Webscrap.main2())
