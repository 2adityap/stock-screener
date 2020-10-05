import requests

key = "1AJHCKC421EAJDT9"
response = requests.get("https://www.alphavantage.co/query?function=OVERVIEW&symbol=SQ&apikey=" + key)
res = response.json()

for key, value in res.items():
    if key == "Description":
        print(value)

response1 = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=" + key)
res1 = response1.json()

for key, value in res1.items():
    for ke, v in value.items():
       print(v)

response2 = requests.get("https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=daily&time_period=10&series_type=open&apikey=" + key)
res2 = response2.json()
print(res2)
