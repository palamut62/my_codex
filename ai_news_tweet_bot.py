import os
import feedparser
import schedule
import tweepy
import time
from datetime import datetime, timedelta
import pytz

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


def tweet_articles():
    articles = fetch_recent_articles()
    if not articles:
        print("No new articles to tweet.")
        return

    auth = tweepy.OAuth1UserHandler(
        os.environ.get("TWITTER_CONSUMER_KEY"),
        os.environ.get("TWITTER_CONSUMER_SECRET"),
        os.environ.get("TWITTER_ACCESS_TOKEN"),
        os.environ.get("TWITTER_ACCESS_SECRET"),
    )
    api = tweepy.API(auth)

    for article in articles:
        tweet_text = f"{article['title']} {article['link']}"
        try:
            api.update_status(status=tweet_text)
            print(f"Tweeted: {tweet_text}")
        except Exception as e:
            print(f"Failed to tweet {tweet_text}: {e}")


def schedule_tweets():
    schedule.every().day.at("07:45").do(tweet_articles)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    schedule_tweets()
