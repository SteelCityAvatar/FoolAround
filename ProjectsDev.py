import praw
import re
import pandas as pd
import openai
import os

os.getcwd()
import json
file_path = r'C:\Users\anura\OneDrive\Documents\Python Scripts\FoolAround\SupportingFiles\company_tickers.json'


class RedditFinancialScraper:
    def __init__(self, client_id, client_secret, user_agent, ticker_file='company_tickers.json'):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self.stock_regex = r'\b[A-Z]{2,4}\b'
        self.nfl_regex = r'\b(49ers|Bears|Bengals|Bills|Broncos|Browns|Buccaneers|Cardinals|Chargers|Chiefs|Colts|Cowboys|Dolphins|Eagles|Falcons|Giants|Jaguars|Jets|Lions|Packers|Panthers|Patriots|Raiders|Rams|Ravens|Redskins|Saints|Seahawks|Steelers|Texans|Titans|Vikings)\b'
        self.ticker_list = self.load_ticker_list(ticker_file)

    def load_ticker_list(self, ticker_file):
        with open(ticker_file, 'r') as file:
            ticker_data = json.load(file)
        return set([ticker['ticker'] for ticker in ticker_data.values()])  # Assuming 'ticker' is the key for ticker symbols

    def get_posts(self, subreddit, category= 'hot', limit= 10):
        """
        Generalized method to get posts from a subreddit.
        'category' can be 'hot', 'new', 'top', etc.
        """
        return getattr(self.reddit.subreddit(subreddit), category)(limit=limit)
    
    def find_symbols(self, text, type):
        if type == 'stocks':
            pattern = self.stock_regex
            found_tickers = set(re.findall(pattern, text, re.IGNORECASE))
            # Filter tickers against the ticker list
            valid_tickers = {ticker for ticker in found_tickers if ticker.upper() in self.ticker_list}
            return valid_tickers
        elif type == 'nfl':
            pattern = self.nfl_regex
            return set(re.findall(pattern, text, re.IGNORECASE))
        else:
            raise ValueError(f"Unknown category: {type}")

    def most_discussed_org(self, subreddit, category='hot',type = 'stocks', limit=10):
        results = []
        counter = {}
        for i, submission in enumerate(self.get_posts(subreddit, category, limit)):
            post_tickers = self.find_symbols(submission.title,type = type) | self.find_symbols(submission.selftext, type = type)
            
            # Update the counter for each ticker found in the post title and body
            for ticker in post_tickers:
                counter[ticker] = counter.get(ticker, 0) + 1
            
            # Add post data to the results
            post_data = {
                "post_title": submission.title,
                "post_number": i,
                "post_body": submission.selftext,
                "relevant_tickers": list(post_tickers)
            }
            results.append(post_data)
            
            # Process the comments
            submission.comments.replace_more(limit=0)  # Load all comments
            for j, comment in enumerate(submission.comments.list()):
                comment_tickers = self.find_symbols(comment.body, type = type)
                
                # Update the counter for each ticker found in the comments
                for ticker in comment_tickers:
                    counter[ticker] = counter.get(ticker, 0) + 1
                
                # Add comment data to the results if tickers are found
                if comment_tickers:
                    comment_data = {
                        "post_title": submission.title,
                        "comment_number": j,
                        "comment": comment.body,
                        "relevant_tickers": list(comment_tickers)
                    }
                    results.append(comment_data)

        return results, sorted(counter.items(), key=lambda item: item[1], reverse=True)

    def most_discussed_org_from_sticky(self, subreddit, type = 'stocks',limit=10):
        results = []
        counter = {}
        for submission in self.get_posts(subreddit, category='hot',limit = limit):
            if submission.stickied:
                submission.comments.replace_more(limit=0)  # Load all comments
                for i, comment in enumerate(submission.comments.list()):
                    tickers = self.find_symbols(comment.body,type= type)
                    for ticker in tickers:
                        counter[ticker] = counter.get(ticker, 0) + 1
                    
                    comment_data = {
                        "stickied_post": submission.title,
                        "comment_number": i,
                        "comment": comment.body,
                        "relevant_tickers": list(tickers)
                    }
                    results.append(comment_data)

        return results, sorted(counter.items(), key=lambda item: item[1], reverse=True)
    def aggr_results(self, df):
        if df == None: 
            rdf == pd.DataFrame()
        else:
            rdf = df
        rdf[rdf[rdf.columns[3]].apply(lambda x: len(x) > 0)]
        
# class Feed_GPT:
#     # Assume 'scraper_results' is the output from your RedditFinancialScraper
#     # For example, a list of dictionaries containing post/comment data

#     # Prepare the data for GPT-4
#     def prepare_data_for_gpt4(scraper_results):
#         formatted_text = ""
#         for item in scraper_results:
#             formatted_text += f"Title: {item['post_title']}\n"
#             formatted_text += f"Body: {item['post_body']}\n"
#             formatted_text += "Tickers: " + ", ".join(item['relevant_tickers']) + "\n\n"
#         return formatted_text

#     # Send the data to GPT-4 for analysis
#     def analyze_with_gpt4(data):
#         openai.api_key = 'your-api-key'

#         response = openai.Completion.create(
#             model="text-davinci-004",
#             prompt=data,
#             max_tokens=150
#         )
        
#         return response.choices[0].text.strip()

#     # Main workflow
#     formatted_data = prepare_data_for_gpt4(scraper_results)
#     gpt4_response = analyze_with_gpt4(formatted_data)

#     print(gpt4_response)

client_id = 'XAk2clILlbCHWFZgIU204g'
client_secret = 'YA8hiEwW_1M0PhatDQMhpzbF1-km0w'
user_agent = "platform:TopTalked:v1.0 (by /u/masterang3)"

gpt_api_key = "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"
alpha_vantage_api_key = "XZHHOU228LC1U5AZ"





scraper = RedditFinancialScraper(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

#ValueInvestingSub
vi_hot_post= scraper.most_discussed_org(subreddit = 'ValueInvesting', category='hot',type = 'stocks')
vihp_df = pd.DataFrame(vi_hot_post[0])
print(vihp_df)
#vihp_df.to_csv(r'C:\Users\anura\OneDrive\Documents\Python Scripts\ValueInvestingTestDf.csv')

r1 = scraper.most_discussed_org_from_sticky(subreddit='ValueInvesting', type = 'stocks')
r1_df = pd.DataFrame(r1[0])
print()

#WallStreetBetsSub
wsb_hot_post = scraper.most_discussed_org(subreddit='wallstreetbets',category = 'hot',type = 'stocks',limit=100)
wsbhp_df = pd.DataFrame(wsb_hot_post[0])
wsbhp_df.to_csv(r'C:\Users\anura\OneDrive\Documents\Python Scripts\WSBTestDf.csv')

r2 = scraper.most_discussed_org_from_sticky(subreddit='wallstreetbets',type = 'stocks')
r2_df = pd.DataFrame(r2[0])

#SportsBetting
sb_hot_post = scraper.most_discussed_org(subreddit = 'sportsbook', type = 'nfl')
pd.DataFrame(sb_hot_post[0])



