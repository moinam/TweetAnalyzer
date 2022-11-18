from auth_config import TWITTER_CONFIG
import tweepy
import pandas as pd

""" Tweepy Client Configuration - START"""
bearer_token = TWITTER_CONFIG['bearer_token']
access_token = TWITTER_CONFIG['access_token']
access_token_secret = TWITTER_CONFIG['access_token_secret']
client = tweepy.Client(
    bearer_token=bearer_token, access_token=access_token, access_token_secret=access_token_secret)
""" Tweepy Client Configuration - END"""

""" Query Config"""
start_time = '2021-06-21T00:00:00Z'
end_time = '2022-10-31T00:00:00Z'
expansions = ['author_id', 'referenced_tweets.id']
tweet_fields = ['created_at', 'public_metrics', 'conversation_id', 'entities']
twitter_query_data = pd.read_csv('twitter_data.csv')
tweetsSet = []
nt_authors = []
authors = twitter_query_data.author_id.unique()
conversations = twitter_query_data.conversation_id.unique()
""" Query Configuration - END"""


def append_tweets(tweets):

    def fill_data_struct(tweet):
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
        except:
            None
        try:
            for tags in tweet['entities']['hashtags']:
                tweet_data_template['hashtags'].append(tags['tag'])
        except:
            None

        return tweet_data_template

    for tweet in tweets.data:
        struct_tweet = fill_data_struct(tweet.data)
        tweetsSet.append(struct_tweet)

    for tweet in tweets.includes[tweets]:
        struct_tweet = fill_data_struct(tweet.data)
        tweetsSet.append(struct_tweet)


def magic_query_maker(authors):
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


for id in range(0, len(authors), 25):
    spec_query = magic_query_maker(authors=authors[id:id+25])
    init_tweets = client.search_all_tweets(
        query=spec_query, start_time=start_time, end_time=end_time, expansions=expansions, tweet_fields=tweet_fields, max_results=500)

    try:
        append_tweets(tweets=init_tweets)
        try:
            next_token = tweets.meta['next_token']
        except:
            next_token = None
        while (next_token):
            tweets = client.search_all_tweets(query=spec_query, start_time=start_time, end_time=end_time,
                                              expansions=expansions, tweet_fields=tweet_fields, max_results=500, next_token=next_token)
            try:
                next_token = tweets.meta['next_token']
            except:
                next_token = None
            append_tweets(tweets=tweets)
    except:
        nt_authors.append(authors[id:id+24])

df = pd.json_normalize(tweetsSet)
df.to_csv("extracted_tweets_dataset.csv")