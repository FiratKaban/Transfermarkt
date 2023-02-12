# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:24:29 2022

@author: FIRATKABAN
@contributer: cerebnismus
"""

from collections import namedtuple
import sys
from bs4 import BeautifulSoup       # bs4 kütüphanesini import ediyoruz
import requests                     # requests kütüphanesini import ediyoruz
from requests import Session        # 
import time, csv
from parsel   import Selector

# python uzerinden aws postgresql baglantisi icin gerekli kütüphaneler
import psycopg2


# TODO: Class mantigi ve veritabani baglantisi icin kod revize edilecek.


HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/45.0.2454.101 Safari/537.36')}

z_url = "https://www.transfermarkt.co.uk"
main_url = "https://www.transfermarkt.co.uk/wettbewerbe/europa"

pagination = []
leagues=[]

def get_league_pagination(url=main_url):
    
    response = requests.get(main_url,headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    pages = soup.find(name="div", attrs={"class": "pager"})
    string = pages.find_all("li")[-1].a.get("href")
    substring = string[25:]
    # print(substring)
    
    # XXX: Pagination'I TEST AMACIYLA 1 SAYFA YAPABILIRSIN     

    for pages in range(1,int(substring)+1):
        url=main_url+'?page='
        url = url+str(pages)
        pagination.append(url)

    return pagination

def get_league_links(pagination):

    for url in range(len(pagination)):
        response = requests.get(pagination[url], headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select("tr.odd, tr.even")
        for link in links:
            leagues.append(z_url+link.select("a")[1]["href"])
            
        print(leagues)
        


link=[] # link with first season year
links=[] # link with all season years

# TODO: OUTDATED !!! 
def get_all_seasons():
    """ production mode """
    """ Bu fonksiyon, liglerin sezonlarini alir. """
    for league in range(len(leagues)):
        response = requests.get(leagues[league], headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        link.append(soup.find(name="div", attrs={"class": "row hide-on-print"}).get("data-path"))
        link.append(soup.find_all("option")[-1].get("value"))

 
 # TODO: Bu yapi daha sonra dictinary olarak degistirilebilir. Yonetmesi daha kolay olur
country=[]
leaguelevel=[]
reigningchampion=[]
recordholdingchampions=[]
recordholdingchampionsvalue=[]
uefa_coefficient=[]
uefa_coefficient_points =[]
league_title=[]
number_of_teams=[]
player_number=[]
player_number_foreigner=[]
player_number_foreigner_percent=[]
player_market_value=[]
player_average_market_value=[] #ortalama yaş alındı.
p_most_player_valuable=[]


def get_seasons():
    """ test mode """
    # https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2021

    response = requests.get('https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2021', headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')    

    link.append(soup.find(name="div", attrs={"class": "row hide-on-print"}).get("data-path"))
    link.append(soup.find_all("option")[-1].get("value"))
    
    # get first and second league banner data
    for allseason in soup.select("div.data-header__club-info"):
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
        
        #Alınan ligin son şampiyon takımı alındı.
        reigning_champion_name = allseason.findAll("span",attrs={'class':'data-header__content'})
        if reigning_champion_name is not None:
            reigning_champion= reigningchampion.append(reigning_champion_name[1].text.strip())
        else:
            reigning_champion= reigningchampion.append('NaN') 
                
        #En fazla şampiyonluğa sahip olan takım elde edildi.                                       
        record_holding_champion_name = allseason.findAll("span",attrs={'class':'data-header__content'})
        if record_holding_champion_name is not None:
               record_champion= recordholdingchampions.append(record_holding_champion_name[2].a.get_text())
        else:
               record_champion= recordholdingchampions.append('NaN')
      
        #En fazla şampiyonluğa sahip olan takımın ne kadar şampiyonluğa 
        #ulaştığı elde edildi.                   
        record_holding_champion_value = allseason.findAll("span",attrs={'class':'data-header__content'})
        if record_holding_champion_value is not None:
               record_champion_value= recordholdingchampionsvalue.append(record_holding_champion_value[3].get_text(strip=True))
        else:
               record_champion_value= recordholdingchampionsvalue.append('NaN')

        #Ülkenin ülke  sıralaması
        uefa_coefficient_arrangement = allseason.findAll("span",attrs={'class':'data-header__content'})
        if uefa_coefficient_arrangement is not None:
            uefa_arrangement= uefa_coefficient.append(uefa_coefficient_arrangement[5].a.get_text(strip=True))
        else:
            uefa_arrangement= uefa_coefficient.append('NaN')

        uefa_coefficient_arrangement_points = allseason.findAll("span",attrs={'class':'data-header__content'})
        if uefa_coefficient_arrangement_points is not None:
            uefa_arrangement_point= uefa_coefficient_points.append(uefa_coefficient_arrangement_points[6].get_text(strip=True))
        else:
            uefa_arrangement_point= uefa_coefficient_points.append('NaN')
            
    for leaguename in soup.select("div.data-header__headline-container"):
        league_name = leaguename.find("h1",attrs={'class':'data-header__headline-wrapper data-header__headline-wrapper--oswald'})
        if league_name is not None:
            league_name_text= league_title.append(league_name.get_text(strip=True))
        else:
            league_name_text= league_title.append('NaN')

    for allseason in soup.select("div.data-header__details"):
        nteams = allseason.findAll("span",attrs={'class':'data-header__content'})[0]
        if nteams is not None:
            nt = number_of_teams.append(nteams.get_text(strip=True).strip())
        else:
            nt = number_of_teams.append('NaN')

        nplayers = allseason.findAll("span",attrs={'class':'data-header__content'})[1]
        if nplayers is not None:
            npp = player_number.append(nplayers.get_text(strip=True).strip())
        else:
            npp = player_number.append('NaN')
        
        nplayers_foreigner = allseason.findAll("span",attrs={'class':'data-header__content'})[2]
        if nplayers_foreigner is not None:
            
            nppf = player_number_foreigner.append(nplayers_foreigner.get_text(strip=True).split('\xa0')[0].strip())
            
        else:
            nppf = player_number_foreigner.append('NaN')
        
        nplayers_foreigner_percent = allseason.findAll("span",attrs={'class':'tabellenplatz'})[0]
        if nplayers_foreigner_percent is not None:
            nppf = player_number_foreigner_percent.append(nplayers_foreigner_percent.get_text(strip=True).strip())
        else:
            nppf = player_number_foreigner_percent.append('NaN')

        market_value = allseason.findAll("span",attrs={'class':'data-header__content'})[3]
        if market_value is not None:
            
            m_v = player_market_value.append(market_value.get_text(strip=True).strip())
            
        else:
            m_v = player_market_value.append('NaN')
        

        average_market_value = allseason.findAll("span",attrs={'class':'data-header__content'})[4]
        if average_market_value is not None:
            
            #strip regex ile değiştirilebilir.
            a_m_v = player_average_market_value.append(average_market_value.get_text(strip=True).strip())
            
        else:
            a_m_v = player_average_market_value.append('NaN')
            
        # TODO: XXX: FIRAT: yukaridaki if else blocklari try except ile degistirilmeli.
        #  sample of try catch blocks
        most_player_valuable = allseason.findAll("span",attrs={'class':'data-header__content'})
        try:
            p_m_v = p_most_player_valuable.append(most_player_valuable[-1].a.get_text(strip=True))
        # catch AttributeError
        except AttributeError:
            # TODO: do nothing
            p_m_v = p_most_player_valuable.append('AttributeError')
        # catch IndexError
        except IndexError:
            p_m_v = p_most_player_valuable.append('IndexError')
        # catch Exception
        except Exception as e:
            p_m_v = p_most_player_valuable.append(e)
            
        
        
            






      
    for year in link:
        season_link = link[0]
        first_year = link[1]
        
        for i in range(int(first_year), 2023): # until 2022
            links.append(season_link + "/?saison_id=" + str(i))
            # print(z_url + season_link + "?saison_id=" + str(i))
            ++i
    
            # returns links list like:
            # https://www.transfermarkt.co.ukpremier-league/startseite/wettbewerb/GB1/plus/?saison_id=1992
            # https://www.transfermarkt.co.ukpremier-league/startseite/wettbewerb/GB1/plus/?saison_id=1993
            # .


        
        # XXX: bu formatta biz bir ligin sezonlarini almak yerine
        # XXX: bir ligdeki ilk sezonun baslangic yilini aliyoruz. orn: 1928
        # XXX: bu yuzden bundan sonraki fonksiyona try catch bloklari ekleyerek
        # XXX: hata aldigimizda ilgili ligin o sezon yilinda aktif olmadigini anlayacagiz.
        
        
    


if __name__ == "__main__":
    # get_league_pagination(main_url)
    # get_league_links(pagination)
    get_seasons()
    # print all lists
    print(country)
    print(league_title)
    print(leaguelevel)
    print(reigningchampion)
    print(recordholdingchampions)
    print(recordholdingchampionsvalue)
    print(uefa_coefficient)
    print(uefa_coefficient_points)
    print(number_of_teams)
    print(player_number)
    print(player_number_foreigner)
    print(player_number_foreigner_percent)
    print(player_market_value)
    print(player_average_market_value)
    print(p_most_player_valuable)
# XXX: end of the project: SERVICE SCRIPT
# python uygulamasinin sunucuda surekli calismasi icin 
# ve surekli calisan uygulamanin monitor edilebilmesi icin
# cron job kullanilabilir. fakat uygulanabilirlik ve monitoring acisindan
# degerlendirdiginde systemctl'de calisacak olan service scripti daha mantikli.
# systemctl example link: https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
    
# XXX: end of the project: ip reputation control & ip changer

"""
z_url = "https://www.transfermarkt.co.uk"
main_url = "https://www.transfermarkt.co.uk/wettbewerbe/europa"

yukaridaki url disindaki urllere erismeyecegiz .
bu urlde ligler var ve bu liglerin sezonlari var.
oncelikle pagination ile urlleri ardindan sezonlari cekiyoruz.

get league pagination:
https://www.transfermarkt.co.uk/wettbewerbe/europa?page=2
https://www.transfermarkt.co.uk/wettbewerbe/europa?page=3
https://www.transfermarkt.co.uk/wettbewerbe/europa?page=4
.
.
.

get leagues links:
https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1
.
.
.

get seasons:
https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2021
.
.
.

(base) 192 Desktop/Transfermarkt ‹main*› » time python3 transfermarkt.py
['premier-league/startseite/wettbewerb/GB1/plus', '1992']

['premier-league/startseite/wettbewerb/GB1/plus?saison_id=1992', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1993', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1994', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1995', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1996', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1997', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1998', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1999', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2000', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2001', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2002', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2003', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2004', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2005', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2006', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2007', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2008', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2009', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2010', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2011', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2012', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2013', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2014', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2015', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2016', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2017', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2018', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2019', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2020', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2021', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2022', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1992', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1993', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1994', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1995', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1996', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1997', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1998', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=1999', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2000', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2001', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2002', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2003', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2004', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2005', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2006', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2007', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2008', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2009', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2010', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2011', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2012', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2013', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2014', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2015', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2016', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2017', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2018', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2019', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2020', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2021', 'premier-league/startseite/wettbewerb/GB1/plus?saison_id=2022']
python3 transfermarkt.py  0.80s user 0.23s system 8% cpu 11.667 total

"""