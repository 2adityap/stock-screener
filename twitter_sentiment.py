import tweepy
import nltk
import os


nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()



CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
print(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

username = '_pshah'
count = 20

tweet_texts = []

try:
 # Creation of query method using parameters
 tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
 for tweet in tweets:
    tweet_texts.append(tweet.text)
except:
    pass

sentiment_list = []
for tweet in tweet_texts:
    sentiment_list.append(vader.polarity_scores(tweet)["compound"])

max_sentiment = max(sentiment_list)
max_index = sentiment_list.index(max_sentiment)

print(max_index)

print(tweet_texts[max_index])
