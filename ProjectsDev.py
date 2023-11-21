import praw
import re
import pandas as pd
import openai
import os

os.getcwd()

class RedditFinancialScraper:
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self.stock_regex = r'\b[A-Z]{2,4}\b'
        self.nfl_regex = r'\b(49ers|Bears|Bengals|Bills|Broncos|Browns|Buccaneers|Cardinals|Chargers|Chiefs|Colts|Cowboys|Dolphins|Eagles|Falcons|Giants|Jaguars|Jets|Lions|Packers|Panthers|Patriots|Raiders|Rams|Ravens|Redskins|Saints|Seahawks|Steelers|Texans|Titans|Vikings)\b'

    def get_posts(self, subreddit, category= 'hot', limit= 10):
        """
        Generalized method to get posts from a subreddit.
        'category' can be 'hot', 'new', 'top', etc.
        """
        return getattr(self.reddit.subreddit(subreddit), category)(limit=limit)

    def find_ticker_symbols(self, text):
        # A simple regex that looks for 2 to 4 uppercase characters in a row, denoting a stock ticker
        if category == 'stocks':
            pattern = self.stock_regex
        elif category == 'nfl':
            pattern = self.nfl_regex
        else:
            raise ValueError(f"Unknown category: {category}")      
       
        return set(re.findall(pattern, text, re.IGNORECASE))


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
    def aggr_results(self, df):
        if df == None: 
            rdf == pd.DataFrame()
        else:
            rdf = df
        rdf[rdf[rdf.columns[3]].apply(lambda x: len(x) > 0)]
        
class Feed_GPT:
    # Assume 'scraper_results' is the output from your RedditFinancialScraper
    # For example, a list of dictionaries containing post/comment data

    # Prepare the data for GPT-4
    def prepare_data_for_gpt4(scraper_results):
        formatted_text = ""
        for item in scraper_results:
            formatted_text += f"Title: {item['post_title']}\n"
            formatted_text += f"Body: {item['post_body']}\n"
            formatted_text += "Tickers: " + ", ".join(item['relevant_tickers']) + "\n\n"
        return formatted_text

    # Send the data to GPT-4 for analysis
    def analyze_with_gpt4(data):
        openai.api_key = 'your-api-key'

        response = openai.Completion.create(
            model="text-davinci-004",
            prompt=data,
            max_tokens=150
        )
        
        return response.choices[0].text.strip()

    # Main workflow
    formatted_data = prepare_data_for_gpt4(scraper_results)
    gpt4_response = analyze_with_gpt4(formatted_data)

    print(gpt4_response)



client_id = 'XAk2clILlbCHWFZgIU204g'
client_secret = 'YA8hiEwW_1M0PhatDQMhpzbF1-km0w'
user_agent = "platform:TopTalked:v1.0 (by /u/masterang3)"

gpt_api_key = "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"




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



 







#rdf = pd.DataFrame(r[0])
#print(rdf)



import re

class DataScraper:

    def find_symbols_or_teams(self, text, category):
        if category == 'stocks':
            pattern = self.stock_regex
        elif category == 'nfl':
            pattern = self.nfl_regex
        else:
            raise ValueError(f"Unknown category: {category}")

        return set(re.findall(pattern, text, re.IGNORECASE))

# Usage example
scraper = DataScraper()
text_to_search = "Sample text containing Giants, NYSE, and Patriots."
matches = scraper.find_symbols_or_teams(text_to_search, "nfl")
print(matches)
