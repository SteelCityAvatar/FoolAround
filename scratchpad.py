import re
dict11 = {
    "comment_date": "2024-04-28T15:20:28",
    "comment_body": "Does anyone else think Brk.b is too high to put in money right now? I am wondering if I should wait til it drops more or just say screw it. VOO is too high as well imo. I have been throwing in my money into KO lately though",
    "relevant_tickers": [
        "KO"
    ]
}

text = dict11['comment_body']
pattern =r'\b[A-Z]{2,5}(?:\.[A-Z]{2,})?\b'
found_tickers = set(re.findall(pattern, text))
found_tickers