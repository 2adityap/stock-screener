import requests


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

#maybe get yahoo finance for this
def current_price(key, symbol):
    response = requests.get(url + "function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + key)
    res = response.json()

    for key, value in res.items():
        if key == "Time Series (Daily)":
            for day in value.items():
                for price in day:
                    print(price)

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

def analyze_earnings(earnings):
    quarter_profit = []
    quarter_revenue = []
    for quarter in earnings:
        quarter_revenue.append(quarter[1])
        quarter_profit.append(quarter[2])
    print(quarter_profit)
    bool_revenue = analyze_earnings_helper(quarter_revenue)
    bool_profit = analyze_earnings_helper(quarter_profit)
    if(bool_profit and bool_revenue):
        return "Both earnings and revenue have increased over the last 4 quarters"
    if(not(bool_revenue) and bool_profit):
       return "Profits have gone up over the last 4 quarters, but the revenue hasn't"
    if(not(bool_profit) and bool_revenue):
        return "Revenue has gone up over the last 4 quarters, but profit hasn't"
    else:
        return "Neither earnings or revenue have increased over the last 4 quarters"

def analyze_earnings_helper(quarter):
    if(quarter[0] > quarter[1] > quarter[2] > quarter[3]):
        return True
    else:
        return False


def main():
    key = "1AJHCKC421EAJDT9"
    symbol = input("What symbol do you want? ")
    year_high, year_low, fifty_moving_avg, two_hundy_moving_avg = get_high_and_averages(key, symbol)
    print("52 Week High: {0}".format(year_high))
    print("52 Week Low: {0}".format(year_low))
    print("50 Day Moving Average: {0}".format(fifty_moving_avg))
    print("200 Day Moving Average: {0}".format(two_hundy_moving_avg))
    earnings = get_earnings(key, symbol)
    #print(earnings)
    print(analyze_earnings(earnings))
    #current_price(key,symbol)

if __name__ == "__main__":
    main()
