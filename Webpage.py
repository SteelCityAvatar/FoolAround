import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
# import ast
# Read the CSV file

vi_hot_post = pd.read_json('vi_hot_post.json')
df = pd.DataFrame(vi_hot_post)
df.columns
def extract_tickers(comments):
    tickers = []
    for comment in comments:
        tickers.extend(list(comment['relevant_tickers'].keys()))
    return tickers

df['relevant_comments'] = df['comments'].apply(extract_tickers)
df.columns

# Well what i'd like to do is to extract tickers from the comments, and keep the comments in a searchable datastructure that Ic an reference based on the tickers


# from collections import defaultdict

# def extract_tickers(comments):
#     tickers = defaultdict(list)
#     for comment in comments:
#         for ticker in comment['relevant_tickers'].keys():
#             tickers[ticker].append(comment['comment_body'])
#     return dict(tickers)

# df['relevant_comments'] = df['comments'].apply(extract_tickers)