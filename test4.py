from bs4 import BeautifulSoup
import requests
import re

URL = "https://www.zeebiz.com/markets/currency/news-cryptocurrency-news-today-june-12-bitcoin-dogecoin-shiba-inu-and-other-top-coins-prices-and-all-latest-updates-158490"

html_content = requests.get(URL).text

soup = BeautifulSoup(html_content, "lxml")

body=soup.body.text

print(body)