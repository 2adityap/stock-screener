import requests
import os
import yfinance as yf
import pandas
from scraping import scrape, clean, earnings_surprise_helper, eps_revisions_helper

url = "https://www.alphavantage.co/query?"

#Returns the high, low, 50 Day SMA and 200 Day SMA of a stock

def get_high_and_averages(key, symbol):
    response = requests.get(url + "function=OVERVIEW&symbol=" + symbol + "&apikey=" + key)
    res = response.json()

    description = ""
    year_high = 0
    year_low = 0
    fifty_moving_avg = 0
    two_hundy_moving_avg = 0

    for key, value in res.items():
        if key == "Description":
            description = value
        if key == "52WeekHigh":
            year_high = value
        if key == "52WeekLow":
            year_low = value
        if key == "50DayMovingAverage":
            fifty_moving_avg = value
        if key == "200DayMovingAverage":
            two_hundy_moving_avg = value

    return year_high, year_low, fifty_moving_avg, two_hundy_moving_avg

#Creates a list of lists of last 5 years of quarterly earnings. Each list has quarter data, revenue and profit, in that order

def get_earnings(key, symbol):
    response = requests.get(url + "function=INCOME_STATEMENT&symbol=" + symbol + "&apikey=" + key)
    res = response.json()

    earnings = []
    count = 0
    for key, value in res.items():
        if key == "quarterlyReports":
            for quarter in value:
                quarter_report = []
                for stats in quarter:
                    if stats == "fiscalDateEnding" or stats == "totalRevenue" or stats == "grossProfit":
                        quarter_report.append(quarter[stats])
                earnings.append(quarter_report)
    return earnings

#Return true if profit and earning went up

def analyze_earnings(earnings):
    quarter_profit = []
    quarter_revenue = []
    for quarter in earnings:
        quarter_revenue.append(quarter[1])
        quarter_profit.append(quarter[2])
    print(quarter_profit)
    bool_revenue = analyze_earnings_helper(quarter_revenue)
    bool_profit = analyze_earnings_helper(quarter_profit)
    return bool_revenue and bool_profit

def analyze_earnings_helper(quarter):
    if(quarter[0] > quarter[1] > quarter[2] > quarter[3]):
        return True
    else:
        return False

##### REVISIT BOOK TO LOOK AT ALL THE STRATEGIES

def get_stock_price(symbol):
    data = yf.download(symbol, period="1d", interval="15m")
    print(data)

#analyze if volume increases with price
def get_volume_changes(symbol):
    data = yf.download(symbol, period="1mo", interval="1d")
    print(data["Volume"], data["Close"])

#Earnings Calendar, analyze tweets a couple weeks before earnings
def earnings_calendar(symbol):
    ticker = yf.Ticker(symbol)
    print(ticker.calendar.iloc[0])
    return None

def get_revisions_earnings_surprise(symbol):
    data = scrape(symbol)
    revisions, surprise = clean(data)
    return revisions, surprise

def main():
    key = os.environ.get("ALPHA_API_KEY")
    symbol = input("What symbol do you want? ")
    year_high, year_low, fifty_moving_avg, two_hundy_moving_avg = get_high_and_averages(key, symbol)
    earnings = get_earnings(key, symbol)
    earnings_calendar(symbol)
    revisions, surprise = get_revisions_earnings_surprise(symbol)
    print(revisions, surprise)

if __name__ == "__main__":
    main()
