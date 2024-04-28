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

    sys.path.append(r"C:\Users\anura\Documents\PyProjects\FoolAround")
    # Get AuthKeys
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
    #ValueInvestingSub
    # Get the most discussed posts
    vi_hot_post = scraper.most_discussed_org(subreddit='ValueInvesting', category='hot', type='stocks', limit=10)
    # Convert the 'comment_date' and 'post_date' to datetime format
    for post in vi_hot_post:
        if 'comment_date' in post:
            post['comment_date'] = datetime.fromtimestamp(post['comment_date']).isoformat()
        if 'post_date' in post:
            post['post_date'] = datetime.fromtimestamp(post['post_date']).isoformat()

    # Convert the first item in vi_hot_post to a JSON string
    json_string = json.dumps(vi_hot_post[0], indent=4)

    # Write the JSON string to a file
    with open('vi_hot_post.json', 'w') as f:
        print(json_string)
        f.write(json_string)

