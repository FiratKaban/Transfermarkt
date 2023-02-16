from collections import namedtuple
import sys
from bs4 import BeautifulSoup       # bs4 kütüphanesini import ediyoruz
import requests                     # requests kütüphanesini import ediyoruz
from requests import Session        # 
import time, csv


def represent_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def represent_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/45.0.2454.101 Safari/537.36')}    

teams={} 
deneme1=[]
deneme2=[]
deneme3=[]
deneme4=[]
deneme5=[]
deneme6=[]
deneme7=[]
deneme8=[]

def get_seasons():
    """ test mode """
    # https://www.transfermarkt.co.uk/manchester-city/startseite/verein/281/saison_id/2022
    response = requests.get('https://www.transfermarkt.co.uk/manchester-city/startseite/verein/281/saison_id/2022', headers=HEADERS)  
    soup = BeautifulSoup(response.content, 'html.parser')
    data =soup.select("table.items")
    
    for allseason in soup.select("div.data-header__club-info"):
         league = allseason.find("span",attrs={'class':'data-header__club'})
         country = allseason.find("span",attrs={'class':'data-header__content'})
         league_level = allseason.find("span",attrs={'class':'data-header__content'})
         tableposition= allseason.findAll("span",attrs={'class':'data-header__content'})[1]
         In_leaguesince= allseason.findAll("span",attrs={'class':'data-header__content'})[2]
         
    try:
            teams['league'] = league.a.get_text(strip=True)
            teams['team_country'] =  country.find('img')['alt']
            teams['league_level'] = league_level.a.get_text(strip=True)
            teams['teams_position'] = tableposition.a.get_text(strip=True)
            teams['in_league_since'] = In_leaguesince.a.get_text(strip=True)
            
    except AttributeError:
            teams['league'] = ('AttributeError')
            teams['team_country'] = ('AttributeError')
            teams['league_level'] = ('AttributeError')
            teams['teams_position'] = ('AttributeError')
            teams['in_league_since'] = ('AttributeError')
            
    except IndexError:
           teams['league'] = ('IndexError')
           teams['team_country'] = ('IndexError')
           teams['league_level'] = ('IndexError')
           teams['teams_position']= ('IndexError')
           teams['in_league_since'] =('IndexError')
           
    except Exception as f:
        teams['league']=(f)
        teams['team_country'] = (f)
        teams['league_level'] = (f)
        teams['teams_position']= (f)
        teams['in_league_since'] = (f)  
       
    for allseason1 in soup.select("div.data-header__details"):
       squad1 = allseason1.find("span",attrs={'class':'data-header__content'})
       age1 = allseason1.findAll("span",attrs={'class':'data-header__content'})[1]
       foreigners1= allseason1.findAll("span",attrs={'class':'data-header__content'})[2]
       foreigners_player_percant1= allseason1.findAll("span",attrs={'class':'tabellenplatz'})[0]
       nationality_players= allseason1.findAll("span",attrs={'class':'data-header__content'})[3]

       stadium= allseason1.findAll("span",attrs={'class':'data-header__content'})[4]
       seats= allseason1.findAll("span",attrs={'class':'tabellenplatz'})[1]
       transfer_record= allseason1.findAll("span",attrs={'class':'data-header__content'})[5]
    try:
        
          teams['teams_squad'] = squad1.get_text(strip=True)
          teams['teams_age'] = age1.get_text(strip=True)
          teams['teams_foreigner_players'] = foreigners1.a.get_text(strip=True)
          teams['teams_foreigner_players_percant'] = foreigners_player_percant1.get_text(strip=True)
          teams['teams_national'] = nationality_players.a.get_text(strip=True)
          teams['teams_stadium_name'] = stadium.a.get_text(strip=True)
          teams['teams_stadium_seats'] = seats.get_text(strip=True)
          teams['teams_transfer_record'] = transfer_record.a.get_text(strip=True)
          
    except AttributeError:
          teams['teams_squad'] = ('AttributeError')
          teams['teams_age']  = ('AttributeError')
          teams['teams_foreigner_players'] = ('AttributeError')
          teams['teams_foreigner_players_percant'] =('AttributeError')
          teams['teams_national'] = ('AttributeError')
          teams['teams_stadium_name'] = ('AttributeError')
          teams['teams_stadium_seats'] = ('AttributeError')
          teams['teams_transfer_record'] = ('AttributeError')
          
    except IndexError:
        teams['teams_squad'] = ('IndexError')
        teams['teams_age']  = ('IndexError')
        teams['teams_foreigner_players'] = ('IndexError')
        teams['teams_foreigner_players_percant'] = ('IndexError')
        teams['teams_national'] = ('IndexError')
        teams['teams_stadium_name'] = ('IndexError')
        teams['teams_stadium_seats'] = ('IndexError')
        teams['teams_transfer_record'] = ('IndexError')
        
    except Exception as f:
        teams['teams_squad'] = (f)
        teams['teams_age']  = (f)
        teams['teams_foreigner_players'] = (f)
        teams['teams_foreigner_players_percant'] = (f)
        teams['teams_national'] = (f)
        teams['teams_stadium_name'] = (f)
        teams['teams_stadium_seats'] = (f)
        teams['teams_transfer_record'] = (f)
        
    """
    data = soup.select("table.items")    
    for allplayers in soup.select("tr.odd,tr.even"):
          tshirt_number = allplayers.find("td",attrs={'class':'zentriert'})
          main_position = allplayers.find("td",attrs={'class':'zentriert'})
          player_name = allplayers.find("span",attrs={'class':'hide-for-small'})
          date_of_birth= allplayers.findAll("td",attrs={'class':'zentriert'})
          nat1= allplayers.findAll("td",attrs={'class':'zentriert'})[1]
          nat2= allplayers.findAll("td",attrs={'class':'zentriert'})[1]
          
    try:
             teams['tshirt_number'] =tshirt_number.get_text(strip=True)
             teams['main_position'] =main_position.find['title']
             teams['player_name'] =player_name.a.get_text(strip=True)
             teams['date_of_birth'] =date_of_birth.get_text(strip=True)
             teams['nat1'] = nat1.find['img']['alt'][0]
             teams['nat2'] = nat2.find['img']['alt'][1]
             
    except AttributeError:
             teams['tshirt_number']= ('AttributeError')
             teams['main_position'] =('AttributeError')
             teams['player_name'] = ('AttributeError')
             teams['date_of_birth'] = ('AttributeError')
             teams['nat1'] =  ('AttributeError')
             teams['nat2'] =  ('AttributeError')
             
    except IndexError:
            teams['tshirt_number'] = ('IndexError')
            teams['main_position'] =('IndexError')
            teams['player_name'] = ('IndexError')
            teams['date_of_birth'] =('IndexError')
            teams['nat1'] = ('IndexError')
            teams['nat2'] =  ('AttributeError')
            
    except Exception as f:
         teams['tshirt_number']=(f)
         teams['main_position'] = (f)
         teams['player_name'] =(f)
         teams['date_of_birth'] =(f)
         teams['nat1'] =  (f)  
         teams['nat2'] =  (f)
  """


    num_of_teams = 0
    for player_data in soup.select('tr.odd,tr.even'):
        player = player_data.find('span',{'class':'show-for-small'})
        if player is not None:
            player = deneme1.append(player.get_text(strip=True))

        playerlink = player_data.find('span', {'class':'show-for-small'})
        if playerlink is not None:
           player_link    =  deneme2.append(playerlink.select('a')[0]['href'])
        ++num_of_teams
    
        squad = player_data.findAll('td')[0].get_text() #Forma Numarası
        if squad != '' and squad is not None:
            squad = deneme3.append(squad)
             
        team_age = player_data.findAll('td')[4].get_text()
        if team_age != '' and team_age is not None:
            team_age = deneme4.append(team_age)
                    
        t_avg_market_value = player_data.findAll('td',attrs={'class':'zentriert'})[1].get_text()
        if t_avg_market_value != '' and t_avg_market_value is not None:
            t_avg_market_value = deneme5.append(t_avg_market_value[:12]) #doğum  günü ve yılı
            
        t_avg_market_value1 = player_data.findAll('td',attrs={'class':'zentriert'})[1].get_text(strip=True)
        if t_avg_market_value1 != '' and t_avg_market_value1 is not None:
            t_avg_market_value1 = deneme6.append(t_avg_market_value1[11:16]) #yaş datası
            
        t_avg_market_value2 = player_data.findAll('td',attrs={'class':'zentriert'})[1].get_text(strip=True)
        if t_avg_market_value2 != '' and t_avg_market_value2 is not None:
           t_avg_market_value2 = deneme7.append(t_avg_market_value2[7:12]) #Doğum Tarihi
           
            
    
           
################################################################################################### 
if __name__ == "__main__":
    # get_league_pagination(main_url)
    # get_league_links(pagination)
    get_seasons()
    # print all lists
    print(teams)
    print(deneme1)
    print(deneme2)
    print(deneme3)
    print(deneme4)
    print(deneme5)
    print(deneme6)
    print(deneme7)