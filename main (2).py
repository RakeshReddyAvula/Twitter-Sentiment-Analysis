# -*- coding: utf-8 -*-
import re 
import tweepy 
# import tweepy.errors.TweepError 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import numpy as np
import json
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'IaIdBOJa7ZwNI6xHS11Jg5DVb'
        consumer_secret = 'IuZ4G5wrK2aYU1yuOwbPqu6G0Rx1hBgHwo6xEOHANhA4gTzJv9'
        access_token = '2158465844-TYtigqXGBQa5KzshKjz5MFO9SqTVkc03FQLL37N'
        access_token_secret = 'ClgQD5kCml8yb70ZlseUQIXOAM6bltOwoPuD5Z3SWguXW'

        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        #import PreProcessing
        #PreProcessing.preProcess(tweet)
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 

        try: 
            # call twitter api to fetch tweets 
            #fetched_tweets = self.api.search(q = query, count = count) 
            tweets_file = open('twitter_data.txt', "r")
            
            # parsing tweets one by one 
            for tweet in tweets_file: 
                # empty dictionary to store required params of a tweet 
                try:
                    parsed_tweet = {} 
                    
                    tweett = json.loads(tweet)
                    tweet =tweett.get("text")
                    parsed_tweet['text']=tweet
                    
                    # saving text of tweet 
                    #parsed_tweet['text'] = tweet.text 
                    # saving sentiment of tweet 
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet) 
    
                    # appending parsed tweet to tweets list 
                    if tweett.get("retweet_count")> 0:
                        # if tweet has retweets, ensure that it is appended only once 
                        if parsed_tweet not in tweets: 
                            tweets.append(parsed_tweet) 
                    else: 
                        tweets.append(parsed_tweet) 
                except:
                    continue
            # return parsed tweets 
            return tweets 

        except tweepy.errors.TweepyException as e: 
            # print error (if any) 
            print("Error : " + str(e)) 

def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    tweets = api.get_tweets() 

    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets per  centage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets    
    nutweets= len(tweets)-(len(ntweets) + len(ptweets))
    print("Neutral tweets percentage: {} % ".format(100*nutweets/len(tweets))) 
    graph={}
    
    graph.update({"Positive tweets":100*len(ptweets)/len(tweets)})
    graph.update({"Negative tweets":100*len(ntweets)/len(tweets)})
    graph.update({"Neutral tweets":100*nutweets/len(tweets)})
    
    
    import matplotlib.pyplot as pyplot
    import collections
    counts = collections.Counter(graph)
    
    pyplot.pie([float(v) for v in counts.values()], labels=[k  for k in counts],
           autopct=None)
    pyplot.show()
    pyplot.bar(range(len(counts)), list(counts.values()), align='center')
    pyplot.xticks(range(len(counts)), list(counts.keys()))
    pyplot.show()
    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets: 
        print(tweet['text']) 

    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets: 
        print(tweet['text']) 
if __name__ == "__main__": 
    # calling main function 
    main() 

