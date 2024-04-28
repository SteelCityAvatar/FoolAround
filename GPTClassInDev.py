
import requests
import openai
from openai import OpenAI
import pandas as pd
import os
import json

# # Iterate through the dataframe and analyze sentiment
# for index, row in vh_slice.iterrows():
#     try:
#         print("_________________________")
#         print(row['post_title'])
#         print(row['post_body'])
#         print(row['relevant_tickers'])
#         print(row['comment_number'])
#         print(row['comment'])
#         print("_________________________")

#         sentiment_analysis = sentiment_analyzer.sentiment_gpt(row['post_title'], row['post_body'], row['relevant_tickers'])
#         vihp_df.at[index, 'sentiment_analysis'] = sentiment_analysis
#     except TypeError:
#          pass


class GptAnalysis:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key

    def get_system_message(self, message):
        if message == "":
            system_message = "You are a highly intelligent financial analyst.  Your job is to provide a sentiment analysis of all tickers that may be discussed in a entered Reddit post.*
        input("Enter your message: ")
    
        return system_message
    
    def get_user_message(self, message):
        return user_message
    
    def structure_message(self, system_message, user_message):
        return {"role": "system", "content": system_message}, {"role": "user", "content": user_message}
    
    def SendMessage(self, system_message, user_message):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        return response                       
    
    def structure_response(self, response):
        return response.choices[0].message['content']