# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 00:01:05 2022

@author: FIRATKABAN
"""




from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

#######################################################################
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
#######################################################################
    
def generalUrl(urlText): return 'https://www.transfermarkt.com.tr'+urlText+'/plus/1'
def generalUrl2(urlText): return 'https://www.transfermarkt.com.tr'+urlText

#text='10,50 mill. €'
#text='1,50 mill. € '

def standardvalue(text):
    textt1='mil'
    textt2='mill'
    
    text=text.replace('€','')
    text=text.replace(',','')
    
    index = text.find(' ')
    importAux=text[:index]
    
    if textt2 in text:
        importt=importAux+'0000'
    elif textt1 in text:
        importt=importAux+'000'
    else:
        importt=0
    return importt


listligs=['https://www.transfermarkt.com.tr/laliga/startseite/wettbewerb/ES1']


print(datetime.now().time())
print("Veriler Toplanıyor.")

url_team_link_total=[]


playername_list=[]
playernumber_list=[]
team_list=[]
lig_list=[]
date_of_birth_list=[]
date_of_year_list=[]
age_list=[]
nationality_list=[]
nationality2_list=[]
height_list=[]
foot_list=[]
date_joined_team_list=[]
contract_end_date_list=[]
contract_end_year_list=[]
current_market_value_list=[]
player_link_list=[]


for url in listligs:
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')
    team_name = soup.find_all('td',class_='zentriert')
    
#Gideceğimiz sayfaların linklerini elde ediyoruz
    url_team_list=[]
    nteams=int(soup.find('table',class_='profilheader').find_all('tr')[1].find('td').text.replace('\n','').replace(' ','')[:2])
    iUrl=4;
    total=nteams*iUrl  
    while(iUrl<=total): 
        urlTeamDetails=generalUrl(team_name[iUrl].find_all('a')[0]['href'])
         #takımların url'si ile oyuncuların özelliklerini elde edeceğiz.
        page = requests.get(urlTeamDetails, headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')
        
        playername=soup.find_all('td',class_='hauptlink')
        tableItems1=soup.find_all('tr',class_='odd')
        tableItems2=soup.find_all('tr',class_='even')
        #-- Transfermarktta çift satırların uzunluğu sınıfı tek satırlardan farklı
        # - tek satırların sınıflarının çift satırlardan uzun olup olmadığını kontrol ediyoruz.
        # bunun sonucunda karşılık gelen değerleri ilgili listeye atacağız.
        
        if len(tableItems2)==len(tableItems1): nPar=nImpar=len(tableItems1)
        else:
            nImpar=len(tableItems1)
            nPar=len(tableItems2)
        #-- çekmek istediğimiz bilgilere gideceğiz.
        iPlayerName=0;
        nElements=(nImpar+nPar)*2
        while(iPlayerName<nElements):            
            playername_list.append(playername[iPlayerName].find('a').text.rstrip().lstrip())
            lig_data = soup.find('span',class_='hauptpunkt')
            if lig_data is not None:
              lig_list.append(lig_data.text.replace('\n','').rstrip().lstrip())
            else:
                lig_list.append('Lig Mevcut Değildir.')
            iPlayerName+=2
        #--# Her oyuncunun verilerini listelere kaydetmek için 1 takım listesini gözden geçiriyoruz 
        team_link_list=[]
        i=0;
        while(i<nPar):
            #Oyuncunun forma numarasını elde edeceğiz.
            playernumber_list.append(tableItems1[i].find_all('td',class_='zentriert')[0].text)
            playernumber_list.append(tableItems2[i].find_all('td',class_='zentriert')[0].text)
            #Doğum Tarihi, Doğum Yılı ve Yaş Verileri EldeEdilecek.
            date_of_birth_age=tableItems1[i].find_all('td',class_='zentriert')[1].text
            date_of_birth=date_of_birth_age[:11] #doğum tarihi datasını elde edeceğiz.
            Year=date_of_birth_age[6:11]         #doğum yılı datasını elde edeceğiz.
            Age=date_of_birth_age[11:14]#oyuncunun yasışını elde deceğiz.
            age_list.append(Age)
            date_of_year_list.append(Year)
            date_of_birth_list.append(date_of_birth)
            
            date_of_birth_age=tableItems2[i].find_all('td',class_='zentriert')[1].text
            date_of_birth=date_of_birth_age[:11] 
            Year=date_of_birth_age[6:11] 
            Age=date_of_birth_age[11:14] 
            age_list.append(Age)
            date_of_year_list.append(Year)
            date_of_birth_list.append(date_of_birth)
            
            nationality_list.append(tableItems1[i].find_all('td',class_='zentriert')[2].find_all('img')[0]['alt'])
            nationality_list.append(tableItems2[i].find_all('td',class_='zentriert')[2].find_all('img')[0]['alt'])            
            if (len(tableItems1[i].find_all('td',class_='zentriert')[2].find_all('img')) >1):
               nationality2_list.append(tableItems1[i].find_all('td',class_='zentriert')[2].find_all('img')[1]['alt'])
            else:
               nationality2_list.append(' ')
           
            if (len(tableItems2[i].find_all('td',class_='zentriert')[2].find_all('img')) >1):
               nationality2_list.append(tableItems2[i].find_all('td',class_='zentriert')[2].find_all('img')[1]['alt'])
            else:
               nationality2_list.append(' ')
            # metin bölümünü kaldırarak ve ',' ile '.' olarak değiştirerek oyuncunun boyunu ekleyeceğiz.
            height_meters=tableItems1[i].find_all('td',class_='zentriert')[3].text
            height=height_meters[:4] 
            height=height.replace(',','.')
            height_list.append(height)
            height_meters=tableItems2[i].find_all('td',class_='zentriert')[3].text
            height=height_meters[:4] 
            height=height.replace(',','.')
            height_list.append(height)
            
            #Oyuncunun ayak özelliğini ekleyeceğiz.

            foot_list.append(tableItems1[i].find_all('td',class_='zentriert')[4].text)
            foot_list.append(tableItems2[i].find_all('td',class_='zentriert')[4].text)
            
            #Oyuncunun takıma katıldığı tarihi ekleyeceğiz.
            date_joined_team_list.append(tableItems1[i].find_all('td',class_='zentriert')[5].text)
            date_joined_team_list.append(tableItems2[i].find_all('td',class_='zentriert')[5].text)
            
            #Oyuncunun sözleşme bitiş tarihini ekleyecepğiz
            contract_end_date_list.append(tableItems1[i].find_all('td',class_='zentriert')[7].text)
            contract_end_year_list.append(tableItems1[i].find_all('td',class_='zentriert')[7].text[6:11])    
            contract_end_date_list.append(tableItems2[i].find_all('td',class_='zentriert')[7].text)
            contract_end_year_list.append(tableItems2[i].find_all('td',class_='zentriert')[7].text[6:11])
            
           #oyuncunun güncel piyasa edeğerini ekleyeceğiz.
            current=tableItems1[i].find_all('td',class_='rechts hauptlink')[0].text
            current_market_value_list.append(standardvalue(current))
            current=tableItems2[i].find_all('td',class_='rechts hauptlink')[0].text
            current_market_value_list.append(standardvalue(current))
            
            #Oyuncunun linkini ekleyeceğiz.
            player_link_list.append(tableItems1[i].find('td',class_='hauptlink').find('a')['href'])
            player_link_list.append(tableItems2[i].find('td',class_='hauptlink').find('a')['href'])

            i+=1;
    
        if(nPar!=nImpar): 
            playernumber_list.append(tableItems1[i].find_all('td',class_='zentriert')[0].text)
            
            date_of_birth_age=tableItems1[i].find_all('td',class_='zentriert')[1].text
            date_of_birth=date_of_birth_age[:11] 
            year=date_of_birth_age[6:11] 
            Age=date_of_birth_age[11:14] 
            age_list.append(Age)
            date_of_year_list.append(Year)
            date_of_birth_list.append(date_of_birth)
            
            nationality_list.append(tableItems1[i].find_all('td',class_='zentriert')[2].find_all('img')[0]['alt'])
            if (len(tableItems1[i].find_all('td',class_='zentriert')[2].find_all('img')) >1):
                nationality2_list.append(tableItems1[i].find_all('td',class_='zentriert')[2].find_all('img')[1]['alt'])
            else:
                nationality2_list.append(' ')
            
            height_meters=tableItems1[i].find_all('td',class_='zentriert')[3].text
            height=height_meters[:4] 
            height=height.replace(',','.')
            height_list.append(height)
    
            foot_list.append(tableItems1[i].find_all('td',class_='zentriert')[4].text)
    
            date_joined_team_list.append(tableItems1[i].find_all('td',class_='zentriert')[5].text)
    
            contract_end_date_list.append(tableItems1[i].find_all('td',class_='zentriert')[7].text)
            contract_end_year_list.append(tableItems1[i].find_all('td',class_='zentriert')[7].text[6:11])    
    
            current=tableItems1[i].find_all('td',class_='rechts hauptlink')[0].text
            current_market_value_list.append(standardvalue(current))
            
            player_link_list.append(tableItems1[i].find('td',class_='hauptlink').find('a')['href'])

        iUrl+=4
        
    url_team_link_total= url_team_link_total+url_team_list
print(datetime.now().time())
list_parameter = [playername_list,playernumber_list,team_list,lig_list,date_of_birth_list,
               date_of_year_list,age_list,nationality_list,nationality2_list,height_list,
               foot_list,date_joined_team_list,contract_end_date_list,contract_end_year_list,
               current_market_value_list,player_link_list,]
parameter=['PlayerName','PlayerNumber','PlayerTeam','Ligs','PlayerBirthDay','PlayerBirthYear',
           'PlayerAge','PlayerNationality1','PlayerNationality2','PlayerHeight','PlayerFoot',
           'PlayerJoinedTeam','PlayerContractEnd','PlayerContractEndYear','PlayerValue','PlayerLinks']
Transfermarkt_Dataframe=pd.DataFrame(list_parameter).T
Transfermarkt_Dataframe.columns=parameter
print(datetime.now().time())
print('Veri Çerçevesi Oluşturuldu')
#KODLARIMDA 263. SATIR SONRASINDA SORUNLARIM MEVCUTTUR.
#KODLARIM BU KISIMA KADAR ÇALIŞIYOR.
#AMA AŞAĞI SATIRLARDA SADECE 
#AttributeError: 'Series' object has no attribute 'url'
#BU HATAYI ALIYORUM.

position1List=[]
position2List=[]

i=0
while i<len(Transfermarkt_Dataframe):
    urlPlayer=generalUrl(Transfermarkt_Dataframe.loc[i]["PlayerLinks"])    
    page = requests.get(urlPlayer, headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')

    nPos=len(soup.find('div',class_='detail-position__box').find_all('dd'))
    position1List.append(soup.find('div',class_='detail-position__box').find_all('dd')[0].text)
    if(nPos>=2):
        position2List.append(soup.find('div',class_='detail-position__box').find_all('dd')[1].text)
    else:
        position2List.append(' ')
    i+=1
    
print(datetime.now().time())
print('DataFrame Oluşturuldu.')

for player1 in range(len(player_link_list)):
       player_link_list[player1] = "https://www.transfermarkt.com.tr"+player_link_list[player1]


place_birth_list=[]
consultancy_company_list=[]
contract_end_renewal_list=[]
outfitter_list=[]
rrss_list=[]

i=0
nPlayer=(len(Transfermarkt_Dataframe))
while i<nPlayer:
        urlPlayer=generalUrl(Transfermarkt_Dataframe.loc[i]["PlayerLinks"])
        page = requests.get(urlPlayer, headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')
        section_label=soup.find_all('span',class_='info-table__content info-table__content--regular')
        section_value=soup.find_all('span',class_='info-table__content info-table__content--bold  info-table__content--flex')
        j=0    
        elements=len(section_label)
        rrss=outfitter=contract_end_renewal=consultancy_company=birth=False
        while(j<elements):
                    if (section_label[j].text.find('PlayerPlaceBirth')!=-1):
                        place_birth_list.append(section_value[j].text.replace('\n','').replace('\xa0',''))
                        birth=True
                    elif (section_label[j].text.find('PlayerConsultancyCompany')!=-1):
                        consultancy_company_list.append(section_value[j].text.replace('\n','').replace('\xa0',''))
                        consultancy_company=True
                    elif (section_label[j].text.find('PlayerContractRenwal')!=-1):
                        contract_end_renewal_list.append(section_value[j].text.replace('\n','').replace('\xa0',''))
                        contract_end_renewal=True
                    elif (section_label[j].text.find('PlayerOutfitter')!=-1):
                        outfitter_list.append(section_value[j].text.replace('\n','').replace(' ',''))
                        outfitter=True         
                    elif (section_label[j].text.find('PlayerRsss')!=-1):
                        rrss_list.append(section_value[j].find_all('a')[0]['href'])
                        rrss=True
                    j+=1
        if(birth==False):
            place_birth_list.append(' ')
        if(consultancy_company==False):
            consultancy_company_list.append(' ')
        if(contract_end_renewal==False):
            contract_end_renewal_list.append(' ')
        if(outfitter==False):
            outfitter_list.append(' ')
        if(rrss==False):
            rrss_list.append(' ')
        i+=1
print(datetime.now().time())
print('DataFrame için yeni listeler oluşturuldu')

i=0
nPlayer=(len(Transfermarkt_Dataframe))

for k in range(len(player_link_list)):
    page = requests.get(player_link_list[k], headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')
    section_label=soup.find_all('span',class_='info-table__content info-table__content--regular')
    section_value=soup.find_all('span',class_='info-table__content info-table__content--bold')
    j=0    
    elements=len(section_label)
    rrss=outfitter=contract_end_renewal=consultancy_company=birth=False
    while(j<elements):
                if (section_label[j].text.find('PlayerPlaceBirth')!=-1):
                    place_birth_list.append(section_value[j].text.replace('\n','').replace('\xa0',''))
                    birth=True
                elif (section_label[j].text.find('PlayerConsultancyCompany')!=-1):
                        consultancy_company_list.append(section_value[j].text.replace('\n','').replace('\xa0',''))
                        consultancy_company=True
                elif (section_label[j].text.find('PlayerContractRenwal')!=-1):
                    contract_end_renewal_list.append(section_value[j].text.replace('\n','').replace('\xa0',''))
                    contract_end_renewal=True
                elif (section_label[j].text.find('PlayerOutfitter')!=-1):
                    outfitter_list.append(section_value[j].text.replace('\n','').replace(' ',''))
                    outfitter=True

                elif (section_label[j].text.find('PlayerRsss')!=-1):
                    rrss_list.append(section_value[j].find_all('a')[0]['href'])
                    rrss=True
                j+=1
    if(birth==False):
        place_birth_list.append(' ')
    if(consultancy_company==False):
        consultancy_company_list.append(' ')
    if(contract_end_renewal==False):
        contract_end_renewal_list.append(' ')
    if(outfitter==False):
        outfitter_list.append(' ')
    if(rrss==False):
        rrss_list.append(' ')
    i+=1
print(datetime.now().time())
print('DataFrame için yeni listeler oluşturuldu')
url

















