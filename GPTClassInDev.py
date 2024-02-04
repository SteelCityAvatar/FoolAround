
import requests
import openai
from openai import OpenAI
import pandas as pd

headers = {'Authorization': 'Bearer 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'}
response = requests.get('https://api.openai.com/v1/models', headers=headers)
models = pd.DataFrame(response.json()['data'])
print(models)

openai.api_key = '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'

response = openai.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a highly intelligent AI assistant who provides sentiment analysis on stock market discussions.  You analyze the sentiment of entered reddit posts from financial subreddits.  If there's a concept discussed in the post, try to elaborate on the financial theory with the goal being to implement into a decision model for stocks"},
    {"role": "user", "content": "Look at the ticker list I provide along with the words in the reddit post and give me some sentiment"},
    {"role": "user", "content": "Post: [Weekly Megathread] Markets and Value Stock Ideas, Week of December 25, 2023, comment: I got a quick question, if anyone can answer: When you see estimates for EPS in the next 5 years, does it mean that it's the per year growth or the total growth in the 5 year period? Example: SKX estimate EPS in the next 5Y is 27.28%. If the last EPS is 3, does it mean that in 5 years it'll be 3\*1.2728=3.8184 or  3*(1.2728)^5 =10.02?, comment_number: 3"}
  ]
)

print(response)




# system_message = (f"You are a highly intelligent AI assistant who provides sentiment analysis on stock market discussions.  You analyze the sentiment of entered reddit posts from financial subreddits,"
#                           f"and evlauate their relevance to the stock market.  You cross check the list of tickers which are provided with the actual post and ID what ticker is actually being discussed while ignoring misc. words.")
#         user_message = (f"Analyze the sentiment of the following Reddit post and its relevance "
#                         f"to the stock market. Identify the sentiment towards the mentioned stocks, "
#                         f"and ignore items in the ticker list that are just regular words used in the post. "
#                         f"Do however try to correctly ID the true tickers in tickerlist that are discussed in each post: "
#                         f"{', '.join(tickers)} if any.\n\nTitle: {post_title}\nBody: {post_body}")

#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": system_message},
#                 {"role": "user", "content": user_message}
#             ]
#         )


# class GptSentimentAnalysis:
#     def __init__(self, openai_api_key):
#         self.openai_api_key = openai_api_key
#         openai.api_key = self.openai_api_key

#     def sentiment_gpt(self, post_title, post_body, comment_body, subreddit,tickers):
#         system_message = (f"You are a highly intelligent AI assistant who provides sentiment analysis on stock market discussions from financial subreddits.x=  .  You analyze the sentiment of entered reddit posts from financial subreddits and evlauate their relevance to the stock market.  You cross check the list of tickers which are provided with the actual post and ID what ticker is actually being discussed while ignoring misc. words.")
        
#         user_message = (f"Analyze the sentiment of the following Reddit post and its relevance "
#                         f"to the stock market. Identify the sentiment towards the mentioned stocks, "
#                         f"and ignore items in the ticker list that are just regular words used in the post. "
#                         f"Do however try to correctly ID the true tickers in tickerlist that are discussed in each post: "
#                         f"{', '.join(tickers)} if any.\n\nTitle: {post_title}\nBody: {post_body} \ncomment_body:{comment_body}")

#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": system_message},
#                 {"role": "user", "content": user_message}
                
#             ]
#         )


#         print(response)



# class GptSentimentAnalysis:
#     def __init__(self, openai_api_key):
#         self.openai_api_key = openai_api_key
#         openai.api_key = self.openai_api_key

#     def sentiment_gpt(self, post_title, post_body, comment_body, subreddit,tickers):
#         system_message = (f"You are a highly intelligent AI assistant who provides sentiment analysis on stock market discussions from financial subreddits.x=  .  You analyze the sentiment of entered reddit posts from financial subreddits and evlauate their relevance to the stock market.  You cross check the list of tickers which are provided with the actual post and ID what ticker is actually being discussed while ignoring misc. words.")
        
#         user_message = (f"Analyze the sentiment of the following Reddit post and its relevance "
#                         f"to the stock market. Identify the sentiment towards the mentioned stocks, "
#                         f"and ignore items in the ticker list that are just regular words used in the post. "
#                         f"Do however try to correctly ID the true tickers in tickerlist that are discussed in each post: "
#                         f"{', '.join(tickers)} if any.\n\nTitle: {post_title}\nBody: {post_body} \ncomment_body:{comment_body}")

#         response = openai.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": system_message},
#                 {"role": "user", "content": user_message}
                
#             ]
#         )


#         print(response)
