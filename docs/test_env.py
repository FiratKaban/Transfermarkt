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

# https://www.transfermarkt.co.uk/erling-haaland/profil/spieler/418560



if __name__ == "__main__":
            # get_league_pagination(main_url)
            # get_league_links(pagination)
            get_seasons()
            
            