import tweepy
import nltk
import numpy as np
import pandas as pd
import os
import re
from datetime import datetime

#create webhook to pull every hour, see how snetiment change matches up with stock price changes

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
    try:
        tweets = tweepy.Cursor(api.search,q=query).items(count)
        for tweet in tweets:
            tweet.text = re.sub("(@[A-Za-z0-9]+|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|[0-9])", '', tweet.text) #removes handles, urls, numbers, dates
            tweet_texts.append([tweet.text, tweet.created_at, vader.polarity_scores(tweet.text)["compound"]])
    except:
        pass
    tweets = remove_duplicates(tweet_texts)
    return tweets

def remove_duplicates(tweets_list):
    tweets = []
    tweet_texts = []
    for tweet in tweets_list:
        if tweet[0] not in tweet_texts:
            tweets.append(tweet)
            tweet_texts.append(tweet[0])
    return tweets

def most_negative_tweet(tweets_list):
    min_sentiment = min(sentiment_list)
    index = sentiment_list.index(min_sentiment)
    return tweets_list[index]

def most_positive_tweet(tweets_list):
    max_sentiment = max(sentiment_list)
    index = sentiment_list.index(max_sentiment)
    return tweets_list[index]

def create_graph(sentiment_list):
    sentiment_df = pd.DataFrame(sentiment_list, columns = ["Text","Date", "Sentiment"])
    sentiment_df.sort_values(by='Sentiment', ascending=True)
    mean_sentiment = sentiment_df["Sentiment"].mean()

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    print(sentiment_df)
    print("MEAN SENTIMENT: {0}".format(mean_sentiment))

def main():
    query = input("What symbol do you want: ")
    query = "${0}".format(query)
    count = 500
    tweets = pull_tweets(query,count)
    create_graph(tweets)

if __name__ == "__main__":
    main()
