import sys

sys.path.append(r"C:\Users\anura\Documents\PyProjects\FoolAround")

import os
import pandas as pd
import numpy as np
import json
import requests
from ProjectsDev import RedditFinancialScraper
# from GPTClassinDev import GptSentimentAnalysis


#Get AuthKeys
client_id = os.environ.get('REDDIT_CLIENT_ID')
client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
user_agent = os.environ.get('REDDIT_USER_AGENT')
openai_api_key = os.environ.get('OPENAI_API_KEY')

json_file_path = r'C:\Users\anura\Documents\PyProjects\FoolAround\SupportingFiles\company_tickers.json'
scraper = RedditFinancialScraper(client_id=client_id, client_secret=client_secret, user_agent=user_agent,ticker_file = json_file_path)

#ValueInvestingSub
vi_hot_post= scraper.most_discussed_org(subreddit = 'ValueInvesting', category='hot',type = 'stocks')
vihp_df = pd.DataFrame(vi_hot_post[0])
print(vihp_df)
vh_slice = vihp_df.iloc[0:5,:]




vihp_df.to_csv(r'C:\Users\anura\OneDrive\Documents\Python Scripts\ValueInvestingTestDf.csv')


 
