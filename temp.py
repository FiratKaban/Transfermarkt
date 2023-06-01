import requests
from bs4 import BeautifulSoup

headerz = {
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/45.0.2454.101 Safari/537.36"
    )
}

data = []

# Send a GET request to the page with the leagues table
url = "https://www.transfermarkt.co.uk/wettbewerbe/europa?page=1"
response = requests.get(url, headers=headerz)
soup = BeautifulSoup(response.content, "html.parser")
leagues_table = soup.select("tr.odd, tr.even")

for leagues_link in leagues_table:

    league_link = leagues_link.select("a")[1]["href"]
    league_name = leagues_link.select("a")[1]["title"]
    league_country = leagues_link.select("img")[1]["title"]

    
    print("url",league_link)
    print("name",league_name)
    print("country",league_country)
