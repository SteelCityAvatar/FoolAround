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
if __name__ == '__main__':

    #add absolute path to directory
    # sys.path.append(r"C:\Users\anura\Documents\PyProjects\FoolAround")
    
    # Get AuthKeys
    client_id = os.environ.get('REDDIT_CLIENT_ID')
    client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
    user_agent = os.environ.get('REDDIT_USER_AGENT')
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    
    # Get the current date and time
    now = datetime.now()
    
    # Format it as a string
    timestamp = now.strftime('%Y%m%d_%H%M%S')

    #Relative path for sec JSON dictionary of companies listed on US stock exchanges
    json_file_path = r'SupportingFiles\company_tickers.json'
    scraper = RedditFinancialScraper(client_id=client_id, client_secret=client_secret, user_agent=user_agent,ticker_file = json_file_path)
    
    #ValueInvestingSub
    # Get the most discussed posts
    vi_hot_post = scraper.most_discussed_org(subreddit='ValueInvesting', category='hot',limit=100)
    # Convert the 'comment_date' and 'post_date' to datetime format
    vi_hot_post
    for post in vi_hot_post:
        if 'comments' in post:
            for comment in post['comments']:
                comment['comment_date'] = datetime.fromtimestamp(comment['comment_date']).isoformat()
        if 'post_date' in post:
            post['post_date'] = datetime.fromtimestamp(post['post_date']).isoformat()
    
    try:
        with open('vi_hot_post.json', 'r') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    test_jsonstr = json.dumps(vi_hot_post, indent=4)
    with open('vi_hot_post.json', 'w') as f:
        f.write(test_jsonstr)
        
    # Update existing data with new data
    existing_data.extend(vi_hot_post)

    # Convert the updated data to a JSON string
    json_string = json.dumps(existing_data, indent=4)

    # Write the updated data back to the file
    with open('vi_hot_post.json', 'w') as f:
         f.write(json_string)

