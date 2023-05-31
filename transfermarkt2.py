# -*- coding: utf-8 -*-
""".

Created on Tue Sep 13 13:24 2022
Updated on Sun Feb 26 12:13 2023
Updated on Wed May 31 13:29 2023

@author: FIRATKABAN
@contributer: cerebnismus
"""


import requests
from bs4 import BeautifulSoup

url = "https://www.transfermarkt.co.uk/wettbewerbe/europa"

headerz = {
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/45.0.2454.101 Safari/537.36"
    )
}


def get_leagues(url):
    """.
    This function gets the leagues data with pagination.
    """
    try:
        r = requests.get(url, headers=headerz)
        soup = BeautifulSoup(r.content, "html.parser")
        page = soup.find("div", {"class": "pager"})
        stri = page.find_all("li")[-1].a.get("href")
        substring = stri[76:]
        print("string:", stri)
        print("substring:", substring)

        return stri
    # trunk-ignore(ruff/E722)
    except:
        print("Pagination error on get_leagues function")
        return 0


if __name__ == "__main__":
    get_league_pagination(main_url)
    get_league_links(pagination)
    get_all_seasons()

    print(league_href)
    print(season_year)
    print(url_season_list)

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
