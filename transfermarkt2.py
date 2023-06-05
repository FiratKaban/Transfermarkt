# -*- coding: utf-8 -*-
""".
Created on Tue Sep 13 13:24 2022
Updated on Sun Feb 26 12:13 2023
Updated on Wed May 31 13:29 2023
Updated on Mon Jun 05 01:29 2023
...
@author: FIRATKABAN
@contributer: cerebnismus
"""

from datetime import datetime
import subprocess

import psycopg2
import requests
from bs4 import BeautifulSoup
from parsel import Selector
# from requests import Session


def create_tables(cur, conn):
    """
    This function creates the necessary tables in the database.
    """

    # Create a cursor object
    # cur = conn.cursor()

    # Create leagues table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leagues (
            league_url TEXT,
            league_name TEXT,
            league_country TEXT,
            league_clubs TEXT,
            league_players TEXT,
            league_avg_age TEXT,
            league_foreigners TEXT,
            league_total_market_value TEXT
        );
    """)

    # Create leagues_data table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leagues_data (
            league_url TEXT,
            league_href TEXT,
            league_name TEXT,
            league_country_name TEXT,
            league_reigning_champion TEXT,
            league_record_holding_champion TEXT,
            league_record_holding_champion_value TEXT,
            league_uefa_coefficient TEXT,
            league_uefa_coefficient_value TEXT,
            league_num_of_clubs TEXT,
            league_num_of_players TEXT,
            league_num_of_foreigners TEXT,
            league_num_of_foreigners_percentage TEXT,
            league_market_value TEXT,
            league_avg_market_value TEXT,
            league_most_player_valuable TEXT
        );
    """)

    # Create teams table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            team TEXT,
            team_link TEXT,
            team_href TEXT,
            squad TEXT,
            team_avg_age TEXT,
            team_foreigners TEXT,
            t_avg_market_value TEXT,
            t_ttl_market_value TEXT
        );
    """)

    # Create teams_data table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams_data (
            league TEXT,
            team_country TEXT,
            team_href TEXT,
            league_level TEXT,
            teams_position TEXT,
            in_league_since TEXT,
            teams_foreigner_players_percant TEXT,
            teams_stadium_name TEXT,
            teams_stadium_seats TEXT,
            teams_transfer_record TEXT
        );
    """)

    # Create players table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            shirt_number TEXT,
            player TEXT,
            playerlink TEXT,
            playerhref TEXT,
            mainposition TEXT,
            dateofbirth TEXT,
            birthday TEXT,
            birthmonth TEXT,
            birthyear TEXT,
            age TEXT,
            nat1 TEXT,
            nat2 TEXT,
            height TEXT,
            foot TEXT,
            joined TEXT,
            joined_day TEXT,
            joined_month TEXT,
            joined_year TEXT,
            previousteam TEXT,
            contractdate TEXT,
            contractday TEXT,
            contractmonth TEXT,
            contractyear TEXT,
            marketvalue TEXT
        );
    """)

    # Create players_data table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players_data (
            id SERIAL PRIMARY KEY,
            player_href TEXT,
            place_of_birth TEXT,
            foot TEXT,
            player_agent TEXT,
            player_agent_url TEXT,
            expires TEXT,
            player_outfitter TEXT,
            twitter TEXT,
            facebook TEXT,
            instagram TEXT
        );
    """)

    # Commit the changes to the database
    conn.commit()

    # Close
    database_closer(cur, conn)


def database_connection():
    """.
    This function connects to the database.
    """
    conn = psycopg2.connect(
        host="44.204.235.127",
        database="postgres",
        user="postgres",
        password="myPassword",
    )
    cur = conn.cursor()
    # cur.execute("SELECT version();")
    # cur.execute('DELETE FROM public.test_table')
    # conn.commit()
    # cur.close()
    # conn.close()
    # record = cur.fetchone()
    # print("You are connected to - ", record, "\n")
    return cur, conn

def database_closer(cur, conn):
    """
    This function closes the database connection.
    """
    cur.close()
    conn.close()
    print("PostgreSQL connection is closed")


url = "https://www.transfermarkt.co.uk/wettbewerbe/europa"
main_url = "https://www.transfermarkt.co.uk"

headerz = { "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)"
                "AppleWebKit/537.36 (KHTML, like Gecko)"
                "Chrome/45.0.2454.101 Safari/537.36")}

teams = {}
team_hrefs = []  # getting the teams hrefs for get_seasons()
leagues_pages = []  # getting the leagues data with pagination

def get_leagues(url):
    """.
    This function gets the leagues data with pagination.

    URL compl    : https://www.transfermarkt.co.uk/wettbewerbe/europa
    URL string   : /wettbewerbe/europa?page=25
    URL substring: 25

    https://www.transfermarkt.co.uk/wettbewerbe/europa?page=1
    https://www.transfermarkt.co.uk/wettbewerbe/europa?page=2
    """
    r = requests.get(url, headers=headerz)
    soup = BeautifulSoup(r.content, "html.parser")
    page = soup.find("div", {"class": "pager"})
    stri = page.find_all("li")[-1].a.get("href")
    # string = /wettbewerbe/europa?page=25
    # substring = 25
    substring = stri[stri.find("=") + 1 :]

    # print new line
    print("                           ")
    print(url)
    print(stri)
    print(substring)

    print("                           ")
    for page in range(1, int(substring) + 1):
        urli = url + "?page=" + str(page)
        leagues_pages.append(urli)
        print(urli)

        try:
            respo = requests.get(urli, headers=headerz)
        except Exception as e:
            print(e)
            break

        # td class hauptlink
        # https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1
        soup = BeautifulSoup(respo.content, "html.parser")
        leagues_table = soup.select("tr.odd, tr.even")
        for leagues_link in leagues_table:
            league_url = str(main_url + leagues_link.select("a")[1]["href"])
            league_name = str(leagues_link.select("a")[1]["title"])
            league_country = str(leagues_link.select("img")[1]["title"])
            league_clubs = str(leagues_link.select("td")[4].text)
            league_players = str(leagues_link.select("td")[5].text)
            league_avg_age = str(leagues_link.select("td")[6].text)
            league_foreigners = str(leagues_link.select("td")[7].text)
            league_total_market_value = str(leagues_link.select("td")[9].text)
            print("Getting league data:")
            print("league_url", league_url)
            print("league_name", league_name)
            print("league_country", league_country)
            print("league_clubs", league_clubs)
            print("league_players", league_players)
            print("league_avg_age", league_avg_age)
            print("league_foreigners", league_foreigners)
            print("league_total_market_value", league_total_market_value)
            print("")

            # create string tuple league
            league = (str(league_url), str(league_name), str(league_country), str(league_clubs), str(league_players), str(league_avg_age), str(league_foreigners), str(league_total_market_value))

            cur, conn = database_connection()
            cur.execute("""
                INSERT INTO leagues (
                    league_url,
                    league_name,
                    league_country,
                    league_clubs,
                    league_players,
                    league_avg_age,
                    league_foreigners,
                    league_total_market_value
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, league)
            conn.commit()
            database_closer(cur, conn)

            get_clubs(league_url)
            # break # test
        # break # test
        # exit() # test


string0 = "https://www.transfermarkt.co.uk"
string1 = "https://www.transfermarkt.co.uk/"
string2 = "?saison_id="


def get_clubs(league_url):
    # getting club info from all seasons of the league in leagues table
    response = requests.get(league_url, headers=headerz)
    # soup = BeautifulSoup(response.content, 'html.parser')
    secici = Selector(response.text)
    print("get_clubs function is running")
    for seasons in secici.xpath("//select[@data-placeholder='Filter by season']/option"):
        season_year = seasons.xpath("./@value").get()
        league_href = seasons.xpath('//*[@id="subnavi"]/@data-path').get()
        league_href = string1 + league_href + string2 + season_year
        # last year data is empty, thats why we need to check
        if season_year != str(datetime.now().year):
            print(league_href)
        else:
            continue  # go to next season

        league_href_response = requests.get(league_href, headers=headerz)
        league_href_soup = BeautifulSoup(league_href_response.content, "html.parser")

        # getting first and second season filtered league banner info
        # banner 1
        print("banner 1")
        for banner_info in league_href_soup.select("div.data-header__club-info"):
            league_country_name = banner_info.find("span", attrs={"class": "data-header__club"}).text.strip()
            league_level_name = banner_info.find("span", attrs={"class": "data-header__content"}).text.strip()
            league_reigning_champion = banner_info.findAll("span", attrs={"class": "data-header__content"})[1].text.strip()
            league_record_holding_champion = banner_info.findAll("span", attrs={"class": "data-header__content"})[2].a.get_text()
            league_record_holding_champion_value = banner_info.findAll("span", attrs={"class": "data-header__content"})[3].get_text(strip=True)
            league_uefa_coefficient = banner_info.findAll("span", attrs={"class": "data-header__content"})[5].a.get_text(strip=True)
            league_uefa_coefficient_value = banner_info.findAll("span", attrs={"class": "data-header__content"})[6].get_text(strip=True)
            print('league_url',league_url)
            print('league_country_name',league_country_name)
            print('league_level_name',league_level_name)
            print('league_reigning_champion',league_reigning_champion)
            print('league_record_holding_champion',league_record_holding_champion)
            print('league_record_holding_champion_value',league_record_holding_champion_value)
            print('league_uefa_coefficient',league_uefa_coefficient)
            print('league_uefa_coefficient_value',league_uefa_coefficient_value)
            print("")

        # banner2
        print("banner 2")
        for x in league_href_soup.select("div.data-header__headline-container"):
            league_name = x.find("h1",attrs={"class": "data-header__headline-wrapper data-header__headline-wrapper--oswald"},).get_text(strip=True)
            print(league_name)
        for x in league_href_soup.select("div.data-header__details"):
            league_num_of_clubs = (x.findAll("span", attrs={"class": "data-header__content"})[0].get_text(strip=True).strip())
            league_num_of_players = (x.findAll("span", attrs={"class": "data-header__content"})[1].get_text(strip=True).strip())
            league_num_of_foreigners = (x.findAll("span", attrs={"class": "data-header__content"})[2].get_text(strip=True).split("\xa0")[0].strip())
            league_num_of_foreigners_percentage = (x.findAll("span", attrs={"class": "tabellenplatz"})[0].get_text(strip=True).strip())
            league_market_value = (x.findAll("span", attrs={"class": "data-header__content"})[3].get_text(strip=True).strip())
            league_avg_market_value = (x.findAll("span", attrs={"class": "data-header__content"})[4].get_text(strip=True).strip())
            league_most_player_valuable = x.findAll("span", attrs={"class": "data-header__content"})[-1].get_text(strip=True)
            print('league_num_of_clubs',league_num_of_clubs)
            print('league_num_of_players',league_num_of_players)
            print('league_num_of_foreigners',league_num_of_foreigners, "Players", league_num_of_foreigners_percentage)
            print('league_market_value',league_market_value)
            print('league_avg_market_value',league_avg_market_value)
            print('league_most_player_valuable',league_most_player_valuable)
            print("")

        # create string tuple league_data
        league_data = (str(league_url), str(league_href), str(league_name), str(league_country_name), str(league_reigning_champion), str(league_record_holding_champion), str(league_record_holding_champion_value), str(league_uefa_coefficient), str(league_uefa_coefficient_value), str(league_num_of_clubs), str(league_num_of_players), str(league_num_of_foreigners), str(league_num_of_foreigners_percentage), str(league_market_value), str(league_avg_market_value), str(league_most_player_valuable))

        cur, conn = database_connection()
        cur.execute("""
            INSERT INTO leagues_data (
                league_url,
                league_href,
                league_name,
                league_country_name,
                league_reigning_champion,
                league_record_holding_champion,
                league_record_holding_champion_value,
                league_uefa_coefficient,
                league_uefa_coefficient_value,
                league_num_of_clubs,
                league_num_of_players,
                league_num_of_foreigners,
                league_num_of_foreigners_percentage,
                league_market_value,
                league_avg_market_value,
                league_most_player_valuable
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, league_data)
        conn.commit()
        database_closer(cur, conn)

        print("Getting clubs page")
        # team
        for detail_data in league_href_soup.select("tr.odd,tr.even"):
            try:
                team = detail_data.find("td", {"class": "hauptlink no-border-links"}).get_text(strip=True)
                team_link = detail_data.find("td", {"class": "hauptlink no-border-links"}).select("a")[0]["href"]
                # https://www.transfermarkt.co.uk//manchester-city/startseite/verein/281/saison_id/2022    for the team compact page
                # https://www.transfermarkt.co.uk/manchester-city/kader/verein/281/saison_id/2022/plus/1   for the team detailed page
                # team_link contains 'startseite' word, we need to replace it with 'kader'
                team_link = team_link.replace("startseite", "kader")
                team_href = string0 + team_link + "/plus/1"
                team_hrefs.append(team_href)
                squad = detail_data.findAll("td")[2].get_text()
                team_avg_age = detail_data.findAll("td")[3].get_text()
                team_foreigners = detail_data.findAll("td")[4].get_text()
                t_avg_market_value = detail_data.findAll("td")[5].get_text()
                t_ttl_market_value = detail_data.findAll("td")[6].get_text()
                print('team',team)
                print('team_link',team_link)
                print('team_href',team_href)
                print('squad',squad,'Players')
                print('team_avg_age',team_avg_age,'Years')
                print('team_foreigners',team_foreigners)
                print('t_avg_market_value',t_avg_market_value)
                print('t_ttl_market_value',t_ttl_market_value)
                print("")

                # create string tuple team
                team = (str(team), str(team_link), str(team_href), str(squad), str(team_avg_age), str(team_foreigners), str(t_avg_market_value), str(t_ttl_market_value))
                cur, conn = database_connection()
                cur.execute("""
                    INSERT INTO teams (
                        team,
                        team_link,
                        team_href,
                        squad,
                        team_avg_age,
                        team_foreigners,
                        t_avg_market_value,
                        t_ttl_market_value
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, team)
                conn.commit()
                database_closer(cur, conn)

            except Exception:
                pass # pass means do nothing

            get_teams(team_href)
            # break; exit()


def get_teams(team_href):
    print("get_teams started")
    response = requests.get(team_href, headers=headerz)

    # check if the page is responding
    if response.status_code == 200:
        print("Page responding witg status code: 200 OK")
    else:
        status = response.status_code
        print("Page is responding with status code:", status)
        pass # pass means do nothing

    soup = BeautifulSoup(response.content, 'html.parser')

    for allseason in soup.select("div.data-header__club-info"):
        # lig kodunu split yapıp sözlüğe yazdıracaz.
        league = allseason.find("span", attrs={'class': 'data-header__club'})
        country = allseason.find(
            "span", attrs={'class': 'data-header__content'})
        league_level = allseason.find(
            "span", attrs={'class': 'data-header__content'})
        tableposition = allseason.findAll(
            "span", attrs={'class': 'data-header__content'})[1]
        In_leaguesince = allseason.findAll(
            "span", attrs={'class': 'data-header__content'})[2]

    try:
        teams['league'] = league.a.get_text(strip=True)
        teams['team_country'] = country.find('img')['alt']
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
        teams['teams_position'] = ('IndexError')
        teams['in_league_since'] = ('IndexError')

    except Exception as f:
        teams['league'] = (f)
        teams['team_country'] = (f)
        teams['league_level'] = (f)
        teams['teams_position'] = (f)
        teams['in_league_since'] = (f)

    for allseason1 in soup.select("div.data-header__details"):
        # takımın sezonu ve linkini split yapacaz ve sözlüğe yazdıracaz.
        team_name = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[4]
        squad1 = allseason1.find(
            "span", attrs={'class': 'data-header__content'})
        age1 = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[1]
        foreigners1 = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[2]
        foreigners_player_percant1 = allseason1.findAll(
            "span", attrs={'class': 'tabellenplatz'})[0]
        nationality_players = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[3]
        stadium = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[4]
        seats = allseason1.findAll("span", attrs={'class': 'tabellenplatz'})[1]
        transfer_record = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[5]
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
        teams['teams_age'] = ('AttributeError')
        teams['teams_foreigner_players'] = ('AttributeError')
        teams['teams_foreigner_players_percant'] = ('AttributeError')
        teams['teams_national'] = ('AttributeError')
        teams['teams_stadium_name'] = ('AttributeError')
        teams['teams_stadium_seats'] = ('AttributeError')
        teams['teams_transfer_record'] = ('AttributeError')

    except IndexError:
        teams['team_name'] = ('IndexError')
        teams['teams_squad'] = ('IndexError')
        teams['teams_age'] = ('IndexError')
        teams['teams_foreigner_players'] = ('IndexError')
        teams['teams_foreigner_players_percant'] = ('IndexError')
        teams['teams_national'] = ('IndexError')
        teams['teams_stadium_name'] = ('IndexError')
        teams['teams_stadium_seats'] = ('IndexError')
        teams['teams_transfer_record'] = ('IndexError')

    except Exception as f:
        teams['team_name'] = (f)
        teams['teams_squad'] = (f)
        teams['teams_age'] = (f)
        teams['teams_foreigner_players'] = (f)
        teams['teams_foreigner_players_percant'] = (f)
        teams['teams_national'] = (f)
        teams['teams_stadium_name'] = (f)
        teams['teams_stadium_seats'] = (f)
        teams['teams_transfer_record'] = (f)

    # team_data with team_href
    print('league',league.a.get_text(strip=True))
    print('team_country',country.find('img')['alt'])
    print('league_level',league_level.a.get_text(strip=True))
    print('teams_position',tableposition.a.get_text(strip=True))
    print('in_league_since',In_leaguesince.a.get_text(strip=True))
    print('teams_foreigner_players_percant',foreigners_player_percant1.get_text(strip=True))
    print('teams_stadium_name',stadium.a.get_text(strip=True))
    print('teams_stadium_seats',seats.get_text(strip=True))
    print('teams_transfer_record',transfer_record.a.get_text(strip=True))
    print('')

    cur, conn = database_connection()
    team_data = (str(league.a.get_text(strip=True)), str(country.find('img')['alt']), str(team_href), str(league_level.a.get_text(strip=True)), str(tableposition.a.get_text(strip=True)), str(In_leaguesince.a.get_text(strip=True)), str(foreigners_player_percant1.get_text(strip=True)), str(stadium.a.get_text(strip=True)), str(seats.get_text(strip=True)), str(transfer_record.a.get_text(strip=True)))
    cur.execute("""
        INSERT INTO teams_data (
            league,
            team_country,
            team_href,
            league_level,
            teams_position,
            in_league_since,
            teams_foreigner_players_percant,
            teams_stadium_name,
            teams_stadium_seats,
            teams_transfer_record
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, team_data)
    conn.commit()
    database_closer(cur, conn)

    nat1 = []
    for player_data in soup.select('tr.odd,tr.even'):
        shirt_number = player_data.find('td', attrs={'class': 'zentriert'}).get_text(strip=True)  # futbolcunun forma numarası
        player = player_data.find('td', {'class': 'hauptlink'}).get_text(strip=True)  # futbolcunun adı
        playerlink = player_data.find('td', {'class': 'hauptlink'}).a.get('href')  # futbolcunun sayfa linki
        player_href = string0 + playerlink
        mainposition = player_data.findAll('td')[4].get_text(strip=True)  # futbolcunun ana mevkisi
        dateofbirth = player_data.findAll('td')[5].get_text(strip=True)[:12]  # futbolcunun doğum tarihi
        birthday = player_data.findAll('td')[5].get_text(strip=True)[4:6]  # futbolcunun doğum günü
        birthmonth = player_data.findAll('td')[5].get_text(strip=True)[0:4]  # futblcunun doğum ayı
        birthyear = player_data.findAll('td')[5].get_text(strip=True)[8:12]  # futblcunun doğum yılı
        age = player_data.findAll('td')[5].get_text(strip=True)[14:16]  # futbolcunun yaşı
        nat1 = player_data.findAll('td')[6].findAll('img')[0]['title'] # ulkesi
        nat2 = player_data.findAll('td')[6].findAll('img')[-1]['title'] # TODO: TRY EXCEPT EKLENECEK
        height = player_data.findAll('td')[7].get_text(strip=True)  # futbolcunun boyu
        foot = player_data.findAll('td')[8].get_text(strip=True)  # futbolcunun kullandığı ayak
        joined = player_data.findAll('td')[9].get_text(strip=True)[:12]  # takıma katıldığı tarih
        joined_day = player_data.findAll('td')[9].get_text(strip=True)[:6]  # takıma katıldığı gün
        joined_month = player_data.findAll('td')[9].get_text(strip=True)[0:4]  # takıma katıldığı ay
        joined_year = player_data.findAll('td')[9].get_text(strip=True)[8:12]  # takıma katıldığı yıl
        previousteam = player_data.findAll('td')[10].img['alt']  # önceki takımı
        contractdate = player_data.findAll('td')[11].get_text(strip=True)[:12]  # kontrat tarihi
        contractday = player_data.findAll('td')[11].get_text(strip=True)[:6]  # kontrat günü
        contractmonth = player_data.findAll('td')[11].get_text(strip=True)[0:4]  # kontrat ayı
        contractyear = player_data.findAll('td')[11].get_text(strip=True)[8:12]  # kontrat yılı
        marketvalue = player_data.findAll('td')[12].get_text(strip=True)

        try:
            print('shirt_number:', shirt_number) 
            print('player:', player)
            print('playerlink:', playerlink)
            print('player_href:', player_href)
            print('mainposition:', mainposition)
            print('dateofbirth:', dateofbirth)
            print('birthday:', birthday)
            print('birthmonth:', birthmonth)
            print('birthyear:', birthyear)
            print('age:', age)
            print('nat1:', nat1)
            print('nat2:', nat2)
            print('height:', height)
            print('foot:', foot)
            print('joined:', joined)
            print('joined_day:', joined_day)
            print('joined_month:', joined_month)
            print('joined_year:', joined_year)
            print('previousteam:', previousteam)  
            print('contractdate:', contractdate)
            print('contractday:', contractday)
            print('contractmonth:', contractmonth)
            print('contractyear:', contractyear)
            print('marketvalue:', marketvalue)
            print('')

            cur, conn = database_connection()
            player = (str(shirt_number), str(player), str(playerlink), str(player_href), str(mainposition), str(dateofbirth), str(birthday), str(birthmonth), str(birthyear), str(age), str(nat1), str(nat2), str(height), str(foot), str(joined), str(joined_day), str(joined_month), str(joined_year), str(previousteam), str(contractdate), str(contractday), str(contractmonth), str(contractyear), str(marketvalue))
            cur.execute("""
                INSERT INTO players (
                    shirt_number,
                    player,
                    playerlink,
                    playerhref,
                    mainposition,
                    dateofbirth,
                    birthday,
                    birthmonth,
                    birthyear,
                    age,
                    nat1,
                    nat2,
                    height,
                    foot,
                    joined,
                    joined_day,
                    joined_month,
                    joined_year,
                    previousteam,
                    contractdate,
                    contractday,
                    contractmonth,
                    contractyear,
                    marketvalue
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s);
            """, player)
            conn.commit()
            database_closer(cur, conn)

        except Exception as e:
            print('Error:', e)
            pass

        get_players(player_href)
        # break; exit()


def get_players(player_href):
    """
    Extract players data for each team
    """
    print('get_players started')
    print('player_href', player_href)
    response = requests.get(player_href, headers=headerz)

    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('span',class_='info-table__content info-table__content--bold')
    agent_data = soup.find_all('span',class_='info-table__content info-table__content--bold info-table__content--flex')

    place_of_birth = data[2].text.strip()
    foot = data[7].text.strip()

    try:
        player_agent = agent_data[0].text.strip()
    except:
        player_agent = 'None'

    try:
        player_agent_url = agent_data[0].a['href']
    except:
        player_agent_url = 'None'

    expires = data[9].text.strip()
    player_outfitter = data[11].text.strip()
    twitter = data[12].findAll('a')[0]['href']
    facebook = data[12].findAll('a')[1]['href']
    instagram = data[12].findAll('a')[2]['href']
    print('player_href:', player_href)
    print('place_of_birth:', place_of_birth)
    print('foot:', foot)
    print('player_agent:', player_agent)
    print('player_agent_url:', string0+player_agent_url)
    print('expires:', expires)
    print('player_outfitter:', player_outfitter)
    print('twitter:', twitter)
    print('facebook:', facebook)
    print('instagram:', instagram)
    print('')

    cur, conn = database_connection()
    player_data = (str(player_href), str(place_of_birth), str(foot), str(player_agent), str(string0+player_agent_url), str(expires), str(player_outfitter), str(twitter), str(facebook), str(instagram))
    cur.execute("""
        INSERT INTO players_data (
            player_href,
            place_of_birth,
            foot,
            player_agent,
            player_agent_url,
            expires,
            player_outfitter,
            twitter,
            facebook,
            instagram
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, player_data)
    conn.commit()
    database_closer(cur, conn)

    exit(0) # its for testing purposes


def main():
    """
    This is the main function that controls the flow of the program.
    """
    # Connect to the database
    cur, conn = database_connection()
    # Create tables if they don't exist
    create_tables(cur, conn)
    print('Database connection established.')

    get_leagues(url) # and insert them into the database

    # Close the database connection
    cur.close()
    conn.close()
    print('Database connection closed.')

    # Print the scraped/inserted data
    # print_data()


if __name__ == "__main__":
    main()
