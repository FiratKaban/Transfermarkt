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


leagues_pages = []
leagues_links = []

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
            leagues_links.append(main_url+leagues_link.select("a")[1]["href"])
            print(main_url+leagues_link.select("a")[1]["href"])



    return 0


if __name__ == "__main__":
    get_leagues(url)
    print(leagues_links)
    print("                           ")
