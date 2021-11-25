from bs4 import BeautifulSoup
import urllib.request
import csv
import pyarrow.parquet as pq
import pandas as pd
import numpy as np
import json
import random

def getInfosChampion():

    # specify the url
    urlpage = 'https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position'

    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # var def
    data = []


    # find results within table
    table = soup.find("table",{"class":"article-table"})
    items_tr = table.find_all('tr')
    
    
    for j, item in enumerate(items_tr[1:]):
        champ = {}
        roles = []
        items_td = item.find_all('td')
        champion = items_td[0].get_text()
        champion = champion.replace("\n", "").replace(" ", "")
        

        for i, item in enumerate(items_td):

            if i==1 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                roles.append("top")
            if i==2 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                roles.append("jungle")
            if i==3 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                roles.append("mid")
            if i==4 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                roles.append("bot")
            if i==5 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                roles.append("support")

        champ = {"id":j, "name":champion, "roles":roles}
        data.append(champ)

 
    """with open("LoLChampions.json", "w") as file:
        json.dump(data, file)"""


    #id(136) Vex : elle n'a pas de rôle, il faudra rtemplir à la main son rôle
    #Mais une condition est toutefois utilisé pour éviter un soucis en cas d'oubli dans le renseignement des rôles d'un personnage
    selectID = random.randint(0,len(data)-1)
    selectName = data[selectID]["name"]
    selectRoles = data[selectID]["roles"]
    selectRole = ""
    if len(selectRoles) != 0:
        selectRole = selectRoles[random.randint(0, len(selectRoles)-1)]
        print("Vous devez jouer avec "+ selectName + " avec le rôle " + selectRole)

    else:
        print("Aucun rôle n'est encore attribué à " + selectName)

def getChampionsRoles():

    # specify the url
    urlpage = 'https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position'

    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    # var def
    top = []
    jungle = []
    mid = []
    adc = []
    support = []

    # find results within table
    table = soup.find("table",{"class":"article-table"})
    items_tr = table.find_all('tr')
    
    
    for j, item in enumerate(items_tr[1:]):
        champ = {}
        
        items_td = item.find_all('td')
        champion = items_td[0].get_text()
        champion = champion.replace("\n", "").replace(" ", "")
        

        for i, item in enumerate(items_td):

            if i==1 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                #roles.append("TOP")
                top.append(champion)
            if i==2 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                #roles.append("JUNGLE")
                jungle.append(champion)
            if i==3 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                #roles.append("MIDDLE")
                mid.append(champion)
            if i==4 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                #roles.append("ADC")
                adc.append(champion)
            if i==5 and (item.getText().replace("\n", "")=="OP" or item.span is not None):
                #roles.append("SUPPORT")
                support.append(champion)

        #champ = {"id":j, "name":champion, "roles":roles}
        #data.append(champ)
    champ = {"TOP":top, "JUNGLE":jungle, "MIDDLE":mid, "ADC":adc, "SUPPORT":support}
    #print(champ)

 
    """with open("LoLChampionsByRoles.json", "w") as file:
        json.dump(champ, file)"""


    #id(136) Vex : elle n'a pas de rôle, il faudra rtemplir à la main son rôle
    #Mais une condition est toutefois utilisé pour éviter un soucis en cas d'oubli dans le renseignement des rôles d'un personnage
    champList = random.choice(champ["TOP"])
    print(champList)
    """selectID = random.randint(0,len(data)-1)
    selectName = data[selectID]["name"]
    selectRoles = data[selectID]["roles"]
    selectRole = ""
    if len(selectRoles) != 0:
        selectRole = selectRoles[random.randint(0, len(selectRoles)-1)]
        print("Vous devez jouer avec "+ selectName + " avec le rôle " + selectRole)

    else:
        print("Aucun rôle n'est encore attribué à " + selectName)"""





#getInfosChampion()

getChampionsRoles()