
#WEB SCRAPE TWEETS (https://medium.com/citrispolicylab/a-simple-guide-to-scrape-tweets-using-python-ba7c691b6efa)
#CLEAN THE DATA
#CLASSIFY TWEETS USING SENTIMENT ANALYSIS
#DETERMINE BUZZ USING RATIOS


#API Key: uArLcf4kc5yhqSdYT6gHwV68y
#API Secret Key: xYrmAeZGbLI2R4OtXINlukuvSUOl6HKG57GwMVbM4N5Sv9zXG4
#Bearer token: AAAAAAAAAAAAAAAAAAAAAI4wKgEAAAAAe4PHUBlYVtF7VGy4ZvIKIr0k6eM%3DVFEK31Hix5qMoMf35b7nsuufHy7fiwLldH2ooGDqNBan4tqzzD

import tweepy
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()



text = "I HATE aditya"


print(vader.polarity_scores(text)["compound"])


CONSUMER_KEY = 'uArLcf4kc5yhqSdYT6gHwV68y'
CONSUMER_SECRET = 'xYrmAeZGbLI2R4OtXINlukuvSUOl6HKG57GwMVbM4N5Sv9zXG4'
ACCESS_TOKEN = '1337205614070669315-cQUWRvqcAU95DMCu7UmrAQZONsRgP3'
ACCESS_TOKEN_SECRET = 'SpIiUd2URckCFy850jbNBSFH9h7pOfOEdSdVUtNH5Qygf'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

username = '_pshah'
count = 20
try:
 # Creation of query method using parameters
 tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
except BaseException as e:
      print('failed on_status,',str(e))
      time.sleep(3)

tweets_list = [[tweet.text] for tweet in tweets]
#print(tweets_list)

print(type(tweets_list[0]))
print(vader.polarity_scores(tweets_list[0])["compound"])
sentiment_list = []

#for tweet in tweets_list:
#    print(vader.polarity_scores(tweet)["compound"])
    #sentiment_list.append(vader.polarity_scores(tweet)["compound"])

print(sentiment_list)
