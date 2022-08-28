from .utils import Utils
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

URL = 'https://www.fabellashop.com/categorie-produit/maquillageongles/teint/'
URL2 = 'http://www.floatrates.com/daily/eur.xml'
#URL2 = 'http://www.floatrates.com/feeds.html'

class Webscrap(object):
    @classmethod
    def httpFetcher(cls, URL=URL):
        with requests.Session() as session:
            result = session.get(URL)
            result = result.text
            return result

    @classmethod
    def scrapLink(cls, URL=URL):
        return cls.httpFetcher(URL)

    @classmethod
    def souper(cls, URL=URL):
        result = cls.scrapLink(URL)
        #return BeautifulSoup(result, 'lxml')
        return BeautifulSoup(result,'html.parser')

    @classmethod
    def getProd(cls,URL=URL):
        produit = cls.souper(URL).find_all("div", {"class" : "title-wrapper"})
        prodTitleList = []
        for x in produit :
            prodTitle = x.find('a')
            dictProd = {'title': prodTitle.text}
            if prodTitle :
                prodTitleList.append(dictProd)
            continue
        return prodTitleList

    @classmethod
    def getProdPrice(cls,URL=URL):
        produit = cls.souper(URL).find_all("div", {"class" : "price-wrapper"})
        prodPriceList = []
        for x in produit :
            prodPrice = x.find("span",{"class" : "woocommerce-Price-amount amount"})
            if prodPrice :
                prix = re.findall("\d+\.\d+", prodPrice.text)  # format le text en filtrant uniquement des chiffres + le point
                prix = prix[0].replace(".","")  # remplace le point dans le price par un caractere vide
                dictProd = {'price': int(prix)}
                prodPriceList.append(dictProd)
            continue
        return prodPriceList

    # Construction du dictionnaire a l'aide des elts de 2 lists LibelleProduit et PrixProduit
    @classmethod
    def mergeDict(cls, URL=URL):
        titre = cls.getProd(URL)
        prix = cls.getProdPrice(URL)
        result = list(map(lambda titre, prix: {**titre,**prix}, titre, prix))
        return result

    # Ajout des clef 'quantity' & 'currency'
    @classmethod
    def addKeys(cls, data):
        i = 0
        for _ in data:
            data[i]['quantity'] = 1
            data[i]['currency'] = 'XOF/CFA'
            i = i + 1
        return data

    @classmethod
    def listProduits(cls, data):
        #print(data[0]['title'])
        #print(data[0]['price'])
        produits = []
        prix = []
        i = 0
        for _ in data:
            produits.append(data[i]['title'])
            prix.append(data[i]['price'])
            #print(prix)
            i = i+1

        columns = ['Product Name', 'Price']
        # Create DataFrame from multiple lists
        df = pd.DataFrame(list(zip(produits, prix)), columns=columns)
        return df


    @classmethod
    def main(cls):
        data = cls.souper()
        data = cls.getProd()
        data = cls.getProdPrice()
        data = cls.mergeDict()
        data = cls.addKeys(data)
        #print(data.prettify())
        data = cls.listProduits(data)
        print(data)
#----------------- Exercice n_2 --------------------------------------------------------------------------
    # Recupere la liste ds libelles des Devices target
    @classmethod
    def getExchange(cls,URL=URL2):
        itemCurrency = cls.souper(URL).find_all("item")
        #print(itemCurrency)
        itemCurrencyName = []
        for x in itemCurrency :
            targetname = x.find('targetname')
            dictTargetName = {'targetname': targetname.text}
            if dictTargetName :
                itemCurrencyName.append(dictTargetName)
            continue
        return itemCurrencyName

    # Recupere la liste des Rate des Devises target
    @classmethod
    def getExchangeRate(cls,URL=URL2):
        ExchangeRate= cls.souper(URL).find_all("item")
        #print(itemCurrency)
        itemExchangeRate = []
        for x in ExchangeRate :
            targetRate = x.find('exchangerate')
            dictTargetRate = {'exchangerate': targetRate.text}
            if dictTargetRate :
                itemExchangeRate.append(dictTargetRate)
            continue
        return itemExchangeRate

    # Recupere la liste des codes des Devises target
    @classmethod
    def getExchangeCode(cls,URL=URL2):
        ExchangeCode= cls.souper(URL).find_all("item")
        itemExchangeCode = []
        for x in ExchangeCode :
            targetCode = x.find('targetcurrency')
            dictTargetCode = {'targetcurrency': targetCode.text}
            if dictTargetCode :
                itemExchangeCode.append(dictTargetCode)
            continue
        return itemExchangeCode

    # Construit un dictionnaire
    @classmethod
    def mergeDictExchange(cls, URL=URL2):
        codeTargetExchange = cls.getExchangeCode(URL)
        rateExchange = cls.getExchangeRate(URL)
        result = list(map(lambda codeTargetExchange, rateExchange: {**codeTargetExchange,**rateExchange}, \
                          codeTargetExchange, rateExchange))
        return result

    # ajoute la cle baseExchange
    @classmethod
    def addKeysExchange(cls, data):
        i = 0
        for _ in data:
            data[i]['baseExchange'] = 'Euro'
            i = i + 1
        return data

    @classmethod
    def listExchange(cls, data):
        i = 0
        currencies = []
        rate = []
        # baseExchange = "'baseExchange': 'Euro'"
        for _ in data:
            currencies.append(data[i]['targetcurrency'])
            rate.append(float(data[i]['exchangerate'].replace(",","")))
            i = i + 1
        return currencies, rate

    # Affiche les donnees
    @classmethod
    def afficheExchange(cls,data):
        # Create multiple lists
        currencies = data[0]
        rates = data[1]
        columns = ['Currency', 'Rate']
        # Create DataFrame from multiple lists
        df = pd.DataFrame(list(zip(currencies, rates)), columns=columns)

        # Write DataFrame to Excel file with sheet name
        # df.to_excel('ExchangeRate.xlsx', sheet_name='RateForEuro')
        #df.to_excel('ExchangeRate.xlsx')
        df.to_csv("./ExchangeRate.csv")
        return df

    @classmethod
    def main2(cls):
        data = cls.souper(URL2)
        data = cls.getExchange()
        data = cls.getExchangeRate()
        data = cls.getExchangeCode()
        data = cls.mergeDictExchange()
        data = cls.addKeysExchange(data)
        data = cls.listExchange(data)
        data = cls.afficheExchange(data)
        print('*** Foreign Exchange Rates for Euro (EUR) ***')
        print(data)
