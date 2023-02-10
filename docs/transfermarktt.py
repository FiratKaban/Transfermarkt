import requests
from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np
import csv
import pandas as pd
import time 
import random



### WEB CRAWLİNG #####

headers = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36')}

musabakalinkleri = []  
for i in range(1,18):
    url='https://www.transfermarkt.co.uk/wettbewerbe/europa?page='
    sayfa = url+str(i)
    musabakalinkleri.append(sayfa)
##############################################################
musabakalinkleri1=[]
for i in range(len(musabakalinkleri)):
    tree = requests.get(musabakalinkleri[i], headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')
    print(f'FIRAT KABAN ; {musabakalinkleri[i]}')
    e = soup.select("tr.odd, tr.even")
    for i in e:
        musabakalinkleri1.append(i.select("a")[1]["href"])
for j in range(len( musabakalinkleri1)):
       musabakalinkleri1[j] = "https://www.transfermarkt.co.uk"+ musabakalinkleri1[j]



yillar=[]
string = "/plus/?saison_id="


for i in range(len(musabakalinkleri1)):
    tree = requests.get(musabakalinkleri1[i], headers = headers)
    ss = BeautifulSoup(tree.content, 'lxml')
    xv1 =ss.find_all('option')
    for i in xv1:
        vl=i.get("value")
        musabakalinkleri2 = list(map(lambda orig_string: orig_string + vl, musabakalinkleri1))












string = "/plus/?saison_id="






denemelinki = musabakalinklerison[31:33]

liglevel = [] #First Tier
for musabaka in range(len(denemelinki)):
    tree = requests.get(denemelinki[musabaka], headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')
    tablo = soup.find('div',{'class':'list'})
    tablo2 = tablo.find('table',{'class':'profilheader'})
    tablo3 = tablo2.find_all('tr')
    tablo4 = tablo3.find_all('td')
    for each_level in tablo4:
        print(each_level.get_text(strip=True))



liglevel = []
num_of_teams = []
num_of_players = []
num_of_foreigners = []



for musabaka in range(len(denemelinki)):
    tree = requests.get(denemelinki[musabaka], headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')
    tablo = soup.find('div',{'class':'list'})
    tablo2 = tablo.find('table',{'class':'profilheader'})
    tablo3 =tablo2.find_all('tr')
    sayac = 0
    for musabakabilgileri in tablo3:
        data1 = musabakabilgileri.find('td')
        if data1 is not None:
            # eğer sayac == 0 ise
            if sayac == 0: # tr taginde sıfırıncı eleman lig level
                liglevel.append(musabakabilgileri.get_text(strip=True))
            elif sayac == 1: # tr taginde sıfırıncı eleman lig level
                num_of_teams.append(musabakabilgileri.get_text(strip=True))
            elif sayac == 2: # tr taginde sıfırıncı eleman lig level
                num_of_players.append(musabakabilgileri.get_text(strip=True))
            elif sayac == 3: # tr taginde sıfırıncı eleman lig level
                num_of_foreigners.append(musabakabilgileri.get_text(strip=True))
            

        else:
            liglevel.append("Lig Level Mevcut Değilir.")
            num_of_teams.append("Lig Level Mevcut Değilir.")
            num_of_players.append("Lig Level Mevcut Değilir.")
            num_of_foreigners.append("Lig Level Mevcut Değilir.")

        sayac += 1
        






###TAKIMLARIN SAYFASININ LİNKLERİNİ ALMAYA ÇALIŞTIM.
teams  =  [] 
for i in range(len(sonlink)):
    tree = requests.get(sonlink[i], headers = headers)
    print(f'FIRAT KABAN ; {sonlink[i]}')
    soup = BeautifulSoup(tree.content, 'html.parser')
    time.sleep(random.randint(1,3))
    k = soup.find_all('td', {'class': 'hauptlink no-border-links hide-for-small hide-for-pad'})
    for a in range(len(k)):
         teams.append(k[a].a.get('href'))
for j in range(len(teams)):
     teams[j] = "https://www.transfermarkt.com.tr"+teams[j]

####OYUNCULARIN SAYFASININ LİNKLERİNİ ALMAYA ÇALIŞTIM.
playerlinks = []
for i in range(len(teams)):
    tree = requests.get(teams[i], headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')
    print(f'FIRAT KABAN ; {teams[i]}')
    k = soup.find_all('div', {'class':'di nowrap'})
    for a in range(len(k)):
      playerlinks.append(k[a].a.get('href'))
for j in range(len(playerlinks)):
     playerlinks[j] = "https://www.transfermarkt.com.tr"+playerlinks[j]

playerlinks = list(set(playerlinks))

players = playerlinks[0:11]
#######  WEB CRAWLİNG #####

results = [r.text.split(' ')[0].strip() for r in all_results]
print(results)



#SOUP'DA SELECT KULLANIMINI İYİCE ARAŞTIRACAZ....
        
###### WEB SCRAPE ########

oyuncu=[]
for i in range(len(players)):
    tree = requests.get(players[i])
    print(f'\t FIRAT KABAN: {players[i]}')
    soup1 = BeautifulSoup(tree.content, 'lxml')
    content = soup1.select('div')    






############################


    
############################


