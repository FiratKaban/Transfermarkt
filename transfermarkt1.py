# -*- coding: utf-8 -*-
# trunk-ignore(ruff/D415)
"""
Created on Sun Feb 26 12:13:20 2023

@author: W10
"""

# 23.56

from collections import namedtuple
from bs4 import BeautifulSoup       # bs4 kütüphanesini import ediyoruz
import requests                     # requests kütüphanesini import ediyoruz
from requests import Session        #
import time
import csv
import sys
from parsel import Selector
from datetime import datetime
import psycopg2


## global vars
##############

link = []  # link with first season year
links = []  # link with all season years

# TODO: Bu yapi daha sonra dictinary olarak degistirilebilir. Yonetmesi daha kolay olur
country = []
leaguelevel = []
reigningchampion = []
recordholdingchampions = []
recordholdingchampionsvalue = []
uefa_coefficient = []
uefa_coefficient_points = []
league_title = []
number_of_teams = []
player_number = []
player_number_foreigner = []
player_number_foreigner_percent = []
player_market_value = []
player_average_market_value = []  # ortalama yaş alındı.
p_most_player_valuable = []

teams_name = []
teams_squad = []
teams_link = []
teams_age = []
teams_foreigners = []
ts_avg_market_value = []
ts_ttl_market_value = []


league_href = []
season_year = []
url_season_list = []

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36')}

# 7 mayis 2023 ekleme yapildi
z_url = "https://web.archive.org"
main_url = "https://web.archive.org/web/20230323192651/https://www.transfermarkt.co.uk/wettbewerbe/europa"
##############################################################################################################

pagination = []
leagues = []


def delete_all_rows():
    conn = psycopg2.connect(
        host="3.92.221.18",
        database="postgres",
        user="postgres",
        password="myPassword")

    cur = conn.cursor()
    cur.execute('DELETE FROM public.test_table')
    conn.commit()

    cur.close()
    conn.close()


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


def request_func():
    response = requests.get(main_url, headers=HEADERS)


def get_league_pagination(url=main_url):

    try:
        request_func()
    except TimeoutError:
        request_func()
    except Exception:
        request_func()

    response = requests.get(main_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    pages = soup.find(name="div", attrs={"class": "pager"})
    string = pages.find_all("li")[-1].a.get("href")
    
    # 7 mayis 2023 25'den 76'ya guncelleme yapildi
    substring = string[76:]
		##############################
  
    # 7 mayis 2023 ekleme yapildi
    print("string:",string)
    print("substring:",substring)
    ##############################
    
    for pages in range(1, int(substring)+1):
        url = main_url+'?page='
        url = url+str(pages)
        pagination.append(url)
    return pagination


def get_league_links(pagination):

    for url in range(len(pagination)):
        # tum responselar try catch bloguna alınıp except ksmnda 3sn bekletıp
        # tekrar request atılmalı, xxx eklenerek belrtld.
        # burası ornek olsun, sen dıger requests.get'lerı guncellersın

        try:
            response = requests.get(pagination[url], headers=HEADERS)
        except Exception:
            time.sleep(1)
            response = requests.get(pagination[url], headers=HEADERS)
        except TimeoutError:
            time.sleep(1)
            response = requests.get(pagination[url], headers=HEADERS)

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select("tr.odd, tr.even")
        for link in links:
            leagues.append(z_url+link.select("a")[1]["href"])
        # print(leagues)


def get_all_seasons():
    print('get_all_seasons calsmaya baslamstr...')
    """ Bu fonksiyon, liglerin sezonlarini alir. """

    try:
        conn = psycopg2.connect(
            host="44.204.235.127",
            database="postgres",
            user="postgres",
            password="myPassword")

        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print('database connected. ', db_version, "\n")

    except Exception:
        print('database baglant hatas aws ip vs ontrol et')

    for league in range(len(leagues)):
        # xxx: try catch
        response = requests.get(leagues[league], headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        secici = Selector(response.text)
        for seasons in secici.xpath("//select[@data-placeholder='Filter by season']/option"):
            
            print(season_year.append(seasons.xpath('./@value').get()))
            print(league_href.append(seasons.xpath('//*[@id="subnavi"]/@data-path').get()))



    string1 = "https://www.transfermarkt.co.uk/"
    string2 = "?saison_id="
    for x, y in zip(league_href, season_year):
        url = string1 + x + string2 + y
        url_season_list.append(url)
            
        cur.execute('INSERT INTO public.url_season_list(full_url, league_href, season_year) VALUES (%s, %s, %s)', (url,x,y,))
        conn.commit() # commit edilmesi gerekiyor.

    print(url_season_list)


    for league in range(len(url_season_list)):

        # https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2021

        # xxx: try catch
        response = requests.get(url_season_list[league], headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')

        # link.append(soup.find(name="div", attrs={"class": "row hide-on-print"}).get("data-path"))
        # link.append(soup.find_all("option")[-1].get("value"))

        # get first and second league banner data
        for allseason in soup.select("div.data-header__club-info"):
            country_name = allseason.find(
                "span", attrs={'class': 'data-header__club'})
            if country_name is not None:
                countryname = country.append(country_name.text.strip())
                cur.execute('UPDATE public.url_season_list SET country_name=%s WHERE full_url=%s)', (country_name.text.strip(),url_season_list[league],))
                conn.commit() # commit edilmesi gerekiyor.
                
            else:
                countryname = country.append('NaN')
###########################################################################################################################################################
            # Lig Seviyesi alındı.
            league_level_name = allseason.find(
                "span", attrs={'class': 'data-header__content'})

            if league_level_name is not None:
                league_level = leaguelevel.append(league_level_name.text.strip())
                cur.execute('UPDATE public.url_season_list SET league_level=%s WHERE full_url=%s)', (league_level_name.text.strip(),url_season_list[league],))
                conn.commit() # commit edilmesi gerekiyor.
            else:
                league_level = leaguelevel.append('NaN')
                
############################################################################################################################################################
            # Alınan ligin son şampiyon takımı alındı.
            reigning_champion_name = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})
            if reigning_champion_name is not None:
                reigning_champion = reigningchampion.append(reigning_champion_name[1].text.strip())
                cur.execute('UPDATE public.url_season_list SET reignig_champion=%s WHERE full_url=%s)', (reigning_champion_name[1].text.strip(),url_season_list[league],))
                conn.commit() # commit edilmesi gerekiyor.
            else:
                reigning_champion = reigningchampion.append('NaN')
#############################################################################################################################################################
            # En fazla şampiyonluğa sahip olan takım elde edildi.
            record_holding_champion_name = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})
            if record_holding_champion_name is not None:
                record_champion = recordholdingchampions.append(record_holding_champion_name[2].a.get_text())
                cur.execute('UPDATE public.url_season_list SET record_holding_champion=%s WHERE full_url=%s)', (record_holding_champion_name[2].a.get_text(),url_season_list[league],))
                conn.commit() # commit edilmesi gerekiyor.
            else:
                record_champion = recordholdingchampions.append('NaN')
################################################################################################################################################################
            # En fazla şampiyonluğa sahip olan takımın ne kadar şampiyonluğa
            # ulaştığı elde edildi.
            record_holding_champion_value = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})
            if record_holding_champion_value is not None:
                record_champion_value = recordholdingchampionsvalue.append(record_holding_champion_value[3].get_text(strip=True))
                cur.execute('UPDATE public.url_season_list SET record_holding_champion_value=%s WHERE full_url=%s)', ( record_holding_champion_value[3].get_text(strip=True),url_season_list[league],))
                conn.commit() # commit edilmesi gerekiyor.
            else:
                record_champion_value = recordholdingchampionsvalue.append(
                    'NaN')
######################################################################################################################################################################
            # Ülkenin ülke  sıralaması
            uefa_coefficient_arrangement = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})
            if uefa_coefficient_arrangement is not None:
                uefa_arrangement = uefa_coefficient.append(uefa_coefficient_arrangement[5].a.get_text(strip=True))
                cur.execute('UPDATE public.url_season_list SET uefa_coefficient=%s WHERE full_url=%s)', (uefa_coefficient_arrangement[5].a.get_text(strip=True) ,url_season_list[league],))
                conn.commit() # commit edilmesi gerekiyor.
            else:
                uefa_arrangement = uefa_coefficient.append('NaN')
            
######################################################################################################################################################################################                
            uefa_coefficient_arrangement_points = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})
            if uefa_coefficient_arrangement_points is not None:
                uefa_arrangement_point = uefa_coefficient_points.append(
                uefa_coefficient_arrangement_points[6].get_text(strip=True))
                cur.execute('UPDATE public.url_season_list SET  uefa_coefficient_arrangement_points=%s WHERE full_url=%s)', (uefa_coefficient_arrangement_points[6].get_text(strip=True) ,url_season_list[league],))
                conn.commit() # commit edilmesi gerekiyor.
                
            else:
                uefa_arrangement_point = uefa_coefficient_points.append('NaN')


##############################################################################################################################################################################################
        for leaguename in soup.select("div.data-header__headline-container"):
            league_name = leaguename.find("h1", attrs={
                'class': 'data-header__headline-wrapper data-header__headline-wrapper--oswald'})
            if league_name is not None:
                league_name_text = league_title.append(
                league_name.get_text(strip=True))
            else:
                league_name_text = league_title.append('NaN')

        for allseason in soup.select("div.data-header__details"):
            nteams = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})[0]
            if nteams is not None:
                nt = number_of_teams.append(
                    nteams.get_text(strip=True).strip())
            else:
                nt = number_of_teams.append('NaN')

            nplayers = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})[1]
            if nplayers is not None:
                npp = player_number.append(
                    nplayers.get_text(strip=True).strip())
            else:
                npp = player_number.append('NaN')

            nplayers_foreigner = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})[2]
            if nplayers_foreigner is not None:

                nppf = player_number_foreigner.append(
                    nplayers_foreigner.get_text(strip=True).split('\xa0')[0].strip())

            else:
                nppf = player_number_foreigner.append('NaN')

            nplayers_foreigner_percent = allseason.findAll(
                "span", attrs={'class': 'tabellenplatz'})[0]
            if nplayers_foreigner_percent is not None:
                nppf = player_number_foreigner_percent.append(
                    nplayers_foreigner_percent.get_text(strip=True).strip())
            else:
                nppf = player_number_foreigner_percent.append('NaN')

            market_value = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})[3]
            if market_value is not None:

                m_v = player_market_value.append(
                    market_value.get_text(strip=True).strip())

            else:
                m_v = player_market_value.append('NaN')

            average_market_value = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})[4]
            if average_market_value is not None:

                # strip regex ile değiştirilebilir.
                a_m_v = player_average_market_value.append(
                    average_market_value.get_text(strip=True).strip())

            else:
                a_m_v = player_average_market_value.append('NaN')

            # TODO: XXX: FIRAT: yukaridaki if else blocklari try except ile degistirilmeli.
            #  sample of try catch blocks
            most_player_valuable = allseason.findAll(
                "span", attrs={'class': 'data-header__content'})
            try:
                p_m_v = p_most_player_valuable.append(
                    most_player_valuable[-1].a.get_text(strip=True))
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



        # teams #
        cur.execute('INSERT INTO public.teams(full_url) VALUES (%s,)', (url_season_list[league],))
        conn.commit() # commit edilmesi gerekiyor.
        
        for detail_data in soup.select('tr.odd,tr.even'):
            team = detail_data.find(
                'td', {'class': 'hauptlink no-border-links'})
            if team is not None:
                team = teams_name.append(team.get_text(strip=True))
                cur.execute('UPDATE public.teams SET club_name=%s WHERE full_url=%s)', (team.get_text(strip=True),url_season_list[league],))
                conn.commit() # commit edilmesi gerekiyor.

            teamlink = detail_data.find(
                'td', {'class': 'hauptlink no-border-links'})
            if teamlink is not None:
                teamlink = teams_link.append(teamlink.select('a')[0]['href'])

            squad = detail_data.findAll('td')[2].get_text()
            if squad != '' and squad is not None:
                squad = teams_squad.append(squad)

            team_age = detail_data.findAll('td')[3].get_text()
            if team_age != '' and team_age is not None and represent_float(team_age) == True:
                team_age = teams_age.append(team_age)

            team_foreigners = detail_data.findAll('td')[4].get_text()
            if team_foreigners != '' and team_foreigners is not None and represent_int(team_foreigners) == True:
                team_foreigners = teams_foreigners.append(team_foreigners)

            t_avg_market_value = detail_data.findAll('td')[5].get_text()
            if t_avg_market_value != '' and t_avg_market_value is not None and represent_int(t_avg_market_value) == False:
                t_avg_market_value = ts_avg_market_value.append(
                    t_avg_market_value)

            t_ttl_market_value = detail_data.findAll('td')[6].get_text()
            if t_ttl_market_value != '' and t_ttl_market_value is not None:
                t_ttl_market_value = ts_ttl_market_value.append(
                    t_ttl_market_value)

        # XXX: TEAMS.PY EKLENECEK

    print('calsma tamamlanmstr...')
    # funct son satrda db conn close etmey unutma
    # close the communication with the PostgreSQL
    cur.close()
    conn.close()
    print('database connecton closed..')


if __name__ == "__main__":

    print('ana func calsmaya baslamstr...')

    frst = datetime.now().time()
    print('calsmaya baslama zaman:', frst)

    get_league_pagination(main_url)
    get_league_links(pagination)
    get_all_seasons()

    print(league_href)
    print(season_year)
    print(url_season_list)
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

    print('calsma tamamlanmstr...')
    scnd = datetime.now().time()
    print('tamamlanma zmaan:', scnd)

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
# -*- coding: utf-8 -*-

    print(scnd - frst)