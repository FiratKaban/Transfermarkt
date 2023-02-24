# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 12:22:16 2023

@author: W10
"""
from collections import namedtuple
import re
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
    response = requests.get(
        'https://www.transfermarkt.co.uk/erling-haaland/profil/spieler/418560', headers=HEADERS)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # social media urls
		# div class="socialmedia-icons" href
    try:
      data = soup.find_all('div', class_='socialmedia-icons')
      for a in data[0].find_all('a'):
        social_media_url = a.get('href')
        print(social_media_url)
        # TODO: degiskenin adini kullanarak db'de ilgili sutuna yazdirabilirsin
    except:
      pass
 
    try:
      player_agent_url = soup.find_all('span', class_='info-table__content--flex')
      player_agent_url = player_agent_url[0].find('a')['href']
      print(player_agent_url)
      # TODO: degiskenin adini kullanarak db'de ilgili sutuna yazdirabilirsin
    except:
      pass
    
    text = soup.find_all('span', class_='info-table__content')
    x = 0
    for i in range(len(text)):
      
      try:
        # sadece index varmi kontrolu icin re.search place 
        place_of_birth_text = re.search('Place', text[i].text).start()
        place_of_birth_text = text[x+1].text
        first_alpha = re.search('[a-zA-Z0-9]', place_of_birth_text).start()
        last_alpha = re.search('[a-zA-Z0-9]', place_of_birth_text[::-1]).start()
        place_of_birth_text = place_of_birth_text[first_alpha:len(place_of_birth_text)-last_alpha]
        print(place_of_birth_text)
        # TODO: degiskenin adini kullanarak db'de ilgili sutuna yazdirabilirsin
      except:
        pass
      
      try:
        place_of_birth_text = re.search('Player agent', text[i].text).start()
        place_of_birth_text = text[x+1].text
        first_alpha = re.search('[a-zA-Z0-9]', place_of_birth_text).start()
        last_alpha = re.search('[a-zA-Z0-9]', place_of_birth_text[::-1]).start()
        place_of_birth_text = place_of_birth_text[first_alpha:len(place_of_birth_text)-last_alpha]
        print(place_of_birth_text)
        # TODO: degiskenin adini kullanarak db'de ilgili sutuna yazdirabilirsin
      except:
        pass
      
      try:
        contract_expires_text = re.search('Contract expires', text[i].text).start()
        contract_expires_text = text[x+1].text
        first_alpha = re.search('[a-zA-Z0-9]', contract_expires_text).start()
        last_alpha = re.search('[a-zA-Z0-9]', contract_expires_text[::-1]).start()
        contract_expires_text = contract_expires_text[first_alpha:len(contract_expires_text)-last_alpha]
        print(contract_expires_text)
        # TODO: degiskenin adini kullanarak db'de ilgili sutuna yazdirabilirsin
      except:
        pass
      
      try:
        outfitter_text = re.search('Outfitter', text[i].text).start()
        outfitter_text = text[x+1].text
        first_alpha = re.search('[a-zA-Z0-9]', outfitter_text).start()
        last_alpha = re.search('[a-zA-Z0-9]', outfitter_text[::-1]).start()
        outfitter_text = outfitter_text[first_alpha:len(outfitter_text)-last_alpha]
        print(outfitter_text)
        # TODO: degiskenin adini kullanarak db'de ilgili sutuna yazdirabilirsin
      except:
        pass
      
      x += 1


if __name__ == "__main__":
            # get_league_pagination(main_url)
            # get_league_links(pagination)
            get_seasons()