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
    print("URL compl    :", url)
    print("URL string   :", stri)
    print("URL substring:", substring)

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




if __name__ == "__main__":

    get_leagues(url)
    print("                           ")
