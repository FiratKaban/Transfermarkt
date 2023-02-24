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
    
    try:
      player_agent_url = soup.find_all('span', class_='info-table__content--flex')
      print(player_agent_url[0].find('a')['href'])
    except:
      pass
    
    text = soup.find_all('span', class_='info-table__content')
    x = 0
    for i in range(len(text)):
      
      try:
        place_of_birth_text = re.search('Place', text[i].text).start()
        place_of_birth_text = text[x+1].text
        first_alpha = re.search('[a-zA-Z0-9]', place_of_birth_text).start()
        last_alpha = re.search('[a-zA-Z0-9]', place_of_birth_text[::-1]).start()
        place_of_birth_text = place_of_birth_text[first_alpha:len(place_of_birth_text)-last_alpha]
        print(place_of_birth_text)
      except:
        pass
      
      try:
        place_of_birth_text = re.search('Player agent', text[i].text).start()
        place_of_birth_text = text[x+1].text
        first_alpha = re.search('[a-zA-Z0-9]', place_of_birth_text).start()
        last_alpha = re.search('[a-zA-Z0-9]', place_of_birth_text[::-1]).start()
        place_of_birth_text = place_of_birth_text[first_alpha:len(place_of_birth_text)-last_alpha]
        print(place_of_birth_text)
      except:
        pass
      
      try:
        contract_expires_text = re.search('Contract expires', text[i].text).start()
        contract_expires_text = text[x+1].text
        first_alpha = re.search('[a-zA-Z0-9]', contract_expires_text).start()
        last_alpha = re.search('[a-zA-Z0-9]', contract_expires_text[::-1]).start()
        contract_expires_text = contract_expires_text[first_alpha:len(contract_expires_text)-last_alpha]
        print(contract_expires_text)
      except:
        pass
      
      x += 1
        

    '''
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
		'''

      
      # //*[@id="main"]/main/div[3]/div[1]/div[2]/div/div[2]/div/span[6]/span/text()
  



if __name__ == "__main__":
            # get_league_pagination(main_url)
            # get_league_links(pagination)
            get_seasons()
            
            