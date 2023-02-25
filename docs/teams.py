from bs4 import BeautifulSoup       # bs4 kütüphanesini import ediyoruz
import requests                     # requests kütüphanesini import ediyoruz
from requests import Session        #

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36')}

teams = {} # banner icin

# TODO: PRINT SATIRLARI DB YE YAZILACAK SEKILDE GUNCELLENECEK

def get_seasons():
    
    response = requests.get('https://www.transfermarkt.co.uk/manchester-city/kader/verein/281/saison_id/2022/plus/1', headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    for allseason in soup.select("div.data-header__club-info"):
        # lig kodunu split yapıp sözlüğe yazdıracaz.
        league = allseason.find("span", attrs={'class': 'data-header__club'})
        country = allseason.find(
            "span", attrs={'class': 'data-header__content'})
        league_level = allseason.find(
            "span", attrs={'class': 'data-header__content'})
        tableposition = allseason.findAll(
            "span", attrs={'class': 'data-header__content'})[1]
        In_leaguesince = allseason.findAll(
            "span", attrs={'class': 'data-header__content'})[2]

    try:
        teams['league'] = league.a.get_text(strip=True)
        teams['team_country'] = country.find('img')['alt']
        teams['league_level'] = league_level.a.get_text(strip=True)
        teams['teams_position'] = tableposition.a.get_text(strip=True)
        teams['in_league_since'] = In_leaguesince.a.get_text(strip=True)

    except AttributeError:
        teams['league'] = ('AttributeError')
        teams['team_country'] = ('AttributeError')
        teams['league_level'] = ('AttributeError')
        teams['teams_position'] = ('AttributeError')
        teams['in_league_since'] = ('AttributeError')

    except IndexError:
        teams['league'] = ('IndexError')
        teams['team_country'] = ('IndexError')
        teams['league_level'] = ('IndexError')
        teams['teams_position'] = ('IndexError')
        teams['in_league_since'] = ('IndexError')

    except Exception as f:
        teams['league'] = (f)
        teams['team_country'] = (f)
        teams['league_level'] = (f)
        teams['teams_position'] = (f)
        teams['in_league_since'] = (f)

    for allseason1 in soup.select("div.data-header__details"):
        # takımın sezonu ve linkini split yapacaz ve sözlüğe yazdıracaz.
        team_name = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[4]
        squad1 = allseason1.find(
            "span", attrs={'class': 'data-header__content'})
        age1 = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[1]
        foreigners1 = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[2]
        foreigners_player_percant1 = allseason1.findAll(
            "span", attrs={'class': 'tabellenplatz'})[0]
        nationality_players = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[3]
        stadium = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[4]
        seats = allseason1.findAll("span", attrs={'class': 'tabellenplatz'})[1]
        transfer_record = allseason1.findAll(
            "span", attrs={'class': 'data-header__content'})[5]
    try:

        teams['team_name'] = team_name.a.get('title')
        teams['teams_squad'] = squad1.get_text(strip=True)
        teams['teams_age'] = age1.get_text(strip=True)
        teams['teams_foreigner_players'] = foreigners1.a.get_text(strip=True)
        teams['teams_foreigner_players_percant'] = foreigners_player_percant1.get_text(strip=True)
        teams['teams_national'] = nationality_players.a.get_text(strip=True)
        teams['teams_stadium_name'] = stadium.a.get_text(strip=True)
        teams['teams_stadium_seats'] = seats.get_text(strip=True)
        teams['teams_transfer_record'] = transfer_record.a.get_text(strip=True)

    except AttributeError:
        teams['team_name'] = ('AttributeError')
        teams['teams_squad'] = ('AttributeError')
        teams['teams_age'] = ('AttributeError')
        teams['teams_foreigner_players'] = ('AttributeError')
        teams['teams_foreigner_players_percant'] = ('AttributeError')
        teams['teams_national'] = ('AttributeError')
        teams['teams_stadium_name'] = ('AttributeError')
        teams['teams_stadium_seats'] = ('AttributeError')
        teams['teams_transfer_record'] = ('AttributeError')

    except IndexError:
        teams['team_name'] = ('IndexError')
        teams['teams_squad'] = ('IndexError')
        teams['teams_age'] = ('IndexError')
        teams['teams_foreigner_players'] = ('IndexError')
        teams['teams_foreigner_players_percant'] = ('IndexError')
        teams['teams_national'] = ('IndexError')
        teams['teams_stadium_name'] = ('IndexError')
        teams['teams_stadium_seats'] = ('IndexError')
        teams['teams_transfer_record'] = ('IndexError')

    except Exception as f:
        teams['team_name'] = (f)
        teams['teams_squad'] = (f)
        teams['teams_age'] = (f)
        teams['teams_foreigner_players'] = (f)
        teams['teams_foreigner_players_percant'] = (f)
        teams['teams_national'] = (f)
        teams['teams_stadium_name'] = (f)
        teams['teams_stadium_seats'] = (f)
        teams['teams_transfer_record'] = (f)

    print('\n\n')


    for player_data in soup.select('tr.odd,tr.even'):
        
        # TODO: TRY EXCEPT EKLENECEK
        shirt_number = player_data.find('td', attrs={'class': 'zentriert'}).get_text(strip=True)  # futbolcunun forma numarası
        player = player_data.find('td', {'class': 'hauptlink'}).get_text(strip=True)  # futbolcunun adı
        playerlink = player_data.find('td', {'class': 'hauptlink'}).a.get('href')  # futbolcunun sayfa linki
        mainposition = player_data.findAll('td')[4].get_text(strip=True)  # futbolcunun ana mevkisi
        dateofbirth = player_data.findAll('td')[5].get_text(strip=True)[:12]  # futbolcunun doğum tarihi
        birthday = player_data.findAll('td')[5].get_text(strip=True)[4:6]  # futbolcunun doğum günü
        birthmonth = player_data.findAll('td')[5].get_text(strip=True)[0:4]  # futblcunun doğum ayı
        birthyear = player_data.findAll('td')[5].get_text(strip=True)[8:12]  # futblcunun doğum yılı
        age = player_data.findAll('td')[5].get_text(strip=True)[14:16]  # futbolcunun yaşı
        nat1 = player_data.findAll('td')[6].img['alt']  # futbolcunun ulkeleri
        nat2 = player_data.findAll('td')[6].img['alt']
        height = player_data.findAll('td')[7].get_text(strip=True)  # futbolcunun boyu
        foot = player_data.findAll('td')[8].get_text(strip=True)  # futbolcunun kullandığı ayak
        joined = player_data.findAll('td')[9].get_text(strip=True)[:12]  # takıma katıldığı tarih
        joined_day = player_data.findAll('td')[9].get_text(strip=True)[:6]  # takıma katıldığı gün
        joined_month = player_data.findAll('td')[9].get_text(strip=True)[0:4]  # takıma katıldığı ay
        joined_year = player_data.findAll('td')[9].get_text(strip=True)[8:12]  # takıma katıldığı yıl
        previousteam = player_data.findAll('td')[10].img['alt']  # önceki takımı
        contractdate = player_data.findAll('td')[11].get_text(strip=True)[:12]  # kontrat tarihi
        contractday = player_data.findAll('td')[11].get_text(strip=True)[:6]  # kontrat günü
        contractmonth = player_data.findAll('td')[11].get_text(strip=True)[0:4]  # kontrat ayı
        contractyear = player_data.findAll('td')[11].get_text(strip=True)[8:12]  # kontrat yılı
        marketvalue = player_data.findAll('td')[12].get_text(strip=True)
        
        try:
            print('\n')
            print('shirt_number: ', shirt_number) 
            print('player: ', player)
            print('playerlink: ', playerlink)
            print('mainposition: ', mainposition)
            print('dateofbirth: ', dateofbirth)
            print('birthday: ', birthday)
            print('birthmonth: ', birthmonth)
            print('birthyear: ', birthyear)
            print('age: ', age)
            print('nat1: ', nat1)
            print('nat2: ', nat2)
            print('height: ', height)
            print('foot: ', foot)
            print('joined: ', joined)
            print('joined_day: ', joined_day)
            print('joined_month: ', joined_month)
            print('joined_year: ', joined_year)
            print('previousteam: ', previousteam)  
            print('contractdate: ', contractdate)
            print('contractday: ', contractday)
            print('contractmonth: ', contractmonth)
            print('contractyear: ', contractyear)
            print('marketvalue: ', marketvalue)
        except:
            pass



if __name__ == "__main__":
    # get_league_pagination(main_url)
    # get_league_links(pagination)
    get_seasons()
    # print all lists
    print(teams)


# TO DO LİST
# 2 uyruklu oyuncuların ikinci uyruk bilgisi alınacak.
# Gidelen takımın sayfasının linki,id bilgisi ve sezon bilgisi sözlüğe yazılacak.
# Takımın ikinci total market value si kısmını istek atmadan nasıl alınacağını bulacağım.
# Para birimlerinin yanındaki para sembolleri kalkmalı (split ile)
# Oyuncu boy bilgisinin yanındaki m harfi kalkmalı (split ile)
# İn league since alanındaki years kelimesi gidecek (split ile)
# Zaman datalarına bir daha bakacağım.