
# ----------- EXERCICE ------------------ #
# 1. Ecrire un script python:
# 	- pour récupérer la liste des produits
# 	- le format est le suivant:
# 		- title: nom du produit
# 		- price: prix du produit
# 		- quantity: 1
# 		- currency: XOF/CFA
# ----------------------------------------- #

from lib.utils import Utils
from lib.scrap import Webscrap

if __name__ == '__main__':
    print(Utils.divider())
    print(Webscrap.main())