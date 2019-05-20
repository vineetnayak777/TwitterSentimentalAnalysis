

import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy as np
import matplotlib.pyplot as plt


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'nvvUNV0SGiRg7CxoZKdfU4fp7'
        consumer_secret = '9NMhqUf5NrlTMDusflewMcFTJVy4Dv97t6EJiTyfbWWJrD4bOT'
        access_token = '1095628662894985218-2t6yTA1FyDevaycazpXuIv99SEHeaP'
        access_token_secret = 'R1vR665G9CTt2hFc783XQMl824M4LkVWOlX2SYOFrhhbo'

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
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

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

    def get_tweets(self, query, count=100000000):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count,lang="en",since="2015-01-20")
            print("Total tweets == %d", len(fetched_tweets))
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main(inputer):
    # creating object of TwitterClient Class
    api = TwitterClient()
    print(inputer)
     # calling function to get tweets
    tweets = api.get_tweets(query=inputer, count=500000)
    print("Total tweets = %d", len(tweets))

    # To Save Tweets Collected
    with open("ReadTweets.csv", "a", encoding="UTF-8") as f:
        for i in range(0, len(tweets)):
            f.write(str(tweets[i]))
            f.write("\n")
        f.close()

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Hello ptweets")

    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))


# picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print(ntweets)
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
        ".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'],"\n")
        ptttweets=tweet['text']

        # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'],"\n")
        ntttweets=tweet['text']

    nuetweets = (len(tweets) - len(ntweets) - len(ptweets))
    nttweets=len(ntweets)
    pttweets=len(ptweets)

    label = "Positive", "Negative", "Neutral"
    explode = (0.1, 0, 0)
    sizes = [len(ptweets), len(ntweets), nuetweets]
    colors = ["Gold", "Red", "green"]
    plt.pie(sizes, explode=explode, labels=label, colors=colors, autopct="%f%%")
    plt.axis("Equal")
    plt.show()
    return pttweets,nttweets,nuetweets,ptttweets,ntttweets,inputer


if __name__ == "__main__":
    # calling main function
    main()