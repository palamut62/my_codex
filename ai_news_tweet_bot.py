import feedparser
import schedule
import tweepy
import time
from datetime import datetime, timedelta
import pytz
import threading
import gradio as gr

FEED_URL = "https://techcrunch.com/category/artificial-intelligence/feed/"


def fetch_recent_articles(hours=16):
    feed = feedparser.parse(FEED_URL)
    threshold = datetime.now(pytz.utc) - timedelta(hours=hours)
    articles = []
    for entry in feed.entries:
        if hasattr(entry, "published_parsed"):
            pub_time = datetime(*entry.published_parsed[:6], tzinfo=pytz.utc)
            if pub_time > threshold:
                articles.append({"title": entry.title, "link": entry.link})
    return articles


def tweet_articles(consumer_key, consumer_secret, access_token, access_secret):
    articles = fetch_recent_articles()
    if not articles:
        print("No new articles to tweet.")
        return

    auth = tweepy.OAuth1UserHandler(
        consumer_key,
        consumer_secret,
        access_token,
        access_secret,
    )
    api = tweepy.API(auth)

    for article in articles:
        tweet_text = f"{article['title']} {article['link']}"
        try:
            api.update_status(status=tweet_text)
            print(f"Tweeted: {tweet_text}")
        except Exception as e:
            print(f"Failed to tweet {tweet_text}: {e}")


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)


def schedule_tweets(consumer_key, consumer_secret, access_token, access_secret):
    schedule.clear()
    schedule.every().day.at("07:45").do(
        tweet_articles, consumer_key, consumer_secret, access_token, access_secret
    )
    threading.Thread(target=run_scheduler, daemon=True).start()


def start_bot(consumer_key, consumer_secret, access_token, access_secret):
    schedule_tweets(consumer_key, consumer_secret, access_token, access_secret)
    return "Bot scheduled to tweet daily at 07:45"


iface = gr.Interface(
    fn=start_bot,
    inputs=[
        gr.Textbox(label="Consumer Key"),
        gr.Textbox(label="Consumer Secret"),
        gr.Textbox(label="Access Token"),
        gr.Textbox(label="Access Secret"),
    ],
    outputs="text",
    title="TechCrunch AI Tweet Bot",
    description=(
        "Enter your Twitter API credentials and launch the bot. It will tweet "
        "recent AI articles from TechCrunch every day at 07:45."
    ),
)


if __name__ == "__main__":
    iface.launch()
