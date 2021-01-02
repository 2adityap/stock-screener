import requests
import os
import yfinance as yf
import pandas as pd
import numpy as np
from scraping import scrape, clean, earnings_surprise_helper, eps_revisions_helper
from prediction import create_df, feature_scaling, train_close_prices, predict_next_day
import datetime

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

#Return closing price as of last minute
def get_recent_close_price(symbol):
    data = (np.array((yf.download(symbol, period="1d", interval="1m")).filter(["Close"]))).tolist()
    recent = data[len(data)-1]
    price = 0.0
    for item in recent:
        price = float(item)

    return round(price,4)

#analyze if volume increases with price
def get_volume_changes(symbol):
    data = yf.download(symbol, period="1mo", interval="1d")
    volume = data.filter(["Volume"])
    mean = int(volume.mean())

    volume.to_csv('stockdata.csv',index = "Date")
    volume_df = pd.read_csv('stockdata.csv')
    length = int(volume_df.size / 2)
    Higher = []
    for i in range(length):
        Higher.append(False)
    volume_df["Higher"] = Higher

    close = data.filter(["Close"])
    close = np.array(close)

    percent_change = []
    for i in range(length):
        percent_change.append(((close[i]-close[i-1])/close[i-1]) * 100)

    volume_df["Percent Change"] = percent_change

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    volume_df["Higher"] = np.where(volume_df["Volume"].values>mean,True,volume_df["Higher"])
    print(volume_df)
    return volume_df

#Earnings Calendar, Returns date
def earnings_calendar(symbol):
    ticker = yf.Ticker(symbol)
    earnings_date = ticker.calendar[0].iloc[0].to_pydatetime()
    today = datetime.datetime.today()
    days_until = earnings_date - today
    return days_until.days

#Returns earnings suprises, average surprise
#TODO: Figure out how to properly scrape revisions
def get_revisions_earnings_surprise(symbol):
    data = scrape(symbol)
    surprise, revisions = clean(data)

    #Calculate if earnings surprise last 4 quarters, average surprise
    annual_earnings_growth = True
    average_surprise = 0.0
    for i in range(len(surprise)):
        percentage = float((surprise[i][0])[:-1].replace(",",""))
        if percentage < 0:
            annual_earnings_growth = False
        average_surprise = average_surprise + percentage
    average_surprise = round(average_surprise/4,2)

    return annual_earnings_growth, average_surprise

#Checks if current price above moving averages
def price_performance(fiftyDay, twoHundyDay, price):
    fiftyDay = float(fiftyDay)
    twoHundyDay = float(twoHundyDay)
    overperformance = False
    if price > fiftyDay and price > twoHundyDay:
        overperformance = True
    return overperformance

def main():
    key = os.environ.get("ALPHA_API_KEY")
    symbol = input("What symbol do you want? ")
    #year_high, year_low, fifty_moving_avg, two_hundy_moving_avg = get_high_and_averages(key, symbol)
    #earnings = get_earnings(key, symbol)
    #print(year_high, year_low, fifty_moving_avg, two_hundy_moving_avg)
    #earnings_calendar(symbol)
    #surprise_bool, average_surprise = get_revisions_earnings_surprise(symbol)
    #get_volume_changes(symbol)
    #price = get_recent_close_price(symbol)
    #print(price, fifty_moving_avg, two_hundy_moving_avg)
    #print(price_performance(fifty_moving_avg, two_hundy_moving_avg, price))


    df = create_df(symbol, "2017-01-01", "2020-12-30")
    train_close_prices(df)

if __name__ == "__main__":
    main()
