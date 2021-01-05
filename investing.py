import requests
import os
import yfinance as yf
import pandas as pd
import numpy as np
from scraping import scrape, clean, earnings_surprise_helper, eps_revisions_helper
from prediction import create_df, feature_scaling, train_close_prices, predict_next_day
from twitter_sentiment import pull_tweets, remove_duplicates, create_graph
import nltk
import datetime
import tweepy

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
key = os.environ.get("ALPHA_API_KEY")

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

def get_description(symbol):
    ticker = yf.Ticker(symbol)
    description = ""
    for key, value in ticker.info.items():
        if key == "longBusinessSummary":
            description = value
    return description

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

    higher = (np.array(volume_df["Higher"])).tolist()

    size = int(volume_df.size / 4)
    count_down = 0
    count_up = 0
    for i in range(size):
        if higher[i]:
            if percent_change[i] > 0.0:
                count_up = count_up + 1
            else:
                count_down = count_down + 1

    return volume_df, count_up, count_down

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

def twitter(symbol):
    #authorize tweepy
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    query = "${0}".format(symbol)
    count = 500
    tweets = pull_tweets(query,count)
    mean, size = create_graph(tweets)
    return mean, size

def present_information(symbol):
    output = ""

    descr = get_description(symbol)

    output = descr

    year_high, year_low, fifty_moving_avg, two_hundy_moving_avg = get_high_and_averages(key, symbol)
    price = get_recent_close_price(symbol)
    priceperf_bool = price_performance(fifty_moving_avg, two_hundy_moving_avg, price)

    if priceperf_bool:
        output = output + " Currently, the stock is at {0}, which is overperforming its 50 day and 200 day moving averages, thus showing strong strength in the last 40 weeks. ".format(price)
    else:
        output = output + " Currently, the stock is at {0}, which is underperforming its 50 day and 200 day moving averages, thus not showing signs of growth in last 40 weeks. ".format(price)

    surprise_bool, average_surprise = get_revisions_earnings_surprise(symbol)

    if surprise_bool:
        output = output + "Over the last 4 quarters, the earnings have surpassed analyst expectations by an average of {0}%, pointing to growth in the company and upcoming price growth as well. ".format(average_surprise)
    else:
        output = output + "Over the last 4 quarters, the earnings have not surpassed analyst expectations, by an average of {0}%, which is not a dealbreaker, but represents that it has failed to meet earnings expectations in the past. ".format(average_surprise)

    volume_df, count_up, count_down = get_volume_changes(symbol)
    if count_up > count_down:
        output = output + "Over the last 4 weeks there have been {0} volume shifts that have been higher than the moving average. Of those shifts, {1} resulted in a positive price change and {2} resulted in a negative price change. This means that most likely a lot of stock has been bought recently, resulting in strong volume and price increase. This boosts the stock's strength. ".format(count_up + count_down, count_up, count_down)
    else:
        output = output + "Over the last 4 weeks there have been {0} volume shifts that have been higher than the moving average. Of those shifts, {1} resulted in a positive price change and {2} resulted in a negative price change. This means that most likely a lot of stock has been sold recently, resulting in strong volume increase but a price decrease. This is a cause of worry and needs to be investigated more. ".format(count_up + count_down, count_up, count_down)

    #Add analyst revisions here
    days = earnings_calendar(symbol)
    output = output + "There are {0} days until the next earnings are given. ".format(days)

    sentiment, size = twitter(symbol)
    if sentiment > 0.0:
        output = output + "Using Twitter, we have pulled the last {0} tweets relating to {1}, and have found the overall sentiment to be positive, thus indicating the general audience of shareholders believe in the stock, another good sign. ".format(size,symbol)
    else:
        output = output + "Using Twitter, we have pulled the last {0} tweets relating to {1}, and have found the overall sentiment to be negative, thus indicating the general audience of shareholders do not believe in the stock, which should be further looked into by you. ".format(size,symbol)

    #Add stock prediction when algorithm is fixed

    print(output)

def main():
    symbol = input("What symbol do you want? ")
    present_information(symbol)

    #df = create_df(symbol, "2017-01-01", "2020-12-30")
    #train_close_prices(df)

if __name__ == "__main__":
    main()
