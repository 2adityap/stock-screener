import requests
from bs4 import BeautifulSoup

URL = "https://finance.yahoo.com/quote/FB/analysis/"
page = requests.get(URL)
print(page)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id = 'Main')



yahoo_scrape_data = []

estimates = results.find_all('span', class_= "Trsdu(0.3s)")
for text in estimates:
    yahoo_scrape_data.append(text.text.strip())

percent_growth = results.find_all('td', class_="Ta(end) Py(10px)")
for text in percent_growth:
    yahoo_scrape_data.append(text.text.strip())

print(yahoo_scrape_data)
