'''
Authors: Anurag Purker, & GPT
'''

import praw
import re
import pandas as pd
# import openai
# import os
# import orjson
from datetime import datetime
import praw
import re
import json
from datetime import datetime
from fuzzywuzzy import fuzz

class RedditFinancialScraper:

    def __init__(self, client_id, client_secret, user_agent, ticker_file):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self.stock_regex = r'\b[A-Z]{2,5}(?:\.[A-Za-z]+)?\b'
        self.ticker_list = self.load_ticker_list(ticker_file)

    def load_ticker_list(self, ticker_file):
        with open(ticker_file, 'r') as file:
            ticker_data = json.load(file)
        ticker_dict = {item["ticker"]: item["title"] for item in ticker_data.values()}
        return ticker_dict

    def get_posts(self, subreddit,category='hot',limit=10):
        ### try to write off file before just dumping data
        return getattr(self.reddit.subreddit(subreddit), category)(limit=limit)
    
    def find_symbols(self, text):
        pattern = self.stock_regex
        found_tickers = set(re.findall(pattern, text))
        matched_companies = self.match_companies(text)
        for company in matched_companies:
            found_tickers.add(company)
        valid_tickers = {ticker: (ticker.upper() in self.ticker_list.keys()) if ticker.upper() in self.ticker_list.keys() else False for ticker in found_tickers}
        return valid_tickers

    def extract_post_data(self, post):
        post_data = {
            "post_title": post.title,
            "post_date": post.created_utc,  
            "post_body": post.selftext,
            "comments": self.extract_comments_data(post.comments)
        }
        post_data['relevant_tickers'] = self.find_symbols(post_data['post_body'])
        return post_data

    def extract_comments_data(self, comments):
        comments.replace_more(limit=None)
        comment_data = []
        for comment in comments.list():
            comment_dict = {
                "comment_date": comment.created_utc,
                "comment_body": comment.body,
            }
            comment_dict['relevant_tickers'] = self.find_symbols(comment_dict['comment_body'])
            comment_data.append(comment_dict)
        return comment_data

    def most_discussed_org(self, subreddit,limit=10,category='hot'):
        results = []
        for post in self.get_posts(subreddit, category, limit=limit):
            post_data = self.extract_post_data(post)
            results.append(post_data)
        return results
    
    def most_discussed_org_from_sticky(self, subreddit, limit=10):
        results = []
        for post in self.get_posts(subreddit, category='hot', limit=limit):
            if post.stickied:
                post_data = self.extract_post_data(post)
                results.append(post_data)
                break  # Stop after processing the first stickied post
        return results

    def match_companies(self, comment_text):
        sec_dict = self.ticker_list
        relevant_tickers = []
        for ticker, company_name in sec_dict.items():
            similarity_score = fuzz.partial_ratio(company_name.lower(), comment_text.lower())
            if similarity_score > 70:
                relevant_tickers.append(ticker)
                # print(f"Found reference to {ticker} ({company_name}) in the comment.")
        return relevant_tickers

# '''
# Authors: Anurag Purker, & GPT
# '''
# import praw
# import re
# import pandas as pd
# import openai
# import os
# import json
# from datetime import datetime
# import praw
# import re
# import json
# from datetime import datetime

# class RedditFinancialScraper:
#     def __init__(self, client_id, client_secret, user_agent, ticker_file):
#         self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
#         self.stock_regex = r'\b[A-Z]{2,5}(?:\.[A-Za-z]+)?\b'
#         self.ticker_list = self.load_ticker_list(ticker_file)

#     def load_ticker_list(self, ticker_file):
#         with open(ticker_file, 'r') as file:
#             ticker_data = json.load(file)
#         return set([ticker['ticker'] for ticker in ticker_data.values()])

#     def get_posts(self, subreddit,category='hot',limit=10):
#         return getattr(self.reddit.subreddit(subreddit), category)(limit=limit)

#     def find_symbols(self, text):
#         pattern = self.stock_regex
#         found_tickers = set(re.findall(pattern, text))
#         valid_tickers = {ticker: (ticker.upper() in self.ticker_list) if ticker.upper() in self.ticker_list else False for ticker in found_tickers}
#         return valid_tickers

#     def extract_post_data(self, post):
#         post_data = {
#             "post_title": post.title,
#             "post_date": post.created_utc,
#             "post_body": post.selftext,
#             "comments": self.extract_comments_data(post.comments)
#         }
#         post_data['relevant_tickers'] = self.find_symbols(post_data['post_body'])
#         return post_data

#     def extract_comments_data(self, comments):
#         comments.replace_more(limit=None)
#         comment_data = []
#         for comment in comments.list():
#             # if isinstance(comment, praw.models.MoreComments):
#             #     continue
#             comment_dict = {
#                 "comment_date": comment.created_utc,
#                 "comment_body": comment.body,
#                 # "relevant_tickers": list(self.find_symbols(comment.body))
#             }
#             comment_dict['relevant_tickers'] = self.find_symbols(comment_dict['comment_body'])
#             comment_data.append(comment_dict)
#         return comment_data

#     def most_discussed_org(self, subreddit,limit=10,category='hot'):
#         results = []
#         for post in self.get_posts(subreddit, category, limit=limit):
#             post_data = self.extract_post_data(post)
#             results.append(post_data)
#         return results
    
#     def most_discussed_org_from_sticky(self, subreddit, limit=10):
#         results = []
#         for post in self.get_posts(subreddit, category='hot', limit=limit):
#             if post.stickied:
#                 post_data = self.extract_post_data(post)
#                 results.append(post_data)
#                 break  # Stop after processing the first stickied post
#         return results
    
#     def match_companies(self, comment_text, ticker_dict):
        
#         if ticker_dict is None:
#             ticker_dict = self.ticker_list
#         sec_dict = {v: k for k, v in self.ticker_list.items()}
        
#         relevant_tickers = []
#         for ticker, company_name in sec_dict.items():
#             similarity_score = fuzz.partial_ratio(company_name.lower(), comment_text.lower())
#             print(similarity_score)
#             if similarity_score > 80:
#             relevant_tickers.append(ticker)
#             print(f"Found reference to {ticker} ({company_name}) in the comment.")
#         return relevant_tickers
        
        
        
        
        
        
        
        
        
        
#         if ticker_dict is None:
#             ticker_dict = self.ticker_list
#         sec_dict = {v: k for k, v in ticker_dict.items()}
        
#         relevant_companies = []
#         for ticker, company_name in sec_dict.items():
#             similarity_score = fuzz.partial_ratio(company_name.lower(), comment_text.lower())
#             sim = fuzz.ratio(comment_text.lower(), company_name.lower())
#             print(similarity_score)
#             print(sim)
#             if similarity_score > 80:
#                 relevant_companies.append(company_name)
#                 print(f"Found reference to {ticker} ({company_name}) in the comment.")
#         return relevant_companies
# # class RedditFinancialScraper:
# #     def __init__(self, client_id, client_secret, user_agent, ticker_file):
# #         self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
# #         self.stock_regex = r'\b[A-Z]{2,5}(?:\.[A-Za-z]+)?\b'
# #         self.ticker_list = self.load_ticker_list(ticker_file)

# #     def load_ticker_list(self, ticker_file):
# #         with open(ticker_file, 'r') as file:
# #             ticker_data = json.load(file)
# #         return set([ticker['ticker'] for ticker in ticker_data.values()])

# #     def get_posts(self, subreddit, category='hot', limit=10):
# #         return getattr(self.reddit.subreddit(subreddit), category)(limit=limit)

# #     def find_symbols(self, text):
# #         pattern = self.stock_regex
# #         found_tickers = set(re.findall(pattern, text))
# #         return found_tickers

# #     def extract_post_data(self, post):
# #         post_data = {
# #             "post_title": post.title,
# #             "post_date": post.created_utc,
# #             "post_body": post.selftext,
# #             "comments": self.extract_comments_data(post.comments)
# #         }
# #         post_data['relevant_tickers'] = list(self.find_symbols(post_data['post_body']))
# #         return post_data

# #     def extract_comments_data(self, comments):
# #         comments.replace_more(limit=None)
# #         comment_data = []
# #         for comment in comments.list():
# #             comment_dict = {
# #                 "comment_date": comment.created_utc,
# #                 "comment_body": comment.body,
# #                 "relevant_tickers": list(self.find_symbols(comment.body))
# #             }
# #             comment_data.append(comment_dict)
# #         return comment_data

# #     def most_discussed_org(self, subreddit, limit=10, category='hot'):
# #         results = []
# #         for post in self.get_posts(subreddit, category, limit=limit):
# #             post_data = self.extract_post_data(post)
# #             results.append(post_data)
# #         return results

# #     def most_discussed_org_from_sticky(self, subreddit, limit=10):
# #         results = []
# #         for post in self.get_posts(subreddit, category='hot', limit=limit):
# #             if post.stickied:
# #                 post_data = self.extract_post_data(post)
# #                 results.append(post_data)
# #                 break  # Stop after processing the first stickied post
# #         return results