# my_codex
# TechCrunch AI Tweet Bot

This repository contains a simple Python script that tweets recent articles from TechCrunch's Artificial Intelligence section. The script reads the last 16 hours of posts from the RSS feed and tweets them every day at **07:45**. A small Gradio web interface is provided so you can supply your Twitter API credentials directly in the browser and start the bot.

## Requirements

- Python 3
- `feedparser` for parsing RSS feeds
- `schedule` for scheduling tasks
- `tweepy` for interacting with the Twitter API
- `pytz` for timezone handling
- `gradio` for the web interface

Install dependencies with:

```bash
pip install -r requirements.txt
```

You can optionally set the following environment variables with your Twitter API credentials if you prefer running the script without the web UI:

- `TWITTER_CONSUMER_KEY`
- `TWITTER_CONSUMER_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

## Running

Run the script to open the Gradio interface. Provide your keys and click "Submit" to start the scheduled tweets:

```bash
python ai_news_tweet_bot.py
```

The script will stay alive and check for scheduled tasks once per minute.