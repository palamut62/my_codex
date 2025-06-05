# TechCrunch AI Tweet Bot

This repository contains a simple Python script that tweets recent articles from TechCrunch's Artificial Intelligence section. The script reads the last 16 hours of posts from the RSS feed and tweets them every day at **07:45**.

## Requirements

- Python 3
- `feedparser` for parsing RSS feeds
- `schedule` for scheduling tasks
- `tweepy` for interacting with the Twitter API
- `pytz` for timezone handling

Install dependencies with:

```bash
pip install -r requirements.txt
```

Set the following environment variables with your Twitter API credentials:

- `TWITTER_CONSUMER_KEY`
- `TWITTER_CONSUMER_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

## Running

Execute the script and keep it running to tweet new AI-related articles every morning:

```bash
python ai_news_tweet_bot.py
```

The script will stay alive and check for scheduled tasks once per minute.
