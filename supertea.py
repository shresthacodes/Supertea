import telebot
import requests

from api_key import api_key
from news_api_key import NEWS_API_KEY

NEWS_API_ENDPOINT = 'https://newsapi.org/v2/top-headlines'
NEWS_API_PARAMS = {
    'country': 'us', 'india'
    'category': 'entertainment',
    'apiKey': NEWS_API_KEY
}

bot = telebot.TeleBot(api_key)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Ask me for the latest celebrity news!")


@bot.message_handler()
def send_celebrity_news(message):
    reply = "Sorry, couldn't fetch the latest celebrity news at the moment."
    try:
        response = requests.get(NEWS_API_ENDPOINT, params=NEWS_API_PARAMS)
        data = response.json()

        if response.status_code == 200 and data['status'] == 'ok':
            articles = data['articles']
            if articles:
                reply = "Latest Celebrity News:\n"
                for article in articles:
                    title = article.get('title', 'N/A')
                    description = article.get('description', 'N/A')
                    url = article.get('url', '#')

                    reply += f"\nTitle: {title}\nDescription: {description}\nURL: {url}\n{'='*30}\n"
    except Exception as e:
        print(f"Error: {e}")

    finally:
        bot.reply_to(message, reply)


print("Loading...")
bot.infinity_polling()
print("Stopped")
