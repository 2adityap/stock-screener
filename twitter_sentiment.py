import tweepy
import nltk
import os


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
    try:
        tweets = tweepy.Cursor(api.search,q=query).items(count)
        for tweet in tweets:
            tweet_texts.append(tweet.text)
    except:
        pass
    return tweet_texts

def analyze_sentiments(tweets_list):
    sentiment_list = []
    for tweet in tweets_list:
        sentiment_list.append(vader.polarity_scores(tweet)["compound"])
    return sentiment_list

def most_negative_tweet(sentiment_list, tweets_list):
    min_sentiment = min(sentiment_list)
    index = sentiment_list.index(min_sentiment)
    return tweets_list[index]

def most_positive_tweet(sentiment_list, tweets_list):
    max_sentiment = max(sentiment_list)
    index = sentiment_list.index(max_sentiment)
    return tweets_list[index]

def main():
    query = '$SQ'
    count = 100
    tweets = pull_tweets(query,count)
    sentiments = analyze_sentiments(tweets)
    print(most_negative_tweet(sentiments, tweets))
    print(most_positive_tweet(sentiments, tweets))
    print((sum(sentiments))/(len(sentiments)))

if __name__ == "__main__":
    main()
