from auth_config import TWITTER_CONFIG
import tweepy

""" Tweepy Client Configuration - START"""
bearer_token = TWITTER_CONFIG['bearer_token']
access_token = TWITTER_CONFIG['access_token']
access_token_secret = TWITTER_CONFIG['access_token_secret']
client = tweepy.Client(
    bearer_token=bearer_token, access_token=access_token, access_token_secret=access_token_secret)
start_time = '2021-06-21T00:00:00Z'
end_time = '2022-10-31T00:00:00Z'
""" Tweepy Client Configuration - END"""

""" Query Config"""
expansions = ['author_id', 'referenced_tweets.id']
tweet_fields = ['created_at', 'public_metrics', 'conversation_id']

query = '("#IchBinHanna" OR "#IchBinReyhan" OR "#IchBinJelena" \
OR "#IchBinMelek" OR "#IchBinHannaCH" OR "#IchBinHannaAT" \
OR "#IchBinHannaInUK" OR "#IchWarHanna" OR "#HannasChef" \
OR "#WissZeitVG" OR "#95vsWissTeitVG" OR "#GegenWissZeitVG10" \
OR "#ACertainDegreeofFlexibility" OR "#WissSystemFehler" \
OR "#FristIsFrust" OR "#Dauerstellen" OR "#AcademicPrecarity" OR "#stopprecarity") \
(from:268413024)'

tweets = client.search_all_tweets(
    query=query, start_time=start_time, end_time=end_time, expansions=expansions, tweet_fields=tweet_fields, max_results=500)

for tweet in tweets.data:
    print(tweet.data)
    # if len(tweet.context_annotations) > 0:
    #     print(tweet.context_annotations)
