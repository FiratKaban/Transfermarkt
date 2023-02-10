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
        musabakalinkleri2 = list(map(lambda orig_string: orig_string + string +vl, musabakalinkleri1))
