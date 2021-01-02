import requests
from bs4 import BeautifulSoup

#TODO: figure out how to index certain values, figure out how to store DataFrame

def scrape(symbol):

    URL = "https://finance.yahoo.com/quote/" + symbol + "/analysis/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id = 'Main')

    scrape_data = []

    estimates = results.find_all('span', class_= "Trsdu(0.3s)")
    for text in estimates:
        scrape_data.append(text.text.strip())

    percent_growth = results.find_all('td', class_="Ta(end) Py(10px)")
    for text in percent_growth:
        scrape_data.append(text.text.strip())

    analyst_rating = results.find_all('span', class_="Bdbw(2px) Bdbs(s) Bdbc($seperatorColor) H(1em) Pos(r) Mt(30px) Mx(10%)")
    print(analyst_rating)
    return scrape_data

def clean(data):
    #remove earnings estimates, revenue estimates, earnings history ( except for surprise %), remove eps trend, keep current quarter eps revisions, remove growth estimates
    #earnings surprise
    earnings_surprise = earnings_surprise_helper(data)
    eps_revisions = eps_revisions_helper(data)
    return earnings_surprise, eps_revisions

# Returns Earnings Surprises from Last 4 Quarters

def earnings_surprise_helper(data):
    earnings_surprise = []
    earnings_surprise_numbers = data[56:60]
    earnings_surprise_label = ["4 Quarters Ago", "3 Quarters Ago", "2 Quarters Ago", "1 Quarter ago"]
    for i in range(len(earnings_surprise_numbers)):
        earnings_surprise.append((earnings_surprise_numbers[i],earnings_surprise_label[i]))
    return earnings_surprise

# TODO: Returns EPS Revisions for Current Quarter

def eps_revisions_helper(data):
    eps_revisions = []
    eps_revisions_labels = ["Up Last 7 Days", "Up Last 30 Days", "Down Last 7 Days", "Down Last 30 Days"]
    eps_revisions_numbers = []
    eps_revisions_numbers.append(data[80])
    eps_revisions_numbers.append(data[84])
    eps_revisions_numbers.append(data[88])
    eps_revisions_numbers.append(data[92])
    print(eps_revisions_numbers)
    for i in range(len(eps_revisions_numbers)):
        eps_revisions.append((eps_revisions_numbers[i], eps_revisions_labels[i]))
    return eps_revisions

def main():
    symbol = input("What symbol do you want? ")
    data = scrape(symbol)
    eps, surprise = clean(data)
    print(eps, surprise)

if __name__ == "__main__":
    main()
