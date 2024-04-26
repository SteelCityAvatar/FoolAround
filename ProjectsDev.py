import sys
import os
import pandas as pd
import numpy as np
import json
import requests
from RedditScraper import RedditFinancialScraper
from pyedgar import EDGARIndex, Filing#, Company
from datetime import datetime

# Add the path to the sys.path list
sys.path.append(r"C:\Users\anura\Documents\PyProjects\FoolAround")

# from GPTClassinDev import GptSentimentAnalysis

#Get AuthKeys
client_id = os.environ.get('REDDIT_CLIENT_ID')
client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
user_agent = os.environ.get('REDDIT_USER_AGENT')
openai_api_key = os.environ.get('OPENAI_API_KEY')

# Get the current date and time
now = datetime.now()
# Format it as a string
timestamp = now.strftime('%Y%m%d_%H%M%S')


json_file_path = r'C:\Users\anura\Documents\PyProjects\FoolAround\SupportingFiles\company_tickers.json'
scraper = RedditFinancialScraper(client_id=client_id, client_secret=client_secret, user_agent=user_agent,ticker_file = json_file_path)

ticker_df = pd.read_json(json_file_path).T
ticker_df[ticker_df['ticker']=='OR']

#ValueInvestingSub
vi_hot_post= scraper.most_discussed_org(subreddit = 'ValueInvesting', category='hot',type = 'stocks',limit = 100)
vihp_df = pd.DataFrame(vi_hot_post[0])
vihp_df['comment_date'] = vihp_df['comment_date'].astype('datetime64[s]')
# rdf = vihp_df.iloc[0:5,:]
# rdf[rdf.columns[3]]#.apply(lambda x: len(x) > 0)]


# Use the timestamp in the filename
vihp_df.to_csv(fr'C:\Users\anura\Documents\PyProjects\FoolAround\{timestamp}_ValueInvestingTestDf.csv')


