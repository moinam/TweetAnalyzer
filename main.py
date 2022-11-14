from twarc.expansions import ensure_flattened
from twarc.client2 import Twarc2
import tweepy

""" Tweepy Client Configuration - START"""
bearer_token = ''
access_token = ''
access_token_secret = ''
client = tweepy.Client(
    bearer_token=bearer_token, access_token=access_token, access_token_secret=access_token_secret)
start_time = '2021-06-21T00:00:00Z'
end_time = '2022-10-31T00:00:00Z'
""" Tweepy Client Configuration - END"""

""" Query Config"""
expansions = ['author_id', 'referenced_tweets.id']
tweet_fields = ['created_at', 'public_metrics', 'conversation_id']

# query = '("#IchBinHanna" OR "#IchBinReyhan" OR "#IchBinJelena" \
# OR "#IchBinMelek" OR "#IchBinHannaCH" OR "#IchBinHannaAT" \
# OR "#IchBinHannaInUK" OR "#IchWarHanna" OR "#HannasChef" \
# OR "#WissZeitVG" OR "#95vsWissTeitVG" OR "#GegenWissZeitVG10" \
# OR "#ACertainDegreeofFlexibility" OR "#WissSystemFehler" \
# OR "#FristIsFrust" OR "#Dauerstellen" OR "#AcademicPrecarity" OR "#stopprecarity") \
# (conversation_id:1585056490288996352) (from:268413024)'

query = '(conversation_id:1585056490288996352) (from:268413024)'

# tweets = client.search_recent_tweets(query=query, max_results=10)
tweets = client.search_all_tweets(
    query=query, start_time=start_time, end_time=end_time, expansions=expansions, tweet_fields=tweet_fields)
# , max_results=500

for tweet in tweets.data:
    print(tweet.data)
    # if len(tweet.context_annotations) > 0:
    #     print(tweet.context_annotations)

# t = Twarc2(bearer_token=bearer_token, access_token=access_token,
#            access_token_secret=access_token_secret)

# # search_results is a generator, max_results is max tweets per page, 100 max for full archive search with all expansions.
# search_results = t.search_all(query="(conversation_id:1586724898331934720)",
#                               start_time=start_time, end_time=end_time, max_results=10)

# # Get all results page by page:
# for page in search_results:
#     # Do something with the whole page of results:
#     print(page)
