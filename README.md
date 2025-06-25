# my_codex

This repository contains two small Python projects:

1. **TechCrunch AI Tweet Bot** - tweets recent articles from TechCrunch's AI feed.
2. **Canal Quantity App** (`canal_app/`) - a Streamlit demo that calculates canal section quantities.

## TechCrunch AI Tweet Bot

Install dependencies and run the Gradio interface to provide Twitter API keys.

```bash
pip install -r requirements.txt
python ai_news_tweet_bot.py
```

The script schedules tweets every day at **07:45**.

## Canal Quantity App

Navigate into `canal_app/` and install the app requirements:

```bash
pip install -r canal_app/requirements.txt
streamlit run canal_app/streamlit_app.py
```

A simple GUI lets you select a canal section, enter dimensions in millimeters, and see live calculations. The Dockerfile allows running with Docker:

```bash
docker build -t canal_app ./canal_app
docker run -p 8501:8501 canal_app
```

Enjoy experimenting with example values in metres (m), square metres (m²) and cubic metres (m³).
