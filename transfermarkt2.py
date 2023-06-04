# -*- coding: utf-8 -*-
""".

Created on Tue Sep 13 13:24 2022
Updated on Sun Feb 26 12:13 2023
Updated on Wed May 31 13:29 2023
...
@author: FIRATKABAN
@contributer: cerebnismus
"""


import requests
from datetime import datetime
from bs4 import BeautifulSoup

url = "https://www.transfermarkt.co.uk/wettbewerbe/europa"
main_url = "https://www.transfermarkt.co.uk"
headerz = {
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/45.0.2454.101 Safari/537.36"
    )
}

# all print lines must be stored in database, update in same line !!!


leagues_pages = []
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
        except requests.exceptions.ConnectionError:
            print("Connection refused", urli)
            break
        except requests.exceptions.Timeout:
            print("Timeout", urli)
            break
        except requests.exceptions.RequestException as e:
            print("Unknown err:", e, urli)
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
            print("url", league_url)
            print("name", league_name)
            print("country", league_country)
            print("clubs", league_clubs)
            print("players", league_players)
            print("avg_age", league_avg_age)
            print("foreigners", league_foreigners)
            print("total_market_value", league_total_market_value)
            print("")
            get_clubs(league_url)



# trunk-ignore(ruff/E402)
from parsel import Selector
string1 = "https://www.transfermarkt.co.uk/"
string2 = "?saison_id="

def get_clubs(league_url):
    # getting club info from all seasons of the league in leagues table
    response = requests.get(league_url, headers=headerz)
    # soup = BeautifulSoup(response.content, 'html.parser')
    secici = Selector(response.text)

    for seasons in secici.xpath("//select[@data-placeholder='Filter by season']/option"):
        season_year = seasons.xpath('./@value').get()
        league_href = seasons.xpath('//*[@id="subnavi"]/@data-path').get()
        league_href = string1 + league_href + string2 + season_year
        # last year data is empty, thats why we need to check
        if season_year != str(datetime.now().year):
            print(league_href)
        else:
            continue # go to next season

        league_href_response = requests.get(league_href, headers=headerz)
        league_href_soup = BeautifulSoup(league_href_response.content, "html.parser")

        # getting first and second season filtered league banner info
        # banner 1
        for banner_info in league_href_soup.select("div.data-header__club-info"):
            league_country_name = banner_info.find("span", attrs={'class': 'data-header__club'}).text.strip()
            league_level_name = banner_info.find("span", attrs={'class': 'data-header__content'}).text.strip()
            league_reigning_champion = banner_info.findAll("span", attrs={'class': 'data-header__content'})[1].text.strip()
            league_record_holding_champion = banner_info.findAll("span", attrs={'class': 'data-header__content'})[2].a.get_text()
            league_record_holding_champion_value = banner_info.findAll("span", attrs={'class': 'data-header__content'})[3].get_text(strip=True)
            league_uefa_coefficient = banner_info.findAll("span", attrs={'class': 'data-header__content'})[5].a.get_text(strip=True)
            league_uefa_coefficient_value = banner_info.findAll("span", attrs={'class': 'data-header__content'})[6].get_text(strip=True)
            print(league_country_name)
            print(league_level_name)
            print(league_reigning_champion)
            print(league_record_holding_champion)
            print(league_record_holding_champion_value)
            print(league_uefa_coefficient)
            print(league_uefa_coefficient_value)
            print("")

        # banner2
        for x in league_href_soup.select("div.data-header__headline-container"):
            league_name = x.find("h1", attrs={'class': 'data-header__headline-wrapper data-header__headline-wrapper--oswald'}).get_text(strip=True)
            print(league_name)

        for x in league_href_soup.select("div.data-header__details"):
            league_num_of_clubs = x.findAll("span", attrs={'class': 'data-header__content'})[0].get_text(strip=True).strip()
            league_num_of_players = x.findAll("span", attrs={'class': 'data-header__content'})[1].get_text(strip=True).strip()
            league_num_of_foreigners = x.findAll("span", attrs={'class': 'data-header__content'})[2].get_text(strip=True).split('\xa0')[0].strip()
            league_num_of_foreigners_percentage = x.findAll("span", attrs={'class': 'tabellenplatz'})[0].get_text(strip=True).strip()
            league_market_value = x.findAll("span", attrs={'class': 'data-header__content'})[3].get_text(strip=True).strip()
            league_avg_market_value = x.findAll("span", attrs={'class': 'data-header__content'})[4].get_text(strip=True).strip()
            league_most_player_valuable = x.findAll("span", attrs={'class': 'data-header__content'})[-1].get_text(strip=True)
            print(league_num_of_clubs)
            print(league_num_of_players)
            print(league_num_of_foreigners,'Players',league_num_of_foreigners_percentage)
            print(league_market_value)
            print(league_avg_market_value)
            print(league_most_player_valuable)
            print("")

        for detail_data in league_href_soup.select('tr.odd,tr.even'):
            team = detail_data.find('td', {'class': 'hauptlink no-border-links'}).get_text(strip=True)
            team_link = detail_data.find('td', {'class': 'hauptlink no-border-links'}).select('a')[0]['href']
            squad = detail_data.findAll('td')[2].get_text()
            team_age = detail_data.findAll('td')[3].get_text()
            team_foreigners = detail_data.findAll('td')[4].get_text()
            t_avg_market_value = detail_data.findAll('td')[5].get_text()
            t_ttl_market_value = detail_data.findAll('td')[6].get_text()

            print(team)
            print(team_link)
            print(squad)
            print(team_age)
            print(team_foreigners)
            print(t_avg_market_value)
            print(t_ttl_market_value)
            print("")

            exit()




if __name__ == "__main__":

    get_leagues(url)
    print("                           ")
