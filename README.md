### SQL STATEMENTS
```sql
-- LEAGUES
SELECT league_url, league_name, league_country, league_clubs, league_players, league_avg_age, league_foreigners, league_total_market_value
	FROM public.leagues;
	
-- LEAGUES_DATA
SELECT league_url, league_href, league_name, league_country_name, league_reigning_champion, league_record_holding_champion, league_record_holding_champion_value, league_uefa_coefficient, league_uefa_coefficient_value, league_num_of_clubs, league_num_of_players, league_num_of_foreigners, league_num_of_foreigners_percentage, league_market_value, league_avg_market_value, league_most_player_valuable
	FROM public.leagues_data;

-- LEAGUES + LEAGUES_DATA
SELECT l.league_url, l.league_name, l.league_country, l.league_clubs, l.league_players, l.league_avg_age, l.league_foreigners, l.league_total_market_value,
       ld.league_url, ld.league_href, ld.league_name, ld.league_country_name, ld.league_reigning_champion, ld.league_record_holding_champion, ld.league_record_holding_champion_value, ld.league_uefa_coefficient, ld.league_uefa_coefficient_value, ld.league_num_of_clubs, ld.league_num_of_players, ld.league_num_of_foreigners, ld.league_num_of_foreigners_percentage, ld.league_market_value, ld.league_avg_market_value, ld.league_most_player_valuable
FROM leagues l
JOIN leagues_data ld ON l.league_url = ld.league_url;

-- PLAYERS
SELECT shirt_number, player, playerlink, playerhref, mainposition, dateofbirth, birthday, birthmonth, birthyear, age, nat1, nat2, height, foot, joined, joined_day, joined_month, joined_year, previousteam, contractdate, contractday, contractmonth, contractyear, marketvalue
	FROM public.players;
	
-- PLAYERS_DATA
SELECT id, player_href, place_of_birth, foot, player_agent, player_agent_url, expires, player_outfitter, twitter, facebook, instagram
	FROM public.players_data;
	
-- PLAYERS + PLAYERS_DATA
SELECT p.shirt_number, p.player, p.playerlink, p.playerhref, p.mainposition, p.dateofbirth, p.birthday, p.birthmonth, p.birthyear, p.age, p.nat1, p.nat2, p.height, p.foot, p.joined, p.joined_day, p.joined_month, p.joined_year, p.previousteam, p.contractdate, p.contractday, p.contractmonth, p.contractyear, p.marketvalue,
       pd.id, pd.player_href, pd.place_of_birth, pd.foot, pd.player_agent, pd.player_agent_url, pd.expires, pd.player_outfitter, pd.twitter, pd.facebook, pd.instagram
FROM players p
JOIN players_data pd ON p.playerhref = pd.player_href;

-- TEAMS
SELECT team, team_link, team_href, squad, team_avg_age, team_foreigners, t_avg_market_value, t_ttl_market_value
	FROM public.teams;

-- TEAMS_DATA
SELECT league, team_country, team_href, league_level, teams_position, in_league_since, teams_foreigner_players_percant, teams_stadium_name, teams_stadium_seats, teams_transfer_record
	FROM public.teams_data;
	
-- TEAMS + TEAMS_DATA	
SELECT t.team, t.team_link, t.team_href, t.squad, t.team_avg_age, t.team_foreigners, t.t_avg_market_value, t.t_ttl_market_value,
       td.league, td.team_country, td.league_level, td.teams_position, td.in_league_since, td.teams_foreigner_players_percant,
       td.teams_stadium_name, td.teams_stadium_seats, td.teams_transfer_record
FROM teams t
JOIN teams_data td ON t.team_href = td.team_href;
```

### SOME NOTES ABOUT THE PROJECT

XXX insert_db.py ve create_db.py dosyalari transfermarkt2.py icine eklendi !

XXX !!! ONCE TRANSFERMARKT.PY NIN DUZGUN CALISTIGINDAN EMIN OLUN !!! XXX
ARALARA PRINT EKLEYIP CIKARARAK DEBUG YAPABILIRSIN

TODO: DEGISKENLERIN DB'DE KARSILIGI OLMALI
      BUNUN ICIN LUCIDCHART VB CROWS FOOT NOTASYONU VB BI EXCEL DE OLABIIR
      HAZIRLARSAN, HAZIR VERIYE GORE DB YAPISINI GUNCELLEYEBILIRIZ

      DB'ye ekleme fonsiyon ornekleri gosterecegim. AWS postgresql kullanacagiz.
      orneklere gore tum degiskenlerin DB'ye yazilmasi kismi sende.

TODO: Bu yapi daha sonra dictinary olarak degistirilebilir. Yonetmesi daha kolay olur

XXX: bu formatta biz bir ligin sezonlarini almak yerine
XXX: bir ligdeki ilk sezonun baslangic yilini aliyoruz. orn: 1928
XXX: bu yuzden bundan sonraki fonksiyona try catch bloklari ekleyerek
XXX: hata aldigimizda ilgili ligin o sezon yilinda aktif olmadigini anlayacagiz
          
XXX: for each link in links list get all team data
     get all team data from league years using 'links' list            

TODO: XXX: FIRAT: yukaridaki if else blocklari try except ile degistirilmeli.
 sample of try catch blocks

        
XXX: for each link in links list get all team data
     get all team data from league years using 'links' list.
          
XXX: TEAMS.PY EKLENECEK

TODO: Class mantigi ve veritabani baglantisi icin kod revize edilecek.

XXX: end of the project: SERVICE SCRIPT
python uygulamasinin sunucuda surekli calismasi icin 
ve surekli calisan uygulamanin monitor edilebilmesi icin
cron job kullanilabilir. fakat uygulanabilirlik ve monitoring acisindan
degerlendirdiginde systemctl'de calisacak olan service scripti daha mantikli.
systemctl example link: https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
    
XXX: end of the project: ip reputation control & ip changer
how to check the string is string or integer
https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
