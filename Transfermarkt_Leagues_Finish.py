# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 23:36:36 2024

@author: W10
"""


import requests
from bs4 import BeautifulSoup
import re
from parsel import Selector
from requests import Session
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

# Oturum oluşturma ve gerekli başlıkları ekleme
oturum = Session()
oturum.headers.update({
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
})

base_url = 'https://www.transfermarkt.co.uk'
tiers = ['First Tier', 'Second Tier', 'Third Tier', 'Fourth Tier', 'Fifth Tier', 'Sixth Tier', 'Youth league']

veri = {}
for say in tqdm(range(1, 27), desc="Lig verilerini çekme"):
    istek = oturum.get(f"https://www.transfermarkt.co.uk/wettbewerbe/europa/wettbewerbe?ajax=yw1&page={say}&plus=1")
    secici = Selector(istek.text)

    for satir in secici.xpath("//table[@class='items']/tbody/tr"):
        lig = satir.xpath(".//td[2]/a/text()").get()
        if not lig:
            yarisma = satir.xpath(".//td[contains(@class, 'hauptlink')]/text()").get()
            if yarisma and yarisma not in veri:
                veri[yarisma] = []
            continue

        league_link = satir.xpath(".//td[2]/a/@href").get()

        if yarisma:
            veri[yarisma].append({
                "league": lig,
                "league_link": league_link,
                "league_ID": league_link.split('/')[-1],
                "country": satir.xpath(".//td[2]/img/@title").get(),
                "club": int(satir.xpath("normalize-space(.//td[3])").get() or 0),
                "player_number": int(satir.xpath("normalize-space(.//td[4])").get().replace(".", "") or 0),
                "average_age": float(satir.xpath("normalize-space(.//td[5])").get() or 0.0),
                "foreigner_player_avg": float(satir.xpath("normalize-space(.//td[6])").get().split()[0].replace("%", "") or 0.0),
                "game_ratio_of_foreign_players": satir.xpath("normalize-space(.//td[7])").get().split()[0].replace("%", "") or "0",
                "goals_per_match": satir.xpath("normalize-space(.//td[8])").get() or "0",
                "average_market_value": satir.xpath("normalize-space(.//td[10])").get() or "0",
                "total_market_value": satir.xpath("normalize-space(.//td[11])").get() or "0",
            })

league_links = []
for tier in tiers:
    if tier in veri:
        league_links.extend([urljoin(base_url, league['league_link']) for league in veri[tier]])

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504, 404, 443), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

data = {}

def parse_team_data(soup, league_code, competition_url):
    team_table = soup.select_one("table.items")
    if team_table:
        try:
            teams = team_table.select("tbody > tr")
            for team in teams:
                team_name = team.select_one("td.hauptlink a").text.strip() if team.select_one("td.hauptlink a") else None
                team_link = team.select_one("td.hauptlink a")
                team_href = base_url + team_link['href'] if team_link else None
                team_id_match = re.search(r'/verein/(\d+)', team_href)
                team_id = team_id_match.group(1) if team_id_match else None

                # Sezon yılını linkten çıkar
                season_year_match = re.search(r'saison_id=(\d+)', competition_url)
                season_year = season_year_match.group(1) if season_year_match else None

                squad_size = team.select("td")[2].text.strip() if len(team.select("td")) > 2 else None
                average_age = team.select("td")[3].text.strip() if len(team.select("td")) > 3 else None
                foreigners = team.select("td")[4].text.strip() if len(team.select("td")) > 4 else None
                average_market_value = team.select("td")[5].text.strip() if len(team.select("td")) > 5 else None
                total_market_value = team.select("td")[6].text.strip() if len(team.select("td")) > 6 else None

                if team_href and season_year:
                    team_href = f"{team_href}/saison_id/{season_year}"

                team_data = {
                    'League Code': league_code,
                    'Season Year': season_year,
                    'Team Name': team_name,
                    'Team ID': team_id,
                    'Team Link': team_href,
                    'Squad Size': squad_size,
                    'Average Age': average_age,
                    'Foreigners': foreigners,
                    'Average Market Value': average_market_value,
                    'Total Market Value': total_market_value,
                }
                if 'Teams' not in data:
                    data['Teams'] = []
                data['Teams'].append(team_data)
        except (AttributeError, IndexError, TypeError, re.error) as e:
            pass  # Hataları sessizce yutmak yerine loglayabilirsiniz

def parse_league_data(soup, competition_url, season_id):
    banner_info = soup.select_one("header.data-header")
    if banner_info:
        try:
            league_level_value = banner_info.find("span", class_="data-header__content").text.strip() if banner_info.find("span", class_="data-header__content") else ""

            country = banner_info.select_one('span.data-header__club')
            if country:
                country_text = country.text.strip()
                if country_text != "Tournament records":
                    league_country_name = country_text
                else:
                    league_name = banner_info.find("h1", class_="data-header__headline-wrapper data-header__headline-wrapper--oswald").text.strip()
                    if "cup" in league_name.lower():
                        league_country_name = league_name.split()[0]
                    else:
                        league_country_name = None
            else:
                league_country_name = None

            country_element = banner_info.select_one("span.data-header__club > a")
            league_country_href = base_url + country_element['href'] if country_element else ""
            league_country_code_match = re.search(r'/wettbewerbe/national/wettbewerbe/(\d+)', league_country_href) if league_country_href else None
            league_country_code_value = league_country_code_match.group(1) if league_country_code_match else ""

            league_name_value = banner_info.find("h1", class_="data-header__headline-wrapper data-header__headline-wrapper--oswald").text.strip()
            league_uefa_coefficient_value = banner_info.findAll("span", class_="data-header__content")[5].a.get_text(strip=True) if len(banner_info.findAll("span", "data-header__content")) > 5 and banner_info.findAll("span", "data-header__content")[5].a else None
            league_uefa_coefficient_points_value = banner_info.findAll("span", class_="data-header__content")[6].get_text(strip=True) if len(banner_info.findAll("span", "data-header__content")) > 6 else None

            league_code_match = re.search(r'wettbewerb/(\w+)', competition_url)
            league_code_value = league_code_match.group(1) if league_code_match else None

            league_details = banner_info.select_one("div.data-header__details")
            if league_details:
                league_details_content = league_details.findAll("span", class_="data-header__content")
                number_of_clubs_value = league_details_content[0].get_text(strip=True) if len(league_details_content) > 0 else None
                number_of_players_value = league_details_content[1].get_text(strip=True) if len(league_details_content) > 1 else None
                number_of_foreigners_value = league_details_content[2].get_text(strip=True).split("\xa0")[0] if len(league_details_content) > 2 else None
                market_value_value = league_details_content[3].get_text(strip=True) if len(league_details_content) > 3 else None
                average_age_value = league_details_content[4].get_text(strip=True) if len(league_details_content) > 4 else None

                percentage_of_foreigners_value = league_details.findAll("span", "tabellenplatz")[0].get_text(strip=True) if league_details.findAll("span", "tabellenplatz") else None
            else:
                number_of_clubs_value = number_of_players_value = number_of_foreigners_value = market_value_value = average_age_value = percentage_of_foreigners_value = None

            total_market_value_tag = banner_info.select_one("div.data-header__box--small a.data-header__market-value-wrapper")
            total_market_value = total_market_value_tag.get_text(strip=True).replace("Total Market Value", "").strip() if total_market_value_tag else None

            season_year_match = re.search(r'saison_id=(\d+)', competition_url)
            season_year = season_year_match.group(1) if season_year_match else None

            if league_level_value not in data:
                data[league_level_value] = {}

            if league_code_value not in data[league_level_value]:
                data[league_level_value][league_code_value] = []

            data[league_level_value][league_code_value].append({
                'League Name': league_name_value or None,
                'Country': league_country_name,
                'Level': league_level_value or None,
                'UEFA Coefficient': league_uefa_coefficient_value or None,
                'UEFA Coefficient Points': league_uefa_coefficient_points_value or None,
                'Number of Clubs': number_of_clubs_value or None,
                'Number of Players': number_of_players_value or None,
                'Number of Foreigners': number_of_foreigners_value or None,
                'Percentage of Foreigners': percentage_of_foreigners_value or None,
                'Market Value': market_value_value or None,
                'Average Age Value': average_age_value or None,
                'Total Market Value': total_market_value or None,
                'Competition Link': competition_url or None,
                'Year': season_year or None
            })
        except (AttributeError, IndexError, TypeError, re.error) as e:
            pass  # Hataları sessizce yutmak yerine loglayabilirsiniz

def scrape_league_data(league_link, session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
    }
    try:
        response = session.get(league_link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        season_id_match = re.search(r'saison_id=(\d+)', response.url)
        season_id = season_id_match.group(1) if season_id_match else None

        parse_league_data(soup, league_link, season_id)
        league_code_match = re.search(r'wettbewerb/(\w+)', league_link)
        league_code = league_code_match.group(1) if league_code_match else None
        parse_team_data(soup, league_code, league_link)
    except requests.exceptions.RequestException as e:
        pass  # Hataları sessizce yutmak yerine loglayabilirsiniz

def get_season_links(league_url, session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
    }
    try:
        response = session.get(league_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        season_select = soup.find('select', {'data-placeholder': 'Filter by season'})

        if season_select:
            season_links = []
            for option in season_select.find_all('option'):
                season_id = option.get('value')
                if season_id:
                    season_link = f"{league_url}/plus/?saison_id={season_id}"
                    season_links.append(season_link)
            return season_links
        else:
            return []

    except requests.exceptions.RequestException as e:
        return []

# Ana kod
start_time = time.time()

all_season_links = []

with requests_retry_session() as session:
    for link in tqdm(league_links, desc="Sezon bağlantılarını çekme"):
        season_links = get_season_links(link, session)
        all_season_links.extend(season_links)

# ThreadPoolExecutor ile paralel işleme
with ThreadPoolExecutor(max_workers=20) as executor:
    list(tqdm(executor.map(lambda link: scrape_league_data(link, oturum), all_season_links), total=len(all_season_links), desc="Lig ve takım verilerini çekme"))

# Takım verilerini DataFrame'e dönüştürme
if 'Teams' in data:
    teams_df = pd.DataFrame(data['Teams'])
    print(teams_df)
else:
    print("No team data found.")

end_time = time.time()
duration_minutes = (end_time - start_time) / 60
print(f"Toplam çalışma süresi: {duration_minutes:.2f} dakika")