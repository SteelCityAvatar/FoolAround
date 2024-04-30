import re
dict11 =            {
    "comment_date": "2024-04-29T10:59:03",
    "comment_body": "There are many answers to that question.  Most are answered based on your overall financial standing in regards to when you want/need to stop working.  For just a get-going portfolio that will help answer retirement questions down the line, I prefer a mix of overall market indexes like VOO (50%), DGRO (10%), SPDW (20%), SPEM (10%), and then the final 10% in a money market to build cash to buy favorite stocks when the market (VOO) drops more than 3% in a day.  Buying on dips with cash is always a good long term feeling.",
    "relevant_tickers": []
}

text = dict11['comment_body']
pattern = r'\b[A-Za-z]{1,5}(?:\.[A-Za-z]+)?\b'
patturn = r'\b[A-Z]{2,5}(?:\.[A-Za-z]+)?\b'
pattirn = r'\b[A-Z]{2,5}(?:\.[A-Za-z]+)?\b'

found_tickers = set(re.findall(pattern, text))
print(found_tickers)

found_tickers = set(re.findall(patturn, text))
print(found_tickers)

found_tickers = set(re.findall(pattirn, text))
print(found_tickers)


