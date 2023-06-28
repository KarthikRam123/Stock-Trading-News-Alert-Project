#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install twilio


# In[2]:


import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "+14849897759"
VERIFIED_NUMBER = "+919167954709"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query?"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "7KAS0ST1V8ZOPQDS"
NEWS_API_KEY = "d4c97f1f9e154092a19003960713ad2f"
TWILIO_SID = "AC05ad426eb0f445f275c3924f6a041dd7"
TWILIO_AUTH_TOKEN = "219366a2486943aebea98a753d7f4f58"

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_WEEKLY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)

response.raise_for_status()

print(response.json())


# In[3]:


import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "+14849897759"
VERIFIED_NUMBER = "+919167954709"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "7KAS0ST1V8ZOPQDS"
NEWS_API_KEY = "d4c97f1f9e154092a19003960713ad2f"
TWILIO_SID = "AC05ad426eb0f445f275c3924f6a041dd7"
TWILIO_AUTH_TOKEN = "219366a2486943aebea98a753d7f4f58"

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_WEEKLY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)

data = response.json()['Weekly Time Series']



data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(yesterday_closing_price) -     float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)


# Instead of printing ("Get News"), using the News API to get articles related to the COMPANY_NAME.
# If difference percentage is greater than 5 then print("Get News").
if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # Using Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]
    print(three_articles)

    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
    # Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Sending each article as a separate message via Twilio.
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )

