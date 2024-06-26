from auth_config import TWITTER_CONFIG
import tweepy
import pandas as pd
import time
from datetime import datetime

def append_tweets(tweets):
    '''Generate Tweet Structure and append in tweetsSet array\n
       Parameters
           tweets: array of tweets object
    '''
    def fill_data_struct(tweet):
        '''Fill up the tweet data structure to be appended\n
           Parameters
                tweets: array of tweets object
        '''
        tweet_data_template = {
            "timestamp": "",
            "tweet_id": "",
            "conversation_id": "",
            "author_id": "",
            "text": "",
            "retweet_count": 0,
            "reply_count": 0,
            "like_count": 0,
            "quote_count": 0,
            "referenced_tweets": [],
            "hashtags": [],
            "tweet_type": "original"
        }
        tweet_data_template['timestamp'] = tweet['created_at']
        tweet_data_template['tweet_id'] = tweet['id']
        tweet_data_template['conversation_id'] = tweet['conversation_id']
        tweet_data_template['author_id'] = tweet['author_id']
        tweet_data_template['text'] = tweet['text']
        tweet_data_template['retweet_count'] = tweet['public_metrics']['retweet_count']
        tweet_data_template['reply_count'] = tweet['public_metrics']['reply_count']
        tweet_data_template['like_count'] = tweet['public_metrics']['like_count']
        tweet_data_template['quote_count'] = tweet['public_metrics']['quote_count']

        try:
            for ref in tweet['referenced_tweets']:
                tweet_data_template['referenced_tweets'].append(ref)
                if ref['type'] == "retweeted":
                    tweet_data_template['tweet_type'] = "retweet"
        except Exception as e:
            None
        try:
            for tags in tweet['entities']['hashtags']:
                tweet_data_template['hashtags'].append(tags['tag'])
        except Exception as e:
            None

        return tweet_data_template

    try:
        for tweet in tweets.data:
            struct_tweet = fill_data_struct(tweet.data)
            tweetsSet.append(struct_tweet)
    except Exception as e:
        print("Exception (tweet.data):", e)
    
    try:
        for tweet in tweets.includes['tweets']:
            struct_tweet = fill_data_struct(tweet.data)
            tweetsSet.append(struct_tweet)
    except Exception as e:
        print("Exception (tweet.includes):", e)


def magic_query_maker(authors):
    '''Create Dynamic query with each query having a set of 20 authors\n
       from where we are to fetch the tweets.\n
       Parameters
          authors: author list to be added in query
       Returns
          query: Created Query 
    '''
    query = '("#IchBinHanna" OR "#IchBinReyhan" OR "#IchBinJelena" \
OR "#IchBinMelek" OR "#IchBinHannaCH" OR "#IchBinHannaAT" \
OR "#IchBinHannaInUK" OR "#IchWarHanna" OR "#HannasChef" \
OR "#WissZeitVG" OR "#95vsWissTeitVG" OR "#GegenWissZeitVG10" \
OR "#ACertainDegreeofFlexibility" OR "#WissSystemFehler" \
OR "#FristIsFrust" OR "#Dauerstellen" OR "#AcademicPrecarity" OR "#stopprecarity") '
    spec_query = query + '('
    for author_id in authors:
        if author_id != authors[-1]:
            spec_query += 'from:' + str(author_id) + ' OR '
        else:
            spec_query += 'from:' + str(author_id)
    spec_query += ')'
    return spec_query


def fetch_query(query, next_token=None):
    ''' Fetch tweets from Twitter V2 API using the client.search_all_tweets()\n
        It has a sleep mechanism to handle rate caps and exceptions from twitter endpoints.\n
        Parameters
          authors: author list to be added in query
        Returns
          query: Created Query 
    '''
    tweets = None
    res = True
    while (res):
        try:
            time.sleep(1)
            if (next_token):
                tweets = client.search_all_tweets(query=query, start_time=start_time, end_time=end_time,
                                                  expansions=expansions, tweet_fields=tweet_fields, max_results=500, next_token=next_token)
            else:
                tweets = client.search_all_tweets(query=query, start_time=start_time, end_time=end_time,
                                                  expansions=expansions, tweet_fields=tweet_fields, max_results=500)
            res = False
        except Exception as e:
            try:
                if e.response.status_code == 429:
                    temp_time = datetime.now().strftime("%c")
                    print(
                    f" Rate Limit Exhausted, Sleeping for 500 seconds. Timestamp:{temp_time}")
                    time.sleep(500)
                else:
                    print(f"Exception: {e}, Retry...")
            except:
                print(f"Exception: {e}, Retry...")
                
    return tweets


def extract_data():
    ''' Main function to be called to start data extraction\n
    '''
    requests = 0
    cur_auth_batch = 0
    for id in range(0, len(authors), 20):
        spec_query = magic_query_maker(authors=authors[id:id+20])
        init_tweets = fetch_query(spec_query)
        requests += 1
        cur_auth_batch += 1
        try:
            append_tweets(tweets=init_tweets)
            try:
                next_token = init_tweets.meta['next_token']
                while (next_token):
                    tweets = fetch_query(spec_query, next_token=next_token)
                    requests += 1
                    try:
                        next_token = tweets.meta['next_token']
                    except:
                        next_token = None
                    append_tweets(tweets=tweets)
            except:
                next_token = None
        except Exception as e:
            print(
                "No Tweets found[likely to be the case] and the Exception: ", e)
        print(
            f"Auth Batch: {cur_auth_batch}: No. of requests to Twitter: {requests}  Tweets Extracted:{len(tweetsSet)}")
            
    df = pd.json_normalize(tweetsSet)
    df.to_csv("extracted_tweets_dataset.csv", index=False)


""" Tweepy Client Configuration - START"""
bearer_token = TWITTER_CONFIG['bearer_token']
access_token = TWITTER_CONFIG['access_token']
access_token_secret = TWITTER_CONFIG['access_token_secret']
client = tweepy.Client(
    bearer_token=bearer_token, access_token=access_token, access_token_secret=access_token_secret)
""" Tweepy Client Configuration - END"""

""" Query Config"""
start_time = '2021-06-01T00:00:00Z'
end_time = '2022-11-01T00:00:00Z'
expansions = ['author_id', 'referenced_tweets.id']
tweet_fields = ['created_at', 'public_metrics', 'conversation_id', 'entities']
twitter_query_data = pd.read_csv('twitter_data.csv')
tweetsSet = []
authors = twitter_query_data.author_id.unique()
conversations = twitter_query_data.conversation_id.unique()
""" Query Configuration - END"""

print("################### Let the Twitter Games Begin ####################")
extract_data()
print("############ Alas the Twitter Games have Ended - Adieu #############")