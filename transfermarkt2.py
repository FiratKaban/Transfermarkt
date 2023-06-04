# -*- coding: utf-8 -*-
""".

Created on Tue Sep 13 13:24 2022
Updated on Sun Feb 26 12:13 2023
Updated on Wed May 31 13:29 2023
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
    cur.execute("SELECT version();")
    # cur.execute('DELETE FROM public.test_table')
    # conn.commit()
    # cur.close()
    # conn.close()
    record = cur.fetchone()
    print("You are connected to - ", record, "\n")
    return cur, conn


url = "https://www.transfermarkt.co.uk/wettbewerbe/europa"
main_url = "https://www.transfermarkt.co.uk"
headerz = { "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)"
                "AppleWebKit/537.36 (KHTML, like Gecko)"
                "Chrome/45.0.2454.101 Safari/537.36"
            )
}
teams = {}
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
            league_url = main_url + leagues_link.select("a")[1]["href"]
            league_name = leagues_link.select("a")[1]["title"]
            league_country = leagues_link.select("img")[1]["title"]
            league_clubs = leagues_link.select("td")[4].text
            league_players = leagues_link.select("td")[5].text
            league_avg_age = leagues_link.select("td")[6].text
            league_foreigners = leagues_link.select("td")[7].text
            league_total_market_value = leagues_link.select("td")[9].text
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
            get_clubs(league_url)


string1 = "https://www.transfermarkt.co.uk/"
string2 = "?saison_id="


def get_clubs(league_url):
    # getting club info from all seasons of the league in leagues table
    response = requests.get(league_url, headers=headerz)
    # soup = BeautifulSoup(response.content, 'html.parser')
    secici = Selector(response.text)
    print("Getting league seasons page")
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
        for banner_info in league_href_soup.select("div.data-header__club-info"):
            league_country_name = banner_info.find("span", attrs={"class": "data-header__club"}).text.strip()
            league_level_name = banner_info.find("span", attrs={"class": "data-header__content"}).text.strip()
            league_reigning_champion = banner_info.findAll("span", attrs={"class": "data-header__content"})[1].text.strip()
            league_record_holding_champion = banner_info.findAll("span", attrs={"class": "data-header__content"})[2].a.get_text()
            league_record_holding_champion_value = banner_info.findAll("span", attrs={"class": "data-header__content"})[3].get_text(strip=True)
            league_uefa_coefficient = banner_info.findAll("span", attrs={"class": "data-header__content"})[5].a.get_text(strip=True)
            league_uefa_coefficient_value = banner_info.findAll("span", attrs={"class": "data-header__content"})[6].get_text(strip=True)
            print('league_country_name',league_country_name)
            print('league_level_name',league_level_name)
            print('league_reigning_champion',league_reigning_champion)
            print('league_record_holding_champion',league_record_holding_champion)
            print('league_record_holding_champion_value',league_record_holding_champion_value)
            print('league_uefa_coefficient',league_uefa_coefficient)
            print('league_uefa_coefficient_value',league_uefa_coefficient_value)
            print("")

        # banner2
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

        print("Getting clubs page")
        for detail_data in league_href_soup.select("tr.odd,tr.even"):
            try:
                team = detail_data.find("td", {"class": "hauptlink no-border-links"}).get_text(strip=True)
                team_link = detail_data.find("td", {"class": "hauptlink no-border-links"}).select("a")[0]["href"]
                team_href = string1 + team_link + "/plus/1"
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
            except Exception:
                pass # pass means do nothing

            # call teams.py with team_href parameter to get teams data
            sub_process = subprocess.Popen(["python3", "teams.py", team_href], stdout=subprocess.PIPE)
            output = sub_process.communicate()
            print(output)
            breakpoint()

if __name__ == "__main__":
    database_connection()
    get_leagues(url)