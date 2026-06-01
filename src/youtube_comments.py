from googleapiclient.discovery import build
from textblob import TextBlob
from urllib.parse import urlparse, parse_qs
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

API_KEY = "AIzaSyBgx328Hz6y1lFxA9V27UWE7ppAwbKFpQM"

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

video_url = input("Paste YouTube URL: ")

video_id = parse_qs(
    urlparse(video_url).query
)["v"][0]

print(f"Video ID: {video_id}")

comments = []

request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=100,
    textFormat="plainText"
)

response = request.execute()

for item in response["items"]:
    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    comments.append(comment)

df = pd.DataFrame(
    comments,
    columns=["Comment"]
)

print(f"\nTotal Comments: {len(df)}")


def get_sentiment(text):

    score = TextBlob(text).sentiment.polarity

    if score > 0:
        return "Positive"

    elif score < 0:
        return "Negative"

    else:
        return "Neutral"


def sentiment_score(text):

    return TextBlob(text).sentiment.polarity


df["Sentiment"] = df["Comment"].apply(get_sentiment)
df["Score"] = df["Comment"].apply(sentiment_score)

print(df.head())

print("\nSentiment Summary")
print(df["Sentiment"].value_counts())

avg_score = round(df["Score"].mean(), 2)

print(f"\nAverage Score: {avg_score}")

sentiment_counts = df["Sentiment"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct="%1.1f%%"
)
plt.title("YouTube Sentiment Analysis")
plt.show()

plt.figure(figsize=(8, 5))
sentiment_counts.plot(kind="bar")
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.show()

text = " ".join(df["Comment"])

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white"
).generate(text)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Most Used Words")
plt.show()

df.to_csv(
    "youtube_sentiment_analysis.csv",
    index=False
)

print("\nReport Saved Successfully")