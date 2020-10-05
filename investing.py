import requests

key = "1AJHCKC421EAJDT9"
url = "https://www.alphavantage.co/query?"
symbol = input("What symbol do you want? ")

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

#print(description)

print("52 Week High: {0}".format(year_high))
print("52 Week Low: {0}".format(year_low))
print("50 Day Moving Average: {0}".format(fifty_moving_avg))
print("200 Day Moving Average: {0}".format(two_hundy_moving_avg))


#Using finnhub.io, for NLP
# List webhook
r2 = requests.get('https://finnhub.io/api/v1/news-sentiment?symbol=TSLA&token=bttm65v48v6ojt2heeq0')
res2 = r2.json()
print(res2)



#response1 = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=" + key)
#res1 = response1.json()

#for key, value in res1.items():
#    for ke, v in value.items():
#       print(v)

#response2 = requests.get("https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=daily&time_period=10&series_type=open&apikey=" + key)
#res2 = response2.json()

#for key, value in res2.items():
#    for k, v in value.items():
#        print(k)
#print(res2)
