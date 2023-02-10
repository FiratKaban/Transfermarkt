

import csv
from collections import namedtuple
 
import requests
from bs4 import BeautifulSoup
from requests import Session
 
 
class HepsiBurada:
    def __init__(self, product) -> None:
        self.url = "https://www.hepsiburada.com"
        self.product = product
        self.request = self.get_session()
 
        self.current_page = 1
        self.last_page = self.get_last_page()
 
    def get_session(self) -> Session:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            }
        )
        return session
 
    def get_last_page(self):
        response = self.request.get(f"{self.url}/{self.product}")
        soup = BeautifulSoup(response.content, "html.parser")
        pages = soup.find(name="div", attrs={"id": "pagination"})
        return int(pages.find_all("li")[-1].a.text)
 
    def get_product_links(self, page=1):
        response = self.request.get(f"{self.url}/{self.product}/?sayfa={page}")
        soup = BeautifulSoup(response.content, "html.parser")
        product_block = soup.find(name="ul", attrs={"class": "product-list"})
        products = product_block.find_all(name="li")
        return [product.a.get("href") for product in products]
 
    def get_rating_count(self, url):
        response = self.request.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        rating = soup.find("div", attrs={"id":"comments-container"})
        if rating is None:
            return 0
        rating = rating.text.strip()
        if rating == "":
            return 0
        return int(rating.split(" ")[0])

    def get_comments_of_page(self, url, page):
        response = self.request.get(f"{url}?sayfa={page}")
        soup = BeautifulSoup(response.content, "html.parser")
        comments = soup.find_all(
            name="div", attrs={"class": "hermes-ReviewCard-module-3Y36S"}
        )
        Comment = namedtuple(
            "Comment",
            (
                "star",
                "date",
                "comment",
                "seller",
                "size",
                "color",
                "name",
                "age",
                "city",
            ),
        )
        comment_list = []
        for comment in comments:
            star_block = comment.find(
                name="div", attrs={"class": "hermes-RatingPointer-module-1OKF3"}
            )
            stars = len(star_block.find_all("div"))
 
            name, age, city = (
                span.text
                for span in comment.find(
                    name="div", attrs={"class": "hermes-ReviewCard-module-1-Wp3"}
                ).find_all("span")
            )
            name = name.strip()
            age = int(age[1:-2]) if age else None
            city = city.split("-")[-1].strip()
 
            date = comment.find(
                name="span", attrs={"class": "hermes-ReviewCard-module-3fj8Y"}
            ).get("content")
 
            text = comment.find(
                name="div", attrs={"class": "hermes-ReviewCard-module-2dVP9"}
            )
            if hasattr(text, "span"):
                text = text.span.text
            else:
                text = "Yorum Yapilmamistir"
 
            seller = comment.find(
                name="span", attrs={"class": "hermes-ReviewCard-module-2wCCu"}
            ).text
            size_block, color_block = comment.find_all(
                name="div", attrs={"class": "hermes-ReviewCard-module-1XNlv"}
            )
            size = size_block.find_all("span")[2].text
            color = color_block.find_all("span")[2].text
 
            comment_list.append(
                Comment(stars, date, text, seller, size, color, name, age, city)
            )
 
        return comment_list
 
    def get_comments(self, url):
        comment_link = f"{self.url}{url}-yorumlari"
        rating_count = self.get_rating_count(comment_link)
        page_count = int((rating_count/25)+1)
        page_count = 2 if page_count == 1 else page_count+1
        all_comments = []
        for page in range(1, page_count):
            all_comments += self.get_comments_of_page(comment_link, page)
        return all_comments
        
 
    def export_to_excel(self, comments):
        with open("C:\\Users\\Hp\\Desktop\\comments.csv", "w", encoding="utf-8") as myfile:
            wr = csv.writer(myfile)
            for comment in comments:
                wr.writerow([*comment])
 
 
if __name__ == "__main__":
    scraper = HepsiBurada("lufian")
    all_comments = []
    while scraper.current_page < scraper.last_page + 1:
        links = scraper.get_product_links(page=scraper.current_page)
        scraper.current_page += 1
        for link in links[:1]:
            comments = scraper.get_comments(link)
            all_comments.extend(comments)
        break
    link = "/lufian-ester-spor-erkek-blazer-ceket-slim-fit-siyah-p-HBCV00001HQCU0"  # No comment
    link = "/lufian-erkek-laon-spor-polo-t-shirt-p-HBV00000QARA1"  # 724 comment
 
    scraper.export_to_excel(all_comments)