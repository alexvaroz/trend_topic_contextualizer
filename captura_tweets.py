from typing import List

import tweepy
from tweepy import OAuthHandler, Stream, Cursor
import streamlit as st
import pandas as pd
import nltk
import re

nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('portuguese')

woeid_Brazil = 23424768

auth = OAuthHandler(st.secrets['consumer_key'], st.secrets['consumer_secret'])
auth.set_access_token(st.secrets['access_token_key'], st.secrets['access_token_secret'])

api = tweepy.API(auth, wait_on_rate_limit=False)


def list_trend_topics():
    trend_topics = api.get_place_trends(woeid_Brazil)
    df_trends = pd.DataFrame(trend_topics[0]['trends'])
    return df_trends['name'].head(10)


def list_tweets_by_trend_topic(trend_topic: str):
    tweets = api.search_tweets(q=trend_topic + " -filter:retweets",
                               tweet_mode='extended', lang='pt', count=100)
    tweets_list = []
    for tweet in tweets:
        tweets_list.append(tweet.full_text)
    return tweets_list


def tweet_cleaner(tweet: str):
    tweet = re.sub("[@&][A-Za-z0-9_]+","", tweet)     # Remove mentions
    tweet = re.sub(r"http\S+","", tweet)           # Remove media links
    return tweet


def prepare_tweets(tweets_list: List[str]):
    clean_tweets = [tweet_cleaner(tweet.lower()) for tweet in tweets_list]
    return clean_tweets


def tweet_cleaner(x):
    text = re.sub("[@&][A-Za-z0-9_]+", "", x)  # Remove mentions
    text = re.sub(r"http\S+", "", text)  # Remove media links
    return text

