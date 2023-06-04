# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:24:29 2022

@author: FIRATKABAN
@contributer: cerebnismus
"""


from collections import namedtuple
from bs4 import BeautifulSoup       # bs4 kütüphanesini import ediyoruz
import requests                     # requests kütüphanesini import ediyoruz
from requests import Session        # 
import time, csv, psycopg2, sys
from parsel   import Selector

# XXX !!! ONCE TRANSFERMARKT.PY NIN DUZGUN CALISTIGINDAN EMIN OLUN !!! XXX
# ARALARA PRINT EKLEYIP CIKARARAK DEBUG YAPABILIRSIN

# TODO: DEGISKENLERIN DB'DE KARSILIGI OLMALI
#       BUNUN ICIN LUCIDCHART VB CROWS FOOT NOTASYONU VB BI EXCEL DE OLABIIR
#       HAZIRLARSAN, HAZIR VERIYE GORE DB YAPISINI GUNCELLEYEBILIRIZ

#       DB'ye ekleme fonsiyon ornekleri gosterecegim. AWS postgresql kullanacagiz.
#       orneklere gore tum degiskenlerin DB'ye yazilmasi kismi sende.

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

teams_name=[]
teams_squad=[]
teams_link=[]
teams_age=[]
teams_foreigners=[]
ts_avg_market_value=[]
ts_ttl_market_value=[]

def get_all_seasons():
    """ Bu fonksiyon, liglerin sezonlarini alir. """
    for league in range(len(leagues)):
        response = requests.get(leagues[league], headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        link.append(soup.find(name="div", attrs={"class": "row hide-on-print"}).get("data-path"))
        link.append(soup.find_all("option")[-1].get("value"))

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
     
 
            
            
    # XXX: for each link in links list get all team data
    #      get all team data from league years using 'links' list
        
    for league in range(len(links)):
        
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
                p_m_v = p_most_player_valuable.append('')
            # catch IndexError
            except IndexError:
                p_m_v = p_most_player_valuable.append('')
            # catch Exception
            except Exception as e:
                p_m_v = p_most_player_valuable.append('')
        

        # XXX: for each link in links list get all team data
        #      get all team data from league years using 'links' list.
        
        for detail_data in soup.select('tr.odd,tr.even'):
            team = detail_data.find('td',{'class':'hauptlink no-border-links'})
            if team is not None:
                team = teams_name.append(team.get_text(strip=True))

            teamlink = detail_data.find('td', {'class':'hauptlink no-border-links'})
            if teamlink is not None:
                teamlink =  teams_link.append(teamlink.select('a')[0]['href'])
        
            squad = detail_data.findAll('td')[2].get_text()
            if squad != '' and squad is not None:
                squad = teams_squad.append(squad)
                    
            team_age = detail_data.findAll('td')[3].get_text()
            if team_age != '' and team_age is not None and represent_float(team_age)==True:
                team_age = teams_age.append(team_age)
            
            team_foreigners = detail_data.findAll('td')[4].get_text()
            if team_foreigners != '' and team_foreigners is not None and represent_int(team_foreigners)==True:
                team_foreigners = teams_foreigners.append(team_foreigners)
                        
            t_avg_market_value = detail_data.findAll('td')[5].get_text()
            if t_avg_market_value != '' and t_avg_market_value is not None and represent_int(t_avg_market_value)==False:
                t_avg_market_value = ts_avg_market_value.append(t_avg_market_value)

            t_ttl_market_value = detail_data.findAll('td')[6].get_text()
            if t_ttl_market_value != '' and t_ttl_market_value is not None:
                t_ttl_market_value = ts_ttl_market_value.append(t_ttl_market_value)
                
                
        # XXX: TEAMS.PY EKLENECEK



if __name__ == "__main__":
   
    get_league_pagination(main_url)
    get_league_links(pagination)
    get_all_seasons()

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
    
    print(teams_name)
    print(teams_link)
    print(teams_squad)
    
    print(teams_age)
    print(teams_foreigners)
    print(ts_avg_market_value)
    print(ts_ttl_market_value)
    
    

# TODO: Class mantigi ve veritabani baglantisi icin kod revize edilecek.

# XXX: end of the project: SERVICE SCRIPT
# python uygulamasinin sunucuda surekli calismasi icin 
# ve surekli calisan uygulamanin monitor edilebilmesi icin
# cron job kullanilabilir. fakat uygulanabilirlik ve monitoring acisindan
# degerlendirdiginde systemctl'de calisacak olan service scripti daha mantikli.
# systemctl example link: https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
    
# XXX: end of the project: ip reputation control & ip changer

# how to check the string is string or integer
# https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
