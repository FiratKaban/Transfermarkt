# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 19:56:13 2023

@author: W10
"""

import requests
from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np
import csv
import pandas as pd
import time 
import random
from requests import get
from parsel   import Selector
import time



### WEB CRAWLİNG #####
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
pagination = []  
for pages in range(1,19):
    url='https://www.transfermarkt.co.uk/wettbewerbe/europa?page='
    page = url+str(pages)
    pagination.append(page)




leagues=[]
for league in range(len(pagination)):
    tree = requests.get(pagination[league], headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')
    print(f'TUBİTAK 2209-A; {pagination[league]}')
    rows = soup.select("tr.odd, tr.even")
    for row in rows:
        leagues.append(row.select("a")[1]["href"])
        
for head_link in range(len(leagues)):
       leagues[head_link] = "https://www.transfermarkt.co.uk"+ leagues[head_link]

https://www.transfermarkt.co.uk/wettbewerbe/europa
https://www.transfermarkt.co.uk/wettbewerbe/europa?ajax=yw1&page=1-18
https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1
https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2021

season=[]
link=[]
for all_leagues in range(len(leagues)):
    tree = requests.get(leagues[all_leagues], headers = headers)
    secici = Selector(tree.text)
    print(f'TUBİTAK 2209-A; {leagues[all_leagues]}')
    for seasons in secici.xpath("//select[@data-placeholder='Filter by season']/option"):
        season.append(seasons.xpath('./@value').get())
        link.append(seasons.xpath('//*[@id="subnavi"]/@data-path').get())



string1 = "https://www.transfermarkt.co.uk/"
string2 = "?saison_id="



url_season_list = []
for x, y in zip(link,season):
    url = string1 + x + string2 + y
    url_season_list.append(url)
print(url_season_list)


url_deneme = [url_season_list[0],url_season_list[1]]


country=[]
leaguelevel=[]
reigningchampion=[]
recordholdingchampions=[]
recordholdingchampionsvalue=[]
uefa_coefficient=[]
uefa_coefficient_points =[]
league_title=[]


number_of_teams=[]
number_of_player=[]
number_of_foreign_players=[]
average_market_value=[]
average_age_value =[]
most_valuable_player_price=[]



for all_season in range(len(url_deneme)):
    tree = requests.get(url_deneme[all_season], headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')    
    print(f'TUBİTAK 2209-A; {url_deneme[all_season]}')
    for allseason in soup.select("div.data-header__club-info"):
     #Ülke Adları alındı.
        country_name = allseason.find("span",attrs={'class':'data-header__club'})
        if country_name is not None:
            countryname = country.append(country_name.text.strip())
        else:
            countryname = country.append('NaN')
        #Lig Seviyesi alındı.
        league_level_name = allseason.find("span",attrs={'class':'data-header__content'})
        
        if league_level_name is not None:
             league_level= leaguelevel.append(league_level_name.text.strip())
        else:
             league_level= leaguelevel.append('NaN')    
#########################################################################################################
        
        #Alınan ligin son şampiyon takımı alındı.
                   
        reigning_champion_name = allseason.findAll("span",attrs={'class':'data-header__content'})
        if reigning_champion_name is not None:
            reigning_champion= reigningchampion.append(reigning_champion_name[1].text.strip())
        else:
            reigning_champion= reigningchampion.append('NaN') 
      
########################################################################################################   
                
        #En fazla şampiyonluğa sahip olan takım elde edildi.
                                       
        record_holding_champion_name = allseason.findAll("span",attrs={'class':'data-header__content'})
        if record_holding_champion_name is not None:
               record_champion= recordholdingchampions.append(record_holding_champion_name[2].a.get_text())
        else:
               record_champion= recordholdingchampions.append('NaN')
      
########################################################################################################        

        #En fazla şampiyonluğa sahip olan takımın ne kadar şampiyonluğa 
        #ulaştığı elde edildi.
                                      
        record_holding_champion_value = allseason.findAll("span",attrs={'class':'data-header__content'})
        if record_holding_champion_value is not None:
               record_champion_value= recordholdingchampionsvalue.append(record_holding_champion_value[3].get_text(strip=True))
        else:
               record_champion_value= recordholdingchampionsvalue.append('NaN')

##########################################################################################################
        
        #Ülkenin ülke  sıralaması
        uefa_coefficient_arrangement = allseason.findAll("span",attrs={'class':'data-header__content'})
        if uefa_coefficient_arrangement is not None:
            uefa_arrangement= uefa_coefficient.append(uefa_coefficient_arrangement[5].a.get_text(strip=True))
        else:
            uefa_arrangement= uefa_coefficient.append('NaN')

##############################################################################################
        uefa_coefficient_arrangement_points = allseason.findAll("span",attrs={'class':'data-header__content'})
        if uefa_coefficient_arrangement_points is not None:
            uefa_arrangement_point= uefa_coefficient_points.append(uefa_coefficient_arrangement_points[6].get_text(strip=True))
        else:
            uefa_arrangement_point= uefa_coefficient_points.append('NaN')
###########################################################################################################            
    for leaguename in soup.select("div.data-header__headline-container"):
        league_name = leaguename.find("h1",attrs={'class':'data-header__headline-wrapper data-header__headline-wrapper--oswald'})
        if league_name is not None:
            league_name_text= league_title.append(league_name.get_text(strip=True))
        else:
            league_name_text= league_title.append('NaN')
################################################################################################################ 

teams_name=[]
teams_link=[]
teams_squad=[]
teams_average_age=[]

for league_detail_data in range(len(url_deneme)):
    tree = requests.get(url_deneme[league_detail_data], headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')
    print(f'TUBİTAK 2209-A; {url_deneme[league_detail_data]}')
    for detail_data in soup.select('tr.odd,tr.even'):
        team = detail_data.find('td',{'class':'hauptlink no-border-links'})
        if team is not None:
            takim = teams_name.append(team.get_text(strip=True))
        else:
            takim = teams_name.append('NaN')
        teamlink = detail_data.find('td', {'class':'hauptlink no-border-links'})
        if teamlink is not None:
              takimlinki =  teams_link.append(teamlink.select('a')[0]['href'])
        else:
              takımlinki =  teams_link.append('NaN')
        
        squad=detail_data.find('td',{'class':'zentriert'})
        if squad is not None:
            kadro = teams_squad.append(squad.text(strip=True))
        else:
            kadro=teams_squad.append('NaN')
        
for team_all_link in range(len(teams_link)):
      teams_link[team_all_link] = "https://www.transfermarkt.co.uk"+ team_all_link[teams_link]
            
#####################Lig sezonunda yer alan takımların adları ve linkleri alındı.##################################            

            
           

       
        

    
