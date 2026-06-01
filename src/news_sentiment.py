import requests
import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud
API_KEY = "c929245c59f44316991075e354f9069b"

url = (
    f"https://newsapi.org/v2/top-headlines?"
    f"country=us&apiKey={API_KEY}"
)

response = requests.get(url)

data = response.json()

articles = []

for article in data["articles"]:

    title = article["title"]

    articles.append(title)

df = pd.DataFrame(
    articles,
    columns=["Headline"]
)

def get_sentiment(text):

    score = TextBlob(text).sentiment.polarity

    if score > 0:
        return "Positive"

    elif score < 0:
        return "Negative"

    else:
        return "Neutral"

df["Sentiment"] = df["Headline"].apply(
    get_sentiment
)

print(df.head())

print("\nSentiment Summary")

print(
    df["Sentiment"].value_counts()
)
total_news = len(df)

positive_count = len(
    df[df["Sentiment"] == "Positive"]
)

neutral_count = len(
    df[df["Sentiment"] == "Neutral"]
)

negative_count = len(
    df[df["Sentiment"] == "Negative"]
)

print("\nKPI Summary")

print(f"Total News     : {total_news}")
print(f"Positive News  : {positive_count}")
print(f"Neutral News   : {neutral_count}")
print(f"Negative News  : {negative_count}")

import matplotlib.pyplot as plt

sentiment_counts = df["Sentiment"].value_counts()

plt.figure(figsize=(6,6))

plt.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct="%1.1f%%"
)

plt.title(
    "News Sentiment Distribution"
)

plt.show()

plt.figure(figsize=(8,5))

sentiment_counts.plot(
    kind="bar"
)

plt.title(
    "News Sentiment Count"
)

plt.xlabel("Sentiment")
plt.ylabel("Count")

plt.show()

text = " ".join(
    df["Headline"]
)

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white"
).generate(text)

plt.figure(figsize=(12,6))

plt.imshow(wordcloud)

plt.axis("off")

plt.title(
    "Most Frequent News Words"
)

plt.show()