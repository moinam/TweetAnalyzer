# TweetAnalyzer : Trend Recognition in the WissZeitVG

Twitter has become a social media platform that gives voice to many people around the world. We used this platform to understand and recognize Twitter trends in the WissZeitVG Discussion: ”#IchBinHanna” and tried to zoom in on the recent aspects of the debate. We focus on the events associated with the amendment to the Science Fixed-Term Contract Act (WissZeitVG) in 2016 (Deutscher Bundestag, 2015).
We performed a trend analysis on the tweets by performing a hashtag analysis and analysis of the text of the tweets. We use a hashtag grouping methodology with sentence embedding to group hashtags and topic modeling techniques such as LDA and BERTopic to find ”interesting” topics of discussion in the tweets. In this report, we summarize our findings and understanding of the tweets as we see them and shed light on the debate of the WissZeitVG Discussion: ”#IchBinHanna”.

## Questions which we seeked to be answered after our analysis:

1. What are the prominent hashtags in the tweets extracted?
    - What is the concurrency between the hashtags?
    - How can we form a cluster of similar hashtags?
    - How do the clusters and hashtags change over time?
2. What latent topics are found in the tweets?
    - How do the topics change over time?
3. What are the topics talked about in each hashtag cluster?
    - How do the topics in the hashtag clusters change over time?

## The scripts overview:

- ``create_dataset.py`` : This python script is responsible for fetching tweets from the Twitter API. ``auth_config.py`` contains the API credentials of the Twitter developer account. You will need to add your credentials here for it to start working out of the box.

- ``Text_Analysis_Visualize.ipynb`` & ``Trend_Evaluation_Hashtag Analysis_Graphs.ipynb`` : This notebook creates visualizations from the tweets gathered from the Twitter API.

- ``Tweet_Analysis_Pipeline.ipynb`` , ``workflow_Clustering_hashtags.ipynb`` & ``TopicModelling.ipynb`` : This notebook contains all the pipeline functions to carry down the tweet analysis before they can be visualized.

## Full System Architecture
![Alt text](graphs/Full%20Arch.PNG)