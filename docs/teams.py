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


def get_seasons():
    """ test mode """
    # https://www.transfermarkt.co.uk/manchester-city/startseite/verein/281/saison_id/2022
    response = requests.get('https://www.transfermarkt.co.uk/manchester-city/kader/verein/281/saison_id/2022/plus/1', headers=HEADERS)  
    soup = BeautifulSoup(response.content, 'html.parser')
    data =soup.select("table.items")
    
    for allseason in soup.select("div.data-header__club-info"):
        #lig kodunu split yapıp sözlüğe yazdıracaz.
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
        #takımın sezonu ve linkini split yapacaz ve sözlüğe yazdıracaz.
       team_name = allseason1.findAll("span",attrs={'class':'data-header__content'})[4]
       squad1 = allseason1.find("span",attrs={'class':'data-header__content'})
       age1 = allseason1.findAll("span",attrs={'class':'data-header__content'})[1]
       foreigners1= allseason1.findAll("span",attrs={'class':'data-header__content'})[2]
       foreigners_player_percant1= allseason1.findAll("span",attrs={'class':'tabellenplatz'})[0]
       nationality_players= allseason1.findAll("span",attrs={'class':'data-header__content'})[3]
       stadium= allseason1.findAll("span",attrs={'class':'data-header__content'})[4]
       seats= allseason1.findAll("span",attrs={'class':'tabellenplatz'})[1]
       transfer_record= allseason1.findAll("span",attrs={'class':'data-header__content'})[5]
    try:
        
          teams['team_name'] = team_name.a.get('title')   
          teams['teams_squad'] = squad1.get_text(strip=True)
          teams['teams_age'] = age1.get_text(strip=True)
          teams['teams_foreigner_players'] = foreigners1.a.get_text(strip=True)
          teams['teams_foreigner_players_percant'] = foreigners_player_percant1.get_text(strip=True)
          teams['teams_national'] = nationality_players.a.get_text(strip=True)
          teams['teams_stadium_name'] = stadium.a.get_text(strip=True)
          teams['teams_stadium_seats'] = seats.get_text(strip=True)
          teams['teams_transfer_record'] = transfer_record.a.get_text(strip=True)
          
    except AttributeError:
          teams['team_name'] = ('AttributeError')
          teams['teams_squad'] = ('AttributeError')
          teams['teams_age']  = ('AttributeError')
          teams['teams_foreigner_players'] = ('AttributeError')
          teams['teams_foreigner_players_percant'] =('AttributeError')
          teams['teams_national'] = ('AttributeError')
          teams['teams_stadium_name'] = ('AttributeError')
          teams['teams_stadium_seats'] = ('AttributeError')
          teams['teams_transfer_record'] = ('AttributeError')
          
    except IndexError:
        teams['team_name'] = ('IndexError')
        teams['teams_squad'] = ('IndexError')
        teams['teams_age']  = ('IndexError')
        teams['teams_foreigner_players'] = ('IndexError')
        teams['teams_foreigner_players_percant'] = ('IndexError')
        teams['teams_national'] = ('IndexError')
        teams['teams_stadium_name'] = ('IndexError')
        teams['teams_stadium_seats'] = ('IndexError')
        teams['teams_transfer_record'] = ('IndexError')
        
    except Exception as f:
        teams['team_name'] = (f)
        teams['teams_squad'] = (f)
        teams['teams_age']  = (f)
        teams['teams_foreigner_players'] = (f)
        teams['teams_foreigner_players_percant'] = (f)
        teams['teams_national'] = (f)
        teams['teams_stadium_name'] = (f)
        teams['teams_stadium_seats'] = (f)
        teams['teams_transfer_record'] = (f)
        

    num_of_teams = 1
    for player_data in soup.select('tr.odd,tr.even'): 
        shirt_number = player_data.find('td',attrs={'class':'zentriert'}) #futbolcunun forma numarası
        player = player_data.find('td',{'class':'hauptlink'})#futbolcunun adı        
        playerlink = player_data.find('td', {'class':'hauptlink'})#futbolcunun sayfa linki
        mainposition= player_data.findAll('td')[4] #futbolcunun ana mevkisi
        dateofbirth = player_data.findAll('td')[5] #futbolcunun doğum tarihi
        birthday = player_data.findAll('td')[5] #futbolcunun doğum günü
        birthmonth = player_data.findAll('td')[5] #futblcunun doğum ayı
        birthyear = player_data.findAll('td')[5] #futblcunun doğum yılı
        age = player_data.findAll('td')[5] # futbolcunun yaşı
        nat1 = player_data.findAll('td')[6]
        nat2 = player_data.findAll('td')[6]
        height = player_data.findAll('td')[7] #futbolcunun boyu
        foot = player_data.findAll('td')[8] #futbolcunun kullandığı ayak
        joined = player_data.findAll('td')[9]   #takıma katıldığı tarih
        joined_day = player_data.findAll('td')[9] #takıma katıldığı gün
        joined_month = player_data.findAll('td')[9] #takıma katıldığı ay
        joined_year = player_data.findAll('td')[9]   #takıma katıldığı yıl
        previousteam = player_data.findAll('td')[10] #önceki takımı
        contractdate = player_data.findAll('td')[11] #kontrat tarihi
        contractday = player_data.findAll('td')[11] #kontrat günü
        contractmonth = player_data.findAll('td')[11] #kontrat ayı
        contractyear = player_data.findAll('td')[11] #kontrat yılı
        marketvalue =  player_data.findAll('td')[12]
        
    try:
        teams['shirt_number'] =shirt_number.get_text(strip=True)
        teams['player'] = player.get_text(strip=True)
        teams['playerlink'] =playerlink.a.get('href')
        teams['mainposition'] =mainposition.get_text(strip=True)
        teams['dateofbirth'] = dateofbirth.get_text(strip=True)[:12]
        teams['birthday'] = birthday.get_text(strip=True)[:6]
        teams['birthmonth'] = birthday.get_text(strip=True)[0:4]
        teams['birthyear'] =birthyear.get_text(strip=True)[8:12]
        teams['age'] =age.get_text(strip=True)[14:16]
        teams['nat1'] =nat1.img['alt']
        teams['nat2'] =nat2.img['alt']
        teams['height'] =height.get_text(strip=True)
        teams['foot'] =foot.get_text(strip=True)
        teams['joined'] =joined.get_text(strip=True)[:12]
        teams['joined_day'] =joined_day.get_text(strip=True)[:6]
        teams['joined_month'] = joined_day.get_text(strip=True)[0:4]
        teams['joined_year'] =joined_year.get_text(strip=True)[8:12]
        teams['previousteam'] =previousteam.img['alt']
        teams['contractdate'] = contractdate.get_text(strip=True)[:12]
        teams['contractday'] =  contractday.get_text(strip=True)[:6]
        teams['contractmonth'] = contractmonth.get_text(strip=True)[0:4]
        teams['contractyear'] = contractyear.get_text(strip=True)[8:12]
        teams['marketvalue'] = marketvalue.get_text(strip=True)


    except AttributeError:
           teams['shirt_number']= ('AttributeError')
           teams['player']= ('AttributeError')
           teams['playerlink']= ('AttributeError')
           teams['mainposition']= ('AttributeError')
           teams['dateofbirth']= ('AttributeError')
           teams['birthday']= ('AttributeError')
           teams['birthmonth']= ('AttributeError')
           teams['birthyear']= ('AttributeError')
           teams['age']= ('AttributeError')
           teams['height']= ('AttributeError')
           teams['foot']= ('AttributeError')
           teams['joined']= ('AttributeError')
           teams['joined_day']= ('AttributeError')
           teams['joined_month']= ('AttributeError')
           teams['joined_year']= ('AttributeError')
           teams['previousteam']=('AttributeError')
           teams['contractdate']=('AttributeError')
           teams['contractday'] = ('AttributeError')
           teams['contractmonth']=('AttributeError')
           teams['contractyear']=('AttributeError')
           teams['marketvalue']=('AttributeError') 
           
    except IndexError:
            teams['shirt_number'] = ('IndexError')
            teams['player']= ('IndexError')
            teams['playerlink']= ('IndexError')
            teams['mainposition']= ('IndexError')
            teams['dateofbirth']=  ('IndexError')
            teams['birthday']=  ('IndexError')
            teams['birthmonth']=  ('IndexError')
            teams['birthyear']=  ('IndexError')
            teams['age']=  ('IndexError')
            teams['height']=  ('IndexError')
            teams['foot']=  ('IndexError')
            teams['joined']= ('IndexError')
            teams['joined_day']= ('IndexError')
            teams['joined_month'] = ('IndexError')
            teams['joined_year']= ('IndexError')
            teams['previousteam'] = ('IndexError')
            teams['contractdate'] =('IndexError')
            teams['contractday']=('IndexError')
            teams['contractmonth']=('IndexError')
            teams['contractyear']=('IndexError')
            teams['marketvalue']=('IndexError')

            
    except Exception as f:
        
         teams['shirt_number'] = (f)
         teams['player']= (f)
         teams['playerlink']= (f)
         teams['mainposition']= (f)
         teams['dateofbirth']=  (f)
         teams['birthday']=  (f)
         teams['birthmonth']=  (f)
         teams['birthyear']=  (f)
         teams['age']=  (f)
         teams['height']=  (f)
         teams['foot']=  (f)
         teams['joined']= (f)
         teams['joined_day']= (f)
         teams['joined_month'] = (f)
         teams['joined_year']= (f)
         teams['previousteam'] = (f)
         teams['contractdate'] = (f)
         teams['contractday'] = (f)
         teams['contractmonth'] =(f)
         teams['contractyear'] =(f)
         teams['marketvalue']=(f)


    +num_of_teams    
   
        
###################################################################################################
if __name__ == "__main__":
            # get_league_pagination(main_url)
            # get_league_links(pagination)
            get_seasons()
            # print all lists
            print(teams)
 

#TO DO LİST    
# For döngüsü oyuncu tablosunu gezmiyor.
#2 uyruklu oyuncuların ikinci uyruk bilgisi alınacak.
#Gidelen takımın sayfasının linki,id bilgisi ve sezon bilgisi sözlüğe yazılacak.
#Takımın ikinci total market value si kısmını istek atmadan nasıl alınacağını bulacağım.
#Para birimlerinin yanındaki para sembolleri kalkmalı (split ile)
#Oyuncu boy bilgisinin yanındaki m harfi kalkmalı (split ile)
#İn league since alanındaki years kelimesi gidecek (split ile)
#Zaman datalarına bir daha bakacağım. 

# çıktı


{'league': 'Premier League', 'team_country': 'England', 'league_level': 'First Tier', 'teams_position': '2', 'in_league_since': '21 years', 'team_name': 'Manchester City', 'teams_squad': '24', 'teams_age': '26.7', 'teams_foreigner_players': '16', 'teams_foreigner_players_percant': '66.7 %', 'teams_national': '17', 'teams_stadium_name': 'Etihad Stadium', 'teams_stadium_seats': '55.017 Seats', 'teams_transfer_record': '+€11.70m', 'shirt_number': '19', 'player': 'Julián Álvarez', 'playerlink': '/julian-alvarez/profil/spieler/576024', 'mainposition': 'Centre-Forward', 'dateofbirth': 'Jan 31, 2000', 'birthday': 'Jan 31', 'birthmonth': 'Jan ', 'birthyear': '2000', 'age': '23', 'nat1': 'Argentina', 'nat2': 'Argentina', 'height': '1,70m', 'foot': 'right', 'joined': 'Jan 31, 2022', 'joined_day': 'Jan 31', 'joined_month': 'Jan ', 'joined_year': '2022', 'previousteam': 'CA River Plate', 'contractdate': 'Jun 30, 2027', 'contractday': 'Jun 30', 'contractmonth': 'Jun ', 'contractyear': '2027', 'marketvalue': '€50.00m'}     
 
    
 
    
 
    
 
    
 
    
 
    
 
    
