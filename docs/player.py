# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 12:22:16 2023

@author: W10
"""
from collections import namedtuple
import sys
from bs4 import BeautifulSoup       # bs4 kütüphanesini import ediyoruz
import requests                     # requests kütüphanesini import ediyoruz
from requests import Session        # 
import time, csv

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/45.0.2454.101 Safari/537.36')}    

place_of_birth=[]
manager_company=[]
expires=[]
player_outfitter=[]
player_rrss=[]

def get_seasons():
    """ test mode """
    # https://www.transfermarkt.co.uk/manchester-city/startseite/verein/281/saison_id/2022
    response = requests.get('https://www.transfermarkt.co.uk/erling-haaland/profil/spieler/418560', headers=HEADERS) 

    soup = BeautifulSoup(response.content, 'html.parser')
    etiket=soup.find_all('span',class_='info-table__content info-table__content--regular')
    deger=soup.find_all('span',class_='info-table__content info-table__content--bold')

    for allseason in soup.select("div.info-table info-table--right-space"):
        #lig kodunu split yapıp sözlüğe yazdıracaz.
        rrss=outfitter=contract_expires=manager=place=False
        if (etiket.text.find('Place of birth:')!=-1):
           place_of_birth.append(etiket.text.replace('\n','').replace('\xa0',''))
           place=True
        elif (etiket.text.find('Player agent:')!=-1):
            manager_company.append(etiket.text.replace('\n','').replace('\xa0',''))
            manager=True
        elif (etiket.text.find('Contract expires:')!=-1):
            expires.append(etiket.text.replace('\n','').replace('\xa0',''))
            contract_expires=True
        elif (etiket.text.find('Outfitter:')!=-1):
            player_outfitter.append(etiket.text.replace('\n','').replace(' ',''))
            outfitter=True
        elif (etiket.text.find('Social-Media:')!=-1):
            player_rrss.append(etiket.find_all('a')[0]['href'])
            rrss=True



        if(place==False):
            place_of_birth.append(' ')
        if(manager==False):
            manager_company.append(' ')
        if(contract_expires==False):
            expires.append(' ')
        if(outfitter==False):
            player_outfitter.append(' ')
        if(rrss==False):
           player_rrss.append(' ')


if __name__ == "__main__":
            # get_league_pagination(main_url)
            # get_league_links(pagination)
            get_seasons()
            # print all lists
            print(place_of_birth)
            print(manager_company)
            print(expires)
            print(player_outfitter)
            print(player_rrss)