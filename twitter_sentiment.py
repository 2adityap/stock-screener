import tweepy
import nltk
import numpy as np
import pandas as pd
import os
import re


#check if there is a relationship between sentiment and stock price, then develop formula using gradient descent?

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()


#Get keys from Twitter API
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")


#authorize tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

def pull_tweets(query, count):
    tweet_texts = []
    sentiment_list = []
    neutral_count = 0
    try:
        tweets = tweepy.Cursor(api.search,q=query, since='2020-12-12').items(count)
        for tweet in tweets:
            tweet.text = re.sub("(@[A-Za-z0-9]+|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|[0-9])", '', tweet.text) #removes handles, urls, numbers, dates
            tweet_texts.append([(tweet.text, vader.polarity_scores(tweet.text)["compound"])])
    except:
        pass
    average_sentiment = 0
    res = [lis[1] for lis in tweet_texts]
    average_sentiment = average_sentiment / len(tweet_texts)
    return tweet_texts, neutral_count, res

def most_negative_tweet(tweets_list):
    min_sentiment = min(sentiment_list)
    index = sentiment_list.index(min_sentiment)
    return tweets_list[index]

def most_positive_tweet(tweets_list):
    max_sentiment = max(sentiment_list)
    index = sentiment_list.index(max_sentiment)
    return tweets_list[index]

def create_graph(sentiment_list):
    return None

def main():
    query = '$SQ'
    count = 1000
    tweets, neutral_count, sentiment_average = pull_tweets(query,count)
    print(sentiment_average, neutral_count)

if __name__ == "__main__":
    main()
