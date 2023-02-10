# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:24:29 2022

@author: FIRATKABAN
"""

from bs4 import BeautifulSoup    # bs4 kütüphanesini import ediyoruz
import requests                  # requests kütüphanesini import ediyoruz
import time
import subprocess


def lig(sıra): # sıra 0 dan başlar
    
    # user agent kimliğimizi belirtiyoruz, bu sayede transfermarkt sitesine giriş yapmış gibi gözüküyoruz. 
    HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/45.0.2454.101 Safari/537.36')}
    
    url = "https://www.transfermarkt.co.uk/wettbewerbe/europa"

    reponse = requests.get(url,headers=HEADERS) # sadece requests.get() kullanacagiz. post put del yok.
    ss = BeautifulSoup(reponse.content,"lxml")
    
    
    
    xv1 =ss.find_all('table',attrs={"class":"inline-table"})[sıra].find_all("a")[1].get("href")
    return xv1


def sezonlar():

    HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                              'AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/45.0.2454.101 Safari/537.36')}
    
    # for all lig
    # TODO: pagination'dan tum ligleri getir
    for i in range(0,433):
        rl=lig(i)
        url=f"https://www.transfermarkt.co.uk{rl}"
        res=requests.get(url,headers=HEADERS)
        ss=BeautifulSoup(res.content,"lxml")
        xv1 =ss.find_all('option')

        for i in xv1:
            vl=i.get("value")
            print(f"{url}/plus/?saison_id={vl}")
            time.sleep(0.1)
        
        
        
if __name__ == "__main__":
    
    if subprocess.call("transfermarkt.co.uk", shell=True) == 0:
    sezonlar()

"""
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2022
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2021
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2020
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2019
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2018
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2017
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2016
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2015
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2014
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2013
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2012
https://www.transfermarkt.co.uk/efbet-liga/startseite/wettbewerb/BU1/plus/?saison_id=2011
.
.
.
# TODO: her ilgili linkte veri var mi yok mu kontrol edilmesi gerekiyor.

# TODO: veri varsa veri çekilmesi gerekiyor. YOKSA, no data yazdırılması gerekiyor.

# her bir url stringinden elde edilecektir.
# link1, sezon(year), link2(lastState), ligAdi, ligKodu, ligdekitakimsayısı, ligoyuncusayısı,ligdekiyabancıoyuncusayısı,
# ligdeğeri , ligintoplamdeğeri 


# https://www.transfermarkt.co.uk/laliga/startseite/wettbewerb/ES1/plus/?saison_id=2022
# ilgili her url response'unsan once sag ust examp: SPAIN tablosundaki satirlar,
# ardindan ikinci, hemen altindaki tablodaki satirlar

# daha sonra hemen altindaki takimlar tablosundan veriler asagidaki gibi cekilecek
# takımların tablosu (her bir sezondan takımların tablosu ve sutunlarin hepsi cekilecek)
# takım adı , squad , average age , foreigners , average market value , total market value

# takimlar tablosuna ek olarak, takim adina baglanmis olan link de alinacak



.. takimdan alinan linklerden yolaca cikarak oyuncular elde edilecek
.. oyuncular linkelerinden yola cikarak performans etc value

# pgAdmin                                                ! OK (aws config)
# postgresql veritabani ?                                ! OK (configuration)
# aws ec2 instance ?  https://aws.amazon.com/tr/pgadmi   ! OK 

# pagination firat bakacak



"""

