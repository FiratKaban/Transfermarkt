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
        


link=[]
def get_seasons():
    """ Bu fonksiyon, liglerin sezonlarini alir. """
    for league in range(len(leagues)):
        response = requests.get(leagues[league], headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        link.append(soup.find(name="div", attrs={"class": "row hide-on-print"}).get("data-path"))
        link.append(soup.find_all("option")[-1].get("value"))
      
      
      
# for i in link:
    
    # i -> datapath url in database  
    # i++
    # if i == 2023 then break
    
    
    # print(link)
        
        # XXX: bu formatta biz bir ligin sezonlarini almak yerine
        # XXX: bir ligdeki ilk sezonun baslangic yilini aliyoruz. orn: 1928
        # XXX: bu yuzden bundan sonraki fonksiyona try catch bloklari ekleyerek
        # XXX: hata aldigimizda ilgili ligin o sezon yilinda aktif olmadigini anlayacagiz.
        
        
    

"""
        for seasons in selected_text.xpath("//select[@data-placeholder='Filter by season']/option"):
            season.append(seasons.xpath('./@value').get())
            link.append(seasons.xpath('//*[@id="subnavi"]/@data-path').get())
            print(season)
            print(link)
            sys.exit()
            
    




string1 = "https://www.transfermarkt.co.uk/"
string2 = "?saison_id="



url_season_list = []
for x, y in zip(link,season):
    url = string1 + x + string2 + y
    url_season_list.append(url)
print(url_season_list)

"""

# main
if __name__ == "__main__":
    get_league_pagination(main_url)
    get_league_links(pagination)
    get_seasons()
    
    
