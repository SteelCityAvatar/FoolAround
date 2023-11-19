import praw
import re
import pandas as pd
import os
os.getcwd()
# Usage
client_id = 'XAk2clILlbCHWFZgIU204g'
client_secret = 'YA8hiEwW_1M0PhatDQMhpzbF1-km0w'
user_agent = "platform:TopTalked:v1.0 (by /u/masterang3)"

#Authorization: Bearer $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



class RedditFinancialScraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)


    def get_posts(self, subreddit, category= 'hot', limit= 10):
        """
        Generalized method to get posts from a subreddit.
        'category' can be 'hot', 'new', 'top', etc.
        """
        return getattr(self.reddit.subreddit(subreddit), category)(limit=limit)

    def find_ticker_symbols(self, text):
        # A simple regex that looks for 2 to 4 uppercase characters in a row, denoting a stock ticker
        return set(re.findall(r'\b[A-Z]{2,4}\b', text))


    def most_discussed_companies(self, subreddit, category='hot', limit=10):
        results = []
        counter = {}
        for i, submission in enumerate(self.get_posts(subreddit, category, limit)):
            post_tickers = self.find_ticker_symbols(submission.title) | self.find_ticker_symbols(submission.selftext)
            
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
                comment_tickers = self.find_ticker_symbols(comment.body)
                
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

    def most_discussed_companies_from_sticky(self, subreddit, limit=10):
        results = []
        counter = {}
        for submission in self.get_posts(subreddit, category='hot',limit = limit):
            if submission.stickied:
                submission.comments.replace_more(limit=0)  # Load all comments
                for i, comment in enumerate(submission.comments.list()):
                    tickers = self.find_ticker_symbols(comment.body)
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



scraper = RedditFinancialScraper(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

#ValueInvestingSub
vi_hot_post= scraper.most_discussed_companies(subreddit = 'ValueInvesting', category='hot')
vihp_df = pd.DataFrame(vi_hot_post[0])
vihp_df.to_csv(r'C:\Users\anura\OneDrive\Documents\Python Scripts\ValueInvestingTestDf.csv')

r1 = scraper.most_discussed_companies_from_sticky(subreddit='ValueInvesting')
r1_df = pd.DataFrame(r1[0])

#WallStreetBetsSub
wsb_hot_post = scraper.most_discussed_companies_from_hot_posts(subreddit='wallstreetbets',limit=100)
wsbhp_df = pd.DataFrame(wsb_hot_post[0])
r2 = scraper.most_discussed_companies_from_sticky(subreddit='wallstreetbets')
r2_df = pd.DataFrame(r2[0])


 



def aggr_results(self, df):


rdf = pd.DataFrame(r[0])
print(rdf)
rdf[rdf[rdf.columns[3]].apply(lambda x: len(x) > 0)]



