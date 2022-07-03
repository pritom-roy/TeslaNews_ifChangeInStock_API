import os
import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

stock_data = requests.get(url=STOCK_ENDPOINT, params=parameter).json()["Time Series (Daily)"]
stock_data = list(stock_data.items())
today_value = float(stock_data[0][1]["4. close"])
yesterday_value = float(stock_data[1][1]["4. close"])

value_increased_percent = round(100 * (abs(yesterday_value - today_value) / yesterday_value))

if value_increased_percent >= 5 or value_increased_percent <= -5:
    if value_increased_percent > 0:
        symbol = "🔺"
    else:
        symbol = "🔻"

    news_parameter = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_data = requests.get(url=NEWS_ENDPOINT, params=news_parameter).json()
    article_data = news_data["articles"]

    article_number = int(news_data["totalResults"])
    if article_number < 4:
        article = article_data[:article_number]
    else:
        article = news_data[:3]

    formatted_article = [
        f"{COMPANY_NAME} {symbol}by {value_increased_percent}%\nHeadline: {item['title']}\n\nDescription: {item['description']}"
        for item in article]

    print(formatted_article)
    account_sid = os.environ['ACCOUNT_SID']
    auth_token = os.environ['AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    for item in formatted_article:
        message = client.messages \
            .create(
            body=item,
            from_='+18508018265',
            to='+8801732792640'
        )

        print(message.sid)
